import streamlit as st
import os

def show():
    st.title("📖 User Manual")
    st.markdown("---")

    # Load from USER_MANUAL.md
    manual_path = os.path.join(os.path.dirname(__file__), "..", "USER_MANUAL.md")
    if os.path.exists(manual_path):
        with open(manual_path, "r") as f:
            content = f.read()
        st.markdown(content)
    else:
        st.error("User Manual not found. Please check implementation.")
