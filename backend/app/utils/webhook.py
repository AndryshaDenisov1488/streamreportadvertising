import logging

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)


async def post_external_webhook(event_type: str, payload: dict) -> None:
    settings = get_settings()
    url = (settings.external_webhook_url or "").strip()
    if not url:
        return
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json={"type": event_type, "payload": payload}, timeout=8.0)
    except Exception as exc:
        logger.warning("webhook_failed %s", exc)
