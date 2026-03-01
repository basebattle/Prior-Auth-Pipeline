import streamlit as st
import json
from services.pa_service import pa_service

def show():
    st.title("🛡️ Human Review Checkpoint")
    st.markdown("---")

    # 🛠️ State Check Pattern
    request_id = st.session_state.get("show_review_id") or st.session_state.get("app_state", {}).get("show_review_id")
    
    if not request_id:
        st.warning("⚠️ No Data Found: No PA request selected for human review.")
        st.info("Check 'Pipeline Visualizer' after a submission or select a case from 'History'.")
        return

    # Load dynamic data from service
    full_data = pa_service.get_full_request_and_package(request_id)
    if not full_data:
        st.error("🚨 Error Retrieval: Case data missing from database.")
        if st.button("Reset Selection"):
            st.session_state["show_review_id"] = None
            st.rerun()
        return

    # Extract metadata and package
    patient_name = full_data.get("patient_name", "Unknown")
    payer_name = full_data.get("payer_name", "Unknown")
    procedure_code = full_data.get("procedure_code", "Unknown")
    
    package = full_data.get("result_package", {})
    # If package is missing but record exists
    if not package:
        st.info("Processing still in progress. Please wait for Decision Synthesis.")
        return

    score = package.get("confidence_score", 0.0)
    risk_level = package.get("risk_level", "Unknown")
    recommendation = package.get("recommendation", "human_review")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Confidence Score")
        st.metric("Score", f"{score:.2f}", f"Recommend: {recommendation.upper()}")
        st.progress(score)

    with col2:
        st.subheader("Denial Risk")
        status_color = "🟢" if risk_level == "low" else "🟡" if risk_level == "medium" else "🔴"
        st.info(f"{status_color} {risk_level.upper()} (Based on historical factors)")

    st.markdown("---")

    # Final Package View
    st.subheader("PA SUBMISSION PACKAGE")
    with st.expander("COVER SHEET", expanded=True):
        st.markdown(package.get("cover_sheet", f"**Patient:** {patient_name}\n**Payer:** {payer_name}\n**Procedure:** {procedure_code}"))

    with st.expander("MEDICAL NECESSITY ARGUMENT", expanded=True):
        st.markdown(package.get("medical_necessity_argument", "No argument generated."))

    with st.expander("DOCUMENTATION CHECKLIST"):
        checklist = package.get("documentation_checklist", [])
        if checklist:
            for item in checklist:
                st.checkbox(item.get("item", "Evidence"), value=(item.get("status") == "present"), disabled=True)
        else:
            st.write("No checklist items generated.")

    # Decisions
    st.markdown("---")
    st.text_area("Reviewer Notes (Optional)")
    
    colA, colB, colC = st.columns([1,1,3])
    with colA:
        if st.button("✅ Approve & Submit"):
            st.success(f"PA-{request_id[:4]} APPROVED. Submission triggered.")
            st.balloons()
            st.session_state["pipeline_status"] = "Submitted"
    with colB:
        if st.button("❌ Reject"):
            st.error(f"PA-{request_id[:4]} REJECTED. Denial notice generated.")
            st.session_state["pipeline_status"] = "Rejected"
    with colC:
        if st.button("⬇ Export to PPTX/PDF"):
            st.write("Exporting package...")
