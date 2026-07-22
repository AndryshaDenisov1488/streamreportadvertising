"""
Signed media URL helpers (SEC-MEDIA-004).

Public StaticFiles `/uploads` is removed; logos and avatars are served via
`/api/v1/media/...` with a short-lived HMAC signature (or Bearer auth).
"""
from __future__ import annotations

import hashlib
import hmac
import time
from pathlib import Path
from typing import Optional
from urllib.parse import quote

from app.core.config import get_settings

ALLOWED_MEDIA_KINDS = frozenset({"logos", "avatars"})


def _signing_key() -> bytes:
    return get_settings().jwt_secret.encode("utf-8")


def backend_public_base_url() -> str:
    """Optional absolute API host from APP_PUBLIC_BASE_URL (panel origin)."""
    settings = get_settings()
    base = (settings.app_public_base_url or "").rstrip("/")
    return base


def normalize_object_key(stored_path: str) -> Optional[str]:
    """
    Normalize a stored path / legacy `/uploads/...` URL to an object key
    under UPLOAD_DIR, e.g. `logos/{uuid}/file.png` or `avatars/{user_id}.jpg`.
    """
    if not stored_path or not str(stored_path).strip():
        return None

    raw = str(stored_path).strip().replace("\\", "/")
    if raw.startswith("http://") or raw.startswith("https://"):
        return None

    raw = raw.split("?", 1)[0]
    raw = raw.lstrip("/")
    if raw.startswith("uploads/"):
        raw = raw[len("uploads/") :]
    if raw.startswith("api/v1/media/"):
        raw = raw[len("api/v1/media/") :]

    if not raw or ".." in raw.split("/"):
        return None

    kind, _, rest = raw.partition("/")
    if kind not in ALLOWED_MEDIA_KINDS or not rest:
        return None
    if any(p in ("", ".", "..") for p in rest.split("/")):
        return None

    return f"{kind}/{rest}"


def create_media_signature(object_key: str, expires_at: int) -> str:
    payload = f"{object_key}:{expires_at}".encode("utf-8")
    return hmac.new(_signing_key(), payload, hashlib.sha256).hexdigest()


def verify_media_signature(object_key: str, expires_at: int, signature: str) -> bool:
    if not signature or expires_at <= 0:
        return False
    if int(time.time()) > int(expires_at):
        return False
    expected = create_media_signature(object_key, int(expires_at))
    return hmac.compare_digest(expected, signature)


def build_signed_media_url(object_key: str, ttl_seconds: Optional[int] = None) -> str:
    key = normalize_object_key(object_key)
    if not key:
        raise ValueError("unsupported media object key")

    settings = get_settings()
    ttl = ttl_seconds if ttl_seconds is not None else settings.media_signed_url_ttl_seconds
    expires_at = int(time.time()) + max(60, int(ttl))
    signature = create_media_signature(key, expires_at)
    encoded = "/".join(quote(part, safe="._-") for part in key.split("/"))
    base = backend_public_base_url()
    prefix = settings.api_v1_prefix.rstrip("/")
    return f"{base}{prefix}/media/{encoded}?expires={expires_at}&sig={signature}"


def build_signed_media_url_from_stored(
    stored_path: Optional[str], ttl_seconds: Optional[int] = None
) -> Optional[str]:
    if not stored_path:
        return None
    if stored_path.startswith("http://") or stored_path.startswith("https://"):
        return stored_path
    key = normalize_object_key(stored_path)
    if not key:
        return None
    return build_signed_media_url(key, ttl_seconds=ttl_seconds)


def resolve_upload_file(object_key: str) -> tuple[Path, str]:
    """
    Resolve object_key to an absolute file path under UPLOAD_DIR.
    Raises ValueError on unsafe keys.
    """
    key = normalize_object_key(object_key)
    if not key:
        raise ValueError("unsupported media object key")

    settings = get_settings()
    upload_root = Path(settings.upload_dir).resolve()
    candidate = (upload_root / key).resolve()
    try:
        candidate.relative_to(upload_root)
    except ValueError as exc:
        raise ValueError("path escapes upload root") from exc

    return candidate, candidate.name


def guess_safe_media_type(filename: str) -> str:
    """Raster image types only — never image/svg+xml (SEC-MEDIA-005)."""
    suffix = Path(filename).suffix.lower()
    mapping = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    return mapping.get(suffix, "application/octet-stream")
