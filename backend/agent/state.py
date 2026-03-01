from typing import TypedDict, Optional, List, Literal
from pydantic import BaseModel

class TriageResult(BaseModel):
    urgency: Literal["urgent", "standard"]
    pa_type: Literal["surgical", "imaging", "medication", "dme", "behavioral_health"]
    routing_path: str
    reasoning: str

class CoverageResult(BaseModel):
    determination: Literal["covered", "not_covered", "conditional", "requires_review"]
    policy_id: Optional[str]
    policy_name: Optional[str]
    criteria_met: List[dict]                # [{"criterion": "...", "met": True/False, "evidence": "..."}]
    documentation_required: List[str]
    reasoning: str

class NPIResult(BaseModel):
    npi_valid: bool
    npi_status: Literal["active", "inactive", "not_found"]
    provider_name: Optional[str]
    provider_specialty: Optional[str]
    specialty_match: bool
    specialty_match_reasoning: str

class MedicalNecessityResult(BaseModel):
    argument: str                           # Structured medical necessity text
    evidence_items: List[dict]              # [{"source": "clinical_notes", "excerpt": "...", "relevance": "..."}]
    gaps: List[str]                         # Missing evidence items
    guidelines_cited: List[dict]            # [{"name": "...", "relevance": "..."}]
    strength: Literal["strong", "moderate", "weak", "insufficient"]

class QualityCheckResult(BaseModel):
    passed: bool
    issues: List[str]                       # Specific issues found
    improvement_instructions: Optional[str] # What to fix on retry
    overall_assessment: str

class DenialRiskResult(BaseModel):
    risk_score: float                       # 0-1
    risk_level: Literal["low", "medium", "high"]
    risk_factors: List[str]
    mitigation_suggestions: List[str]
    reasoning: str

class AppealResult(BaseModel):
    appeal_letter: str
    key_arguments: List[str]
    citations: List[str]
    status: Literal["draft", "ready", "error"]

class PAPackage(BaseModel):
    cover_sheet: str
    medical_necessity_argument: str
    supporting_evidence: List[dict]
    documentation_checklist: List[dict]     # [{"item": "...", "status": "present"/"missing"/"partial"}]
    npi_verification: dict
    risk_factors: List[str]
    recommended_actions: List[str]
    confidence_score: float                 # 0-1
    recommendation: Literal["auto_approve", "human_review", "likely_deny", "insufficient_info"]

class PARequestState(TypedDict):
    # Input
    request_id: str
    patient_id: str
    patient_name: str
    patient_dob: str
    payer_name: str
    procedure_code: str
    procedure_description: Optional[str]
    diagnosis_codes: List[str]
    diagnosis_descriptions: Optional[List[str]]
    requesting_provider_npi: str
    requesting_provider_name: Optional[str]
    clinical_notes: str
    urgency: str

    # Agent Outputs (populated sequentially)
    triage_result: Optional[TriageResult]
    coverage_result: Optional[CoverageResult]
    npi_result: Optional[NPIResult]
    medical_necessity_result: Optional[MedicalNecessityResult]
    quality_check_result: Optional[QualityCheckResult]
    denial_risk_result: Optional[DenialRiskResult]
    appeal_result: Optional[AppealResult]
    pa_package: Optional[PAPackage]

    # Control Flow
    current_agent: str
    iteration_count: int                    # Max 3
    error: Optional[str]
    pipeline_status: str                    # pending, in_progress, complete, error, human_review
    processing_start_time: float
    agent_timings: dict                     # {agent_name: duration_seconds}
