import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class StreamLogoItemOut(BaseModel):
    id: uuid.UUID
    filename_original: str
    public_url: str
    sort_order: int
    created_at: datetime


class LogoLibraryItemOut(BaseModel):
    id: uuid.UUID
    filename_original: str
    public_url: str
    created_at: datetime
    uploaded_by_id: uuid.UUID | None


class LogoAttachBody(BaseModel):
    logo_id: uuid.UUID = Field(description="Идентификатор файла из медиатеки")
