"""Синтетические регрессионные тесты recovery-links-20261113."""

from __future__ import annotations

import sys
import uuid
from datetime import date

import pytest

from app.services.recovery_links_20261113 import (
    CUTOFF_DATE,
    MIGRATION_VERSION,
    AmbiguousMatchError,
    DateMappingConflictError,
    IdCollisionError,
    RecoveryPlan,
    TournamentIdConflictError,
    build_recovery_plan,
    business_date,
    day_index_for_business_date,
    deterministic_day_id,
)
from scripts.recovery_links_20261113 import (
    adapt,
    assert_postapply_invariant,
    check_columns,
    plan_sha256,
    sync_url,
)
from scripts.recovery_links_20261113 import main as cli_main


def _user(user_id: str, email: str) -> dict:
    return {"id": user_id, "email": email}


def _event(
    event_id: str,
    *,
    title: str = "Турнир",
    start: str = "2026-10-20",
    duration: int = 1,
    tournament_id: int | None = None,
    content_url: str | None = None,
    created_by_id: str | None = None,
) -> dict:
    return {
        "id": event_id,
        "title": title,
        "start_date": start,
        "duration_days": duration,
        "ffkm_admin_tournament_id": tournament_id,
        "content_url": content_url,
        "created_by_id": created_by_id,
    }


def _day(day_id: str, event_id: str, day_index: int, stream_url: str = "", server_url: str = "", stream_key: str = "") -> dict:
    return {
        "id": day_id,
        "stream_event_id": event_id,
        "day_index": day_index,
        "stream_url": stream_url,
        "server_url": server_url,
        "stream_key": stream_key,
    }


def _plan(**overrides):
    base = {
        "current_users": [],
        "legacy_users": [],
        "current_events": [],
        "legacy_events": [],
        "current_days": [],
        "legacy_days": [],
    }
    base.update(overrides)
    return build_recovery_plan(**base)


def test_cutoff_and_multiday_only_historical_days_qualify() -> None:
    plan = _plan(
        current_events=[_event("live", start="2026-10-25", duration=5)],
        legacy_events=[_event("old", start="2026-10-25", duration=5)],
        current_days=[_day("d1", "live", 1), _day("d2", "live", 2), _day("d5", "live", 5)],
        legacy_days=[
            _day("o1", "old", 1, stream_url="https://old/1"),
            _day("o2", "old", 2, stream_url="https://old/2"),
            _day("o4", "old", 4, stream_url=""),
            _day("o5", "old", 5, stream_url="https://old/5"),
            _day("o6", "old", 6, stream_url=""),
            _day("o7", "old", 7, stream_url=""),
            _day("o8", "old", 8, stream_url="https://old/8"),
        ],
    )
    # day 1,2,5 до cutoff (2026-10-25, 2026-10-26, 2026-10-29) — обновляются;
    # day 4,6,7 с пустым stream_url и day 8 (2026-11-01 = cutoff) — пропускаются.
    assert plan.day_updates == [
        {"id": "d1", "stream_url": "https://old/1"},
        {"id": "d2", "stream_url": "https://old/2"},
        {"id": "d5", "stream_url": "https://old/5"},
    ]
    assert plan.day_inserts == []
    assert plan.skipped_days == 4


def test_missing_historical_day_outside_current_duration_is_conflict() -> None:
    with pytest.raises(DateMappingConflictError):
        _plan(
            current_events=[_event("live", start="2026-10-25", duration=2)],
            legacy_events=[_event("old", start="2026-10-25", duration=5)],
            current_days=[_day("d1", "live", 1), _day("d2", "live", 2)],
            legacy_days=[_day("o3", "old", 3, stream_url="https://old/3")],
        )


def test_day_mapped_by_business_date_not_source_day_index() -> None:
    # Регрессия: legacy start позже current start при том же tournament_id.
    # day_index источника нельзя переиспользовать — URL должен лечь на день
    # с той же фактической бизнес-датой (2026-10-26), а не на day_index 1.
    plan = _plan(
        current_events=[_event("live", start="2026-10-25", duration=5, tournament_id=7)],
        legacy_events=[_event("old", start="2026-10-26", duration=4, tournament_id=7)],
        current_days=[_day("d1", "live", 1), _day("d2", "live", 2)],
        legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
    )
    assert plan.day_updates == [{"id": "d2", "stream_url": "https://old/1"}]
    assert plan.day_inserts == []


def test_date_incompatible_tournament_match_is_rejected_not_silently_shifted() -> None:
    # Регрессия (correction 3): одинаковый tournament_id, но дата начала
    # источника вне окна текущего события. Раньше планировщик вставлял новое
    # событие, СОХРАНЯЯ tournament_id — на apply это падало бы на unique
    # constraint (models/stream.py) и откатывало всю миграцию. Теперь это
    # конфликт идентичности: исключение до любой записи (сухой прогон тоже).
    with pytest.raises(TournamentIdConflictError):
        _plan(
            current_events=[_event("live", start="2026-10-25", duration=1, tournament_id=7)],
            legacy_events=[_event("old", start="2026-10-26", duration=1, tournament_id=7)],
            current_days=[_day("d1", "live", 1)],
            legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
        )
    # Даже при частичном пересечении окон: дата начала источника 2026-10-27
    # вне окна текущего события 10-25..10-26 — матча по tournament_id нет,
    # а вставка с занятым tournament_id — конфликт идентичности, не событие.
    with pytest.raises(TournamentIdConflictError):
        _plan(
            current_events=[_event("live", start="2026-10-25", duration=2, tournament_id=7)],
            legacy_events=[_event("old", start="2026-10-27", duration=2, tournament_id=7)],
            current_days=[_day("d1", "live", 1), _day("d2", "live", 2)],
            legacy_days=[_day("o2", "old", 2, stream_url="https://old/2")],
        )


def test_new_event_without_tournament_id_still_inserted_when_dates_incompatible() -> None:
    # Конфликт идентичности касается только занятого ffkm_admin_tournament_id:
    # без него несовместимые по датам события по-прежнему вставляются отдельно.
    plan = _plan(
        current_events=[_event("live", start="2026-10-25", duration=1)],
        legacy_events=[_event("old", start="2026-10-26", duration=1)],
        current_days=[_day("d1", "live", 1)],
        legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
    )
    assert plan.day_updates == []
    assert len(plan.event_inserts) == 1
    assert plan.event_inserts[0]["id"] == "old"
    assert plan.event_inserts[0]["ffkm_admin_tournament_id"] is None


def test_matched_event_day_outside_current_duration_is_conflict() -> None:
    # Регрессия DateMappingConflictError для реально совпавших событий (по
    # сигнатуре title+start_date без tournament_id): бизнес-дата дня
    # источника не помещается в текущую длительность — явный конфликт.
    with pytest.raises(DateMappingConflictError):
        _plan(
            current_events=[_event("live", start="2026-10-25", duration=2)],
            legacy_events=[_event("old", start="2026-10-25", duration=5)],
            current_days=[_day("d1", "live", 1), _day("d2", "live", 2)],
            legacy_days=[_day("o3", "old", 3, stream_url="https://old/3")],
        )
    # Тот же конфликт на матче по tournament_id: дата начала источника
    # совместима (внутри окна), но день выходит за текущую длительность.
    with pytest.raises(DateMappingConflictError):
        _plan(
            current_events=[_event("live", start="2026-10-26", duration=2, tournament_id=7)],
            legacy_events=[_event("old", start="2026-10-26", duration=3, tournament_id=7)],
            current_days=[_day("d1", "live", 1), _day("d2", "live", 2)],
            legacy_days=[_day("o3", "old", 3, stream_url="https://old/3")],
        )


def test_renamed_event_matches_by_tournament_id_and_compatible_dates() -> None:
    # Регрессия (correction 2): переименованное событие с тем же verified
    # tournament ID и совместимой датой начала (внутри окна текущего события)
    # обязано матчиться — title не обязан совпадать.
    plan = _plan(
        current_events=[_event("live", title="Новое название", start="2026-10-25", duration=5, tournament_id=7)],
        legacy_events=[_event("old", title="Старое название", start="2026-10-26", duration=2, tournament_id=7)],
        current_days=[_day("d1", "live", 1), _day("d2", "live", 2)],
        legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
    )
    assert plan.event_inserts == []
    # бизнес-дата дня источника 2026-10-26 → day 2 текущего события
    assert plan.day_updates == [{"id": "d2", "stream_url": "https://old/1"}]


def test_remap_users_no_inserts_and_unmatched_becomes_none() -> None:
    plan = _plan(
        current_users=[_user("new-op", "Op@Example.com")],
        legacy_users=[_user("old-op", "op@example.com"), _user("ghost", "ghost@example.com")],
        current_events=[],
        legacy_events=[
            _event("old-1", start="2026-10-20", created_by_id="old-op"),
            _event("old-2", start="2026-10-21", created_by_id="ghost"),
            _event("old-3", start="2026-10-22", created_by_id=None),
        ],
        legacy_days=[
            _day("d1", "old-1", 1, stream_url="https://a"),
            _day("d2", "old-2", 1, stream_url="https://b"),
            _day("d3", "old-3", 1, stream_url="https://c"),
        ],
    )
    assert plan.user_remap == {"old-op": "new-op"}
    creators = {row["id"]: row["created_by_id"] for row in plan.event_inserts}
    assert creators["old-1"] == "new-op"
    assert creators["old-2"] is None
    assert creators["old-3"] is None


def test_same_id_email_match_keeps_creator_mapping() -> None:
    # Регрессия: email совпал и id совпадают — remap обязан сохраниться,
    # иначе новые события теряют идентифицируемого создателя.
    plan = _plan(
        current_users=[_user("op", "op@example.com")],
        legacy_users=[_user("op", "op@example.com")],
        legacy_events=[_event("old", start="2026-10-25", created_by_id="op")],
        legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
    )
    assert plan.user_remap == {"op": "op"}
    assert len(plan.event_inserts) == 1
    assert plan.event_inserts[0]["created_by_id"] == "op"


