import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.audit import AuditLogOut


class ProfileUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=40)
    telegram: str | None = Field(default=None, max_length=80)
    onboarding_completed: bool | None = None
    # только false: отклонить экран смены пароля при первом входе (без смены пароля)
    suggest_password_change: bool | None = None


class ChangePasswordIn(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class SessionOut(BaseModel):
    id: uuid.UUID
    created_at: datetime
    expires_at: datetime
    user_agent: str | None
    is_current: bool

    model_config = {"from_attributes": True}


class MyActivityPage(BaseModel):
    items: list[AuditLogOut]
    total: int
    page: int
    page_size: int


class DashboardSummaryOut(BaseModel):
    role: str
    title: str
    cards: list[dict]
