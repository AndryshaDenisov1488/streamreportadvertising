"""
Authenticated / signed media delivery (SEC-MEDIA-004).

Replaces public StaticFiles `/uploads`. Only `logos/` and `avatars/` objects.
SVG is never served as image/svg+xml (SEC-MEDIA-005).
"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.media_urls import (
    ALLOWED_MEDIA_KINDS,
    guess_safe_media_type,
    normalize_object_key,
    resolve_upload_file,
    verify_media_signature,
)
from app.core.security import parse_uuid
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/media", tags=["media"])
_optional_bearer = HTTPBearer(auto_error=False)


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Требуется авторизация",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Файл не найден",
    )


async def _user_from_bearer(
    credentials: HTTPAuthorizationCredentials,
    session: AsyncSession,
) -> Optional[User]:
    settings = get_settings()
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except (ExpiredSignatureError, JWTError):
        return None
    if not payload or payload.get("type") != "access":
        return None
    sub = payload.get("sub")
    if not sub:
        return None
    try:
        uid = parse_uuid(sub)
    except ValueError:
        return None
    result = await session.execute(select(User).where(User.id == uid))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        return None
    return user


@router.get("/{object_path:path}")
async def get_media_file(
    object_path: str,
    expires: Optional[int] = Query(default=None),
    sig: Optional[str] = Query(default=None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_optional_bearer),
    session: AsyncSession = Depends(get_db),
) -> FileResponse:
    """
    Serve a private media object.

    Access: valid signed URL **or** any authenticated active user.
    """
    object_key = normalize_object_key(object_path)
    if not object_key:
        raise _not_found()

    kind = object_key.split("/", 1)[0]
    if kind not in ALLOWED_MEDIA_KINDS:
        raise _not_found()

    has_valid_signature = False
    if expires is not None and sig:
        has_valid_signature = verify_media_signature(object_key, int(expires), sig)

    if not has_valid_signature:
        if credentials is None or not credentials.credentials:
            raise _unauthorized()
        current_user = await _user_from_bearer(credentials, session)
        if current_user is None:
            raise _unauthorized()

    try:
        file_path, safe_name = resolve_upload_file(object_key)
    except ValueError:
        raise _not_found()

    if not file_path.is_file():
        raise _not_found()

    # SEC-MEDIA-005: refuse to serve SVG even if a legacy file remains on disk
    if file_path.suffix.lower() in {".svg", ".svgz"}:
        raise _not_found()

    media_type = guess_safe_media_type(safe_name)
    return FileResponse(
        path=str(file_path),
        media_type=media_type,
        content_disposition_type="inline",
        headers={
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'none'; sandbox",
        },
    )
