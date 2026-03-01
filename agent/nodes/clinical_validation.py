import time
import json
from typing import Dict, Any
from agent.state import PARequestState, CoverageResult
from agent.prompts.clinical_validation_prompt import CLINICAL_VALIDATION_SYSTEM_PROMPT, CLINICAL_VALIDATION_USER_TEMPLATE
from utils.llm import call_claude, parse_json_response
from tools import cms_coverage, payer_policy
from config.settings import SONNET_MODEL

def run(state: PARequestState) -> Dict[str, Any]:
    """Clinical Validation Agent: Logic to check policy coverage."""
    start_time = time.time()
    
    # 1. Access reference data via tools
    procedure_code = state.get("procedure_code")
    payer_name = state.get("payer_name")
    
    cms_policy = cms_coverage.lookup_cms_policy(procedure_code)
    p_policy = payer_policy.lookup_payer_policy(payer_name, procedure_code)

    # 2. Format LLM inputs
    prompt = CLINICAL_VALIDATION_USER_TEMPLATE.format(
        patient_name=state.get("patient_name"),
        payer_name=payer_name,
        procedure_code=procedure_code,
        procedure_description=state.get("procedure_description", "Unknown"),
        diagnosis_codes=", ".join(state.get("diagnosis_codes", [])),
        clinical_notes_excerpt=state.get("clinical_notes", "")[:500],
        cms_policy=json.dumps(cms_policy) if cms_policy else "None found",
        payer_policy=json.dumps(p_policy) if p_policy else "None found"
    )

    # 3. Call LLM (Sonnet for reasoning)
    response = call_claude(prompt, system_prompt=CLINICAL_VALIDATION_SYSTEM_PROMPT, model=SONNET_MODEL)
    result_data = parse_json_response(response)

    # 4. Parse result
    try:
        # Default policy_id/name if LLM misses but tools found something
        if not result_data.get("policy_id") and cms_policy:
            result_data["policy_id"] = cms_policy.get("policy_id")
        if not result_data.get("policy_name") and cms_policy:
            result_data["policy_name"] = cms_policy.get("policy_name")
            
        coverage_result = CoverageResult(**result_data)
    except Exception as e:
        coverage_result = CoverageResult(
            determination="requires_review",
            policy_id="Unknown",
            policy_name="Unknown",
            criteria_met=[],
            documentation_required=[],
            reasoning=f"Error parsing coverage response: {e}"
        )

    elapsed = time.time() - start_time
    timings = state.get("agent_timings", {})
    timings["clinical_validation"] = elapsed

    return {
        "coverage_result": coverage_result,
        "current_agent": "npi_verification",
        "agent_timings": timings
    }
