import json
from pathlib import Path
from typing import Optional, List, Dict

# Path to reference data
BASE_REF_DIR = Path(__file__).resolve().parent.parent / "data" / "reference"

def _load_cms_policies() -> List[Dict]:
    path = BASE_REF_DIR / "cms_coverage_policies.json"
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return []

CMS_POLICIES = _load_cms_policies()

def lookup_cms_policy(procedure_code: str) -> Optional[Dict]:
    """Return CMS policy details if available for the given procedure code."""
    for policy in CMS_POLICIES:
        if procedure_code in policy["procedure_codes"]:
            return policy
    return None

def check_diagnosis_requirements(policy: Dict, diagnosis_codes: List[str]) -> bool:
    """Check if the provided diagnosis codes meet policy requirements."""
    required = policy.get("diagnosis_requirements", {}).get("required_primary", [])
    if not required:
        return True
    return any(dx in required for dx in diagnosis_codes)

def get_documentation_list(procedure_code: str) -> List[str]:
    """Return list of documentation requirements for a procedure."""
    policy = lookup_cms_policy(procedure_code)
    if policy:
        return policy.get("documentation_requirements", [])
    return []
