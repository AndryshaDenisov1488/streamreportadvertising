from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+asyncpg://streaming:streaming@localhost:5432/streaming"
    database_url_sync: str = "postgresql://streaming:streaming@localhost:5432/streaming"

    jwt_secret: str = "change-me"
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

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
