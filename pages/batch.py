import streamlit as st
import pandas as pd
import asyncio
import time
from services.pa_service import pa_service
from data.schemas import PARequestInput

def show():
    st.title("📦 Batch Processing")
    st.markdown("---")

    # Upload interface
    uploaded_file = st.file_uploader("Upload CSV of Prior Auth Requests", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("CSV Validation (Preview)")
        st.dataframe(df.head(), use_container_width=True)

        if st.button("Start Batch Processing ▶"):
            with st.spinner("Processing batch..."):
                results = []
                # Simple loop for batch
                for index, row in df.iterrows():
                    try:
                        # 1. Transform to schema
                        request_data = PARequestInput(
                            patient_id=row.get("patient_id", f"P{index}"),
                            patient_name=row.get("patient_name", f"Patient {index}"),
                            patient_dob=row.get("patient_dob", "1965-03-15"),
                            payer_name=row.get("payer_name", "UnitedHealthcare"),
                            procedure_code=str(row.get("procedure_code", "27447")),
                            diagnosis_codes=str(row.get("diagnosis_codes", "M17.11")).split(","),
                            requesting_provider_npi=str(row.get("provider_npi", "1234567890")),
                            clinical_notes=row.get("clinical_notes", ""),
                            urgency="standard"
                        )

                        # 2. Call service (Sync call is safer)
                        pa_service.submit_request_sync(request_data)
                        st.info(f"Processing {index+1}/{len(df)}: {row.get('patient_name')}")
                        
                    except Exception as e:
                        st.error(f"Error on row {index}: {e}")
                
            st.success(f"Batch Processing Complete for {len(df)} requests.")
            st.info("Check 'History' for processing status.")

    # Template download
    st.markdown("---")
    st.subheader("Batch Template")
    template_df = pd.DataFrame([
        {
            "patient_id": "P1234",
            "patient_name": "John Doe",
            "patient_dob": "1970-01-01",
            "payer_name": "Aetna",
            "procedure_code": "27447",
            "diagnosis_codes": "M17.11,M17.12",
            "provider_npi": "1234567890",
            "clinical_notes": "Clinical justification here..."
        }
    ])
    st.download_button("Download CSV Template", template_df.to_csv(index=False), file_name="pa_batch_template.csv")
