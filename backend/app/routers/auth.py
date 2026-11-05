"""Account registration, login, and server-side browser sessions."""
from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field
from pwdlib import PasswordHash
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models import LoginAttempt, User, UserSession

router = APIRouter(prefix="/v1/auth", tags=["auth"])
password_hash = PasswordHash.recommended()
_DUMMY_PASSWORD_HASH = password_hash.hash("invalid-login-dummy")
SESSION_TTL = timedelta(days=30)
LOGIN_WINDOW = timedelta(minutes=15)
MAX_LOGIN_ATTEMPTS = 5


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[A-Za-z0-9_]+$")
    password: str = Field(min_length=8, max_length=128)


class AuthUser(BaseModel):
    id: int
    username: str
    csrf_token: str


@dataclass(frozen=True)
class AuthContext:
    user: User
    session: UserSession


def _token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _ip_digest(ip_address: str) -> str:
    return hmac.new(
        settings.auth_rate_limit_key.encode("utf-8"),
        ip_address.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=int(SESSION_TTL.total_seconds()),
        httponly=True,
        secure=settings.secure_session_cookie,
        samesite="lax",
        path="/",
    )


async def get_optional_auth(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> AuthContext | None:
    token = request.cookies.get(settings.session_cookie_name)
    if not token:
        return None

    session = await db.get(UserSession, _token_digest(token))
    now = _utcnow()
    if session is None or session.expires_at <= now:
        if session is not None:
            await db.delete(session)
            await db.commit()
        return None

    user = await db.get(User, session.user_id)
    if user is None:
        await db.delete(session)
        await db.commit()
        return None
    return AuthContext(user=user, session=session)


async def require_csrf(
    request: Request,
    auth: AuthContext | None = Depends(get_optional_auth),
) -> AuthContext | None:
    if auth is not None:
        supplied = request.headers.get("x-csrf-token", "")
        if not hmac.compare_digest(supplied, auth.session.csrf_token):
            raise HTTPException(status_code=403, detail="Invalid CSRF token")
    return auth


async def require_auth(
    auth: AuthContext | None = Depends(get_optional_auth),
) -> AuthContext:
    if auth is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return auth


async def _create_session(
    user: User,
    db: AsyncSession,
    response: Response,
) -> AuthUser:
    raw_token = secrets.token_urlsafe(32)
    csrf_token = secrets.token_urlsafe(32)
    session = UserSession(
        token_hash=_token_digest(raw_token),
        csrf_token=csrf_token,
        user_id=user.id,
        expires_at=_utcnow() + SESSION_TTL,
    )
    db.add(session)
    await db.commit()
    _set_session_cookie(response, raw_token)
    return AuthUser(id=user.id, username=user.username, csrf_token=csrf_token)


async def _failed_login_count(
    db: AsyncSession, username: str, ip_hash: str, now: datetime
) -> int:
    count = await db.scalar(
        select(func.count(LoginAttempt.id)).where(
            LoginAttempt.created_at >= now - LOGIN_WINDOW,
            or_(
                LoginAttempt.username_normalized == username,
                LoginAttempt.ip_hash == ip_hash,
            ),
        )
    )
    return count or 0


async def _record_failed_login(
    db: AsyncSession, username: str, ip_hash: str, now: datetime
) -> None:
    await db.execute(
        LoginAttempt.__table__.delete().where(
            LoginAttempt.created_at < now - timedelta(days=1)
        )
    )
    db.add(
        LoginAttempt(
            username_normalized=username,
            ip_hash=ip_hash,
            created_at=now,
        )
    )
    await db.commit()


def _validate_origin(request: Request) -> None:
    origin = request.headers.get("origin")
    if origin and origin not in settings.cors_origins:
        raise HTTPException(status_code=403, detail="Origin not allowed")


@router.post("/register", response_model=AuthUser, status_code=201)
async def register(
    credentials: Credentials,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    _validate_origin(request)
    username = credentials.username.strip()
    normalized = username.casefold()
    user = User(
        username=username,
        username_normalized=normalized,
        password_hash=password_hash.hash(credentials.password),
    )
    db.add(user)
    try:
        await db.flush()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Ce pseudo est déjà utilisé") from None
    await db.commit()
    await db.refresh(user)
    return await _create_session(user, db, response)


@router.post("/login", response_model=AuthUser)
async def login(
    credentials: Credentials,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    _validate_origin(request)
    username = credentials.username.strip().casefold()
    client_ip = request.client.host if request.client else "unknown"
    ip_hash = _ip_digest(client_ip)
    now = _utcnow()
    if await _failed_login_count(db, username, ip_hash, now) >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(status_code=429, detail="Trop de tentatives. Réessayez dans 15 minutes.")

    user = await db.scalar(
        select(User).where(User.username_normalized == username)
    )
    stored_hash = user.password_hash if user else _DUMMY_PASSWORD_HASH
    valid_password = password_hash.verify(credentials.password, stored_hash)
    if user is None or not valid_password:
        await _record_failed_login(db, username, ip_hash, now)
        raise HTTPException(status_code=401, detail="Pseudo ou mot de passe incorrect")

    return await _create_session(user, db, response)


@router.get("/me", response_model=AuthUser)
async def me(auth: AuthContext = Depends(require_auth)):
    return AuthUser(
        id=auth.user.id,
        username=auth.user.username,
        csrf_token=auth.session.csrf_token,
    )


@router.post("/logout", status_code=204)
async def logout(
    request: Request,
    response: Response,
    auth: AuthContext | None = Depends(require_csrf),
    db: AsyncSession = Depends(get_db),
):
    _validate_origin(request)
    if auth is not None:
        await db.delete(auth.session)
        await db.commit()
    response.delete_cookie(
        settings.session_cookie_name,
        path="/",
        secure=settings.secure_session_cookie,
        httponly=True,
        samesite="lax",
    )
