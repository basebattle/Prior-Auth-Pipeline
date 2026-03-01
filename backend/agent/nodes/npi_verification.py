import time
import json
from typing import Dict, Any
from agent.state import PARequestState, NPIResult
from agent.prompts.npi_prompt import NPI_VERIFICATION_SYSTEM_PROMPT, NPI_USER_TEMPLATE
from utils.llm import call_claude, parse_json_response
from tools import npi_lookup
from config.settings import HAIKU_MODEL

def run(state: PARequestState) -> Dict[str, Any]:
    """NPI Verification Agent: Verify provider NPI and specialty match."""
    start_time = time.time()
    
    # 1. Access NPI Registry tool
    npi = state.get("requesting_provider_npi")
    provider_data = npi_lookup.sync_lookup_npi(npi)
    
    # 2. Format LLM inputs
    prompt = NPI_USER_TEMPLATE.format(
        npi=npi,
        procedure_code=state.get("procedure_code")
    )
    system_prompt = NPI_VERIFICATION_SYSTEM_PROMPT.format(
        provider_data=json.dumps(provider_data.dict()) if provider_data else "No data for this NPI",
        procedure_code=state.get("procedure_code"),
        procedure_description=state.get("procedure_description", "Unknown")
    )

    # 3. Call LLM (Haiku is enough)
    response = call_claude(prompt, system_prompt=system_prompt, model=HAIKU_MODEL)
    result_data = parse_json_response(response)

    # 4. Parse result
    try:
        npi_result = NPIResult(**result_data)
    except Exception as e:
        npi_result = NPIResult(
            npi_valid=False if not provider_data else True,
            npi_status="active" if (provider_data and provider_data.status == "A") else "not_found",
            provider_name=provider_data.provider_name if provider_data else "Unknown",
            provider_specialty=provider_data.specialty if provider_data else "Unknown",
            specialty_match=True, # default to pass if uncertainty
            specialty_match_reasoning=f"Error parsing NPI response: {e}"
        )

    elapsed = time.time() - start_time
    timings = state.get("agent_timings", {})
    timings["npi_verification"] = elapsed

    return {
        "npi_result": npi_result,
        "current_agent": "medical_necessity",
        "agent_timings": timings
    }
