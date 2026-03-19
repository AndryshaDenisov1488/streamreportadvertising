"""Приветственное письмо при создании пользователя суперадмином."""

import asyncio
import html
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import get_settings
from app.models.enums import UserRole
from app.services.email_html_layout import wrap_email_html


def _role_label_ru(role: UserRole) -> str:
    return {
        UserRole.SUPERADMIN: "Суперадминистратор",
        UserRole.STREAM_MANAGER: "Менеджер стримов",
        UserRole.OPERATOR: "Оператор",
    }.get(role, role.value)


def _send_welcome_sync(
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


async def send_welcome_email(
    *,
    to_email: str,
    first_name: str,
    role: UserRole,
    plain_password: str,
) -> None:
    """Письмо с временным паролем (всегда генерируется при создании учётной записи)."""
    settings = get_settings()
    if not settings.smtp_host:
        raise RuntimeError("SMTP не настроен (smtp_host пустой в .env)")

    base = (settings.app_public_base_url or "").strip().rstrip("/")
    role_ru = _role_label_ru(role)
    greeting = (first_name or "").strip() or "коллега"
    headline = f"Здравствуйте, {greeting}!"

    login_href = f"{base}/login" if base else ""
    if base:
        cta_block = (
            f'<p style="margin:20px 0 0">'
            f'<a href="{html.escape(login_href, quote=True)}" '
            'style="display:inline-block;padding:12px 24px;background:#2563eb;'
            'color:#ffffff !important;text-decoration:none;border-radius:8px;'
            'font-weight:600;font-size:15px;font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif">'
            "Войти в панель</a></p>"
            f'<p style="margin:12px 0 0;font-size:13px;color:#8b9cb0">'
            f'Или откройте в браузере: {html.escape(login_href)}</p>'
        )
    else:
        cta_block = (
            "<p style=\"margin:16px 0 0;color:#8b9cb0\">"
            "Ссылку для входа сообщит администратор.</p>"
        )

    cred_box = (
        '<div style="background:#0d1219;border:1px solid #2a3f5c;border-radius:10px;padding:16px 18px;margin:0 0 14px">'
        '<p style="margin:0 0 10px;font-size:13px;color:#8b9cb0;text-transform:uppercase;letter-spacing:0.06em">'
        "Данные для входа</p>"
        '<p style="margin:0 0 6px;font-size:13px;color:#a8bdd4"><strong>Логин (email)</strong></p>'
        f'<div style="font-family:Consolas,Menlo,monospace;font-size:15px;color:#e8f0ff;word-break:break-all;'
        f'margin-bottom:14px">{html.escape(to_email)}</div>'
        '<p style="margin:0 0 6px;font-size:13px;color:#a8bdd4"><strong>Пароль</strong> (временный)</p>'
        f'<div style="font-family:Consolas,Menlo,monospace;font-size:15px;color:#e8f0ff;word-break:break-all;'
        f'letter-spacing:0.02em">{html.escape(plain_password)}</div>'
        "</div>"
    )
    inner = (
        '<p style="margin:0 0 14px">Вам открыт доступ к <strong>MainStream Ops</strong> — '
        "учёт эфиров и спонсорских упоминаний.</p>"
        f'<p style="margin:0 0 18px"><strong>Ваша роль:</strong> {html.escape(role_ru)}</p>'
        f"{cred_box}"
        "<p style=\"margin:0 0 12px\">Вход выполняется по <strong>email</strong> (логин) и <strong>паролю</strong> "
        "из блока выше.</p>"
        "<p style=\"margin:0 0 16px\">После входа сначала откроется экран <strong>смены пароля</strong> "
        "(можно отложить). Затем начнётся короткое <strong>знакомство с панелью</strong> — там можно указать телефон "
        "в любом привычном формате, он сохранится единообразно.</p>"
        f"{cta_block}"
        '<p style="margin:22px 0 0;font-size:14px;color:#9fb0c8">С уважением,<br/>команда MainStream</p>'
    )

    body_html = wrap_email_html(
        headline=headline,
        inner_html=inner,
        public_base_url=base,
    )
    subject = "Доступ к панели MainStream Ops"
    await asyncio.to_thread(
        _send_welcome_sync,
        host=settings.smtp_host,
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
