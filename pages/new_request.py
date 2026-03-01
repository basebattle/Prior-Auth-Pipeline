import streamlit as st
import json
import asyncio
from datetime import datetime
from data.schemas import PARequestInput
from services.pa_service import pa_service
from config.constants import SUPPORTED_PAYERS
from utils.ocr import ocr_tool
from utils.voice import voice_tool

def show():
    st.title("📄 New Prior Authorization Request")
    st.markdown("---")

    # 🛠️ Step 2: Form Fix (Encapsulated State Handling)
    # Initialize page-specific state if not existing
    if "clinical_notes" not in st.session_state:
        st.session_state["clinical_notes"] = ""

    # Sample Data Loader (Outside form)
    if st.button("🚀 Load Sample Orthopedic PA"):
        from data import synthetic_generator
        scenario = synthetic_generator.SCENARIOS[0] # TKR
        st.session_state["patient_id"] = "P1001"
        st.session_state["patient_name"] = "John Smith"
        st.session_state["patient_dob"] = "1965-03-15"
        st.session_state["payer_name"] = "UnitedHealthcare"
        st.session_state["procedure_code"] = scenario["procedure_code"]
        st.session_state["diagnosis_codes"] = scenario["diagnosis_codes"]
        st.session_state["requesting_provider_npi"] = "1234567890"
        st.session_state["clinical_notes"] = scenario["notes"]
        st.rerun()

    # Form Structure
    with st.form("pa_request_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Patient Info")
            patient_id = st.text_input("Patient ID", value=st.session_state.get("patient_id", ""))
            patient_name = st.text_input("Name", value=st.session_state.get("patient_name", ""))
            patient_dob = st.text_input("DOB (YYYY-MM-DD)", value=st.session_state.get("patient_dob", ""))
            
            # Safe index lookup for Payer selectbox
            default_payer = st.session_state.get("payer_name", "UnitedHealthcare")
            payer_index = SUPPORTED_PAYERS.index(default_payer) if default_payer in SUPPORTED_PAYERS else 0
            payer_name = st.selectbox("Payer", SUPPORTED_PAYERS, index=payer_index)

        with col2:
            st.subheader("Procedure Info")
            procedure_code = st.text_input("Procedure Code (CPT/HCPCS)", value=st.session_state.get("procedure_code", ""))
            
            diag_val = st.session_state.get("diagnosis_codes", [])
            if isinstance(diag_val, list):
                diag_str = ", ".join(diag_val)
            else:
                diag_str = diag_val
                
            diagnosis_codes_input = st.text_area("ICD-10 Diagnosis Codes (comma separated)", value=diag_str)
            requesting_provider_npi = st.text_input("Provider NPI", value=st.session_state.get("requesting_provider_npi", ""))
            urgency = st.radio("Urgency", ["standard", "urgent"], horizontal=True)

        st.subheader("Clinical Justification")
        
        # Phase 3: Advanced Input
        tabs = st.tabs(["📝 Manual Entry", "📄 OCR Upload", "🎤 Voice-to-PA"])
        
        with tabs[0]:
            # Always sync this back to state on change
            clinical_notes = st.text_area("Notes", value=st.session_state.get("clinical_notes", ""), height=200, key="manual_notes")

        with tabs[1]:
            uploaded_docs = st.file_uploader("Upload clinical records (PDF/JPG)", accept_multiple_files=True)
            ocr_trigger = st.form_submit_button("🔍 Extract Clinical Evidence")
            if ocr_trigger and uploaded_docs:
                extracted_texts = []
                for doc in uploaded_docs:
                    with st.spinner(f"Processing {doc.name}..."):
                        text = ocr_tool.process_document(doc.read(), doc.name)
                        extracted_texts.append(f"--- {doc.name} ---\n{text}")
                st.session_state["clinical_notes"] = "\n\n".join(extracted_texts)
                st.success("Extraction Complete. Click 'Submit PA Request' to proceed.")
                st.rerun()

        with tabs[2]:
            st.info("Direct audio recording (Simulated)")
            voice_trigger = st.form_submit_button("🎤 Record Clinical Summary")
            if voice_trigger:
                with st.spinner("Transcribing..."):
                    transcription = voice_tool.transcribe_audio(b"dummy")
                    st.session_state["clinical_notes"] = transcription
                    st.success("Transcription Complete. Click 'Submit PA Request' to proceed.")
                    st.rerun()

        submitted = st.form_submit_button("✅ Submit PA Request ▶")

    if submitted:
        # Use simple manual entry notes if others weren't triggered
        final_notes = st.session_state.get("clinical_notes") if st.session_state.get("clinical_notes") else clinical_notes
        
        if not patient_id or not procedure_code:
            st.error("Missing Data: Please ensure Patient ID and Procedure Code are provided.")
            return

        try:
            # 1. Validate data
            request_data = PARequestInput(
                patient_id=patient_id,
                patient_name=patient_name,
                patient_dob=patient_dob,
                payer_name=payer_name,
                procedure_code=procedure_code,
                diagnosis_codes=[d.strip() for d in diagnosis_codes_input.split(",") if d.strip()],
                requesting_provider_npi=requesting_provider_npi,
                clinical_notes=final_notes,
                urgency=urgency
            )

            # 2. Call service (Synchronous for Streamlit stability)
            with st.spinner("Processing through Agent Pipeline (60-90s)..."):
                request_id = pa_service.submit_request_sync(request_data)
                
                # Update global state for other pages
                st.session_state["last_request_id"] = request_id
                st.session_state["app_state"]["last_request_id"] = request_id
                
                st.success(f"Successfully Submitted! (ID: {request_id[:8]})")
                st.balloons()
                st.info("Navigate to 'Pipeline Visualizer' to see agent logic.")

        except Exception as e:
            st.error(f"Form Error: {e}")
