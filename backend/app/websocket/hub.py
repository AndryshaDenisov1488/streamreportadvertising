import uuid
from typing import Any

from fastapi import WebSocket
from starlette.websockets import WebSocketState


class StreamEventHub:
    def __init__(self, max_subscribers_per_room: int = 80) -> None:
        self._rooms: dict[uuid.UUID, list[WebSocket]] = {}
        self._max_subscribers_per_room = max_subscribers_per_room

    async def connect(self, stream_event_id: uuid.UUID, websocket: WebSocket) -> bool:
        room = self._rooms.setdefault(stream_event_id, [])
        if len(room) >= self._max_subscribers_per_room:
            await websocket.close(code=4429)
            return False
        room.append(websocket)
        await self._publish_presence(stream_event_id)
        return True

    def disconnect(self, stream_event_id: uuid.UUID, websocket: WebSocket) -> None:
        room = self._rooms.get(stream_event_id)
        if not room:
            return
        if websocket in room:
            room.remove(websocket)
        if not room:
            del self._rooms[stream_event_id]

    async def notify_presence(self, stream_event_id: uuid.UUID) -> None:
        await self._publish_presence(stream_event_id)

    async def _publish_presence(self, stream_event_id: uuid.UUID) -> None:
        room = list(self._rooms.get(stream_event_id, []))
        n = len(room)
        msg: dict[str, Any] = {"type": "presence", "payload": {"viewers": n}}
        for ws in room:
            if ws.client_state != WebSocketState.CONNECTED:
                continue
            try:
                await ws.send_json(msg)
            except Exception:
                self.disconnect(stream_event_id, ws)

    async def publish(self, stream_event_id: uuid.UUID, message: dict[str, Any]) -> None:
        room = list(self._rooms.get(stream_event_id, []))
        for ws in room:
            if ws.client_state != WebSocketState.CONNECTED:
                self.disconnect(stream_event_id, ws)
                continue
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(stream_event_id, ws)