def test_deterministic_day_id_collisions_are_rejected() -> None:
    source_event = _event("old", start="2026-10-25", duration=2)
    source_day = _day("o1", "old", 1, stream_url="https://old/1")
    new_id = deterministic_day_id("old", "o1")
    uuid.UUID(new_id)
    with pytest.raises(IdCollisionError):
        _plan(
            current_events=[_event("live", start="2026-10-25", duration=2)],
            legacy_events=[source_event],
            current_days=[_day(new_id, "live", 2)],
            legacy_days=[source_day],
        )


def test_ambiguous_tournament_match_raises_before_writes() -> None:
    with pytest.raises(AmbiguousMatchError):
        _plan(
            current_events=[
                _event("live-1", start="2026-10-25", duration=2, tournament_id=7),
                _event("live-2", start="2026-10-25", duration=2, tournament_id=7),
            ],
            legacy_events=[_event("old", start="2026-10-25", duration=2, tournament_id=7)],
            legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
        )


def test_ambiguous_title_signature_raises() -> None:
    with pytest.raises(AmbiguousMatchError):
        _plan(
            current_events=[
                _event("live-1", title="Кубок", start="2026-10-25"),
                _event("live-2", title="кубок", start="2026-10-25"),
            ],
            legacy_events=[_event("old", title="Кубок", start="2026-10-25")],
            legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
        )


def test_tournament_ambiguity_considers_all_candidates_before_used_target_filter() -> None:
    # Регрессия (correction 3): неоднозначность оценивается среди ВСЕХ
    # совместимых кандидатов, до исключения занятых. Два совместимых
    # кандидата с одним tournament_id: первый занят другим событием
    # источника (через точный id), второй «свободен». Молчаливый выбор
    # «свободного» запрещён — идентичность неоднозначна, исключение до записи.
    with pytest.raises(AmbiguousMatchError):
        _plan(
            current_events=[
                # окна: live-1 = 10-25..10-26, live-2 = 10-26..10-26
                _event("live-1", title="Кубок", start="2026-10-25", duration=2, tournament_id=7),
                _event("live-2", title="Кубок", start="2026-10-26", duration=1, tournament_id=7),
            ],
            legacy_events=[
                # old-1 (start 10-25) совместим ТОЛЬКО с live-1 и занимает его
                _event("old-1", title="Кубок", start="2026-10-25", duration=2, tournament_id=7),
                # old-2 (start 10-26) совместим с ОБОИМИ: live-1 уже занят,
                # live-2 «свободен» — но неоднозначность считается по всем
                # кандидатам: исключение, а не молчаливый выбор live-2
                _event("old-2", title="Кубок", start="2026-10-26", duration=1, tournament_id=7),
            ],
            current_days=[_day("d1", "live-1", 1), _day("d2", "live-2", 1)],
            legacy_days=[
                _day("o1", "old-1", 1, stream_url="https://old/1"),
                _day("o2", "old-2", 1, stream_url="https://old/2"),
            ],
        )


def test_signature_ambiguity_considers_all_candidates_before_used_target_filter() -> None:
    # Та же регрессия для ветки сигнатуры title+start_date: один совпадающий
    # кандидат занят событием источника через tournament_id, второй свободен.
    # «Свободный» не выбирается молча: среди всех кандидатов сигнатуры — два.
    with pytest.raises(AmbiguousMatchError):
        _plan(
            current_events=[
                _event("live-1", title="Кубок", start="2026-10-25", duration=2, tournament_id=7),
                _event("live-2", title="кубок", start="2026-10-25", duration=2),
            ],
            legacy_events=[
                # old-1 занимает live-1 по tournament_id
                _event("old-1", title="Другое название", start="2026-10-25", duration=2, tournament_id=7),
                # old-2 матчится по сигнатуре на ОБА текущих события
                # (нормализация title casefold/ё-е); live-1 занят — исключение
                _event("old-2", title="Кубок", start="2026-10-25", duration=2),
            ],
            current_days=[_day("d1", "live-1", 1), _day("d2", "live-2", 1)],
            legacy_days=[
                _day("o1", "old-1", 1, stream_url="https://old/1"),
                _day("o2", "old-2", 1, stream_url="https://old/2"),
            ],
        )


def test_single_compatible_candidate_claimed_by_other_source_event_raises() -> None:
    # Регрессия: единственный совместимый кандидат, уже занятый другим
    # событием источника, — исключение (не молчаливый выбор, не вставка
    # дубля с занятым tournament_id).
    with pytest.raises(AmbiguousMatchError):
        _plan(
            current_events=[
                _event("live-1", start="2026-10-25", duration=2, tournament_id=7),
            ],
            legacy_events=[
                _event("old-1", start="2026-10-25", duration=2, tournament_id=7),
                _event("old-2", start="2026-10-25", duration=2, tournament_id=7),
            ],
            current_days=[_day("d1", "live-1", 1), _day("d2", "live-1", 2)],
            legacy_days=[
                _day("o1", "old-1", 1, stream_url="https://old/1"),
                _day("o2", "old-2", 2, stream_url="https://old/2"),
            ],
        )


def test_same_id_with_different_identity_raises() -> None:
    with pytest.raises(AmbiguousMatchError):
        _plan(
            current_events=[_event("same", title="Новое", start="2026-10-25")],
            legacy_events=[_event("same", title="Старое", start="2026-10-25")],
            legacy_days=[_day("o1", "same", 1, stream_url="https://old/1")],
        )


def test_two_legacy_events_competing_for_one_current_event_raise() -> None:
    with pytest.raises(AmbiguousMatchError):
        _plan(
            current_events=[_event("live", start="2026-10-25", duration=2, tournament_id=7)],
            legacy_events=[
                _event("old-1", start="2026-10-25", duration=2, tournament_id=7),
                _event("old-2", start="2026-10-25", duration=2, tournament_id=7),
            ],
            legacy_days=[
                _day("a", "old-1", 1, stream_url="https://old/a"),
                _day("b", "old-2", 1, stream_url="https://old/b"),
            ],
        )


def test_two_legacy_events_with_same_id_cannot_target_one_current_event() -> None:
    # Регрессия: точный id не проверял, что текущее событие уже занято другим
    # событием источника — конкурирующие обновления без ошибки неоднозначности.
    with pytest.raises(AmbiguousMatchError):
        _plan(
            current_events=[_event("live", title="Турнир", start="2026-10-25", duration=2)],
            legacy_events=[
                _event("old-1", title="Турнир", start="2026-10-25", duration=2),
                _event("old-2", title="Турнир", start="2026-10-25", duration=2),
            ],
            current_days=[_day("d1", "live", 1), _day("d2", "live", 2)],
            legacy_days=[
                _day("a", "old-1", 1, stream_url="https://old/a"),
                _day("b", "old-2", 2, stream_url="https://old/b"),
            ],
        )


def test_blank_title_cannot_establish_identity_by_exact_id() -> None:
    # Регрессия: два пустых title раньше давали равные сигнатуры (None == None)
    # и ложно подтверждали идентичность по точному id.
    with pytest.raises(AmbiguousMatchError):
        _plan(
            current_events=[_event("same", title="", start="2026-10-25")],
            legacy_events=[_event("same", title="  ", start="2026-10-25")],
            legacy_days=[_day("o1", "same", 1, stream_url="https://old/1")],
        )


def test_blank_title_cannot_establish_identity_by_signature() -> None:
    # Пустой title не доказывает идентичность и по сигнатуре: событие с пустым
    # title не матчится на текущее с тем же start_date, а вставляется отдельно.
    plan = _plan(
        current_events=[_event("live", title="", start="2026-10-25", duration=1)],
        legacy_events=[_event("old", title="", start="2026-10-25", duration=1)],
        current_days=[_day("d1", "live", 1)],
        legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
    )
    assert plan.day_updates == []
    assert len(plan.event_inserts) == 1
    assert plan.event_inserts[0]["id"] == "old"


def test_historical_url_overwrites_only_target_day() -> None:
    plan = _plan(
        current_events=[_event("live", start="2026-10-25", duration=2)],
        legacy_events=[_event("old", start="2026-10-25", duration=2)],
        current_days=[
            _day("d1", "live", 1, stream_url="https://current/1", server_url="rtmp://srv", stream_key="key-1"),
            _day("d2", "live", 2, stream_url="https://current/2", server_url="rtmp://srv2", stream_key="key-2"),
        ],
        legacy_days=[_day("o1", "old", 1, stream_url="https://old/1", server_url="rtmp://old", stream_key="old-key")],
    )
    assert plan.day_updates == [{"id": "d1", "stream_url": "https://old/1"}]
    assert plan.day_inserts == []
    # нет затрагивания day 2: server_url/stream_key текущих дней не попадают в план
    assert all(set(row) <= {"id", "stream_url"} for row in plan.day_updates)


def test_current_auth_fields_are_never_in_plan() -> None:
    plan = _plan(
        current_users=[_user("op", "op@example.com")],
        legacy_users=[_user("old-op", "op@example.com")],
        legacy_events=[_event("old", start="2026-10-25", created_by_id="old-op")],
        legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
    )
    blob = repr(plan)
    assert "password" not in blob
    assert "role" not in blob
    assert plan.user_remap == {"old-op": "op"}
    assert len(plan.event_inserts) == 1


def test_source_server_url_and_stream_key_are_not_imported() -> None:
    plan = _plan(
        legacy_events=[_event("old", start="2026-10-25", duration=2)],
        legacy_days=[
            _day("o1", "old", 1, stream_url="https://old/1", server_url="rtmp://legacy", stream_key="secret-key"),
            _day("o2", "old", 2, stream_url="https://old/2", server_url="rtmp://legacy2", stream_key="secret-key-2"),
        ],
    )
    assert len(plan.event_inserts) == 1
    assert plan.event_inserts[0]["duration_days"] == 2
    assert len(plan.day_inserts) == 2
    for row in plan.day_inserts:
        assert row["server_url"] == ""
        assert row["stream_key"] == ""
        assert "rtmp://legacy" not in repr(row)
        assert "secret-key" not in repr(row)


