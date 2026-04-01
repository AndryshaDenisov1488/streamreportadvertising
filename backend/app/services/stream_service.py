from collections import defaultdict
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import and_, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.timezone import MOSCOW_TZ, add_seconds_to_start, format_moscow_datetime, utc_now
from app.models.enums import AuditActionType, UserRole
from app.models.logo import StreamEventLogo
from app.models.stream import (
    BroadcastSession,
    MentionAdjustment,
    SponsorMention,
    StreamDay,
    StreamDayAssignment,
    StreamEvent,
    StreamEventTemplate,
)
from app.models.user import User
from app.schemas.logo import StreamLogoItemOut
from app.schemas.stream import (
    BroadcastSessionOut,
    DayAssignmentOut,
    MentionAdjustmentOut,
    SponsorMentionOut,
    StreamDayIn,
    StreamDayOut,
    StreamEventCreate,
    StreamDayLinkOut,
    StreamEventDetailOut,
    StreamEventListOut,
    StreamEventUpdate,
)
from app.services.audit_service import write_audit
from app.services.notification_service import create_for_users_with_roles
from app.utils.display_name import user_display_name
from app.utils.timecode import seconds_to_hhmmss

# Повторный старт эфира запрещён, если был завершённый эфир дольше этого порога и с упоминаниями (таймкодами)
BROADCAST_RESTART_BLOCK_MIN_DURATION = timedelta(hours=1)


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
        absolute_moscow_original=format_moscow_datetime(abs_orig),
        absolute_moscow_adjusted=format_moscow_datetime(abs_adj),
        is_adjusted=mention.original_offset_sec != mention.adjusted_offset_sec,
        created_at=mention.created_at,
        adjustments=adjustments,
    )


async def _get_event(session: AsyncSession, stream_id: UUID) -> StreamEvent:
    result = await session.execute(
        select(StreamEvent)
        .options(
            selectinload(StreamEvent.days),
            selectinload(StreamEvent.broadcast_sessions),
            selectinload(StreamEvent.event_logos).selectinload(StreamEventLogo.logo),
        )
        .where(StreamEvent.id == stream_id)
    )
    ev = result.scalar_one_or_none()
    if not ev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Мероприятие не найдено")
    return ev


def _logos_for_stream(ev: StreamEvent) -> list[StreamLogoItemOut]:
    if not ev.event_logos:
        return []
    items: list[StreamLogoItemOut] = []
    for link in sorted(ev.event_logos, key=lambda x: x.sort_order):
        lg = link.logo
        if not lg:
            continue
        pub = f"/uploads/{lg.stored_path.lstrip('/')}"
        items.append(
            StreamLogoItemOut(
                id=lg.id,
                filename_original=lg.filename_original,
                public_url=pub,
                sort_order=link.sort_order,
                created_at=lg.created_at,
            )
        )
    return items


async def assert_valid_stream_day(session: AsyncSession, stream_id: UUID, day_index: int) -> None:
    if day_index < 1 or day_index > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный день")
    ev = await _get_event(session, stream_id)
    if day_index > ev.duration_days:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="День вне длительности мероприятия")


async def _broadcast_restart_blocked_days(
    session: AsyncSession, *, stream_id: UUID, duration_days: int
) -> list[int]:
    """Дни, для которых нельзя снова начать эфир (уже был длинный эфир с таймкодами)."""
    result = await session.execute(
        select(BroadcastSession.id, BroadcastSession.day_index, BroadcastSession.started_at, BroadcastSession.ended_at).where(
            BroadcastSession.stream_event_id == stream_id,
            BroadcastSession.ended_at.isnot(None),
        )
    )
    long_with_mentions: list[tuple[UUID, int]] = []
    for sid, d_idx, started, ended in result.all():
        if d_idx < 1 or d_idx > duration_days or not started or not ended:
            continue
        if ended - started <= BROADCAST_RESTART_BLOCK_MIN_DURATION:
            continue
        long_with_mentions.append((sid, d_idx))
    if not long_with_mentions:
        return []
    session_ids = [x[0] for x in long_with_mentions]
    cnt_r = await session.execute(
        select(SponsorMention.broadcast_session_id, func.count())
        .where(SponsorMention.broadcast_session_id.in_(session_ids))
        .group_by(SponsorMention.broadcast_session_id)
    )
    with_counts = {row[0]: int(row[1]) for row in cnt_r.all()}
    blocked: set[int] = set()
    for sid, d_idx in long_with_mentions:
        if with_counts.get(sid, 0) > 0:
            blocked.add(d_idx)
    return sorted(blocked)


