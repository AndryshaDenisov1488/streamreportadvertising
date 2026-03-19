from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import SuperAdminUser
from app.db.session import get_db
from app.schemas.audit import AuditLogOut, AuditLogPage
from app.services.audit_service import list_audit_logs

router = APIRouter(prefix="/audit-logs", tags=["audit"])


@router.get("", response_model=AuditLogPage)
async def list_logs(
    _: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    user_id: UUID | None = Query(default=None),
    action_type: str | None = Query(default=None),
) -> AuditLogPage:
    items, total = await list_audit_logs(
        session,
        page=page,
        page_size=page_size,
        user_id=user_id,
        action_type=action_type,
    )
    return AuditLogPage(
        items=[AuditLogOut.model_validate(x) for x in items],
        total=total,
        page=page,
        page_size=page_size,
    )
