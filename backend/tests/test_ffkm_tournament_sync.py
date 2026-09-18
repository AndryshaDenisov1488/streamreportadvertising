"""Unit tests for FFKM → streaming tournament synchronization."""

from datetime import date
import uuid

import pytest

from app.models.stream import StreamDay, StreamEvent

from app.services.ffkm_tournament_sync import (
    LOCK_FFKM_SYNC,
    SyncStats,
    duration_from_dates,
    ensure_ffkm_link_for_stream,
    ensure_ffkm_link_for_stream_locked,
    link_manual_stream_events,
    normalize_rank,
    should_keep_rank,
    sync_tournaments_from_ffkm_admin,
    run_ffkm_sync_locked,
    titles_match,
)
from app.services.ffkm_stream_push import (
    build_stream_schedule_payload,
    primary_stream_url,
    public_online_stream_url,
)


class _Day:
    def __init__(self, day_index: int, stream_url: str = "", stream_key: str = ""):
        self.day_index = day_index
        self.stream_url = stream_url
        self.stream_key = stream_key


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
    assert schedule[0]["day_index"] == 1
    assert schedule[0]["title"] == "День 1"
    assert schedule[0]["online_stream_url"] is None
    assert schedule[1]["stream_date"] == "2026-09-02"
    assert schedule[1]["day_index"] == 2
    assert schedule[1]["title"] == "День 2"
    assert schedule[1]["stream_date_ru"] == "02.09.2026"
    assert schedule[1]["online_stream_url"] == "https://vk.com/video-1_2"
    assert primary_stream_url(ev) == "https://vk.com/video-1_2"  # type: ignore[arg-type]


def test_public_online_stream_url_prefers_today_then_last_filled():
    ev = _Event(
        date(2026, 8, 24),
        [_Day(1, "https://vk.com/d1"), _Day(2, "https://vk.com/d2"), _Day(3, "")],
    )
    assert public_online_stream_url(ev, today=date(2026, 8, 24)) == "https://vk.com/d1"  # type: ignore[arg-type]
    assert public_online_stream_url(ev, today=date(2026, 8, 25)) == "https://vk.com/d2"  # type: ignore[arg-type]
    assert public_online_stream_url(ev, today=date(2026, 8, 26)) == "https://vk.com/d2"  # type: ignore[arg-type]
    assert primary_stream_url(ev) == "https://vk.com/d1"  # type: ignore[arg-type]


def test_stream_key_is_never_published_as_public_url():
    ev = _Event(
        date(2026, 8, 24),
        [
            _Day(1, "https://vkvideo.ru/live-1"),
            _Day(2, "1125900042558359_key", "https://vkvideo.ru/private-ingest"),
        ],
    )
    schedule = build_stream_schedule_payload(ev)  # type: ignore[arg-type]
    assert schedule[1]["online_stream_url"] is None
    assert public_online_stream_url(ev, today=date(2026, 8, 25)) == "https://vkvideo.ru/live-1"  # type: ignore[arg-type]


class _ScalarResult:
    def __init__(self, rows):
        self.rows = list(rows)

    def scalars(self):
        return self

    def all(self):
        return list(self.rows)

    def scalar_one_or_none(self):
        return self.rows[0] if self.rows else None

    def __iter__(self):
        return iter(self.rows)


class _SyncSession:
    """Small in-memory AsyncSession stand-in for sync idempotency regression."""

    def __init__(self):
        self.events: list[StreamEvent] = []
        self.commit_count = 0

    async def execute(self, statement):
        sql = str(statement)
        if "FROM stream_days" in sql:
            return _ScalarResult([day for event in self.events for day in event.days])
        if sql.startswith("SELECT stream_events.ffkm_admin_tournament_id"):
            return _ScalarResult(
                [
                    event.ffkm_admin_tournament_id
                    for event in self.events
                    if event.ffkm_admin_tournament_id is not None
                ]
            )
        if "ffkm_admin_tournament_id IS NULL" in sql:
            return _ScalarResult(
                [event for event in self.events if event.ffkm_admin_tournament_id is None]
            )
        if "ffkm_admin_tournament_id IS NOT NULL" in sql:
            return _ScalarResult(
                [event for event in self.events if event.ffkm_admin_tournament_id is not None]
            )
        if "ffkm_admin_tournament_id =" in sql:
            return _ScalarResult(self.events)
        if "WHERE stream_events.id =" in sql:
            return _ScalarResult(self.events)
        raise AssertionError(f"Unexpected statement: {sql}")

    def add(self, value):
        if isinstance(value, StreamEvent):
            if value.id is None:
                value.id = uuid.uuid4()
            self.events.append(value)
            return
        if isinstance(value, StreamDay):
            event = next(event for event in self.events if event.id == value.stream_event_id)
            event.days.append(value)
            return
        raise AssertionError(f"Unexpected model: {type(value)}")

    async def flush(self):
        return None

    async def commit(self):
        self.commit_count += 1

    async def rollback(self):
        return None


class _FfkmClient:
    async def iter_all_tournaments(self):
        return [
            {
                "id": 2026091901,
                "title": "Памяти Олимпийского чемпиона С. Гринькова",
                "start_date": "2026-09-19",
                "end_date": "2026-09-20",
                "rank": "all_russian",
            },
            {
                "id": 2026091902,
                "title": "Физкультурное мероприятие",
                "start_date": "2026-09-19",
                "end_date": "2026-09-20",
                "rank": "official_physical_culture",
            },
        ]


