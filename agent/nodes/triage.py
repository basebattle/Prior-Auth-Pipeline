import time
from typing import Dict, Any
from agent.state import PARequestState, TriageResult
from agent.prompts.triage_prompt import TRIAGE_SYSTEM_PROMPT, TRIAGE_USER_TEMPLATE
from utils.llm import call_claude, parse_json_response
from config.settings import HAIKU_MODEL

def run(state: PARequestState) -> Dict[str, Any]:
    """Triage Agent: Classifies urgency and type."""
    start_time = time.time()
    
    # Format inputs for prompt
    diagnosis_codes_formatted = ", ".join(state.get("diagnosis_codes", []))
    prompt = TRIAGE_USER_TEMPLATE.format(
        patient_name=state.get("patient_name"),
        patient_dob=state.get("patient_dob"),
        payer_name=state.get("payer_name"),
        procedure_code=state.get("procedure_code"),
        procedure_description=state.get("procedure_description", "Unknown"),
        diagnosis_codes_formatted=diagnosis_codes_formatted,
        clinical_notes_excerpt=state.get("clinical_notes", "")[:500],
        urgency=state.get("urgency", "standard")
    )

    # Call LLM
    response = call_claude(prompt, system_prompt=TRIAGE_SYSTEM_PROMPT, model=HAIKU_MODEL)
    result_data = parse_json_response(response)

    # Parse result into TriageResult model
    try:
        triage_result = TriageResult(**result_data)
    except Exception as e:
        # Graceful failure - default to standard
        triage_result = TriageResult(
            urgency="standard",
            pa_type="surgical" if state.get("procedure_code", "").startswith("2") else "medication",
            routing_path="Default fallback",
            reasoning=f"Error parsing triage response: {e}"
        )

    # Update state
    elapsed = time.time() - start_time
    timings = state.get("agent_timings", {})
    timings["triage"] = elapsed

    return {
        "triage_result": triage_result,
        "current_agent": "clinical_validation",
        "agent_timings": timings
    }
