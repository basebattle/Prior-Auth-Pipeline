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
    # 🛠️ White-Box Audit: Unified state handler
    if "submission_success" not in st.session_state:
        st.session_state["submission_success"] = False

    st.title("📄 New Prior Authorization Request")
    st.markdown("---")

    # Sample Data Loader (Always outside form to trigger reruns correctly)
    if st.button("🚀 Load Sample Orthopedic PA"):
        from data import synthetic_generator
        scenario = synthetic_generator.SCENARIOS[0] # TKR
        st.session_state["patient_id"] = "P1001"
        st.session_state["patient_name"] = "John Smith"
        st.session_state["patient_dob"] = "1965-03-15"
        st.session_state["payer_name"] = "UnitedHealthcare"
        st.session_state["procedure_code"] = scenario["procedure_code"]
        st.session_state["diagnosis_codes"] = scenario["diagnosis_codes"]
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
            
            payer_val = st.session_state.get("payer_name", "UnitedHealthcare")
            payer_index = SUPPORTED_PAYERS.index(payer_val) if payer_val in SUPPORTED_PAYERS else 0
            payer_name = st.selectbox("Payer", SUPPORTED_PAYERS, index=payer_index)

        with col2:
            st.subheader("Procedure Info")
            procedure_code = st.text_input("Procedure Code", value=st.session_state.get("procedure_code", ""))
            
            diag_val = st.session_state.get("diagnosis_codes", [])
            diag_str = ", ".join(diag_val) if isinstance(diag_val, list) else str(diag_val)
            diagnosis_codes_input = st.text_area("ICD-10 (comma separated)", value=diag_str)
            
            requesting_provider_npi = st.text_input("Provider NPI", value=st.session_state.get("requesting_provider_npi", ""))
            urgency = st.radio("Urgency", ["standard", "urgent"], horizontal=True)

        st.subheader("Clinical Justification")
        tabs = st.tabs(["📝 Manual Entry", "📄 OCR Upload", "🎤 Voice-to-PA"])
        
        with tabs[0]:
            clinical_notes = st.text_area("Notes", value=st.session_state.get("clinical_notes", ""), height=200, key="manual_notes")

        with tabs[1]:
            uploaded_docs = st.file_uploader("Upload records (PDF/JPG)", accept_multiple_files=True)
            ocr_trigger = st.form_submit_button("🔍 Extract Clinical Evidence")
            if ocr_trigger and uploaded_docs:
                extracted_texts = []
                for doc in uploaded_docs:
                    with st.spinner(f"Extracting {doc.name}..."):
                        text = ocr_tool.process_document(doc.read(), doc.name)
                        extracted_texts.append(f"--- {doc.name} ---\n{text}")
                st.session_state["clinical_notes"] = "\n\n".join(extracted_texts)
                st.success("Extracted! Click 'Submit' to process.")
                st.rerun()

        with tabs[2]:
            st.info("Direct audio recording (Simulated)")
            voice_trigger = st.form_submit_button("🎤 Record Clinical Summary")
            if voice_trigger:
                with st.spinner("Transcribing..."):
                    transcription = voice_tool.transcribe_audio(b"dummy")
                    st.session_state["clinical_notes"] = transcription
                    st.success("Transcribed! Click 'Submit' to process.")
                    st.rerun()

        submitted = st.form_submit_button("✅ Submit PA Request ▶")

    if submitted:
        if not patient_id or not procedure_code:
            st.error("Submission Failed: Patient ID and Procedure Code are mandatory.")
            return

        try:
            # 1. Prepare Payload
            request_data = PARequestInput(
                patient_id=patient_id,
                patient_name=patient_name,
                patient_dob=patient_dob,
                payer_name=payer_name,
                procedure_code=procedure_code,
                diagnosis_codes=[d.strip() for d in diagnosis_codes_input.split(",") if d.strip()],
                requesting_provider_npi=requesting_provider_npi,
                clinical_notes=st.session_state.get("clinical_notes") or clinical_notes,
                urgency=urgency
            )

            # 2. Synchronous Execution for UI Stability
            with st.spinner("🤖 Agents working... (Estimated 45-60s)"):
                request_id = pa_service.submit_request_sync(request_data)
                
                # Critical: Populate session state for transition
                st.session_state["last_request_id"] = request_id
                st.session_state["app_state"]["last_request_id"] = request_id
                st.session_state["submission_success"] = True
                
                st.success(f"Success! PA Request ID: {request_id[:8]}")
                st.balloons()
                
                # Auto-Navigation Trigger
                st.session_state["active_page"] = "Pipeline Visualizer"
                st.rerun()

        except Exception as e:
            st.error(f"Logic Error: {e}")
