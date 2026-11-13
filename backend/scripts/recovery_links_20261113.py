"""Восстановление исторических публичных ссылок стриминга (recovery-links-20261113).

Отдельная database со старым дампом:

    sudo -u postgres createdb streaming_legacy
    sudo -u postgres pg_restore -d streaming_legacy /path/to/streaming.dump

Проверка без записи (только счётчики и хэш плана, без URL и PII):

    cd /opt/streaming/backend
    sudo -u streaming .venv/bin/python -m scripts.recovery_links_20261113 \\
        --current-url postgresql://streaming@/streaming \\
        --legacy-url postgresql://streaming@/streaming_legacy

Запись (после свежего бэкапа боевой базы и uploads/):

    sudo -u streaming .venv/bin/python -m scripts.recovery_links_20261113 \\
        --current-url postgresql://streaming@/streaming \\
        --legacy-url postgresql://streaming@/streaming_legacy \\
        --apply --expected-plan-sha256 <sha256 из сухого прогона>

Правила: backend/app/services/recovery_links_20261113.py.
Переносятся только публичные stream_url дней строго до 2026-11-01.
Пользователи, пароли, роли, ключи, серверы, блокировки, авторизация,
уведомления, сессии, назначения и аналитика не трогаются.

Протокол записи: в --apply блокировки ACCESS EXCLUSIVE (stream_days,
stream_events, users — в фиксированном порядке) выполняются до любого
другого запроса к текущей базе, так что снимок REPEATABLE READ берётся
уже после ожидания LOCK. Источник читается в REPEATABLE READ readonly.
Отпечаток перед записью — полные строки всех трёх таблиц (SELECT *):
хэш плана привязан к каждой колонке, пост-записной инвариант разрешает
отличия только в намеренно изменённых URL (stream_url дней плана,
content_url событий плана).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, datetime
from typing import Any
from uuid import UUID

from app.services.recovery_links_20261113 import (
    CUTOFF_DATE,
    CURRENT_REQUIRED_COLUMNS,
    DAY_COLUMNS,
    EVENT_COLUMNS,
    LEGACY_REQUIRED_COLUMNS,
    MIGRATION_VERSION,
    USER_COLUMNS,
    RecoveryPlan,
    build_recovery_plan,
)

CURRENT_TABLES = ("users", "stream_events", "stream_days")
LEGACY_TABLES = ("users", "stream_events", "stream_days")

ALLOWED_COLUMNS = {
    "users": USER_COLUMNS,
    "stream_events": EVENT_COLUMNS,
    "stream_days": DAY_COLUMNS,
}


def sync_url(url: str) -> str:
    return url.replace("postgresql+asyncpg://", "postgresql://", 1).replace(
        "postgres+asyncpg://", "postgresql://", 1
    )


def adapt(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, default=str)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    return value


def _canonical_row_list(rows: list[dict[str, Any]]) -> list[str]:
    """Канонический порядок строк плана: физический порядок SELECT-ов
    (или перемешанные входные списки) не должен менять хэш."""
    return sorted(json.dumps(row, ensure_ascii=False, sort_keys=True, default=str) for row in rows)


def plan_sha256(plan: RecoveryPlan, snapshots: dict[str, Any] | None = None) -> str:
    """SHA-256 плана, привязанный к полным снимкам источника и текущей базы.

    Снимок текущей базы — все колонки всех строк users/stream_events/
    stream_days: прообразы перезаписываемых URL входят в полные строки, и
    изменение любого поля любой строки между сухим прогоном и --apply меняет
    хэш — запись отклоняется. Списки операций канонизируются по содержимому:
    хэш не зависит от порядка строк.
    """
    payload = {
        "version": plan.version,
        "cutoff_date": plan.cutoff_date,
        "user_remap": plan.user_remap,
        "event_remap": plan.event_remap,
        "event_inserts": _canonical_row_list(plan.event_inserts),
        "event_updates": _canonical_row_list(plan.event_updates),
        "day_inserts": _canonical_row_list(plan.day_inserts),
        "day_updates": _canonical_row_list(plan.day_updates),
        "snapshots": snapshots or {},
    }
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def check_columns(conn: Any, tables: tuple[str, ...], required: dict[str, tuple[str, ...]]) -> None:
    """Preflight: public.<table> существует и содержит все колонки набора
    required, реально читаемые из ЭТОГО подключения (набор задан отдельно
    для текущей базы и для legacy)."""
    with conn.cursor() as cur:
        for table in tables:
            cur.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = %s
                ORDER BY ordinal_position
                """,
                (table,),
            )
            present = {row[0] for row in cur.fetchall()}
            if not present:
                raise SystemExit(f"public.{table}: таблица отсутствует; схема не соответствует ожиданиям")
            missing = [name for name in required[table] if name not in present]
            if missing:
                raise SystemExit(f"public.{table}: нет колонок {missing}; схема не соответствует ожиданиям")


