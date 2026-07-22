"""SEC-MEDIA-004 / SEC-MEDIA-005: uploads auth gate + SVG rejection."""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient

from app.core.config import get_settings
from app.core.media_urls import (
    build_signed_media_url,
    build_signed_media_url_from_stored,
    create_media_signature,
    guess_safe_media_type,
    normalize_object_key,
    verify_media_signature,
)
from app.db.session import get_db
from app.main import app
from app.services.logo_service import assert_logo_upload_allowed


@pytest.fixture(autouse=True)
def _clear_settings_cache() -> None:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def upload_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "uploads"
    root.mkdir()
    monkeypatch.setenv("UPLOAD_DIR", str(root))
    get_settings.cache_clear()
    return root


async def _fake_db():
    yield MagicMock()


class TestNormalizeAndSign:
    def test_normalize_strips_uploads_prefix(self) -> None:
        lid = uuid4()
        assert normalize_object_key(f"/uploads/logos/{lid}/a.png") == f"logos/{lid}/a.png"
        assert normalize_object_key(f"avatars/{lid}.jpg") == f"avatars/{lid}.jpg"

    def test_normalize_rejects_traversal(self) -> None:
        assert normalize_object_key("logos/../avatars/x.jpg") is None
        assert normalize_object_key("documents/secret.zip") is None

    def test_signed_url_roundtrip(self) -> None:
        key = f"logos/{uuid4()}/logo.png"
        url = build_signed_media_url(key, ttl_seconds=120)
        assert "/api/v1/media/logos/" in url
        assert "sig=" in url
        assert "expires=" in url
        assert "/uploads/" not in url

        expires = int(url.split("expires=")[1].split("&")[0])
        sig = url.split("sig=")[1]
        assert verify_media_signature(key, expires, sig) is True
        assert verify_media_signature(key, expires, "deadbeef") is False
        assert verify_media_signature(key, int(time.time()) - 10, sig) is False

    def test_build_from_stored_legacy_uploads(self) -> None:
        lid = uuid4()
        url = build_signed_media_url_from_stored(f"/uploads/logos/{lid}/x.png")
        assert url is not None
        assert f"/api/v1/media/logos/{lid}/x.png" in url

    def test_guess_media_type_never_svg(self) -> None:
        assert guess_safe_media_type("x.png") == "image/png"
        assert guess_safe_media_type("evil.svg") == "application/octet-stream"
        assert guess_safe_media_type("x.svgz") == "application/octet-stream"


class TestSvgRejection:
    def test_rejects_svg_mime(self) -> None:
        with pytest.raises(HTTPException) as exc:
            assert_logo_upload_allowed(content_type="image/svg+xml", filename="logo.png")
        assert exc.value.status_code == 400
        assert "SVG" in exc.value.detail

    def test_rejects_svg_extension(self) -> None:
        with pytest.raises(HTTPException) as exc:
            assert_logo_upload_allowed(content_type="image/png", filename="logo.svg")
        assert exc.value.status_code == 400

    def test_allows_png(self) -> None:
        assert_logo_upload_allowed(content_type="image/png", filename="logo.png")

    def test_rejects_unknown_type(self) -> None:
        with pytest.raises(HTTPException) as exc:
            assert_logo_upload_allowed(content_type="application/pdf", filename="logo.pdf")
        assert exc.value.status_code == 400


@pytest.mark.anyio
async def test_legacy_uploads_path_is_not_public(upload_dir: Path) -> None:
    (upload_dir / "avatars").mkdir()
    secret = upload_dir / "avatars" / f"{uuid4()}.png"
    secret.write_bytes(b"\x89PNG\r\n\x1a\n")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get(f"/uploads/avatars/{secret.name}")
    assert r.status_code == 404


@pytest.mark.anyio
async def test_media_unauth_without_signature_denied(upload_dir: Path) -> None:
    app.dependency_overrides[get_db] = _fake_db
    lid = uuid4()
    path = upload_dir / "logos" / str(lid)
    path.mkdir(parents=True)
    (path / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get(f"/api/v1/media/logos/{lid}/logo.png")
    assert r.status_code == 401


@pytest.mark.anyio
async def test_media_signed_url_ok(upload_dir: Path) -> None:
    app.dependency_overrides[get_db] = _fake_db
    lid = uuid4()
    path = upload_dir / "logos" / str(lid)
    path.mkdir(parents=True)
    (path / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n")

    key = f"logos/{lid}/logo.png"
    expires = int(time.time()) + 600
    sig = create_media_signature(key, expires)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get(
            f"/api/v1/media/logos/{lid}/logo.png",
            params={"expires": expires, "sig": sig},
        )
    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("image/png")
    assert "svg" not in r.headers.get("content-type", "").lower()
    assert r.headers.get("x-content-type-options") == "nosniff"


@pytest.mark.anyio
async def test_media_expired_signature_denied(upload_dir: Path) -> None:
    app.dependency_overrides[get_db] = _fake_db
    lid = uuid4()
    path = upload_dir / "logos" / str(lid)
    path.mkdir(parents=True)
    (path / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n")

    key = f"logos/{lid}/logo.png"
    expires = int(time.time()) - 30
    sig = create_media_signature(key, expires)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get(
            f"/api/v1/media/logos/{lid}/logo.png",
            params={"expires": expires, "sig": sig},
        )
    assert r.status_code == 401


@pytest.mark.anyio
async def test_legacy_svg_on_disk_not_served(upload_dir: Path) -> None:
    app.dependency_overrides[get_db] = _fake_db
    lid = uuid4()
    path = upload_dir / "logos" / str(lid)
    path.mkdir(parents=True)
    (path / "xss.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>')

    key = f"logos/{lid}/xss.svg"
    expires = int(time.time()) + 600
    sig = create_media_signature(key, expires)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get(
            f"/api/v1/media/logos/{lid}/xss.svg",
            params={"expires": expires, "sig": sig},
        )
    assert r.status_code == 404
