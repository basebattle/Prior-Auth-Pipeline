import streamlit as st
import json
from services.pa_service import pa_service

def show():
    st.title("⚖️ Automated Appeals Management")
    st.markdown("---")

    # Fetch denied or high risk requests
    requests = pa_service.get_all_requests(limit=50)
    # Filter for simulation purposes - in reality we would check DB status
    denied_requests = [r for r in requests if r.get("status") in ["denied", "error", "complete"]]

    if not denied_requests:
        st.info("No denied PA requests available for appeal.")
        return

    st.subheader("Select Denied PA for Appeal Generation")
    req_options = {f"PA-2026-{r['id'][:4]} | {r['patient_name']}": r['id'] for r in denied_requests}
    selected_name = st.selectbox("Request", list(req_options.keys()))
    selected_id = req_options[selected_name]

    if st.button("Generate Formal Appeal Package ▶"):
        with st.spinner("Generating clinical appeal argument..."):
            # Simulation of appeal agent
            # In V2, we would call the AppealGenerationAgent node
            
            st.success("Appeal Letter Generated Successfully!")
            
            with st.expander("FORMAL APPEAL LETTER", expanded=True):
                st.markdown(f"""
                ### APPEAL FOR PRIOR AUTHORIZATION DENIAL
                **Date:** March 1, 2026  
                **Payer:** UnitedHealthcare  
                **Patient:** {selected_name.split('|')[1].strip()}  
                
                Dear Utilization Review Department,
                
                We are formally appealing the denial of prior authorization for procedure **CPT 27447 (Total Knee Replacement)**. 
                The denial appears to cite 'insufficient medical necessity evidence.' However, clinician documentation clearly 
                establishes that this patient meets all criteria defined in **Medicare NCD 150.6**.
                
                **Key Clinical Arguments:**
                1. Radiographic evidence confirms Kellgren-Lawrence Grade IV osteoarthritis.
                2. Patient has failed a minimum of 6 months of conservative treatment including PT and injections.
                3. Functional impairment is documented as 'Severe,' impacting activities of daily living (ADLs).
                
                We request an immediate reversal of this decision based on the attached clinical evidence.
                
                Sincerely,
                *Agentic Prior Auth System*
                """)
                
            col1, col2 = st.columns(2)
            with col1:
                st.button("Send to Payer Portal")
            with col2:
                st.download_button("Download Appeal PDF", "Sample PDF content", file_name="appeal.pdf")
