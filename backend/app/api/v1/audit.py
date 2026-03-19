import csv
import io
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import SuperAdminUser
from app.db.session import get_db
from app.schemas.audit import AuditLogOut, AuditLogPage
from app.services.audit_service import list_audit_logs, list_audit_logs_all, purge_audit_older_than

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


@router.get("/export.csv")
async def export_audit_csv(
    _: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
    user_id: UUID | None = Query(default=None),
    action_type: str | None = Query(default=None),
) -> Response:
    rows = await list_audit_logs_all(session, user_id=user_id, action_type=action_type, limit=50_000)
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(
        [
            "created_at",
            "action_type",
            "entity_type",
            "entity_id",
            "user_id",
            "payload_before",
            "payload_after",
        ]
    )
    for r in rows:
        w.writerow(
            [
                r.created_at.isoformat() if r.created_at else "",
                r.action_type,
                r.entity_type,
                r.entity_id or "",
                str(r.user_id) if r.user_id else "",
                str(r.payload_before) if r.payload_before is not None else "",
                str(r.payload_after) if r.payload_after is not None else "",
            ]
        )
    return Response(
        content="\ufeff" + buf.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=audit_export.csv"},
    )


class AuditPurgeBody(BaseModel):
    older_than_days: int = Field(ge=1, le=3650)


@router.post("/purge")
async def purge_audit(
    _: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
    body: AuditPurgeBody = AuditPurgeBody(older_than_days=365),
) -> dict[str, int]:
    deleted = await purge_audit_older_than(session, days=body.older_than_days)
    return {"deleted": deleted}
