from langgraph.graph import StateGraph, END
from typing import Dict, Any

from agent.state import PARequestState
from agent.nodes import triage, clinical_validation, npi_verification, medical_necessity, decision_synthesis, quality_check, denial_risk
from config.constants import MAX_PIPELINE_ITERATIONS

def route_after_quality_check(state: PARequestState) -> str:
    """Conditional routing based on quality check result."""
    qc = state.get("quality_check_result")
    iteration = state.get("iteration_count", 0)
    
    if qc and qc.passed:
        return "proceed"
    elif iteration >= MAX_PIPELINE_ITERATIONS:
        # Max retries exceeded, proceed anyway but synthesis will note it
        return "fail"
    else:
        # Fail/Incomplete, retry clinical/necessity logic
        return "retry"

def build_pa_pipeline() -> StateGraph:
    """Construct the LangGraph workflow for Prior Authorization."""
    workflow = StateGraph(PARequestState)

    # 1. Add nodes
    workflow.add_node("triage", triage.run)
    workflow.add_node("clinical_validation", clinical_validation.run)
    workflow.add_node("npi_verification", npi_verification.run)
    workflow.add_node("medical_necessity", medical_necessity.run)
    workflow.add_node("quality_check", quality_check.run)
    workflow.add_node("denial_risk", denial_risk.run)
    workflow.add_node("decision_synthesis", decision_synthesis.run)

    # 2. Define edges and routing
    workflow.set_entry_point("triage")
    workflow.add_edge("triage", "clinical_validation")
    workflow.add_edge("clinical_validation", "npi_verification")
    workflow.add_edge("npi_verification", "medical_necessity")
    workflow.add_edge("medical_necessity", "quality_check")

    # 3. Add conditional edge for reflection loop
    workflow.add_conditional_edges(
        "quality_check",
        route_after_quality_check,
        {
            "retry": "clinical_validation",     # loop back to fix metadata/evidence
            "proceed": "denial_risk",
            "fail": "denial_risk"               # continue but as failed state
        }
    )
    
    # 4. Final steps
    workflow.add_edge("denial_risk", "decision_synthesis")
    workflow.add_edge("decision_synthesis", END)

    return workflow.compile()

# instance for direct usage
pa_pipeline = build_pa_pipeline()
