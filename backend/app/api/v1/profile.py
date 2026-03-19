from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import AnyAuthenticated
from app.db.session import get_db
from app.schemas.audit import AuditLogOut
from app.schemas.profile import MyActivityPage, ProfileUpdate
from app.schemas.user import UserOut
from app.services.audit_service import list_audit_logs
from app.services import profile_service

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=UserOut)
async def get_profile(user: AnyAuthenticated, session: AsyncSession = Depends(get_db)) -> UserOut:
    await session.refresh(user)
    return UserOut.model_validate(user)


@router.patch("", response_model=UserOut)
async def patch_profile(
    body: ProfileUpdate,
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> UserOut:
    u = await profile_service.update_profile(session, user_id=user.id, data=body)
    return UserOut.model_validate(u)


@router.post("/avatar", response_model=UserOut)
async def post_avatar(
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
) -> UserOut:
    u = await profile_service.save_avatar_file(session, user_id=user.id, file=file)
    return UserOut.model_validate(u)


@router.get("/activity", response_model=MyActivityPage)
async def get_my_activity(
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> MyActivityPage:
    items, total = await list_audit_logs(
        session,
        page=page,
        page_size=page_size,
        user_id=user.id,
        action_type=None,
    )
    return MyActivityPage(
        items=[AuditLogOut.model_validate(x) for x in items],
        total=total,
        page=page,
        page_size=page_size,
    )
