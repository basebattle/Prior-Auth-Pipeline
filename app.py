import streamlit as st
import base64
from datetime import datetime
from pathlib import Path

# Fix python import path
import sys
sys.path.append(str(Path(__file__).resolve().parent))

# Import constants and settings
from config.settings import PAGE_TITLE, PAGE_ICON
from config.constants import SUPPORTED_PAYERS, PA_TYPES

# Sidebar Navigation Structure
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

def main():
    # Initialize basic session state keys for cross-page persistence
    default_states = {
        "patient_id": "",
        "patient_name": "",
        "patient_dob": "",
        "payer_name": "UnitedHealthcare",
        "procedure_code": "",
        "diagnosis_codes": [],
        "requesting_provider_npi": "",
        "clinical_notes": "",
        "last_request_id": None,
        "show_review_id": None
    }
    for key, val in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = val

    st.sidebar.title("🩺 Prior Auth Pipeline")
    st.sidebar.markdown("---")
    
    # Navigation menu
    menu = ["New PA Request", "Pipeline Visualizer", "Appeals Management", "Analytics Dashboard", "Batch Processing", "History", "User Manual", "Settings"]
    selection = st.sidebar.radio("Navigation", menu)

    st.sidebar.markdown("---")
    st.sidebar.info("Authorized Healthcare Personnel Only. Data is processed in-memory (synthetic for demonstration).")

    # Routing based on selection
    if selection == "New PA Request":
        from pages import new_request
        new_request.show()
    elif selection == "Pipeline Visualizer":
        from pages import pipeline_view
        pipeline_view.show()
    elif selection == "Appeals Management":
        from pages import appeals
        appeals.show()
    elif selection == "Analytics Dashboard":
        from pages import analytics
        analytics.show()
    elif selection == "Batch Processing":
        from pages import batch
        batch.show()
    elif selection == "History":
        from pages import history
        history.show()
    elif selection == "User Manual":
        from pages import user_manual
        user_manual.show()
    elif selection == "Settings":
        st.write("Settings and API Config")

if __name__ == "__main__":
    main()
