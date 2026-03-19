import uuid
from datetime import date

from pydantic import BaseModel, Field


class LockAssignmentOut(BaseModel):
    stream_event_id: uuid.UUID
    title: str
    summary: str


class OperatorDayStatsOut(BaseModel):
    operator_id: uuid.UUID
    email: str
    display_name: str
    role: str
    broadcasts_week: int = Field(ge=0)
    mentions_week: int = Field(ge=0)
    mentions_norm_week: int = Field(ge=0, description="Ожидаемо упоминаний: 4 на каждый эфир")
    mentions_met_week: bool
    broadcasts_month: int = Field(ge=0)
    mentions_month: int = Field(ge=0)
    mentions_norm_month: int = Field(ge=0)
    mentions_met_month: bool


class OperatorStatsOverviewOut(BaseModel):
    stat_date: date
    week_start: date
    week_end: date
    month_start: date
    month_end: date
    assignments: list[LockAssignmentOut]
    operators: list[OperatorDayStatsOut]
    total_broadcasts_week: int
    total_mentions_week: int
    total_broadcasts_month: int
    total_mentions_month: int
