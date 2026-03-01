import json
from pathlib import Path
from typing import Optional, List, Dict

# Path to reference data
BASE_REF_DIR = Path(__file__).resolve().parent.parent / "data" / "reference"

def _load_payer_policies() -> List[Dict]:
    path = BASE_REF_DIR / "payer_policies.json"
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return []

PAYER_POLICIES = _load_payer_policies()

def lookup_payer_policy(payer_name: str, procedure_code: str) -> Optional[Dict]:
    """Return payer-specific policy details if available."""
    for policy in PAYER_POLICIES:
        if policy["payer_name"].lower() == payer_name.lower() and policy["procedure_code"] == procedure_code:
            return policy
    return None

def get_pa_requirements(payer_name: str, procedure_code: str) -> Optional[Dict]:
    """Return PA criteria for a procedure for a specific payer."""
    policy = lookup_payer_policy(payer_name, procedure_code)
    if policy:
        return policy.get("pa_criteria", {})
    return None

def check_pa_required(payer_name: str, procedure_code: str) -> bool:
    """Check if PA is required for a procedure for a specific payer."""
    policy = lookup_payer_policy(payer_name, procedure_code)
    if policy:
        return policy.get("requires_pa", True)
    return True
