"""Match lifecycle orchestration: Redis state caching & DB persistence."""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import desc, select

from app.core import GameError, Match, MAX_LIVES, TIME_LIMITS
from app.database import async_session_factory
from app.models import MatchRecord, MoveRecord
from app.redis_client import cache_delete, cache_get, cache_set
from .graph_service import get_or_load_pack
from .synonym_service import find_hint

logger = logging.getLogger(__name__)

MATCH_TTL = 3600 * 24  # 24 hours in Redis


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class MatchService:

    @staticmethod
    async def create_match(
        lang: str,
        level: str,
        mode: str = "solo",
        play_all_parts: bool = False,
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
            "scores": match.scores,
            "lives": match.lives,
            "word_length": match.word_length,
            "used": list(match.used),
            "current": match.current,
            "to_move": match.to_move,
            "turn_started": time.time(),
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
                scores=match.scores,
                winner=match.winner,
                total_moves=0,
                created_at=_utcnow(),
            )
            session.add(record)
            await session.commit()

        return match.state()

    @staticmethod
    async def get_match_state(match_id: str) -> dict[str, Any]:
        # Try active Redis state
        raw = await cache_get(f"match:{match_id}")
        if raw:
            data = json.loads(raw)

            return {
                "match_id": data["match_id"],
                "part": data["part"],
                "scores": data["scores"],
                "lives": data.get("lives", [MAX_LIVES, MAX_LIVES]),
                "word_length": data.get("word_length", len(data.get("current", "")) or 4),
                "current_word": data["current"],
                "to_move": data["to_move"],
                "time_limit": TIME_LIMITS.get(data["level"], 80),
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

        # Rehydrate Match instance
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
        match.used = set(data["used"])
        match.current = data["current"]
        match.to_move = data["to_move"]
        match.turn_started = data.get("monotonic_turn", time.monotonic())
        match.finished = data["finished"]
        match.winner = data["winner"]
        match.last_event = data["last_event"]

        # Execute move
        state = match.play(player, word)

        # Persist MoveRecord
        async with async_session_factory() as session:
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
                record.total_moves = data.get("total_moves", 0) + 1
                if match.finished:
                    record.finished_at = _utcnow()
                    record.winner = match.winner
            await session.commit()

        # Update Redis cache
        data.update({
            "part": match.part,
            "scores": match.scores,
            "lives": match.lives,
            "word_length": match.word_length,
            "used": list(match.used),
            "current": match.current,
            "to_move": match.to_move,
            "monotonic_turn": time.monotonic(),
            "finished": match.finished,
            "winner": match.winner,
            "last_event": match.last_event,
            "total_moves": data.get("total_moves", 0) + 1,
        })
        await cache_set(f"match:{match.id}", json.dumps(data), ex=MATCH_TTL)

        return state

    @staticmethod
    async def timeout(match_id: str, player: int) -> dict[str, Any]:
        raw = await cache_get(f"match:{match_id}")
        if not raw:
            raise GameError("not_found", "Match not found or already archived")

        data = json.loads(raw)
        pack = await get_or_load_pack(data["lang"])

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
        match.used = set(data["used"])
        match.current = data["current"]
        match.to_move = data["to_move"]
        match.turn_started = 0.0
        match.finished = data["finished"]
        match.winner = data["winner"]
        match.last_event = data["last_event"]

        state = match.timeout(player)

        async with async_session_factory() as session:
            record = await session.get(MatchRecord, match_id)
            if record:
                record.scores = match.scores
                if match.finished:
                    record.finished_at = _utcnow()
                    record.winner = match.winner
            await session.commit()

        data.update({
            "part": match.part,
            "scores": match.scores,
            "lives": match.lives,
            "word_length": match.word_length,
            "used": list(match.used),
            "current": match.current,
            "to_move": match.to_move,
            "monotonic_turn": time.monotonic(),
            "finished": match.finished,
            "winner": match.winner,
            "last_event": match.last_event,
        })
        await cache_set(f"match:{match.id}", json.dumps(data), ex=MATCH_TTL)

        return state

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
            stmt = select(MatchRecord).where(MatchRecord.finished_at.is_not(None))
            if lang:
                stmt = stmt.where(MatchRecord.lang == lang)
            stmt = stmt.order_by(desc(MatchRecord.total_moves), desc(MatchRecord.finished_at)).limit(limit)

            rows = await session.execute(stmt)
            records = rows.scalars().all()

            results = []
            for rank, r in enumerate(records, start=1):
                results.append({
                    "rank": rank,
                    "match_id": r.id,
                    "lang": r.lang,
                    "level": r.level,
                    "mode": r.mode,
                    "scores": r.scores,
                    "winner": r.winner,
                    "total_moves": r.total_moves,
                    "finished_at": r.finished_at.isoformat() if r.finished_at else None,
                })
            return results
