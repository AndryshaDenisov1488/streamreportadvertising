"""Исходящий push ссылок на трансляцию в ffkm-admin (HMAC webhook)."""

from __future__ import annotations

import json
import logging
import uuid
from datetime import date, timedelta
from typing import Any
from uuid import UUID

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.timezone import now_moscow
from app.models.stream import StreamEvent
from app.utils.webhook import sign_webhook_body

logger = logging.getLogger(__name__)


def _day_date(ev: StreamEvent, day_index: int) -> date:
    return ev.start_date + timedelta(days=int(day_index) - 1)


def build_stream_schedule_payload(ev: StreamEvent) -> list[dict[str, Any]]:
    """По одному эфиру на календарный день турнира (все дни, не только первый)."""
    days = sorted(ev.days or [], key=lambda d: d.day_index)
    schedule: list[dict[str, Any]] = []
    for d in days:
        stream_date = _day_date(ev, d.day_index)
        url = (d.stream_url or "").strip()
        schedule.append(
            {
                "day_index": int(d.day_index),
                "day": int(d.day_index),
                "title": f"День {int(d.day_index)}",
                "stream_date": stream_date.isoformat(),
                "stream_date_ru": stream_date.strftime("%d.%m.%Y"),
                "online_stream_url": url or None,
            }
        )
    return schedule


def filled_stream_urls_in_order(ev: StreamEvent) -> list[str]:
    days = sorted(ev.days or [], key=lambda d: d.day_index)
    out: list[str] = []
    for d in days:
        u = (d.stream_url or "").strip()
        if u:
            out.append(u)
    return out


def primary_stream_url(ev: StreamEvent) -> str | None:
    """Первая непустая ссылка (совместимость). Для сайта/вебхука см. public_online_stream_url."""
    urls = filled_stream_urls_in_order(ev)
    return urls[0] if urls else None


def public_online_stream_url(ev: StreamEvent, *, today: date | None = None) -> str | None:
    """Ссылка для поля online_stream_url: сегодняшний день (МСК), иначе последний заполненный.

    Иначе при уже заполненном дне 1 повторный push с тем же primary часто игнорируется
    на стороне ffkm-admin, и дни 2+ не попадают на ffkm.ru.
    """
    today = today or now_moscow().date()
    days = sorted(ev.days or [], key=lambda d: d.day_index)
    last_filled: str | None = None
    for d in days:
        u = (d.stream_url or "").strip()
        if not u:
            continue
        last_filled = u
        if _day_date(ev, d.day_index) == today:
            return u
    return last_filled


async def build_ffkm_stream_webhook_body(session: AsyncSession, stream_id: UUID) -> dict[str, Any] | None:
    result = await session.execute(
        select(StreamEvent)
        .options(selectinload(StreamEvent.days))
        .where(StreamEvent.id == stream_id)
    )
    ev = result.scalar_one_or_none()
    if ev is None or ev.ffkm_admin_tournament_id is None:
        return None
    schedule = build_stream_schedule_payload(ev)
    filled = filled_stream_urls_in_order(ev)
    return {
        "idempotency_key": f"streaming-stream-{ev.id}-{uuid.uuid4()}",
        "event": "streaming.stream_urls.updated",
        "payload": {
            "tournament_id": int(ev.ffkm_admin_tournament_id),
            "stream_event_id": str(ev.id),
            "online_stream_url": public_online_stream_url(ev),
            "online_stream_url_first": primary_stream_url(ev),
            "online_stream_urls": filled,
            "online_stream_schedule": schedule,
        },
    }


async def push_stream_urls_to_ffkm_admin(session: AsyncSession, stream_id: UUID) -> bool:
    """POST HMAC-signed webhook в ffkm-admin. Возвращает True при успехе / пропуске без URL."""
    settings = get_settings()
    url = (settings.ffkm_stream_webhook_url or "").strip()
    secret = (settings.ffkm_stream_webhook_secret or "").strip()
    if not url:
        logger.warning("ffkm_stream_push_skipped_missing_url stream_id=%s", stream_id)
        return False
    if not secret:
        logger.warning("ffkm_stream_push_skipped_missing_secret")
        return False

    body = await build_ffkm_stream_webhook_body(session, stream_id)
    if body is None:
        logger.info("ffkm_stream_push_skipped_unlinked stream_id=%s", stream_id)
        return False

    raw = json.dumps(body, ensure_ascii=False, default=str).encode("utf-8")
    signature = sign_webhook_body(raw, secret)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Webhook-Signature": signature,
        "X-Idempotency-Key": str(body["idempotency_key"]),
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, content=raw, headers=headers, timeout=12.0)
        if response.status_code >= 400:
            logger.warning(
                "ffkm stream push failed status=%s body=%s",
                response.status_code,
                response.text[:200],
            )
            return False
        logger.info(
            "ffkm stream push ok tournament_id=%s days=%s",
            body["payload"].get("tournament_id"),
            [row.get("day_index") for row in body["payload"].get("online_stream_schedule") or []],
        )
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning("ffkm stream push failed: %s", exc)
        return False
