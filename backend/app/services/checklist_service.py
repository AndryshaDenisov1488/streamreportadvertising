from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.platform_extra import BroadcastChecklist
from app.models.user import User


async def get_checklist_row(
    session: AsyncSession, *, stream_event_id: UUID, user_id: UUID
) -> BroadcastChecklist | None:
    result = await session.execute(
        select(BroadcastChecklist).where(
            BroadcastChecklist.stream_event_id == stream_event_id,
            BroadcastChecklist.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def get_or_create_checklist(
    session: AsyncSession, *, stream_event_id: UUID, user: User
) -> BroadcastChecklist:
    result = await session.execute(
        select(BroadcastChecklist).where(
            BroadcastChecklist.stream_event_id == stream_event_id,
            BroadcastChecklist.user_id == user.id,
        )
    )
    row = result.scalar_one_or_none()
    if row:
        return row
    row = BroadcastChecklist(stream_event_id=stream_event_id, user_id=user.id)
    session.add(row)
    await session.flush()
    return row


async def update_checklist(
    session: AsyncSession,
    *,
    stream_event_id: UUID,
    user: User,
    mic_ok: bool | None,
    scene_ok: bool | None,
    sponsor_slots_ok: bool | None,
    keys_tested_ok: bool | None,
) -> BroadcastChecklist:
    row = await get_or_create_checklist(session, stream_event_id=stream_event_id, user=user)
    if mic_ok is not None:
        row.mic_ok = mic_ok
    if scene_ok is not None:
        row.scene_ok = scene_ok
    if sponsor_slots_ok is not None:
        row.sponsor_slots_ok = sponsor_slots_ok
    if keys_tested_ok is not None:
        row.keys_tested_ok = keys_tested_ok
    await session.commit()
    await session.refresh(row)
    return row
