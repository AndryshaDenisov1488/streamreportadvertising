from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.enums import AuditActionType
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.audit_service import write_audit


async def list_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).order_by(User.created_at.desc()))
    return list(result.scalars().all())


async def get_user(session: AsyncSession, user_id: UUID) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user


async def create_user(session: AsyncSession, *, actor_id: UUID, data: UserCreate) -> User:
    exists = await session.execute(select(User.id).where(User.email == data.email))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email уже занят")
    user = User(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        password_hash=hash_password(data.password),
        role=data.role,
        is_active=data.is_active,
    )
    session.add(user)
    await session.flush()
    await write_audit(
        session,
        user_id=actor_id,
        action_type=AuditActionType.USER_CREATE,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=None,
        payload_after={
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role.value,
        },
    )
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(session: AsyncSession, *, actor_id: UUID, user_id: UUID, data: UserUpdate) -> User:
    user = await get_user(session, user_id)
    before = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "telegram": user.telegram,
        "role": user.role.value,
        "is_active": user.is_active,
    }
    if data.email is not None and data.email != user.email:
        exists = await session.execute(select(User.id).where(User.email == data.email))
        if exists.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email уже занят")
        user.email = data.email
    if data.first_name is not None:
        user.first_name = data.first_name
    if data.last_name is not None:
        user.last_name = data.last_name
    if data.phone is not None:
        user.phone = data.phone or None
    if data.telegram is not None:
        user.telegram = data.telegram or None
    if data.password is not None:
        if len(data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароль не короче 8 символов",
            )
        user.password_hash = hash_password(data.password)
    if data.role is not None:
        user.role = data.role
    if data.is_active is not None:
        user.is_active = data.is_active
    await session.flush()
    await write_audit(
        session,
        user_id=actor_id,
        action_type=AuditActionType.USER_UPDATE,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=before,
        payload_after={
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "telegram": user.telegram,
            "role": user.role.value,
            "is_active": user.is_active,
        },
    )
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, *, actor_id: UUID, user_id: UUID) -> None:
    user = await get_user(session, user_id)
    if user.id == actor_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нельзя удалить себя")
    before = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role.value,
    }
    await session.delete(user)
    await session.flush()
    await write_audit(
        session,
        user_id=actor_id,
        action_type=AuditActionType.USER_DELETE,
        entity_type="user",
        entity_id=str(user_id),
        payload_before=before,
        payload_after=None,
    )
    await session.commit()
