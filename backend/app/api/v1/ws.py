import asyncio
import json
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from app.core.security import decode_token_safe
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.websocket.hub import StreamEventHub

router = APIRouter()

_WS_AUTH_TIMEOUT_S = 15.0


@router.websocket("/ws/stream-events/{stream_event_id}")
async def stream_events_ws(
    websocket: WebSocket,
    stream_event_id: uuid.UUID,
) -> None:
    await websocket.accept()
    try:
        raw = await asyncio.wait_for(websocket.receive_text(), timeout=_WS_AUTH_TIMEOUT_S)
    except (asyncio.TimeoutError, WebSocketDisconnect):
        await websocket.close(code=4401)
        return
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        await websocket.close(code=4401)
        return
    token = msg.get("access_token") or msg.get("token")
    if not token or not isinstance(token, str):
        await websocket.close(code=4401)
        return
    payload = decode_token_safe(token)
    if not payload or payload.get("type") != "access":
        await websocket.close(code=4401)
        return
    sub = payload.get("sub")
    if not sub:
        await websocket.close(code=4401)
        return
    try:
        uid = uuid.UUID(sub)
    except ValueError:
        await websocket.close(code=4401)
        return
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == uid))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            await websocket.close(code=4401)
            return
    hub: StreamEventHub = websocket.app.state.ws_hub
    ok = await hub.connect(stream_event_id, websocket)
    if not ok:
        return
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        hub.disconnect(stream_event_id, websocket)
        await hub.notify_presence(stream_event_id)
