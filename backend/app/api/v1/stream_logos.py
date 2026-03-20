import io
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin, OperatorOrAbove
from app.db.session import get_db
from app.models.enums import AuditActionType
from app.schemas.logo import LogoAttachBody
from app.services import logo_service
from app.services.audit_service import write_audit

router = APIRouter(prefix="/stream-events", tags=["stream-events"])


@router.post("/{stream_id}/logos", status_code=204)
async def attach_logo_route(
    stream_id: UUID,
    body: LogoAttachBody,
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> None:
    await logo_service.attach_logo_to_stream(session, actor=actor, stream_id=stream_id, logo_id=body.logo_id)


@router.delete("/{stream_id}/logos/{logo_id}", status_code=204)
async def detach_logo_route(
    stream_id: UUID,
    logo_id: UUID,
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> None:
    await logo_service.detach_logo_from_stream(session, actor=actor, stream_id=stream_id, logo_id=logo_id)


@router.get("/{stream_id}/logos/archive.zip")
async def download_logos_zip_route(
    stream_id: UUID,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    data, zip_name = await logo_service.build_stream_logos_zip(session, stream_id=stream_id)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.LOGO_DOWNLOAD_ARCHIVE,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before=None,
        payload_after={"zip_name": zip_name},
    )
    await session.commit()
    headers = {"Content-Disposition": f'attachment; filename="{zip_name}"'}
    return StreamingResponse(io.BytesIO(data), media_type="application/zip", headers=headers)


@router.get("/{stream_id}/logos/{logo_id}/file")
async def download_logo_file_route(
    stream_id: UUID,
    logo_id: UUID,
    _: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> FileResponse:
    await logo_service.assert_logo_on_stream(session, stream_id=stream_id, logo_id=logo_id)
    logo = await logo_service.get_logo_row(session, logo_id)
    if not logo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Логотип не найден")
    path = logo_service.logo_file_abs_path(logo.stored_path)
    if not path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Файл на диске не найден")
    return FileResponse(
        path=str(path),
        filename=logo.filename_original,
        media_type="application/octet-stream",
    )
