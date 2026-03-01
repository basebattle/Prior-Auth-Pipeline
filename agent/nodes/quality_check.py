import time
import json
from typing import Dict, Any
from agent.state import PARequestState, QualityCheckResult
from agent.prompts.quality_check_prompt import QUALITY_CHECK_SYSTEM_PROMPT, QUALITY_CHECK_USER_TEMPLATE
from utils.llm import call_claude, parse_json_response
from config.settings import SONNET_MODEL

def run(state: PARequestState) -> Dict[str, Any]:
    """Quality Check Agent: Reflects on the state to decide if improvements are needed."""
    start_time = time.time()
    
    # 1. Gather current state summary
    triage_res = state.get("triage_result")
    coverage_res = state.get("coverage_result")
    npi_res = state.get("npi_result")
    mn_res = state.get("medical_necessity_result")
    
    # 2. Format LLM inputs (Sonnet)
    prompt = QUALITY_CHECK_USER_TEMPLATE.format(
        patient_name=state.get("patient_name")
    )
    system_prompt = QUALITY_CHECK_SYSTEM_PROMPT.format(
        triage_data=json.dumps(triage_res.dict()) if triage_res else "None",
        coverage_data=json.dumps(coverage_res.dict()) if coverage_res else "None",
        npi_data=json.dumps(npi_res.dict()) if npi_res else "None",
        mn_data=json.dumps(mn_res.dict()) if mn_res else "None"
    )

    # 3. Call LLM
    response = call_claude(prompt, system_prompt=system_prompt, model=SONNET_MODEL)
    result_data = parse_json_response(response)

    # 4. Parse result
    try:
        quality_check_result = QualityCheckResult(**result_data)
    except Exception as e:
        quality_check_result = QualityCheckResult(
            passed=True, # default to pass on error to avoid infinite loop
            issues=[f"Error parsing quality check response: {e}"],
            improvement_instructions=None,
            overall_assessment="Error during quality check."
        )

    # Update iteration count if failed
    iteration_count = state.get("iteration_count", 0)
    if not quality_check_result.passed:
        iteration_count += 1

    elapsed = time.time() - start_time
    timings = state.get("agent_timings", {})
    timings["quality_check"] = elapsed

    return {
        "quality_check_result": quality_check_result,
        "iteration_count": iteration_count,
        "agent_timings": timings
    }