async def _day_blocked_for_new_broadcast(
    session: AsyncSession, *, stream_id: UUID, day_index: int, duration_days: int
) -> bool:
    blocked = await _broadcast_restart_blocked_days(session, stream_id=stream_id, duration_days=duration_days)
    return day_index in blocked


async def _assignment_operator_for_day(
    session: AsyncSession, stream_id: UUID, day_index: int
) -> UUID | None:
    r = await session.execute(
        select(StreamDayAssignment.operator_id).where(
            StreamDayAssignment.stream_event_id == stream_id,
            StreamDayAssignment.day_index == day_index,
        )
    )
    return r.scalar_one_or_none()


def _format_days_label(days: list[int]) -> str:
    days = sorted(days)
    if len(days) == 1:
        return str(days[0])
    if days == list(range(days[0], days[-1] + 1)):
        return f"{days[0]}–{days[-1]}"
    return ", ".join(str(d) for d in days)


def _assignment_summary_from_pairs(pairs: list[tuple[int, User]]) -> str | None:
    if not pairs:
        return None
    by_op: dict[UUID, list[int]] = defaultdict(list)
    users: dict[UUID, User] = {}
    for day_idx, u in pairs:
        by_op[u.id].append(day_idx)
        users[u.id] = u
    parts: list[str] = []
    for uid in sorted(users.keys(), key=lambda x: str(x)):
        u = users[uid]
        parts.append(f"{user_display_name(u)}: дни {_format_days_label(by_op[uid])}")
    return "; ".join(parts)


async def _load_assignment_pairs(
    session: AsyncSession, stream_ids: list[UUID]
) -> dict[UUID, list[tuple[int, User]]]:
    if not stream_ids:
        return {}
    q = (
        select(StreamDayAssignment, User)
        .join(User, StreamDayAssignment.operator_id == User.id)
        .where(StreamDayAssignment.stream_event_id.in_(stream_ids))
        .order_by(StreamDayAssignment.stream_event_id, StreamDayAssignment.day_index)
    )
    rows = (await session.execute(q)).all()
    out: dict[UUID, list[tuple[int, User]]] = defaultdict(list)
    for a, u in rows:
        out[a.stream_event_id].append((a.day_index, u))
    return out


async def _day_assignments_out(session: AsyncSession, stream_id: UUID) -> list[DayAssignmentOut]:
    pairs = (await _load_assignment_pairs(session, [stream_id])).get(stream_id, [])
    return [
        DayAssignmentOut(
            day_index=d,
            operator_id=u.id,
            operator_display_name=user_display_name(u),
            operator_email=u.email,
        )
        for d, u in pairs
    ]


async def _stream_has_assignments_to_other_than(
    session: AsyncSession, *, stream_event_id: UUID, user_id: UUID
) -> bool:
    r = await session.execute(
        select(func.count())
        .select_from(StreamDayAssignment)
        .where(
            StreamDayAssignment.stream_event_id == stream_event_id,
            StreamDayAssignment.operator_id != user_id,
        )
    )
    return int(r.scalar_one() or 0) > 0


async def _sync_legacy_locked_by(session: AsyncSession, ev: StreamEvent) -> None:
    r = await session.execute(
        select(StreamDayAssignment.operator_id)
        .where(StreamDayAssignment.stream_event_id == ev.id)
        .distinct()
    )
    ids = list(r.scalars().all())
    if len(ids) == 1:
        ev.locked_by_user_id = ids[0]
    else:
        ev.locked_by_user_id = None


async def _active_broadcast_ids(session: AsyncSession) -> set[UUID]:
    q = select(BroadcastSession.stream_event_id).where(BroadcastSession.ended_at.is_(None))
    result = await session.execute(q)
    return set(result.scalars().all())


async def _users_by_ids(session: AsyncSession, user_ids: set[UUID]) -> dict[UUID, User]:
    if not user_ids:
        return {}
    result = await session.execute(select(User).where(User.id.in_(list(user_ids))))
    return {u.id: u for u in result.scalars().all()}


async def _locked_by_display_name(session: AsyncSession, locked_by_user_id: UUID | None) -> str | None:
    if locked_by_user_id is None:
        return None
    result = await session.execute(select(User).where(User.id == locked_by_user_id))
    u = result.scalar_one_or_none()
    return user_display_name(u) if u else None


