"""SEC-WH-004: outbound webhook HMAC signature presence and correctness."""

from __future__ import annotations

import hashlib
import hmac
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_settings
from app.utils.webhook import (
    WEBHOOK_SIGNATURE_HEADER,
    build_webhook_body,
    post_external_webhook,
    sign_webhook_body,
)

_STRONG_JWT = "unit-test-only-jwt-secret-value-32chars-min"
_WEBHOOK_SECRET = "unit-test-webhook-signing-secret-32c"


@pytest.fixture(autouse=True)
def _clear_settings_cache() -> None:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


class TestSignWebhookBody:
    def test_format_is_sha256_hex(self) -> None:
        body = b'{"type":"broadcast_started","payload":{}}'
        sig = sign_webhook_body(body, _WEBHOOK_SECRET)
        assert sig.startswith("sha256=")
        digest = sig.removeprefix("sha256=")
        assert len(digest) == 64
        assert all(c in "0123456789abcdef" for c in digest)

    def test_matches_stdlib_hmac(self) -> None:
        body = build_webhook_body("broadcast_stopped", {"day_index": 1})
        expected = "sha256=" + hmac.new(
            _WEBHOOK_SECRET.encode("utf-8"),
            body,
            hashlib.sha256,
        ).hexdigest()
        assert sign_webhook_body(body, _WEBHOOK_SECRET) == expected

    def test_different_secret_different_signature(self) -> None:
        body = b'{"type":"x","payload":{}}'
        a = sign_webhook_body(body, "secret-a-long-enough-for-tests-xx")
        b = sign_webhook_body(body, "secret-b-long-enough-for-tests-yy")
        assert a != b


class TestWebhookSecretSettings:
    def test_url_without_secret_fails(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENVIRONMENT", "test")
        with pytest.raises(ValidationError) as exc_info:
            Settings(
                jwt_secret=_STRONG_JWT,
                external_webhook_url="https://hooks.example.com/stream",
                external_webhook_secret="",
                _env_file=None,
            )
        assert "EXTERNAL_WEBHOOK_SECRET" in str(exc_info.value)

    def test_url_with_secret_ok(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENVIRONMENT", "test")
        settings = Settings(
            jwt_secret=_STRONG_JWT,
            external_webhook_url="https://hooks.example.com/stream",
            external_webhook_secret=_WEBHOOK_SECRET,
            _env_file=None,
        )
        assert settings.external_webhook_url.endswith("/stream")
        assert settings.external_webhook_secret == _WEBHOOK_SECRET

    def test_empty_url_without_secret_ok(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENVIRONMENT", "test")
        settings = Settings(
            jwt_secret=_STRONG_JWT,
            external_webhook_url="",
            external_webhook_secret="",
            _env_file=None,
        )
        assert settings.external_webhook_url == ""


class TestPostExternalWebhook:
    @pytest.mark.asyncio
    async def test_no_url_skips_post(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENVIRONMENT", "test")
        monkeypatch.setenv("JWT_SECRET", _STRONG_JWT)
        monkeypatch.delenv("EXTERNAL_WEBHOOK_URL", raising=False)
        monkeypatch.delenv("EXTERNAL_WEBHOOK_SECRET", raising=False)
        get_settings.cache_clear()

        with patch("app.utils.webhook.httpx.AsyncClient") as client_cls:
            await post_external_webhook("broadcast_started", {"day_index": 0})
            client_cls.assert_not_called()

    @pytest.mark.asyncio
    async def test_posts_signed_body(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENVIRONMENT", "test")
        monkeypatch.setenv("JWT_SECRET", _STRONG_JWT)
        monkeypatch.setenv("EXTERNAL_WEBHOOK_URL", "https://hooks.example.com/stream")
        monkeypatch.setenv("EXTERNAL_WEBHOOK_SECRET", _WEBHOOK_SECRET)
        get_settings.cache_clear()

        payload = {"stream_event_id": "abc", "day_index": 2}
        expected_body = build_webhook_body("broadcast_started", payload)
        expected_sig = sign_webhook_body(expected_body, _WEBHOOK_SECRET)

        mock_response = MagicMock()
        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)

        with patch("app.utils.webhook.httpx.AsyncClient", return_value=mock_client):
            await post_external_webhook("broadcast_started", payload)

        mock_client.post.assert_awaited_once()
        _args, kwargs = mock_client.post.await_args
        assert _args[0] == "https://hooks.example.com/stream"
        assert kwargs["content"] == expected_body
        headers = kwargs["headers"]
        assert headers[WEBHOOK_SIGNATURE_HEADER] == expected_sig
        assert WEBHOOK_SIGNATURE_HEADER in headers
        assert headers["Content-Type"].startswith("application/json")

    @pytest.mark.asyncio
    async def test_missing_secret_at_runtime_skips_unsigned(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Defense in depth if settings somehow bypass boot validation."""
        monkeypatch.setenv("ENVIRONMENT", "test")
        monkeypatch.setenv("JWT_SECRET", _STRONG_JWT)
        monkeypatch.delenv("EXTERNAL_WEBHOOK_URL", raising=False)
        monkeypatch.delenv("EXTERNAL_WEBHOOK_SECRET", raising=False)
        get_settings.cache_clear()

        settings = get_settings()
        object.__setattr__(settings, "external_webhook_url", "https://hooks.example.com/stream")
        object.__setattr__(settings, "external_webhook_secret", "")

        with patch("app.utils.webhook.httpx.AsyncClient") as client_cls:
            await post_external_webhook("broadcast_stopped", {"day_index": 1})
            client_cls.assert_not_called()
