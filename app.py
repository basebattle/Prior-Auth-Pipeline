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
    # 🛠️ Step 1: Core State Fix (Structured Initialization)
    if "app_state" not in st.session_state:
        st.session_state["app_state"] = {
            "requests": [],            # Cache for history
            "last_request_id": None,   # ID for Pipeline View
            "show_review_id": None,    # ID for Human Review
            "clinical_notes": "",      # Shared notes buffer
            "form_data": {},           # Persistent form inputs
            "pipeline_status": "idle"  # Status tracker
        }
    
    # Backwards compatibility for existing logic
    for key in ["patient_id", "patient_name", "patient_dob", "payer_name", "procedure_code", "diagnosis_codes", "requesting_provider_npi", "clinical_notes"]:
        if key not in st.session_state:
            st.session_state[key] = "" if key != "diagnosis_codes" else []
    
    if "last_request_id" not in st.session_state:
        st.session_state["last_request_id"] = None
    if "show_review_id" not in st.session_state:
        st.session_state["show_review_id"] = None

    st.sidebar.title("🩺 Prior Auth Pipeline")
    st.sidebar.markdown("---")
    
    # Navigation menu
    menu = ["New PA Request", "Pipeline Visualizer", "Appeals Management", "Analytics Dashboard", "Batch Processing", "History", "User Manual", "Settings"]
    selection = st.sidebar.radio("Navigation", menu)

    st.sidebar.markdown("---")
    st.sidebar.info("Authorized Healthcare Personnel Only. Data processed in-memory (synthetic).")

    # Routing based on selection with robust protection
    try:
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
    except Exception as e:
        st.error(f"🚨 Module Error: Unable to load '{selection}'")
        st.warning("This is often caused by a background script error or missing data state.")
        with st.expander("Technical Traceback"):
            import traceback
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