def test_new_historical_event_duration_clipped_to_last_day_before_cutoff() -> None:
    plan = _plan(
        legacy_events=[_event("old", start="2026-10-28", duration=10)],
        legacy_days=[
            _day("o1", "old", 1, stream_url="https://old/1"),
            _day("o2", "old", 2, stream_url="https://old/2"),
            _day("o3", "old", 3, stream_url="https://old/3"),
            _day("o4", "old", 4, stream_url="https://old/4"),
        ],
    )
    assert len(plan.event_inserts) == 1
    # последний qualifying день — 2026-10-31 (day 4), дальше cutoff
    assert plan.event_inserts[0]["duration_days"] == 4
    assert len(plan.day_inserts) == 4


def test_event_without_qualifying_links_is_not_inserted() -> None:
    plan = _plan(
        legacy_events=[_event("old", start="2026-10-25", duration=1)],
        legacy_days=[_day("o1", "old", 1, stream_url="")],
    )
    assert plan.event_inserts == []
    assert plan.day_inserts == []
    assert plan.skipped_events == 1


def test_content_url_restored_only_for_events_entirely_before_cutoff() -> None:
    plan = _plan(
        current_events=[
            _event("past", start="2026-10-20", duration=2),
            _event("boundary", start="2026-10-30", duration=3),
            _event("future", start="2026-11-10", duration=1),
        ],
        legacy_events=[
            _event("old-past", start="2026-10-20", duration=2, content_url="https://disk/past"),
            _event("old-boundary", start="2026-10-30", duration=3, content_url="https://disk/boundary"),
            _event("old-future", start="2026-11-10", duration=1, content_url="https://disk/future"),
        ],
        current_days=[
            _day("p1", "past", 1),
            _day("p2", "past", 2),
            _day("b1", "boundary", 1),
            _day("b2", "boundary", 2),
            _day("b3", "boundary", 3),
            _day("f1", "future", 1),
        ],
        legacy_days=[
            _day("op1", "old-past", 1, stream_url="https://x/1"),
            _day("ob1", "old-boundary", 1, stream_url="https://x/2"),
            _day("ob2", "old-boundary", 2, stream_url="https://x/3"),
            _day("ob3", "old-boundary", 3, stream_url="https://x/4"),
            _day("of1", "old-future", 1, stream_url="https://x/5"),
        ],
    )
    updates = {row["id"]: row["content_url"] for row in plan.event_updates}
    assert updates == {"past": "https://disk/past"}
    # boundary (2026-10-30..2026-11-01) пересекает cutoff — content_url не трогаем,
    # но дни до cutoff обновляются; future — не трогаем вообще.
    assert {row["id"] for row in plan.day_updates} == {"p1", "b1", "b2"}


def test_content_url_never_copied_from_source_crossing_cutoff() -> None:
    # Регрессия: источник пересекает cutoff, а назначение (после обрезки окна
    # текущим duration) — нет. content_url источника всё равно не переносится.
    plan = _plan(
        current_events=[_event("live", start="2026-10-28", duration=2, content_url=None)],
        legacy_events=[
            _event("old", start="2026-10-28", duration=5, content_url="https://disk/crossing")
        ],
        current_days=[_day("d1", "live", 1), _day("d2", "live", 2)],
        legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
    )
    assert plan.event_updates == []
    assert plan.day_updates == [{"id": "d1", "stream_url": "https://old/1"}]


def test_content_url_not_set_on_new_event_clipped_from_crossing_source() -> None:
    # Регрессия: новое событие обрезано по последнему историческому дню и
    # выглядит «целиком до cutoff», но источник пересекал cutoff — content_url
    # не копируется.
    plan = _plan(
        legacy_events=[
            _event("old", start="2026-10-28", duration=10, content_url="https://disk/crossing")
        ],
        legacy_days=[
            _day("o1", "old", 1, stream_url="https://old/1"),
            _day("o2", "old", 2, stream_url="https://old/2"),
        ],
    )
    assert len(plan.event_inserts) == 1
    assert plan.event_inserts[0]["duration_days"] == 2
    assert plan.event_inserts[0]["content_url"] is None


def test_content_url_only_link_is_restored_for_matched_past_event() -> None:
    # у события нет qualifying stream_url, но есть content_url целиком до cutoff —
    # ссылка не теряется молча, а восстанавливается на matched-событие.
    plan = _plan(
        current_events=[_event("live", start="2026-10-20", duration=2, content_url=None)],
        legacy_events=[_event("old", start="2026-10-20", duration=2, content_url="https://disk/only")],
        current_days=[_day("d1", "live", 1), _day("d2", "live", 2)],
        legacy_days=[_day("o1", "old", 1, stream_url="")],
    )
    assert plan.event_updates == [{"id": "live", "content_url": "https://disk/only"}]
    assert plan.day_updates == []
    assert plan.day_inserts == []


def test_content_url_only_skipped_on_boundary_crossing_matched_event() -> None:
    plan = _plan(
        current_events=[_event("live", start="2026-10-30", duration=3, content_url=None)],
        legacy_events=[_event("old", start="2026-10-30", duration=3, content_url="https://disk/x")],
        current_days=[_day("d1", "live", 1)],
        legacy_days=[_day("o1", "old", 1, stream_url="")],
    )
    assert plan.event_updates == []
    assert plan.event_inserts == []


def test_content_only_historical_event_absent_current_is_inserted() -> None:
    # Регрессия: content-only событие, отсутствующее в текущей базе, молча
    # пропускалось — публичная ссылка терялась. Теперь оно восстанавливается
    # новым событием с явными безопасными метаданными.
    plan = _plan(
        current_users=[_user("op", "op@example.com")],
        legacy_users=[_user("old-op", "op@example.com")],
        legacy_events=[
            _event(
                "old",
                title="Архив",
                start="2026-10-20",
                duration=2,
                content_url="https://disk/archive",
                created_by_id="old-op",
            )
        ],
        legacy_days=[_day("o1", "old", 1, stream_url="")],
    )
    assert len(plan.event_inserts) == 1
    new_event = plan.event_inserts[0]
    assert new_event["id"] == "old"
    assert new_event["title"] == "Архив"
    assert new_event["start_date"] == date(2026, 10, 20)
    assert new_event["duration_days"] == 2
    assert new_event["content_url"] == "https://disk/archive"
    assert new_event["created_by_id"] == "op"
    assert new_event["ffkm_admin_tournament_id"] is None
    assert plan.day_inserts == []
    assert plan.skipped_events == 0


def test_content_only_new_event_duration_clipped_before_cutoff() -> None:
    # Длительность content-only события обрезается по последнему дню целиком
    # до cutoff: будущие дни не создаются. Источник целиком до cutoff —
    # content_url восстанавливается.
    plan = _plan(
        legacy_events=[
            _event("old", title="Архив", start="2026-10-28", duration=3, content_url="https://disk/a")
        ],
        legacy_days=[_day("o1", "old", 1, stream_url="")],
    )
    assert len(plan.event_inserts) == 1
    # 2026-10-28 + 3 дня = 2026-10-31 < cutoff; обрезки нет.
    assert plan.event_inserts[0]["duration_days"] == 3
    assert plan.event_inserts[0]["content_url"] == "https://disk/a"


def test_content_only_event_crossing_cutoff_is_not_inserted() -> None:
    # Источник пересекает cutoff — content_url не восстановим, событие пропускается.
    plan = _plan(
        legacy_events=[
            _event("old", title="Архив", start="2026-10-30", duration=5, content_url="https://disk/x")
        ],
        legacy_days=[_day("o1", "old", 1, stream_url="")],
    )
    assert plan.event_inserts == []
    assert plan.skipped_events == 1


def test_plan_is_idempotent_after_simulated_apply() -> None:
    current_events = [_event("live", start="2026-10-25", duration=2)]
    current_days = [_day("d1", "live", 1), _day("d2", "live", 2)]
    legacy_events = [_event("old", start="2026-10-25", duration=2)]
    legacy_days = [_day("o1", "old", 1, stream_url="https://old/1")]
    first = _plan(
        current_events=current_events,
        legacy_events=legacy_events,
        current_days=current_days,
        legacy_days=legacy_days,
    )
    assert len(first.day_updates) == 1
    # симулируем применение: stream_url перенесён, новых событий нет
    current_days[0]["stream_url"] = "https://old/1"
    second = _plan(
        current_events=current_events,
        legacy_events=legacy_events,
        current_days=current_days,
        legacy_days=legacy_days,
    )
    assert not second.has_changes()
    assert second.day_updates == []
    assert second.day_inserts == []
    assert second.event_inserts == []
    assert second.event_updates == []


def test_plan_sha256_stable_and_sensitive_to_content() -> None:
    kwargs = dict(
        current_events=[_event("live", start="2026-10-25", duration=1)],
        legacy_events=[_event("old", start="2026-10-25", duration=1)],
        current_days=[_day("d1", "live", 1)],
        legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
    )
    sha1 = plan_sha256(_plan(**kwargs))
    sha2 = plan_sha256(_plan(**kwargs))
    assert sha1 == sha2
    changed = dict(kwargs)
    changed["legacy_days"] = [dict(kwargs["legacy_days"][0], stream_url="https://old/2")]
    assert plan_sha256(_plan(**changed)) != sha1


