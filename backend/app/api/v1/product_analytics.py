from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import AnyAuthenticated, SuperAdminUser
from app.db.session import get_db
from app.schemas.platform import AnalyticsIn, AnalyticsRow, AnalyticsSummaryOut
from app.services import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/events", status_code=204)
async def track_event(
    body: AnalyticsIn,
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> None:
    await analytics_service.track_event(
        session,
        user_id=user.id,
        event_name=body.event_name,
        meta=body.meta,
    )


@router.get("/summary", response_model=AnalyticsSummaryOut)
async def analytics_summary(
    _: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
) -> AnalyticsSummaryOut:
    rows = await analytics_service.summary_last_days(session, days=7)
    return AnalyticsSummaryOut(
        by_event=[AnalyticsRow(event_name=r["event_name"], count=r["count"]) for r in rows],
    )
