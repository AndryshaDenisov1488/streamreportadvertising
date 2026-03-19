from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.platform_extra import ProductAnalyticsEvent


async def track_event(
    session: AsyncSession, *, user_id: UUID | None, event_name: str, meta: dict | None
) -> None:
    session.add(ProductAnalyticsEvent(user_id=user_id, event_name=event_name, meta=meta))
    await session.commit()


async def summary_last_days(session: AsyncSession, *, days: int = 7) -> list[dict[str, int | str]]:
    since = datetime.now(timezone.utc) - timedelta(days=days)
    q = (
        select(ProductAnalyticsEvent.event_name, func.count().label("cnt"))
        .where(ProductAnalyticsEvent.created_at >= since)
        .group_by(ProductAnalyticsEvent.event_name)
        .order_by(func.count().desc())
    )
    result = await session.execute(q)
    return [{"event_name": r[0], "count": int(r[1])} for r in result.all()]
