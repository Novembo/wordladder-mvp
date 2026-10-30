"""Graph build, pack serialization, Redis caching, and DB sync."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any
import msgpack
from sqlalchemy import insert, select

from ..config import settings
from ..core import Pack, build_graph
from ..database import async_session_factory
from ..models import GraphEdge, Word
from ..redis_client import cache_get, cache_set
from .dictionary import download_dictionary, partition_levels

logger = logging.getLogger(__name__)

_memory_packs: dict[str, Pack] = {}


def pack_to_dict(pack: Pack) -> dict[str, Any]:
    return {
        "lang": pack.lang,
        "version": pack.version,
        "graph": {w: sorted(nbs) for w, nbs in pack.graph.items()},
        "levels": {lvl: sorted(ws) for lvl, ws in pack.level_words.items()},
    }


def dict_to_pack(data: dict[str, Any]) -> Pack:
    return Pack(
        lang=data["lang"],
        version=data.get("version", "1.0.0"),
        graph={w: set(nbs) for w, nbs in data["graph"].items()},
        level_words={lvl: set(ws) for lvl, ws in data["levels"].items()},
    )


async def get_or_load_pack(lang: str) -> Pack:
    """Retrieve pack from in-memory cache, Redis msgpack, disk JSON, or auto-generate."""
    if lang in _memory_packs:
        return _memory_packs[lang]

    # 1. Try Redis cache
    redis_key = f"pack:{lang}"
    cached = await cache_get(redis_key)
    if cached:
        try:
            try:
                data = msgpack.unpackb(bytes.fromhex(cached), raw=False)
            except Exception:
                data = json.loads(cached)
            pack = dict_to_pack(data)
            _memory_packs[lang] = pack
            return pack
        except Exception as e:
            logger.warning("Failed parsing cached pack for %s: %s", lang, e)

    # 2. Try disk pack JSON
    pack_dir = Path(settings.pack_dir)
    pack_dir.mkdir(parents=True, exist_ok=True)
    json_path = pack_dir / f"{lang}.json"

    if json_path.exists():
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            pack = dict_to_pack(data)
            _memory_packs[lang] = pack
            await cache_pack(pack)
            return pack
        except Exception as e:
            logger.warning("Failed loading pack %s from file: %s", json_path, e)

    # 3. Build pack from dictionary
    pack = await build_and_save_pack(lang)
    _memory_packs[lang] = pack
    return pack


async def cache_pack(pack: Pack) -> None:
    try:
        data = pack_to_dict(pack)
        packed = msgpack.packb(data, use_bin_type=True).hex()
        await cache_set(f"pack:{pack.lang}", packed)
    except Exception as exc:
        logger.warning("Could not cache pack in Redis: %s", exc)


async def build_and_save_pack(lang: str) -> Pack:
    """Build pack from wordlist, save to JSON and cache in Redis."""
    words = download_dictionary(lang)
    raw_graph = build_graph(words)
    playable = {w for w, nbs in raw_graph.items() if nbs}
    graph = {w: raw_graph[w] for w in playable}

    partitions = partition_levels(list(playable))
    level_words = {
        lvl: {w for w in ws if w in playable}
        for lvl, ws in partitions.items()
    }

    pack = Pack(
        lang=lang,
        version="1.0.0",
        graph=graph,
        level_words=level_words,
    )

    # Save to disk
    pack_dir = Path(settings.pack_dir)
    pack_dir.mkdir(parents=True, exist_ok=True)
    json_path = pack_dir / f"{lang}.json"
    data = pack_to_dict(pack)
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Cache in Redis
    await cache_pack(pack)
    _memory_packs[lang] = pack

    # Batch insert into DB
    try:
        await sync_pack_to_db(pack)
    except Exception as exc:
        logger.warning("Could not sync pack %s to DB: %s", lang, exc)

    return pack


async def sync_pack_to_db(pack: Pack) -> None:
    """Fast batch insertion of words and graph edges into SQLite."""
    async with async_session_factory() as session:
        existing = await session.execute(
            select(Word.id).where(Word.lang == pack.lang).limit(1)
        )
        if existing.scalar() is not None:
            return

        # 1. Insert words
        word_items = [
            {"text": w, "lang": pack.lang, "length": len(w), "frequency": 1.0}
            for w in pack.graph
        ]
        if word_items:
            await session.execute(insert(Word), word_items)
            await session.commit()

        # 2. Map word to id
        rows = await session.execute(
            select(Word.id, Word.text).where(Word.lang == pack.lang)
        )
        word_map = {text: wid for wid, text in rows}

        # 3. Insert unique undirected edges
        edges_set = set()
        edge_items = []
        for w, nbs in pack.graph.items():
            u = word_map.get(w)
            if not u:
                continue
            for nb in nbs:
                v = word_map.get(nb)
                if not v or u == v:
                    continue
                pair = (min(u, v), max(u, v))
                if pair not in edges_set:
                    edges_set.add(pair)
                    edge_items.append({"word_a_id": pair[0], "word_b_id": pair[1]})

        if edge_items:
            # Batch in chunks of 5000 to respect SQLite limits
            chunk_size = 5000
            for i in range(0, len(edge_items), chunk_size):
                chunk = edge_items[i:i + chunk_size]
                await session.execute(insert(GraphEdge), chunk)
            await session.commit()
