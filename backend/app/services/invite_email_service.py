"""Письмо со ссылкой, по которой новый пользователь сам задаёт пароль."""

import asyncio
import html
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import quote

from fastapi import HTTPException, status

from app.core.config import get_settings
from app.models.enums import UserRole
from app.services.email_html_layout import wrap_email_html
from app.services.welcome_email_service import role_label_ru


def require_invite_mail_ready() -> str:
    """Публичный адрес и SMTP должны быть заданы до создания приглашения."""
    settings = get_settings()
    base = (settings.app_public_base_url or "").strip().rstrip("/")
    if not base:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Не задан публичный адрес платформы (APP_PUBLIC_BASE_URL), ссылку в письме собрать нельзя",
        )
    if not (settings.smtp_host or "").strip():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Почта на сервере не настроена, письмо отправить нельзя",
        )
    return base


def accept_invite_url(token: str) -> str:
    base = require_invite_mail_ready()
    return f"{base}/accept-invite?token={quote(token, safe='')}"


def _send_invite_sync(
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
        return
    with smtplib.SMTP(host, port, timeout=60) as smtp:
        if use_tls:
            smtp.starttls()
        if user and password:
            smtp.login(user, password)
        smtp.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])


async def send_invite_email(
    *,
    to_email: str,
    full_name: str,
    role: UserRole,
    accept_url: str,
) -> None:
    settings = get_settings()
    base = (settings.app_public_base_url or "").strip().rstrip("/")
    role_ru = role_label_ru(role)
    greeting = full_name.strip() or "коллега"
    safe_link = html.escape(accept_url, quote=True)
    inner = (
        f'<p style="margin:0 0 14px">Здравствуйте, {html.escape(greeting)}!</p>'
        "<p style=\"margin:0 0 14px\">Вам открывают доступ к <strong>MainStream Ops</strong> — "
        "учёт эфиров и спонсорских упоминаний.</p>"
        f'<p style="margin:0 0 18px"><strong>Назначенная роль:</strong> {html.escape(role_ru)}</p>'
        "<p style=\"margin:0 0 18px\">Нажмите кнопку, придумайте пароль и введите его дважды. "
        "После сохранения учётка откроется. Ссылка действует <strong>7 дней</strong>.</p>"
        f'<p style="margin:20px 0 0">'
        f'<a href="{safe_link}" '
        'style="display:inline-block;padding:12px 24px;background:#2563eb;'
        'color:#ffffff !important;text-decoration:none;border-radius:8px;'
        'font-weight:600;font-size:15px;font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif">'
        "Задать пароль</a></p>"
        f'<p style="margin:12px 0 0;font-size:13px;color:#8b9cb0">'
        f"Если кнопка не открывается, скопируйте адрес: {safe_link}</p>"
        '<p style="margin:22px 0 0;font-size:14px;color:#9fb0c8">С уважением,<br/>команда MainStream</p>'
    )
    body_html = wrap_email_html(
        headline="Доступ к панели MainStream Ops",
        inner_html=inner,
        public_base_url=base,
    )
    subject = f"Доступ к панели MainStream Ops — {role_ru}"
    await asyncio.to_thread(
        _send_invite_sync,
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
