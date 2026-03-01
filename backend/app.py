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
    # 🛠️ Unified State Initialization
    if "app_state" not in st.session_state:
        st.session_state["app_state"] = {
            "last_request_id": None,
            "show_review_id": None,
            "active_page": "New PA Request",
            "pipeline_status": "idle"
        }

    # Backward compatibility and shortcuts
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "New PA Request"
    if "last_request_id" not in st.session_state:
        st.session_state["last_request_id"] = None
    if "show_review_id" not in st.session_state:
        st.session_state["show_review_id"] = None

    st.sidebar.title("🩺 Prior Auth Pipeline")
    st.sidebar.markdown("---")
    
    # Navigation menu - Linked to Session State
    menu = ["New PA Request", "Pipeline Visualizer", "Human Review", "Appeals Management", "Analytics Dashboard", "Batch Processing", "History", "User Manual", "Settings"]
    
    # Determine default index
    default_idx = menu.index(st.session_state["active_page"]) if st.session_state["active_page"] in menu else 0
    
    selection = st.sidebar.radio(
        "Navigation", 
        menu, 
        index=default_idx, 
        key="navigation_radio"
    )

    # Sync selection back to state
    if selection != st.session_state["active_page"]:
        st.session_state["active_page"] = selection
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.info("Authorized Healthcare Personnel Only. Data processed in-memory.")

    # Routing based on state-driven selection
    active_page = st.session_state["active_page"]
    
    try:
        if active_page == "New PA Request":
            from modules import new_request
            new_request.show()
        elif active_page == "Pipeline Visualizer":
            from modules import pipeline_view
            pipeline_view.show()
        elif active_page == "Human Review":
            from modules import review
            review.show()
        elif active_page == "Appeals Management":
            from modules import appeals
            appeals.show()
        elif active_page == "Analytics Dashboard":
            from modules import analytics
            analytics.show()
        elif active_page == "Batch Processing":
            from modules import batch
            batch.show()
        elif active_page == "History":
            from modules import history
            history.show()
        elif active_page == "User Manual":
            from modules import user_manual
            user_manual.show()
        elif active_page == "Settings":
            st.write("Settings and API Config")
    except Exception as e:
        st.error(f"🚨 Module Error: Unable to load '{active_page}'")
        st.warning("State mechanism recovered. Please retry navigation.")
        with st.expander("Technical Traceback"):
            import traceback
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
