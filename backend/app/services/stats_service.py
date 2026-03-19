from datetime import date, datetime, time, timedelta, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.timezone import MOSCOW_TZ
from app.models.stream import BroadcastSession, SponsorMention, StreamEvent
from app.models.user import User
from app.schemas.stats import LockAssignmentOut, OperatorDayStatsOut, OperatorStatsOverviewOut
from app.utils.display_name import user_display_name


def _moscow_day_bounds_utc(d: date) -> tuple[datetime, datetime]:
    start_local = datetime.combine(d, time.min, tzinfo=MOSCOW_TZ)
    end_local = start_local + timedelta(days=1)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)


async def get_operator_stats_overview(session: AsyncSession, *, stat_date: date) -> OperatorStatsOverviewOut:
    start_utc, end_utc = _moscow_day_bounds_utc(stat_date)

    # Текущие назначения: события с блокировкой
    q_locks = (
        select(StreamEvent, User)
        .join(User, StreamEvent.locked_by_user_id == User.id)
        .where(StreamEvent.locked_by_user_id.isnot(None))
        .order_by(StreamEvent.title.asc())
    )
    lock_rows = (await session.execute(q_locks)).all()
    assignments = [
        LockAssignmentOut(
            stream_event_id=ev.id,
            title=ev.title,
            locked_by_user_id=u.id,
            locked_by_email=u.email,
            locked_by_display_name=user_display_name(u),
        )
        for ev, u in lock_rows
    ]

    # Трансляции за сутки (МСК): по оператору
    q_bs = (
        select(BroadcastSession.operator_id, func.count(BroadcastSession.id))
        .where(BroadcastSession.started_at >= start_utc, BroadcastSession.started_at < end_utc)
        .group_by(BroadcastSession.operator_id)
    )
    bs_counts: dict[UUID, int] = {}
    for oid, cnt in (await session.execute(q_bs)).all():
        bs_counts[oid] = int(cnt)

    # Упоминания за сутки: по оператору сессии
    q_m = (
        select(BroadcastSession.operator_id, func.count(SponsorMention.id))
        .join(SponsorMention, SponsorMention.broadcast_session_id == BroadcastSession.id)
        .where(SponsorMention.created_at >= start_utc, SponsorMention.created_at < end_utc)
        .group_by(BroadcastSession.operator_id)
    )
    m_counts: dict[UUID, int] = {}
    for oid, cnt in (await session.execute(q_m)).all():
        m_counts[oid] = int(cnt)

    all_ids = set(bs_counts) | set(m_counts)
    if not all_ids:
        return OperatorStatsOverviewOut(
            stat_date=stat_date,
            assignments=assignments,
            operators=[],
            total_broadcasts_day=sum(bs_counts.values()),
            total_mentions_day=sum(m_counts.values()),
        )

    users_result = await session.execute(select(User).where(User.id.in_(list(all_ids))))
    users_list = users_result.scalars().all()
    by_id = {u.id: u for u in users_list}

    operators: list[OperatorDayStatsOut] = []
    for uid in sorted(all_ids, key=lambda x: str(x)):
        u = by_id.get(uid)
        if not u:
            continue
        operators.append(
            OperatorDayStatsOut(
                operator_id=u.id,
                email=u.email,
                display_name=user_display_name(u),
                role=u.role.value,
                broadcasts_count=bs_counts.get(uid, 0),
                mentions_count=m_counts.get(uid, 0),
            )
        )

    return OperatorStatsOverviewOut(
        stat_date=stat_date,
        assignments=assignments,
        operators=operators,
        total_broadcasts_day=sum(bs_counts.values()),
        total_mentions_day=sum(m_counts.values()),
    )
