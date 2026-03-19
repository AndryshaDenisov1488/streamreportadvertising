from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import SuperAdminUser
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserOut])
async def list_users(
    _: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
) -> list[UserOut]:
    users = await user_service.list_users(session)
    return [UserOut.model_validate(u) for u in users]


@router.post("", response_model=UserOut)
async def create_user(
    body: UserCreate,
    actor: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
) -> UserOut:
    user = await user_service.create_user(session, actor_id=actor.id, data=body)
    return UserOut.model_validate(user)


@router.patch("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: UUID,
    body: UserUpdate,
    actor: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
) -> UserOut:
    user = await user_service.update_user(session, actor_id=actor.id, user_id=user_id, data=body)
    return UserOut.model_validate(user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID,
    actor: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
) -> None:
    await user_service.delete_user(session, actor_id=actor.id, user_id=user_id)
