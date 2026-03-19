import uuid
from datetime import datetime

from pydantic import BaseModel, Field

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
    email: str = Field(min_length=3, max_length=320)
    role: UserRole


class InviteCreatedOut(BaseModel):
    token: str
    invite_url_hint: str


class AcceptInviteIn(BaseModel):
    token: str = Field(min_length=10, max_length=64)
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)


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
