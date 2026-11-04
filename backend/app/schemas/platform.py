import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from app.models.enums import UserRole


class NotificationOut(BaseModel):
    id: uuid.UUID
    title: str
    body: str
    kind: str | None
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationListOut(BaseModel):
    items: list[NotificationOut]
    unread_count: int


class AnalyticsIn(BaseModel):
    event_name: str = Field(min_length=1, max_length=100)
    meta: dict | None = None


class InviteCreate(BaseModel):
    email: EmailStr
    role: UserRole
    full_name: str = Field(min_length=3, max_length=200)

    @field_validator("full_name")
    @classmethod
    def full_name_has_surname_and_given_name(cls, value: str) -> str:
        text = " ".join(value.split())
        parts = text.split(" ")
        if len(parts) < 2:
            raise ValueError("Укажите фамилию и имя")
        last_name = parts[0]
        first_name = " ".join(parts[1:])
        if len(last_name) > 100 or len(first_name) > 100:
            raise ValueError("ФИО слишком длинное")
        return text


class InviteCreatedOut(BaseModel):
    email: str
    role: UserRole
    full_name: str
    expires_at: datetime
    message: str


class InvitePendingOut(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    role: UserRole
    expires_at: datetime
    created_at: datetime


class InvitePreviewOut(BaseModel):
    ok: bool
    full_name: str | None = None
    email: str | None = None
    role: UserRole | None = None


class AcceptInviteIn(BaseModel):
    token: str = Field(min_length=10, max_length=128)
    password: str = Field(min_length=8, max_length=128)
    password_confirm: str = Field(min_length=8, max_length=128)

    @model_validator(mode="after")
    def passwords_match(self) -> "AcceptInviteIn":
        if self.password != self.password_confirm:
            raise ValueError("Пароли должны совпадать")
        return self


class ChecklistOut(BaseModel):
    stream_event_id: uuid.UUID
    day_index: int
    picture_exposure_ok: bool
    judges_stream_ok: bool
    splitter_socket_ok: bool
    key_stream_started_ok: bool
    kick_ok: bool
    mentions_four_ok: bool
    updated_at: datetime


class ChecklistUpdate(BaseModel):
    picture_exposure_ok: bool | None = None
    judges_stream_ok: bool | None = None
    splitter_socket_ok: bool | None = None
    key_stream_started_ok: bool | None = None
    kick_ok: bool | None = None
    mentions_four_ok: bool | None = None


class AnalyticsRow(BaseModel):
    event_name: str
    count: int


class AnalyticsSummaryOut(BaseModel):
    """Агрегаты за последние 7 дней по имени события."""

    by_event: list[AnalyticsRow]