def test_plan_sha256_bound_to_destination_url_preimages() -> None:
    # Регрессия: хэш плана не включал прообразы назначения. Для legacy URL C
    # смена текущего URL дня с A на B оставляла план и хэш прежними, и apply
    # перезаписывал непроверенное изменение. Теперь хэш обязан отличаться.
    plan = _plan(
        current_events=[_event("live", start="2026-10-25", duration=1)],
        legacy_events=[_event("old", start="2026-10-25", duration=1)],
        current_days=[_day("d1", "live", 1, stream_url="https://current/A")],
        legacy_days=[_day("o1", "old", 1, stream_url="https://old/C")],
    )
    snapshots_a = {
        "current": _snapshot(days=[("d1", "live", 1, "https://current/A", "", "")]),
        "legacy": {},
    }
    snapshots_b = {
        "current": _snapshot(days=[("d1", "live", 1, "https://current/B", "", "")]),
        "legacy": {},
    }
    sha_a = plan_sha256(plan, snapshots_a)
    sha_b = plan_sha256(plan, snapshots_b)
    assert sha_a != sha_b
    # План (update A->C) тот же, но хэш привязан к снимку — drift пойман.
    assert plan.day_updates == [{"id": "d1", "stream_url": "https://old/C"}]


def test_plan_sha256_bound_to_protected_fields() -> None:
    plan = _plan(
        current_events=[_event("live", start="2026-10-25", duration=1)],
        legacy_events=[_event("old", start="2026-10-25", duration=1)],
        current_days=[_day("d1", "live", 1)],
        legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
    )
    base = {
        "current": _snapshot(
            days=[("d1", "live", 1, "", "", "")],
            events=[("live", "Турнир", "2026-10-25", 1, None, None, "rank", None, "op", "c", "u")],
            users=[("op", "op@example.com", "name", True, "hash", "admin")],
        ),
        "legacy": {},
    }
    sha = plan_sha256(plan, base)
    mutated_users = {
        "current": _snapshot(
            days=base["current"]["days"]["rows"],
            events=base["current"]["events"]["rows"],
            users=[("op", "op@example.com", "name", True, "hash2", "admin")],
        ),
        "legacy": {},
    }
    assert plan_sha256(plan, mutated_users) != sha
    mutated_events = {
        "current": _snapshot(
            days=base["current"]["days"]["rows"],
            events=[("live", "Турнир", "2026-10-25", 2, None, None, "rank", None, "op", "c", "u")],
            users=base["current"]["users"]["rows"],
        ),
        "legacy": {},
    }
    assert plan_sha256(plan, mutated_events) != sha
    # drift в ЛЮБОМ поле полного снимка меняет хэш: ffkm_admin_rank события,
    # username/is_active пользователя, server_url/stream_key дня.
    mutated_rank = {
        "current": _snapshot(
            days=base["current"]["days"]["rows"],
            events=[("live", "Турнир", "2026-10-25", 1, None, None, "rank2", None, "op", "c", "u")],
            users=base["current"]["users"]["rows"],
        ),
        "legacy": {},
    }
    assert plan_sha256(plan, mutated_rank) != sha
    mutated_username = {
        "current": _snapshot(
            days=base["current"]["days"]["rows"],
            events=base["current"]["events"]["rows"],
            users=[("op", "op@example.com", "name2", True, "hash", "admin")],
        ),
        "legacy": {},
    }
    assert plan_sha256(plan, mutated_username) != sha
    mutated_active = {
        "current": _snapshot(
            days=base["current"]["days"]["rows"],
            events=base["current"]["events"]["rows"],
            users=[("op", "op@example.com", "name", False, "hash", "admin")],
        ),
        "legacy": {},
    }
    assert plan_sha256(plan, mutated_active) != sha
    mutated_server_url = {
        "current": _snapshot(
            days=[("d1", "live", 1, "", "srv2", "")],
            events=base["current"]["events"]["rows"],
            users=base["current"]["users"]["rows"],
        ),
        "legacy": {},
    }
    assert plan_sha256(plan, mutated_server_url) != sha
    mutated_legacy = {
        "current": base["current"],
        "legacy": {"days": [("o1", "old", 1, "https://old/2", "", "")]},
    }
    assert plan_sha256(plan, mutated_legacy) != sha


def test_idempotence_with_new_event_and_day_inserts() -> None:
    legacy_events = [_event("old", start="2026-10-25", duration=2, content_url="https://disk/x")]
    legacy_days = [
        _day("o1", "old", 1, stream_url="https://old/1"),
        _day("o2", "old", 2, stream_url="https://old/2"),
    ]
    current_events = []
    current_days = []
    first = _plan(
        current_events=current_events,
        legacy_events=legacy_events,
        current_days=current_days,
        legacy_days=legacy_days,
    )
    assert len(first.event_inserts) == 1
    assert len(first.day_inserts) == 2
    # симулируем применение: событие и дни появились в текущей базе с теми же id
    applied_event = dict(first.event_inserts[0])
    current_events.append(applied_event)
    for row in first.day_inserts:
        current_days.append(dict(row))
    second = _plan(
        current_events=current_events,
        legacy_events=legacy_events,
        current_days=current_days,
        legacy_days=legacy_days,
    )
    assert not second.has_changes()
    assert second.event_inserts == []
    assert second.day_inserts == []
    assert second.day_updates == []
    assert second.event_updates == []


def test_adapt_handles_none_uuid_and_dates() -> None:
    assert adapt(None) is None
    assert adapt(uuid.UUID("12345678-1234-5678-1234-567812345678")) == "12345678-1234-5678-1234-567812345678"
    assert adapt(date(2026, 11, 1)) == "2026-11-01"
    assert adapt({"a": 1}) == '{"a": 1}'


def test_business_date_is_one_based() -> None:
    assert business_date("2026-10-25", 1) == date(2026, 10, 25)
    assert business_date("2026-10-25", 3) == date(2026, 10, 27)
    assert business_date("2026-10-25", 0) is None
    assert CUTOFF_DATE == date(2026, 11, 1)
    assert MIGRATION_VERSION == "recovery-links-20261113"


def test_sync_url_strips_asyncpg_driver() -> None:
    assert sync_url("postgresql+asyncpg://u@h/db") == "postgresql://u@h/db"
    assert sync_url("postgresql://u@h/db") == "postgresql://u@h/db"


def test_apply_requires_expected_plan_sha256(monkeypatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "recovery_links_20261113",
            "--current-url",
            "postgresql://a/db1",
            "--legacy-url",
            "postgresql://b/db2",
            "--apply",
        ],
    )
    with pytest.raises(SystemExit):
        cli_main()


def test_rejects_same_database_for_current_and_legacy(monkeypatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "recovery_links_20261113",
            "--current-url",
            "postgresql://a/db1",
            "--legacy-url",
            "postgresql://a/db1",
        ],
    )
    with pytest.raises(SystemExit):
        cli_main()


def _snapshot(days=(), events=(), users=(), postcutoff_days=None) -> dict:
    """Снимок полных строк в форме snapshot_fingerprint (кортежи или dict-ы)."""
    day_cols = ["id", "stream_event_id", "day_index", "stream_url", "server_url", "stream_key"]
    event_cols = [
        "id", "title", "start_date", "duration_days", "ffkm_admin_tournament_id",
        "ffkm_admin_rank", "content_url", "locked_by_user_id", "created_by_id",
        "created_at", "updated_at",
    ]
    user_cols = ["id", "email", "username", "is_active", "password_hash", "role"]

    def _rows(cols, values):
        return [dict(v) if isinstance(v, dict) else dict(zip(cols, v)) for v in values]

    day_rows = _rows(day_cols, days)
    return {
        "days": {"columns": day_cols, "rows": day_rows},
        "events": {"columns": event_cols, "rows": _rows(event_cols, events)},
        "users": {"columns": user_cols, "rows": _rows(user_cols, users)},
        "postcutoff_days": {
            "columns": day_cols,
            "rows": day_rows if postcutoff_days is None else _rows(day_cols, postcutoff_days),
        },
    }


def _empty_plan() -> RecoveryPlan:
    return RecoveryPlan()


def test_postapply_invariant_allows_new_rows_but_not_mutations() -> None:
    before = _snapshot(
        days=[("day-x", "ev", 5, "u", "s", "k")],
        events=[("ev", "t", "2026-10-01", 1, None, None, "rank", None, "u", "c", "x")],
        users=[("u", "m", "name", True, "h", "role")],
    )
    after_new_rows = _snapshot(
        days=[("day-x", "ev", 5, "u", "s", "k"), ("new-day", "new-ev", 1, "nu", "", "")],
        events=before["events"]["rows"] + [("new", "t2", "2026-10-02", 1, None, None, None, None, None, "c2", "x2")],
        users=before["users"]["rows"],
        postcutoff_days=[("day-x", "ev", 5, "u", "s", "k")],
    )
    assert_postapply_invariant(before, after_new_rows, _empty_plan())
    after_mutated = _snapshot(
        days=[("day-x", "ev", 5, "u2", "s", "k")],
        events=before["events"]["rows"],
        users=before["users"]["rows"],
        postcutoff_days=[("day-x", "ev", 5, "u2", "s", "k")],
    )
    with pytest.raises(SystemExit):
        assert_postapply_invariant(before, after_mutated, _empty_plan())
    after_lost = _snapshot(
        days=[],
        events=before["events"]["rows"],
        users=before["users"]["rows"],
        postcutoff_days=[],
    )
    with pytest.raises(SystemExit):
        assert_postapply_invariant(before, after_lost, _empty_plan())