@pytest.mark.asyncio
async def test_grinkov_all_russian_two_day_sync_is_idempotent(monkeypatch):
    monkeypatch.setenv("FFKM_ADMIN_SYNC_FROM_DATE", "2026-07-01")
    session = _SyncSession()
    client = _FfkmClient()

    first = await sync_tournaments_from_ffkm_admin(session, client=client)  # type: ignore[arg-type]
    second = await sync_tournaments_from_ffkm_admin(session, client=client)  # type: ignore[arg-type]

    assert first.created == 1
    assert first.skipped_physical == 1
    assert second.created == 0
    assert second.updated == 0
    assert second.skipped_physical == 1
    assert len(session.events) == 1
    event = session.events[0]
    assert event.title == "Памяти Олимпийского чемпиона С. Гринькова"
    assert event.start_date == date(2026, 9, 19)
    assert event.duration_days == 2
    assert event.ffkm_admin_rank == "all_russian"
    assert [day.day_index for day in event.days] == [1, 2]


@pytest.mark.asyncio
async def test_sync_prefers_matching_manual_event_before_unique_upsert():
    session = _SyncSession()
    manual = StreamEvent(
        id=uuid.uuid4(),
        title="Памяти Олимпийского чемпиона С. Гринькова",
        start_date=date(2026, 9, 19),
        duration_days=1,
        ffkm_admin_tournament_id=None,
        ffkm_admin_rank=None,
        created_by_id=None,
    )
    manual.days = []
    session.events.append(manual)

    stats = await sync_tournaments_from_ffkm_admin(
        session, client=_FfkmClient()  # type: ignore[arg-type]
    )

    assert stats.linked_manual == 1
    assert stats.created == 0
    assert len(session.events) == 1
    assert session.events[0] is manual
    assert manual.ffkm_admin_tournament_id == 2026091901
    assert manual.duration_days == 2


@pytest.mark.asyncio
async def test_manual_and_on_save_linking_reject_physical_and_old_tournaments():
    session = _SyncSession()
    manual = StreamEvent(
        id=uuid.uuid4(),
        title="Физкультурное мероприятие",
        start_date=date(2026, 9, 19),
        duration_days=2,
        ffkm_admin_tournament_id=None,
        ffkm_admin_rank=None,
        created_by_id=None,
    )
    manual.days = []
    session.events.append(manual)
    physical_items = [
        {
            "id": 55,
            "title": manual.title,
            "start_date": "2026-09-19",
            "end_date": "2026-09-20",
            "rank": "official_physical_culture",
        },
        {
            "id": 56,
            "title": manual.title,
            "start_date": "2026-01-01",
            "end_date": "2026-01-02",
            "rank": "all_russian",
        },
    ]

    assert (
        await link_manual_stream_events(
            session, physical_items, from_date=date(2026, 7, 1)  # type: ignore[arg-type]
        )
        == 0
    )

    class _RejectedClient:
        async def iter_all_tournaments(self):
            return physical_items

    assert (
        await ensure_ffkm_link_for_stream(
            session, manual.id, client=_RejectedClient()  # type: ignore[arg-type]
        )
        is False
    )
    assert manual.ffkm_admin_tournament_id is None


@pytest.mark.asyncio
async def test_public_sync_wrapper_uses_shared_advisory_lock(monkeypatch):
    seen: list[int] = []
    expected = SyncStats(fetched=1)

    async def _locked(lock_key, callback):
        seen.append(lock_key)
        assert callable(callback)
        return expected

    monkeypatch.setattr(
        "app.services.ffkm_tournament_sync.run_if_leader", _locked
    )
    result = await run_ffkm_sync_locked(client=_FfkmClient())  # type: ignore[arg-type]

    assert result is expected
    assert seen == [LOCK_FFKM_SYNC]


@pytest.mark.asyncio
async def test_on_save_lock_is_held_through_commit(monkeypatch):
    order: list[str] = []

    class _CommitSession:
        async def commit(self):
            order.append("commit")

        async def rollback(self):
            order.append("rollback")

    async def _ensure(session, stream_id, client=None):
        order.append("assign")
        return True

    async def _lock(lock_key, callback):
        assert lock_key == LOCK_FFKM_SYNC
        order.append("lock-acquired")
        result = await callback()
        order.append("lock-released")
        return result

    monkeypatch.setattr(
        "app.services.ffkm_tournament_sync.ensure_ffkm_link_for_stream", _ensure
    )
    monkeypatch.setattr(
        "app.services.ffkm_tournament_sync.run_if_leader", _lock
    )

    assert (
        await ensure_ffkm_link_for_stream_locked(
            _CommitSession(), uuid.uuid4()  # type: ignore[arg-type]
        )
        is True
    )
    assert order == ["lock-acquired", "assign", "commit", "lock-released"]


@pytest.mark.asyncio
async def test_on_save_link_skips_tournament_id_occupied_by_other_event():
    current = StreamEvent(
        id=uuid.uuid4(),
        title="Памяти Олимпийского чемпиона С. Гринькова",
        start_date=date(2026, 9, 19),
        duration_days=2,
        ffkm_admin_tournament_id=None,
        ffkm_admin_rank=None,
        created_by_id=None,
    )
    occupied_id = uuid.uuid4()

    class _OccupiedSession:
        def __init__(self):
            self.calls = 0

        async def execute(self, statement):
            self.calls += 1
            return _ScalarResult([current] if self.calls == 1 else [occupied_id])

        async def flush(self):
            raise AssertionError("occupied link must not flush")

    assert (
        await ensure_ffkm_link_for_stream(
            _OccupiedSession(), current.id, client=_FfkmClient()  # type: ignore[arg-type]
        )
        is False
    )
    assert current.ffkm_admin_tournament_id is None
