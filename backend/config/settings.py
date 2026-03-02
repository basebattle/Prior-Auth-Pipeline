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
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "Prior-Auth-Pipeline")

# Model Configuration
HAIKU_MODEL = "anthropic/claude-3.5-haiku"  # OpenRouter format
SONNET_MODEL = "anthropic/claude-3.5-sonnet" # OpenRouter format

# RAG Configuration
CHROMA_PERSIST_DIRECTORY = str(BASE_DIR / "data" / "chroma_db")

# Streamlit Configuration
PAGE_TITLE = "Prior Auth Pipeline"
PAGE_ICON = "🩺"
