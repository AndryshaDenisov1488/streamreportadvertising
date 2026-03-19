import uuid
from datetime import date

from pydantic import BaseModel, Field


class LockAssignmentOut(BaseModel):
    stream_event_id: uuid.UUID
    title: str
    locked_by_user_id: uuid.UUID
    locked_by_email: str
    locked_by_display_name: str


class OperatorDayStatsOut(BaseModel):
    operator_id: uuid.UUID
    email: str
    display_name: str
    role: str
    broadcasts_count: int = Field(ge=0)
    mentions_count: int = Field(ge=0)


class OperatorStatsOverviewOut(BaseModel):
    stat_date: date
    assignments: list[LockAssignmentOut]
    operators: list[OperatorDayStatsOut]
    total_broadcasts_day: int
    total_mentions_day: int
