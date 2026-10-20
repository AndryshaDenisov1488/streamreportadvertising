"""Планировщик: пн 00:05 и 1-е число 00:10 (МСК) — отчёты на почту.

При нескольких uvicorn workers каждый worker поднимает свой APScheduler;
исполнение job_* защищено PostgreSQL advisory lock (см. background_lock).
"""

import logging
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config import get_settings
from app.services.broadcast_alert_service import job_long_broadcast_alerts
from app.services.email_report_service import job_monthly_report, job_weekly_report

logger = logging.getLogger(__name__)


def setup_report_scheduler() -> AsyncIOScheduler | None:
    settings = get_settings()
    if not settings.smtp_host:
        logger.info("SMTP не настроен — фоновые отчёты отключены")
        return None
    sched = AsyncIOScheduler(timezone=ZoneInfo("Europe/Moscow"))
    sched.add_job(
        job_weekly_report,
        CronTrigger(day_of_week="mon", hour=0, minute=5),
        id="weekly_report",
        replace_existing=True,
    )
    sched.add_job(
        job_monthly_report,
        CronTrigger(day=1, hour=0, minute=10),
        id="monthly_report",
        replace_existing=True,
    )
    sched.add_job(
        job_long_broadcast_alerts,
        CronTrigger(minute="*/10"),
        id="long_broadcast_alerts",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
    )
    sched.start()
    logger.info("Планировщик SMTP запущен (отчёты + проверка длительных эфиров каждые 10 минут)")
    return sched
