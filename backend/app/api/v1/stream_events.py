from uuid import UUID

from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin, OperatorOrAbove
from app.db.session import get_db
from app.schemas.platform import ChecklistOut, ChecklistUpdate
from app.schemas.stream import (
    BroadcastActualStartBody,
    BroadcastSessionOut,
    SponsorMentionOut,
    StreamEventCreate,
    StreamEventDetailOut,
    StreamEventListOut,
    StreamEventUpdate,
    StreamLockBody,
)
from app.services import checklist_service, stream_service
from app.utils.webhook import post_external_webhook
from app.websocket.hub import StreamEventHub

router = APIRouter(prefix="/stream-events", tags=["stream-events"])


@router.get("", response_model=list[StreamEventListOut])
async def list_streams(
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> list[StreamEventListOut]:
    return await stream_service.list_stream_events(session, viewer=actor)


@router.post("/sync/ffkm-admin")
async def sync_ffkm_admin_tournaments(
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Подтянуть турниры из ffkm-admin в мероприятия (upsert по ffkm_admin_tournament_id)."""
    from fastapi import HTTPException, status

    from app.services.ffkm_admin_client import FfkmAdminClientError
    from app.services.ffkm_tournament_sync import sync_tournaments_from_ffkm_admin

    _ = actor
    try:
        stats = await sync_tournaments_from_ffkm_admin(session)
    except FfkmAdminClientError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
    return stats.as_dict()


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
    day_ix = body.day_indices if body else None
    detail = await stream_service.lock_stream(
        session,
        actor=actor,
        stream_id=stream_id,
        assign_user_id=assign,
        day_indices=day_ix,
    )
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
    background_tasks: BackgroundTasks,
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
    background_tasks.add_task(
        post_external_webhook,
        "broadcast_started",
        {
            "stream_event_id": str(stream_id),
            "day_index": day_index,
            "session_id": str(out.id),
            "started_at": out.started_at.isoformat(),
        },
    )
    return out


@router.post(
    "/{stream_id}/days/{day_index}/broadcast/actual-start",
    response_model=BroadcastSessionOut,
)
async def realign_broadcast_actual_start_route(
    stream_id: UUID,
    day_index: int,
    body: BroadcastActualStartBody,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> BroadcastSessionOut:
    out = await stream_service.realign_broadcast_actual_start(
        session,
        actor=actor,
        stream_id=stream_id,
        day_index=day_index,
        actual_started_at=body.actual_started_at,
    )
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(
        stream_id,
        {
            "type": "broadcast_realigned",
            "payload": {"day_index": day_index, "started_at": out.started_at.isoformat()},
        },
    )
    return out


@router.post("/{stream_id}/days/{day_index}/broadcast/stop", status_code=204)
async def stop_broadcast_route(
    stream_id: UUID,
    day_index: int,
    request: Request,
    background_tasks: BackgroundTasks,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> None:
    await stream_service.stop_broadcast(session, actor=actor, stream_id=stream_id, day_index=day_index)
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(stream_id, {"type": "broadcast_stopped", "payload": {"day_index": day_index}})
    background_tasks.add_task(
        post_external_webhook,
        "broadcast_stopped",
        {"stream_event_id": str(stream_id), "day_index": day_index},
    )


@router.get("/{stream_id}/days/{day_index}/checklist", response_model=ChecklistOut)
async def get_checklist_route(
    stream_id: UUID,
    day_index: int,
    user: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> ChecklistOut:
    await stream_service.assert_valid_stream_day(session, stream_id, day_index)
    row = await checklist_service.get_checklist_row(
        session, stream_event_id=stream_id, user_id=user.id, day_index=day_index
    )
    if not row:
        return ChecklistOut(
            stream_event_id=stream_id,
            day_index=day_index,
            picture_exposure_ok=False,
            judges_stream_ok=False,
            splitter_socket_ok=False,
            key_stream_started_ok=False,
            kick_ok=False,
            mentions_four_ok=False,
            updated_at=datetime.now(timezone.utc),
        )
    return ChecklistOut(
        stream_event_id=row.stream_event_id,
        day_index=row.day_index,
        picture_exposure_ok=row.picture_exposure_ok,
        judges_stream_ok=row.judges_stream_ok,
        splitter_socket_ok=row.splitter_socket_ok,
        key_stream_started_ok=row.key_stream_started_ok,
        kick_ok=row.kick_ok,
        mentions_four_ok=row.mentions_four_ok,
        updated_at=row.updated_at,
    )


@router.put("/{stream_id}/days/{day_index}/checklist", response_model=ChecklistOut)
async def put_checklist_route(
    stream_id: UUID,
    day_index: int,
    body: ChecklistUpdate,
    user: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> ChecklistOut:
    await stream_service.assert_valid_stream_day(session, stream_id, day_index)
    row = await checklist_service.update_checklist(
        session,
        stream_event_id=stream_id,
        user=user,
        day_index=day_index,
        picture_exposure_ok=body.picture_exposure_ok,
        judges_stream_ok=body.judges_stream_ok,
        splitter_socket_ok=body.splitter_socket_ok,
        key_stream_started_ok=body.key_stream_started_ok,
        kick_ok=body.kick_ok,
        mentions_four_ok=body.mentions_four_ok,
    )
    return ChecklistOut(
        stream_event_id=row.stream_event_id,
        day_index=row.day_index,
        picture_exposure_ok=row.picture_exposure_ok,
        judges_stream_ok=row.judges_stream_ok,
        splitter_socket_ok=row.splitter_socket_ok,
        key_stream_started_ok=row.key_stream_started_ok,
        kick_ok=row.kick_ok,
        mentions_four_ok=row.mentions_four_ok,
        updated_at=row.updated_at,
    )


@router.get("/{stream_id}/days/{day_index}/mentions", response_model=list[SponsorMentionOut])
async def list_mentions_route(
    stream_id: UUID,
    day_index: int,
    _: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> list[SponsorMentionOut]:
    return await stream_service.list_mentions_for_event_day(session, stream_id=stream_id, day_index=day_index)
