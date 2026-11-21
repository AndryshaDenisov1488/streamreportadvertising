from functools import lru_cache
from pathlib import Path

from alembic.script import ScriptDirectory
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


@lru_cache(maxsize=1)
def migration_heads() -> frozenset[str]:
    directory = Path(__file__).resolve().parents[2] / "alembic"
    return frozenset(ScriptDirectory(str(directory)).get_heads())


@router.get("/health/ready")
async def health_ready(session: AsyncSession = Depends(get_db)) -> dict[str, str | None]:
    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready", "database": "unavailable"},
        ) from exc
    try:
        rows = await session.execute(text("SELECT version_num FROM alembic_version"))
        revisions = frozenset(rows.scalars().all())
        ready = bool(revisions) and revisions == migration_heads()
    except Exception:
        ready = False
    if not ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready", "database": "schema_unavailable"},
        )
    return {
        "status": "ready",
        "database": "ok",
        "alembic_revision": ",".join(sorted(revisions)),
        "version": get_settings().app_version,
    }
