import streamlit as st
import time
from services.pa_service import pa_service
from components.agent_step import show_agent_step

def show():
    st.title("🔄 Pipeline Visualizer")
    st.markdown("---")

    # Selection Logic
    last_id = st.session_state.get("last_request_id")
    if last_id:
        st.subheader(f"Analyzing PA-2026-{last_id[:4]}")
        
        # Simulated sequence for demonstration (V1 is synchronous for now)
        # But in a production version, we'd poll the DB.
        
        show_agent_step("Triage Agent", "complete", "3.2s", "Classified as SURGICAL (Standard)")
        show_agent_step("Clinical Validation Agent", "complete", "12.8s", "Medical necessity criteria identified (Medicare NCD 150.6)")
        show_agent_step("NPI Verification Agent", "complete", "2.1s", "NPI active. Specialty MATCH (Orthopedic Surgery)")
        show_agent_step("Medical Necessity Agent", "complete", "35.5s", "Evidence extracted: Failed 6m PT, imaging results match GRADE IV OA.")
        show_agent_step("Denial Risk Agent", "complete", "4.2s", "Risk Assessment Complete. Level: LOW.")
        show_agent_step("Decision Synthesis Agent", "complete", "1.5s", "Final PA Package Compiled. Confidence Score: 0.87")
        
        st.success("PA Package Ready for Review!")
        if st.button("Open Human Review Checkpoint ▶"):
            st.session_state["show_review_id"] = last_id
            # redirect handled in main app logic or simple conditional here
            from pages import review
            review.show()
    else:
        st.info("No active PA request in pipeline. Submit one through 'New PA Request'.")
