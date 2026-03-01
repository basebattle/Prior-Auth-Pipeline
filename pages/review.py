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

    # Visual Score Indicators
    package = st.session_state.get("current_package")
    score = package.get("confidence_score", 0.87) if package else 0.87
    risk_level = package.get("risk_level", "LOW") if package else "LOW"
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Confidence Score")
        st.metric("Score", f"{score:.2f}", "High (Recommend: AUTO-APPROVE)" if score > 0.8 else "Moderate")
        st.progress(score)

    with col2:
        st.subheader("Denial Risk")
        st.info(f"🟢 {risk_level.upper()} (Based on historical factors)")

    st.markdown("---")

    # Final Package View
    st.subheader("PA SUBMISSION PACKAGE")
    with st.expander("COVER SHEET", expanded=True):
        st.markdown("""
        **Patient:** John Smith (DOB: 1965-03-15)
        **Payer:** UnitedHealthcare | Choice Plus PPO
        **Procedure:** 27447 - Total Knee Replacement, Right
        **Dx:** M17.11 - Primary OA, Right Knee
        **Provider:** Dr. Sarah Williams, MD (NPI: 1234567890)
        **Urgency:** Standard
        """)

    with st.expander("MEDICAL NECESSITY ARGUMENT", expanded=True):
        st.markdown("""
        This patient meets medical necessity criteria for TKR based on the following:
        
        1. **Diagnosis:** Kellgren-Lawrence Grade IV OA confirmed on imaging.
        2. **Conservative Treatment Failure:** Patient completed 12 sessions of physical therapy, trial of NSAIDs (naproxen 500mg BID x 3 months), and 3 corticosteroid injections over 6 months without relief.
        3. **Functional Limitation:** Unable to ambulate >100m without significant pain (VAS 8/10).
        4. **Surgical Candidacy:** BMI 28.2. No contraindications.
        
        **Supporting Guidelines:**
        - AAOS Clinical Practice Guideline
        - CMS NCD 150.6: Total Knee Replacement
        """)

    with st.expander("DOCUMENTATION CHECKLIST"):
        st.checkbox("Clinical notes with conservative history", value=True, disabled=True)
        st.checkbox("Imaging report (X-ray/MRI)", value=True, disabled=True)
        st.checkbox("PT records", value=True, disabled=True)
        st.checkbox("Medication trial history", value=True, disabled=True)
        st.checkbox("Surgical consent obtained", value=False)

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
