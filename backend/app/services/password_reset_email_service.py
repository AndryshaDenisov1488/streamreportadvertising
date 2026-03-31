"""Письмо со ссылкой сброса пароля."""

import asyncio
import html
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import get_settings
from app.services.email_html_layout import wrap_email_html

log = logging.getLogger(__name__)


def _send_password_reset_sync(
    *,
    host: str,
    port: int,
    user: str,
    password: str,
    use_tls: bool,
    use_ssl: bool,
    from_addr: str,
    to_addr: str,
    subject: str,
    body_html: str,
) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.attach(MIMEText(body_html, "html", "utf-8"))
    if use_ssl:
        with smtplib.SMTP_SSL(host, port, timeout=60) as smtp:
            if user and password:
                smtp.login(user, password)
            smtp.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])
    else:
        with smtplib.SMTP(host, port, timeout=60) as smtp:
            if use_tls:
                smtp.starttls()
            if user and password:
                smtp.login(user, password)
            smtp.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])


async def send_password_reset_email(*, to_email: str, reset_link: str, greeting_name: str) -> None:
    settings = get_settings()
    if not (settings.smtp_host or "").strip():
        raise RuntimeError("SMTP не настроен")
    base = (settings.app_public_base_url or "").strip().rstrip("/")
    headline = "Сброс пароля — MainStream Ops"
    safe_link = html.escape(reset_link, quote=True)
    who = (greeting_name or "").strip() or "коллега"
    minutes = settings.password_reset_expire_minutes
    inner = (
        f'<p style="margin:0 0 14px">Здравствуйте, {html.escape(who)}!</p>'
        "<p style=\"margin:0 0 18px\">Вы запросили <strong>сброс пароля</strong> для входа в панель. "
        f"Нажмите кнопку ниже и задайте новый пароль. Ссылка активна <strong>{minutes} мин.</strong></p>"
        f'<p style="margin:20px 0 0">'
        f'<a href="{safe_link}" '
        'style="display:inline-block;padding:12px 24px;background:#2563eb;'
        'color:#ffffff !important;text-decoration:none;border-radius:8px;'
        'font-weight:600;font-size:15px;font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif">'
        "Сбросить пароль</a></p>"
        f'<p style="margin:12px 0 0;font-size:13px;color:#8b9cb0">'
        f"Если кнопка не открывается, скопируйте адрес: {safe_link}</p>"
        "<p style=\"margin:18px 0 0;font-size:13px;color:#94a3b8\">"
        "Если вы не запрашивали сброс, просто проигнорируйте это письмо.</p>"
        '<p style="margin:22px 0 0;font-size:14px;color:#9fb0c8">С уважением,<br/>команда MainStream</p>'
    )
    body_html = wrap_email_html(
        headline=headline,
        inner_html=inner,
        public_base_url=base,
    )
    subject = "Сброс пароля — MainStream Ops"
    await asyncio.to_thread(
        _send_password_reset_sync,
        host=settings.smtp_host.strip(),
        port=settings.smtp_port,
        user=settings.smtp_user,
        password=settings.smtp_password,
        use_tls=settings.smtp_use_tls,
        use_ssl=settings.smtp_use_ssl,
        from_addr=settings.smtp_from,
        to_addr=to_email,
        subject=subject,
        body_html=body_html,
    )


async def send_password_reset_email_task(to_email: str, reset_link: str, greeting_name: str) -> None:
    try:
        await send_password_reset_email(to_email=to_email, reset_link=reset_link, greeting_name=greeting_name)
    except Exception:
        log.exception("Password reset email failed for %s", to_email)
