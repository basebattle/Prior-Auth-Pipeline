import json
from uuid import uuid4
from datetime import date, timedelta
import random
from typing import List, Dict, Any

# Mock patient data
FAM_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
FIRST_NAMES = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]

PAYERS = ["UnitedHealthcare", "Aetna", "BCBS", "Cigna", "Humana", "Medicare", "Medicaid"]

# Sample procedures for scenarios
SCENARIOS = [
    {
        "type": "surgical",
        "procedure_code": "27447",
        "procedure_description": "Total Knee Replacement",
        "diagnosis_codes": ["M17.11"],
        "diagnosis_descriptions": ["Primary osteoarthritis, right knee"],
        "notes": "Patient presents with severe OA of right knee. Failed 6 months of PT (12 sessions), NSAIDs, 3 steroid injections. X-ray confirms Grade IV OA. BMI 28.2. Functional limitation: unable to walk >100m. No contraindications."
    },
    {
        "type": "surgical",
        "procedure_code": "27130",
        "procedure_description": "Total Hip Replacement",
        "diagnosis_codes": ["M16.11"],
        "diagnosis_descriptions": ["Primary osteoarthritis, right hip"],
        "notes": "Right hip pain increasing for 2 yrs. Radiographic joint space narrowing. Failed aquatic therapy and oral analgesics. High pain score (7/10). No surgical contraindications."
    },
    {
        "type": "imaging",
        "procedure_code": "70553",
        "procedure_description": "MRI Brain with & without contrast",
        "diagnosis_codes": ["G43.9"],
        "diagnosis_descriptions": ["Migraine, unspecified"],
        "notes": "Patient with chronic migraine shows change in headache pattern and new focal neurological signs. Red flag symptoms. Rule out intracranial pathology."
    },
    {
        "type": "medication",
        "procedure_code": "J1745",
        "procedure_description": "Infliximab injection",
        "diagnosis_codes": ["K50.90"],
        "diagnosis_descriptions": ["Crohn's disease, unspecified"],
        "notes": "Severe Crohn's disease, failed first-line therapies (mesalamine, steroids). Escalation of therapy justified by CDAI score >300."
    }
]

def generate_patient() -> Dict[str, str]:
    fn = random.choice(FIRST_NAMES)
    ln = random.choice(FAM_NAMES)
    return {
        "patient_id": f"P{random.randint(10000, 99999)}",
        "patient_name": f"{fn} {ln}",
        "patient_dob": (date.today() - timedelta(days=random.randint(6570, 29200))).isoformat()  # Age 18-80
    }

def generate_scenarios(count: int = 20) -> List[Dict[str, Any]]:
    scenarios = []
    for _ in range(count):
        patient = generate_patient()
        template = random.choice(SCENARIOS)
        payer = random.choice(PAYERS)
        
        scenario = {
            "id": str(uuid4()),
            "patient_id": patient["patient_id"],
            "patient_name": patient["patient_name"],
            "patient_dob": patient["patient_dob"],
            "payer_name": payer,
            "procedure_code": template["procedure_code"],
            "procedure_description": template["procedure_description"],
            "diagnosis_codes": template["diagnosis_codes"],
            "diagnosis_descriptions": template["diagnosis_descriptions"],
            "requesting_provider_npi": f"{random.randint(1000000000, 9999999999)}",
            "clinical_notes": template["notes"],
            "urgency": "standard",
            "type": template["type"]
        }
        scenarios.append(scenario)
    return scenarios

if __name__ == "__main__":
    count = 20
    test_cases = generate_scenarios(count)
    print(f"Generated {count} test cases.")
    with open("data/synthetic_scenarios.json", "w") as f:
        json.dump(test_cases, f, indent=2)
