from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.timezone import add_seconds_to_start, format_moscow_iso, utc_now
from app.models.enums import AuditActionType, UserRole
from app.models.stream import BroadcastSession, MentionAdjustment, SponsorMention, StreamDay, StreamEvent
from app.models.user import User
from app.schemas.stream import (
    BroadcastSessionOut,
    MentionAdjustmentOut,
    SponsorMentionOut,
    StreamDayIn,
    StreamDayOut,
    StreamEventCreate,
    StreamEventDetailOut,
    StreamEventListOut,
    StreamEventUpdate,
)
from app.services.audit_service import write_audit
from app.utils.timecode import seconds_to_hhmmss


def _mention_to_out(mention: SponsorMention) -> SponsorMentionOut:
    bs = mention.broadcast_session
    started = bs.started_at
    if started.tzinfo is None:
        started = started.replace(tzinfo=timezone.utc)
    abs_orig = add_seconds_to_start(started, mention.original_offset_sec)
    abs_adj = add_seconds_to_start(started, mention.adjusted_offset_sec)
    adjustments = [
        MentionAdjustmentOut.model_validate(a) for a in sorted(mention.adjustments, key=lambda x: x.created_at)
    ]
    return SponsorMentionOut(
        id=mention.id,
        broadcast_session_id=mention.broadcast_session_id,
        original_offset_sec=mention.original_offset_sec,
        adjusted_offset_sec=mention.adjusted_offset_sec,
        original_timecode=seconds_to_hhmmss(mention.original_offset_sec),
        adjusted_timecode=seconds_to_hhmmss(mention.adjusted_offset_sec),
        absolute_moscow_original=format_moscow_iso(abs_orig),
        absolute_moscow_adjusted=format_moscow_iso(abs_adj),
        is_adjusted=mention.original_offset_sec != mention.adjusted_offset_sec,
        created_at=mention.created_at,
        adjustments=adjustments,
    )


async def _get_event(session: AsyncSession, stream_id: UUID) -> StreamEvent:
    result = await session.execute(
        select(StreamEvent)
        .options(selectinload(StreamEvent.days), selectinload(StreamEvent.broadcast_sessions))
        .where(StreamEvent.id == stream_id)
    )
    ev = result.scalar_one_or_none()
    if not ev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Событие не найдено")
    return ev


async def _active_broadcast_ids(session: AsyncSession) -> set[UUID]:
    q = select(BroadcastSession.stream_event_id).where(BroadcastSession.ended_at.is_(None))
    result = await session.execute(q)
    return set(result.scalars().all())


async def list_stream_events(session: AsyncSession) -> list[StreamEventListOut]:
    active_ids = await _active_broadcast_ids(session)
    result = await session.execute(select(StreamEvent).order_by(StreamEvent.start_date.desc(), StreamEvent.created_at.desc()))
    items: list[StreamEventListOut] = []
    for ev in result.scalars().all():
        items.append(
            StreamEventListOut(
                id=ev.id,
                title=ev.title,
                start_date=ev.start_date,
                duration_days=ev.duration_days,
                locked_by_user_id=ev.locked_by_user_id,
                has_active_broadcast=ev.id in active_ids,
                created_at=ev.created_at,
            )
        )
    return items


async def get_stream_event_detail(session: AsyncSession, stream_id: UUID) -> StreamEventDetailOut:
    ev = await _get_event(session, stream_id)
    ev.days.sort(key=lambda d: d.day_index)
    active_broadcasts = [
        BroadcastSessionOut(
            id=b.id,
            stream_event_id=b.stream_event_id,
            day_index=b.day_index,
            operator_id=b.operator_id,
            started_at=b.started_at,
            ended_at=b.ended_at,
            is_active=b.ended_at is None,
        )
        for b in ev.broadcast_sessions
        if b.ended_at is None
    ]
    return StreamEventDetailOut(
        id=ev.id,
        title=ev.title,
        start_date=ev.start_date,
        duration_days=ev.duration_days,
        locked_by_user_id=ev.locked_by_user_id,
        days=[StreamDayOut.model_validate(d) for d in ev.days],
        active_broadcasts=active_broadcasts,
        created_at=ev.created_at,
        updated_at=ev.updated_at,
    )