def fetch_columns(conn: Any, table: str, columns: tuple[str, ...]) -> list[dict[str, Any]]:
    from psycopg2 import sql

    if table not in ALLOWED_COLUMNS or any(name not in ALLOWED_COLUMNS[table] for name in columns):
        raise SystemExit(f"public.{table}: запрошены колонки вне allowlist")
    # Детерминированный физический порядок строк: без ORDER BY один и тот же
    # набор строк мог вернуться в разном порядке, а порядок входных списков
    # входит в порядок операций плана.
    order_by = ("id",) if "id" in columns else columns
    query = sql.SQL("SELECT {cols} FROM {table} ORDER BY {order_by}").format(
        cols=sql.SQL(", ").join(sql.Identifier(name) for name in columns),
        table=sql.Identifier("public", table),
        order_by=sql.SQL(", ").join(sql.Identifier(name) for name in order_by),
    )
    with conn.cursor() as cur:
        cur.execute("SELECT to_regclass(%s)", (f"public.{table}",))
        if cur.fetchone()[0] is None:
            raise SystemExit(f"public.{table}: таблица отсутствует; схема не соответствует ожиданиям")
        cur.execute(query)
        rows = cur.fetchall()
        return [dict(zip(columns, row)) for row in rows]


def load_inputs(legacy_conn: Any, current_conn: Any) -> dict[str, list[dict[str, Any]]]:
    return {
        "current_users": fetch_columns(current_conn, "users", USER_COLUMNS),
        "legacy_users": fetch_columns(legacy_conn, "users", USER_COLUMNS),
        "current_events": fetch_columns(current_conn, "stream_events", EVENT_COLUMNS),
        "legacy_events": fetch_columns(legacy_conn, "stream_events", EVENT_COLUMNS),
        "current_days": fetch_columns(current_conn, "stream_days", DAY_COLUMNS),
        "legacy_days": fetch_columns(legacy_conn, "stream_days", DAY_COLUMNS),
    }


def build_plan_from(inputs: dict[str, list[dict[str, Any]]]) -> RecoveryPlan:
    return build_recovery_plan(
        current_users=inputs["current_users"],
        legacy_users=inputs["legacy_users"],
        current_events=inputs["current_events"],
        legacy_events=inputs["legacy_events"],
        current_days=inputs["current_days"],
        legacy_days=inputs["legacy_days"],
        cutoff=CUTOFF_DATE,
    )


