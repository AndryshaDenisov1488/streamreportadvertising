from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin, OperatorOrAbove
from app.db.session import get_db
from app.schemas.stream import (
    BroadcastSessionOut,
    SponsorMentionOut,
    StreamEventCreate,
    StreamEventDetailOut,
    StreamEventListOut,
    StreamEventUpdate,
    StreamLockBody,
)
from app.services import stream_service
from app.websocket.hub import StreamEventHub

router = APIRouter(prefix="/stream-events", tags=["stream-events"])


@router.get("", response_model=list[StreamEventListOut])
async def list_streams(
    _: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> list[StreamEventListOut]:
    return await stream_service.list_stream_events(session)


@router.get("/{stream_id}", response_model=StreamEventDetailOut)
async def get_stream(
    stream_id: UUID,
    _: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> StreamEventDetailOut:
    return await stream_service.get_stream_event_detail(session, stream_id)


@router.post("", response_model=StreamEventDetailOut)
async def create_stream(
    body: StreamEventCreate,
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> StreamEventDetailOut:
    return await stream_service.create_stream_event(session, actor=actor, data=body)


@router.patch("/{stream_id}", response_model=StreamEventDetailOut)
async def update_stream(
    stream_id: UUID,
    body: StreamEventUpdate,
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> StreamEventDetailOut:
    return await stream_service.update_stream_event(session, actor=actor, stream_id=stream_id, data=body)


@router.delete("/{stream_id}", status_code=204)
async def delete_stream(
    stream_id: UUID,
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> None:
    await stream_service.delete_stream_event(session, actor=actor, stream_id=stream_id)


@router.post("/{stream_id}/lock", response_model=StreamEventDetailOut)
async def lock_stream_route(
    stream_id: UUID,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
    body: StreamLockBody | None = None,
) -> StreamEventDetailOut:
    assign = body.assign_user_id if body else None
    detail = await stream_service.lock_stream(session, actor=actor, stream_id=stream_id, assign_user_id=assign)
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(
        stream_id,
        {
            "type": "lock_changed",
            "payload": {"locked_by_user_id": str(detail.locked_by_user_id) if detail.locked_by_user_id else None},
        },
    )
    return detail


@router.post("/{stream_id}/unlock", response_model=StreamEventDetailOut)
async def unlock_stream_route(
    stream_id: UUID,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> StreamEventDetailOut:
    detail = await stream_service.unlock_stream(session, actor=actor, stream_id=stream_id)
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(stream_id, {"type": "lock_changed", "payload": {"locked_by_user_id": None}})
    return detail


@router.post("/{stream_id}/days/{day_index}/broadcast/start", response_model=BroadcastSessionOut)
async def start_broadcast_route(
    stream_id: UUID,
    day_index: int,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> BroadcastSessionOut:
    out = await stream_service.start_broadcast(session, actor=actor, stream_id=stream_id, day_index=day_index)
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(
        stream_id,
        {
            "type": "broadcast_started",
            "payload": {
                "session_id": str(out.id),
                "day_index": out.day_index,
                "started_at": out.started_at.isoformat(),
            },
        },
    )
    return out


@router.post("/{stream_id}/days/{day_index}/broadcast/stop", status_code=204)
async def stop_broadcast_route(
    stream_id: UUID,
    day_index: int,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> None:
    await stream_service.stop_broadcast(session, actor=actor, stream_id=stream_id, day_index=day_index)
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(stream_id, {"type": "broadcast_stopped", "payload": {"day_index": day_index}})


@router.get("/{stream_id}/days/{day_index}/mentions", response_model=list[SponsorMentionOut])
async def list_mentions_route(
    stream_id: UUID,
    day_index: int,
    _: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> list[SponsorMentionOut]:
    return await stream_service.list_mentions_for_event_day(session, stream_id=stream_id, day_index=day_index)
