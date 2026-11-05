"""Application configuration — reads from .env or environment variables."""
from __future__ import annotations

from pathlib import Path
import secrets

from pydantic import Field
from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    database_url: str = f"sqlite+aiosqlite:///{ROOT_DIR / 'wordladder.db'}"
    redis_url: str = "redis://localhost:6379/0"
    redis_enabled: bool = True
    environment: str = "production"
    enable_db_reset: bool = False
    session_cookie_secure: bool = True
    session_cookie_name: str = "wordladder_session"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    auth_rate_limit_key: str = Field(
        default_factory=secrets.token_urlsafe,
        min_length=32,
    )
    dict_dir: str = str(ROOT_DIR / "data" / "dictionaries")
    pack_dir: str = str(ROOT_DIR / "data" / "packs")
    min_word_length: int = 3
    max_word_length: int = 8
    supported_langs: list[str] = ["en", "fr", "es"]

    # Developer / Author Information
    dev_prenom: str = "Obed .L .S"
    dev_nom: str = "VODOUHE"
    dev_email: str = "leonardovodouhe06@gmail.com"
    dev_contact: str = "+229 01 53 95 45 01"

    model_config = {"env_file": ".env", "env_prefix": "WL_"}

    @property
    def db_reset_enabled(self) -> bool:
        return self.environment.lower() == "development" and self.enable_db_reset

    @property
    def secure_session_cookie(self) -> bool:
        return self.session_cookie_secure and self.environment.lower() != "development"


settings = Settings()