async def list_stream_events(
    session: AsyncSession,
    *,
    viewer: User | None = None,
) -> list[StreamEventListOut]:
    active_ids = await _active_broadcast_ids(session)
    result = await session.execute(select(StreamEvent).order_by(StreamEvent.start_date.desc(), StreamEvent.created_at.desc()))
    events = list(result.scalars().all())
    eids = [e.id for e in events]
    days_by_event: dict[UUID, list[StreamDay]] = defaultdict(list)
    if eids:
        dr = await session.execute(
            select(StreamDay)
            .where(StreamDay.stream_event_id.in_(eids))
            .order_by(StreamDay.stream_event_id, StreamDay.day_index)
        )
        for row in dr.scalars().all():
            days_by_event[row.stream_event_id].append(row)
    pairs_by = await _load_assignment_pairs(session, eids)
    lock_ids = {e.locked_by_user_id for e in events if e.locked_by_user_id}
    users_map = await _users_by_ids(session, lock_ids)
    items: list[StreamEventListOut] = []
    for ev in events:
        lock_u = users_map.get(ev.locked_by_user_id) if ev.locked_by_user_id else None
        locked_by_display_name = user_display_name(lock_u) if lock_u else None
        summary = _assignment_summary_from_pairs(pairs_by.get(ev.id, []))
        pairs = pairs_by.get(ev.id, [])
        assigned_days = {d for d, _ in pairs}
        has_slot = True
        if viewer is not None:
            if viewer.role == UserRole.SUPERADMIN:
                has_slot = True
            elif not assigned_days:
                has_slot = True
            elif any(u.id == viewer.id for _, u in pairs):
                has_slot = True
            elif len(assigned_days) < ev.duration_days:
                has_slot = True
            else:
                has_slot = False
        day_links = [
            StreamDayLinkOut(day_index=d.day_index, stream_url=d.stream_url or "")
            for d in days_by_event.get(ev.id, [])
        ]
        items.append(
            StreamEventListOut(
                id=ev.id,
                title=ev.title,
                start_date=ev.start_date,
                duration_days=ev.duration_days,
                locked_by_user_id=ev.locked_by_user_id,
                locked_by_display_name=locked_by_display_name,
                assignment_summary=summary,
                has_slot_for_me=has_slot,
                has_active_broadcast=ev.id in active_ids,
                created_at=ev.created_at,
                day_stream_links=day_links,
            )
        )
    return items


async def get_stream_event_detail(session: AsyncSession, stream_id: UUID) -> StreamEventDetailOut:
    ev = await _get_event(session, stream_id)
    ev.days.sort(key=lambda d: d.day_index)
    locked_by_display_name = await _locked_by_display_name(session, ev.locked_by_user_id)
    day_assignments = await _day_assignments_out(session, stream_id)
    active_broadcasts = [
        BroadcastSessionOut(
            id=b.id,
            stream_event_id=b.stream_event_id,
            day_index=b.day_index,
            operator_id=b.operator_id,
            started_at=b.started_at,
            ended_at=b.ended_at,
            is_active=True,
        )
        for b in ev.broadcast_sessions
        if b.ended_at is None
    ]
    ended_raw = [b for b in ev.broadcast_sessions if b.ended_at is not None]
    ended_ids = [b.id for b in ended_raw]
    mention_counts: dict[UUID, int] = {}
    if ended_ids:
        cr = await session.execute(
            select(SponsorMention.broadcast_session_id, func.count())
            .where(SponsorMention.broadcast_session_id.in_(ended_ids))
            .group_by(SponsorMention.broadcast_session_id)
        )
        mention_counts = {row[0]: int(row[1]) for row in cr.all()}
    ended_sorted = sorted(
        ended_raw,
        key=lambda b: (
            b.day_index,
            -(b.ended_at.timestamp() if b.ended_at else 0.0),
        ),
    )
    ended_broadcasts = [
        BroadcastSessionOut(
            id=b.id,
            stream_event_id=b.stream_event_id,
            day_index=b.day_index,
            operator_id=b.operator_id,
            started_at=b.started_at,
            ended_at=b.ended_at,
            is_active=False,
            mentions_count=mention_counts.get(b.id, 0),
        )
        for b in ended_sorted
    ]
    restart_blocked = await _broadcast_restart_blocked_days(
        session, stream_id=stream_id, duration_days=ev.duration_days
    )
    return StreamEventDetailOut(
        id=ev.id,
        title=ev.title,
        start_date=ev.start_date,
        duration_days=ev.duration_days,
        locked_by_user_id=ev.locked_by_user_id,
        locked_by_display_name=locked_by_display_name,
        day_assignments=day_assignments,
        days=[StreamDayOut.model_validate(d) for d in ev.days],
        active_broadcasts=active_broadcasts,
        ended_broadcasts=ended_broadcasts,
        broadcast_restart_blocked_days=restart_blocked,
        content_url=ev.content_url,
        logos=_logos_for_stream(ev),
        created_at=ev.created_at,
        updated_at=ev.updated_at,
    )


