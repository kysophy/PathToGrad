from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str = (
        "mysql+pymysql://root:pathtograd@localhost:3306/pathtograd"
    )

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GEMINI_TIMEOUT_MS: int = 20000
    DEFAULT_TERM_ID: str = "TERM-2026-1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
