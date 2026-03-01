# Urgency Levels
URGENCY_TYPES = ["urgent", "standard"]

# Prior Authorization Categories
PA_TYPES = [
    "surgical",
    "imaging",
    "medication",
    "dme",
    "behavioral_health"
]

# Pipeline Configuration
MAX_PIPELINE_ITERATIONS = 3
CONFIDENCE_THRESHOLD_STRICT = 0.8
CONFIDENCE_THRESHOLD_MODERATE = 0.5

# Payer List (Commercial and Government)
SUPPORTED_PAYERS = [
    "UnitedHealthcare",
    "Aetna",
    "BCBS",
    "Cigna",
    "Humana",
    "Medicare",
    "Medicaid"
]

# NPPES API Configuration
NPPES_API_URL = "https://npiregistry.cms.hhs.gov/api/"
NPI_CACHE_EXPIRY_HOURS = 24
MAX_NPI_REQUESTS_PER_MINUTE = 20

# Medical Necessity Scoring Metrics
MN_RUBRIC_CRITERIA = [
    "Clinical Evidence",
    "Payer Criteria Alignment",
    "Conservative Treatment Documentation",
    "Logical Structure",
    "Gap Identification"
]

# Common Denial Codes
DENIAL_REASONS = [
    "Insufficient conservative treatment duration",
    "Missing imaging documentation",
    "BMI not documented",
    "Diagnosis code mismatch",
    "Provider specialty mismatch",
    "Medical necessity not established"
]
