"""Match management endpoints: /v1/matches/*"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.routers.auth import AuthContext, require_csrf
from app.core import GameError
from app.schemas import HintResponse, MatchState, MoveRequest, NewMatchRequest, TimeoutRequest
from app.services.match_service import MatchService


router = APIRouter(prefix="/v1/matches", tags=["matches"])


def handle_game_error(err: GameError):
    status_code = 404 if err.code == "not_found" else 422
    raise HTTPException(
        status_code=status_code,
        detail={"code": err.code, "message": err.message},
    )


@router.post("", response_model=MatchState, status_code=201)
async def create_match(
    body: NewMatchRequest,
    auth: AuthContext | None = Depends(require_csrf),
):
    try:
        return await MatchService.create_match(
            lang=body.lang,
            level=body.level,
            mode=body.mode,
            play_all_parts=body.play_all_parts,
            user_id=auth.user.id if auth else None,
        )
    except GameError as err:
        handle_game_error(err)


@router.get("/{match_id}", response_model=MatchState)
async def get_match(match_id: str):
    try:
        return await MatchService.get_match_state(match_id)
    except GameError as err:
        handle_game_error(err)


@router.post("/{match_id}/moves", response_model=MatchState)
async def play_move(
    match_id: str,
    body: MoveRequest,
    _auth: AuthContext | None = Depends(require_csrf),
):
    try:
        return await MatchService.play_move(match_id, body.player, body.word)
    except GameError as err:
        handle_game_error(err)


@router.post("/{match_id}/timeout", response_model=MatchState)
async def declare_timeout(
    match_id: str,
    body: TimeoutRequest,
    _auth: AuthContext | None = Depends(require_csrf),
):
    try:
        return await MatchService.timeout(match_id, body.player)
    except GameError as err:
        handle_game_error(err)


@router.post("/{match_id}/hint", response_model=HintResponse)
async def get_hint(match_id: str):
    try:
        return await MatchService.get_hint(match_id)
    except GameError as err:
        handle_game_error(err)
