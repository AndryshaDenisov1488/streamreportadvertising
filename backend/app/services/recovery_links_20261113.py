"""План восстановления исторических публичных ссылок стриминга (recovery-links-20261113).

Версионная миграция данных: достаёт из старой базы только публичные stream_url
дней с бизнес-датой строго раньше cutoff (2026-11-01) и переносит их в текущую
базу. Это НЕ общее слияние legacy: пользователи, пароли, роли, ключи, серверы,
блокировки, авторизация, уведомления, сессии, назначения и аналитика не трогаются.

Правила:
- пользователи: created_by_id старых событий переназначается по уникальному
  нормализованному непустому email на текущего пользователя; совпадение id —
  тоже валидный remap; без совпадения — None; вставок пользователей нет;
- события: совпадение по ffkm_admin_tournament_id при совместимой дате
  начала источника (та же дата или внутри окна текущего события);
  неоднозначность оценивается среди ВСЕХ совместимых кандидатов, до
  исключения уже занятых: занятый одним событием источника кандидат не
  делает «свободного» однозначным — исключение до записи; title не
  обязан совпадать (переимнованное событие с тем же verified tournament
  ID совместимо), но совпадение title никогда не перекрывает
  несовместимую дату; иначе точный id при подтверждённой идентичности
  (непустой title + start_date), иначе нормализованный title+start_date
  при уникальности; новое событие никогда не сохраняет
  ffkm_admin_tournament_id, уже занятый любым текущим событием
  (уникальный constraint): это конфликт идентичности, исключение до
  любой записи, а не отказ посреди apply;
- дни сопоставляются по фактической бизнес-дате (start_date + day_index - 1),
  а не по переиспользованному day_index источника; день источника, чья
  бизнес-дата не помещается в текущую длительность события, — явный конфликт,
  а не молчаливый сдвиг дат;
- дни: только старые дни с бизнес-датой < cutoff и непустым stream_url;
  текущие дни >= cutoff не меняются и не создаются;
- новые исторические события — только с qualifying-ссылками; content-only
  события, отсутствующие в текущей базе, тоже восстанавливаются с явными
  безопасными метаданными; id дней — детерминированный UUID5 (версия + id
  источника); коллизии id — отказ;
- server_url и stream_key новых дней — пустые строки;
- длительность новых событий обрезается по последнему историческому дню до
  cutoff; будущие дни не создаются; длительности существующих событий не меняются;
- content_url восстанавливается только если И событие-источник, И событие-
  назначение целиком до cutoff (в том числе content_url-only ссылки событий
  без qualifying stream_url); обрезка длительности нового события не
  разрешает перенос content_url с события, пересекающего cutoff.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any

MIGRATION_VERSION = "recovery-links-20261113"
CUTOFF_DATE = date(2026, 11, 1)

UUID_NAMESPACE = uuid.UUID("6f1e6f3a-4b3c-5d2e-9a1f-7c8d9e0f1a2b")

EVENT_COLUMNS = (
    "id",
    "title",
    "start_date",
    "duration_days",
    "ffkm_admin_tournament_id",
    "content_url",
    "created_by_id",
)
DAY_COLUMNS = ("id", "stream_event_id", "day_index", "stream_url", "server_url", "stream_key")
USER_COLUMNS = ("id", "email")

# Колонки, обязательные в текущей базе до построения плана: только колонки,
# читаемые по имени (SELECT-ы плана, включая stream_events.content_url).
# Отпечаток защищённых строк (snapshot_fingerprint) читает строки целиком
# (SELECT *: все колонки users/stream_events/stream_days), поэтому hardcoded
# списки fingerprint-колонок больше не нужны и любой drift любого поля
# (ffkm_admin_rank, username, is_active, server_url, stream_key, ...) меняет
# хэш плана; preflight заодно не отвергает совместимые схемы с дополнительными
# колонками.
CURRENT_REQUIRED_COLUMNS = {
    "users": USER_COLUMNS,
    "stream_events": EVENT_COLUMNS,
    "stream_days": DAY_COLUMNS,
}

# В legacy читаются только колонки плана: fingerprint-поля текущей базы
# (password_hash, role, locked_by_user_id, created_at, updated_at) там не
# требуются — иначе совместимые старые схемы отвергались бы напрасно.
LEGACY_REQUIRED_COLUMNS = {
    "users": USER_COLUMNS,
    "stream_events": EVENT_COLUMNS,
    "stream_days": DAY_COLUMNS,
}


class RecoveryLinksError(Exception):
    """Базовая ошибка планировщика восстановления ссылок."""


class AmbiguousMatchError(RecoveryLinksError):
    """Неоднозначная идентификация события или пользователя."""


class TournamentIdConflictError(RecoveryLinksError):
    """ffkm_admin_tournament_id уникален: вставка нового события с id турнира,
    уже занятым несовместимым текущим событием, нарушила бы unique constraint.
    Конфликт идентичности обязан быть найден планировщиком до любой записи."""


class IdCollisionError(RecoveryLinksError):
    """Детерминированный UUID5 дня конфликтует с существующим id."""


class DateMappingConflictError(RecoveryLinksError):
    """Бизнес-дата исторического дня несовместима с датами текущего события."""


def is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False


def _key(value: Any) -> str:
    return str(value)


def _to_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    text = str(value).strip()
    if not text:
        return None
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def _email(row: dict[str, Any]) -> str:
    return str(row.get("email") or "").strip().lower()


def _norm_title(value: Any) -> str:
    return " ".join(str(value or "").casefold().replace("ё", "е").split())


def business_date(start_date: Any, day_index: Any) -> date | None:
    """Бизнес-дата дня: start_date + (day_index - 1). day_index — с 1."""
    start = _to_date(start_date)
    if start is None:
        return None
    try:
        index = int(day_index)
    except (TypeError, ValueError):
        return None
    if index < 1:
        return None
    return start + timedelta(days=index - 1)


def day_index_for_business_date(start_date: Any, day_date: Any) -> int | None:
    """day_index (с 1) внутри события с датой start_date для бизнес-даты day_date."""
    start = _to_date(start_date)
    target = _to_date(day_date)
    if start is None or target is None:
        return None
    offset = (target - start).days
    if offset < 0:
        return None
    return offset + 1


def deterministic_day_id(source_event_id: Any, source_day_id: Any) -> str:
    name = f"{MIGRATION_VERSION}:{_key(source_event_id)}:{_key(source_day_id)}"
    return str(uuid.uuid5(UUID_NAMESPACE, name))


def _event_signature(row: dict[str, Any]) -> tuple[str, str] | None:
    title = _norm_title(row.get("title"))
    start = _to_date(row.get("start_date"))
    if not title or start is None:
        return None
    return title, start.isoformat()


def _duration_days(row: dict[str, Any]) -> int:
    try:
        return max(int(row.get("duration_days") or 1), 1)
    except (TypeError, ValueError):
        return 1


def _event_window(row: dict[str, Any]) -> tuple[date, date] | None:
    start = _to_date(row.get("start_date"))
    if start is None:
        return None
    return start, start + timedelta(days=_duration_days(row) - 1)


def _event_entirely_before_cutoff(row: dict[str, Any], cutoff: date) -> bool:
    window = _event_window(row)
    return window is not None and window[1] < cutoff


def _compatible_start(legacy_start: date | None, current: dict[str, Any]) -> bool:
    """Дата начала источника совместима с текущим событием: та же дата или
    внутри его окна [start_date, start_date + duration_days - 1]."""
    if legacy_start is None:
        return False
    window = _event_window(current)
    if window is None:
        return False
    return window[0] <= legacy_start <= window[1]


@dataclass
class RecoveryPlan:
    version: str = MIGRATION_VERSION
    cutoff_date: str = CUTOFF_DATE.isoformat()
    user_remap: dict[str, str] = field(default_factory=dict)
    event_remap: dict[str, str] = field(default_factory=dict)
    event_inserts: list[dict[str, Any]] = field(default_factory=list)
    event_updates: list[dict[str, Any]] = field(default_factory=list)
    day_inserts: list[dict[str, Any]] = field(default_factory=list)
    day_updates: list[dict[str, Any]] = field(default_factory=list)
    skipped_events: int = 0
    skipped_days: int = 0

    def counts(self) -> dict[str, int]:
        return {
            "users_linked_by_email": len(self.user_remap),
            "events_linked": sum(1 for old, new in self.event_remap.items() if old != new),
            "events_insert": len(self.event_inserts),
            "event_fields_updated": len(self.event_updates),
            "days_insert": len(self.day_inserts),
            "days_updated": len(self.day_updates),
            "events_skipped_no_qualifying_links": self.skipped_events,
            "days_skipped_not_qualifying": self.skipped_days,
        }

    def has_changes(self) -> bool:
        return bool(self.event_inserts or self.event_updates or self.day_inserts or self.day_updates)


def build_recovery_plan(
    *,
    current_users: list[dict[str, Any]],
    legacy_users: list[dict[str, Any]],
    current_events: list[dict[str, Any]],
    legacy_events: list[dict[str, Any]],
    current_days: list[dict[str, Any]],
    legacy_days: list[dict[str, Any]],
    cutoff: date = CUTOFF_DATE,
) -> RecoveryPlan:
    plan = RecoveryPlan(cutoff_date=cutoff.isoformat())

    by_email: dict[str, dict[str, Any]] = {}
    for row in current_users:
        email = _email(row)
        if not email:
            continue
        if email in by_email:
            raise AmbiguousMatchError(f"email {email!r} встречается у нескольких текущих пользователей")
        by_email[email] = row

    for row in legacy_users:
        email = _email(row)
        if not email:
            continue
        existing = by_email.get(email)
        if existing is not None:
            old_id = _key(row["id"])
            new_id = _key(existing["id"])
            # Совпадение id — тоже валидный remap: resolve_user не должен
            # терять создателя, когда email совпал и id совпадают.
            plan.user_remap[old_id] = new_id

    def resolve_user(user_id: Any) -> str | None:
        if user_id is None or is_blank(user_id):
            return None
        return plan.user_remap.get(_key(user_id))

    current_event_ids = {_key(row["id"]) for row in current_events}
    current_by_id = {_key(row["id"]): row for row in current_events}
    by_tournament: dict[Any, list[dict[str, Any]]] = {}
    for row in current_events:
        tournament_id = row.get("ffkm_admin_tournament_id")
        if tournament_id is not None:
            by_tournament.setdefault(tournament_id, []).append(row)
    by_signature: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in current_events:
        signature = _event_signature(row)
        if signature is not None:
            by_signature.setdefault(signature, []).append(row)

    claimed_current_ids: set[str] = set()
    event_remap: dict[str, str] = {}

    def identify_event(legacy_row: dict[str, Any]) -> dict[str, Any] | None:
        old_id = _key(legacy_row["id"])
        tournament_id = legacy_row.get("ffkm_admin_tournament_id")
        legacy_start = _to_date(legacy_row.get("start_date"))
        candidates: list[dict[str, Any]] = []
        if tournament_id is not None:
            # Совпадение по tournament_id требует совместимой даты начала
            # источника: та же дата или внутри окна текущего события.
            # title не обязан совпадать — переименованное событие с тем же
            # verified tournament ID совместимо; но совпадение title никогда
            # не перекрывает несовместимую дату (чужое событие не затирается).
            # Неоднозначность оценивается среди ВСЕХ совместимых кандидатов,
            # до исключения уже занятых: если совместимых кандидатов два, а
            # один занят другим событием источника, «свободный» всё равно не
            # выбирается молча — идентичность неоднозначна, исключение до записей.
            compatible = [
                current
                for current in by_tournament.get(tournament_id, [])
                if _compatible_start(legacy_start, current)
            ]
            if len(compatible) > 1:
                raise AmbiguousMatchError(
                    f"ffkm_admin_tournament_id={tournament_id!r} неоднозначен среди текущих событий"
                )
            if len(compatible) == 1:
                current = compatible[0]
                if _key(current["id"]) in claimed_current_ids:
                    raise AmbiguousMatchError(
                        f"текущее событие с ffkm_admin_tournament_id={tournament_id!r} "
                        "уже занято другим событием источника"
                    )
                candidates = compatible
        if not candidates and old_id in current_event_ids:
            # Точный id — только при подтверждённой идентичности (title+start_date).
            # Пустая сигнатура (пустой title или дата) идентичность не доказывает:
            # два None не считаются равными «доказательствами».
            current = current_by_id[old_id]
            current_sig = _event_signature(current)
            legacy_sig = _event_signature(legacy_row)
            if current_sig is not None and current_sig == legacy_sig:
                if old_id in claimed_current_ids:
                    raise AmbiguousMatchError(
                        f"текущее событие {old_id} уже занято другим событием источника"
                    )
                event_remap[old_id] = old_id
                claimed_current_ids.add(old_id)
                return current
            raise AmbiguousMatchError(
                f"старый id {old_id} занят текущим событием с другой идентичностью"
            )
        if not candidates:
            signature = _event_signature(legacy_row)
            if signature is not None:
                # Как и для tournament_id: неоднозначность — среди всех
                # совпадающих по сигнатуре строк, до фильтра занятых. Один
                # совпадающий кандидат, уже занятый другим событием источника,
                # — исключение, а не повод молча выбирать оставшегося.
                matches = by_signature.get(signature, [])
                if len(matches) > 1:
                    raise AmbiguousMatchError(
                        f"сигнатура {signature!r} неоднозначна среди текущих событий"
                    )
                if len(matches) == 1:
                    current = matches[0]
                    if _key(current["id"]) in claimed_current_ids:
                        raise AmbiguousMatchError(
                            f"текущее событие с сигнатурой {signature!r} уже занято "
                            "другим событием источника"
                        )
                    current_tournament = current.get("ffkm_admin_tournament_id")
                    if (
                        tournament_id is None
                        or current_tournament is None
                        or current_tournament == tournament_id
                    ):
                        candidates = matches
        if len(candidates) == 1:
            current = candidates[0]
            event_remap[old_id] = _key(current["id"])
            claimed_current_ids.add(_key(current["id"]))
            return current
        return None

    legacy_event_by_id = {_key(row["id"]): row for row in legacy_events}
    qualifying_days: dict[str, list[dict[str, Any]]] = {}
    for row in legacy_days:
        event_id = _key(row.get("stream_event_id"))
        legacy_event = legacy_event_by_id.get(event_id)
        if legacy_event is None:
            plan.skipped_days += 1
            continue
        day_date = business_date(legacy_event.get("start_date"), row.get("day_index"))
        if day_date is None or day_date >= cutoff:
            plan.skipped_days += 1
            continue
        if is_blank(row.get("stream_url")):
            plan.skipped_days += 1
            continue
        qualifying_days.setdefault(event_id, []).append(row)

    current_day_index: dict[tuple[str, int], dict[str, Any]] = {}
    for row in current_days:
        current_day_index[(_key(row["stream_event_id"]), int(row["day_index"]))] = row
    existing_day_ids = {_key(row["id"]) for row in current_days}
    planned_day_ids: set[str] = set()

    def plan_day_insert(new_id: str, event_id: str, day_index: int, stream_url: str) -> dict[str, Any]:
        if new_id in existing_day_ids or new_id in planned_day_ids:
            raise IdCollisionError(f"коллизия детерминированного id дня {new_id}")
        planned_day_ids.add(new_id)
        return {
            "id": new_id,
            "stream_event_id": event_id,
            "day_index": day_index,
            "stream_url": stream_url,
            "server_url": "",
            "stream_key": "",
        }

    def content_url_update(current: dict[str, Any], legacy_row: dict[str, Any]) -> dict[str, Any] | None:
        """content_url — только если целиком до cutoff и источник, и назначение."""
        if not _event_entirely_before_cutoff(current, cutoff):
            return None
        if not _event_entirely_before_cutoff(legacy_row, cutoff):
            return None
        if is_blank(legacy_row.get("content_url")):
            return None
        if str(current.get("content_url") or "") == str(legacy_row["content_url"]):
            return None
        return {"id": _key(current["id"]), "content_url": str(legacy_row["content_url"])}

    def plan_matched_days(
        current: dict[str, Any], legacy_row: dict[str, Any], days: list[dict[str, Any]]
    ) -> None:
        """Переносит дни на matched-событие строго по фактической бизнес-дате."""
        current_id = _key(current["id"])
        current_start = _to_date(current.get("start_date"))
        current_duration = _duration_days(current)
        for row in days:
            source_date = business_date(legacy_row.get("start_date"), row.get("day_index"))
            day_index = day_index_for_business_date(current_start, source_date)
            if day_index is None or day_index > current_duration:
                raise DateMappingConflictError(
                    f"исторический день с бизнес-датой {source_date} не помещается в окно "
                    f"текущего события {current_id} ({current_start} + {current_duration} дн.); "
                    "молчаливый сдвиг дат запрещён"
                )
            existing = current_day_index.get((current_id, day_index))
            if existing is not None:
                if str(existing.get("stream_url") or "") != str(row["stream_url"]):
                    plan.day_updates.append(
                        {"id": _key(existing["id"]), "stream_url": str(row["stream_url"])}
                    )
                continue
            new_id = deterministic_day_id(_key(legacy_row["id"]), row["id"])
            plan.day_inserts.append(
                plan_day_insert(new_id, current_id, day_index, str(row["stream_url"]))
            )

    def plan_new_event(legacy_event: dict[str, Any], days: list[dict[str, Any]]) -> None:
        old_event_id = _key(legacy_event["id"])
        new_event_id = old_event_id
        if new_event_id in current_event_ids or new_event_id in claimed_current_ids:
            raise AmbiguousMatchError(f"нельзя вставить событие {new_event_id}: id занят")
        # ffkm_admin_tournament_id уникален в текущей базе (models/stream.py).
        # Новое событие, сохраняющее id турнира, уже занятый несовместимым по
        # датам текущим событием, на apply упало бы на unique constraint и
        # откатило бы всю миграцию — конфликт идентичности обязан быть найден
        # планировщиком до любой записи (сухой прогон тоже падает, не только apply).
        tournament_id = legacy_event.get("ffkm_admin_tournament_id")
        if tournament_id is not None and by_tournament.get(tournament_id):
            raise TournamentIdConflictError(
                f"нельзя вставить событие {new_event_id}: ffkm_admin_tournament_id="
                f"{tournament_id!r} уже занят текущим событием "
                f"{_key(by_tournament[tournament_id][0]['id'])!r} с несовместимой датой"
            )
        start = _to_date(legacy_event.get("start_date"))
        if days:
            max_index = max(int(row["day_index"]) for row in days)
            last_day_date = business_date(legacy_event.get("start_date"), max_index)
            duration = max_index
            if last_day_date is not None and start is not None:
                duration = max(1, (last_day_date - start).days + 1)
        else:
            # content-only событие без qualifying-дней: длительность обрезается
            # по последнему дню целиком до cutoff, чтобы не создавать будущее.
            duration = _duration_days(legacy_event)
            if start is not None:
                duration = min(duration, max(1, (cutoff - start).days))
        new_event = {
            "id": new_event_id,
            "title": str(legacy_event.get("title") or ""),
            "start_date": start,
            "duration_days": duration,
            "ffkm_admin_tournament_id": legacy_event.get("ffkm_admin_tournament_id"),
            "content_url": None,
            "created_by_id": resolve_user(legacy_event.get("created_by_id")),
        }
        if _event_entirely_before_cutoff(legacy_event, cutoff) and not is_blank(
            legacy_event.get("content_url")
        ):
            new_event["content_url"] = str(legacy_event["content_url"])
        plan.event_inserts.append(new_event)
        event_remap[old_event_id] = new_event_id
        claimed_current_ids.add(new_event_id)
        for row in days:
            new_id = deterministic_day_id(old_event_id, row["id"])
            plan.day_inserts.append(
                plan_day_insert(new_id, new_event_id, int(row["day_index"]), str(row["stream_url"]))
            )

    for legacy_event in legacy_events:
        old_event_id = _key(legacy_event["id"])
        days = qualifying_days.get(old_event_id, [])
        if not days:
            # qualifying stream_url нет; content_url-only историческую ссылку
            # учитываем, только если она вообще восстановима (непустая и событие
            # целиком до cutoff) — иначе событие не идентифицируем и пропускаем.
            legacy_start = _to_date(legacy_event.get("start_date"))
            if (
                legacy_start is not None
                and not is_blank(legacy_event.get("content_url"))
                and _event_signature(legacy_event) is not None
            ):
                current = identify_event(legacy_event)
                if current is not None:
                    update = content_url_update(current, legacy_event)
                    if update is not None:
                        plan.event_updates.append(update)
                        continue
                elif _event_entirely_before_cutoff(legacy_event, cutoff):
                    # content-only историческое событие, отсутствующее в текущей
                    # базе: восстанавливаем ссылку новым событием с явными
                    # безопасными метаданными (server_url/stream_key пустые,
                    # created_by — по email-remap, длительность обрезана).
                    # Источник пересекает cutoff — content_url не восстановим,
                    # событие пропускается целиком, а не вставляется пустым.
                    plan_new_event(legacy_event, [])
                    continue
            plan.skipped_events += 1
            continue
        current = identify_event(legacy_event)
        if current is not None:
            plan_matched_days(current, legacy_event, days)
            update = content_url_update(current, legacy_event)
            if update is not None:
                plan.event_updates.append(update)
            continue

        plan_new_event(legacy_event, days)

    plan.event_remap = event_remap
    return plan
