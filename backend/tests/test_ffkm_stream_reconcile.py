from copy import deepcopy

import pytest

from app.services.ffkm_stream_reconcile import build_plan, plan_hash, require_reviewed_plan


def event():
    return {"id": "event", "tournament_id": 1, "start_date": "2026-11-01", "duration_days": 3,
            "days": [{"id": "day1", "day_index": 1, "stream_url": "https://old.test/1"},
                     {"id": "day3", "day_index": 3, "stream_url": "https://old.test/3"}]}


def tournament(**kwargs):
    return {"id": 1, "start_date": "2026-11-01", **kwargs}


def test_department_wins_and_local_holes_preserved():
    source = event()
    plan = build_plan([source], [tournament(online_stream_url="https://new.test/1\nhttps://new.test/2\n")])
    assert plan["summary"]["conflicts"] == 1
    assert plan["changes"][0]["updates"] == [
        {"day_index": 1, "stream_url": "https://new.test/1"},
        {"day_index": 2, "stream_url": "https://new.test/2"}]
    assert source == event()


def test_dated_schedule_overrides_scalar_and_is_order_independent():
    import json
    rows = [{"stream_date": "2026-11-02", "online_stream_url": "https://new.test/2"}]
    plan = build_plan([event()], [tournament(online_stream_schedule=json.dumps(rows), online_stream_url="https://wrong.test")])
    assert plan["changes"][0]["updates"] == [{"day_index": 2, "stream_url": "https://new.test/2"}]


def test_legacy_blank_lines_do_not_shift_dates():
    plan = build_plan([event()], [tournament(online_stream_url="\nhttps://new.test/2")])
    assert plan["changes"][0]["updates"][0]["day_index"] == 2


def test_reject_invalid_and_ambiguous_whole_event():
    cases = [tournament(start_date="2026-11-02"),
             tournament(online_stream_url="javascript:alert(1)"),
             tournament(online_stream_url="https://user:secret@example.test"),
             tournament(online_stream_url="https://example.test/with space"),
             tournament(online_stream_url="\n\n\nhttps://new.test"),
             tournament(online_stream_schedule=[{"stream_date": "2026-11-04"}]),
             tournament(online_stream_schedule=[{"stream_date": "2026-11-01"}] * 2)]
    for item in cases:
        result = build_plan([event()], [item])
        assert not result["changes"] and result["summary"]["skipped"] == 1


def test_missing_or_duplicate_id_never_matches_by_title():
    assert build_plan([event()], [])["summary"]["skipped"] == 1
    assert build_plan([event()], [tournament(), tournament()])["summary"]["skipped"] == 1


def test_repeat_is_unchanged_and_snapshot_hash_detects_change():
    original = event()
    item = tournament(online_stream_url="https://old.test/1")
    assert build_plan([original], [item])["changes"] == []
    changed = deepcopy(original)
    changed["days"][0]["stream_url"] = "https://concurrent.test"
    assert plan_hash(original) != plan_hash(changed)
    with pytest.raises(ValueError, match="no longer matches"):
        require_reviewed_plan(changed, plan_hash(original))
    assert require_reviewed_plan(original, plan_hash(original)) == plan_hash(original)


@pytest.mark.asyncio
async def test_cli_push_includes_streaming_only_and_retry_after_apply():
    from scripts.reconcile_ffkm_streams import push_plan
    from uuid import uuid4

    local = event()
    local["id"] = str(uuid4())
    calls = []

    async def push(session, event_id):
        calls.append(str(event_id))
        return True

    unchanged = build_plan([local], [tournament()])
    assert not unchanged["changes"]
    await push_plan(None, unchanged, push=push)
    assert calls == [local["id"]]

    item = tournament(online_stream_url="https://new.test/1")
    before = build_plan([local], [item])
    assert before["changes"]
    local["days"][0]["stream_url"] = "https://new.test/1"  # committed apply
    retry = build_plan([local], [item])
    assert not retry["changes"]
    await push_plan(None, retry, push=push)
    assert calls == [local["id"], local["id"]]


@pytest.mark.asyncio
async def test_cli_push_excludes_skipped_and_reports_failure_after_commit():
    from scripts.reconcile_ffkm_streams import push_plan
    from uuid import uuid4

    local = event()
    local["id"] = str(uuid4())
    skipped = build_plan([local], [tournament(start_date="2026-11-03")])
    assert skipped["push_targets"] == []
    calls = []

    async def fail(session, event_id):
        calls.append(event_id)
        return False

    await push_plan(None, skipped, push=fail)
    assert calls == []
    with pytest.raises(RuntimeError, match="DB committed; 1 Department pushes failed"):
        await push_plan(None, build_plan([local], [tournament()]), push=fail)
