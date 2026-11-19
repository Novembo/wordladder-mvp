"""Match lifecycle orchestration: Redis state caching & DB persistence."""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import desc, select

from app.core import GameError, Match, Pack, MAX_LIVES, TIME_LIMITS
from app.database import async_session_factory
from app.models import MatchRecord, MoveRecord, User
from app.redis_client import cache_delete, cache_get, cache_set
from .graph_service import get_or_load_pack
from .synonym_service import find_hint

logger = logging.getLogger(__name__)

MATCH_TTL = 3600 * 24  # 24 hours in Redis


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _deadline_timestamp(time_limit: int) -> float:
    return time.time() + time_limit


def _deadline_iso(timestamp: float | None) -> str | None:
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()


def _match_from_data(data: dict[str, Any], pack: Pack) -> Match:
    match = Match.__new__(Match)
    match.pack = pack
    match.level = data["level"]
    match.mode = data["mode"]
    match.play_all_parts = data["play_all_parts"]
    match.rng = Match.__dataclass_fields__["rng"].default_factory()
    match.id = data["match_id"]
    match.scores = list(data["scores"])
    match.lives = list(data.get("lives", [MAX_LIVES, MAX_LIVES]))
    match.word_length = data.get("word_length", len(data["current"]))
    match.part = data["part"]
    match.time_adjustment = data.get("time_adjustment", 0)
    match.used = set(data["used"])
    match.current = data["current"]
    match.to_move = data["to_move"]
    match.finished = data["finished"]
    match.winner = data["winner"]
    match.last_event = data["last_event"]
    deadline = data.get("deadline_at")
    if deadline is None:
        # Existing Redis entries get one deadline when first read after upgrade.
        deadline = _deadline_timestamp(data.get("time_limit", TIME_LIMITS.get(match.level, 80)))
        data["deadline_at"] = deadline
    remaining = max(0.0, deadline - time.time())
    match.turn_started = time.monotonic() - max(0.0, match.time_limit - remaining)
    return match


def _state_with_deadline(match: Match, deadline: float) -> dict[str, Any]:
    return {**match.state(), "deadline_at": _deadline_iso(deadline)}


