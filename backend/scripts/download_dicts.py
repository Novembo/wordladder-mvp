"""CLI script to download dictionaries and pre-generate language packs and database tables."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Add backend root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.config import settings
from app.database import init_db
from app.services.graph_service import build_and_save_pack


async def main(langs: list[str] | None = None):
    target_langs = langs or settings.supported_langs
    print(f"Initializing database at {settings.database_url}...")
    await init_db()

    for lang in target_langs:
        print(f"Building pack for '{lang}'...")
        pack = await build_and_save_pack(lang)
        playable_count = len(pack.graph)
        print(f"  -> '{lang}' complete: {playable_count} playable words in graph.")

    print("All packs generated successfully.")


if __name__ == "__main__":
    args = sys.argv[1:]
    asyncio.run(main(args if args else None))

