import pytest
from httpx import AsyncClient


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
