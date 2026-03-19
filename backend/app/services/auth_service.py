from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token_payload,
    decode_token_safe,
    hash_password,
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
    user_agent: str | None = None,
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
            user_agent=(user_agent[:500] if user_agent else None),
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
    user_agent: str | None = None,
) -> tuple[str, str, datetime]:
    """Выдать access + refresh после регистрации по приглашению (и записать LOGIN)."""
    refresh_token, jti, exp = create_refresh_token_payload()
    session.add(
        RefreshToken(
            user_id=user.id,
            jti=jti,
            expires_at=exp,
            user_agent=(user_agent[:500] if user_agent else None),
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


async def change_password(
    session: AsyncSession,
    *,
    user_id: UUID,
    current_password: str,
    new_password: str,
    current_jti: str | None,
) -> None:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    if not verify_password(current_password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный текущий пароль")
    user.password_hash = hash_password(new_password)
    await session.flush()
    now = datetime.now(timezone.utc)
    rt_result = await session.execute(
        select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))
    )
    for row in rt_result.scalars().all():
        if current_jti and row.jti == current_jti:
            continue
        row.revoked_at = now
    await write_audit(
        session,
        user_id=user_id,
        action_type=AuditActionType.USER_UPDATE,
        entity_type="user",
        entity_id=str(user_id),
        payload_before=None,
        payload_after={"password_changed": True},
    )
    await session.commit()


async def list_active_refresh_tokens(session: AsyncSession, *, user_id: UUID) -> list[RefreshToken]:
    now = datetime.now(timezone.utc)
    result = await session.execute(
        select(RefreshToken)
        .where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked_at.is_(None),
            RefreshToken.expires_at > now,
        )
        .order_by(RefreshToken.created_at.desc())
    )
    return list(result.scalars().all())


async def revoke_refresh_session_by_id(session: AsyncSession, *, user_id: UUID, session_id: UUID) -> None:
    result = await session.execute(
        select(RefreshToken).where(RefreshToken.id == session_id, RefreshToken.user_id == user_id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сессия не найдена")
    if row.revoked_at is None:
        row.revoked_at = datetime.now(timezone.utc)
    await session.commit()
