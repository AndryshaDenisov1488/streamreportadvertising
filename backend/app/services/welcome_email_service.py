"""Приветственное письмо при создании пользователя суперадмином."""

import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import get_settings
from app.models.enums import UserRole


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
            smtp.sendmail(from_addr, [to_addr], msg.as_string())
    else:
        with smtplib.SMTP(host, port, timeout=60) as smtp:
            if use_tls:
                smtp.starttls()
            if user and password:
                smtp.login(user, password)
            smtp.sendmail(from_addr, [to_addr], msg.as_string())


async def send_welcome_email(
    *,
    to_email: str,
    first_name: str,
    role: UserRole,
    plain_password: str | None,
    password_was_auto_generated: bool,
) -> None:
    """Отправить письмо. plain_password обязателен если password_was_auto_generated."""
    settings = get_settings()
    if not settings.smtp_host:
        raise RuntimeError("SMTP не настроен (smtp_host пустой в .env)")

    base = (settings.app_public_base_url or "").strip().rstrip("/")
    link_line = (
        f'<p>Вход в панель: <a href="{base}/login">{base}/login</a></p>'
        if base
        else "<p>Вход выполняется по адресу панели, который вам сообщит администратор.</p>"
    )

    role_ru = _role_label_ru(role)
    greeting = first_name.strip() or "коллега"

    if password_was_auto_generated and plain_password:
        pwd_block = (
            f"<p><strong>Временный пароль:</strong> {plain_password}</p>"
            "<p>Сохраните его в надёжном месте. После входа рекомендуется сменить пароль "
            "в разделе «Профиль» (это необязательно).</p>"
        )
    else:
        pwd_block = (
            "<p>Пароль для входа был задан администратором при создании учётной записи. "
            "Если вы его не знаете — запросите у администратора.</p>"
        )

    body_html = f"""\
<html><body>
<p>Здравствуйте, {greeting}!</p>
<p>Вам открыт доступ к рабочей панели <strong>MainStream Ops</strong> (учёт эфиров и упоминаний).</p>
<p><strong>Ваша роль:</strong> {role_ru}</p>
{pwd_block}
{link_line}
<p>С уважением,<br/>команда MainStream</p>
</body></html>"""

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
