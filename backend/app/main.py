"""FastAPI application factory for Word Ladder MVP."""
from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db
from .redis_client import close_redis, get_redis
from .routers import auth, leaderboard, matches, maintenance, packs, ws
from .schemas import HealthResponse
from .services.graph_service import get_or_load_pack


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist and warm up English starter pack
    await init_db()
    try:
        await get_redis()
        # Warm-up default language pack asynchronously
        await get_or_load_pack("en")
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning("Warmup notice: %s", exc)
    yield
    # Shutdown
    await close_redis()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Word Ladder EdTech API",
        version="1.0.0",
        description="Educational Word Ladder game API with real-time state caching, vocab levels & multilingual graph.",
        lifespan=lifespan,
    )

    # Enable CORS for local Vite development & mobile devices
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "X-CSRF-Token"],
    )

    # Include routers
    app.include_router(auth.router)
    app.include_router(matches.router)
    app.include_router(packs.router)
    app.include_router(leaderboard.router)
    app.include_router(maintenance.router)
    app.include_router(ws.router)

    @app.get("/")
    async def root():
        return {
            "title": "Word Ladder EdTech API",
            "version": "1.0.0",
            "description": "Jeu éducatif de vocabulaire multilingue",
            "developpeur": {
                "prenom": settings.dev_prenom,
                "nom": settings.dev_nom,
                "email": settings.dev_email,
                "contact": settings.dev_contact,
            },
            "endpoints": {
                "documentation": "/docs",
                "sante": "/health",
                "niveaux": "/v1/levels",
                "classement": "/v1/leaderboard",
                "matchs": "/v1/matches",
            }
        }

    @app.get("/health", response_model=HealthResponse)
    async def health():
        redis_client = await get_redis()
        return {
            "status": "healthy",
            "redis": "connected" if redis_client else "in-memory-fallback",
            "database": "sqlite-aiosqlite",
            "languages": settings.supported_langs,
        }

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
