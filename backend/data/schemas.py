from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from datetime import date

class PARequestInput(BaseModel):
    patient_id: str = Field(..., description="Unique patient identifier")
    patient_name: str = Field(..., description="Full name of the patient")
    patient_dob: str = Field(..., description="Patient date of birth (YYYY-MM-DD)")
    payer_name: str = Field(..., description="Insurance payer name")
    procedure_code: str = Field(..., description="CPT or HCPCS code for the requested procedure")
    diagnosis_codes: List[str] = Field(..., description="List of ICD-10 diagnosis codes")
    requesting_provider_npi: str = Field(..., description="10-digit National Provider Identifier")
    clinical_notes: str = Field(..., description="Clinical justification for the request")
    urgency: Literal["standard", "urgent"] = "standard"

    @validator("patient_dob")
    def validate_dob(cls, v):
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Patient DOB must be in YYYY-MM-DD format")

    @validator("requesting_provider_npi")
    def validate_npi(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError("NPI must be a 10-digit number")
        return v

class PAStatus(BaseModel):
    request_id: str
    status: Literal["pending", "in_progress", "complete", "error", "human_review"]
    current_agent: Optional[str]
    elapsed_seconds: float

class PAPackageResponse(BaseModel):
    request_id: str
    package_document: str
    confidence_score: float
    risk_factors: List[str]
    recommended_actions: List[str]
    recommendation: str
