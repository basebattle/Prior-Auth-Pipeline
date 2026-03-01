import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "pa_pipeline.db"
GUIDELINES_DIR = BASE_DIR / "data" / "guidelines"
EXPORTS_DIR = BASE_DIR / "exports"

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "Prior-Auth-Pipeline")

# Model Configuration
HAIKU_MODEL = "claude-3-5-haiku-20241022"  # Fast, cheap for classification
SONNET_MODEL = "claude-3-5-sonnet-20241022" # reasoning for clinical analysis

# RAG Configuration
CHROMA_PERSIST_DIRECTORY = str(BASE_DIR / "data" / "chroma_db")

# Streamlit Configuration
PAGE_TITLE = "Prior Auth Pipeline"
PAGE_ICON = "🩺"