def test_postapply_invariant_allows_only_planned_url_mutations() -> None:
    # Регрессия (correction 3): пост-записной инвариант разрешает отличия
    # строго в намеренно мутированных URL плана и ни в чём больше.
    before = _snapshot(
        days=[("day-x", "ev", 1, "old-url", "srv", "key"), ("day-y", "ev", 2, "keep", "srv2", "key2")],
        events=[("ev", "t", "2026-10-01", 2, 7, None, "old-content", None, "u", "c", "x")],
        users=[("u", "m", "name", True, "h", "role")],
    )
    plan = RecoveryPlan(
        day_updates=[{"id": "day-x", "stream_url": "new-url"}],
        event_updates=[{"id": "ev", "content_url": "new-content"}],
    )
    ok = _snapshot(
        days=[("day-x", "ev", 1, "new-url", "srv", "key"), ("day-y", "ev", 2, "keep", "srv2", "key2")],
        events=[("ev", "t", "2026-10-01", 2, 7, None, "new-content", None, "u", "c", "x")],
        users=before["users"]["rows"],
    )
    assert_postapply_invariant(before, ok, plan)
    # server_url дня из плана тронут — неразрешённое поле, отказ
    bad_server = _snapshot(
        days=[("day-x", "ev", 1, "new-url", "srv-CHANGED", "key"), ("day-y", "ev", 2, "keep", "srv2", "key2")],
        events=ok["events"]["rows"],
        users=before["users"]["rows"],
    )
    with pytest.raises(SystemExit):
        assert_postapply_invariant(before, bad_server, plan)
    # stream_key дня из плана тронут — отказ
    bad_key = _snapshot(
        days=[("day-x", "ev", 1, "new-url", "srv", "key-CHANGED"), ("day-y", "ev", 2, "keep", "srv2", "key2")],
        events=ok["events"]["rows"],
        users=before["users"]["rows"],
    )
    with pytest.raises(SystemExit):
        assert_postapply_invariant(before, bad_key, plan)
    # день ВНЕ плана перезаписан — отказ
    bad_other_day = _snapshot(
        days=[("day-x", "ev", 1, "new-url", "srv", "key"), ("day-y", "ev", 2, "keep-CHANGED", "srv2", "key2")],
        events=ok["events"]["rows"],
        users=before["users"]["rows"],
    )
    with pytest.raises(SystemExit):
        assert_postapply_invariant(before, bad_other_day, plan)
    # нессылочное поле события из плана (title) тронуто — отказ
    bad_title = _snapshot(
        days=ok["days"]["rows"],
        events=[("ev", "t-CHANGED", "2026-10-01", 2, 7, None, "new-content", None, "u", "c", "x")],
        users=before["users"]["rows"],
    )
    with pytest.raises(SystemExit):
        assert_postapply_invariant(before, bad_title, plan)
    # ffkm_admin_rank события из плана тронут — отказ (поле вне белого списка URL)
    bad_rank = _snapshot(
        days=ok["days"]["rows"],
        events=[("ev", "t", "2026-10-01", 2, 7, "rank-CHANGED", "new-content", None, "u", "c", "x")],
        users=before["users"]["rows"],
    )
    with pytest.raises(SystemExit):
        assert_postapply_invariant(before, bad_rank, plan)
    # username/is_active пользователя тронуты — отказ
    bad_user = _snapshot(
        days=ok["days"]["rows"],
        events=ok["events"]["rows"],
        users=[("u", "m", "name-CHANGED", True, "h", "role")],
    )
    with pytest.raises(SystemExit):
        assert_postapply_invariant(before, bad_user, plan)
    bad_user_active = _snapshot(
        days=ok["days"]["rows"],
        events=ok["events"]["rows"],
        users=[("u", "m", "name", False, "h", "role")],
    )
    with pytest.raises(SystemExit):
        assert_postapply_invariant(before, bad_user_active, plan)
    # новый пост-cutoff день — отказ
    bad_postcutoff = _snapshot(
        days=ok["days"]["rows"] + [("future-day", "ev", 9, "u", "", "")],
        events=ok["events"]["rows"],
        users=before["users"]["rows"],
        postcutoff_days=[("future-day", "ev", 9, "u", "", "")],
    )
    with pytest.raises(SystemExit):
        assert_postapply_invariant(before, bad_postcutoff, plan)


def test_duplicate_current_email_is_ambiguous() -> None:
    with pytest.raises(AmbiguousMatchError):
        _plan(
            current_users=[_user("u1", "dup@example.com"), _user("u2", "DUP@example.com")],
            legacy_users=[_user("old", "dup@example.com")],
        )


def test_new_event_id_collision_with_unrelated_current_event_raises() -> None:
    # id совпадает, но идентичность другая; tournament/signature не дают совпадения —
    # вставка с занятым id должна быть отвергнута, а не замаскирована.
    with pytest.raises(AmbiguousMatchError):
        _plan(
            current_events=[_event("old", title="Другое", start="2026-11-10", duration=1)],
            legacy_events=[_event("old", title="Турнир", start="2026-10-25", duration=1)],
            legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
        )


def test_new_event_clipped_from_crossing_source_omits_content_url() -> None:
    # Регрессия (finding 2): источник пересекает cutoff, а назначение после
    # обрезки выглядит «целиком до cutoff». content_url всё равно не копируется.
    plan = _plan(
        legacy_events=[_event("old", start="2026-10-30", duration=5, content_url="https://disk/x")],
        legacy_days=[
            _day("o1", "old", 1, stream_url="https://old/1"),
            _day("o2", "old", 2, stream_url="https://old/2"),
        ],
    )
    assert len(plan.event_inserts) == 1
    assert plan.event_inserts[0]["duration_days"] == 2
    assert plan.event_inserts[0]["content_url"] is None


def test_no_day_inserted_on_or_after_cutoff_for_matched_event() -> None:
    plan = _plan(
        current_events=[_event("live", start="2026-10-30", duration=5)],
        legacy_events=[_event("old", start="2026-10-30", duration=5)],
        current_days=[_day("d1", "live", 1)],
        legacy_days=[
            _day("o1", "old", 1, stream_url="https://old/1"),
            _day("o2", "old", 2, stream_url="https://old/2"),  # 2026-10-31 — до cutoff, вставка
            _day("o3", "old", 3, stream_url="https://old/3"),  # 2026-11-01 = cutoff — пропуск
        ],
    )
    assert plan.day_updates == [{"id": "d1", "stream_url": "https://old/1"}]
    assert len(plan.day_inserts) == 1
    assert plan.day_inserts[0]["day_index"] == 2
    assert plan.skipped_days == 1


def test_future_current_event_days_never_touched() -> None:
    plan = _plan(
        current_events=[_event("live", start="2026-11-05", duration=2)],
        legacy_events=[_event("old", start="2026-11-05", duration=2)],
        current_days=[_day("d1", "live", 1, stream_url="https://current/1")],
        legacy_days=[_day("o1", "old", 1, stream_url="https://old/1")],
    )
    assert plan.day_updates == []
    assert plan.day_inserts == []
    assert plan.event_updates == []
    assert plan.skipped_days == 1


class _FakeCursor:
    def __init__(self, conn):
        self.connection = conn
        self.description = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def execute(self, query, params=None):
        text = str(query)
        self.connection.executed.append((text, params))
        self.description = None
        if "to_regclass" in text:
            self.connection._pending = [("exists",)]
        elif text.lstrip().upper().startswith("SELECT"):
            # пакет строк выбирается по форме запроса: одно и то же «состояние
            # базы» на каждом проходе (dry-run, чтение в apply, fingerprint
            # до/после), независимо от порядка и количества запросов
            key = _classify_query(text, params)
            packet = self.connection.packets.get(key, {})
            if isinstance(packet, dict):
                # снимок: пакет с колонками (cur.description) и строками
                self.description = tuple((name,) for name in packet.get("columns", []))
                self.connection._pending = list(packet.get("rows", []))
            else:
                self.connection._pending = list(packet)

    def fetchall(self):
        rows = list(self.connection._pending)
        self.connection._pending = []
        return rows

    def fetchone(self):
        rows = self.fetchall()
        return rows[0] if rows else None


def _classify_query(text: str, params=None) -> str:
    """Ключ пакета строк по форме SQL: какая таблица и какие колонки читаются."""
    t = " ".join(str(text).split()).upper()
    if "INFORMATION_SCHEMA.COLUMNS" in t:
        # schema-проверка: пакет колонок свой для каждой таблицы (параметр %s)
        return f"columns:{params[0] if params else '?'}"
    if "FROM PUBLIC.STREAM_DAYS" in t:
        if "DAY_INDEX - 1" in t:
            return "postcutoff_days"
        return "days"
    if "FROM PUBLIC.STREAM_EVENTS" in t:
        return "events"
    if "FROM PUBLIC.USERS" in t:
        return "users"
    return "misc"


class _FakeConn:
    """Имитация psycopg2-соединения для CLI-тестов без базы.

    packets: {ключ формы запроса: строки} — каждый SELECT получает пакет по
    форме запроса, поэтому повторные чтения видят одно и то же состояние.
    """

    def __init__(self, packets=None):
        self.packets = dict(packets or {})
        self._pending = []
        self.executed = []
        self.committed = False
        self.rolled_back = False
        self.closed = False
        self.session = None

    def cursor(self):
        return _FakeCursor(self)

    def set_session(self, **kwargs):
        self.session = kwargs

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


def _run_cli(monkeypatch, argv, current_packets, legacy_packets):
    import scripts.recovery_links_20261113 as cli

    conns = {"current": _FakeConn(current_packets), "legacy": _FakeConn(legacy_packets)}

    def fake_connect(url):
        return conns["current"] if "current" in url else conns["legacy"]

    fake_psycopg2 = type(sys)("psycopg2")
    fake_psycopg2.connect = fake_connect
    fake_sql = type(sys)("psycopg2.sql")

    class _FakeSQL:
        def __init__(self, s):
            self.s = s

        def format(self, **kwargs):
            # подставляем идентификаторы в шаблон, чтобы текст запроса был
            # похож на реальный SQL — классификация пакетов по форме запроса
            # опирается на имена таблиц и колонок в тексте.
            rendered = self.s
            for key, value in kwargs.items():
                rendered = rendered.replace("{" + key + "}", str(value))
            return _FakeSQL(rendered)

        def join(self, other):
            return _FakeSQL(", ".join(str(item) for item in other))

        def __str__(self):
            return self.s

    fake_sql.SQL = _FakeSQL
    fake_sql.Identifier = lambda *names: _FakeSQL(".".join(str(n) for n in names))
    fake_psycopg2.sql = fake_sql
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setitem(sys.modules, "psycopg2", fake_psycopg2)
    monkeypatch.setitem(sys.modules, "psycopg2.sql", fake_sql)
    monkeypatch.setattr(cli, "check_columns", lambda conn, tables, required: None)
    return conns, cli


