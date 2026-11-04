from app.services.legacy_merge import build_merge_plan


def test_same_email_keeps_current_password_and_remaps_old_user() -> None:
    plan = build_merge_plan(
        current_users=[{"id": "new-user", "email": "Op@Example.com", "password_hash": "new", "phone": None, "first_name": "Анна"}],
        legacy_users=[{"id": "old-user", "email": "op@example.com", "password_hash": "old", "phone": "+79990000000", "first_name": "Старое"}],
        current_events=[],
        legacy_events=[],
        current_days=[],
        legacy_days=[],
        current_assignments=[],
        legacy_assignments=[],
        current_sessions=[],
        legacy_sessions=[],
        current_mentions=[],
        legacy_mentions=[],
        current_adjustments=[],
        legacy_adjustments=[],
    )
    assert plan.user_inserts == []
    assert plan.user_remap["old-user"] == "new-user"
    assert plan.user_fills == [{"id": "new-user", "phone": "+79990000000"}]


def test_new_email_is_inserted_with_the_old_id() -> None:
    plan = build_merge_plan(
        current_users=[],
        legacy_users=[{"id": "old-user", "email": "old@example.com"}],
        current_events=[],
        legacy_events=[],
        current_days=[],
        legacy_days=[],
        current_assignments=[],
        legacy_assignments=[],
        current_sessions=[],
        legacy_sessions=[],
        current_mentions=[],
        legacy_mentions=[],
        current_adjustments=[],
        legacy_adjustments=[],
    )
    assert plan.user_inserts[0]["id"] == "old-user"
    assert plan.user_inserts[0]["email"] == "old@example.com"


def test_same_tournament_keeps_filled_stream_key_and_fills_blank_url() -> None:
    plan = build_merge_plan(
        current_users=[{"id": "user", "email": "a@example.com"}],
        legacy_users=[{"id": "user", "email": "a@example.com"}],
        current_events=[{"id": "live", "ffkm_admin_tournament_id": 15, "duration_days": 1, "content_url": None, "ffkm_admin_rank": None}],
        legacy_events=[{"id": "old", "ffkm_admin_tournament_id": 15, "duration_days": 2, "content_url": "https://disk", "ffkm_admin_rank": "all_russian", "created_by_id": "user"}],
        current_days=[{"id": "day-live", "stream_event_id": "live", "day_index": 1, "stream_url": "", "server_url": "rtmp://live", "stream_key": "kept"}],
        legacy_days=[{"id": "day-old", "stream_event_id": "old", "day_index": 1, "stream_url": "https://watch", "server_url": "rtmp://old", "stream_key": "old-key"}],
        current_assignments=[{"id": "as-live", "stream_event_id": "live", "day_index": 1, "operator_id": "user"}],
        legacy_assignments=[{"id": "as-old", "stream_event_id": "old", "day_index": 1, "operator_id": "user"}],
        current_sessions=[],
        legacy_sessions=[],
        current_mentions=[],
        legacy_mentions=[],
        current_adjustments=[],
        legacy_adjustments=[],
    )
    assert plan.event_inserts == []
    assert plan.event_remap["old"] == "live"
    assert plan.event_fills == [{"id": "live", "content_url": "https://disk", "ffkm_admin_rank": "all_russian"}]
    assert plan.day_inserts == []
    assert plan.day_fills == [{"id": "day-live", "stream_url": "https://watch"}]
    assert plan.assignment_inserts == []
    assert plan.assignment_skipped == 1


def test_manual_event_links_to_legacy_by_title_and_date() -> None:
    plan = build_merge_plan(
        current_users=[],
        legacy_users=[],
        current_events=[{"id": "live", "title": "Кубок  Москвы", "start_date": "2026-11-20", "duration_days": 1, "ffkm_admin_tournament_id": None, "content_url": None, "ffkm_admin_rank": None}],
        legacy_events=[{"id": "old", "title": "кубок москвы", "start_date": "2026-11-20", "duration_days": 1, "ffkm_admin_tournament_id": 77, "content_url": None, "ffkm_admin_rank": "all_russian"}],
        current_days=[],
        legacy_days=[],
        current_assignments=[],
        legacy_assignments=[],
        current_sessions=[],
        legacy_sessions=[],
        current_mentions=[],
        legacy_mentions=[],
        current_adjustments=[],
        legacy_adjustments=[],
    )
    assert plan.event_inserts == []
    assert plan.event_remap["old"] == "live"
    assert plan.event_fills == [{"id": "live", "ffkm_admin_rank": "all_russian", "ffkm_admin_tournament_id": 77}]


