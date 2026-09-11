from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root:
# document_intelligence/
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    DATABASE_URL: str = "sqlite:///./document_intelligence.db"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()