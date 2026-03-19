"""Проверка отправки почты с настройками из backend/.env.

Запуск из каталога backend (как seed):

  cd /opt/streaming/backend
  source .venv/bin/activate
  set -a && source .env && set +a
  python -m scripts.test_smtp your@email.ru

Или один аргумент — адрес получателя теста.
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def main() -> None:
    from app.core.config import get_settings
    from app.services.welcome_email_service import _send_welcome_sync

    settings = get_settings()
    to_addr = sys.argv[1] if len(sys.argv) > 1 else ""
    if not to_addr.strip():
        print("Использование: python -m scripts.test_smtp получатель@example.com")
        sys.exit(1)

    if not (settings.smtp_host or "").strip():
        print("Ошибка: SMTP_HOST пустой в .env — письма не отправляются.")
        sys.exit(1)

    print("--- Настройки (пароль не показываем) ---")
    print(f"  SMTP_HOST={settings.smtp_host!r}")
    print(f"  SMTP_PORT={settings.smtp_port}")
    print(f"  SMTP_USE_TLS={settings.smtp_use_tls}")
    print(f"  SMTP_USE_SSL={settings.smtp_use_ssl}")
    print(f"  SMTP_USER={'(задан)' if settings.smtp_user else '(пусто)'}")
    print(f"  SMTP_FROM={settings.smtp_from!r}")
    print(f"  APP_PUBLIC_BASE_URL={settings.app_public_base_url!r}")
    print(f"--- Отправка теста на {to_addr!r} ---")

    try:
        _send_welcome_sync(
            host=settings.smtp_host.strip(),
            port=settings.smtp_port,
            user=settings.smtp_user or "",
            password=settings.smtp_password or "",
            use_tls=settings.smtp_use_tls,
            use_ssl=settings.smtp_use_ssl,
            from_addr=settings.smtp_from,
            to_addr=to_addr.strip(),
            subject="MainStream Ops — тест SMTP",
            body_html="<p>Если вы видите это письмо, SMTP настроен верно.</p>",
        )
    except Exception as e:
        print(f"ОШИБКА: {type(e).__name__}: {e}")
        print()
        print("Частые причины на Beget:")
        print("  • Порт 465 — часто нужен SSL с самого начала, а не STARTTLS (587).")
        print("  • SMTP_USER и SMTP_FROM должны совпадать с реальным ящиком в панели Beget.")
        print("  • Проверьте пароль приложения / пароль ящика.")
        sys.exit(1)

    print("OK: письмо принято сервером. Проверьте входящие и папку «Спам».")


if __name__ == "__main__":
    main()
