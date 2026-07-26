"""Unit tests for ffkm-admin → streaming tournament mapping helpers."""

from datetime import date

from app.services.ffkm_tournament_sync import (
    duration_from_dates,
    normalize_rank,
    should_keep_rank,
    titles_match,
)
from app.services.ffkm_stream_push import build_stream_schedule_payload, primary_stream_url


class _Day:
    def __init__(self, day_index: int, stream_url: str = ""):
        self.day_index = day_index
        self.stream_url = stream_url


class _Event:
    def __init__(self, start, days):
        self.start_date = start
        self.days = days


def test_should_keep_rank_filters_physical():
    assert should_keep_rank("official_sports_significant") is True
    assert should_keep_rank("all_russian") is True
    assert should_keep_rank("official_physical_culture") is False
    assert should_keep_rank(None) is False
    assert should_keep_rank("unknown") is False


def test_normalize_rank():
    assert normalize_rank("OFFICIAL_SPORTS_SIGNIFICANT") == "official_sports_significant"


def test_duration_from_dates_caps_at_5():
    assert duration_from_dates(date(2026, 8, 1), date(2026, 8, 1)) == 1
    assert duration_from_dates(date(2026, 8, 1), date(2026, 8, 3)) == 3
    assert duration_from_dates(date(2026, 8, 1), date(2026, 8, 10)) == 5
    assert duration_from_dates(date(2026, 8, 5), date(2026, 8, 1)) == 1


def test_titles_match_fuzzy():
    assert titles_match(
        "Физкультурное мероприятие Финал Кубка «Открываем возможности»",
        "Финал Кубка «Открываем возможности»",
    )
    assert titles_match("Турнир А", "Турнир Б") is False


def test_build_stream_schedule_and_primary():
    ev = _Event(
        date(2026, 9, 1),
        [_Day(1, ""), _Day(2, "https://vk.com/video-1_2")],
    )
    schedule = build_stream_schedule_payload(ev)  # type: ignore[arg-type]
    assert schedule[0]["stream_date"] == "2026-09-01"
    assert schedule[0]["online_stream_url"] is None
    assert schedule[1]["stream_date"] == "2026-09-02"
    assert schedule[1]["online_stream_url"] == "https://vk.com/video-1_2"
    assert primary_stream_url(ev) == "https://vk.com/video-1_2"  # type: ignore[arg-type]
