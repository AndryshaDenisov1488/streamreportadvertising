import uuid
from typing import Any

from fastapi import WebSocket
from starlette.websockets import WebSocketState


class StreamEventHub:
    def __init__(self) -> None:
        self._rooms: dict[uuid.UUID, list[WebSocket]] = {}

    async def connect(self, stream_event_id: uuid.UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self._rooms.setdefault(stream_event_id, []).append(websocket)

    def disconnect(self, stream_event_id: uuid.UUID, websocket: WebSocket) -> None:
        room = self._rooms.get(stream_event_id)
        if not room:
            return
        if websocket in room:
            room.remove(websocket)
        if not room:
            del self._rooms[stream_event_id]

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
