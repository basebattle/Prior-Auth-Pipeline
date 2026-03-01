import time
import json
from typing import Dict, Any
from agent.state import PARequestState, AppealResult
from agent.prompts.appeal_prompt import APPEAL_SYSTEM_PROMPT, APPEAL_USER_TEMPLATE
from utils.llm import call_claude, parse_json_response
from config.settings import SONNET_MODEL

def run(state: PARequestState) -> Dict[str, Any]:
    """Appeal Generation Agent: Creates an appeal letter for denied PAs."""
    start_time = time.time()
    
    # 1. Gather denial context
    # Note: Appeal is usually triggered manually by a human or if denial risk is VERY high.
    # For now, it's a node in the graph that can be called.
    
    mn_res = state.get("medical_necessity_result")
    coverage_res = state.get("coverage_result")
    
    # 2. Format LLM inputs (Sonnet)
    prompt = APPEAL_USER_TEMPLATE.format(
        patient_name=state.get("patient_name"),
        procedure_code=state.get("procedure_code"),
        procedure_description=state.get("procedure_description", "Unknown"),
        payer_name=state.get("payer_name"),
        denial_reason="Medical necessity not established (Sample)",
        clinical_evidence=mn_res.argument if mn_res else "No evidence available",
        policy_citations=coverage_res.reasoning if coverage_res else "No policy data"
    )

    # 3. Call LLM
    response = call_claude(prompt, system_prompt=APPEAL_SYSTEM_PROMPT, model=SONNET_MODEL)
    result_data = parse_json_response(response)

    # 4. Parse result
    try:
        appeal_result = AppealResult(**result_data)
        appeal_result.status = "ready"
    except Exception as e:
        appeal_result = AppealResult(
            appeal_letter=f"Error generating appeal letter: {e}",
            key_arguments=[],
            citations=[],
            status="error"
        )

    elapsed = time.time() - start_time
    timings = state.get("agent_timings", {})
    timings["appeal_generation"] = elapsed

    return {
        "appeal_result": appeal_result,
        "agent_timings": timings
    }
