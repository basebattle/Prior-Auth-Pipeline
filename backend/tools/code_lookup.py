import json
from pathlib import Path
from typing import Optional, List, Dict

# Path to reference data
BASE_REF_DIR = Path(__file__).resolve().parent.parent / "data" / "reference"

def _load_json(filename: str) -> List[Dict]:
    path = BASE_REF_DIR / filename
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return []

CPT_REFERENCE = _load_json("cpt_codes.json")
ICD10_REFERENCE = _load_json("icd10_codes.json")
HCPCS_REFERENCE = _load_json("hcpcs_codes.json")

def lookup_cpt(code: str) -> Optional[str]:
    """Return description for a CPT code."""
    for item in CPT_REFERENCE:
        if item["code"] == code:
            return item["description"]
    return None

def lookup_icd10(code: str) -> Optional[str]:
    """Return description for an ICD-10 code."""
    for item in ICD10_REFERENCE:
        if item["code"] == code:
            return item["description"]
    return None

def lookup_hcpcs(code: str) -> Optional[str]:
    """Return description for an HCPCS code."""
    for item in HCPCS_REFERENCE:
        if item["code"] == code:
            return item["description"]
    return None

def validate_procedure_code(code: str) -> bool:
    """Validate if the code exists in CPT or HCPCS references."""
    return any(c["code"] == code for c in CPT_REFERENCE + HCPCS_REFERENCE)

def validate_icd10_codes(codes: List[str]) -> List[str]:
    """Return list of codes that are valid."""
    valid_codes = [c["code"] for c in ICD10_REFERENCE]
    return [c for c in codes if c in valid_codes]
