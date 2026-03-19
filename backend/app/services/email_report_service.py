"""Отчёты менеджерам/админам по почте: период + вложение Word с упоминаниями."""

import asyncio
import html
import smtplib
from datetime import date, datetime, timedelta
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.timezone import MOSCOW_TZ, format_moscow_date
from app.models.enums import UserRole
from app.models.stream import StreamDayAssignment, StreamEvent
from app.models.user import User
from app.services.email_html_layout import wrap_email_html
from app.services.report_service import export_mentions_docx
from app.services.stream_service import _assignment_summary_from_pairs, _load_assignment_pairs


def _send_smtp_sync(
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
    attachment_name: str,
    attachment_bytes: bytes,
) -> None:
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)
    msg.attach(MIMEText(body_html, "html", "utf-8"))
    part = MIMEApplication(attachment_bytes, _subtype="vnd.openxmlformats-officedocument.wordprocessingml.document")
    part.add_header("Content-Disposition", "attachment", filename=attachment_name)
    msg.attach(part)
    if use_ssl:
        with smtplib.SMTP_SSL(host, port, timeout=60) as smtp:
            if user and password:
                smtp.login(user, password)
            smtp.send_message(msg, from_addr=from_addr, to_addrs=to_addrs)
    else:
        with smtplib.SMTP(host, port, timeout=60) as smtp:
            if use_tls:
                smtp.starttls()
            if user and password:
                smtp.login(user, password)
            smtp.send_message(msg, from_addr=from_addr, to_addrs=to_addrs)


async def _recipient_emails(session: AsyncSession) -> list[str]:
    r = await session.execute(
        select(User.email).where(
            User.is_active.is_(True),
            User.role.in_((UserRole.STREAM_MANAGER, UserRole.SUPERADMIN)),
        )
    )
    return [e for e in r.scalars().all() if e]


async def _html_digest(session: AsyncSession, *, date_from: date, date_to: date) -> str:
    r = await session.execute(select(StreamEvent).order_by(StreamEvent.start_date.desc()))
    events = list(r.scalars().all())
    eids = [e.id for e in events]
    pairs_by = await _load_assignment_pairs(session, eids)
    rows: list[str] = []
    for ev in events:
        summary = _assignment_summary_from_pairs(pairs_by.get(ev.id, [])) or "не назначено"
        rows.append(
            "<tr>"
            f'<td style="border-bottom:1px solid #2a3f5c;padding:6px 8px">{html.escape(ev.title)}</td>'
            f'<td style="border-bottom:1px solid #2a3f5c;padding:6px 8px">{ev.duration_days}</td>'
            f'<td style="border-bottom:1px solid #2a3f5c;padding:6px 8px">'
            f"{html.escape(format_moscow_date(ev.start_date))}</td>"
            f'<td style="border-bottom:1px solid #2a3f5c;padding:6px 8px">{html.escape(summary)}</td>'
            "</tr>"
        )
    inner = (
        f"<p style=\"margin:0 0 14px\">Период (МСК): {format_moscow_date(date_from)} — "
        f"{format_moscow_date(date_to)}</p>"
        "<table border='0' cellpadding='8' cellspacing='0' style=\"width:100%;border-collapse:collapse;"
        "border:1px solid #2a3f5c;background:#0d1219\">"
        "<tr style=\"background:#152030\">"
        "<th align=\"left\" style=\"border-bottom:1px solid #2a3f5c;color:#e8eef8\">Мероприятие</th>"
        "<th align=\"left\" style=\"border-bottom:1px solid #2a3f5c;color:#e8eef8;width:56px\">Дней</th>"
        "<th align=\"left\" style=\"border-bottom:1px solid #2a3f5c;color:#e8eef8\">Старт</th>"
        "<th align=\"left\" style=\"border-bottom:1px solid #2a3f5c;color:#e8eef8\">Операторы по дням</th>"
        "</tr>"
        + "".join(rows)
        + "</table>"
        "<p style=\"margin:16px 0 0\">Во вложении — выгрузка упоминаний (таймкоды) за период в Word.</p>"
    )
    settings = get_settings()
    base = (settings.app_public_base_url or "").strip().rstrip("/")
    return wrap_email_html(
        headline="Сводка по эфирам",
        inner_html=inner,
        public_base_url=base,
        footer_line="MainStream Ops · автоматическая рассылка",
    )


async def send_period_report_email(
    session: AsyncSession,
    *,
    date_from: date,
    date_to: date,
    subject_prefix: str,
) -> None:
    settings = get_settings()
    if not settings.smtp_host:
        return
    to_addrs = await _recipient_emails(session)
    if not to_addrs:
        return
    docx = await export_mentions_docx(
        session,
        stream_event_id=None,
        date_from=date_from,
        date_to=date_to,
    )
    html = await _html_digest(session, date_from=date_from, date_to=date_to)
    subj = f"{subject_prefix} {format_moscow_date(date_from)} — {format_moscow_date(date_to)}"
    fname = f"mentions_{date_from}_{date_to}.docx"
    await asyncio.to_thread(
        _send_smtp_sync,
        host=settings.smtp_host,
        port=settings.smtp_port,
        user=settings.smtp_user,
        password=settings.smtp_password,
        use_tls=settings.smtp_use_tls,
        use_ssl=settings.smtp_use_ssl,
        from_addr=settings.smtp_from,
        to_addrs=to_addrs,
        subject=subj,
        body_html=html,
        attachment_name=fname,
        attachment_bytes=docx,
    )


def previous_week_moscow_bounds(today: date) -> tuple[date, date]:
    """Прошлая полная неделя пн–вс относительно понедельника today."""
    this_mon = today - timedelta(days=today.weekday())
    prev_sun = this_mon - timedelta(days=1)
    prev_mon = prev_sun - timedelta(days=6)
    return prev_mon, prev_sun


def previous_month_bounds(today: date) -> tuple[date, date]:
    first_this = today.replace(day=1)
    last_prev = first_this - timedelta(days=1)
    first_prev = last_prev.replace(day=1)
    return first_prev, last_prev


async def job_weekly_report() -> None:
    from app.db.session import AsyncSessionLocal

    now_m = datetime.now(MOSCOW_TZ).date()
    d0, d1 = previous_week_moscow_bounds(now_m)
    async with AsyncSessionLocal() as session:
        await send_period_report_email(
            session,
            date_from=d0,
            date_to=d1,
            subject_prefix="[MainStream] Недельный отчёт",
        )


async def job_monthly_report() -> None:
    from app.db.session import AsyncSessionLocal

    now_m = datetime.now(MOSCOW_TZ).date()
    d0, d1 = previous_month_bounds(now_m)
    async with AsyncSessionLocal() as session:
        await send_period_report_email(
            session,
            date_from=d0,
            date_to=d1,
            subject_prefix="[MainStream] Месячный отчёт",
        )
