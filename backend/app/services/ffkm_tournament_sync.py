"""Синхронизация мероприятий streaming из календаря ffkm-admin."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.stream import StreamDay, StreamEvent
from app.services.ffkm_admin_client import FfkmAdminClient, FfkmAdminClientError

logger = logging.getLogger(__name__)

EXCLUDED_RANKS = frozenset({"official_physical_culture"})
KEEP_RANKS = frozenset(
    {
        "official_sports_significant",
        "official_physical_culture_and_mass_sports_show",
        "all_russian",
    }
)
MAX_DURATION_DAYS = 5


@dataclass
class SyncStats:
    fetched: int = 0
    kept: int = 0
    created: int = 0
    updated: int = 0
    skipped_physical: int = 0
    skipped_before_from_date: int = 0
    skipped_rank: int = 0
    linked_manual: int = 0
    push_attempted: int = 0
    pushed_urls: int = 0
    errors: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "fetched": self.fetched,
            "kept": self.kept,
            "created": self.created,
            "updated": self.updated,
            "skipped_physical": self.skipped_physical,
            "skipped_before_from_date": self.skipped_before_from_date,
            "skipped_rank": self.skipped_rank,
            "linked_manual": self.linked_manual,
            "push_attempted": self.push_attempted,
            "pushed_urls": self.pushed_urls,
            "errors": list(self.errors),
        }


def normalize_rank(rank: Any) -> str:
    if rank is None:
        return ""
    if hasattr(rank, "value"):
        rank = rank.value
    text = str(rank).strip()
    if not text:
        return ""
    return text.lower()


def should_keep_rank(rank: Any) -> bool:
    normalized = normalize_rank(rank)
    if not normalized:
        return False
    if normalized in EXCLUDED_RANKS:
        return False
    return normalized in KEEP_RANKS


def parse_sync_from_date(raw: str | None = None) -> date:
    settings = get_settings()
    value = (raw or settings.ffkm_admin_sync_from_date or "2026-07-01").strip()
    return date.fromisoformat(value)


def _parse_item_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    text = str(value).strip()
    if not text:
        return None
    if "T" in text:
        text = text.split("T", 1)[0]
    return date.fromisoformat(text[:10])


def duration_from_dates(start: date, end: date | None) -> int:
    if end is None or end < start:
        return 1
    days = (end - start).days + 1
    return max(1, min(MAX_DURATION_DAYS, days))


def normalize_title_for_match(title: str) -> str:
    import re

    text = (title or "").lower().strip()
    text = re.sub(r"[^\w\s«»\"'\-]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def titles_match(left: str, right: str) -> bool:
    a = normalize_title_for_match(left)
    b = normalize_title_for_match(right)
    if not a or not b:
        return False
    if a == b:
        return True
    if a in b or b in a:
        return True
    return a[:40] == b[:40]


def tournaments_by_start_date(items: list[dict[str, Any]]) -> dict[date, list[dict[str, Any]]]:
    from collections import defaultdict

    grouped: dict[date, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        start = _parse_item_date(item.get("start_date"))
        if start is not None:
            grouped[start].append(item)
    return grouped


def match_tournament_for_event(ev: StreamEvent, items: list[dict[str, Any]]) -> dict[str, Any] | None:
    by_date = tournaments_by_start_date(items)
    candidates = by_date.get(ev.start_date, [])
    if not candidates:
        return None
    for item in candidates:
        if titles_match(ev.title, str(item.get("title") or "")):
            return item
    return None


async def link_manual_stream_events(
    session: AsyncSession,
    items: list[dict[str, Any]],
) -> int:
    """Привязать вручную созданные мероприятия к турнирам ffkm-admin (дата + название)."""
    result = await session.execute(
        select(StreamEvent).where(StreamEvent.ffkm_admin_tournament_id.is_(None))
    )
    manual_events = result.scalars().all()
    linked = 0
    for ev in manual_events:
        match = match_tournament_for_event(ev, items)
        if not match or match.get("id") is None:
            continue
        ev.ffkm_admin_tournament_id = int(match["id"])
        rank_norm = normalize_rank(match.get("rank"))
        ev.ffkm_admin_rank = rank_norm or None
        linked += 1
    if linked:
        await session.flush()
    return linked


async def ensure_ffkm_link_for_stream(
    session: AsyncSession,
    stream_id: Any,
    *,
    client: FfkmAdminClient | None = None,
) -> bool:
    """Попытаться привязать одно мероприятие перед push ссылок."""
    from uuid import UUID

    sid = stream_id if isinstance(stream_id, UUID) else UUID(str(stream_id))
    result = await session.execute(select(StreamEvent).where(StreamEvent.id == sid))
    ev = result.scalar_one_or_none()
    if ev is None or ev.ffkm_admin_tournament_id is not None:
        return ev is not None and ev.ffkm_admin_tournament_id is not None

    api = client or FfkmAdminClient()
    try:
        items = await api.iter_all_tournaments()
    except FfkmAdminClientError as exc:
        logger.warning("ffkm link lookup failed for %s: %s", sid, exc)
        return False

    match = match_tournament_for_event(ev, items)
    if not match or match.get("id") is None:
        return False
    ev.ffkm_admin_tournament_id = int(match["id"])
    ev.ffkm_admin_rank = normalize_rank(match.get("rank")) or None
    await session.flush()
    return True


async def push_all_linked_stream_urls(session: AsyncSession) -> tuple[int, int]:
    """Отправить ссылки в ffkm-admin для всех привязанных мероприятий с URL."""
    from sqlalchemy.orm import selectinload

    from app.services.ffkm_stream_push import primary_stream_url, push_stream_urls_to_ffkm_admin

    result = await session.execute(
        select(StreamEvent)
        .options(selectinload(StreamEvent.days))
        .where(StreamEvent.ffkm_admin_tournament_id.isnot(None))
    )
    attempted = 0
    pushed = 0
    for ev in result.scalars():
        if not primary_stream_url(ev):
            continue
        attempted += 1
        if await push_stream_urls_to_ffkm_admin(session, ev.id):
            pushed += 1
    return attempted, pushed


async def _ensure_day_rows(
    session: AsyncSession, *, stream_event_id: Any, duration_days: int
) -> None:
    result = await session.execute(
        select(StreamDay).where(StreamDay.stream_event_id == stream_event_id)
    )
    existing = {d.day_index: d for d in result.scalars().all()}
    for idx in range(1, duration_days + 1):
        if idx not in existing:
            session.add(
                StreamDay(
                    stream_event_id=stream_event_id,
                    day_index=idx,
                    stream_url="",
                    server_url="",
                    stream_key="",
                )
            )


async def sync_tournaments_from_ffkm_admin(
    session: AsyncSession,
    *,
    client: FfkmAdminClient | None = None,
) -> SyncStats:
    settings = get_settings()
    stats = SyncStats()
    api = client or FfkmAdminClient()
    from_date = parse_sync_from_date()

    try:
        items = await api.iter_all_tournaments()
    except FfkmAdminClientError as exc:
        stats.errors.append(str(exc))
        logger.warning("ffkm tournament sync failed: %s", exc)
        return stats

    stats.fetched = len(items)

    for item in items:
        try:
            tid_raw = item.get("id")
            if tid_raw is None:
                continue
            tournament_id = int(tid_raw)
            rank = item.get("rank")
            if normalize_rank(rank) in EXCLUDED_RANKS:
                stats.skipped_physical += 1
                continue
            if not should_keep_rank(rank):
                stats.skipped_rank += 1
                continue

            start = _parse_item_date(item.get("start_date"))
            if start is None:
                stats.errors.append(f"tournament {tournament_id}: no start_date")
                continue
            if start < from_date:
                stats.skipped_before_from_date += 1
                continue

            end = _parse_item_date(item.get("end_date"))
            title = (item.get("title") or "").strip() or f"Турнир #{tournament_id}"
            rank_norm = normalize_rank(rank)
            duration = duration_from_dates(start, end)
            stats.kept += 1

            result = await session.execute(
                select(StreamEvent).where(StreamEvent.ffkm_admin_tournament_id == tournament_id)
            )
            ev = result.scalar_one_or_none()
            if ev is None:
                ev = StreamEvent(
                    title=title,
                    start_date=start,
                    duration_days=duration,
                    ffkm_admin_tournament_id=tournament_id,
                    ffkm_admin_rank=rank_norm or None,
                    created_by_id=None,
                )
                session.add(ev)
                await session.flush()
                await _ensure_day_rows(session, stream_event_id=ev.id, duration_days=duration)
                stats.created += 1
            else:
                changed = False
                if ev.title != title:
                    ev.title = title
                    changed = True
                if ev.start_date != start:
                    ev.start_date = start
                    changed = True
                if (ev.ffkm_admin_rank or None) != (rank_norm or None):
                    ev.ffkm_admin_rank = rank_norm or None
                    changed = True
                if ev.duration_days != duration:
                    # Не уменьшаем длительность, если уже больше (локальные дни/эфиры)
                    if duration > ev.duration_days:
                        ev.duration_days = duration
                        changed = True
                    elif duration < ev.duration_days:
                        # Уменьшаем только если нет «лишних» дней с заполненными ключами/URL
                        pass
                    else:
                        pass
                await _ensure_day_rows(session, stream_event_id=ev.id, duration_days=ev.duration_days)
                if changed:
                    stats.updated += 1
        except Exception as exc:  # noqa: BLE001 — собираем ошибки по элементам
            stats.errors.append(f"item error: {exc}")
            logger.exception("ffkm tournament sync item failed")

    try:
        stats.linked_manual = await link_manual_stream_events(session, items)
    except Exception as exc:  # noqa: BLE001
        stats.errors.append(f"link manual: {exc}")
        logger.exception("ffkm manual link failed")

    await session.commit()

    try:
        stats.push_attempted, stats.pushed_urls = await push_all_linked_stream_urls(session)
    except Exception as exc:  # noqa: BLE001
        stats.errors.append(f"push urls: {exc}")
        logger.exception("ffkm stream url push batch failed")

    logger.info(
        "ffkm tournament sync done fetched=%s kept=%s created=%s updated=%s linked=%s pushed=%s/%s from=%s base=%s",
        stats.fetched,
        stats.kept,
        stats.created,
        stats.updated,
        stats.linked_manual,
        stats.pushed_urls,
        stats.push_attempted,
        from_date.isoformat(),
        (settings.ffkm_admin_api_base_url or "")[:60],
    )
    return stats


async def job_ffkm_tournament_sync() -> dict[str, Any]:
    settings = get_settings()
    if not (settings.ffkm_admin_api_base_url or "").strip():
        return {"skipped": True, "reason": "FFKM_ADMIN_API_BASE_URL empty"}
    if not (settings.ffkm_admin_api_token or "").strip():
        return {"skipped": True, "reason": "FFKM_ADMIN_API_TOKEN empty"}
    from app.db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        stats = await sync_tournaments_from_ffkm_admin(session)
        return stats.as_dict()


async def ffkm_tournament_sync_loop() -> None:
    settings = get_settings()
    if not settings.ffkm_admin_sync_enabled:
        logger.info("ffkm tournament sync loop disabled (FFKM_ADMIN_SYNC_ENABLED=false)")
        return
    delay = max(int(settings.ffkm_admin_sync_initial_delay_seconds), 5)
    interval = max(int(settings.ffkm_admin_sync_interval_seconds), 60)
    await asyncio.sleep(delay)
    while True:
        try:
            result = await job_ffkm_tournament_sync()
            logger.info("ffkm tournament sync loop tick: %s", result)
        except asyncio.CancelledError:
            raise
        except Exception:  # noqa: BLE001
            logger.exception("ffkm tournament sync loop failed")
        await asyncio.sleep(interval)