def _fetch_snapshot(cur: Any) -> dict[str, Any]:
    """Все строки результата как dict по именам колонок (cur.description)."""
    columns = [desc[0] for desc in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return {"columns": columns, "rows": rows}


def snapshot_fingerprint(conn: Any) -> dict[str, Any]:
    """Полные канонические снимки ВСЕХ строк трёх таблиц (все колонки).

    Прообраз (до записи) обязан покрывать каждую колонку users/stream_events/
    stream_days — включая ffkm_admin_rank, username, is_active, server_url,
    stream_key и любые будущие поля, — иначе заявленная полная сохранность
    нецелевых строк и drift-проверка были бы неполными. Поэтому снимок —
    SELECT * (порядок колонок фиксирован ordinal_position схемы, строки —
    ORDER BY id), без списков колонок, которые можно забыть дополнить.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM public.stream_days ORDER BY id")
        days = _fetch_snapshot(cur)
        cur.execute("SELECT * FROM public.stream_events ORDER BY id")
        events = _fetch_snapshot(cur)
        cur.execute("SELECT * FROM public.users ORDER BY id")
        users = _fetch_snapshot(cur)
        cur.execute(
            """
            SELECT d.* FROM public.stream_days d
            WHERE (SELECT e.start_date FROM public.stream_events e
                   WHERE e.id = d.stream_event_id)
                  + (d.day_index - 1) >= %s
            ORDER BY d.id
            """,
            (CUTOFF_DATE,),
        )
        postcutoff_days = _fetch_snapshot(cur)
    return {
        "days": days,
        "events": events,
        "users": users,
        "postcutoff_days": postcutoff_days,
    }


def assert_postapply_invariant(
    before: dict[str, Any], after: dict[str, Any], plan: RecoveryPlan
) -> None:
    """Строки, существовавшие до миграции, не изменились, кроме намеренно
    мутированных URL-полей плана; новых пост-cutoff дней не появилось.

    Исключения строго по белому списку плана: stream_url только у дней из
    plan.day_updates и content_url только у событий из plan.event_updates.
    Любое другое отличие (включая server_url, stream_key, ffkm_admin_rank,
    username, is_active, title, даты) — отказ и откат.
    """
    allowed_day_url_changes = {str(row["id"]) for row in plan.day_updates}
    allowed_event_url_changes = {str(row["id"]) for row in plan.event_updates}
    allowed_field = {"days": "stream_url", "events": "content_url"}
    allowed_ids = {"days": allowed_day_url_changes, "events": allowed_event_url_changes}
    for key in ("days", "events", "users"):
        before_rows = {str(row["id"]): row for row in before[key]["rows"]}
        after_rows = {str(row["id"]): row for row in after[key]["rows"]}
        for row_id, row in before_rows.items():
            new_row = after_rows.get(row_id)
            if new_row is None:
                raise SystemExit(
                    f"нарушены инварианты: удалена защищённая строка {key}:{row_id}. "
                    "Транзакция откачена."
                )
            if new_row == row:
                continue
            field = allowed_field.get(key)
            if field is None or row_id not in allowed_ids[key]:
                raise SystemExit(
                    f"нарушены инварианты: изменилась защищённая строка {key}:{row_id}. "
                    "Транзакция откачена."
                )
            for column in row:
                if column == field:
                    continue
                if row[column] != new_row.get(column):
                    raise SystemExit(
                        f"нарушены инварианты: в строке {key}:{row_id} изменилось "
                        f"поле {column!r} (разрешено только {field!r}). "
                        "Транзакция откачена."
                    )
    before_postcutoff = {str(row["id"]) for row in before["postcutoff_days"]["rows"]}
    after_postcutoff = {str(row["id"]) for row in after["postcutoff_days"]["rows"]}
    if after_postcutoff != before_postcutoff:
        raise SystemExit(
            "нарушены инварианты: изменилось множество пост-cutoff дней. "
            "Транзакция откачена."
        )


def lock_tables(conn: Any) -> None:
    """ACCESS EXCLUSIVE на всех затрагиваемых таблицах до первого чтения.

    Блокировки обязаны быть первым обращением к текущей базе в транзакции
    REPEATABLE READ: снимок фиксируется первым запросом, и если до LOCK уже
    выполнились schema-проверки или SELECT-ы, строки, закоммиченные другой
    сессией во время ожидания блокировки, остались бы невидимы — план и хэш
    увидели бы устаревшее состояние. Порядок таблиц фиксирован (по имени)
    против взаимных блокировок. users блокируется тоже: его неизменный
    прообраз (email/password_hash/role) входит в хэш плана и проверяется
    перед коммитом.
    """
    with conn.cursor() as cur:
        cur.execute(
            "LOCK TABLE public.stream_days, public.stream_events, public.users "
            "IN ACCESS EXCLUSIVE MODE"
        )


def apply_plan(conn: Any, plan: RecoveryPlan) -> None:
    with conn.cursor() as cur:
        for row in plan.event_inserts:
            cur.execute(
                """
                INSERT INTO public.stream_events
                    (id, title, start_date, duration_days, ffkm_admin_tournament_id,
                     content_url, created_by_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    adapt(row["id"]),
                    adapt(row["title"]),
                    adapt(row["start_date"]),
                    adapt(row["duration_days"]),
                    adapt(row["ffkm_admin_tournament_id"]),
                    adapt(row["content_url"]),
                    adapt(row["created_by_id"]),
                ),
            )
        for row in plan.event_updates:
            cur.execute(
                "UPDATE public.stream_events SET content_url = %s WHERE id = %s",
                (adapt(row["content_url"]), adapt(row["id"])),
            )
        for row in plan.day_inserts:
            cur.execute(
                """
                INSERT INTO public.stream_days
                    (id, stream_event_id, day_index, stream_url, server_url, stream_key)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    adapt(row["id"]),
                    adapt(row["stream_event_id"]),
                    adapt(row["day_index"]),
                    adapt(row["stream_url"]),
                    adapt(row["server_url"]),
                    adapt(row["stream_key"]),
                ),
            )
        for row in plan.day_updates:
            cur.execute(
                "UPDATE public.stream_days SET stream_url = %s WHERE id = %s",
                (adapt(row["stream_url"]), adapt(row["id"])),
            )


def print_counts(plan: RecoveryPlan, sha: str) -> None:
    for name, count in plan.counts().items():
        print(f"{name}={count}")
    print(f"plan_sha256={sha}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Восстановить исторические публичные ссылки (recovery-links-20261113)"
    )
    parser.add_argument("--current-url", required=True, help="Боевая database")
    parser.add_argument("--legacy-url", required=True, help="Отдельная database со старым дампом")
    parser.add_argument("--apply", action="store_true", help="Записать план. Без флага только счётчики")
    parser.add_argument(
        "--expected-plan-sha256",
        default="",
        help="SHA-256 плана из проверенного сухого прогона; обязателен с --apply",
    )
    args = parser.parse_args()

    current_url = sync_url(args.current_url)
    legacy_url = sync_url(args.legacy_url)
    if current_url == legacy_url:
        raise SystemExit("legacy-url и текущая база совпадают. Старый дамп кладут в отдельную database")
    if args.apply and not args.expected_plan_sha256:
        raise SystemExit("--apply требует --expected-plan-sha256 из проверенного сухого прогона")

    import psycopg2

    legacy_conn = psycopg2.connect(legacy_url)
    current_conn = psycopg2.connect(current_url)
    try:
        # Источник — согласованный read-only снимок: отдельные SELECT-ы не
        # должны видеть разные состояния, если базу трогают параллельно.
        legacy_conn.set_session(isolation_level="REPEATABLE READ", readonly=True, autocommit=False)
        current_conn.set_session(isolation_level="REPEATABLE READ", autocommit=False)

        if args.apply:
            # Блокировки — до ЛЮБОГО запроса к текущей базе (включая
            # schema-проверки и SELECT-ы плана): снимок REPEATABLE READ
            # фиксируется первым запросом, и читать до LOCK нельзя.
            lock_tables(current_conn)

        check_columns(legacy_conn, LEGACY_TABLES, LEGACY_REQUIRED_COLUMNS)
        check_columns(current_conn, CURRENT_TABLES, CURRENT_REQUIRED_COLUMNS)

        inputs = load_inputs(legacy_conn, current_conn)
        plan = build_plan_from(inputs)
        # Хэш привязан к полным снимкам обеих баз: текущая — все колонки всех
        # строк users/stream_events/stream_days (прообразы URL включены, т.к.
        # входят в строки целиком), legacy — канонизированные строки входов.
        snapshots = {
            "current": snapshot_fingerprint(current_conn),
            "legacy": {
                "users": sorted(tuple(str(v) for v in (row["id"], row["email"])) for row in inputs["legacy_users"]),
                "events": sorted(
                    tuple(str(row.get(name)) for name in EVENT_COLUMNS) for row in inputs["legacy_events"]
                ),
                "days": sorted(
                    tuple(str(row.get(name)) for name in DAY_COLUMNS) for row in inputs["legacy_days"]
                ),
            },
        }
        sha = plan_sha256(plan, snapshots)
        print_counts(plan, sha)

        if not args.apply:
            current_conn.rollback()
            print("dry-run: база не изменена. Для записи добавьте --apply с --expected-plan-sha256.")
            return

        # План выше построен уже под блокировками на снимке, взятом после
        # LOCK: drift между сухим прогоном и записью меняет хэш, и apply
        # отказывается писать.
        if sha != args.expected_plan_sha256.strip().lower():
            current_conn.rollback()
            raise SystemExit(
                "план изменился относительно проверенного сухого прогона "
                "(drift или другой вход). Запись отменена."
            )

        before = snapshot_fingerprint(current_conn)
        apply_plan(current_conn, plan)
        after = snapshot_fingerprint(current_conn)
        assert_postapply_invariant(before, after, plan)
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
