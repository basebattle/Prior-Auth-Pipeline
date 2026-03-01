import time
import json
from typing import Dict, Any
from agent.state import PARequestState, DenialRiskResult
from agent.prompts.denial_risk_prompt import DENIAL_RISK_SYSTEM_PROMPT, DENIAL_RISK_USER_TEMPLATE
from utils.llm import call_claude, parse_json_response
from config.settings import SONNET_MODEL

def run(state: PARequestState) -> Dict[str, Any]:
    """Denial Risk Agent: Predicts denial probability."""
    start_time = time.time()
    
    # 1. Gather results from previous agents
    coverage_res = state.get("coverage_result")
    npi_res = state.get("npi_result")
    mn_res = state.get("medical_necessity_result")
    
    # 2. Format LLM inputs (Sonnet)
    prompt = DENIAL_RISK_USER_TEMPLATE.format(
        patient_name=state.get("patient_name"),
        procedure_code=state.get("procedure_code"),
        payer_name=state.get("payer_name"),
        coverage_determination=coverage_res.determination if coverage_res else "Unknown",
        npi_status=npi_res.npi_status if npi_res else "Unknown",
        mn_strength=mn_res.strength if mn_res else "Unknown",
        mn_gaps=", ".join(mn_res.gaps) if mn_res and mn_res.gaps else "None",
        denial_patterns="Missing PT documentation, insufficient conservative treatment duration, specialty mismatch."
    )

    # 3. Call LLM
    response = call_claude(prompt, system_prompt=DENIAL_RISK_SYSTEM_PROMPT, model=SONNET_MODEL)
    result_data = parse_json_response(response)

    # 4. Parse result
    try:
        denial_risk_result = DenialRiskResult(**result_data)
    except Exception as e:
        denial_risk_result = DenialRiskResult(
            risk_score=0.5,
            risk_level="medium",
            risk_factors=["Error during risk analysis parsing"],
            mitigation_suggestions=["Manually review all clinical findings"],
            reasoning=f"Error parsing denial risk response: {e}"
        )

    elapsed = time.time() - start_time
    timings = state.get("agent_timings", {})
    timings["denial_risk"] = elapsed

    return {
        "denial_risk_result": denial_risk_result,
        "current_agent": "decision_synthesis",
        "agent_timings": timings
    }
