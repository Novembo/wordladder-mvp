import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import delete, select

from app.config import settings
from app.database import async_session_factory
from app.models import LoginAttempt, MatchRecord, User, UserSession


@pytest.fixture(autouse=True)
def insecure_cookie_for_http_test_client(monkeypatch):
    monkeypatch.setattr(settings, "session_cookie_secure", False)


@pytest.mark.asyncio
async def test_register_login_session_csrf_and_logout(client: AsyncClient):
    username = f"Player_{uuid.uuid4().hex[:8]}"
    password = "secure test password"

    response = await client.post(
        "/v1/auth/register",
        json={"username": username, "password": password},
    )
    assert response.status_code == 201
    auth_data = response.json()
    assert auth_data["username"] == username
    assert "csrf_token" in auth_data
    cookie = response.headers["set-cookie"]
    assert "HttpOnly" in cookie
    assert "SameSite=lax" in cookie

    async with async_session_factory() as session:
        user = await session.scalar(
            select(User).where(User.username_normalized == username.casefold())
        )
        assert user is not None
        assert user.password_hash != password
        assert user.password_hash.startswith("$argon2")

    response = await client.get("/v1/auth/me")
    assert response.status_code == 200
    assert response.json()["id"] == auth_data["id"]

    response = await client.post(
        "/v1/matches",
        json={"lang": "en", "level": "basic", "mode": "solo"},
    )
    assert response.status_code == 403

    response = await client.post(
        "/v1/matches",
        json={"lang": "en", "level": "basic", "mode": "solo"},
        headers={"X-CSRF-Token": auth_data["csrf_token"]},
    )
    assert response.status_code == 201
    async with async_session_factory() as session:
        match = await session.get(MatchRecord, response.json()["match_id"])
        assert match is not None
        assert match.user_id == auth_data["id"]

    response = await client.post(
        "/v1/auth/logout",
        headers={"X-CSRF-Token": auth_data["csrf_token"]},
    )
    assert response.status_code == 204
    assert (await client.get("/v1/auth/me")).status_code == 401

    async with async_session_factory() as session:
        sessions = await session.scalars(
            select(UserSession).where(UserSession.user_id == auth_data["id"])
        )
        assert sessions.all() == []

    response = await client.post(
        "/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    assert response.json()["username"] == username


@pytest.mark.asyncio
async def test_username_is_case_insensitive_and_login_is_rate_limited(
    client: AsyncClient,
):
    username = f"Player_{uuid.uuid4().hex[:8]}"
    response = await client.post(
        "/v1/auth/register",
        json={"username": username, "password": "secure test password"},
    )
    assert response.status_code == 201

    response = await client.post(
        "/v1/auth/register",
        json={"username": username.swapcase(), "password": "secure test password"},
    )
    assert response.status_code == 409

    async with async_session_factory() as session:
        await session.execute(delete(LoginAttempt))
        await session.commit()

    for _ in range(5):
        response = await client.post(
            "/v1/auth/login",
            json={"username": username, "password": "incorrect password"},
        )
        assert response.status_code == 401

    response = await client.post(
        "/v1/auth/login",
        json={"username": username, "password": "secure test password"},
    )
    assert response.status_code == 429
