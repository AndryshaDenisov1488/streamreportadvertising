import calendar
from datetime import date, datetime, time, timedelta, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.timezone import MOSCOW_TZ
from app.models.enums import UserRole
from app.models.stream import BroadcastSession, SponsorMention, StreamDayAssignment, StreamEvent
from app.models.user import User
from app.schemas.stats import LockAssignmentOut, OperatorDayStatsOut, OperatorStatsOverviewOut
from app.services.stream_service import _assignment_summary_from_pairs, _load_assignment_pairs
from app.utils.display_name import user_display_name

MENTIONS_PER_BROADCAST = 4


def _moscow_day_bounds_utc(d: date) -> tuple[datetime, datetime]:
    start_local = datetime.combine(d, time.min, tzinfo=MOSCOW_TZ)
    end_local = start_local + timedelta(days=1)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)


def _moscow_range_to_utc(day_from: date, day_to_inclusive: date) -> tuple[datetime, datetime]:
    start_local = datetime.combine(day_from, time.min, tzinfo=MOSCOW_TZ)
    end_local = datetime.combine(day_to_inclusive + timedelta(days=1), time.min, tzinfo=MOSCOW_TZ)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)


def _week_mon_sun_moscow(d: date) -> tuple[date, date]:
    mon = d - timedelta(days=d.weekday())
    sun = mon + timedelta(days=6)
    return mon, sun


def _month_first_last(d: date) -> tuple[date, date]:
    first = d.replace(day=1)
    last = d.replace(day=calendar.monthrange(d.year, d.month)[1])
    return first, last


async def _count_broadcasts(
    session: AsyncSession, operator_id: UUID, start_utc: datetime, end_utc: datetime
) -> int:
    r = await session.execute(
        select(func.count())
        .select_from(BroadcastSession)
        .where(
            BroadcastSession.operator_id == operator_id,
            BroadcastSession.started_at >= start_utc,
            BroadcastSession.started_at < end_utc,
        )
    )
    return int(r.scalar_one() or 0)


async def _count_mentions(
    session: AsyncSession, operator_id: UUID, start_utc: datetime, end_utc: datetime
) -> int:
    r = await session.execute(
        select(func.count())
        .select_from(SponsorMention)
        .join(BroadcastSession, SponsorMention.broadcast_session_id == BroadcastSession.id)
        .where(
            BroadcastSession.operator_id == operator_id,
            SponsorMention.created_at >= start_utc,
            SponsorMention.created_at < end_utc,
        )
    )
    return int(r.scalar_one() or 0)


async def get_operator_stats_overview(session: AsyncSession, *, stat_date: date) -> OperatorStatsOverviewOut:
    week_start, week_end = _week_mon_sun_moscow(stat_date)
    month_start, month_end = _month_first_last(stat_date)
    w0, w1 = _moscow_range_to_utc(week_start, week_end)
    m0, m1 = _moscow_range_to_utc(month_start, month_end)

    # Назначения по дням (сводка по событиям)
    sid_rows = await session.execute(select(StreamDayAssignment.stream_event_id.distinct()))
    stream_ids = list(sid_rows.scalars().all())
    pairs_by = await _load_assignment_pairs(session, stream_ids)
    assignments: list[LockAssignmentOut] = []
    if stream_ids:
        evs = (await session.execute(select(StreamEvent).where(StreamEvent.id.in_(stream_ids)))).scalars().all()
        by_ev = {e.id: e for e in evs}
        for seid in sorted(stream_ids, key=lambda x: (by_ev.get(x).title if by_ev.get(x) else "", str(x))):
            ev = by_ev.get(seid)
            if not ev:
                continue
            summary = _assignment_summary_from_pairs(pairs_by.get(seid, [])) or "—"
            assignments.append(
                LockAssignmentOut(
                    stream_event_id=seid,
                    title=ev.title,
                    summary=summary,
                )
            )

    users_result = await session.execute(
        select(User).where(User.role == UserRole.OPERATOR, User.is_active.is_(True)).order_by(User.email)
    )
    operators_list = list(users_result.scalars().all())

    operators: list[OperatorDayStatsOut] = []
    tb_w = tm_w = tb_m = tm_m = 0
    for u in operators_list:
        bw = await _count_broadcasts(session, u.id, w0, w1)
        mw = await _count_mentions(session, u.id, w0, w1)
        bm = await _count_broadcasts(session, u.id, m0, m1)
        mm = await _count_mentions(session, u.id, m0, m1)
        tb_w += bw
        tm_w += mw
        tb_m += bm
        tm_m += mm
        norm_w = MENTIONS_PER_BROADCAST * bw
        norm_m = MENTIONS_PER_BROADCAST * bm
        met_w = mw >= norm_w if bw > 0 else True
        met_m = mm >= norm_m if bm > 0 else True
        operators.append(
            OperatorDayStatsOut(
                operator_id=u.id,
                email=u.email,
                display_name=user_display_name(u),
                role=u.role.value,
                broadcasts_week=bw,
                mentions_week=mw,
                mentions_norm_week=norm_w,
                mentions_met_week=met_w,
                broadcasts_month=bm,
                mentions_month=mm,
                mentions_norm_month=norm_m,
                mentions_met_month=met_m,
            )
        )

    return OperatorStatsOverviewOut(
        stat_date=stat_date,
        week_start=week_start,
        week_end=week_end,
        month_start=month_start,
        month_end=month_end,
        assignments=assignments,
        operators=operators,
        total_broadcasts_week=tb_w,
        total_mentions_week=tm_w,
        total_broadcasts_month=tb_m,
        total_mentions_month=tm_m,
    )
