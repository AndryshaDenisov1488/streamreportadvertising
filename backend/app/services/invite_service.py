import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.enums import AuditActionType, UserRole
from app.models.platform_extra import UserInvite
from app.models.user import User
from app.schemas.platform import AcceptInviteIn, InviteCreate
from app.services.audit_service import write_audit


async def create_invite(
    session: AsyncSession, *, actor_id: UUID, data: InviteCreate, expires_days: int = 7
) -> str:
    exists = await session.execute(select(User.id).where(User.email == data.email))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с таким email уже есть")
    token = secrets.token_urlsafe(48)[:64]
    now = datetime.now(timezone.utc)
    inv = UserInvite(
        token=token,
        email=data.email,
        role=data.role,
        created_by_user_id=actor_id,
        expires_at=now + timedelta(days=expires_days),
    )
    session.add(inv)
    await session.flush()
    await write_audit(
        session,
        user_id=actor_id,
        action_type=AuditActionType.USER_CREATE,
        entity_type="user_invite",
        entity_id=str(inv.id),
        payload_before=None,
        payload_after={"email": data.email, "role": data.role.value},
    )
    await session.commit()
    return token


async def accept_invite(session: AsyncSession, body: AcceptInviteIn) -> User:
    result = await session.execute(select(UserInvite).where(UserInvite.token == body.token))
    inv = result.scalar_one_or_none()
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Приглашение не найдено")
    if inv.used_at is not None:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Приглашение уже использовано")
    if inv.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Срок приглашения истёк")
    exists = await session.execute(select(User.id).where(User.email == inv.email))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email уже зарегистрирован")
    user = User(
        email=inv.email,
        first_name=body.first_name,
        last_name=body.last_name,
        password_hash=hash_password(body.password),
        role=inv.role,
        is_active=True,
    )
    session.add(user)
    inv.used_at = datetime.now(timezone.utc)
    await session.flush()
    await write_audit(
        session,
        user_id=user.id,
        action_type=AuditActionType.USER_CREATE,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=None,
        payload_after={"email": user.email, "via": "invite"},
    )
    await session.commit()
    await session.refresh(user)
    return user
