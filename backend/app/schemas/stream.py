import uuid
from datetime import date, datetime

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator

from app.core.timezone import MOSCOW_TZ
from app.schemas.logo import StreamLogoItemOut

class StreamDayIn(BaseModel):
    day_index: int = Field(ge=1, le=5)
    stream_url: str = ""
    server_url: str = ""
    stream_key: str = ""


class StreamDayOut(BaseModel):
    id: uuid.UUID
    day_index: int
    stream_url: str
    server_url: str
    stream_key: str

    model_config = {"from_attributes": True}


class StreamEventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    start_date: date
    duration_days: int = Field(ge=1, le=5)
    days: list[StreamDayIn] | None = None
    """Если задан template_id — из шаблона берётся только URL сервера во все дни; поле days игнорируется."""
    template_id: uuid.UUID | None = None


class StreamLockBody(BaseModel):
    assign_user_id: uuid.UUID | None = Field(default=None, description="Для SUPERADMIN: на кого повесить дни")
    day_indices: list[int] | None = Field(
        default=None,
        description="Если null или пусто — все дни 1..N; иначе только перечисленные дни",
    )


class BroadcastActualStartBody(BaseModel):
    """Фактическое время начала эфира (когда картинка реально пошла). Без таймзоны — интерпретируется как МСК."""

    actual_started_at: datetime

    @field_validator("actual_started_at", mode="after")
    @classmethod
    def naive_as_moscow(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=MOSCOW_TZ)
        return v


class DayAssignmentOut(BaseModel):
    day_index: int
    operator_id: uuid.UUID
    operator_display_name: str
    operator_email: str = ""

    model_config = {"from_attributes": False}


class StreamEventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    start_date: date | None = None
    duration_days: int | None = Field(default=None, ge=1, le=5)
    days: list[StreamDayIn] | None = None
    content_url: AnyHttpUrl | None = None

    @field_validator("content_url", mode="before")
    @classmethod
    def empty_content_url_to_none(cls, v: object) -> object:
        if v == "":
            return None
        return v


class StreamDayLinkOut(BaseModel):
    """День мероприятия и ссылка на трансляцию (для списка без захода в карточку)."""

    day_index: int
    stream_url: str


class StreamEventListOut(BaseModel):
    id: uuid.UUID
    title: str
    start_date: date
    duration_days: int
    locked_by_user_id: uuid.UUID | None
    locked_by_display_name: str | None = None
    """Устар.: один «кто в работе»; при нескольких операторах смотрите assignment_summary."""
    assignment_summary: str | None = None
    """Кратко: кто какие дни ведёт."""
    has_slot_for_me: bool = True
    """Для текущего пользователя: есть ли свободные дни или уже свои назначения."""
    has_active_broadcast: bool
    has_ended_broadcast: bool = False
    ended_day_indices: list[int] = []
    created_at: datetime
    day_stream_links: list[StreamDayLinkOut] = []
    """По дням: ссылки на трансляцию (копирование из списка)."""

    model_config = {"from_attributes": True}


class BroadcastSessionOut(BaseModel):
    id: uuid.UUID
    stream_event_id: uuid.UUID
    day_index: int
    operator_id: uuid.UUID
    started_at: datetime
    ended_at: datetime | None
    is_active: bool
    """Число упоминаний (только в деталке мероприятия для завершённых сессий)."""
    mentions_count: int | None = None

    model_config = {"from_attributes": True}


class StreamEventDetailOut(BaseModel):
    id: uuid.UUID
    title: str
    start_date: date
    duration_days: int
    locked_by_user_id: uuid.UUID | None
    locked_by_display_name: str | None = None
    day_assignments: list[DayAssignmentOut] = []
    """Назначения операторов по дням."""
    days: list[StreamDayOut]
    active_broadcasts: list[BroadcastSessionOut]
    ended_broadcasts: list[BroadcastSessionOut] = []
    """Завершённые эфиры (для сдвига фактического старта менеджером)."""
    broadcast_restart_blocked_days: list[int] = []
    """Дни, где после завершённого эфира >1 ч с таймкодами повторный «Начать эфир» недоступен."""
    content_url: str | None = None
    """Ссылка на материалы (например Яндекс.Диск)."""
    logos: list[StreamLogoItemOut] = []
    created_at: datetime
    updated_at: datetime


class SponsorMentionCreate(BaseModel):
    pass


class SponsorMentionUpdate(BaseModel):
    adjusted_offset_sec: int = Field(ge=0)


class MentionAdjustmentOut(BaseModel):
    id: uuid.UUID
    editor_user_id: uuid.UUID
    previous_adjusted_sec: int
    new_adjusted_sec: int
    created_at: datetime

    model_config = {"from_attributes": True}


class SponsorMentionOut(BaseModel):
    id: uuid.UUID
    broadcast_session_id: uuid.UUID
    original_offset_sec: int
    adjusted_offset_sec: int
    original_timecode: str
    adjusted_timecode: str
    absolute_moscow_original: str
    absolute_moscow_adjusted: str
    is_adjusted: bool
    created_at: datetime
    adjustments: list[MentionAdjustmentOut]

    model_config = {"from_attributes": True}
