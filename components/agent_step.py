import streamlit as st
import time

def show_agent_step(name: str, status: str, duration: str = "0.0s", summary: str = ""):
    """Component to display a single agent step."""
    icon = "✅" if status == "complete" else "🔄" if status == "running" else "⚪"
    color = "green" if status == "complete" else "blue" if status == "running" else "gray"
    
    with st.container():
        st.markdown(f"### {icon} {name} ( {duration} )")
        if status == "complete":
            st.success(f"Processing Complete: {summary}")
        elif status == "running":
            st.info(f"Agent Processing... {summary}")
        else:
            st.write("Pending...")
        st.markdown("---")
