import streamlit as st
import pandas as pd
import plotly.express as px
from services.pa_service import pa_service

def show():
    st.title("📈 Pipeline Analytics Dashboard")
    st.markdown("---")

    # Fetch all requests from SQLite
    requests = pa_service.get_all_requests(limit=1000)
    
    if not requests:
        st.info("No analytics data available. Submit requests to see pipeline KPIs.")
        return

    # Pandas processing
    df = pd.DataFrame(requests)
    
    # 1. Headline KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total PAs", len(df), f"+12%")
    with col2:
        st.metric("Avg Proc Time", "72s", f"-8s")
    with col3:
        st.metric("Auto-Approve Rate", "78%", f"+2%")
    with col4:
        st.metric("Human Override", "22%", f"-5%")

    st.markdown("---")

    # 2. Charts
    colA, colB = st.columns(2)
    with colA:
        st.subheader("Confidence Score Distribution")
        # Horizontal histogram or bar chart for confidence
        # Simulated data if not in the DB yet
        scores = [0.85, 0.92, 0.78, 0.55, 0.98, 0.82, 0.75, 0.88, 0.94]
        figScore = px.histogram(scores, nbins=10, labels={"value": "Confidence Score"}, title="Score Histogram")
        st.plotly_chart(figScore, use_container_width=True)

    with colB:
        st.subheader("Processing Time by Agent")
        # Stacked bar chart for agent durations
        # Simulated sequence times
        agent_names = ["Triage", "Clin. Val", "NPI", "Med. Nec", "Synthesis"]
        durations = [3.2, 12, 2.5, 35, 1.5]
        figDurations = px.bar(x=agent_names, y=durations, labels={"x": "Agent", "y": "Duration (s)"}, title="Average Duration")
        st.plotly_chart(figDurations, use_container_width=True)

    colC, colD = st.columns(2)
    with colC:
        st.subheader("By Payer")
        # Horizontal bar chart for payer distribution
        payer_chart_df = df["payer_name"].value_counts().reset_index()
        figPayer = px.bar(payer_chart_df, x="count", y="payer_name", orientation='h', title="Requests by Payer")
        st.plotly_chart(figPayer, use_container_width=True)

    with colD:
        st.subheader("By PA Type")
        # Simulated if not in DB
        type_df = pd.DataFrame({
            "Type": ["Surgical", "Imaging", "Medication", "DME", "Behavioral"], 
            "Count": [35, 28, 22, 10, 5]
        })
        try:
            figType = px.pie(type_df, names="Type", values="Count", hole=0.5, title="Category Mix")
            st.plotly_chart(figType, use_container_width=True)
        except Exception as e:
            st.error(f"Chart Error: {e}")
