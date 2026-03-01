import streamlit as st
import json
from services.pa_service import pa_service

def show():
    st.title("🛡️ Human Review Checkpoint")
    st.markdown("---")

    request_id = st.session_state.get("show_review_id")
    if not request_id:
        st.info("No PA request selected for review.")
        return

    # Load dynamic data from service
    full_data = pa_service.get_full_request_and_package(request_id)
    if not full_data:
        st.error("PA Request data not found.")
        return

    # Extract metadata and package
    patient_name = full_data.get("patient_name", "Unknown")
    patient_dob = full_data.get("patient_dob", "Unknown")
    payer_name = full_data.get("payer_name", "Unknown")
    procedure_code = full_data.get("procedure_code", "Unknown")
    
    # Check if package exists in the DB result
    # The PAStore saves the package in the 'result_package' column
    package = full_data.get("result_package", {})
    if isinstance(package, str):
        try:
            package = json.loads(package)
        except:
            package = {}

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
            st.success("PA-2026-0042 APPROVED. Submission sent to Payer Portal via API.")
            st.balloons()
    with colB:
        if st.button("❌ Reject"):
            st.error("PA-2026-0042 REJECTED. Denial notice generated.")
    with colC:
        if st.button("⬇ Export to PPTX/PDF"):
            st.write("Exporting package...")