_DAY_SNAPSHOT_COLUMNS = ["id", "stream_event_id", "day_index", "stream_url", "server_url", "stream_key"]
_EVENT_SNAPSHOT_COLUMNS = [
    "id", "title", "start_date", "duration_days", "ffkm_admin_tournament_id",
    "ffkm_admin_rank", "content_url", "locked_by_user_id", "created_by_id",
    "created_at", "updated_at",
]
_USER_SNAPSHOT_COLUMNS = ["id", "email", "username", "is_active", "password_hash", "role"]


def _snapshot_packet(columns: list, rows: list) -> dict:
    return {"columns": columns, "rows": rows}


def _packets(current_fetch: list) -> dict:
    """Порядковый список пакетов (users, events, days, postcutoff_days —
    каждый снимок dict с columns/rows) → словарь по классам запросов."""
    keys = ["users", "events", "days", "postcutoff_days"]
    return {key: packet for key, packet in zip(keys, current_fetch)}


def _legacy_packets(legacy_fetch: list) -> dict:
    keys = ["users", "events", "days"]
    return {key: packet for key, packet in zip(keys, legacy_fetch)}


def _current_snapshot_packets() -> dict:
    """Снимки текущей базы для _FakeConn: SELECT * users/events/days + пост-cutoff."""
    return _packets(
        [
            _snapshot_packet(_USER_SNAPSHOT_COLUMNS, [("user-1", "op@example.com", "op", True, "hash", "admin")]),
            _snapshot_packet(
                _EVENT_SNAPSHOT_COLUMNS,
                [("ev-1", "Турнир", "2026-10-25", 1, None, None, None, None, None, "c", "u")],
            ),
            _snapshot_packet(_DAY_SNAPSHOT_COLUMNS, [("day-1", "ev-1", 1, "", "", "")]),
            _snapshot_packet(_DAY_SNAPSHOT_COLUMNS, []),
        ]
    )


def test_cli_dry_run_rolls_back_and_prints_only_counts(monkeypatch, capsys) -> None:
    # порядок запросов: load_inputs (users, events, days каждой базы), затем
    # snapshot_fingerprint текущей базы (SELECT * days, events, users,
    # пост-cutoff дни).
    legacy_fetch = [
        [("old-user", "op@example.com")],
        [("old-ev", "Турнир", "2026-10-25", 1, None, None, "old-user")],
        [("old-day", "old-ev", 1, "https://old/1", "rtmp://legacy", "secret")],
    ]
    conns, cli = _run_cli(
        monkeypatch,
        [
            "recovery_links_20261113",
            "--current-url",
            "postgresql://a/current",
            "--legacy-url",
            "postgresql://b/legacy",
        ],
        _current_snapshot_packets(),
        _legacy_packets(legacy_fetch),
    )
    cli.main()
    assert conns["current"].rolled_back is True
    assert conns["current"].committed is False
    # источник изолирован согласованным read-only снимком REPEATABLE READ:
    # отдельные SELECT-ы не должны видеть разные состояния legacy
    assert conns["legacy"].session == {
        "isolation_level": "REPEATABLE READ",
        "readonly": True,
        "autocommit": False,
    }
    assert conns["current"].session == {"isolation_level": "REPEATABLE READ", "autocommit": False}
    out = capsys.readouterr().out
    assert "plan_sha256=" in out
    assert "days_updated=1" in out
    assert "dry-run" in out
    # stdout не содержит URL, ключей и PII — только счётчики и хэш
    assert "https://old/1" not in out
    assert "rtmp://legacy" not in out
    assert "secret" not in out
    assert "op@example.com" not in out


def test_cli_apply_rejects_mismatched_plan_hash(monkeypatch, capsys) -> None:
    conns, cli = _run_cli(
        monkeypatch,
        [
            "recovery_links_20261113",
            "--current-url",
            "postgresql://a/current",
            "--legacy-url",
            "postgresql://b/legacy",
            "--apply",
            "--expected-plan-sha256",
            "0" * 64,
        ],
        {key: _snapshot_packet([], []) for key in ("users", "events", "days", "postcutoff_days")},
        {key: [] for key in ("users", "events", "days")},
    )
    with pytest.raises(SystemExit):
        cli.main()
    assert conns["current"].committed is False
    assert conns["current"].rolled_back is True
    # хэш не сошёлся — до записи дело не дошло: ни одного INSERT/UPDATE
    assert not any(text.startswith("INSERT") or text.startswith("UPDATE") for text, _ in conns["current"].executed)


def _apply_argv(sha: str) -> list[str]:
    return [
        "recovery_links_20261113",
        "--current-url",
        "postgresql://a/current",
        "--legacy-url",
        "postgresql://b/legacy",
        "--apply",
        "--expected-plan-sha256",
        sha,
    ]


def test_cli_apply_lock_precedes_any_current_snapshot_read(monkeypatch, capsys) -> None:
    # Регрессия (correction 2): в --apply блокировки обязаны быть первым
    # обращением к текущей базе — до schema-проверок и любых SELECT-ов:
    # снимок REPEATABLE READ фиксируется первым запросом, и чтение до LOCK
    # оставило бы невидимыми коммиты, случившиеся во время ожидания блокировки.
    legacy_fetch = [
        [("old-user", "op@example.com")],
        [("old-ev", "Турнир", "2026-10-25", 1, None, None, "old-user")],
        [("old-day", "old-ev", 1, "https://old/1", "rtmp://legacy", "secret")],
    ]
    conns, cli = _run_cli(monkeypatch, _apply_argv("0" * 64), _current_snapshot_packets(), _legacy_packets(legacy_fetch))
    with pytest.raises(SystemExit):
        cli.main()
    executed = [text for text, _ in conns["current"].executed]
    lock_pos = next(i for i, text in enumerate(executed) if text.startswith("LOCK TABLE"))
    first_read = next(
        i
        for i, text in enumerate(executed)
        if i != lock_pos and (text.lstrip().upper().startswith("SELECT") or "information_schema" in text)
    )
    assert lock_pos < first_read, "LOCK TABLE должен предшествовать любому чтению текущей базы"
    # LOCK на всех трёх таблицах, включая users (неизменный прообраз в хэше),
    # в детерминированном порядке
    lock_stmt = executed[lock_pos]
    assert "public.stream_days" in lock_stmt
    assert "public.stream_events" in lock_stmt
    assert "public.users" in lock_stmt
    assert lock_stmt.index("stream_days") < lock_stmt.index("stream_events") < lock_stmt.index("users")
    assert conns["current"].committed is False
    assert conns["current"].rolled_back is True


def test_cli_apply_happy_path_commits_and_writes(monkeypatch, capsys) -> None:
    # Сухой прогон даёт sha; apply с тем же sha под фиктивной базой с тем же
    # состоянием проходит до коммита и выполняет операции плана.
    legacy_fetch = [
        [("old-user", "op@example.com")],
        [("old-ev", "Турнир", "2026-10-25", 1, None, None, "old-user")],
        [("old-day", "old-ev", 1, "https://old/1", "rtmp://legacy", "secret")],
    ]
    dry_conns, cli = _run_cli(
        monkeypatch,
        [
            "recovery_links_20261113",
            "--current-url",
            "postgresql://a/current",
            "--legacy-url",
            "postgresql://b/legacy",
        ],
        _current_snapshot_packets(),
        _legacy_packets(legacy_fetch),
    )
    cli.main()
    out = capsys.readouterr().out
    sha = next(line.split("=", 1)[1] for line in out.splitlines() if line.startswith("plan_sha256="))
    assert sha != "0" * 64

    apply_conns, cli = _run_cli(monkeypatch, _apply_argv(sha), _current_snapshot_packets(), _legacy_packets(legacy_fetch))
    cli.main()
    assert apply_conns["current"].committed is True
    assert apply_conns["current"].rolled_back is False
    executed = [text for text, _ in apply_conns["current"].executed]
    lock_pos = next(i for i, text in enumerate(executed) if text.startswith("LOCK TABLE"))
    first_select = next(i for i, text in enumerate(executed) if text.lstrip().upper().startswith("SELECT"))
    assert lock_pos < first_select
    updates = [text for text in executed if text.startswith("UPDATE")]
    assert len(updates) == 1 and "stream_url" in updates[0]
    assert "apply: записано" in capsys.readouterr().out


def test_fetch_columns_qualifies_public_schema(monkeypatch) -> None:
    # Регрессия: SELECT использовал неqualified имя таблицы и мог читать
    # другую таблицу из search_path. Теперь идентификатор — public.<table>.
    import scripts.recovery_links_20261113 as cli

    captured = {}

    class _SQL:
        def __init__(self, s):
            self.s = s

        def format(self, **kwargs):
            captured.update(kwargs)
            # подставляем идентификаторы в шаблон: текст запроса должен
            # совпадать с реальным SQL, иначе классификация пакетов строк
            # по форме запроса не сработает.
            rendered = self.s
            for key, value in kwargs.items():
                rendered = rendered.replace("{" + key + "}", str(value))
            return _SQL(rendered)

        def join(self, other):
            return _SQL(", ".join(str(item) for item in other))

        def __str__(self):
            return self.s

    fake_psycopg2 = type(sys)("psycopg2")
    fake_sql = type(sys)("psycopg2.sql")
    fake_sql.SQL = _SQL
    fake_sql.Identifier = lambda *names: _SQL(".".join(str(n) for n in names))
    fake_psycopg2.sql = fake_sql
    monkeypatch.setitem(sys.modules, "psycopg2", fake_psycopg2)
    monkeypatch.setitem(sys.modules, "psycopg2.sql", fake_sql)
    # to_regclass в FakeCursor не потребляет пакет fetch_rows — первый (и
    # единственный) пакет уходит на сам SELECT.
    conn = _FakeConn({"days": [("row-1", "https://x", "ev-1", 1, "", "")]})
    rows = cli.fetch_columns(conn, "stream_days", ("id", "stream_url"))
    assert rows == [{"id": "row-1", "stream_url": "https://x"}]
    assert str(captured["table"]) == "public.stream_days"