def _server_url_from_template_days(days_json: list | None) -> str:
    if not days_json:
        return ""
    for item in days_json:
        if not isinstance(item, dict):
            continue
        u = (item.get("server_url") or "").strip()
        if u:
            return u
    return ""


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
    days_for_sync = data.days
    if data.template_id is not None:
        res_tpl = await session.execute(select(StreamEventTemplate).where(StreamEventTemplate.id == data.template_id))
        tpl = res_tpl.scalar_one_or_none()
        if tpl is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Шаблон не найден")
        server_url = _server_url_from_template_days(tpl.days_json)
        days_for_sync = [
            StreamDayIn(day_index=i, stream_url="", server_url=server_url, stream_key="")
            for i in range(1, data.duration_days + 1)
        ]
    ev = StreamEvent(
        title=data.title,
        start_date=data.start_date,
        duration_days=data.duration_days,
        created_by_id=actor.id,
    )
    session.add(ev)
    await session.flush()
    await _sync_days(session, ev.id, data.duration_days, days_for_sync)
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
    before = {
        "title": ev.title,
        "start_date": str(ev.start_date),
        "duration_days": ev.duration_days,
        "content_url": ev.content_url,
    }
    if data.title is not None:
        ev.title = data.title
    if data.start_date is not None:
        ev.start_date = data.start_date
    new_duration = data.duration_days if data.duration_days is not None else ev.duration_days
    if data.duration_days is not None:
        ev.duration_days = data.duration_days
    if "content_url" in data.model_fields_set:
        ev.content_url = str(data.content_url) if data.content_url is not None else None
    await _sync_days(session, ev.id, new_duration, data.days)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_UPDATE,
        entity_type="stream_event",
        entity_id=str(ev.id),
        payload_before=before,
        payload_after={
            "title": ev.title,
            "start_date": str(ev.start_date),
            "duration_days": ev.duration_days,
            "content_url": ev.content_url,
        },
    )
    await session.commit()
    return await get_stream_event_detail(session, stream_id)


async def delete_stream_event(session: AsyncSession, *, actor: User, stream_id: UUID) -> None:
    ev = await _get_event(session, stream_id)
    active_ids = await _active_broadcast_ids(session)
    if stream_id in active_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить мероприятие с активным эфиром. Сначала остановите эфир.",
        )
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
    day_indices: list[int] | None,
) -> StreamEventDetailOut:
    ev = await _get_event(session, stream_id)
    if actor.role == UserRole.STREAM_MANAGER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

    target_operator_id: UUID
    if actor.role == UserRole.SUPERADMIN:
        if assign_user_id is not None:
            ures = await session.execute(select(User).where(User.id == assign_user_id))
            target = ures.scalar_one_or_none()
            if not target or target.role != UserRole.OPERATOR:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нужен оператор")
            target_operator_id = assign_user_id
        else:
            target_operator_id = actor.id
    else:
        target_operator_id = actor.id

    if actor.role == UserRole.SUPERADMIN and assign_user_id is None:
        if target_operator_id == actor.id and await _stream_has_assignments_to_other_than(
            session, stream_event_id=ev.id, user_id=actor.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Дни назначены операторам — «взять в работу» с пульта суперадмином недоступен",
            )

    want_days: list[int]
    if day_indices is None or len(day_indices) == 0:
        want_days = list(range(1, ev.duration_days + 1))
    else:
        want_days = sorted(set(day_indices))
        for d in want_days:
            if d < 1 or d > ev.duration_days:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"День {d} вне длительности мероприятия")

    before_lock = ev.locked_by_user_id
    for d in want_days:
        cur = await session.execute(
            select(StreamDayAssignment).where(
                StreamDayAssignment.stream_event_id == ev.id,
                StreamDayAssignment.day_index == d,
            )
        )
        row = cur.scalar_one_or_none()
        if row is not None and row.operator_id != target_operator_id:
            ures = await session.execute(select(User).where(User.id == row.operator_id))
            other = ures.scalar_one_or_none()
            who = user_display_name(other) if other else "оператор"
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"День {d} уже назначен: {who}",
            )

    for d in want_days:
        cur = await session.execute(
            select(StreamDayAssignment).where(
                StreamDayAssignment.stream_event_id == ev.id,
                StreamDayAssignment.day_index == d,
            )
        )
        row = cur.scalar_one_or_none()
        if row is None:
            session.add(
                StreamDayAssignment(
                    stream_event_id=ev.id,
                    day_index=d,
                    operator_id=target_operator_id,
                )
            )
        else:
            row.operator_id = target_operator_id

    await _sync_legacy_locked_by(session, ev)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_LOCK,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before={"locked_by": str(before_lock) if before_lock else None},
        payload_after={
            "locked_by": str(ev.locked_by_user_id) if ev.locked_by_user_id else None,
            "days": want_days,
            "operator": str(target_operator_id),
        },
    )
    await session.commit()
    return await get_stream_event_detail(session, stream_id)


