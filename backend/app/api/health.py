from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_live() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "version": settings.app_version}


@router.get("/health/ready")
async def health_ready(session: AsyncSession = Depends(get_db)) -> dict[str, str | None]:
    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready", "database": str(exc)},
        ) from exc
    revision: str | None = None
    try:
        row = await session.execute(text("SELECT version_num FROM alembic_version LIMIT 1"))
        revision = row.scalar_one_or_none()
    except Exception:
        revision = None
    return {
        "status": "ready",
        "database": "ok",
        "alembic_revision": revision,
        "version": get_settings().app_version,
    }