def test_missing_day_is_added_and_duration_grows() -> None:
    plan = build_merge_plan(
        current_users=[],
        legacy_users=[],
        current_events=[{"id": "live", "ffkm_admin_tournament_id": 3, "duration_days": 1}],
        legacy_events=[{"id": "old", "ffkm_admin_tournament_id": 3, "duration_days": 2}],
        current_days=[{"id": "d1", "stream_event_id": "live", "day_index": 1, "stream_url": "u", "server_url": "s", "stream_key": "k"}],
        legacy_days=[
            {"id": "old-d1", "stream_event_id": "old", "day_index": 1, "stream_url": "", "server_url": "", "stream_key": ""},
            {"id": "old-d2", "stream_event_id": "old", "day_index": 2, "stream_url": "u2", "server_url": "s2", "stream_key": "k2"},
        ],
        current_assignments=[],
        legacy_assignments=[],
        current_sessions=[],
        legacy_sessions=[],
        current_mentions=[],
        legacy_mentions=[],
        current_adjustments=[],
        legacy_adjustments=[],
    )
    assert len(plan.day_inserts) == 1
    assert plan.day_inserts[0]["stream_event_id"] == "live"
    assert plan.day_inserts[0]["day_index"] == 2
    assert plan.duration_updates == [{"id": "live", "duration_days": 2}]


def test_open_legacy_session_is_skipped_when_the_day_is_already_on_air() -> None:
    plan = build_merge_plan(
        current_users=[{"id": "op", "email": "op@example.com"}],
        legacy_users=[{"id": "old-op", "email": "op@example.com"}],
        current_events=[{"id": "live", "ffkm_admin_tournament_id": 9, "duration_days": 1}],
        legacy_events=[{"id": "old", "ffkm_admin_tournament_id": 9, "duration_days": 1}],
        current_days=[],
        legacy_days=[],
        current_assignments=[],
        legacy_assignments=[],
        current_sessions=[{"id": "live-session", "stream_event_id": "live", "day_index": 1, "operator_id": "op", "ended_at": None}],
        legacy_sessions=[{"id": "old-session", "stream_event_id": "old", "day_index": 1, "operator_id": "old-op", "ended_at": None}],
        current_mentions=[],
        legacy_mentions=[{"id": "old-mention", "broadcast_session_id": "old-session", "original_offset_sec": 1, "adjusted_offset_sec": 1}],
        current_adjustments=[],
        legacy_adjustments=[],
    )
    assert plan.session_inserts == []
    assert plan.session_skipped == 1
    assert plan.mention_inserts == []


def test_finished_legacy_session_and_mention_are_copied() -> None:
    plan = build_merge_plan(
        current_users=[{"id": "op", "email": "op@example.com"}],
        legacy_users=[{"id": "old-op", "email": "op@example.com"}],
        current_events=[],
        legacy_events=[{"id": "old-event", "ffkm_admin_tournament_id": 4, "duration_days": 1, "created_by_id": "old-op"}],
        current_days=[],
        legacy_days=[],
        current_assignments=[],
        legacy_assignments=[],
        current_sessions=[],
        legacy_sessions=[{"id": "old-session", "stream_event_id": "old-event", "day_index": 1, "operator_id": "old-op", "ended_at": "2026-10-01T12:00:00"}],
        current_mentions=[],
        legacy_mentions=[{"id": "old-mention", "broadcast_session_id": "old-session", "original_offset_sec": 5, "adjusted_offset_sec": 5}],
        current_adjustments=[],
        legacy_adjustments=[],
    )
    assert plan.event_inserts[0]["id"] == "old-event"
    assert plan.event_inserts[0]["created_by_id"] == "op"
    assert plan.session_inserts[0]["operator_id"] == "op"
    assert plan.mention_inserts[0]["id"] == "old-mention"
