from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import UserRole
from app.models.platform_extra import Notification
from app.models.user import User


async def create_for_users_with_roles(
    session: AsyncSession,
    *,
    roles: list[UserRole],
    title: str,
    body: str,
    kind: str | None = None,
) -> None:
    q = select(User.id).where(User.role.in_(roles), User.is_active.is_(True))
    result = await session.execute(q)
    for (uid,) in result.all():
        session.add(
            Notification(
                user_id=uid,
                title=title,
                body=body,
                kind=kind,
            )
        )


async def count_unread(session: AsyncSession, *, user_id: UUID) -> int:
    q = select(func.count()).where(
        Notification.user_id == user_id,
        Notification.is_read.is_(False),
    )
    result = await session.execute(q)
    return int(result.scalar_one() or 0)


async def list_notifications(
    session: AsyncSession, *, user_id: UUID, limit: int = 50
) -> list[Notification]:
    q = (
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(q)
    return list(result.scalars().all())


async def mark_read(session: AsyncSession, *, user_id: UUID, notification_id: UUID) -> bool:
    result = await session.execute(
        select(Notification).where(Notification.id == notification_id, Notification.user_id == user_id)
    )
    n = result.scalar_one_or_none()
    if not n:
        return False
    n.is_read = True
    return True


async def mark_all_read(session: AsyncSession, *, user_id: UUID) -> None:
    result = await session.execute(select(Notification).where(Notification.user_id == user_id, Notification.is_read.is_(False)))
    for n in result.scalars().all():
        n.is_read = True
