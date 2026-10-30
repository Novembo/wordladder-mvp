"""Leaderboard endpoint: /v1/leaderboard"""
from __future__ import annotations

from fastapi import APIRouter, Query

try:
    from app.schemas import LeaderboardEntry
    from app.services.match_service import MatchService
except (ImportError, ValueError):
    from ..schemas import LeaderboardEntry
    from ..services.match_service import MatchService

router = APIRouter(prefix="/v1/leaderboard", tags=["leaderboard"])


@router.get("", response_model=list[LeaderboardEntry])
async def get_leaderboard(
    lang: str | None = Query(None, description="Filter by language"),
    limit: int = Query(50, ge=1, le=100),
):
    return await MatchService.get_leaderboard(lang=lang, limit=limit)

