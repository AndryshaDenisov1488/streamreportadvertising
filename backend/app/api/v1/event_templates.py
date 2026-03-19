from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin
from app.db.session import get_db
from app.schemas.stream import StreamEventDetailOut
from app.schemas.templates import (
    InstantiateTemplateBody,
    StreamEventTemplateCreate,
    StreamEventTemplateOut,
    TemplateFromEventBody,
)
from app.services import template_service

router = APIRouter(prefix="/stream-event-templates", tags=["stream-event-templates"])


@router.get("", response_model=list[StreamEventTemplateOut])
async def list_templates(
    _: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> list[StreamEventTemplateOut]:
    rows = await template_service.list_templates(session)
    return [StreamEventTemplateOut.model_validate(r) for r in rows]


@router.post("", response_model=StreamEventTemplateOut)
async def create_template(
    body: StreamEventTemplateCreate,
    user: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> StreamEventTemplateOut:
    t = await template_service.create_template(session, actor=user, body=body)
    return StreamEventTemplateOut.model_validate(t)


@router.delete("/{template_id}", status_code=204)
async def delete_template(
    template_id: UUID,
    user: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> None:
    await template_service.delete_template(session, actor=user, template_id=template_id)


@router.post("/from-event/{stream_id}", response_model=StreamEventTemplateOut)
async def template_from_event(
    stream_id: UUID,
    body: TemplateFromEventBody,
    user: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> StreamEventTemplateOut:
    t = await template_service.template_from_event(session, actor=user, stream_id=stream_id, body=body)
    return StreamEventTemplateOut.model_validate(t)


@router.post("/{template_id}/instantiate", response_model=StreamEventDetailOut)
async def instantiate_template(
    template_id: UUID,
    body: InstantiateTemplateBody,
    user: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> StreamEventDetailOut:
    return await template_service.instantiate_template(
        session,
        actor=user,
        template_id=template_id,
        start_date=body.start_date,
    )
