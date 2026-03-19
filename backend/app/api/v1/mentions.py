from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import OperatorOrAbove
from app.db.session import get_db
from app.models.stream import BroadcastSession
from app.schemas.stream import SponsorMentionOut, SponsorMentionUpdate
from app.services import stream_service
from app.websocket.hub import StreamEventHub

router = APIRouter(tags=["mentions"])


@router.post("/broadcast-sessions/{session_id}/mentions", response_model=SponsorMentionOut)
async def add_mention(
    session_id: UUID,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> SponsorMentionOut:
    out = await stream_service.add_sponsor_mention(session, actor=actor, broadcast_session_id=session_id)
    res = await session.execute(
        select(BroadcastSession.stream_event_id).where(BroadcastSession.id == out.broadcast_session_id)
    )
    stream_event_id = res.scalar_one()
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(
        stream_event_id,
        {"type": "mention_created", "payload": out.model_dump(mode="json")},
    )
    return out


@router.patch("/sponsor-mentions/{mention_id}", response_model=SponsorMentionOut)
async def patch_mention(
    mention_id: UUID,
    body: SponsorMentionUpdate,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> SponsorMentionOut:
    out = await stream_service.update_sponsor_mention(
        session, actor=actor, mention_id=mention_id, new_adjusted_sec=body.adjusted_offset_sec
    )
    res = await session.execute(
        select(BroadcastSession.stream_event_id).where(BroadcastSession.id == out.broadcast_session_id)
    )
    stream_event_id = res.scalar_one()
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(
        stream_event_id,
        {"type": "mention_updated", "payload": out.model_dump(mode="json")},
    )
    return out
