import uuid
from pathlib import Path
from typing import Any

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.user import User
from app.schemas.profile import ProfileUpdate


async def update_profile(session: AsyncSession, *, user_id: uuid.UUID, data: ProfileUpdate) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    if data.first_name is not None:
        user.first_name = data.first_name
    if data.last_name is not None:
        user.last_name = data.last_name
    if data.phone is not None:
        user.phone = data.phone or None
    if data.telegram is not None:
        user.telegram = data.telegram or None
    if data.onboarding_completed is not None:
        user.onboarding_completed = data.onboarding_completed
    await session.commit()
    await session.refresh(user)
    return user


ALLOWED_AVATAR = {"image/jpeg", "image/png", "image/webp"}
EXT = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}


async def save_avatar_file(
    session: AsyncSession,
    *,
    user_id: uuid.UUID,
    file: UploadFile,
) -> User:
    if file.content_type not in ALLOWED_AVATAR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Допустимы только JPEG, PNG, WebP",
        )
    settings = get_settings()
    base = Path(settings.upload_dir) / "avatars"
    base.mkdir(parents=True, exist_ok=True)
    ext = EXT.get(file.content_type, ".bin")
    dest = base / f"{user_id}{ext}"
    data = await file.read()
    if len(data) > 2 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл больше 2 МБ")
    dest.write_bytes(data)
    public_path = f"/uploads/avatars/{user_id}{ext}"
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    user.avatar_url = public_path
    await session.commit()
    await session.refresh(user)
    return user
