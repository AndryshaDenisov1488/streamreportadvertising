from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin
from app.core.timezone import now_moscow
from app.db.session import get_db
from app.schemas.stats import OperatorStatsOverviewOut
from app.services.stats_service import get_operator_stats_overview

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/operators", response_model=OperatorStatsOverviewOut)
async def operator_stats(
    _: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    stat_date: date | None = Query(
        default=None,
        description="Календарный день по Москве; по умолчанию — сегодня",
    ),
) -> OperatorStatsOverviewOut:
    d = stat_date or now_moscow().date()
    return await get_operator_stats_overview(session, stat_date=d)
