import streamlit as st
import pandas as pd
from services.pa_service import pa_service

def show():
    st.title("📂 PA Request History")
    st.markdown("---")

    # Fetch all requests from SQLite
    requests = pa_service.get_all_requests(limit=100)
    
    if not requests:
        st.info("No prior authorization requests submitted yet. Start by creating a new request or uploading a batch.")
        if st.button("Submit New Request"):
            # logic to switch tab in app.py if needed, here just info
            st.write("Navigate to 'New PA Request' in sidebar.")
        return

    # Pandas visualization
    df = pd.DataFrame(requests)
    
    # Simple table display
    # We display ID, Patient, Payer, Code, Urgency, Status, Created At
    if not df.empty:
        df["created_at"] = pd.to_datetime(df["created_at"])
        cols_to_show = ["id", "patient_name", "payer_name", "procedure_code", "urgency", "status", "created_at"]
        st.dataframe(df[cols_to_show], hide_index=True, use_container_width=True)

    # Allow selection
    st.subheader("Select Request for Details")
    selected_id = st.selectbox("Request ID", df["id"].tolist())
    if st.button("View Pipeline for Selection"):
        st.session_state["last_request_id"] = selected_id
        st.write("Navigate to 'Pipeline Visualizer' to see result details.")
