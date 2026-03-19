import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, computed_field, field_validator

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
    created_at: datetime

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def display_name(self) -> str:
        s = f"{self.last_name} {self.first_name}".strip()
        return s if s else str(self.email)


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    password: str | None = Field(
        default=None,
        max_length=128,
        description="Не указывайте — пароль сгенерируется и будет отправлен на email (при настроенном SMTP)",
    )
    role: UserRole
    is_active: bool = True

    @field_validator("password", mode="before")
    @classmethod
    def empty_password_none(cls, v: str | None) -> str | None:
        if v is None:
            return None
        s = str(v).strip()
        return s if s else None

    @field_validator("password")
    @classmethod
    def password_min_len(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if len(v) < 8:
            raise ValueError("Пароль не короче 8 символов")
        return v


class UserCreatedOut(BaseModel):
    user: UserOut
    welcome_email_sent: bool
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
