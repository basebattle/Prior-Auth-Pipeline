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

    # Sample Data Loader
    if st.button("Load Sample Orthopedic PA"):
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

    # Form Structure
    with st.form("pa_request_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Patient Info")
            patient_id = st.text_input("Patient ID", value=st.session_state.get("patient_id", ""))
            patient_name = st.text_input("Name", value=st.session_state.get("patient_name", ""))
            patient_dob = st.text_input("DOB (YYYY-MM-DD)", value=st.session_state.get("patient_dob", ""))
            payer_name = st.selectbox("Payer", SUPPORTED_PAYERS, index=SUPPORTED_PAYERS.index(st.session_state.get("payer_name", "UnitedHealthcare")))

        with col2:
            st.subheader("Procedure Info")
            procedure_code = st.text_input("Procedure Code (CPT/HCPCS)", value=st.session_state.get("procedure_code", ""))
            diagnosis_codes = st.text_area("ICD-10 Diagnosis Codes (comma separated)", value=", ".join(st.session_state.get("diagnosis_codes", [])))
            requesting_provider_npi = st.text_input("Provider NPI", value=st.session_state.get("requesting_provider_npi", ""))
            urgency = st.radio("Urgency", ["standard", "urgent"], horizontal=True)

        st.subheader("Clinical Justification")
        
        # Phase 3: Advanced Input
        tabs = st.tabs(["📝 Manual Entry", "📄 OCR Upload", "🎤 Voice-to-PA"])
        
        with tabs[0]:
            clinical_notes = st.text_area("Notes", value=st.session_state.get("clinical_notes", ""), height=200)

        with tabs[1]:
            uploaded_docs = st.file_uploader("Upload clinical records (PDF/JPG)", accept_multiple_files=True)
            if uploaded_docs:
                if st.button("Extract Clinical Evidence"):
                    extracted_texts = []
                    for doc in uploaded_docs:
                        with st.spinner(f"Processsing {doc.name}..."):
                            text = ocr_tool.process_document(doc.read(), doc.name)
                            extracted_texts.append(f"--- {doc.name} ---\n{text}")
                    st.success("Extraction Complete.")
                    clinical_notes = "\n\n".join(extracted_texts)
                    st.session_state["clinical_notes"] = clinical_notes
                    st.rerun()

        with tabs[2]:
            st.info("Direct audio recording (Simulated)")
            if st.button("🎤 Record Clinical Summary"):
                with st.spinner("Transcribing..."):
                    transcription = voice_tool.transcribe_audio(b"dummy")
                    st.success("Transcription Complete.")
                    st.session_state["clinical_notes"] = transcription
                    st.rerun()

        submitted = st.form_submit_button("Submit PA Request ▶")

    if submitted:
        try:
            # 1. Validate data
            request_data = PARequestInput(
                patient_id=patient_id,
                patient_name=patient_name,
                patient_dob=patient_dob,
                payer_name=payer_name,
                procedure_code=procedure_code,
                diagnosis_codes=[d.strip() for d in diagnosis_codes.split(",")],
                requesting_provider_npi=requesting_provider_npi,
                clinical_notes=clinical_notes,
                urgency=urgency
            )

            # 2. Call service (async logic)
            with st.spinner("Processing through Agent Pipeline..."):
                request_id = asyncio.run(pa_service.submit_request(request_data))
                st.success(f"PA-2026-{request_id[:4]} submitted successfully!")
                st.info("Navigate to 'Pipeline Visualizer' to see agent progress.")
                st.session_state["last_request_id"] = request_id

        except Exception as e:
            st.error(f"Form validation error: {e}")
