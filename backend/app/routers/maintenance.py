"""Development-only database maintenance endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models import MatchRecord, MoveRecord
from app.routers.auth import AuthContext, require_csrf
from app.schemas import DatabaseResetResponse, ResetAvailability

router = APIRouter(prefix="/v1/maintenance", tags=["development"])


@router.get("/reset", response_model=ResetAvailability)
async def reset_availability():
    return {"enabled": settings.db_reset_enabled}


@router.post("/reset", response_model=DatabaseResetResponse)
async def reset_match_history(
    _auth: AuthContext | None = Depends(require_csrf),
    db: AsyncSession = Depends(get_db),
):
    if not settings.db_reset_enabled:
        raise HTTPException(status_code=404, detail="Not found")

    archived_match_ids = select(MatchRecord.id).where(MatchRecord.finished_at.is_not(None))
    move_result = await db.execute(
        delete(MoveRecord).where(MoveRecord.match_id.in_(archived_match_ids))
    )
    match_result = await db.execute(
        delete(MatchRecord).where(MatchRecord.finished_at.is_not(None))
    )
    await db.commit()

    return {
        "deleted_matches": match_result.rowcount or 0,
        "deleted_moves": move_result.rowcount or 0,
    }
