from datetime import date, datetime
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


def format_moscow_datetime(dt: datetime) -> str:
    """Отображение даты и времени в часовом поясе МСК: dd.mm.yyyy HH:mm (24ч)."""
    return to_moscow(dt).strftime("%d.%m.%Y %H:%M")


def format_moscow_date(d: date) -> str:
    """Только дата в МСК-смысле (календарная дата события): dd.mm.yyyy."""
    return d.strftime("%d.%m.%Y")


def add_seconds_to_start(started_at: datetime, offset_sec: int) -> datetime:
    from datetime import timedelta

    base = started_at if started_at.tzinfo else started_at.replace(tzinfo=ZoneInfo("UTC"))
    return base + timedelta(seconds=offset_sec)
