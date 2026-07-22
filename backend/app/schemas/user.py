import uuid
from datetime import datetime
from typing import Self

from pydantic import BaseModel, EmailStr, Field, computed_field, model_validator

from app.core.media_urls import build_signed_media_url_from_stored
from app.models.enums import UserRole


class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone: str | None = None
    telegram: str | None = None
    avatar_url: str | None = None
    role: UserRole
    is_active: bool
    suggest_password_change: bool = False
    onboarding_completed: bool = False
    last_login_at: datetime | None = None
    last_login_ip: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}

    @model_validator(mode="after")
    def _sign_avatar_url(self) -> Self:
        """Emit signed /api/v1/media/... URL for stored avatar object keys (SEC-MEDIA-004)."""
        if not self.avatar_url:
            return self
        signed = build_signed_media_url_from_stored(self.avatar_url)
        if signed:
            object.__setattr__(self, "avatar_url", signed)
        return self

    @computed_field
    @property
    def display_name(self) -> str:
        s = f"{self.last_name} {self.first_name}".strip()
        return s if s else str(self.email)


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    role: UserRole
    is_active: bool = True


class UserCreatedOut(BaseModel):
    user: UserOut
    """Письмо уходит в фоне после ответа; True если SMTP настроен и задача поставлена."""
    welcome_email_queued: bool = False
    welcome_email_skipped_reason: str | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=40)
    telegram: str | None = Field(default=None, max_length=80)
    password: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None
