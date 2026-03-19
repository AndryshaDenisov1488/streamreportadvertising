from datetime import date, datetime
from zoneinfo import ZoneInfo

from app.core.timezone import format_moscow_date, format_moscow_datetime, to_moscow


def test_format_moscow_datetime_from_utc() -> None:
    dt = datetime(2026, 3, 19, 18, 4, 28, tzinfo=ZoneInfo("UTC"))
    assert format_moscow_datetime(dt) == "19.03.2026 21:04"


def test_format_moscow_date() -> None:
    assert format_moscow_date(date(2026, 3, 7)) == "07.03.2026"


def test_to_moscow_naive_utc() -> None:
    dt = datetime(2026, 1, 1, 12, 0, 0)
    m = to_moscow(dt)
    assert m.tzinfo == ZoneInfo("Europe/Moscow")
