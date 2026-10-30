"""Pydantic request / response schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


# ── Requests ──────────────────────────────────────────────────────────

class NewMatchRequest(BaseModel):
    lang: str = Field(examples=["fr"])
    level: str = Field(examples=["basic"])
    mode: str = Field(default="solo", examples=["solo", "duo"])
    play_all_parts: bool = False


class MoveRequest(BaseModel):
    player: int = Field(ge=0, le=1)
    word: str = Field(min_length=1, max_length=40)


class TimeoutRequest(BaseModel):
    player: int = Field(ge=0, le=1)


# ── Responses ─────────────────────────────────────────────────────────

class MatchState(BaseModel):
    match_id: str
    part: int
    scores: list[int]
    lives: list[int] = [3, 3]
    word_length: int = 4
    current_word: str
    to_move: int
    time_limit: int
    used_count: int
    finished: bool
    winner: int | None
    event: str


class HintResponse(BaseModel):
    match_id: str
    hint_type: str = "synonym"
    word_length: int
    clue: str


class ErrorDetail(BaseModel):
    code: str
    message: str
    state: MatchState | None = None


class PackInfo(BaseModel):
    lang: str
    version: str
    word_count: int
    playable_count: int
    levels: list[str]


class LeaderboardEntry(BaseModel):
    rank: int
    match_id: str
    lang: str
    level: str
    mode: str
    scores: list[int]
    winner: int | None
    total_moves: int
    finished_at: str | None


class HealthResponse(BaseModel):
    status: str
    redis: str
    database: str
    languages: list[str]
