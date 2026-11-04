"""Слияние дампа стриминга с Beget в текущую базу.

Старую базу сначала восстанавливают в ОТДЕЛЬНУЮ database, не в боевую:

    sudo -u postgres createdb streaming_legacy
    sudo -u postgres pg_restore -d streaming_legacy /path/to/streaming.dump

Проверка без записи:

    cd /opt/streaming/backend
    sudo -u streaming .venv/bin/python -m scripts.merge_legacy_streaming \\
        --legacy-url postgresql://streaming@/streaming_legacy

Запись (после свежего бэкапа боевой базы):

    sudo -u streaming .venv/bin/python -m scripts.merge_legacy_streaming \\
        --legacy-url postgresql://streaming@/streaming_legacy --apply

Правила: backend/app/services/legacy_merge.py.
Файлы логотипов из старого uploads/ копировать отдельно и не затирать уже существующие.
Токены входа, сброс пароля и приглашения из старой базы не переносятся.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from psycopg2.extras import Json, RealDictCursor

from app.services.legacy_merge import MergePlan, build_merge_plan

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

TABLES = (
    "users",
    "stream_events",
    "stream_days",
    "stream_day_assignments",
    "broadcast_sessions",
    "sponsor_mentions",
    "mention_adjustments",
    "stream_event_templates",
    "logos",
    "stream_event_logos",
    "broadcast_checklists",
    "notifications",
    "audit_logs",
)

ENUM_CASTS = {("users", "role"): "userrole"}


def sync_url(url: str) -> str:
    return url.replace("postgresql+asyncpg://", "postgresql://", 1).replace(
        "postgres+asyncpg://", "postgresql://", 1
    )


def current_url_from_env() -> str:
    raw = os.getenv("DATABASE_URL_SYNC") or os.getenv("DATABASE_URL") or ""
    url = sync_url(raw.strip())
    if not url:
        raise SystemExit("Не задан DATABASE_URL_SYNC или --current-url")
    return url


def fetch_table(conn: Any, table: str) -> list[dict[str, Any]]:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT to_regclass(%s)", (f"public.{table}",))
        if cur.fetchone()["to_regclass"] is None:
            return []
        cur.execute(f"SELECT * FROM {table}")
        return [dict(row) for row in cur.fetchall()]


def table_columns(conn: Any, table: str) -> list[str]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position
            """,
            (table,),
        )
        return [row[0] for row in cur.fetchall()]


