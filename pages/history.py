import streamlit as st
import pandas as pd
from services.pa_service import pa_service

def show():
    st.title("📂 PA Request History")
    st.markdown("---")

    # Fetch all requests from SQLite
    requests = pa_service.get_all_requests(limit=100)
    
    if not requests:
        st.warning("⚠️ No Data Found: No prior authorization requests submitted yet.")
        st.info("Start by creating a new request or uploading a batch.")
        if st.button("➕ Create New Case"):
             # In a real app we might redirect, here we just prompt
             st.info("Use the sidebar to navigate to 'New PA Request'.")
        return

    # Pandas visualization
    df = pd.DataFrame(requests)
    
    if not df.empty:
        # Ensure all required columns exist
        for col in ["id", "patient_name", "payer_name", "procedure_code", "urgency", "status", "created_at"]:
            if col not in df.columns:
                df[col] = "N/A"
        
        df["created_at"] = pd.to_datetime(df["created_at"])
        cols_to_show = ["id", "patient_name", "payer_name", "procedure_code", "urgency", "status", "created_at"]
        st.dataframe(df[cols_to_show], hide_index=True, use_container_width=True)

        # 🛠️ Selection Logic (Sync to Global State)
        st.markdown("---")
        st.subheader("Inspection Tools")
        selected_id = st.selectbox("Select a Request ID to inspect", df["id"].tolist())
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 View in Pipeline Visualizer"):
                st.session_state["last_request_id"] = selected_id
                st.session_state["app_state"]["last_request_id"] = selected_id
                st.success(f"Attached {selected_id[:8]} to Pipeline View.")
                st.rerun()
        with col2:
            if st.button("🛡️ Open for Human Review"):
                st.session_state["show_review_id"] = selected_id
                st.session_state["app_state"]["show_review_id"] = selected_id
                st.success(f"Attached {selected_id[:8]} to Review Checkpoint.")
                st.rerun()
