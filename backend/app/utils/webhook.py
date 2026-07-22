"""Outbound stream-event webhooks with HMAC-SHA256 signatures (SEC-WH-004)."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)

# Header consumers must verify against EXTERNAL_WEBHOOK_SECRET
WEBHOOK_SIGNATURE_HEADER = "X-Webhook-Signature"


def sign_webhook_body(body: bytes, secret: str) -> str:
    """Return `sha256=<hex>` HMAC over the exact request body bytes."""
    mac = hmac.new(secret.encode("utf-8"), body, hashlib.sha256)
    return f"sha256={mac.hexdigest()}"


def build_webhook_body(event_type: str, payload: dict) -> bytes:
    """Serialize the webhook JSON body (bytes that will be signed and POSTed)."""
    body_dict = {"type": event_type, "payload": payload}
    return json.dumps(body_dict, ensure_ascii=False, default=str).encode("utf-8")


async def post_external_webhook(event_type: str, payload: dict) -> None:
    settings = get_settings()
    url = (settings.external_webhook_url or "").strip()
    if not url:
        return

    secret = (settings.external_webhook_secret or "").strip()
    if not secret:
        # Fail closed: never send unsigned payloads when URL is configured
        logger.warning("webhook_skipped_missing_secret")
        return

    body = build_webhook_body(event_type, payload)
    signature = sign_webhook_body(body, secret)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        WEBHOOK_SIGNATURE_HEADER: signature,
    }
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, content=body, headers=headers, timeout=8.0)
    except Exception as exc:
        logger.warning("webhook_failed %s", exc)
