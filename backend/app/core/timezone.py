from datetime import datetime
from zoneinfo import ZoneInfo

MOSCOW_TZ = ZoneInfo("Europe/Moscow")


def now_moscow() -> datetime:
    return datetime.now(MOSCOW_TZ)


def utc_now() -> datetime:
    return datetime.now(ZoneInfo("UTC"))


def to_moscow(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(MOSCOW_TZ)


def format_moscow_iso(dt: datetime) -> str:
    return to_moscow(dt).isoformat()


def add_seconds_to_start(started_at: datetime, offset_sec: int) -> datetime:
    from datetime import timedelta

    base = started_at if started_at.tzinfo else started_at.replace(tzinfo=ZoneInfo("UTC"))
    return base + timedelta(seconds=offset_sec)