async def unlock_stream(session: AsyncSession, *, actor: User, stream_id: UUID) -> StreamEventDetailOut:
    ev = await _get_event(session, stream_id)
    if actor.role == UserRole.STREAM_MANAGER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    prev = ev.locked_by_user_id
    if actor.role == UserRole.SUPERADMIN:
        if await _stream_has_assignments_to_other_than(session, stream_event_id=ev.id, user_id=actor.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Дни назначены операторам — снять назначения может сам оператор",
            )
        await session.execute(delete(StreamDayAssignment).where(StreamDayAssignment.stream_event_id == ev.id))
    else:
        cnt_r = await session.execute(
            select(func.count())
            .select_from(StreamDayAssignment)
            .where(
                StreamDayAssignment.stream_event_id == ev.id,
                StreamDayAssignment.operator_id == actor.id,
            )
        )
        my_days = int(cnt_r.scalar_one() or 0)
        if my_days == 0 and ev.locked_by_user_id != actor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас нет назначенных дней на этом мероприятии",
            )
        await session.execute(
            delete(StreamDayAssignment).where(
                StreamDayAssignment.stream_event_id == ev.id,
                StreamDayAssignment.operator_id == actor.id,
            )
        )
    await _sync_legacy_locked_by(session, ev)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_UNLOCK,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before={"locked_by": str(prev) if prev else None},
        payload_after={"locked_by": str(ev.locked_by_user_id) if ev.locked_by_user_id else None},
    )
    await session.commit()
    return await get_stream_event_detail(session, stream_id)


def _can_control_broadcast(actor: User, ev: StreamEvent, session_operator_id: UUID) -> bool:
    if actor.role == UserRole.SUPERADMIN:
        return True
    if actor.role != UserRole.OPERATOR:
        return False
    return session_operator_id == actor.id


def _can_realign_broadcast_start(actor: User, ev: StreamEvent, session_operator_id: UUID) -> bool:
    if actor.role == UserRole.SUPERADMIN:
        return True
    if actor.role == UserRole.STREAM_MANAGER:
        return True
    if actor.role == UserRole.OPERATOR:
        return session_operator_id == actor.id
    return False


def _can_realign_ended_broadcast(actor: User, bs: BroadcastSession) -> bool:
    """Завершённый эфир: менеджер, суперадмин или оператор, который вёл эту сессию."""
    if actor.role == UserRole.SUPERADMIN:
        return True
    if actor.role == UserRole.STREAM_MANAGER:
        return True
    if actor.role == UserRole.OPERATOR:
        return bs.operator_id == actor.id
    return False


def _datetime_to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=MOSCOW_TZ)
    return dt.astimezone(timezone.utc)


