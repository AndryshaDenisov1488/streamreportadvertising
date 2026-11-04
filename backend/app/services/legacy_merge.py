"""План слияния старой базы стриминга (дамп Beget) с текущей.

Текущие строки не удаляются и не затираются. Совпадение пользователя — по email:
пароль и роль, заданные после переезда, остаются. Совпадение мероприятия — по
ffkm_admin_tournament_id: пустые ссылки и ключи добираются из старой базы,
уже заполненные не трогаются. Сессии, токены сброса и приглашения из старой
базы не переносятся.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any


def is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False


def _key(value: Any) -> str:
    return str(value)


def _email(row: dict[str, Any]) -> str:
    return str(row.get("email") or "").strip().lower()


@dataclass
class MergePlan:
    user_inserts: list[dict[str, Any]] = field(default_factory=list)
    user_remap: dict[str, str] = field(default_factory=dict)
    user_fills: list[dict[str, Any]] = field(default_factory=list)
    event_inserts: list[dict[str, Any]] = field(default_factory=list)
    event_remap: dict[str, str] = field(default_factory=dict)
    event_fills: list[dict[str, Any]] = field(default_factory=list)
    duration_updates: list[dict[str, Any]] = field(default_factory=list)
    day_inserts: list[dict[str, Any]] = field(default_factory=list)
    day_fills: list[dict[str, Any]] = field(default_factory=list)
    assignment_inserts: list[dict[str, Any]] = field(default_factory=list)
    assignment_skipped: int = 0
    session_inserts: list[dict[str, Any]] = field(default_factory=list)
    session_skipped: int = 0
    mention_inserts: list[dict[str, Any]] = field(default_factory=list)
    adjustment_inserts: list[dict[str, Any]] = field(default_factory=list)
    adjustment_skipped: int = 0
    template_inserts: list[dict[str, Any]] = field(default_factory=list)
    logo_inserts: list[dict[str, Any]] = field(default_factory=list)
    event_logo_inserts: list[dict[str, Any]] = field(default_factory=list)
    checklist_inserts: list[dict[str, Any]] = field(default_factory=list)
    notification_inserts: list[dict[str, Any]] = field(default_factory=list)
    audit_inserts: list[dict[str, Any]] = field(default_factory=list)

    def counts(self) -> dict[str, int]:
        return {
            "users_insert": len(self.user_inserts),
            "users_linked_by_email": sum(
                1 for old, new in self.user_remap.items() if old != new
            ),
            "user_fields_filled": len(self.user_fills),
            "events_insert": len(self.event_inserts),
            "events_linked_by_tournament": sum(
                1 for old, new in self.event_remap.items() if old != new
            ),
            "event_fields_filled": len(self.event_fills),
            "duration_updates": len(self.duration_updates),
            "days_insert": len(self.day_inserts),
            "days_filled": len(self.day_fills),
            "assignments_insert": len(self.assignment_inserts),
            "assignments_kept_current": self.assignment_skipped,
            "sessions_insert": len(self.session_inserts),
            "sessions_skipped": self.session_skipped,
            "mentions_insert": len(self.mention_inserts),
            "adjustments_insert": len(self.adjustment_inserts),
            "adjustments_skipped": self.adjustment_skipped,
            "templates_insert": len(self.template_inserts),
            "logos_insert": len(self.logo_inserts),
            "event_logos_insert": len(self.event_logo_inserts),
            "checklists_insert": len(self.checklist_inserts),
            "notifications_insert": len(self.notification_inserts),
            "audit_insert": len(self.audit_inserts),
        }


def _blank_patch(current: dict[str, Any], legacy: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    patch: dict[str, Any] = {}
    for name in fields:
        if name not in legacy:
            continue
        if is_blank(current.get(name)) and not is_blank(legacy.get(name)):
            patch[name] = legacy[name]
    return patch


def build_merge_plan(
    *,
    current_users: list[dict[str, Any]],
    legacy_users: list[dict[str, Any]],
    current_events: list[dict[str, Any]],
    legacy_events: list[dict[str, Any]],
    current_days: list[dict[str, Any]],
    legacy_days: list[dict[str, Any]],
    current_assignments: list[dict[str, Any]],
    legacy_assignments: list[dict[str, Any]],
    current_sessions: list[dict[str, Any]],
    legacy_sessions: list[dict[str, Any]],
    current_mentions: list[dict[str, Any]],
    legacy_mentions: list[dict[str, Any]],
    current_adjustments: list[dict[str, Any]],
    legacy_adjustments: list[dict[str, Any]],
    current_templates: list[dict[str, Any]] | None = None,
    legacy_templates: list[dict[str, Any]] | None = None,
    current_logos: list[dict[str, Any]] | None = None,
    legacy_logos: list[dict[str, Any]] | None = None,
    current_event_logos: list[dict[str, Any]] | None = None,
    legacy_event_logos: list[dict[str, Any]] | None = None,
    current_checklists: list[dict[str, Any]] | None = None,
    legacy_checklists: list[dict[str, Any]] | None = None,
    current_notifications: list[dict[str, Any]] | None = None,
    legacy_notifications: list[dict[str, Any]] | None = None,
    current_audit: list[dict[str, Any]] | None = None,
    legacy_audit: list[dict[str, Any]] | None = None,
) -> MergePlan:
    plan = MergePlan()
    current_user_ids = {_key(row["id"]) for row in current_users}
    by_email = {_email(row): row for row in current_users if _email(row)}
    inserted_user_ids: set[str] = set()

    for row in legacy_users:
        email = _email(row)
        old_id = _key(row["id"])
        if not email:
            continue
        existing = by_email.get(email)
        if existing is not None:
            plan.user_remap[old_id] = _key(existing["id"])
            patch = _blank_patch(
                existing,
                row,
                ("first_name", "last_name", "phone", "telegram", "avatar_url"),
            )
            if patch:
                plan.user_fills.append({"id": _key(existing["id"]), **patch})
                existing.update(patch)
            continue
        new_row = dict(row)
        if old_id in current_user_ids or old_id in inserted_user_ids:
            new_id = str(uuid.uuid4())
            new_row["id"] = new_id
            plan.user_remap[old_id] = new_id
            inserted_user_ids.add(new_id)
        else:
            plan.user_remap[old_id] = old_id
            inserted_user_ids.add(old_id)
        new_row["email"] = email
        plan.user_inserts.append(new_row)
        by_email[email] = new_row

    known_users = current_user_ids | inserted_user_ids

    def resolve_user(user_id: Any) -> str | None:
        if user_id is None or is_blank(user_id):
            return None
        mapped = plan.user_remap.get(_key(user_id), _key(user_id))
        if mapped in known_users:
            return mapped
        return None

    current_event_ids = {_key(row["id"]) for row in current_events}
    by_tournament = {
        row["ffkm_admin_tournament_id"]: row
        for row in current_events
        if row.get("ffkm_admin_tournament_id") is not None
    }
    inserted_event_ids: set[str] = set()
    events_by_id = {_key(row["id"]): row for row in current_events}

    for row in legacy_events:
        old_id = _key(row["id"])
        if old_id in current_event_ids:
            plan.event_remap[old_id] = old_id
            continue
        tournament_id = row.get("ffkm_admin_tournament_id")
        if tournament_id is not None and tournament_id in by_tournament:
            target = by_tournament[tournament_id]
            target_id = _key(target["id"])
            plan.event_remap[old_id] = target_id
            patch = _blank_patch(target, row, ("content_url", "ffkm_admin_rank"))
            if patch:
                plan.event_fills.append({"id": target_id, **patch})
                target.update(patch)
            continue
        new_row = dict(row)
        if old_id in current_event_ids or old_id in inserted_event_ids:
            new_id = str(uuid.uuid4())
            new_row["id"] = new_id
        else:
            new_id = old_id
        plan.event_remap[old_id] = new_id
        new_row["id"] = new_id
        new_row["created_by_id"] = resolve_user(row.get("created_by_id"))
        new_row["locked_by_user_id"] = resolve_user(row.get("locked_by_user_id"))
        plan.event_inserts.append(new_row)
        inserted_event_ids.add(new_id)
        events_by_id[new_id] = new_row
        if tournament_id is not None:
            by_tournament[tournament_id] = new_row

    def resolve_event(event_id: Any) -> str | None:
        if event_id is None:
            return None
        mapped = plan.event_remap.get(_key(event_id), _key(event_id))
        if mapped in current_event_ids or mapped in inserted_event_ids:
            return mapped
        return None

    day_index: dict[tuple[str, int], dict[str, Any]] = {
        (_key(row["stream_event_id"]), int(row["day_index"])): row for row in current_days
    }
    day_ids = {_key(row["id"]) for row in current_days}
    max_day: dict[str, int] = {}
    for row in current_days:
        event_id = _key(row["stream_event_id"])
        max_day[event_id] = max(max_day.get(event_id, 0), int(row["day_index"]))

    for row in legacy_days:
        event_id = resolve_event(row.get("stream_event_id"))
        if event_id is None:
            continue
        key = (event_id, int(row["day_index"]))
        existing = day_index.get(key)
        if existing is not None:
            patch = _blank_patch(existing, row, ("stream_url", "server_url", "stream_key"))
            if patch:
                plan.day_fills.append({"id": _key(existing["id"]), **patch})
                existing.update(patch)
            continue
        new_row = dict(row)
        new_row["stream_event_id"] = event_id
        if _key(new_row["id"]) in day_ids:
            new_row["id"] = str(uuid.uuid4())
        day_ids.add(_key(new_row["id"]))
        plan.day_inserts.append(new_row)
        day_index[key] = new_row
        max_day[event_id] = max(max_day.get(event_id, 0), int(new_row["day_index"]))

    for event_id, top_day in max_day.items():
        event = events_by_id.get(event_id)
        if event is None:
            continue
        current_duration = int(event.get("duration_days") or 1)
        if top_day > current_duration:
            event["duration_days"] = top_day
            if event_id in inserted_event_ids:
                continue
            plan.duration_updates.append({"id": event_id, "duration_days": top_day})

    assignment_keys = {
        (_key(row["stream_event_id"]), int(row["day_index"])) for row in current_assignments
    }
    for row in legacy_assignments:
        event_id = resolve_event(row.get("stream_event_id"))
        operator_id = resolve_user(row.get("operator_id"))
        if event_id is None or operator_id is None:
            plan.assignment_skipped += 1
            continue
        key = (event_id, int(row["day_index"]))
        if key in assignment_keys:
            plan.assignment_skipped += 1
            continue
        new_row = dict(row)
        new_row["id"] = str(uuid.uuid4())
        new_row["stream_event_id"] = event_id
        new_row["operator_id"] = operator_id
        plan.assignment_inserts.append(new_row)
        assignment_keys.add(key)

    session_ids = {_key(row["id"]) for row in current_sessions}
    open_days = {
        (_key(row["stream_event_id"]), int(row["day_index"]))
        for row in current_sessions
        if row.get("ended_at") is None
    }
    kept_sessions = set(session_ids)
    for row in legacy_sessions:
        old_id = _key(row["id"])
        if old_id in session_ids:
            kept_sessions.add(old_id)
            continue
        event_id = resolve_event(row.get("stream_event_id"))
        operator_id = resolve_user(row.get("operator_id"))
        if event_id is None or operator_id is None:
            plan.session_skipped += 1
            continue
        if row.get("ended_at") is None and (event_id, int(row["day_index"])) in open_days:
            plan.session_skipped += 1
            continue
        new_row = dict(row)
        new_row["stream_event_id"] = event_id
        new_row["operator_id"] = operator_id
        plan.session_inserts.append(new_row)
        kept_sessions.add(old_id)
        session_ids.add(old_id)
        if new_row.get("ended_at") is None:
            open_days.add((event_id, int(new_row["day_index"])))

    mention_ids = {_key(row["id"]) for row in current_mentions}
    kept_mentions = set(mention_ids)
    for row in legacy_mentions:
        old_id = _key(row["id"])
        if old_id in mention_ids:
            kept_mentions.add(old_id)
            continue
        if _key(row.get("broadcast_session_id")) not in kept_sessions:
            continue
        plan.mention_inserts.append(dict(row))
        kept_mentions.add(old_id)
        mention_ids.add(old_id)

    adjustment_ids = {_key(row["id"]) for row in current_adjustments}
    for row in legacy_adjustments:
        if _key(row["id"]) in adjustment_ids:
            continue
        if _key(row.get("mention_id")) not in kept_mentions:
            continue
        editor_id = resolve_user(row.get("editor_user_id"))
        if editor_id is None:
            plan.adjustment_skipped += 1
            continue
        new_row = dict(row)
        new_row["editor_user_id"] = editor_id
        plan.adjustment_inserts.append(new_row)

    _copy_by_id(plan.template_inserts, current_templates or [], legacy_templates or [], rewrite=lambda row: {
        **row,
        "created_by_id": resolve_user(row.get("created_by_id")),
    })
    _copy_by_id(plan.logo_inserts, current_logos or [], legacy_logos or [])
    logo_ids = {_key(row["id"]) for row in (current_logos or [])} | {_key(row["id"]) for row in plan.logo_inserts}
    event_logo_pairs = {
        (_key(row["stream_event_id"]), _key(row["logo_id"])) for row in (current_event_logos or [])
    }
    for row in legacy_event_logos or []:
        event_id = resolve_event(row.get("stream_event_id"))
        logo_id = _key(row.get("logo_id"))
        if event_id is None or logo_id not in logo_ids:
            continue
        pair = (event_id, logo_id)
        if pair in event_logo_pairs:
            continue
        new_row = dict(row)
        new_row["id"] = str(uuid.uuid4())
        new_row["stream_event_id"] = event_id
        plan.event_logo_inserts.append(new_row)
        event_logo_pairs.add(pair)

    checklist_keys = {
        (_key(row["stream_event_id"]), _key(row["user_id"]), int(row["day_index"]))
        for row in (current_checklists or [])
    }
    for row in legacy_checklists or []:
        event_id = resolve_event(row.get("stream_event_id"))
        user_id = resolve_user(row.get("user_id"))
        if event_id is None or user_id is None:
            continue
        key = (event_id, user_id, int(row["day_index"]))
        if key in checklist_keys:
            continue
        new_row = dict(row)
        new_row["id"] = str(uuid.uuid4())
        new_row["stream_event_id"] = event_id
        new_row["user_id"] = user_id
        plan.checklist_inserts.append(new_row)
        checklist_keys.add(key)

    for row in legacy_notifications or []:
        user_id = resolve_user(row.get("user_id"))
        if user_id is None or _key(row["id"]) in {_key(item["id"]) for item in (current_notifications or [])}:
            continue
        new_row = dict(row)
        new_row["user_id"] = user_id
        plan.notification_inserts.append(new_row)

    current_audit_ids = {_key(row["id"]) for row in (current_audit or [])}
    for row in legacy_audit or []:
        if _key(row["id"]) in current_audit_ids:
            continue
        new_row = dict(row)
        if row.get("user_id") is not None:
            new_row["user_id"] = resolve_user(row.get("user_id"))
        plan.audit_inserts.append(new_row)

    return plan


def _copy_by_id(
    target: list[dict[str, Any]],
    current: list[dict[str, Any]],
    legacy: list[dict[str, Any]],
    *,
    rewrite: Any = None,
) -> None:
    seen = {_key(row["id"]) for row in current}
    for row in legacy:
        if _key(row["id"]) in seen:
            continue
        copied = rewrite(dict(row)) if rewrite else dict(row)
        target.append(copied)
        seen.add(_key(copied["id"]))