def test_check_columns_requires_all_used_columns(monkeypatch) -> None:
    # Регрессия: preflight проверял лишь подмножество колонок. Теперь любая
    # отсутствующая колонка из набора, читаемого по имени из текущей базы, —
    # явная остановка до плана. Отпечаток (snapshot_fingerprint) читает строки
    # целиком (SELECT *), поэтому hardcoded fingerprint-поля больше не нужны,
    # а лишние колонки схемы (username, is_active, ffkm_admin_rank, ...) —
    # не причина для отказа.
    import scripts.recovery_links_20261113 as cli

    conn = _FakeConn(
        {
            "columns:users": [("id",), ("email",)],
            # stream_events без content_url: обязательная колонка плана
            # (EVENT_COLUMNS) — preflight обязан остановиться.
            "columns:stream_events": [
                ("id",),
                ("title",),
                ("start_date",),
                ("duration_days",),
                ("ffkm_admin_tournament_id",),
                ("created_by_id",),
            ],
            "columns:stream_days": [
                ("id",),
                ("stream_event_id",),
                ("day_index",),
                ("stream_url",),
                ("server_url",),
                ("stream_key",),
            ],
        }
    )
    with pytest.raises(SystemExit):
        cli.check_columns(conn, ("users", "stream_events", "stream_days"), cli.CURRENT_REQUIRED_COLUMNS)

    ok_conn = _FakeConn(
        {
            # полный набор текущей схемы, включая колонки вне чтения по имени:
            # preflight не должен отвергать совместимые схемы с доп. колонками
            "columns:users": [("id",), ("email",), ("username",), ("is_active",), ("password_hash",), ("role",)],
            "columns:stream_events": [
                ("id",),
                ("title",),
                ("start_date",),
                ("duration_days",),
                ("ffkm_admin_tournament_id",),
                ("ffkm_admin_rank",),
                ("content_url",),
                ("created_by_id",),
                ("locked_by_user_id",),
                ("created_at",),
                ("updated_at",),
            ],
            "columns:stream_days": [
                ("id",),
                ("stream_event_id",),
                ("day_index",),
                ("stream_url",),
                ("server_url",),
                ("stream_key",),
            ],
        }
    )
    cli.check_columns(ok_conn, ("users", "stream_events", "stream_days"), cli.CURRENT_REQUIRED_COLUMNS)


def test_check_columns_legacy_needs_only_plan_columns(monkeypatch) -> None:
    # Регрессия (correction 2): legacy-preflight требовал fingerprint-поля
    # (password_hash, role, locked_by_user_id, created_at, updated_at), которых
    # план никогда не читает из старой базы, — совместимые старые схемы
    # отвергались напрасно. Достаточно колонок, реально читаемых из legacy.
    import scripts.recovery_links_20261113 as cli

    legacy_conn = _FakeConn(
        {
            "columns:users": [("id",), ("email",)],
            "columns:stream_events": [
                ("id",),
                ("title",),
                ("start_date",),
                ("duration_days",),
                ("ffkm_admin_tournament_id",),
                ("content_url",),
                ("created_by_id",),
            ],
            "columns:stream_days": [
                ("id",),
                ("stream_event_id",),
                ("day_index",),
                ("stream_url",),
                ("server_url",),
                ("stream_key",),
            ],
        }
    )
    cli.check_columns(legacy_conn, ("users", "stream_events", "stream_days"), cli.LEGACY_REQUIRED_COLUMNS)

    # но обязательные колонки плана в legacy всё же нужны: без content_url —
    # останов (content_url-only ссылки невосстановимы иначе).
    legacy_no_content = _FakeConn(
        {
            "columns:users": [("id",), ("email",)],
            "columns:stream_events": [
                ("id",),
                ("title",),
                ("start_date",),
                ("duration_days",),
                ("ffkm_admin_tournament_id",),
                ("created_by_id",),
            ],
            "columns:stream_days": [
                ("id",),
                ("stream_event_id",),
                ("day_index",),
                ("stream_url",),
                ("server_url",),
                ("stream_key",),
            ],
        }
    )
    with pytest.raises(SystemExit):
        cli.check_columns(
            legacy_no_content, ("users", "stream_events", "stream_days"), cli.LEGACY_REQUIRED_COLUMNS
        )


def test_plan_sha256_independent_of_input_row_order() -> None:
    # Регрессия (correction 2): физический порядок строк входных SELECT-ов
    # (или перемешанные входные списки) не должен менять хэш плана — иначе
    # один и тот же набор данных давал бы разные «проверенные» хэши.
    current_users = [_user("u1", "a@example.com"), _user("u2", "b@example.com")]
    legacy_users = [_user("o1", "a@example.com"), _user("o2", "c@example.com")]
    current_events = [
        _event("live-1", start="2026-10-20", duration=2),
        _event("live-2", start="2026-10-25", duration=2, content_url=None),
    ]
    legacy_events = [
        _event("old-1", start="2026-10-20", duration=2),
        _event("old-2", start="2026-10-25", duration=2, content_url="https://disk/x"),
    ]
    current_days = [_day("d1", "live-1", 1), _day("d2", "live-1", 2), _day("d3", "live-2", 1)]
    legacy_days = [
        _day("o1", "old-1", 1, stream_url="https://old/1"),
        _day("o2", "old-1", 2, stream_url="https://old/2"),
        _day("o3", "old-2", 1, stream_url="https://old/3"),
    ]
    base = _plan(
        current_users=current_users,
        legacy_users=legacy_users,
        current_events=current_events,
        legacy_events=legacy_events,
        current_days=current_days,
        legacy_days=legacy_days,
    )
    sha_base = plan_sha256(base)
    # тот же набор строк в обратном (и произвольно перемешанном) порядке
    shuffled = _plan(
        current_users=list(reversed(current_users)),
        legacy_users=list(reversed(legacy_users)),
        current_events=list(reversed(current_events)),
        legacy_events=list(reversed(legacy_events)),
        current_days=[current_days[2], current_days[0], current_days[1]],
        legacy_days=[legacy_days[2], legacy_days[0], legacy_days[1]],
    )
    assert plan_sha256(shuffled) == sha_base
    # и на уровне плана: наборы операций совпадают независимо от порядка входа
    assert sorted(map(repr, shuffled.day_inserts + shuffled.day_updates)) == sorted(
        map(repr, base.day_inserts + base.day_updates)
    )


def test_content_only_same_tournament_and_title_but_incompatible_date_is_conflict() -> None:
    # Регрессия (correction 3): content-only ссылка с совпадающими tournament_id
    # и title, но несовместимой датой начала. Раньше планировщик вставлял новое
    # событие с тем же tournament_id: сухой прогон «успешен», а apply падал бы
    # на unique constraint и откатывал всю миграцию. Теперь — конфликт
    # идентичности до любой записи; чужое текущее событие гарантированно
    # не тронуто, потому что плана вообще нет.
    with pytest.raises(TournamentIdConflictError):
        _plan(
            current_events=[
                _event("live", title="Турнир", start="2026-10-25", duration=1, tournament_id=7, content_url=None)
            ],
            legacy_events=[
                _event(
                    "old",
                    title="Турнир",
                    start="2026-10-26",
                    duration=1,
                    tournament_id=7,
                    content_url="https://disk/old",
                )
            ],
            current_days=[_day("d1", "live", 1)],
            legacy_days=[_day("o1", "old", 1, stream_url="")],
        )


def test_content_only_same_tournament_incompatible_date_without_tournament_on_current() -> None:
    # Текущее событие без tournament_id: конфликта нет, content-only ссылка
    # восстанавливается отдельной вставкой (tournament_id текущей базы не занят).
    plan = _plan(
        current_events=[
            _event("live", title="Турнир", start="2026-10-25", duration=1, content_url=None)
        ],
        legacy_events=[
            _event(
                "old",
                title="Турнир",
                start="2026-10-26",
                duration=1,
                tournament_id=7,
                content_url="https://disk/old",
            )
        ],
        current_days=[_day("d1", "live", 1)],
        legacy_days=[_day("o1", "old", 1, stream_url="")],
    )
    assert plan.event_updates == []
    assert len(plan.event_inserts) == 1
    assert plan.event_inserts[0]["content_url"] == "https://disk/old"
    assert plan.event_inserts[0]["ffkm_admin_tournament_id"] == 7


def test_content_only_ambiguous_tournament_candidates_raise_before_writes() -> None:
    # Два текущих события с одним tournament_id и совместимыми датами —
    # неоднозначность для content-only ссылки: исключение до любых записей.
    with pytest.raises(AmbiguousMatchError):
        _plan(
            current_events=[
                _event("live-1", start="2026-10-25", duration=2, tournament_id=7),
                _event("live-2", start="2026-10-26", duration=2, tournament_id=7),
            ],
            legacy_events=[
                _event("old", start="2026-10-26", duration=2, tournament_id=7, content_url="https://disk/x")
            ],
            current_days=[_day("d1", "live-1", 1), _day("d2", "live-2", 1)],
            legacy_days=[_day("o1", "old", 1, stream_url="")],
        )


