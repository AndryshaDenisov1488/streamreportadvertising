import asyncio
import html
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.timezone import format_moscow_datetime, utc_now
from app.db.session import AsyncSessionLocal
from app.models.stream import BroadcastSession, StreamEvent
from app.models.user import User
from app.services.background_lock import LOCK_LONG_BROADCAST_ALERTS, run_if_leader
from app.services.email_html_layout import wrap_email_html
from app.utils.display_name import user_display_name

logger = logging.getLogger(__name__)

FIRST_ALERT_HOURS = 15
ALERT_STEP_HOURS = 5


def _send_smtp_html_sync(
    *,
    host: str,
    port: int,
    user: str,
    password: str,
    use_tls: bool,
    use_ssl: bool,
    from_addr: str,
    to_addrs: list[str],
    subject: str,
    body_html: str,
) -> None:
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)
    msg.attach(MIMEText(body_html, "html", "utf-8"))
    if use_ssl:
        with smtplib.SMTP_SSL(host, port, timeout=60) as smtp:
            if user and password:
                smtp.login(user, password)
            smtp.send_message(msg, from_addr=from_addr, to_addrs=to_addrs)
        return
    with smtplib.SMTP(host, port, timeout=60) as smtp:
        if use_tls:
            smtp.starttls()
        if user and password:
            smtp.login(user, password)
        smtp.send_message(msg, from_addr=from_addr, to_addrs=to_addrs)


def _highest_reached_threshold(elapsed_hours: int) -> int:
    if elapsed_hours < FIRST_ALERT_HOURS:
        return 0
    steps = (elapsed_hours - FIRST_ALERT_HOURS) // ALERT_STEP_HOURS
    return FIRST_ALERT_HOURS + steps * ALERT_STEP_HOURS


async def _send_long_broadcast_email(
    *,
    to_addr: str,
    operator_name: str,
    stream_title: str,
    day_index: int,
    started_at_label: str,
    elapsed_hours: int,
) -> None:
    settings = get_settings()
    base = (settings.app_public_base_url or "").strip().rstrip("/")
    subject = f"[MainStream] Эфир длится уже {elapsed_hours} ч"
    inner = (
        f"<p style='margin:0 0 12px'>Здравствуйте, {html.escape(operator_name)}.</p>"
        f"<p style='margin:0 0 12px'>Эфир <b>{html.escape(stream_title)}</b> (день {day_index}) "
        f"длится уже <b>{elapsed_hours} часов</b>.</p>"
        f"<p style='margin:0 0 12px'>Старт эфира: {html.escape(started_at_label)} (МСК).</p>"
        "<p style='margin:0'>Проверьте, пожалуйста: возможно, эфир уже завершён и его нужно остановить.</p>"
    )
    body_html = wrap_email_html(
        headline="Проверьте длительность эфира",
        inner_html=inner,
        public_base_url=base,
        footer_line="MainStream Ops · автоматическое уведомление",
    )
    await asyncio.to_thread(
        _send_smtp_html_sync,
        host=settings.smtp_host,
        port=settings.smtp_port,
        user=settings.smtp_user,
        password=settings.smtp_password,
        use_tls=settings.smtp_use_tls,
        use_ssl=settings.smtp_use_ssl,
        from_addr=settings.smtp_from,
        to_addrs=[to_addr],
        subject=subject,
        body_html=body_html,
    )


async def check_long_running_broadcasts(session: AsyncSession) -> int:
    settings = get_settings()
    if not settings.smtp_host:
        return 0
    now_utc = utc_now()
    result = await session.execute(
        select(BroadcastSession, StreamEvent, User)
        .join(StreamEvent, BroadcastSession.stream_event_id == StreamEvent.id)
        .join(User, BroadcastSession.operator_id == User.id)
        .where(BroadcastSession.ended_at.is_(None), User.is_active.is_(True))
        .with_for_update(of=BroadcastSession, skip_locked=True)
    )
    sent_count = 0
    for bs, ev, operator in result.all():
        if not operator.email:
            continue
        started = bs.started_at if bs.started_at.tzinfo else bs.started_at.replace(tzinfo=now_utc.tzinfo)
        elapsed_hours = int((now_utc - started).total_seconds() // 3600)
        reached_threshold = _highest_reached_threshold(elapsed_hours)
        if reached_threshold <= 0:
            continue
        if reached_threshold <= (bs.duration_alert_last_sent_hour or 0):
            continue
        await _send_long_broadcast_email(
            to_addr=operator.email,
            operator_name=user_display_name(operator),
            stream_title=ev.title,
            day_index=bs.day_index,
            started_at_label=format_moscow_datetime(bs.started_at),
            elapsed_hours=reached_threshold,
        )
        bs.duration_alert_last_sent_hour = reached_threshold
        await session.commit()
        sent_count += 1
    return sent_count


async def job_long_broadcast_alerts() -> None:
    async def _run() -> None:
        async with AsyncSessionLocal() as session:
            sent_count = await check_long_running_broadcasts(session)
            if sent_count > 0:
                logger.info("Отправлены предупреждения по длительным эфирам: %s", sent_count)

    try:
        await run_if_leader(LOCK_LONG_BROADCAST_ALERTS, _run)
    except Exception:
        logger.exception("Ошибка фоновой проверки длительных эфиров")