async def start_broadcast(session: AsyncSession, *, actor: User, stream_id: UUID, day_index: int) -> BroadcastSessionOut:
    if day_index < 1 or day_index > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный день")
    ev = await _get_event(session, stream_id)
    if day_index > ev.duration_days:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="День вне длительности мероприятия")
    if await _day_blocked_for_new_broadcast(
        session, stream_id=stream_id, day_index=day_index, duration_days=ev.duration_days
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Этот день уже был в эфире более часа с таймкодами — повторный старт недоступен",
        )
    day_op = await _assignment_operator_for_day(session, stream_id, day_index)
    if day_op is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Сначала назначьте день на оператора: «Взять в работу» (весь турнир или выбранные дни)",
        )
    if actor.role == UserRole.OPERATOR:
        if day_op != actor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет назначения на этот день — возьмите этот день в работу",
            )
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
    if actor.role == UserRole.OPERATOR:
        operator_id = actor.id
    else:
        operator_id = day_op
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
    await create_for_users_with_roles(
        session,
        roles=[UserRole.STREAM_MANAGER, UserRole.SUPERADMIN],
        title="Начало эфира",
        body=f"{ev.title} — день {day_index}",
        kind="broadcast_start",
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


async def realign_broadcast_actual_start(
    session: AsyncSession,
    *,
    actor: User,
    stream_id: UUID,
    day_index: int,
    actual_started_at: datetime,
) -> BroadcastSessionOut:
    """Сдвигает started_at на фактическое время и добавляет дельту ко всем таймкодам упоминаний."""
    if day_index < 1 or day_index > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный день")
    ev = await _get_event(session, stream_id)
    if day_index > ev.duration_days:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="День вне длительности мероприятия")

    result = await session.execute(
        select(BroadcastSession)
        .options(selectinload(BroadcastSession.mentions).selectinload(SponsorMention.adjustments))
        .where(
            and_(
                BroadcastSession.stream_event_id == stream_id,
                BroadcastSession.day_index == day_index,
                BroadcastSession.ended_at.is_(None),
            )
        )
    )
    bs = result.scalar_one_or_none()
    if bs is None:
        result_ended = await session.execute(
            select(BroadcastSession)
            .options(selectinload(BroadcastSession.mentions).selectinload(SponsorMention.adjustments))
            .where(
                and_(
                    BroadcastSession.stream_event_id == stream_id,
                    BroadcastSession.day_index == day_index,
                    BroadcastSession.ended_at.isnot(None),
                )
            )
            .order_by(BroadcastSession.ended_at.desc())
            .limit(1)
        )
        bs = result_ended.scalar_one_or_none()
    if not bs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Эфир для этого дня не найден",
        )

    if bs.ended_at is not None:
        if not _can_realign_ended_broadcast(actor, bs):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для правки времени начала этого завершённого эфира",
            )
    elif not _can_realign_broadcast_start(actor, ev, bs.operator_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

    new_started_utc = _datetime_to_utc(actual_started_at)
    old_started = bs.started_at
    if old_started.tzinfo is None:
        old_started = old_started.replace(tzinfo=timezone.utc)
    else:
        old_started = old_started.astimezone(timezone.utc)

    delta_sec = int((old_started - new_started_utc).total_seconds())

    if new_started_utc > utc_now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Время начала не может быть в будущем",
        )

    if delta_sec == 0:
        return BroadcastSessionOut(
            id=bs.id,
            stream_event_id=bs.stream_event_id,
            day_index=bs.day_index,
            operator_id=bs.operator_id,
            started_at=bs.started_at,
            ended_at=bs.ended_at,
            is_active=bs.ended_at is None,
        )

    mentions = list(bs.mentions)
    for m in mentions:
        if m.original_offset_sec + delta_sec < 0 or m.adjusted_offset_sec + delta_sec < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Указанное время приводит к отрицательным таймкодам. Задайте более раннее время начала эфира "
                "(когда реально пошла картинка).",
            )
    for m in mentions:
        for adj in m.adjustments:
            if adj.previous_adjusted_sec + delta_sec < 0 or adj.new_adjusted_sec + delta_sec < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Указанное время несовместимо с историей правок. Задайте более раннее время начала эфира.",
                )

    for m in mentions:
        m.original_offset_sec += delta_sec
        m.adjusted_offset_sec += delta_sec
        for adj in m.adjustments:
            adj.previous_adjusted_sec += delta_sec
            adj.new_adjusted_sec += delta_sec

    bs.started_at = new_started_utc

    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.BROADCAST_ACTUAL_START,
        entity_type="broadcast_session",
        entity_id=str(bs.id),
        payload_before={"started_at": old_started.isoformat()},
        payload_after={
            "started_at": new_started_utc.isoformat(),
            "delta_sec": delta_sec,
            "day_index": day_index,
        },
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
        is_active=bs.ended_at is None,
    )


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
