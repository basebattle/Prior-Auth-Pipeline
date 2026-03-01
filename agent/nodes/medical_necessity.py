import time
import json
from typing import Dict, Any
from agent.state import PARequestState, MedicalNecessityResult
from agent.prompts.medical_necessity_prompt import MEDICAL_NECESSITY_SYSTEM_PROMPT, MEDICAL_NECESSITY_USER_TEMPLATE
from utils.llm import call_claude, parse_json_response
from tools.clinical_guidelines import guidelines_tool
from config.settings import SONNET_MODEL

def run(state: PARequestState) -> Dict[str, Any]:
    """Medical Necessity Agent: Evidence extraction and argument building."""
    start_time = time.time()
    
    # 1. Access RAG tool for guidelines
    procedure_code = state.get("procedure_code")
    procedure_description = state.get("procedure_description", "Unknown")
    search_query = f"{procedure_code} {procedure_description} indications criteria"
    guideline_snippets = guidelines_tool.search(search_query)

    # 2. Get payer criteria from previous step
    coverage_result = state.get("coverage_result")
    payer_criteria = "No specific criteria extracted"
    if coverage_result:
        # Extract metadata from coverage result if available
        payer_criteria = coverage_result.reasoning if hasattr(coverage_result, 'reasoning') else str(coverage_result)

    # 3. Format LLM inputs (Sonnet)
    prompt = MEDICAL_NECESSITY_USER_TEMPLATE.format(
        patient_name=state.get("patient_name"),
        procedure_code=procedure_code
    )
    system_prompt = MEDICAL_NECESSITY_SYSTEM_PROMPT.format(
        procedure_code=procedure_code,
        procedure_description=procedure_description,
        diagnosis_codes=", ".join(state.get("diagnosis_codes", [])),
        clinical_notes=state.get("clinical_notes", "")[:2000],
        payer_criteria=payer_criteria,
        guideline_snippets=json.dumps(guideline_snippets)
    )

    # 4. Call LLM
    response = call_claude(prompt, system_prompt=system_prompt, model=SONNET_MODEL)
    result_data = parse_json_response(response)

    # 5. Parse result
    try:
        medical_necessity_result = MedicalNecessityResult(**result_data)
    except Exception as e:
        medical_necessity_result = MedicalNecessityResult(
            argument="Manual clinical case review recommended due to parsing error.",
            evidence_items=[],
            gaps=["Clinical justification parsing failed"],
            guidelines_cited=[],
            strength="insufficient"
        )

    elapsed = time.time() - start_time
    timings = state.get("agent_timings", {})
    timings["medical_necessity"] = elapsed

    return {
        "medical_necessity_result": medical_necessity_result,
        "current_agent": "quality_check",
        "agent_timings": timings
    }
