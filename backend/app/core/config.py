from functools import lru_cache
import os

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Known-weak placeholders — never accept these as live JWT signing secrets
_WEAK_JWT_PLACEHOLDERS = frozenset({
    "change-me",
    "changeme",
    "secret",
    "password",
    "jwt-secret",
    "jwt_secret",
    "change-me-in-production-use-long-random",
    "change-me-to-a-long-random-string-in-production",
    "your-secret-key",
    "your-secret-key-change-in-production",
})

_MIN_JWT_SECRET_LEN_NON_DEV = 32


def is_explicit_development_mode() -> bool:
    """True only when ENVIRONMENT / APP_ENV / SENTRY_ENVIRONMENT is an explicit non-prod label."""
    env = (
        os.getenv("ENVIRONMENT")
        or os.getenv("APP_ENV")
        or os.getenv("SENTRY_ENVIRONMENT")
        or ""
    ).strip().lower()
    return env in {"development", "dev", "local", "test"}


def is_weak_jwt_placeholder(secret: str) -> bool:
    normalized = secret.strip().lower()
    if not normalized:
        return True
    if normalized in _WEAK_JWT_PLACEHOLDERS:
        return True
    if normalized.startswith("change-me"):
        return True
    return False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+asyncpg://streaming:streaming@localhost:5432/streaming"
    database_url_sync: str = "postgresql://streaming:streaming@localhost:5432/streaming"

    # Required from env — no code default (SEC-AUTH-004)
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_expire_minutes: int = 30
    jwt_refresh_expire_days: int = 7

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    refresh_cookie_name: str = "refresh_token"
    refresh_cookie_secure: bool = False
    refresh_cookie_samesite: str = "lax"

    api_v1_prefix: str = "/api/v1"

    upload_dir: str = "uploads"

    app_version: str = "1.0.0"

    # Публичный URL панели (для ссылок в письмах), например https://streaming.example.ru
    app_public_base_url: str = ""

    # Срок жизни ссылки сброса пароля (минуты)
    password_reset_expire_minutes: int = 10

    sentry_dsn: str = ""
    sentry_environment: str = "development"
    sentry_traces_sample_rate: float = 0.1

    # Опционально: POST JSON при событиях эфира (начало/конец)
    external_webhook_url: str = ""

    # Дни хранения журнала аудита (0 = не удалять; фоновые задачи — вне HTTP)
    audit_retention_days: int = 0

    # SMTP для еженедельных/ежемесячных отчётов (пустой host — рассылка отключена)
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@localhost"
    smtp_use_tls: bool = True
    # True — порт 465 (implicit SSL). False — обычный SMTP + STARTTLS (например 587)
    smtp_use_ssl: bool = False

    @field_validator("jwt_secret", mode="before")
    @classmethod
    def _strip_jwt_secret(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @model_validator(mode="after")
    def _validate_jwt_secret(self) -> "Settings":
        """Fail-fast: reject empty / placeholder JWT secrets; enforce length outside development."""
        secret = self.jwt_secret
        if not secret:
            raise ValueError(
                "JWT_SECRET must be set to a non-empty value "
                "(no default is provided). Set it in the environment or .env."
            )

        # Placeholders always rejected (even in development) — finding class change-me/secret
        if is_weak_jwt_placeholder(secret):
            raise ValueError(
                "JWT_SECRET must not be a known weak placeholder "
                "(change-me, secret, …). Generate a long random value."
            )

        # Length relaxed only under explicit development|dev|local|test
        if len(secret) < _MIN_JWT_SECRET_LEN_NON_DEV and not is_explicit_development_mode():
            raise ValueError(
                f"JWT_SECRET must be at least {_MIN_JWT_SECRET_LEN_NON_DEV} characters "
                "outside development. Set ENVIRONMENT=development|test for local short secrets only."
            )

        return self

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
