import time
import json
from typing import Dict, Any
from agent.state import PARequestState, PAPackage
from agent.prompts.synthesis_prompt import SYNTHESIS_SYSTEM_PROMPT, SYNTHESIS_USER_TEMPLATE
from utils.llm import call_claude, parse_json_response
from config.settings import SONNET_MODEL

def run(state: PARequestState) -> Dict[str, Any]:
    """Decision Synthesis Agent: Compiles all prior agent outputs into a final package."""
    start_time = time.time()
    
    # 1. Gather all prior results
    triage_res = state.get("triage_result")
    coverage_res = state.get("coverage_result")
    npi_res = state.get("npi_result")
    mn_res = state.get("medical_necessity_result")
    risk_res = state.get("denial_risk_result")
    
    # 2. Format LLM inputs for synthesis (Sonnet)
    prompt = SYNTHESIS_USER_TEMPLATE.format(
        patient_name=state.get("patient_name")
    )
    system_prompt = SYNTHESIS_SYSTEM_PROMPT.format(
        triage_data=json.dumps(triage_res.dict()) if triage_res else "None",
        coverage_data=json.dumps(coverage_res.dict()) if coverage_res else "None",
        npi_data=json.dumps(npi_res.dict()) if npi_res else "None",
        mn_data=json.dumps(mn_res.dict()) if mn_res else "None",
        risk_data=json.dumps(risk_res.dict()) if risk_res else "None"
    )

    # 3. Call LLM
    response = call_claude(prompt, system_prompt=system_prompt, model=SONNET_MODEL)
    result_data = parse_json_response(response)

    # 4. Parse result
    try:
        pa_package = PAPackage(**result_data)
    except Exception as e:
        pa_package = PAPackage(
            cover_sheet=f"Error compiling package: {e}",
            medical_necessity_argument="Manual synthesis required.",
            supporting_evidence=[],
            documentation_checklist=[],
            npi_verification={"status": "error", "provider": state.get("requesting_provider_name", "Unknown")},
            risk_factors=["Synthesis error incurred"],
            recommended_actions=["Manually review all previous agent steps"],
            confidence_score=0.1,
            recommendation="human_review"
        )

    elapsed = time.time() - start_time
    timings = state.get("agent_timings", {})
    timings["decision_synthesis"] = elapsed

    return {
        "pa_package": pa_package,
        "pipeline_status": "complete",
        "agent_timings": timings
    }
