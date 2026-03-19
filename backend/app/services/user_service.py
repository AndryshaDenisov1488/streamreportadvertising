import logging
import secrets
from typing import NamedTuple
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import hash_password
from app.models.enums import AuditActionType, UserRole
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.audit_service import write_audit
from app.services.welcome_email_service import send_welcome_email
from app.utils.phone_ru import normalize_ru_mobile_phone

log = logging.getLogger(__name__)


class WelcomeEmailPayload(NamedTuple):
    to_email: str
    first_name: str
    role: UserRole
    plain_password: str


class CreateUserOutcome(NamedTuple):
    user: User
    welcome_email_payload: WelcomeEmailPayload | None
    welcome_email_skipped_reason: str | None


async def list_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).order_by(User.created_at.desc()))
    return list(result.scalars().all())


async def get_user(session: AsyncSession, user_id: UUID) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user


async def create_user(session: AsyncSession, *, actor_id: UUID, data: UserCreate) -> CreateUserOutcome:
    exists = await session.execute(select(User.id).where(User.email == data.email))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email уже занят")

    plain_password = secrets.token_urlsafe(14)

    user = User(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        password_hash=hash_password(plain_password),
        role=data.role,
        is_active=data.is_active,
        suggest_password_change=True,
        onboarding_completed=False,
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
            "password_auto_generated": True,
        },
    )
    await session.commit()
    await session.refresh(user)

    settings = get_settings()
    if not settings.smtp_host.strip():
        return CreateUserOutcome(
            user,
            None,
            "SMTP не настроен (smtp_host пустой в backend/.env) — письма не отправляются",
        )

    payload = WelcomeEmailPayload(
        to_email=user.email,
        first_name=user.first_name,
        role=user.role,
        plain_password=plain_password,
    )
    return CreateUserOutcome(user, payload, None)


async def send_welcome_email_task(payload: WelcomeEmailPayload) -> None:
    """Фоновая отправка после HTTP-ответа (не блокирует создание пользователя)."""
    try:
        await send_welcome_email(
            to_email=payload.to_email,
            first_name=payload.first_name,
            role=payload.role,
            plain_password=payload.plain_password,
        )
        log.info("Welcome email sent to %s", payload.to_email)
    except Exception:
        log.exception("Welcome email failed for %s", payload.to_email)


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
        trimmed = (data.phone or "").strip()
        if not trimmed:
            user.phone = None
        else:
            try:
                user.phone = normalize_ru_mobile_phone(trimmed)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e) or "Некорректный номер телефона",
                ) from e
    if data.telegram is not None:
        user.telegram = data.telegram or None
    if data.password is not None:
        if len(data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароль не короче 8 символов",
            )
        user.password_hash = hash_password(data.password)
        user.suggest_password_change = False
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