def _run_cli_with_schema(monkeypatch, argv, current_packets, legacy_packets):
    """Как _run_cli, но с настоящей check_columns: schema-пакеты обязаны
    присутствовать, и LOCK обязан предшествовать и information_schema-запросам."""
    import scripts.recovery_links_20261113 as cli

    conns = {"current": _FakeConn(current_packets), "legacy": _FakeConn(legacy_packets)}

    def fake_connect(url):
        return conns["current"] if "current" in url else conns["legacy"]

    fake_psycopg2 = type(sys)("psycopg2")
    fake_psycopg2.connect = fake_connect
    fake_sql = type(sys)("psycopg2.sql")

    class _FakeSQL:
        def __init__(self, s):
            self.s = s

        def format(self, **kwargs):
            rendered = self.s
            for key, value in kwargs.items():
                rendered = rendered.replace("{" + key + "}", str(value))
            return _FakeSQL(rendered)

        def join(self, other):
            return _FakeSQL(", ".join(str(item) for item in other))

        def __str__(self):
            return self.s

    fake_sql.SQL = _FakeSQL
    fake_sql.Identifier = lambda *names: _FakeSQL(".".join(str(n) for n in names))
    fake_psycopg2.sql = fake_sql
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setitem(sys.modules, "psycopg2", fake_psycopg2)
    monkeypatch.setitem(sys.modules, "psycopg2.sql", fake_sql)
    return conns, cli


_CURRENT_SCHEMA_PACKETS = {
    "columns:users": [("id",), ("email",), ("username",), ("is_active",), ("password_hash",), ("role",)],
    "columns:stream_events": [
        ("id",),
        ("title",),
        ("start_date",),
        ("duration_days",),
        ("ffkm_admin_tournament_id",),
        ("ffkm_admin_rank",),
        ("content_url",),
        ("created_by_id",),
        ("locked_by_user_id",),
        ("created_at",),
        ("updated_at",),
    ],
    "columns:stream_days": [
        ("id",),
        ("stream_event_id",),
        ("day_index",),
        ("stream_url",),
        ("server_url",),
        ("stream_key",),
    ],
}

_LEGACY_SCHEMA_PACKETS = {
    "columns:users": [("id",), ("email",)],
    "columns:stream_events": [
        ("id",),
        ("title",),
        ("start_date",),
        ("duration_days",),
        ("ffkm_admin_tournament_id",),
        ("content_url",),
        ("created_by_id",),
    ],
    "columns:stream_days": [
        ("id",),
        ("stream_event_id",),
        ("day_index",),
        ("stream_url",),
        ("server_url",),
        ("stream_key",),
    ],
}


def test_cli_apply_lock_precedes_schema_queries(monkeypatch, capsys) -> None:
    # Регрессия (correction 2): снимок REPEATABLE READ фиксируется первым
    # запросом транзакции, поэтому в --apply LOCK обязан предшествовать даже
    # information_schema-проверкам схемы — иначе коммит другой сессии во время
    # ожидания блокировки остался бы невидим для плана и хэша.
    legacy_fetch = [
        [("old-user", "op@example.com")],
        [("old-ev", "Турнир", "2026-10-25", 1, None, None, "old-user")],
        [("old-day", "old-ev", 1, "https://old/1", "rtmp://legacy", "secret")],
    ]
    current_packets = dict(_CURRENT_SCHEMA_PACKETS)
    current_packets.update(_current_snapshot_packets())
    legacy_packets = dict(_LEGACY_SCHEMA_PACKETS)
    legacy_packets.update(_legacy_packets(legacy_fetch))
    conns, cli = _run_cli_with_schema(monkeypatch, _apply_argv("0" * 64), current_packets, legacy_packets)
    with pytest.raises(SystemExit):
        cli.main()
    executed = [text for text, _ in conns["current"].executed]
    lock_pos = next(i for i, text in enumerate(executed) if text.startswith("LOCK TABLE"))
    schema_pos = next(i for i, text in enumerate(executed) if "information_schema" in text)
    first_select = next(i for i, text in enumerate(executed) if text.lstrip().upper().startswith("SELECT"))
    assert lock_pos < schema_pos, "LOCK TABLE должен предшествовать schema-проверкам текущей базы"
    assert lock_pos < first_select, "LOCK TABLE должен предшествовать любым SELECT-ам текущей базы"
    assert conns["current"].committed is False
    assert conns["current"].rolled_back is True


def test_pg_two_session_lock_snapshot_regression() -> None:
    # Двухсессионная регрессия на настоящем PostgreSQL. Сессия A (apply)
    # ждёт ACCESS EXCLUSIVE; сессия B, державшая блокировку, коммитит НОВОЕ
    # текущее событие с той же сигнатурой, что у события источника, прежде чем
    # A получит блокировку. Если бы снимок A был взят до LOCK (schema-проверкой
    # или SELECT-ом), план A не увидел бы его и вставил бы дубль события.
    # Протокол «LOCK до первого запроса» обязывает A увидеть коммит B, план
    # изменится относительно сухого прогона и apply откажется по хэшу.
    # Тест пропускается (SKIP, не PASS), если PostgreSQL/psycopg2 недоступны.
    import os

    try:
        import psycopg2  # noqa: F401
    except ImportError:
        pytest.skip("psycopg2 недоступен: двухсессионная PG-регрессия не запущена")
    dsn = os.environ.get("RECOVERY_TEST_PG_DSN", "")
    if not dsn:
        pytest.skip("RECOVERY_TEST_PG_DSN не задан: двухсессионная PG-регрессия не запущена")

    import scripts.recovery_links_20261113 as cli

    DDL = """
    DROP TABLE IF EXISTS public.stream_days;
    DROP TABLE IF EXISTS public.stream_events;
    DROP TABLE IF EXISTS public.users;
    CREATE TABLE public.users (
        id text PRIMARY KEY, email text, password_hash text, role text
    );
    CREATE TABLE public.stream_events (
        id text PRIMARY KEY, title text, start_date date, duration_days int,
        ffkm_admin_tournament_id int UNIQUE, ffkm_admin_rank text,
        content_url text,
        locked_by_user_id text, created_by_id text,
        created_at timestamp, updated_at timestamp
    );
    CREATE TABLE public.stream_days (
        id text PRIMARY KEY, stream_event_id text REFERENCES public.stream_events(id),
        day_index int, stream_url text, server_url text, stream_key text
    );
    INSERT INTO public.users VALUES ('u1', 'op@example.com', 'h', 'admin');
    """

    LEGACY_EVENTS = [
        {
            "id": "old-ev",
            "title": "Турнир",
            "start_date": "2026-10-25",
            "duration_days": 1,
            "ffkm_admin_tournament_id": None,
            "content_url": None,
            "created_by_id": None,
        }
    ]
    LEGACY_DAYS = [
        {
            "id": "old-day",
            "stream_event_id": "old-ev",
            "day_index": 1,
            "stream_url": "https://old/1",
            "server_url": "",
            "stream_key": "",
        }
    ]

    def build_inputs(conn) -> dict:
        return {
            "current_users": cli.fetch_columns(conn, "users", cli.USER_COLUMNS),
            "legacy_users": [],
            "current_events": cli.fetch_columns(conn, "stream_events", cli.EVENT_COLUMNS),
            "legacy_events": [dict(row) for row in LEGACY_EVENTS],
            "current_days": cli.fetch_columns(conn, "stream_days", cli.DAY_COLUMNS),
            "legacy_days": [dict(row) for row in LEGACY_DAYS],
        }

    setup_conn = psycopg2.connect(dsn)
    setup_conn.autocommit = True
    with setup_conn.cursor() as cur:
        cur.execute(DDL)
    setup_conn.close()

    # Сухой прогон: текущая база пуста — план вставляет old-ev и его день.
    dry = psycopg2.connect(dsn)
    dry.set_session(isolation_level="REPEATABLE READ", readonly=True, autocommit=False)
    cli.check_columns(dry, ("users", "stream_events", "stream_days"), cli.CURRENT_REQUIRED_COLUMNS)
    dry_plan = cli.build_plan_from(build_inputs(dry))
    dry_sha = cli.plan_sha256(dry_plan, {"current": cli.snapshot_fingerprint(dry), "legacy": {}})
    dry.rollback()
    dry.close()
    assert len(dry_plan.event_inserts) == 1

    # Apply-сессия A: блокируется на LOCK. Сессия B коммитит конкурирующее
    # текущее событие live-x с той же сигнатурой (title+start_date), что и у
    # old-ev, и освобождает блокировку.
    apply_conn = psycopg2.connect(dsn)
    apply_conn.set_session(isolation_level="REPEATABLE READ", autocommit=False)
    blocker = psycopg2.connect(dsn)
    blocker.autocommit = False
    blocker.cursor().execute("LOCK TABLE public.stream_days IN ACCESS EXCLUSIVE MODE")

    import threading

    lock_acquired = threading.Event()

    def acquire_lock() -> None:
        cli.lock_tables(apply_conn)
        lock_acquired.set()

    t = threading.Thread(target=acquire_lock)
    t.start()
    import time

    time.sleep(0.3)  # A точно ждёт LOCK
    with blocker.cursor() as cur:
        cur.execute(
            """
            INSERT INTO public.stream_events
                (id, title, start_date, duration_days, ffkm_admin_tournament_id,
                 content_url, locked_by_user_id, created_by_id, created_at, updated_at)
            VALUES ('live-x', 'Турнир', '2026-10-25', 1, NULL, NULL, NULL, 'u1', now(), now())
            """
        )
    blocker.commit()
    blocker.close()
    t.join(timeout=10)
    assert lock_acquired.is_set(), "apply-сессия не получила блокировку"

    # Снимок взят после LOCK: коммит B виден. live-x совпадает по сигнатуре с
    # old-ev — план строит перенос дня на live-x вместо вставки дубля, и хэш
    # обязан отличаться от сухого прогона (иначе drift незаметен).
    cli.check_columns(apply_conn, ("users", "stream_events", "stream_days"), cli.CURRENT_REQUIRED_COLUMNS)
    apply_plan = cli.build_plan_from(build_inputs(apply_conn))
    apply_sha = cli.plan_sha256(apply_plan, {"current": cli.snapshot_fingerprint(apply_conn), "legacy": {}})
    apply_conn.rollback()
    apply_conn.close()

    assert apply_plan.event_inserts == [], "дубль события не должен планироваться"
    assert len(apply_plan.day_inserts) == 1
    assert apply_plan.day_inserts[0]["stream_event_id"] == "live-x"
    assert apply_sha != dry_sha, "план обязан измениться после коммита конкурента"
