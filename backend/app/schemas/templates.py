import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field

from app.schemas.stream import StreamDayIn


class StreamEventTemplateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=500)
    duration_days: int = Field(ge=1, le=5)
    days: list[StreamDayIn] | None = None


class StreamEventTemplateOut(BaseModel):
    id: uuid.UUID
    name: str
    title: str
    duration_days: int
    created_at: datetime

    model_config = {"from_attributes": True}


class InstantiateTemplateBody(BaseModel):
    start_date: date


class TemplateFromEventBody(BaseModel):
    name: str = Field(min_length=1, max_length=200)
