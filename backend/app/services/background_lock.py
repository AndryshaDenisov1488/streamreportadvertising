"""PostgreSQL advisory locks — один исполнитель фоновой задачи при нескольких uvicorn workers."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import TypeVar

from sqlalchemy import text

from app.db.session import AsyncSessionLocal

logger = logging.getLogger(__name__)

# Фиксированные ключи (int64); не менять после деплоя без осознанной миграции.
LOCK_WEEKLY_REPORT = 847_291_001
LOCK_MONTHLY_REPORT = 847_291_002
LOCK_LONG_BROADCAST_ALERTS = 847_291_003
LOCK_FFKM_SYNC = 847_291_004

T = TypeVar("T")


@asynccontextmanager
async def try_advisory_lock(lock_key: int) -> AsyncIterator[bool]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT pg_try_advisory_lock(:key)"), {"key": lock_key})
        acquired = bool(result.scalar())
        try:
            yield acquired
        finally:
            if acquired:
                await session.execute(text("SELECT pg_advisory_unlock(:key)"), {"key": lock_key})
                await session.commit()


async def run_if_leader(lock_key: int, fn: Callable[[], Awaitable[T]]) -> T | None:
    async with try_advisory_lock(lock_key) as acquired:
        if not acquired:
            logger.debug("Background job skipped (advisory lock %s busy)", lock_key)
            return None
        return await fn()
