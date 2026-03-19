from datetime import date, datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog
from app.models.enums import UserRole
from app.models.stream import StreamEvent
from app.models.user import User
from app.models.platform_extra import Notification
from app.services.stats_service import get_operator_stats_overview


async def build_dashboard_summary(session: AsyncSession, *, user: User) -> dict[str, Any]:
    role = user.role.value
    cards: list[dict[str, Any]] = []

    if user.role == UserRole.OPERATOR:
        n_streams = await session.scalar(select(func.count()).select_from(StreamEvent))
        cards.append({"key": "events", "title": "Мероприятий в системе", "value": int(n_streams or 0), "hint": "Все запланированные эфиры"})
        today = date.today()
        try:
            overview = await get_operator_stats_overview(session, stat_date=today)
            my_mentions = 0
            for o in overview.operators:
                if o.operator_id == user.id:
                    my_mentions = o.mentions_week
                    break
            cards.append(
                {
                    "key": "mentions_week",
                    "title": "Ваши упоминания за неделю (МСК)",
                    "value": my_mentions,
                    "hint": f"Всего по операторам за неделю: {overview.total_mentions_week}",
                }
            )
        except Exception:
            cards.append({"key": "mentions_today", "title": "Упоминания сегодня", "value": "—", "hint": "Статистика недоступна"})
        return {"role": role, "title": "Пульт оператора", "cards": cards}

    if user.role == UserRole.STREAM_MANAGER:
        n_streams = await session.scalar(select(func.count()).select_from(StreamEvent))
        cards.append({"key": "streams", "title": "Мероприятий", "value": int(n_streams or 0), "hint": "В каталоге"})
        return {"role": role, "title": "Трансляции и мероприятия", "cards": cards}

    # SUPERADMIN
    n_users = await session.scalar(select(func.count()).select_from(User))
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    n_audit = await session.scalar(select(func.count()).select_from(AuditLog).where(AuditLog.created_at >= since))
    cards.append({"key": "users", "title": "Пользователей", "value": int(n_users or 0), "hint": "В системе"})
    cards.append({"key": "audit24", "title": "Записей аудита за 24 ч", "value": int(n_audit or 0), "hint": "Журнал действий"})
    n_unread_notifications = await session.scalar(
        select(func.count()).select_from(Notification).where(Notification.user_id == user.id, Notification.is_read.is_(False))
    )
    cards.append({"key": "notif", "title": "Непрочитанных уведомлений", "value": int(n_unread_notifications or 0), "hint": "Колокольчик в шапке"})
    return {"role": role, "title": "Администрирование", "cards": cards}