def adapt(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return Json(value)
    return value


def insert_rows(cur: Any, table: str, rows: list[dict[str, Any]], columns: list[str]) -> None:
    allowed = set(columns)
    for row in rows:
        present = [name for name in columns if name in row and name in allowed]
        if not present:
            continue
        values = [adapt(row[name]) for name in present]
        placeholders = []
        for name in present:
            cast = ENUM_CASTS.get((table, name))
            placeholders.append("%s::" + cast if cast else "%s")
        collist = ", ".join(present)
        sql = f"INSERT INTO {table} ({collist}) VALUES ({', '.join(placeholders)}) ON CONFLICT (id) DO NOTHING"
        cur.execute(sql, values)


def apply_fills(cur: Any, table: str, rows: list[dict[str, Any]], columns: set[str]) -> None:
    for row in rows:
        fields = [name for name in row if name != "id" and name in columns]
        if not fields:
            continue
        assignments = ", ".join(f"{name} = %s" for name in fields)
        cur.execute(
            f"UPDATE {table} SET {assignments} WHERE id = %s",
            [adapt(row[name]) for name in fields] + [row["id"]],
        )


def apply_plan(conn: Any, plan: MergePlan) -> None:
    columns = {table: table_columns(conn, table) for table in TABLES}
    with conn.cursor() as cur:
        insert_rows(cur, "users", plan.user_inserts, columns["users"])
        apply_fills(cur, "users", plan.user_fills, set(columns["users"]))
        insert_rows(cur, "stream_event_templates", plan.template_inserts, columns["stream_event_templates"])
        insert_rows(cur, "stream_events", plan.event_inserts, columns["stream_events"])
        apply_fills(cur, "stream_events", plan.event_fills, set(columns["stream_events"]))
        apply_fills(cur, "stream_events", plan.duration_updates, set(columns["stream_events"]))
        insert_rows(cur, "stream_days", plan.day_inserts, columns["stream_days"])
        apply_fills(cur, "stream_days", plan.day_fills, set(columns["stream_days"]))
        insert_rows(cur, "stream_day_assignments", plan.assignment_inserts, columns["stream_day_assignments"])
        insert_rows(cur, "broadcast_sessions", plan.session_inserts, columns["broadcast_sessions"])
        insert_rows(cur, "sponsor_mentions", plan.mention_inserts, columns["sponsor_mentions"])
        insert_rows(cur, "mention_adjustments", plan.adjustment_inserts, columns["mention_adjustments"])
        insert_rows(cur, "logos", plan.logo_inserts, columns["logos"])
        insert_rows(cur, "stream_event_logos", plan.event_logo_inserts, columns["stream_event_logos"])
        insert_rows(cur, "broadcast_checklists", plan.checklist_inserts, columns["broadcast_checklists"])
        insert_rows(cur, "notifications", plan.notification_inserts, columns["notifications"])
        insert_rows(cur, "audit_logs", plan.audit_inserts, columns["audit_logs"])


def load_plan(legacy_conn: Any, current_conn: Any) -> MergePlan:
    def both(table: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        return fetch_table(current_conn, table), fetch_table(legacy_conn, table)

    current_users, legacy_users = both("users")
    current_events, legacy_events = both("stream_events")
    current_days, legacy_days = both("stream_days")
    current_assignments, legacy_assignments = both("stream_day_assignments")
    current_sessions, legacy_sessions = both("broadcast_sessions")
    current_mentions, legacy_mentions = both("sponsor_mentions")
    current_adjustments, legacy_adjustments = both("mention_adjustments")
    current_templates, legacy_templates = both("stream_event_templates")
    current_logos, legacy_logos = both("logos")
    current_event_logos, legacy_event_logos = both("stream_event_logos")
    current_checklists, legacy_checklists = both("broadcast_checklists")
    current_notifications, legacy_notifications = both("notifications")
    current_audit, legacy_audit = both("audit_logs")
    return build_merge_plan(
        current_users=current_users,
        legacy_users=legacy_users,
        current_events=current_events,
        legacy_events=legacy_events,
        current_days=current_days,
        legacy_days=legacy_days,
        current_assignments=current_assignments,
        legacy_assignments=legacy_assignments,
        current_sessions=current_sessions,
        legacy_sessions=legacy_sessions,
        current_mentions=current_mentions,
        legacy_mentions=legacy_mentions,
        current_adjustments=current_adjustments,
        legacy_adjustments=legacy_adjustments,
        current_templates=current_templates,
        legacy_templates=legacy_templates,
        current_logos=current_logos,
        legacy_logos=legacy_logos,
        current_event_logos=current_event_logos,
        legacy_event_logos=legacy_event_logos,
        current_checklists=current_checklists,
        legacy_checklists=legacy_checklists,
        current_notifications=current_notifications,
        legacy_notifications=legacy_notifications,
        current_audit=current_audit,
        legacy_audit=legacy_audit,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Слить дамп стриминга Beget с текущей базой")
    parser.add_argument("--legacy-url", required=True, help="Отдельная database со старым дампом")
    parser.add_argument("--current-url", default="", help="Боевая database; по умолчанию из .env")
    parser.add_argument("--apply", action="store_true", help="Записать план. Без флага только счётчики")
    args = parser.parse_args()

    import psycopg2

    current_url = sync_url(args.current_url) if args.current_url else current_url_from_env()
    legacy_url = sync_url(args.legacy_url)
    if current_url == legacy_url:
        raise SystemExit("legacy-url и текущая база совпадают. Старый дамп кладут в отдельную database")

    legacy_conn = psycopg2.connect(legacy_url)
    current_conn = psycopg2.connect(current_url)
    try:
        legacy_conn.set_session(readonly=True)
        plan = load_plan(legacy_conn, current_conn)
        for name, count in plan.counts().items():
            print(f"{name}={count}")
        if not args.apply:
            print("dry-run: база не изменена. Для записи добавьте --apply после свежего бэкапа.")
            return
        apply_plan(current_conn, plan)
        current_conn.commit()
        print("apply: записано")
    except Exception:
        current_conn.rollback()
        raise
    finally:
        legacy_conn.close()
        current_conn.close()


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