async def _sync_days(
    session: AsyncSession,
    stream_event_id: UUID,
    duration_days: int,
    days_input: list[StreamDayIn] | None,
) -> None:
    result = await session.execute(select(StreamDay).where(StreamDay.stream_event_id == stream_event_id))
    existing = {d.day_index: d for d in result.scalars().all()}
    for idx in range(1, duration_days + 1):
        if idx not in existing:
            session.add(
                StreamDay(
                    stream_event_id=stream_event_id,
                    day_index=idx,
                    stream_url="",
                    server_url="",
                    stream_key="",
                )
            )
    to_remove = [d for d in existing.values() if d.day_index > duration_days]
    for d in to_remove:
        sess_count = await session.execute(
            select(func.count())
            .select_from(BroadcastSession)
            .where(
                and_(
                    BroadcastSession.stream_event_id == stream_event_id,
                    BroadcastSession.day_index == d.day_index,
                )
            )
        )
        if sess_count.scalar_one() > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Нельзя уменьшить длительность: есть эфир для дня {d.day_index}",
            )
        await session.delete(d)
    if days_input:
        by_idx = {x.day_index: x for x in days_input}
        result2 = await session.execute(select(StreamDay).where(StreamDay.stream_event_id == stream_event_id))
        for row in result2.scalars().all():
            inc = by_idx.get(row.day_index)
            if inc:
                row.stream_url = inc.stream_url
                row.server_url = inc.server_url
                row.stream_key = inc.stream_key


async def create_stream_event(session: AsyncSession, *, actor: User, data: StreamEventCreate) -> StreamEventDetailOut:
    ev = StreamEvent(
        title=data.title,
        start_date=data.start_date,
        duration_days=data.duration_days,
        created_by_id=actor.id,
    )
    session.add(ev)
    await session.flush()
    await _sync_days(session, ev.id, data.duration_days, data.days)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_CREATE,
        entity_type="stream_event",
        entity_id=str(ev.id),
        payload_before=None,
        payload_after={"title": ev.title, "start_date": str(ev.start_date), "duration_days": ev.duration_days},
    )
    await session.commit()
    return await get_stream_event_detail(session, ev.id)


async def update_stream_event(session: AsyncSession, *, actor: User, stream_id: UUID, data: StreamEventUpdate) -> StreamEventDetailOut:
    ev = await _get_event(session, stream_id)
    before = {"title": ev.title, "start_date": str(ev.start_date), "duration_days": ev.duration_days}
    if data.title is not None:
        ev.title = data.title
    if data.start_date is not None:
        ev.start_date = data.start_date
    new_duration = data.duration_days if data.duration_days is not None else ev.duration_days
    if data.duration_days is not None:
        ev.duration_days = data.duration_days
    await _sync_days(session, ev.id, new_duration, data.days)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_UPDATE,
        entity_type="stream_event",
        entity_id=str(ev.id),
        payload_before=before,
        payload_after={"title": ev.title, "start_date": str(ev.start_date), "duration_days": ev.duration_days},
    )
    await session.commit()
    return await get_stream_event_detail(session, stream_id)


async def delete_stream_event(session: AsyncSession, *, actor: User, stream_id: UUID) -> None:
    ev = await _get_event(session, stream_id)
    before = {"title": ev.title}
    await session.delete(ev)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_DELETE,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before=before,
        payload_after=None,
    )
    await session.commit()


async def lock_stream(
    session: AsyncSession,
    *,
    actor: User,
    stream_id: UUID,
    assign_user_id: UUID | None,
) -> StreamEventDetailOut:
    ev = await _get_event(session, stream_id)
    if actor.role == UserRole.STREAM_MANAGER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    before_lock = ev.locked_by_user_id
    if actor.role == UserRole.OPERATOR:
        if ev.locked_by_user_id is not None and ev.locked_by_user_id != actor.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Событие занято другим оператором")
        ev.locked_by_user_id = actor.id
    elif actor.role == UserRole.SUPERADMIN:
        if assign_user_id is not None:
            ures = await session.execute(select(User).where(User.id == assign_user_id))
            target = ures.scalar_one_or_none()
            if not target or target.role != UserRole.OPERATOR:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нужен оператор")
            ev.locked_by_user_id = assign_user_id
        else:
            ev.locked_by_user_id = actor.id
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_LOCK,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before={"locked_by": str(before_lock) if before_lock else None},
        payload_after={"locked_by": str(ev.locked_by_user_id) if ev.locked_by_user_id else None},
    )
    await session.commit()
    return await get_stream_event_detail(session, stream_id)


