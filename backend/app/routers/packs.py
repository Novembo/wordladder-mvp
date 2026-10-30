"""Pack and language endpoints: /v1/packs/* and /v1/levels"""
from __future__ import annotations

from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

try:
    from app.config import settings
    from app.core import TIME_LIMITS
    from app.schemas import PackInfo
    from app.services.graph_service import get_or_load_pack
except (ImportError, ValueError):
    from ..config import settings
    from ..core import TIME_LIMITS
    from ..schemas import PackInfo
    from ..services.graph_service import get_or_load_pack

router = APIRouter(tags=["packs"])


@router.get("/v1/levels")
def get_levels():
    return {"time_limits_seconds": TIME_LIMITS}


@router.get("/v1/packs/{lang}/info", response_model=PackInfo)
async def get_pack_info(lang: str):
    if lang not in settings.supported_langs:
        raise HTTPException(status_code=404, detail=f"Unsupported language: {lang}")
    pack = await get_or_load_pack(lang)
    return {
        "lang": pack.lang,
        "version": pack.version,
        "word_count": len(pack.graph),
        "playable_count": len([w for w, nbs in pack.graph.items() if nbs]),
        "levels": list(pack.level_words.keys()),
    }


@router.get("/v1/packs/{lang}")
async def download_pack(lang: str):
    """Download full pack JSON for offline client caching."""
    if lang not in settings.supported_langs:
        raise HTTPException(status_code=404, detail=f"Unsupported language: {lang}")
    await get_or_load_pack(lang)
    path = Path(settings.pack_dir) / f"{lang}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Pack file not found for {lang}")
    return FileResponse(path, media_type="application/json")

