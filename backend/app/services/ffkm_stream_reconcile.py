"""One-off, date-based reconciliation. Never changes metadata or ingest credentials."""
from __future__ import annotations

import hashlib
import json
from datetime import date
from urllib.parse import urlsplit


def public_url(value):
    value = str(value or "").strip()
    if not value:
        return ""
    if any(character.isspace() or ord(character) < 32 for character in value):
        raise ValueError("invalid public URL")
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("invalid public URL")
    return value


def plan_hash(plan):
    raw = json.dumps(plan, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def require_reviewed_plan(document, reviewed_hash):
    digest = plan_hash(document)
    if digest != reviewed_hash:
        raise ValueError("Reviewed plan no longer matches: rerun dry-run and review")
    return digest


def build_plan(events, tournaments):
    """Inputs are public snapshots; reject an entire event on ambiguous input."""
    grouped = {}
    for item in tournaments:
        grouped.setdefault(str(item.get("id")), []).append(item)
    changes, skipped, push_targets, conflicts = [], [], [], 0
    for event in sorted(events, key=lambda row: row["id"]):
        tid = event.get("tournament_id")
        candidates = grouped.get(str(tid), []) if tid is not None else []
        reason = None
        if len(candidates) != 1:
            reason = "missing_or_ambiguous_tournament"
        else:
            item = candidates[0]
            try:
                start = date.fromisoformat(event["start_date"])
                duration = int(event["duration_days"])
                if str(item.get("start_date", ""))[:10] != start.isoformat():
                    raise ValueError("start_date_mismatch")
                schedule = item.get("online_stream_schedule")
                if isinstance(schedule, str):
                    schedule = json.loads(schedule) if schedule.strip() else []
                if schedule is not None and not isinstance(schedule, list):
                    raise ValueError("invalid_schedule")
                incoming = {}
                if schedule:
                    for row in schedule:
                        day = date.fromisoformat(str(row.get("stream_date") or ""))
                        idx = (day - start).days + 1
                        if not 1 <= idx <= duration:
                            raise ValueError("date_out_of_range")
                        if idx in incoming:
                            raise ValueError("ambiguous_schedule")
                        incoming[idx] = public_url(row.get("online_stream_url"))
                else:
                    # Department's legacy UI maps physical lines to days, including holes.
                    scalar = str(item.get("online_stream_url") or "")
                    lines = scalar.replace("\r\n", "\n").replace("\r", "\n").split("\n")
                    if len(lines) > duration:
                        raise ValueError("legacy_out_of_range")
                    incoming = {i: public_url(value) for i, value in enumerate(lines, 1)}
                existing = {int(day["day_index"]): day["stream_url"] for day in event["days"]}
                if len(existing) != len(event["days"]) or any(not 1 <= idx <= duration for idx in existing):
                    raise ValueError("invalid_local_days")
                updates = []
                event_conflicts = 0
                for idx, url in sorted(incoming.items()):
                    if not url:
                        continue
                    old = existing.get(idx, "")
                    if old != url:
                        event_conflicts += bool(old)
                        updates.append({"day_index": idx, "stream_url": url})
                conflicts += event_conflicts
                merged = {**existing, **{idx: url for idx, url in incoming.items() if url}}
                if any(merged.values()):
                    push_targets.append(event["id"])
                if updates:
                    changes.append({"snapshot": event, "updates": updates})
            except (ValueError, TypeError, KeyError, AttributeError):
                reason = "invalid_dates_schedule_or_url"
        if reason:
            skipped.append({"event_id": event["id"], "reason": reason})
    return {"version": 1, "changes": changes, "push_targets": push_targets, "skipped": skipped,
            "summary": {"events": len(events), "changed_events": len(changes),
                        "changed_days": sum(len(row["updates"]) for row in changes),
                        "conflicts": conflicts, "skipped": len(skipped),
                        "push_targets": len(push_targets)}}