async def unlock_stream(session: AsyncSession, *, actor: User, stream_id: UUID) -> StreamEventDetailOut:
    ev = await _get_event(session, stream_id)
    if actor.role == UserRole.STREAM_MANAGER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    if actor.role == UserRole.OPERATOR:
        if ev.locked_by_user_id != actor.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Не вы взяли событие в работу")
    prev = ev.locked_by_user_id
    ev.locked_by_user_id = None
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_UNLOCK,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before={"locked_by": str(prev) if prev else None},
        payload_after={"locked_by": None},
    )
    await session.commit()
    return await get_stream_event_detail(session, stream_id)


def _can_control_broadcast(actor: User, ev: StreamEvent, session_operator_id: UUID) -> bool:
    if actor.role == UserRole.SUPERADMIN:
        return True
    if actor.role != UserRole.OPERATOR:
        return False
    if ev.locked_by_user_id != actor.id:
        return False
    return session_operator_id == actor.id


async def start_broadcast(session: AsyncSession, *, actor: User, stream_id: UUID, day_index: int) -> BroadcastSessionOut:
    if day_index < 1 or day_index > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный день")
    ev = await _get_event(session, stream_id)
    if day_index > ev.duration_days:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="День вне длительности события")
    if actor.role == UserRole.OPERATOR:
        if ev.locked_by_user_id != actor.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Сначала возьмите событие в работу")
    elif actor.role != UserRole.SUPERADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    active = await session.execute(
        select(BroadcastSession).where(
            and_(
                BroadcastSession.stream_event_id == stream_id,
                BroadcastSession.day_index == day_index,
                BroadcastSession.ended_at.is_(None),
            )
        )
    )
    if active.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Эфир для этого дня уже идёт")
    started = utc_now()
    operator_id = actor.id if actor.role == UserRole.OPERATOR else (ev.locked_by_user_id or actor.id)
    if actor.role == UserRole.SUPERADMIN and ev.locked_by_user_id:
        operator_id = ev.locked_by_user_id
    bs = BroadcastSession(
        stream_event_id=stream_id,
        day_index=day_index,
        operator_id=operator_id,
        started_at=started,
    )
    session.add(bs)
    await session.flush()
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.BROADCAST_START,
        entity_type="broadcast_session",
        entity_id=str(bs.id),
        payload_after={"stream_event_id": str(stream_id), "day_index": day_index, "started_at": started.isoformat()},
        payload_before=None,
    )
    await session.commit()
    await session.refresh(bs)
    return BroadcastSessionOut(
        id=bs.id,
        stream_event_id=bs.stream_event_id,
        day_index=bs.day_index,
        operator_id=bs.operator_id,
        started_at=bs.started_at,
        ended_at=bs.ended_at,
        is_active=True,
    )


async def stop_broadcast(session: AsyncSession, *, actor: User, stream_id: UUID, day_index: int) -> None:
    ev = await _get_event(session, stream_id)
    result = await session.execute(
        select(BroadcastSession).where(
            and_(
                BroadcastSession.stream_event_id == stream_id,
                BroadcastSession.day_index == day_index,
                BroadcastSession.ended_at.is_(None),
            )
        )
    )
    bs = result.scalar_one_or_none()
    if not bs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Активный эфир не найден")
    if not _can_control_broadcast(actor, ev, bs.operator_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    bs.ended_at = utc_now()
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.BROADCAST_STOP,
        entity_type="broadcast_session",
        entity_id=str(bs.id),
        payload_before={"ended_at": None},
        payload_after={"ended_at": bs.ended_at.isoformat()},
    )
    await session.commit()


