"""Медиатека логотипов и связь с мероприятиями."""

import io
import re
import zipfile
from pathlib import Path
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.timezone import format_moscow_date
from app.models.enums import AuditActionType
from app.models.logo import Logo, StreamEventLogo
from app.models.stream import StreamEvent
from app.models.user import User
from app.schemas.logo import LogoLibraryItemOut
from app.services.audit_service import write_audit
from app.services.stream_service import _get_event

ALLOWED_LOGO_TYPES = {
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
    "image/svg+xml",
}
MAX_LOGO_BYTES = 15 * 1024 * 1024


def _safe_original_filename(name: str) -> str:
    base = Path(name).name
    if not base or base in (".", ".."):
        return "logo.bin"
    base = re.sub(r"[^\w.\- \u0400-\u04FF]", "_", base)
    return base[:240] if len(base) > 240 else base


def logo_library_item(logo: Logo) -> LogoLibraryItemOut:
    pub = f"/uploads/{logo.stored_path.lstrip('/')}"
    return LogoLibraryItemOut(
        id=logo.id,
        filename_original=logo.filename_original,
        public_url=pub,
        created_at=logo.created_at,
        uploaded_by_id=logo.uploaded_by_id,
    )


async def _persist_one_logo(session: AsyncSession, *, actor: User, file: UploadFile) -> Logo:
    ct = file.content_type or ""
    if ct not in ALLOWED_LOGO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Допустимы только PNG, JPEG, GIF, WebP, SVG",
        )
    raw_name = file.filename or "logo"
    filename_original = _safe_original_filename(raw_name)
    data = await file.read()
    if len(data) > MAX_LOGO_BYTES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл больше 15 МБ")

    settings = get_settings()
    logo = Logo(
        filename_original=filename_original,
        stored_path="",
        uploaded_by_id=actor.id,
    )
    session.add(logo)
    await session.flush()

    subdir = Path(settings.upload_dir) / "logos" / str(logo.id)
    subdir.mkdir(parents=True, exist_ok=True)
    dest_name = filename_original
    dest_path = subdir / dest_name
    dest_path.write_bytes(data)
    rel = f"logos/{logo.id}/{dest_name}"
    logo.stored_path = rel
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.LOGO_UPLOAD,
        entity_type="logo",
        entity_id=str(logo.id),
        payload_before=None,
        payload_after={"filename_original": filename_original, "stored_path": rel},
    )
    return logo


async def upload_logo(session: AsyncSession, *, actor: User, file: UploadFile) -> LogoLibraryItemOut:
    logo = await _persist_one_logo(session, actor=actor, file=file)
    await session.commit()
    await session.refresh(logo)
    return logo_library_item(logo)


async def upload_logos_batch(
    session: AsyncSession, *, actor: User, files: list[UploadFile]
) -> list[LogoLibraryItemOut]:
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нет файлов")
    if len(files) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не более 50 файлов за раз")
    logos: list[Logo] = []
    for f in files:
        logos.append(await _persist_one_logo(session, actor=actor, file=f))
    await session.commit()
    out: list[LogoLibraryItemOut] = []
    for lg in logos:
        await session.refresh(lg)
        out.append(logo_library_item(lg))
    return out


async def list_library(session: AsyncSession) -> list[LogoLibraryItemOut]:
    result = await session.execute(select(Logo).order_by(Logo.created_at.desc()))
    rows = list(result.scalars().all())
    return [logo_library_item(x) for x in rows]


async def _stream_logo_link(
    session: AsyncSession, *, stream_id: UUID, logo_id: UUID
) -> StreamEventLogo | None:
    r = await session.execute(
        select(StreamEventLogo).where(
            StreamEventLogo.stream_event_id == stream_id,
            StreamEventLogo.logo_id == logo_id,
        )
    )
    return r.scalar_one_or_none()


async def attach_logo_to_stream(
    session: AsyncSession, *, actor: User, stream_id: UUID, logo_id: UUID
) -> None:
    await _get_event(session, stream_id)
    lr = await session.execute(select(Logo).where(Logo.id == logo_id))
    logo = lr.scalar_one_or_none()
    if not logo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Логотип не найден")
    if await _stream_logo_link(session, stream_id=stream_id, logo_id=logo_id):
        return
    max_r = await session.execute(
        select(StreamEventLogo.sort_order)
        .where(StreamEventLogo.stream_event_id == stream_id)
        .order_by(StreamEventLogo.sort_order.desc())
        .limit(1)
    )
    mx = max_r.scalar_one_or_none()
    nxt = (int(mx) + 1) if mx is not None else 0
    session.add(StreamEventLogo(stream_event_id=stream_id, logo_id=logo_id, sort_order=nxt))
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.LOGO_ATTACH,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before=None,
        payload_after={"logo_id": str(logo_id), "filename": logo.filename_original},
    )
    await session.commit()


async def detach_logo_from_stream(
    session: AsyncSession, *, actor: User, stream_id: UUID, logo_id: UUID
) -> None:
    await _get_event(session, stream_id)
    link = await _stream_logo_link(session, stream_id=stream_id, logo_id=logo_id)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Связь не найдена")
    await session.delete(link)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.LOGO_DETACH,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before={"logo_id": str(logo_id)},
        payload_after=None,
    )
    await session.commit()


def logo_file_abs_path(stored_path: str) -> Path:
    settings = get_settings()
    return Path(settings.upload_dir) / stored_path


async def get_logo_row(session: AsyncSession, logo_id: UUID) -> Logo | None:
    r = await session.execute(select(Logo).where(Logo.id == logo_id))
    return r.scalar_one_or_none()


async def assert_logo_on_stream(session: AsyncSession, *, stream_id: UUID, logo_id: UUID) -> None:
    await _get_event(session, stream_id)
    link = await _stream_logo_link(session, stream_id=stream_id, logo_id=logo_id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Логотип не прикреплён к этому мероприятию",
        )


def stream_zip_filename(title: str, moscow_date_str: str) -> str:
    safe = re.sub(r"[^\w\-]+", "_", title).strip("_")[:60] or "stream"
    return f"{safe}_{moscow_date_str}_assets.zip"


async def build_stream_logos_zip(session: AsyncSession, *, stream_id: UUID) -> tuple[bytes, str]:
    ev = await _get_event(session, stream_id)
    result = await session.execute(
        select(StreamEventLogo)
        .options(selectinload(StreamEventLogo.logo))
        .where(StreamEventLogo.stream_event_id == stream_id)
        .order_by(StreamEventLogo.sort_order)
    )
    links = list(result.scalars().all())
    if not links:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нет логотипов для выгрузки")

    date_str = format_moscow_date(ev.start_date)
    zip_name = stream_zip_filename(ev.title, date_str)

    buf = io.BytesIO()
    seen_counts: dict[str, int] = {}
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for link in links:
            lg = link.logo
            if not lg:
                continue
            path = logo_file_abs_path(lg.stored_path)
            if not path.is_file():
                continue
            orig = lg.filename_original
            n = seen_counts.get(orig, 0)
            seen_counts[orig] = n + 1
            if n == 0:
                inner = orig
            else:
                stem = Path(orig).stem
                suf = Path(orig).suffix
                inner = f"{stem}_{n}{suf}"
            zf.write(path, arcname=inner)
    buf.seek(0)
    return buf.getvalue(), zip_name
