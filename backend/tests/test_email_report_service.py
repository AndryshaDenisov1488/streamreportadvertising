from datetime import date

from app.services.broadcast_alert_service import (
    ALERT_STEP_HOURS,
    FIRST_ALERT_HOURS,
    _highest_reached_threshold,
)
from app.services.email_report_service import event_overlaps_period


def test_event_overlaps_period_single_day_inside():
    assert event_overlaps_period(
        start_date=date(2026, 7, 10),
        duration_days=1,
        date_from=date(2026, 7, 8),
        date_to=date(2026, 7, 12),
    )


def test_event_overlaps_period_multi_day_spanning_boundary():
    assert event_overlaps_period(
        start_date=date(2026, 7, 1),
        duration_days=5,
        date_from=date(2026, 7, 4),
        date_to=date(2026, 7, 6),
    )


def test_event_overlaps_period_before_range():
    assert not event_overlaps_period(
        start_date=date(2026, 6, 1),
        duration_days=2,
        date_from=date(2026, 7, 1),
        date_to=date(2026, 7, 7),
    )


def test_event_overlaps_period_after_range():
    assert not event_overlaps_period(
        start_date=date(2026, 8, 1),
        duration_days=1,
        date_from=date(2026, 7, 1),
        date_to=date(2026, 7, 7),
    )


def test_event_overlaps_period_touching_last_day():
    assert event_overlaps_period(
        start_date=date(2026, 7, 1),
        duration_days=3,
        date_from=date(2026, 7, 3),
        date_to=date(2026, 7, 10),
    )


def test_highest_reached_threshold_steps():
    assert _highest_reached_threshold(FIRST_ALERT_HOURS - 1) == 0
    assert _highest_reached_threshold(FIRST_ALERT_HOURS) == FIRST_ALERT_HOURS
    assert _highest_reached_threshold(FIRST_ALERT_HOURS + ALERT_STEP_HOURS) == FIRST_ALERT_HOURS + ALERT_STEP_HOURS
    assert _highest_reached_threshold(FIRST_ALERT_HOURS + ALERT_STEP_HOURS - 1) == FIRST_ALERT_HOURS
