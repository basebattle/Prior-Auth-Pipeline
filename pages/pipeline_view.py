import streamlit as st
import time
from services.pa_service import pa_service
from components.agent_step import show_agent_step

def show():
    # 🛠️ Step 3: Module Sync (Pipeline Visualizer)
    st.title("🔄 Pipeline Visualizer")
    st.markdown("---")

    # Selection Logic from session_state
    current_request_id = st.session_state.get("last_request_id") or st.session_state.get("app_state", {}).get("last_request_id")
    
    if not current_request_id:
        st.warning("⚠️ No Data Found: No active PA request in pipeline.")
        st.info("Please submit a request through 'New PA Request' or select a historical case from 'History'.")
        return

    st.subheader(f"Analyzing PA-2026-{current_request_id[:8]}")
    
    # In V2, we actually fetch the request from the DB to see if processing is complete
    request_data = pa_service.get_full_request_and_package(current_request_id)
    
    if not request_data:
        st.error("Error: Case file not found in database.")
        return

    # Pipeline status visualizer
    status = request_data.get("status", "pending")
    
    # Display steps (Simulated visual for V1-V2 transition)
    show_agent_step("Triage Agent", "complete", "3.2s", "Classified as SURGICAL (Standard)")
    show_agent_step("Clinical Validation Agent", "complete", "12.8s", "Medical necessity criteria identified (Medicare NCD 150.6)")
    show_agent_step("NPI Verification Agent", "complete", "2.1s", "NPI active. Specialty MATCH (Orthopedic Surgery)")
    show_agent_step("Medical Necessity Agent", "complete", "35.5s", "Evidence extracted: Failed 6m PT, imaging results match GRADE IV OA.")
    show_agent_step("Denial Risk Agent", "complete", "4.2s", "Risk Assessment Complete. Level: LOW.")
    show_agent_step("Decision Synthesis Agent", "complete" if status == 'complete' else 'running', "1.5s", "Final PA Package Compiled. Confidence Score: 0.87")
    
    if status == 'complete' or status == 'processed':
        st.success("✅ AI Analysis Complete")
        if st.button("🛡️ Open Human Review Checkpoint ▶"):
            st.session_state["show_review_id"] = current_request_id
            st.session_state["app_state"]["show_review_id"] = current_request_id
            st.rerun() # Ensure app updates to show Review page if radio button selection is updated or handle routing.
    else:
        st.info("🕒 Agent Processing Loop in Progress...")
