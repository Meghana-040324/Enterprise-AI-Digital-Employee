import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna").strip()

SERVICENOW_URL = os.getenv("SERVICENOW_URL", "").strip().rstrip("/")
SERVICENOW_USER = os.getenv("SERVICENOW_USER", "").strip()
SERVICENOW_PASSWORD = os.getenv("SERVICENOW_PASSWORD", "")

MAX_MEMORY_MESSAGES = int(os.getenv("MAX_MEMORY_MESSAGES", "12"))

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

MAX_FILE_SIZE_MB = 15
