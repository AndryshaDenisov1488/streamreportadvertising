"""Run from backend: python -m scripts.reconcile_ffkm_streams --help."""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from sqlalchemy import select

from app.models.stream import StreamDay, StreamEvent
from app.services.ffkm_stream_reconcile import build_plan, plan_hash, require_reviewed_plan


async def snapshot(session, *, lock=False):
    query = select(StreamEvent).order_by(StreamEvent.id)
    days_query = select(StreamDay).order_by(StreamDay.stream_event_id, StreamDay.day_index)
    if lock:
        query = query.with_for_update()
        days_query = days_query.with_for_update()
    events = (await session.execute(query)).scalars().all()
    days = (await session.execute(days_query)).scalars().all()
    return [{"id": str(event.id), "tournament_id": event.ffkm_admin_tournament_id,
             "start_date": event.start_date.isoformat(), "duration_days": event.duration_days,
             "days": [{"id": str(day.id), "day_index": day.day_index,
                       "stream_url": day.stream_url}
                      for day in days if day.stream_event_id == event.id]} for event in events]


async def push_plan(session, plan, *, push=None):
    """Push all eligible merged events, including unchanged events and retries."""
    from uuid import UUID
    if push is None:
        from app.services.ffkm_stream_push import push_stream_urls_to_ffkm_admin
        push = push_stream_urls_to_ffkm_admin
    failed = 0
    for event_id in plan["push_targets"]:
        failed += not await push(session, UUID(event_id))
    if failed:
        raise RuntimeError(f"DB committed; {failed} Department pushes failed")


async def main(args):
    from app.db.session import AsyncSessionLocal
    if args.input:
        source = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
        items = source.get("items") if isinstance(source, dict) else source
    else:
        from app.services.ffkm_admin_client import FfkmAdminClient
        items = await FfkmAdminClient().iter_all_tournaments()
    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        raise ValueError("Expected a tournament list or {items: [...]} export")
    if args.apply and (not args.reviewed_plan_hash or not args.backup_verified):
        raise ValueError("Apply requires --reviewed-plan-hash and --backup-verified")
    async with AsyncSessionLocal() as session:
        async with session.begin():
            current = await snapshot(session, lock=args.apply)
            plan = build_plan(current, items)
            # Bind review to the entire public DB snapshot, including unchanged/skipped rows.
            document = {"plan": plan, "snapshot": current}
            digest = plan_hash(document)
            if args.apply:
                require_reviewed_plan(document, args.reviewed_plan_hash)
                from uuid import UUID
                for change in plan["changes"]:
                    event_id = UUID(change["snapshot"]["id"])
                    for update in change["updates"]:
                        query = select(StreamDay).where(StreamDay.stream_event_id == event_id,
                                                        StreamDay.day_index == update["day_index"])
                        day = (await session.execute(query)).scalar_one_or_none()
                        if day is None:
                            day = StreamDay(stream_event_id=event_id, day_index=update["day_index"],
                                            server_url="", stream_key="")
                            session.add(day)
                        day.stream_url = update["stream_url"]
        if args.output:
            # Explicit output only: public links and snapshots, never ingest credentials.
            Path(args.output).write_text(json.dumps({**document, "hash": digest}, ensure_ascii=False,
                                                   indent=2), encoding="utf-8")
        print(json.dumps({"applied": args.apply, "hash": digest, **plan["summary"]}))
        if args.push:
            await push_plan(session, plan)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="One-off public URL merge; default dry-run. Department wins per date.")
    parser.add_argument("--input", help="Department JSON export; omit to read configured Integration API")
    parser.add_argument("--output", help="Explicit plan JSON destination outside Git; contains public URLs")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--reviewed-plan-hash")
    parser.add_argument("--backup-verified", action="store_true", help="Operator confirms fresh verified backup and restore path")
    parser.add_argument("--push", action="store_true", help="Push all eligible merged events AFTER DB commit, including unchanged retry targets; requires --apply")
    arguments = parser.parse_args()
    if arguments.push and not arguments.apply:
        parser.error("--push requires --apply")
    asyncio.run(main(arguments))