class MatchService:

    @staticmethod
    async def create_match(
        lang: str,
        level: str,
        mode: str = "solo",
        play_all_parts: bool = False,
        user_id: int | None = None,
    ) -> dict[str, Any]:
        pack = await get_or_load_pack(lang)
        match = Match(
            pack=pack,
            level=level,
            mode=mode,
            play_all_parts=play_all_parts,
        )

        match_data = {
            "match_id": match.id,
            "lang": lang,
            "level": level,
            "mode": mode,
            "play_all_parts": play_all_parts,
            "part": match.part,
            "time_adjustment": match.time_adjustment,
            "time_limit": match.time_limit,
            "scores": match.scores,
            "lives": match.lives,
            "word_length": match.word_length,
            "used": list(match.used),
            "current": match.current,
            "to_move": match.to_move,
            "deadline_at": _deadline_timestamp(match.time_limit),
            "finished": match.finished,
            "winner": match.winner,
            "last_event": match.last_event,
            "total_moves": 0,
        }

        # Cache in Redis
        await cache_set(f"match:{match.id}", json.dumps(match_data), ex=MATCH_TTL)

        # Create record in DB
        async with async_session_factory() as session:
            record = MatchRecord(
                id=match.id,
                lang=lang,
                level=level,
                mode=mode,
                user_id=user_id,
                scores=match.scores,
                winner=match.winner,
                total_moves=0,
                created_at=_utcnow(),
            )
            session.add(record)
            await session.commit()

        return _state_with_deadline(match, match_data["deadline_at"])

    @staticmethod
    async def get_match_state(match_id: str) -> dict[str, Any]:
        # Try active Redis state
        raw = await cache_get(f"match:{match_id}")
        if raw:
            data = json.loads(raw)
            deadline = data.get("deadline_at")
            if deadline is None:
                deadline = _deadline_timestamp(data.get("time_limit", TIME_LIMITS.get(data["level"], 80)))
                data["deadline_at"] = deadline
                await cache_set(f"match:{match_id}", json.dumps(data), ex=MATCH_TTL)

            return {
                "match_id": data["match_id"],
                "part": data["part"],
                "scores": data["scores"],
                "lives": data.get("lives", [MAX_LIVES, MAX_LIVES]),
                "word_length": data.get("word_length", len(data.get("current", "")) or 4),
                "current_word": data["current"],
                "to_move": data["to_move"],
                "time_limit": data.get("time_limit", TIME_LIMITS.get(data["level"], 80)),
                "deadline_at": _deadline_iso(deadline),
                "used_count": len(data["used"]),
                "finished": data["finished"],
                "winner": data["winner"],
                "event": data["last_event"],
            }

        # Fallback to DB archived match
        async with async_session_factory() as session:
            record = await session.get(MatchRecord, match_id)
            if not record:
                raise GameError("not_found", "Match not found")
            return {
                "match_id": record.id,
                "part": 3,
                "scores": record.scores,
                "lives": [0, 0],
                "word_length": 4,
                "current_word": "",
                "to_move": 0,
                "time_limit": 80,
                "deadline_at": None,
                "used_count": record.total_moves,
                "finished": True,
                "winner": record.winner,
                "event": "archived",
            }

    @staticmethod
    async def play_move(match_id: str, player: int, word: str) -> dict[str, Any]:
        raw = await cache_get(f"match:{match_id}")
        if not raw:
            raise GameError("not_found", "Match not found or already archived")

        data = json.loads(raw)
        pack = await get_or_load_pack(data["lang"])
        match = _match_from_data(data, pack)

        # Enforce server-side deadline
        deadline = data.get("deadline_at")
        if deadline and time.time() > deadline:
            state = match.timeout(player)
        else:
            # Execute move
            state = match.play(player, word)

        # Persist MoveRecord if it was a valid move (even if it ends the part)
        async with async_session_factory() as session:
            event = state.get("event", "")
            is_valid_move = "move_ok" in event or "dead_end" in event
            
            if is_valid_move:
                move_rec = MoveRecord(
                    match_id=match_id,
                    player=player,
                    word=word,
                    part=match.part,
                    created_at=_utcnow(),
                )
                session.add(move_rec)

            record = await session.get(MatchRecord, match_id)
            if record:
                record.scores = match.scores
                if is_valid_move:
                    record.total_moves = (record.total_moves or 0) + 1
                if match.finished:
                    record.finished_at = _utcnow()
                    record.winner = match.winner
            await session.commit()

        # Update Redis cache
        deadline = _deadline_timestamp(match.time_limit)
        data.update({
            "part": match.part,
            "time_adjustment": match.time_adjustment,
            "time_limit": match.time_limit,
            "scores": match.scores,
            "lives": match.lives,
            "word_length": match.word_length,
            "used": list(match.used),
            "current": match.current,
            "to_move": match.to_move,
            "deadline_at": deadline,
            "finished": match.finished,
            "winner": match.winner,
            "last_event": match.last_event,
            "total_moves": (data.get("total_moves", 0) + 1) if is_valid_move else data.get("total_moves", 0),
        })
        await cache_set(f"match:{match.id}", json.dumps(data), ex=MATCH_TTL)

        return {**state, "deadline_at": _deadline_iso(deadline)}

    @staticmethod
    async def timeout(match_id: str, player: int) -> dict[str, Any]:
        raw = await cache_get(f"match:{match_id}")
        if not raw:
            raise GameError("not_found", "Match not found or already archived")

        data = json.loads(raw)
        pack = await get_or_load_pack(data["lang"])

        deadline = data.get("deadline_at")
        if deadline is None:
            deadline = _deadline_timestamp(data.get("time_limit", TIME_LIMITS.get(data["level"], 80)))
            data["deadline_at"] = deadline
            await cache_set(f"match:{match_id}", json.dumps(data), ex=MATCH_TTL)
        if time.time() < deadline:
            raise GameError("too_early", "Le temps du tour n’est pas encore écoulé.")

        match = _match_from_data(data, pack)

        state = match.timeout(player)

        async with async_session_factory() as session:
            record = await session.get(MatchRecord, match_id)
            if record:
                record.scores = match.scores
                if match.finished:
                    record.finished_at = _utcnow()
                    record.winner = match.winner
            await session.commit()

        deadline = _deadline_timestamp(match.time_limit)
        data.update({
            "part": match.part,
            "time_adjustment": match.time_adjustment,
            "time_limit": match.time_limit,
            "scores": match.scores,
            "lives": match.lives,
            "word_length": match.word_length,
            "used": list(match.used),
            "current": match.current,
            "to_move": match.to_move,
            "deadline_at": deadline,
            "finished": match.finished,
            "winner": match.winner,
            "last_event": match.last_event,
        })
        await cache_set(f"match:{match.id}", json.dumps(data), ex=MATCH_TTL)

        return {**state, "deadline_at": _deadline_iso(deadline)}

    @staticmethod
    async def get_hint(match_id: str) -> dict[str, Any]:
        raw = await cache_get(f"match:{match_id}")
        if not raw:
            raise GameError("not_found", "Match not found")

        data = json.loads(raw)
        pack = await get_or_load_pack(data["lang"])
        current_word = data["current"]
        used = set(data["used"])
        available = pack.graph.get(current_word, set()) - used

        hint = find_hint(current_word, available, data["lang"])
        return {
            "match_id": match_id,
            "hint_type": hint["hint_type"],
            "word_length": hint["word_length"],
            "clue": hint["clue"],
        }

    @staticmethod
    async def get_leaderboard(lang: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
        async with async_session_factory() as session:
            stmt = (
                select(MatchRecord, User.username)
                .outerjoin(User, MatchRecord.user_id == User.id)
                .where(MatchRecord.finished_at.is_not(None))
            )
            if lang:
                stmt = stmt.where(MatchRecord.lang == lang)
            stmt = stmt.order_by(desc(MatchRecord.total_moves), desc(MatchRecord.finished_at)).limit(limit)

            rows = await session.execute(stmt)
            records = rows.all()

            results = []
            for rank, (r, username) in enumerate(records, start=1):
                results.append({
                    "rank": rank,
                    "match_id": r.id,
                    "lang": r.lang,
                    "level": r.level,
                    "mode": r.mode,
                    "username": username,
                    "scores": r.scores,
                    "winner": r.winner,
                    "total_moves": r.total_moves,
                    "finished_at": r.finished_at.isoformat() if r.finished_at else None,
                })
            return results
