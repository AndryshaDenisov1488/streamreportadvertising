from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.platform_extra import BroadcastChecklist
from app.models.user import User


async def get_checklist_row(
    session: AsyncSession, *, stream_event_id: UUID, user_id: UUID, day_index: int
) -> BroadcastChecklist | None:
    result = await session.execute(
        select(BroadcastChecklist).where(
            BroadcastChecklist.stream_event_id == stream_event_id,
            BroadcastChecklist.user_id == user_id,
            BroadcastChecklist.day_index == day_index,
        )
    )
    return result.scalar_one_or_none()


async def get_or_create_checklist(
    session: AsyncSession, *, stream_event_id: UUID, user: User, day_index: int
) -> BroadcastChecklist:
    result = await session.execute(
        select(BroadcastChecklist).where(
            BroadcastChecklist.stream_event_id == stream_event_id,
            BroadcastChecklist.user_id == user.id,
            BroadcastChecklist.day_index == day_index,
        )
    )
    row = result.scalar_one_or_none()
    if row:
        return row
    row = BroadcastChecklist(stream_event_id=stream_event_id, user_id=user.id, day_index=day_index)
    session.add(row)
    await session.flush()
    return row


async def update_checklist(
    session: AsyncSession,
    *,
    stream_event_id: UUID,
    user: User,
    day_index: int,
    picture_exposure_ok: bool | None,
    judges_stream_ok: bool | None,
    splitter_socket_ok: bool | None,
    key_stream_started_ok: bool | None,
    kick_ok: bool | None,
    mentions_four_ok: bool | None,
) -> BroadcastChecklist:
    row = await get_or_create_checklist(session, stream_event_id=stream_event_id, user=user, day_index=day_index)
    if picture_exposure_ok is not None:
        row.picture_exposure_ok = picture_exposure_ok
    if judges_stream_ok is not None:
        row.judges_stream_ok = judges_stream_ok
    if splitter_socket_ok is not None:
        row.splitter_socket_ok = splitter_socket_ok
    if key_stream_started_ok is not None:
        row.key_stream_started_ok = key_stream_started_ok
    if kick_ok is not None:
        row.kick_ok = kick_ok
    if mentions_four_ok is not None:
        row.mentions_four_ok = mentions_four_ok
    await session.commit()
    await session.refresh(row)
    return row