"""SQLAlchemy async engine and session management."""
from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings

engine = create_async_engine(settings.database_url, echo=False)
async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    """FastAPI dependency — yields an async SQLAlchemy session."""
    async with async_session_factory() as session:
        yield session


async def init_db():
    """Upgrade the database to the latest Alembic revision."""
    async with engine.begin() as conn:
        def migrate(connection):
            from app import models  # noqa: F401

            alembic_cfg = Config(str(Path(__file__).resolve().parent.parent / "alembic.ini"))
            alembic_cfg.attributes["connection"] = connection
            tables = set(inspect(connection).get_table_names())
            required_legacy_tables = {
                "words",
                "graph_edges",
                "match_records",
                "move_records",
            }

            if (
                "alembic_version" not in tables
                and required_legacy_tables.issubset(tables)
            ):
                command.stamp(alembic_cfg, "280b92e91b41")
            command.upgrade(alembic_cfg, "head")

        await conn.run_sync(migrate)
