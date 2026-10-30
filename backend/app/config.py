"""Application configuration — reads from .env or environment variables."""
from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    database_url: str = f"sqlite+aiosqlite:///{ROOT_DIR / 'wordladder.db'}"
    redis_url: str = "redis://localhost:6379/0"
    redis_enabled: bool = True
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

    model_config = {"env_file": ".env", "en,kv_prefix": "WL_"}


settings = Settings()
