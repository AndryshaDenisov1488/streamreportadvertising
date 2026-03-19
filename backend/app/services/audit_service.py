from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog
from app.models.enums import AuditActionType


async def list_audit_logs(
    session: AsyncSession,
    *,
    page: int,
    page_size: int,
    user_id: UUID | None,
    action_type: str | None,
) -> tuple[list[AuditLog], int]:
    q = select(AuditLog).order_by(AuditLog.created_at.desc())
    count_base = select(func.count()).select_from(AuditLog)
    if user_id is not None:
        q = q.where(AuditLog.user_id == user_id)
        count_base = count_base.where(AuditLog.user_id == user_id)
    if action_type:
        q = q.where(AuditLog.action_type == action_type)
        count_base = count_base.where(AuditLog.action_type == action_type)
    total_result = await session.execute(count_base)
    total = int(total_result.scalar_one())
    q = q.offset((page - 1) * page_size).limit(page_size)
    result = await session.execute(q)
    return list(result.scalars().all()), total


async def write_audit(
    session: AsyncSession,
    *,
    user_id: UUID | None,
    action_type: AuditActionType,
    entity_type: str,
    entity_id: str | None,
    payload_before: dict[str, Any] | None,
    payload_after: dict[str, Any] | None,
) -> None:
    log = AuditLog(
        user_id=user_id,
        action_type=action_type.value,
        entity_type=entity_type,
        entity_id=entity_id,
        payload_before=payload_before,
        payload_after=payload_after,
    )
    session.add(log)


async def list_audit_logs_all(
    session: AsyncSession,
    *,
    user_id: UUID | None,
    action_type: str | None,
    limit: int = 50_000,
) -> list[AuditLog]:
    q = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    if user_id is not None:
        q = q.where(AuditLog.user_id == user_id)
    if action_type:
        q = q.where(AuditLog.action_type == action_type)
    result = await session.execute(q)
    return list(result.scalars().all())


async def purge_audit_older_than(session: AsyncSession, *, days: int) -> int:
    if days <= 0:
        return 0
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    result = await session.execute(delete(AuditLog).where(AuditLog.created_at < cutoff))
    await session.commit()
    return int(result.rowcount or 0)
