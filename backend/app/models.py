"""SQLAlchemy ORM models."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Float, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON, DateTime

from .database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Word(Base):
    """A single dictionary word for a given language."""

    __tablename__ = "words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(40), nullable=False)
    lang: Mapped[str] = mapped_column(String(5), nullable=False)
    length: Mapped[int] = mapped_column(Integer, nullable=False)
    frequency: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint("text", "lang", name="uq_word_lang"),
        Index("ix_word_lang_length", "lang", "length"),
    )


class GraphEdge(Base):
    """An edge between two words differing by one letter."""

    __tablename__ = "graph_edges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    word_a_id: Mapped[int] = mapped_column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False, index=True)
    word_b_id: Mapped[int] = mapped_column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("word_a_id", "word_b_id", name="uq_graph_edge"),
    )


class MatchRecord(Base):
    """Archived match (persisted once the match finishes)."""

    __tablename__ = "match_records"

    id: Mapped[str] = mapped_column(String(8), primary_key=True)
    lang: Mapped[str] = mapped_column(String(5), nullable=False)
    level: Mapped[str] = mapped_column(String(20), nullable=False)
    mode: Mapped[str] = mapped_column(String(10), nullable=False)
    scores: Mapped[list] = mapped_column(JSON, default=list)
    winner: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_moves: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class MoveRecord(Base):
    """Individual move within a match."""

    __tablename__ = "move_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    match_id: Mapped[str] = mapped_column(String(8), nullable=False, index=True)
    player: Mapped[int] = mapped_column(Integer, nullable=False)
    word: Mapped[str] = mapped_column(String(40), nullable=False)
    part: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
