from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin, OperatorOrAbove
from app.db.session import get_db
from app.schemas.logo import LogoLibraryItemOut
from app.services import logo_service

router = APIRouter(prefix="/logos", tags=["logos"])


@router.post("/upload", response_model=LogoLibraryItemOut)
async def upload_logo_route(
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
) -> LogoLibraryItemOut:
    return await logo_service.upload_logo(session, actor=actor, file=file)


@router.post("/upload-batch", response_model=list[LogoLibraryItemOut])
async def upload_logos_batch_route(
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    files: list[UploadFile] = File(...),
) -> list[LogoLibraryItemOut]:
    return await logo_service.upload_logos_batch(session, actor=actor, files=files)


@router.get("", response_model=list[LogoLibraryItemOut])
async def list_logos_route(
    _: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> list[LogoLibraryItemOut]:
    return await logo_service.list_library(session)
