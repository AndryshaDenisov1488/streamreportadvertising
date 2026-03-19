import uuid

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token_safe
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.websocket.hub import StreamEventHub

router = APIRouter()


@router.websocket("/ws/stream-events/{stream_event_id}")
async def stream_events_ws(
    websocket: WebSocket,
    stream_event_id: uuid.UUID,
    token: str | None = Query(default=None),
) -> None:
    if not token:
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
    await hub.connect(stream_event_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        hub.disconnect(stream_event_id, websocket)
