import uuid
from datetime import date, datetime

from pydantic import BaseModel


class ReportMentionRow(BaseModel):
    mention_id: uuid.UUID
    stream_event_id: uuid.UUID
    stream_title: str
    event_day_date: date
    day_index: int
    broadcast_session_id: uuid.UUID
    original_timecode: str
    adjusted_timecode: str
    absolute_moscow_adjusted: str
    is_adjusted: bool
    mention_created_at: datetime


class ReportMentionsOut(BaseModel):
    items: list[ReportMentionRow]
    total: int
