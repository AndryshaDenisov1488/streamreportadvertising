from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import AnyAuthenticated
from app.db.session import get_db
from app.schemas.platform import NotificationListOut, NotificationOut
from app.services import notification_service

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=NotificationListOut)
async def list_my_notifications(
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> NotificationListOut:
    items = await notification_service.list_notifications(session, user_id=user.id)
    unread = await notification_service.count_unread(session, user_id=user.id)
    return NotificationListOut(
        items=[NotificationOut.model_validate(x) for x in items],
        unread_count=unread,
    )


@router.post("/{notification_id}/read", status_code=204)
async def mark_notification_read(
    notification_id: UUID,
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> None:
    ok = await notification_service.mark_read(session, user_id=user.id, notification_id=notification_id)
    if ok:
        await session.commit()
    else:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдено")


@router.post("/read-all", status_code=204)
async def mark_all_read(
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> None:
    await notification_service.mark_all_read(session, user_id=user.id)
    await session.commit()
