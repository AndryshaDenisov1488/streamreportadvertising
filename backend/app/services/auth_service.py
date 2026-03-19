from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token_payload,
    decode_token_safe,
    verify_password,
)
from app.models.enums import AuditActionType
from app.models.user import RefreshToken, User
from app.services.audit_service import write_audit


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def login_user(
    session: AsyncSession,
    *,
    email: str,
    password: str,
    request_ip: str | None,
) -> tuple[User, str, str, datetime]:
    user = await authenticate_user(session, email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")
    refresh_token, jti, exp = create_refresh_token_payload()
    session.add(
        RefreshToken(
            user_id=user.id,
            jti=jti,
            expires_at=exp,
        )
    )
    await write_audit(
        session,
        user_id=user.id,
        action_type=AuditActionType.LOGIN,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=None,
        payload_after={"email": user.email, "ip": request_ip},
    )
    await session.commit()
    access = create_access_token(subject=str(user.id), role=user.role.value)
    return user, access, refresh_token, exp


async def refresh_access_token(session: AsyncSession, refresh_token: str) -> tuple[User, str]:
    payload = decode_token_safe(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный refresh")
    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный refresh")
    result = await session.execute(select(RefreshToken).where(RefreshToken.jti == jti))
    row = result.scalar_one_or_none()
    if not row or row.revoked_at is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен отозван")
    if row.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истёк")
    user_result = await session.execute(select(User).where(User.id == row.user_id))
    user = user_result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
    access = create_access_token(subject=str(user.id), role=user.role.value)
    return user, access


async def create_fresh_session(
    session: AsyncSession,
    *,
    user: User,
    request_ip: str | None,
) -> tuple[str, str, datetime]:
    """Выдать access + refresh после регистрации по приглашению (и записать LOGIN)."""
    refresh_token, jti, exp = create_refresh_token_payload()
    session.add(
        RefreshToken(
            user_id=user.id,
            jti=jti,
            expires_at=exp,
        )
    )
    await write_audit(
        session,
        user_id=user.id,
        action_type=AuditActionType.LOGIN,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=None,
        payload_after={"email": user.email, "ip": request_ip, "via": "accept_invite"},
    )
    await session.commit()
    access = create_access_token(subject=str(user.id), role=user.role.value)
    return access, refresh_token, exp


async def logout_user(session: AsyncSession, *, user_id: UUID, refresh_token: str | None) -> None:
    if not refresh_token:
        await write_audit(
            session,
            user_id=user_id,
            action_type=AuditActionType.LOGOUT,
            entity_type="user",
            entity_id=str(user_id),
            payload_before=None,
            payload_after=None,
        )
        await session.commit()
        return
    payload = decode_token_safe(refresh_token)
    jti = payload.get("jti") if payload else None
    if jti:
        result = await session.execute(select(RefreshToken).where(RefreshToken.jti == jti))
        row = result.scalar_one_or_none()
        if row and row.user_id == user_id:
            row.revoked_at = datetime.now(timezone.utc)
    await write_audit(
        session,
        user_id=user_id,
        action_type=AuditActionType.LOGOUT,
        entity_type="user",
        entity_id=str(user_id),
        payload_before=None,
        payload_after=None,
    )
    await session.commit()