async def add_sponsor_mention(session: AsyncSession, *, actor: User, broadcast_session_id: UUID) -> SponsorMentionOut:
    result = await session.execute(
        select(BroadcastSession)
        .options(selectinload(BroadcastSession.stream_event), selectinload(BroadcastSession.mentions))
        .where(BroadcastSession.id == broadcast_session_id)
    )
    bs = result.scalar_one_or_none()
    if not bs or bs.ended_at is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Сессия эфира неактивна")
    ev = bs.stream_event
    if not _can_control_broadcast(actor, ev, bs.operator_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    start = bs.started_at if bs.started_at.tzinfo else bs.started_at.replace(tzinfo=timezone.utc)
    now = utc_now()
    offset = int((now - start).total_seconds())
    if offset < 0:
        offset = 0
    mention = SponsorMention(
        broadcast_session_id=bs.id,
        original_offset_sec=offset,
        adjusted_offset_sec=offset,
    )
    session.add(mention)
    await session.flush()
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.MENTION_CREATE,
        entity_type="sponsor_mention",
        entity_id=str(mention.id),
        payload_before=None,
        payload_after={"offset_sec": offset, "broadcast_session_id": str(bs.id)},
    )
    await session.commit()
    await session.refresh(mention)
    mres = await session.execute(
        select(SponsorMention)
        .options(
            selectinload(SponsorMention.adjustments),
            selectinload(SponsorMention.broadcast_session),
        )
        .where(SponsorMention.id == mention.id)
    )
    mention = mres.scalar_one()
    return _mention_to_out(mention)


async def update_sponsor_mention(
    session: AsyncSession,
    *,
    actor: User,
    mention_id: UUID,
    new_adjusted_sec: int,
) -> SponsorMentionOut:
    result = await session.execute(
        select(SponsorMention)
        .options(
            selectinload(SponsorMention.adjustments),
            selectinload(SponsorMention.broadcast_session).selectinload(BroadcastSession.stream_event),
        )
        .where(SponsorMention.id == mention_id)
    )
    mention = result.scalar_one_or_none()
    if not mention:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Упоминание не найдено")
    bs = mention.broadcast_session
    ev = bs.stream_event
    if bs.ended_at is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Эфир завершён")
    if not _can_control_broadcast(actor, ev, bs.operator_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    prev = mention.adjusted_offset_sec
    if prev == new_adjusted_sec:
        return _mention_to_out(mention)
    adj = MentionAdjustment(
        mention_id=mention.id,
        editor_user_id=actor.id,
        previous_adjusted_sec=prev,
        new_adjusted_sec=new_adjusted_sec,
    )
    session.add(adj)
    mention.adjusted_offset_sec = new_adjusted_sec
    await session.flush()
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.MENTION_UPDATE,
        entity_type="sponsor_mention",
        entity_id=str(mention.id),
        payload_before={"adjusted_offset_sec": prev},
        payload_after={"adjusted_offset_sec": new_adjusted_sec},
    )
    await session.commit()
    await session.refresh(mention)
    mres = await session.execute(
        select(SponsorMention)
        .options(
            selectinload(SponsorMention.adjustments),
            selectinload(SponsorMention.broadcast_session),
        )
        .where(SponsorMention.id == mention_id)
    )
    mention = mres.scalar_one()
    return _mention_to_out(mention)


async def list_mentions_for_event_day(
    session: AsyncSession,
    *,
    stream_id: UUID,
    day_index: int,
) -> list[SponsorMentionOut]:
    ev = await _get_event(session, stream_id)
    if day_index > ev.duration_days:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный день")
    result = await session.execute(
        select(SponsorMention)
        .join(BroadcastSession)
        .options(
            selectinload(SponsorMention.adjustments),
            selectinload(SponsorMention.broadcast_session),
        )
        .where(
            and_(
                BroadcastSession.stream_event_id == stream_id,
                BroadcastSession.day_index == day_index,
            )
        )
        .order_by(SponsorMention.created_at.asc())
    )
    return [_mention_to_out(m) for m in result.scalars().all()]
