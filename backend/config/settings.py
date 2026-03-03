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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBkma1v3eRRHg1FQ0f3Lw83cxObmFK0bGo")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "Prior-Auth-Pipeline")

# Model Configuration
HAIKU_MODEL = "gemini-2.5-flash"  # Gemini format
SONNET_MODEL = "gemini-2.5-flash" # Gemini format


# RAG Configuration
CHROMA_PERSIST_DIRECTORY = str(BASE_DIR / "data" / "chroma_db")

# Streamlit Configuration
PAGE_TITLE = "Prior Auth Pipeline"
PAGE_ICON = "🩺"
