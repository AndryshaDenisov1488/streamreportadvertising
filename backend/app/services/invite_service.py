import logging
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.enums import AuditActionType, UserRole
from app.models.platform_extra import UserInvite
from app.models.user import User
from app.schemas.platform import AcceptInviteIn, InviteCreate
from app.services.audit_service import write_audit
from app.services.invite_email_service import accept_invite_url, require_invite_mail_ready, send_invite_email

log = logging.getLogger(__name__)

INVITE_TTL_DAYS = 7


def split_full_name(full_name: str) -> tuple[str, str]:
    """Фамилия — первое слово, имя и отчество — остальное."""
    parts = full_name.split()
    if len(parts) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Укажите фамилию и имя")
    last_name = parts[0]
    first_name = " ".join(parts[1:])
    if len(last_name) > 100 or len(first_name) > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ФИО слишком длинное")
    return first_name, last_name


def invite_full_name(invite: UserInvite) -> str:
    return f"{invite.last_name} {invite.first_name}".strip()


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


async def list_pending_invites(session: AsyncSession) -> list[UserInvite]:
    now = datetime.now(timezone.utc)
    result = await session.execute(
        select(UserInvite)
        .where(UserInvite.used_at.is_(None), UserInvite.expires_at > now)
        .order_by(UserInvite.created_at.desc())
    )
    return list(result.scalars().all())


async def create_invite(session: AsyncSession, *, actor_id: UUID, data: InviteCreate) -> UserInvite:
    require_invite_mail_ready()
    email = str(data.email).strip().lower()
    first_name, last_name = split_full_name(data.full_name)
    exists = await session.execute(select(User.id).where(func.lower(User.email) == email))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с таким email уже есть")

    now = datetime.now(timezone.utc)
    previous = await session.execute(
        select(UserInvite).where(func.lower(UserInvite.email) == email, UserInvite.used_at.is_(None))
    )
    for old in previous.scalars().all():
        old.expires_at = now

    token = secrets.token_urlsafe(48)[:64]
    invite = UserInvite(
        token=token,
        email=email,
        first_name=first_name,
        last_name=last_name,
        role=data.role,
        created_by_user_id=actor_id,
        expires_at=now + timedelta(days=INVITE_TTL_DAYS),
    )
    session.add(invite)
    await session.flush()
    await write_audit(
        session,
        user_id=actor_id,
        action_type=AuditActionType.USER_CREATE,
        entity_type="user_invite",
        entity_id=str(invite.id),
        payload_before=None,
        payload_after={"email": email, "role": data.role.value, "full_name": data.full_name},
    )
    await session.commit()
    await session.refresh(invite)

    try:
        link = accept_invite_url(invite.token)
        await send_invite_email(
            to_email=invite.email,
            full_name=invite_full_name(invite),
            role=invite.role,
            accept_url=link,
        )
    except HTTPException:
        await discard_invite(session, invite.id)
        raise
    except Exception as exc:
        log.exception("invite email failed for %s", invite.email)
        await discard_invite(session, invite.id)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Письмо не отправилось, приглашение отменено. Проверьте почту на сервере.",
        ) from exc
    return invite


async def discard_invite(session: AsyncSession, invite_id: UUID) -> None:
    invite = await session.get(UserInvite, invite_id)
    if invite is None or invite.used_at is not None:
        return
    await session.delete(invite)
    await session.commit()


async def preview_invite(session: AsyncSession, token: str) -> UserInvite | None:
    result = await session.execute(select(UserInvite).where(UserInvite.token == token))
    invite = result.scalar_one_or_none()
    if invite is None or invite.used_at is not None:
        return None
    if _as_utc(invite.expires_at) < datetime.now(timezone.utc):
        return None
    if not (invite.first_name or "").strip() or not (invite.last_name or "").strip():
        return None
    return invite


async def accept_invite(session: AsyncSession, body: AcceptInviteIn) -> User:
    result = await session.execute(select(UserInvite).where(UserInvite.token == body.token))
    invite = result.scalar_one_or_none()
    if not invite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Приглашение не найдено")
    if invite.used_at is not None:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Приглашение уже использовано")
    if _as_utc(invite.expires_at) < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Срок приглашения истёк")
    first_name = (invite.first_name or "").strip()
    last_name = (invite.last_name or "").strip()
    if not first_name or not last_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В приглашении нет ФИО. Попросите отправить его заново.",
        )
    exists = await session.execute(select(User.id).where(func.lower(User.email) == invite.email.lower()))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email уже зарегистрирован")
    user = User(
        email=invite.email,
        first_name=first_name,
        last_name=last_name,
        password_hash=hash_password(body.password),
        role=invite.role if isinstance(invite.role, UserRole) else UserRole(invite.role),
        is_active=True,
        suggest_password_change=False,
        onboarding_completed=True,
    )
    session.add(user)
    invite.used_at = datetime.now(timezone.utc)
    await session.flush()
    await write_audit(
        session,
        user_id=user.id,
        action_type=AuditActionType.USER_CREATE,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=None,
        payload_after={"email": user.email, "role": user.role.value, "via": "invite"},
    )
    await session.commit()
    await session.refresh(user)
    return user
