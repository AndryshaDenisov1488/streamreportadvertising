"""SEC-AUTH-004: JWT_SECRET fail-fast — no weak defaults / placeholders."""

from __future__ import annotations

import os

import pytest
from pydantic import ValidationError

from app.core.config import (
    Settings,
    get_settings,
    is_weak_jwt_placeholder,
)


@pytest.fixture(autouse=True)
def _clear_settings_cache() -> None:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


class TestWeakJwtPlaceholderHelper:
    def test_empty_is_weak(self) -> None:
        assert is_weak_jwt_placeholder("") is True
        assert is_weak_jwt_placeholder("   ") is True

    def test_change_me_class_is_weak(self) -> None:
        assert is_weak_jwt_placeholder("change-me") is True
        assert is_weak_jwt_placeholder("CHANGE-ME") is True
        assert is_weak_jwt_placeholder("change-me-in-production-use-long-random") is True
        assert is_weak_jwt_placeholder("change-me-to-a-long-random-string-in-production") is True
        assert is_weak_jwt_placeholder("change-me-anything-extra") is True

    def test_secret_is_weak(self) -> None:
        assert is_weak_jwt_placeholder("secret") is True

    def test_strong_value_is_not_weak(self) -> None:
        assert is_weak_jwt_placeholder("unit-test-only-jwt-secret-value-32chars-min") is False


class TestJwtSecretSettings:
    def test_missing_jwt_secret_fails(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("JWT_SECRET", raising=False)
        with pytest.raises(ValidationError) as exc_info:
            Settings(_env_file=None)
        assert "jwt_secret" in str(exc_info.value).lower()

    def test_empty_jwt_secret_fails(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENVIRONMENT", "production")
        with pytest.raises(ValidationError) as exc_info:
            Settings(jwt_secret="   ", _env_file=None)
        assert "JWT_SECRET" in str(exc_info.value)

    def test_change_me_placeholder_fails(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENVIRONMENT", "production")
        with pytest.raises(ValidationError) as exc_info:
            Settings(jwt_secret="change-me", _env_file=None)
        assert "placeholder" in str(exc_info.value).lower()

    def test_change_me_fails_even_in_development(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENVIRONMENT", "development")
        with pytest.raises(ValidationError) as exc_info:
            Settings(jwt_secret="change-me", _env_file=None)
        assert "placeholder" in str(exc_info.value).lower()

    def test_secret_placeholder_fails(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ENVIRONMENT", raising=False)
        monkeypatch.delenv("APP_ENV", raising=False)
        monkeypatch.delenv("SENTRY_ENVIRONMENT", raising=False)
        with pytest.raises(ValidationError) as exc_info:
            Settings(jwt_secret="secret", _env_file=None)
        assert "placeholder" in str(exc_info.value).lower()

    def test_short_secret_fails_outside_development(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ENVIRONMENT", raising=False)
        monkeypatch.delenv("APP_ENV", raising=False)
        monkeypatch.delenv("SENTRY_ENVIRONMENT", raising=False)
        with pytest.raises(ValidationError) as exc_info:
            Settings(jwt_secret="short-but-not-placeholder", _env_file=None)
        assert "32" in str(exc_info.value)

    def test_short_secret_ok_in_explicit_development(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENVIRONMENT", "development")
        settings = Settings(jwt_secret="local-dev-short-secret", _env_file=None)
        assert settings.jwt_secret == "local-dev-short-secret"

    def test_strong_secret_ok_without_development(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("ENVIRONMENT", raising=False)
        monkeypatch.delenv("APP_ENV", raising=False)
        monkeypatch.delenv("SENTRY_ENVIRONMENT", raising=False)
        secret = "production-grade-jwt-secret-value-32c"
        settings = Settings(jwt_secret=secret, _env_file=None)
        assert settings.jwt_secret == secret

    def test_no_change_me_default_in_source(self) -> None:
        import inspect

        from app.core import config as config_module

        source = inspect.getsource(config_module.Settings)
        assert 'jwt_secret: str = "change-me"' not in source
        assert 'jwt_secret: str = "secret"' not in source
