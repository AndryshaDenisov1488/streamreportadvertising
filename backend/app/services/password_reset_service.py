import hashlib
import logging
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import hash_password
from app.models.enums import AuditActionType
from app.models.user import PasswordResetToken, RefreshToken, User
from app.services.audit_service import write_audit

log = logging.getLogger(__name__)


def hash_reset_token(raw: str) -> str:
    return hashlib.sha256(raw.strip().encode("utf-8")).hexdigest()


async def request_password_reset(session: AsyncSession, *, email: str) -> tuple[str | None, str | None, str]:
    """
    При активном пользователе и настроенных SMTP + APP_PUBLIC_BASE_URL создаёт токен.
    Возвращает (reset_link, to_email, greeting_name) для фоновой отправки; link/email могут быть None.
    """
    settings = get_settings()
    normalized = (email or "").strip().lower()
    greeting = ""
    if not normalized:
        return None, None, greeting
    result = await session.execute(select(User).where(func.lower(User.email) == normalized))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        return None, None, greeting
    greeting = (user.first_name or "").strip() or user.email.split("@", 1)[0]
    base = (settings.app_public_base_url or "").strip().rstrip("/")
    smtp_ok = bool((settings.smtp_host or "").strip())
    if not smtp_ok or not base:
        log.warning(
            "Password reset skipped: need SMTP_HOST and APP_PUBLIC_BASE_URL (user_id=%s)",
            user.id,
        )
        return None, None, greeting
    await session.execute(
        delete(PasswordResetToken).where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        )
    )
    raw = secrets.token_urlsafe(40)
    token_hash = hash_reset_token(raw)
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.password_reset_expire_minutes)
    session.add(
        PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=exp,
        )
    )
    await session.commit()
    reset_link = f"{base}/reset-password?token={raw}"
    return reset_link, user.email, greeting


async def token_is_valid(session: AsyncSession, *, raw_token: str) -> bool:
    if not raw_token or len(raw_token) < 20:
        return False
    th = hash_reset_token(raw_token)
    now = datetime.now(timezone.utc)
    result = await session.execute(
        select(PasswordResetToken.id).where(
            PasswordResetToken.token_hash == th,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > now,
        )
    )
    return result.scalar_one_or_none() is not None


async def reset_password_with_token(session: AsyncSession, *, raw_token: str, new_password: str) -> None:
    if not raw_token or len(raw_token) < 20:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недействительная ссылка")
    th = hash_reset_token(raw_token)
    now = datetime.now(timezone.utc)
    result = await session.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == th,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > now,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ссылка недействительна или истекла. Запросите новую на странице входа.",
        )
    user_result = await session.execute(select(User).where(User.id == row.user_id))
    user = user_result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь не найден")
    user.password_hash = hash_password(new_password)
    user.suggest_password_change = False
    row.used_at = now
    rt_result = await session.execute(
        select(RefreshToken).where(RefreshToken.user_id == user.id, RefreshToken.revoked_at.is_(None))
    )
    for rt in rt_result.scalars().all():
        rt.revoked_at = now
    await write_audit(
        session,
        user_id=user.id,
        action_type=AuditActionType.USER_UPDATE,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=None,
        payload_after={"password_reset_via_email": True},
    )
    await session.commit()
