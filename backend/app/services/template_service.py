import uuid
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import AuditActionType
from app.models.stream import StreamEventTemplate
from app.models.user import User
from app.schemas.stream import StreamDayIn, StreamEventCreate
from app.schemas.templates import StreamEventTemplateCreate, TemplateFromEventBody
from app.services.audit_service import write_audit
from app.services.stream_service import create_stream_event, get_stream_event_detail


async def list_templates(session: AsyncSession) -> list[StreamEventTemplate]:
    result = await session.execute(select(StreamEventTemplate).order_by(StreamEventTemplate.created_at.desc()))
    return list(result.scalars().all())


async def create_template(
    session: AsyncSession, *, actor: User, body: StreamEventTemplateCreate
) -> StreamEventTemplate:
    days_data: list[dict] = []
    if body.days:
        for d in body.days:
            days_data.append(
                {"day_index": d.day_index, "stream_url": d.stream_url, "server_url": d.server_url, "stream_key": d.stream_key}
            )
    else:
        for i in range(1, body.duration_days + 1):
            days_data.append({"day_index": i, "stream_url": "", "server_url": "", "stream_key": ""})
    t = StreamEventTemplate(
        name=body.name,
        title=body.title,
        duration_days=body.duration_days,
        days_json=days_data,
        created_by_id=actor.id,
    )
    session.add(t)
    await session.flush()
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_CREATE,
        entity_type="stream_event_template",
        entity_id=str(t.id),
        payload_before=None,
        payload_after={"name": t.name},
    )
    await session.commit()
    await session.refresh(t)
    return t


async def template_from_event(
    session: AsyncSession, *, actor: User, stream_id: uuid.UUID, body: TemplateFromEventBody
) -> StreamEventTemplate:
    detail = await get_stream_event_detail(session, stream_id)
    days_data = [
        {
            "day_index": d.day_index,
            "stream_url": d.stream_url,
            "server_url": d.server_url,
            "stream_key": d.stream_key,
        }
        for d in detail.days
    ]
    t = StreamEventTemplate(
        name=body.name,
        title=detail.title,
        duration_days=detail.duration_days,
        days_json=days_data,
        created_by_id=actor.id,
    )
    session.add(t)
    await session.flush()
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_CREATE,
        entity_type="stream_event_template",
        entity_id=str(t.id),
        payload_before=None,
        payload_after={"name": t.name, "from_event": str(stream_id)},
    )
    await session.commit()
    await session.refresh(t)
    return t


async def delete_template(session: AsyncSession, *, actor: User, template_id: uuid.UUID) -> None:
    result = await session.execute(select(StreamEventTemplate).where(StreamEventTemplate.id == template_id))
    t = result.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Шаблон не найден")
    await session.delete(t)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_DELETE,
        entity_type="stream_event_template",
        entity_id=str(template_id),
        payload_before={"name": t.name},
        payload_after=None,
    )
    await session.commit()


async def instantiate_template(
    session: AsyncSession, *, actor: User, template_id: uuid.UUID, start_date: date
):
    result = await session.execute(select(StreamEventTemplate).where(StreamEventTemplate.id == template_id))
    t = result.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Шаблон не найден")
    days_in = [StreamDayIn.model_validate(d) for d in t.days_json]
    data = StreamEventCreate(title=t.title, start_date=start_date, duration_days=t.duration_days, days=days_in)
    return await create_stream_event(session, actor=actor, data=data)
