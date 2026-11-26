import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///chat_documents.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 20 * 1024 * 1024

    UPLOAD_FOLDER = BASE_DIR / "uploads"

    CHROMA_PATH = BASE_DIR / "chroma_db"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")