from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import AnyAuthenticated
from app.db.session import get_db
from app.schemas.profile import DashboardSummaryOut
from app.services.dashboard_service import build_dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardSummaryOut)
async def dashboard_summary(
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> DashboardSummaryOut:
    data = await build_dashboard_summary(session, user=user)
    return DashboardSummaryOut(**data)
