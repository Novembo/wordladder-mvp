"""Redis client with graceful fallback to an in-memory dict.

If Redis is unreachable or disabled via ``WL_REDIS_ENABLED=false``, all
cache operations transparently use a process-local dictionary instead.
"""
from __future__ import annotations

import fnmatch
import logging

from .config import settings

logger = logging.getLogger(__name__)

_redis = None
_fallback: dict[str, str] = {}
_using_fallback = False


async def get_redis():
    """Return the async Redis client, or *None* if in fallback mode."""
    global _redis, _using_fallback
    if _using_fallback:
        return None
    if not settings.redis_enabled:
        _using_fallback = True
        logger.info("Redis disabled by config — using in-memory fallback")
        return None
    if _redis is None:
        try:
            import redis.asyncio as aioredis

            _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
            await _redis.ping()
            logger.info("Connected to Redis at %s", settings.redis_url)
        except Exception as exc:
            logger.warning("Redis unavailable (%s) — using in-memory fallback", exc)
            _redis = None
            _using_fallback = True
    return _redis


async def cache_get(key: str) -> str | None:
    r = await get_redis()
    if r:
        return await r.get(key)
    return _fallback.get(key)


async def cache_set(key: str, value: str, ex: int | None = None) -> None:
    r = await get_redis()
    if r:
        await r.set(key, value, ex=ex)
    else:
        _fallback[key] = value


async def cache_delete(key: str) -> None:
    r = await get_redis()
    if r:
        await r.delete(key)
    else:
        _fallback.pop(key, None)


async def cache_keys(pattern: str) -> list[str]:
    r = await get_redis()
    if r:
        return [k async for k in r.scan_iter(pattern)]
    return [k for k in _fallback if fnmatch.fnmatch(k, pattern)]


async def close_redis() -> None:
    global _redis
    if _redis:
        await _redis.aclose()
        _redis = None
