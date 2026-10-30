"""WebSocket endpoint for real-time duo multiplayer match synchronization."""
from __future__ import annotations

import json
import logging
from collections import defaultdict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.match_service import MatchService


logger = logging.getLogger(__name__)
router = APIRouter(tags=["websocket"])

# Active connections by match_id
_connections: dict[str, set[WebSocket]] = defaultdict(set)


async def broadcast_match_state(match_id: str, state: dict):
    clients = _connections.get(match_id, set())
    for ws in list(clients):
        try:
            await ws.send_text(json.dumps(state))
        except Exception:
            clients.discard(ws)


@router.websocket("/ws/matches/{match_id}")
async def match_websocket(websocket: WebSocket, match_id: str):
    await websocket.accept()
    _connections[match_id].add(websocket)

    try:
        # Send initial state
        state = await MatchService.get_match_state(match_id)
        await websocket.send_text(json.dumps(state))

        while True:
            # Keep connection alive & handle incoming client events
            data = await websocket.receive_text()
            payload = json.loads(data)
            action = payload.get("action")

            if action == "move":
                player = payload.get("player")
                word = payload.get("word")
                new_state = await MatchService.play_move(match_id, player, word)
                await broadcast_match_state(match_id, new_state)

            elif action == "timeout":
                player = payload.get("player")
                new_state = await MatchService.timeout(match_id, player)
                await broadcast_match_state(match_id, new_state)

            elif action == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))

    except WebSocketDisconnect:
        _connections[match_id].discard(websocket)
    except Exception as exc:
        logger.warning("WebSocket error for match %s: %s", match_id, exc)
        _connections[match_id].discard(websocket)
