# Почта не приходит: проверка SMTP

## 1. Тест с сервера

```bash
cd /opt/streaming/backend
source .venv/bin/activate
set -a && source .env && set +a
python -m scripts.test_smtp ВАШ_EMAIL@mail.ru
```

Скрипт выведет параметры (без пароля) и попытается отправить тест. При ошибке — текст исключения (часто «Connection refused», «Authentication failed», SSL).

Если видите **`UnicodeEncodeError: 'ascii' codec can't encode`** — в теме или теле письма есть кириллица; в приложении для отправки используется `SMTP.send_message` (UTF-8). Обновите бэкенд с последнего коммита.

## 2. Логи бэкенда после создания пользователя

Приветственное письмо уходит **в фоне**. Ошибки смотрите так:

```bash
journalctl -u streaming-backend -n 100 --no-pager | grep -i welcome
```

Успех: строка `Welcome email sent to ...`. Ошибка: `Welcome email failed` со stack trace.

## 3. Beget и порты

| Вариант | Обычно |
|--------|--------|
| **587** + STARTTLS | `SMTP_USE_TLS=true`, в коде используется `SMTP` + `starttls()` |
| **465** | Implicit SSL — стандартный `smtplib.SMTP` + `starttls()` **может не подойти**; нужен `SMTP_SSL` |

Если используете **порт 465**, в `.env` задайте:

```env
SMTP_PORT=465
SMTP_USE_SSL=true
SMTP_USE_TLS=false
```

Иначе клиент пытается обычный `SMTP` + `STARTTLS`, что для 465 обычно **не подходит**.

Альтернатива: **587** или **2525** с `SMTP_USE_TLS=true` и `SMTP_USE_SSL=false`.

## 4. Обязательные поля в `.env`

- `SMTP_HOST` — например `smtp.beget.com`
- `SMTP_FROM` и обычно **`SMTP_USER`** — полный адрес ящика, созданного в панели Beget
- `SMTP_PASSWORD` — пароль этого ящика

Пустой `SMTP_HOST` — письма **не отправляются** (пользователь всё равно создаётся).

## 5. Письмо «есть», но не в «Входящих»

Проверьте **Спам**, фильтры Mail.ru, задержку 5–15 минут.
