from datetime import datetime, timezone

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.config import settings
from app.database import async_session_factory
from app.models import MatchRecord, MoveRecord, Word


@pytest.mark.asyncio
async def test_health_and_levels(client: AsyncClient):
    r = await client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
    assert "en" in data["languages"]

    r = await client.get("/v1/levels")
    assert r.status_code == 200
    limits = r.json()["time_limits_seconds"]
    assert limits["basic"] == 80
    assert limits["intermediate"] == 60
    assert limits["advanced"] == 40


@pytest.mark.asyncio
async def test_match_flow_api(client: AsyncClient):
    # 1. Create a duo match
    res = await client.post("/v1/matches", json={"lang": "en", "level": "basic", "mode": "duo"})
    assert res.status_code == 201
    state = res.json()
    match_id = state["match_id"]
    assert state["finished"] is False
    assert state["to_move"] == 0
    assert state["lives"] == [3, 3]
    assert state["word_length"] > 0

    # 2. Query match status
    res = await client.get(f"/v1/matches/{match_id}")
    assert res.status_code == 200
    assert res.json()["match_id"] == match_id

    # 3. Test wrong player move rejection
    res = await client.post(
        f"/v1/matches/{match_id}/moves",
        json={"player": 1, "word": "cold"}
    )
    assert res.status_code == 422
    assert res.json()["detail"]["code"] == "not_your_turn"

    # 4. Request a pedagogical hint / synonym
    res = await client.post(f"/v1/matches/{match_id}/hint")
    assert res.status_code == 200
    hint = res.json()
    assert "clue" in hint
    assert hint["word_length"] == state["word_length"]

    # 5. Trigger timeout: should reduce player 0 lives from 3 to 2, still in part 1
    res = await client.post(f"/v1/matches/{match_id}/timeout", json={"player": 0})
    assert res.status_code == 200
    updated = res.json()
    assert updated["lives"] == [2, 3]
    assert updated["part"] == 1

    # 6. Check pack info
    res = await client.get("/v1/packs/en/info")
    assert res.status_code == 200
    assert res.json()["lang"] == "en"

    # 7. Leaderboard
    res = await client.get("/v1/leaderboard")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


@pytest.mark.asyncio
async def test_adaptive_timer_persists_between_parts(client: AsyncClient):
    response = await client.post(
        "/v1/matches",
        json={"lang": "en", "level": "basic", "mode": "duo"},
    )
    match_id = response.json()["match_id"]

    for _ in range(3):
        response = await client.post(
            f"/v1/matches/{match_id}/timeout",
            json={"player": 0},
        )
        assert response.status_code == 200

    assert response.json()["part"] == 2
    assert response.json()["time_limit"] == 90

    response = await client.get(f"/v1/matches/{match_id}")
    assert response.json()["time_limit"] == 90


@pytest.mark.asyncio
async def test_database_reset_is_development_only_and_preserves_dictionary(
    client: AsyncClient, monkeypatch
):
    monkeypatch.setattr(settings, "environment", "production")
    monkeypatch.setattr(settings, "enable_db_reset", True)

    response = await client.get("/v1/maintenance/reset")
    assert response.json() == {"enabled": False}
    response = await client.post("/v1/maintenance/reset")
    assert response.status_code == 404

    monkeypatch.setattr(settings, "environment", "development")
    async with async_session_factory() as session:
        session.add(Word(text="keep", lang="en", length=4))
        session.add(
            MatchRecord(
                id="active01",
                lang="en",
                level="basic",
                mode="duo",
                scores=[1, 0],
                winner=0,
                total_moves=1,
                finished_at=None,
            )
        )
        await session.flush()
        finished_match = MatchRecord(
            id="done0001",
            lang="en",
            level="basic",
            mode="duo",
            scores=[2, 0],
            winner=0,
            total_moves=1,
        )
        finished_match.finished_at = datetime.now(timezone.utc)
        session.add(finished_match)
        session.add_all(
            [
                MoveRecord(match_id="active01", player=0, word="cold", part=1),
                MoveRecord(match_id="done0001", player=0, word="cord", part=1),
            ]
        )
        await session.commit()

    response = await client.post("/v1/maintenance/reset")
    assert response.status_code == 200
    assert response.json() == {"deleted_matches": 1, "deleted_moves": 1}

    async with async_session_factory() as session:
        assert await session.get(MatchRecord, "active01") is not None
        assert await session.get(MatchRecord, "done0001") is None
        remaining_moves = await session.execute(
            select(MoveRecord).where(MoveRecord.match_id == "active01")
        )
        assert len(remaining_moves.scalars().all()) == 1
        words = await session.execute(select(Word.id).limit(1))
        assert words.scalar_one_or_none() is not None
