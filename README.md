# Платформа эфиров MainStream

<p align="center">
  <strong>Платформа для видеооператоров: стрим-события, блокировки, таймкоды спонсоров, WebSocket, отчёты Word</strong>
</p>

<p align="center">
  <a href="https://streaming.mainstreamfs.ru">streaming.mainstreamfs.ru</a> ·
  <a href=".cursor/skills/streaming/reference.md">Полная документация (Ultra)</a> ·
  <a href=".cursor/skills/streaming/SKILL.md">AI Skill</a>
</p>

---

## Содержание

1. [О проекте](#о-проекте)
2. [Ключевые возможности](#ключевые-возможности)
3. [Архитектура](#архитектура)
4. [Технологический стек](#технологический-стек)
5. [Структура репозитория](#структура-репозитория)
6. [API](#api)
7. [База данных](#база-данных)
8. [Установка и разработка](#установка-и-разработка)
9. [Деплой на production](#деплой-на-production)
10. [Конфигурация (.env)](#конфигурация-env)
11. [Мониторинг и логи](#мониторинг-и-логи)
12. [Бэкапы](#бэкапы)
13. [Безопасность](#безопасность)
14. [Интеграции](#интеграции)
15. [Документация](#документация)

---

## О проекте

**Платформа эфиров MainStream** — Платформа для видеооператоров: стрим-события, блокировки, таймкоды спонсоров, WebSocket, отчёты Word.

Система является частью экосистемы **MainStream** и развёрнута на production-сервере:

| | |
|--|--|
| Сервер | xkvlorcrjx (45.12.237.105, Beget VPS) |
| ОС | Ubuntu 22.04.5 LTS |
| URL | https://streaming.mainstreamfs.ru |
| Backend | 127.0.0.1:8010 (Uvicorn) |
| БД | PostgreSQL: streaming |
| Systemd | streaming-backend |
| Unix user | root |
| Интеграции | mainstreamfs.ru |

### Расположение на сервере

| Параметр | Значение |
|----------|----------|
| Путь | `/opt/streaming` |
| Домен | `streaming.mainstreamfs.ru` |
| Порт backend | `8010 (Uvicorn)` |
| Systemd | `streaming-backend` |
| Пользователь | `root` |
| БД | `PostgreSQL: streaming` |

---

## Ключевые возможности

Сгенерированные типы OpenAPI: выполните из каталога `frontend` при запущенном backend:

```bash
npm run codegen:api
```

Файл `schema.ts` создаётся автоматически (при необходимости добавьте в `.gitignore`).

---

## Архитектура

## 1.1 Описание продукта

**Платформа эфиров MainStream** — Платформа для видеооператоров: стрим-события, блокировки, таймкоды спонсоров, WebSocket, отчёты Word.

Система является частью экосистемы **MainStream** и развёрнута на production-сервере:

| | |
|--|--|
| Сервер | xkvlorcrjx (45.12.237.105, Beget VPS) |
| ОС | Ubuntu 22.04.5 LTS |
| URL | https://streaming.mainstreamfs.ru |
| Backend | 127.0.0.1:8010 (Uvicorn) |
| БД | PostgreSQL: streaming |
| Systemd | streaming-backend |
| Unix user | root |
| Интеграции | mainstreamfs.ru |

## 1.2

```
Интернет → nginx (443) → 127.0.0.1:8010 (Uvicorn) → systemd (streaming-backend)
```

---

## Технологический стек

ЗАВИСИМОСТИ И СТЕК

## 2.1 Python зависимости

```
alembic>=1.13.0
apscheduler>=3.10.0
asyncpg>=0.29.0
bcrypt>=4.1.0
email-validator>=2.0.0
fastapi>=0.109.0
greenlet>=3.0.0
httpx>=0.26.0
openpyxl>=3.1.0
passlib
psycopg2-binary>=2.9.9
pydantic-settings>=2.1.0
pydantic>=2.5.0
pytest-asyncio>=0.23.0
pytest>=8.0.0
python-docx>=1.1.0
python-jose
python-multipart>=0.0.6
sentry-sdk
slowapi>=0.1.9
sqlalchemy
uvicorn
```

## 2.2 JavaScript зависимости

```json
{
  "dependencies": {
    "@ant-design/icons": "^5.5.1",
    "@sentry/react": "^8.42.0",
    "@tanstack/react-query": "^5.59.0",
    "antd": "^5.21.0",
    "dayjs": "^1.11.13",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.28.0"
  },
  "devDependencies": {
    "@playwright/test": "^1.49.1",
    "@storybook/addon-essentials": "^8.4.7",
    "@storybook/react": "^8.4.7",
    "@storybook/react-vite": "^8.4.7",
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.3.3",
    "openapi-typescript": "^7.4.4",
    "storybook": "^8.4.7",
    "typescript": "~5.6.3",
    "vite": "^5.4.11",
    "vite-plugin-pwa": "^0.21.1"
  }
}
```

---

---

## Структура репозитория

```
.
./backups
./frontend
./frontend/e2e
./frontend/.storybook
./frontend/public
./frontend/dist
./frontend/dist/assets
./frontend/src
./frontend/src/api
./frontend/src/pages
./frontend/src/stories
./frontend/src/components
./frontend/src/utils
./frontend/src/layouts
./frontend/src/auth
./frontend/src/content
./frontend/src/hooks
./frontend/src/styles
./frontend/node_modules
./frontend/node_modules/@emotion
./frontend/node_modules/update-browserslist-db
./frontend/node_modules/reflect.getprototypeof
./frontend/node_modules/babel-plugin-polyfill-corejs2
./frontend/node_modules/workbox-range-requests
./frontend/node_modules/rc-rate
./frontend/node_modules/available-typed-arrays
./frontend/node_modules/@redocly
./frontend/node_modules/jsdoc-type-pratt-parser
./frontend/node_modules/is-wsl
./frontend/node_modules/json-schema-traverse
./frontend/node_modules/unicode-match-property-value-ecmascript
./frontend/node_modules/copy-to-clipboard
./frontend/node_modules/get-intrinsic
./frontend/node_modules/async
./frontend/node_modules/hoist-non-react-statics
./frontend/node_modules/jake
./frontend/node_modules/toggle-selection
./frontend/node_modules/@sentry-internal
./frontend/node_modules/workbox-build
./frontend/node_modules/is-weakset
./frontend/node_modules/is-string
./frontend/node_modules/js-levenshtein
./frontend/node_modules/lodash.debounce
./frontend/node_modules/gopd
./frontend/node_modules/signal-exit
./frontend/node_modules/playwright-core
./frontend/node_modules/json5
./frontend/node_modules/unbox-primitive
./frontend/node_modules/rc-motion
./frontend/node_modules/is-async-function
./frontend/node_modules/strip-comments
./frontend/node_modules/rc-virtual-list
./frontend/node_modules/workbox-broadcast-update
./frontend/node_modules/is-typed-array
./frontend/node_modules/esutils
./frontend/node_modules/side-channel-map
./frontend/node_modules/smob
./frontend/node_modules/rc-menu
./frontend/node_modules/unicode-canonical-property-names-ecmascript
./frontend/node_modules/react-router-dom
./frontend/node_modules/throttle-debounce
./frontend/node_modules/common-tags
./frontend/node_modules/better-opn
./frontend/node_modules/tempy
./frontend/node_modules/js-tokens
./frontend/node_modules/path-exists
./frontend/node_modules/vite-plugin-pwa
./frontend/node_modules/data-view-buffer
./frontend/node_modules/unplugin
./frontend/node_modules/filelist
./frontend/node_modules/node-releases
./frontend/node_modules/rc-input-number
./frontend/node_modules/regexp.prototype.flags
./frontend/node_modules/compute-scroll-into-view
./frontend/node_modules/is-callable
./frontend/node_modules/define-properties
./frontend/node_modules/safe-array-concat
./frontend/node_modules/@apideck
./frontend/node_modules/storybook
```

Полный каталог: [reference.md § Часть III](.cursor/skills/streaming/reference.md)

---

## API

И МАРШРУТЫ (ПОЛНЫЙ РЕЕСТР)

Всего: **52** endpoints

```
GET /health  ← `backend/app/api/health.py`
GET /health/ready  ← `backend/app/api/health.py`
GET /export.csv  ← `backend/app/api/v1/audit.py`
POST /purge  ← `backend/app/api/v1/audit.py`
POST /accept-invite  ← `backend/app/api/v1/auth.py`
POST /forgot-password  ← `backend/app/api/v1/auth.py`
GET /password-reset/validate  ← `backend/app/api/v1/auth.py`
POST /reset-password  ← `backend/app/api/v1/auth.py`
POST /login  ← `backend/app/api/v1/auth.py`
POST /refresh  ← `backend/app/api/v1/auth.py`
POST /logout  ← `backend/app/api/v1/auth.py`
GET /me  ← `backend/app/api/v1/auth.py`
POST /change-password  ← `backend/app/api/v1/auth.py`
GET /sessions  ← `backend/app/api/v1/auth.py`
DELETE /sessions/{session_id}  ← `backend/app/api/v1/auth.py`
DELETE /{template_id}  ← `backend/app/api/v1/event_templates.py`
POST /from-event/{stream_id}  ← `backend/app/api/v1/event_templates.py`
POST /{template_id}/instantiate  ← `backend/app/api/v1/event_templates.py`
POST /upload  ← `backend/app/api/v1/logos.py`
POST /upload-batch  ← `backend/app/api/v1/logos.py`
POST /broadcast-sessions/{session_id}/mentions  ← `backend/app/api/v1/mentions.py`
PATCH /sponsor-mentions/{mention_id}  ← `backend/app/api/v1/mentions.py`
DELETE /sponsor-mentions/{mention_id}  ← `backend/app/api/v1/mentions.py`
POST /{notification_id}/read  ← `backend/app/api/v1/notifications.py`
POST /read-all  ← `backend/app/api/v1/notifications.py`
POST /events  ← `backend/app/api/v1/product_analytics.py`
GET /summary  ← `backend/app/api/v1/product_analytics.py`
POST /avatar  ← `backend/app/api/v1/profile.py`
GET /activity  ← `backend/app/api/v1/profile.py`
GET /mentions  ← `backend/app/api/v1/reports.py`
GET /export.docx  ← `backend/app/api/v1/reports.py`
GET /export.csv  ← `backend/app/api/v1/reports.py`
GET /export.xlsx  ← `backend/app/api/v1/reports.py`
GET /operators  ← `backend/app/api/v1/stats.py`
GET /{stream_id}  ← `backend/app/api/v1/stream_events.py`
PATCH /{stream_id}  ← `backend/app/api/v1/stream_events.py`
DELETE /{stream_id}  ← `backend/app/api/v1/stream_events.py`
POST /{stream_id}/lock  ← `backend/app/api/v1/stream_events.py`
POST /{stream_id}/unlock  ← `backend/app/api/v1/stream_events.py`
POST /{stream_id}/days/{day_index}/broadcast/start  ← `backend/app/api/v1/stream_events.py`
POST /{stream_id}/days/{day_index}/broadcast/actual-start  ← `backend/app/api/v1/stream_events.py`
POST /{stream_id}/days/{day_index}/broadcast/stop  ← `backend/app/api/v1/stream_events.py`
GET /{stream_id}/days/{day_index}/checklist  ← `backend/app/api/v1/stream_events.py`
PUT /{stream_id}/days/{day_index}/checklist  ← `backend/app/api/v1/stream_events.py`
GET /{stream_id}/days/{day_index}/mentions  ← `backend/app/api/v1/stream_events.py`
POST /{stream_id}/logos  ← `backend/app/api/v1/stream_logos.py`
DELETE /{stream_id}/logos/{logo_id}  ← `backend/app/api/v1/stream_logos.py`
GET /{stream_id}/logos/archive.zip  ← `backend/app/api/v1/stream_logos.py`
GET /{stream_id}/logos/{logo_id}/file  ← `backend/app/api/v1/stream_logos.py`
POST /invites  ← `backend/app/api/v1/users.py`
PATCH /{user_id}  ← `backend/app/api/v1/users.py`
DELETE /{user_id}  ← `backend/app/api/v1/users.py`
```

---

---

## База данных

PostgreSQL: streaming

Схема: [reference.md Часть VII](.cursor/skills/streaming/reference.md)

---

## Установка и разработка

### Требования

- Python 3.10+ / Node.js 18+ (см. проект)
- SQLite / PostgreSQL (см. конфиг)
- nginx (production)

### Локальный запуск

```bash
git clone <repo>
cd streaming
cp env.example .env   # настроить
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# или: cd backend && pip install -r requirements.txt
# Frontend: cd frontend && npm ci && npm run dev
```

---

## Деплой на production

ОПЕРАЦИИ

## Деплой
```bash
cd /opt/streaming
git pull
# pip install / npm ci / build / migrate
systemctl restart streaming-backend
```

## Диагностика
```bash
systemctl status streaming-backend
journalctl -u streaming-backend -n 200 --no-pager
curl -s http://127.0.0.1:<port>/health
```

## Бэкапы
- Cron 04:00: `/usr/local/sbin/ffkm-project-backups.sh`
- Лог: `/var/log/ffkm-project-backups.log`

---

### ТЗ сервера

# ТЗ: размещение на сервере — Streaming platform (streaming.mainstreamfs.ru)

## Назначение
Платформа **стриминга/трансляций** (отдельно от магазина MainStream в `/root/mainstreamfs.ru`): **FastAPI** backend с WebSocket/долгими соединениями, фронт — **SPA** из `frontend/dist`.

## Путь на сервере
`/opt/streaming/`
- `backend/` — Python, Uvicorn.
- `frontend/dist` — статика для nginx.

## Systemd
- **`streaming-backend.service`**:  
  `uvicorn app.main:app --host 127.0.0.1 --port 8010 --workers 2`  
  venv: `/opt/streaming/backend/.venv`.

## Сеть и домены
- **HTTPS:** `streaming.mainstreamfs.ru`.
- Nginx `/etc/nginx/sites-available/streaming.conf`:
  - `/` → `try_files` в `frontend/dist`;
  - `/api/`, `/health`, `/openapi.json` → backend **8010**;
  - `/uploads/` → **deny** (404); media via `/api/v1/media/...` (signed URL or Bearer);
  - длинный `proxy_read_timeout` для WebSocket.

## Связь с MainStream Shop
Тот же бренд в домене (**mainstreamfs**), но **другой код** и **другой systemd** на сервере.

## Данные
- Загрузки и БД приложения — внутри `/opt/streaming/backend` по конфигурации.


---

## Конфигурация (.env)

Переменные — в `env.example`. **Никогда не коммитить `.env`.**

На production: `chmod 600 .env`

Полный список: [reference.md Часть VI](.cursor/skills/streaming/reference.md)

---

## Мониторинг и логи

```bash
journalctl -u streaming-backend -f
systemctl status streaming-backend
```

Prometheus exporters на сервере: node_exporter, nginx_exporter, postgres_exporter.

---

## Бэкапы

- **Расписание:** ежедневно 04:00 MSK
- **Скрипт:** `/usr/local/sbin/ffkm-project-backups.sh`
- **Лог:** `/var/log/ffkm-project-backups.log`
- **Ротация:** 7 дней

---

## Безопасность

- Backend слушает только `127.0.0.1`
- SSL через Let's Encrypt (certbot)
- UFW + Fail2ban на сервере
- `.env` права 600
- nginx блокирует `/.env`, `/.git`
- Аудит: `/root/server_audit_report_2026-06-10.docx`

---

## Интеграции

mainstreamfs.ru

### Outbound stream webhook (optional)

When `EXTERNAL_WEBHOOK_URL` is set, the backend POSTs JSON `{ "type", "payload" }` on broadcast start/stop.

| Item | Value |
|------|-------|
| Secret env | `EXTERNAL_WEBHOOK_SECRET` (required if URL is set; generate e.g. `openssl rand -hex 32`) |
| Signature header | `X-Webhook-Signature` |
| Algorithm | HMAC-SHA256 over the **exact** raw request body bytes |
| Header format | `sha256=<hex digest>` |

Consumers must recompute HMAC over the raw body and compare with `hmac.compare_digest`. Unsigned deliveries are not sent (URL without secret fails at Settings boot).

---

## Документация

| Документ | Описание | Размер |
|----------|----------|--------|
| [reference.md](.cursor/skills/streaming/reference.md) | Исчерпывающая техдокументация | ~912K символов |
| [SKILL.md](.cursor/skills/streaming/SKILL.md) | Навигация для AI-агента | — |
| [ТЗ-сервер.md](ТЗ-сервер.md) | ТЗ размещения | — |
| [ffkm-server](/root/.cursor/skills/ffkm-server/) | Документация всего сервера | — |

---


---

## Детальный анализ файлов (выдержка)

### Файл: `.env.example`

| Свойство | Значение |
|----------|----------|
| Строк | 70 |
| Размер | 3,515 байт |

### Файл: `README.md`

| Свойство | Значение |
|----------|----------|
| Строк | 453 |
| Размер | 19,563 байт |

### Файл: `backend/Dockerfile`

| Свойство | Значение |
|----------|----------|
| Строк | 26 |
| Размер | 746 байт |

### Файл: `backend/alembic.ini`

| Свойство | Значение |
|----------|----------|
| Строк | 43 |
| Размер | 637 байт |

### Файл: `backend/alembic/env.py`

| Свойство | Значение |
|----------|----------|
| Строк | 78 |
| Размер | 1,897 байт |
| Функции | 5 |

**Функции верхнего уровня:**

- `get_url()` L38
- `run_migrations_offline()` L42
- `do_run_migrations(connection)` L53
- `run_async_migrations()` L59
- `run_migrations_online()` L70

### Файл: `backend/app/api/health.py`

| Свойство | Значение |
|----------|----------|
| Строк | 38 |
| Размер | 1,173 байт |
| Маршруты | 2 |
| Функции | 2 |

**Функции верхнего уровня:**

- `health_live()` L12
- `health_ready(session)` L18

**Маршруты:**
```
GET /health
GET /health/ready
```


### Файл: `backend/app/api/v1/audit.py`

| Свойство | Значение |
|----------|----------|
| Строк | 93 |
| Размер | 2,817 байт |
| Маршруты | 2 |
| Классы | 1 |
| Функции | 3 |

**Классы:**

- `AuditPurgeBody` (строка 81)

**Функции верхнего уровня:**

- `list_logs(_, session, page, page_size, user_id, action_type)` L18
- `export_audit_csv(_, session, user_id, action_type)` L42
- `purge_audit(_, session, body)` L86

**Маршруты:**
```
GET /export.csv
POST /purge
```


### Файл: `backend/app/api/v1/auth.py`

| Свойство | Значение |
|----------|----------|
| Строк | 214 |
| Размер | 7,009 байт |
| Маршруты | 11 |
| Функции | 11 |

**Функции верхнего уровня:**

- `accept_invite_route(request, response, body, session)` L31
- `forgot_password_route(request, background_tasks, body, session)` L62
- `password_reset_validate_route(request, token, session)` L76
- `reset_password_route(request, body, session)` L89
- `login(request, response, body, session)` L103
- `refresh_token(request, response, session, body)` L133
- `logout(request, response, user, session, body)` L152
- `me(user)` L168
- `change_password_route(body, user, current_jti, session)` L173
- `list_sessions_route(user, current_jti, session)` L189
- `revoke_session_route(session_id, user, session)` L208

**Маршруты:**
```
POST /accept-invite
POST /forgot-password
GET /password-reset/validate
POST /reset-password
POST /login
POST /refresh
POST /logout
GET /me
POST /change-password
GET /sessions
DELETE /sessions/{session_id}
```


### Файл: `backend/app/api/v1/dashboard.py`

| Свойство | Значение |
|----------|----------|
| Строк | 19 |
| Размер | 627 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `dashboard_summary(user, session)` L13

### Файл: `backend/app/api/v1/event_templates.py`

| Свойство | Значение |
|----------|----------|
| Строк | 74 |
| Размер | 2,392 байт |
| Маршруты | 3 |
| Функции | 5 |

**Функции верхнего уровня:**

- `list_templates(_, session)` L21
- `create_template(body, user, session)` L30
- `delete_template(template_id, user, session)` L40
- `template_from_event(stream_id, body, user, session)` L49
- `instantiate_template(template_id, body, user, session)` L60

**Маршруты:**
```
DELETE /{template_id}
POST /from-event/{stream_id}
POST /{template_id}/instantiate
```


### Файл: `backend/app/api/v1/logos.py`

| Свойство | Значение |
|----------|----------|
| Строк | 36 |
| Размер | 1,209 байт |
| Маршруты | 2 |
| Функции | 3 |

**Функции верхнего уровня:**

- `upload_logo_route(actor, session, file)` L13
- `upload_logos_batch_route(actor, session, files)` L22
- `list_logos_route(_, session)` L31

**Маршруты:**
```
POST /upload
POST /upload-batch
```


### Файл: `backend/app/api/v1/mentions.py`

| Свойство | Значение |
|----------|----------|
| Строк | 74 |
| Размер | 2,652 байт |
| Маршруты | 3 |
| Функции | 3 |

**Функции верхнего уровня:**

- `add_mention(session_id, request, actor, session)` L18
- `patch_mention(mention_id, body, request, actor, session)` L38
- `delete_mention(mention_id, request, actor, session)` L61

**Маршруты:**
```
POST /broadcast-sessions/{session_id}/mentions
PATCH /sponsor-mentions/{mention_id}
DELETE /sponsor-mentions/{mention_id}
```


### Файл: `backend/app/api/v1/notifications.py`

| Свойство | Значение |
|----------|----------|
| Строк | 49 |
| Размер | 1,616 байт |
| Маршруты | 2 |
| Функции | 3 |

**Функции верхнего уровня:**

- `list_my_notifications(user, session)` L15
- `mark_notification_read(notification_id, user, session)` L28
- `mark_all_read(user, session)` L43

**Маршруты:**
```
POST /{notification_id}/read
POST /read-all
```


### Файл: `backend/app/api/v1/product_analytics.py`

| Свойство | Значение |
|----------|----------|
| Строк | 35 |
| Размер | 1,073 байт |
| Маршруты | 2 |
| Функции | 2 |

**Функции верхнего уровня:**

- `track_event(body, user, session)` L13
- `analytics_summary(_, session)` L27

**Маршруты:**
```
POST /events
GET /summary
```


### Файл: `backend/app/api/v1/profile.py`

| Свойство | Значение |
|----------|----------|
| Строк | 61 |
| Размер | 1,897 байт |
| Маршруты | 2 |
| Функции | 4 |

**Функции верхнего уровня:**

- `get_profile(user, session)` L16
- `patch_profile(body, user, session)` L22
- `post_avatar(user, session, file)` L32
- `get_my_activity(user, session, page, page_size)` L42

**Маршруты:**
```
POST /avatar
GET /activity
```


### Файл: `backend/app/api/v1/reports.py`

| Свойство | Значение |
|----------|----------|
| Строк | 98 |
| Размер | 2,928 байт |
| Маршруты | 4 |
| Функции | 4 |

**Функции верхнего уровня:**

- `report_mentions(_, session, stream_id, date_from, date_to)` L22
- `export_docx(_, session, stream_id, date_from, date_to)` L38
- `export_csv(_, session, stream_id, date_from, date_to)` L59
- `export_xlsx(_, session, stream_id, date_from, date_to)` L80

**Маршруты:**
```
GET /mentions
GET /export.docx
GET /export.csv
GET /export.xlsx
```


### Файл: `backend/app/api/v1/router.py`

| Свойство | Значение |
|----------|----------|
| Строк | 37 |
| Размер | 953 байт |

### Файл: `backend/app/api/v1/stats.py`

| Свойство | Значение |
|----------|----------|
| Строк | 26 |
| Размер | 897 байт |
| Маршруты | 1 |
| Функции | 1 |

**Функции верхнего уровня:**

- `operator_stats(_, session, stat_date)` L16

**Маршруты:**
```
GET /operators
```


### Файл: `backend/app/api/v1/stream_events.py`

| Свойство | Значение |
|----------|----------|
| Строк | 276 |
| Размер | 9,170 байт |
| Маршруты | 11 |
| Функции | 13 |

**Функции верхнего уровня:**

- `list_streams(actor, session)` L29
- `get_stream(stream_id, _, session)` L37
- `create_stream(body, actor, session)` L46
- `update_stream(stream_id, body, actor, session)` L55
- `delete_stream(stream_id, actor, session)` L65
- `lock_stream_route(stream_id, request, actor, session, body)` L74
- `unlock_stream_route(stream_id, request, actor, session)` L102
- `start_broadcast_route(stream_id, day_index, request, background_tasks, actor, session)` L115
- `realign_broadcast_actual_start_route(stream_id, day_index, body, request, actor, session)` L153
- `stop_broadcast_route(stream_id, day_index, request, background_tasks, actor, session)` L180
- `get_checklist_route(stream_id, day_index, user, session)` L199
- `put_checklist_route(stream_id, day_index, body, user, session)` L235
- `list_mentions_route(stream_id, day_index, _, session)` L269

**Маршруты:**
```
GET /{stream_id}
PATCH /{stream_id}
DELETE /{stream_id}
POST /{stream_id}/lock
POST /{stream_id}/unlock
POST /{stream_id}/days/{day_index}/broadcast/start
POST /{stream_id}/days/{day_index}/broadcast/actual-start
POST /{stream_id}/days/{day_index}/broadcast/stop
GET /{stream_id}/days/{day_index}/checklist
PUT /{stream_id}/days/{day_index}/checklist
GET /{stream_id}/days/{day_index}/mentions
```


### Файл: `backend/app/api/v1/stream_logos.py`

| Свойство | Значение |
|----------|----------|
| Строк | 78 |
| Размер | 2,807 байт |
| Маршруты | 4 |
| Функции | 4 |

**Функции верхнего уровня:**

- `attach_logo_route(stream_id, body, actor, session)` L19
- `detach_logo_route(stream_id, logo_id, actor, session)` L29
- `download_logos_zip_route(stream_id, actor, session)` L39
- `download_logo_file_route(stream_id, logo_id, _, session)` L60

**Маршруты:**
```
POST /{stream_id}/logos
DELETE /{stream_id}/logos/{logo_id}
GET /{stream_id}/logos/archive.zip
GET /{stream_id}/logos/{logo_id}/file
```


### Файл: `backend/app/api/v1/users.py`

| Свойство | Значение |
|----------|----------|
| Строк | 72 |
| Размер | 2,464 байт |
| Маршруты | 3 |
| Функции | 5 |

**Функции верхнего уровня:**

- `list_users(_, session)` L16
- `create_invite(body, actor, session)` L25
- `create_user(body, actor, background_tasks, session)` L38
- `update_user(user_id, body, actor, session)` L55
- `delete_user(user_id, actor, session)` L66

**Маршруты:**
```
POST /invites
PATCH /{user_id}
DELETE /{user_id}
```


### Файл: `backend/app/api/v1/ws.py`

| Свойство | Значение |
|----------|----------|
| Строк | 69 |
| Размер | 2,048 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `stream_events_ws(websocket, stream_event_id)` L19

### Файл: `backend/app/core/config.py`

| Свойство | Значение |
|----------|----------|
| Строк | 63 |
| Размер | 2,216 байт |
| Классы | 1 |
| Функции | 1 |

**Классы:**

- `Settings` (строка 6)
  - `cors_origins_list(self)` L56

**Функции верхнего уровня:**

- `get_settings()` L61

### Файл: `backend/app/core/deps.py`

| Свойство | Значение |
|----------|----------|
| Строк | 81 |
| Размер | 3,335 байт |
| Функции | 3 |

**Функции верхнего уровня:**

- `get_current_user(session, credentials)` L18
- `require_roles()` L54
- `get_refresh_jti(request)` L71

### Файл: `backend/app/core/limiter.py`

| Свойство | Значение |
|----------|----------|
| Строк | 5 |
| Размер | 120 байт |

### Файл: `backend/app/core/security.py`

| Свойство | Значение |
|----------|----------|
| Строк | 54 |
| Размер | 1,708 байт |
| Функции | 7 |

**Функции верхнего уровня:**

- `hash_password(plain)` L11
- `verify_password(plain, hashed)` L15
- `create_access_token()` L22
- `create_refresh_token_payload()` L31
- `decode_token(token)` L40
- `decode_token_safe(token)` L45
- `parse_uuid(subject)` L52

### Файл: `backend/app/core/timezone.py`

| Свойство | Значение |
|----------|----------|
| Строк | 36 |
| Размер | 1,067 байт |
| Функции | 6 |

**Функции верхнего уровня:**

- `now_moscow()` L7
- `utc_now()` L11
- `to_moscow(dt)` L15
- `format_moscow_datetime(dt)` L21
- `format_moscow_date(d)` L26
- `add_seconds_to_start(started_at, offset_sec)` L31

### Файл: `backend/app/db/base.py`

| Свойство | Значение |
|----------|----------|
| Строк | 6 |
| Размер | 83 байт |
| Классы | 1 |

**Классы:**

- `Base` (строка 4)

### Файл: `backend/app/db/session.py`

| Свойство | Значение |
|----------|----------|
| Строк | 14 |
| Размер | 486 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `get_db()` L11

### Файл: `backend/app/main.py`

| Свойство | Значение |
|----------|----------|
| Строк | 67 |
| Размер | 2,182 байт |
| Функции | 2 |

**Функции верхнего уровня:**

- `lifespan(app)` L20
- `create_app()` L31

### Файл: `backend/app/middleware/request_id.py`

| Свойство | Значение |
|----------|----------|
| Строк | 21 |
| Размер | 774 байт |
| Классы | 1 |

**Классы:**

- `RequestIDMiddleware` (строка 12)
  - Docstring: Пробрасывает X-Request-ID: из заголовка или генерирует UUID, кладёт в request.state и ответ.
  - `dispatch(self, request, call_next)` L15

### Файл: `backend/app/models/__init__.py`

| Свойство | Значение |
|----------|----------|
| Строк | 37 |
| Размер | 914 байт |

### Файл: `backend/app/models/audit.py`

| Свойство | Значение |
|----------|----------|
| Строк | 23 |
| Размер | 1,040 байт |
| Классы | 1 |

**Классы:**

- `AuditLog` (строка 12)

### Файл: `backend/app/models/enums.py`

| Свойство | Значение |
|----------|----------|
| Строк | 30 |
| Размер | 851 байт |
| Классы | 2 |

**Классы:**

- `UserRole` (строка 4)
- `AuditActionType` (строка 10)

### Файл: `backend/app/models/logo.py`

| Свойство | Значение |
|----------|----------|
| Строк | 47 |
| Размер | 2,131 байт |
| Классы | 2 |

**Классы:**

- `Logo` (строка 11)
  - Docstring: Файл логотипа в медиатеке (переиспользуется между мероприятиями).
- `StreamEventLogo` (строка 30)
  - Docstring: Связь мероприятие ↔ логотип (многие-ко-многим с порядком).

### Файл: `backend/app/models/platform_extra.py`

| Свойство | Значение |
|----------|----------|
| Строк | 72 |
| Размер | 3,719 байт |
| Классы | 4 |

**Классы:**

- `Notification` (строка 13)
- `ProductAnalyticsEvent` (строка 25)
- `UserInvite` (строка 37)
- `BroadcastChecklist` (строка 55)

### Файл: `backend/app/models/stream.py`

| Свойство | Значение |
|----------|----------|
| Строк | 163 |
| Размер | 7,875 байт |
| Классы | 7 |

**Классы:**

- `StreamEvent` (строка 13)
- `StreamDayAssignment` (строка 49)
  - Docstring: Какой оператор ведёт конкретный день многодневного эфира (уникально по событию и дню).
- `StreamDay` (строка 69)
- `BroadcastSession` (строка 85)
- `SponsorMention` (строка 115)
- `MentionAdjustment` (строка 132)
- `StreamEventTemplate` (строка 149)
  - Docstring: Шаблон события: название шаблона, заголовок эфира по умолчанию, дни (URL/ключи).

### Файл: `backend/app/models/user.py`

| Свойство | Значение |
|----------|----------|
| Строк | 66 |
| Размер | 3,501 байт |
| Классы | 3 |

**Классы:**

- `User` (строка 12)
- `PasswordResetToken` (строка 39)
- `RefreshToken` (строка 52)

### Файл: `backend/app/schemas/__init__.py`

| Свойство | Значение |
|----------|----------|
| Строк | 36 |
| Размер | 834 байт |

### Файл: `backend/app/schemas/audit.py`

| Свойство | Значение |
|----------|----------|
| Строк | 26 |
| Размер | 509 байт |
| Классы | 2 |

**Классы:**

- `AuditLogOut` (строка 8)
- `AuditLogPage` (строка 21)

### Файл: `backend/app/schemas/auth.py`

| Свойство | Значение |
|----------|----------|
| Строк | 49 |
| Размер | 1,221 байт |
| Классы | 8 |

**Классы:**

- `LoginRequest` (строка 6)
- `ForgotPasswordIn` (строка 11)
- `ForgotPasswordOut` (строка 15)
- `PasswordResetValidateOut` (строка 21)
- `ResetPasswordIn` (строка 25)
  - `passwords_match(self)` L31
- `RefreshRequest` (строка 37)
- `TokenResponse` (строка 41)
- `MeOut` (строка 47)

### Файл: `backend/app/schemas/logo.py`

| Свойство | Значение |
|----------|----------|
| Строк | 25 |
| Размер | 538 байт |
| Классы | 3 |

**Классы:**

- `StreamLogoItemOut` (строка 7)
- `LogoLibraryItemOut` (строка 15)
- `LogoAttachBody` (строка 23)

### Файл: `backend/app/schemas/platform.py`

| Свойство | Значение |
|----------|----------|
| Строк | 77 |
| Размер | 1,758 байт |
| Классы | 10 |

**Классы:**

- `NotificationOut` (строка 9)
- `NotificationListOut` (строка 20)
- `AnalyticsIn` (строка 25)
- `InviteCreate` (строка 30)
- `InviteCreatedOut` (строка 35)
- `AcceptInviteIn` (строка 40)
- `ChecklistOut` (строка 47)
- `ChecklistUpdate` (строка 59)
- `AnalyticsRow` (строка 68)
- `AnalyticsSummaryOut` (строка 73)
  - Docstring: Агрегаты за последние 7 дней по имени события.

### Файл: `backend/app/schemas/profile.py`

| Свойство | Значение |
|----------|----------|
| Строк | 45 |
| Размер | 1,230 байт |
| Классы | 5 |

**Классы:**

- `ProfileUpdate` (строка 9)
- `ChangePasswordIn` (строка 19)
- `SessionOut` (строка 24)
- `MyActivityPage` (строка 34)
- `DashboardSummaryOut` (строка 41)

### Файл: `backend/app/schemas/report.py`

| Свойство | Значение |
|----------|----------|
| Строк | 24 |
| Размер | 506 байт |
| Классы | 2 |

**Классы:**

- `ReportMentionRow` (строка 7)
- `ReportMentionsOut` (строка 21)

### Файл: `backend/app/schemas/stats.py`

| Свойство | Значение |
|----------|----------|
| Строк | 40 |
| Размер | 1,026 байт |
| Классы | 3 |

**Классы:**

- `LockAssignmentOut` (строка 7)
- `OperatorDayStatsOut` (строка 13)
- `OperatorStatsOverviewOut` (строка 28)

### Файл: `backend/app/schemas/stream.py`

| Свойство | Значение |
|----------|----------|
| Строк | 177 |
| Размер | 5,883 байт |
| Классы | 15 |

**Классы:**

- `StreamDayIn` (строка 9)
- `StreamDayOut` (строка 16)
- `StreamEventCreate` (строка 26)
- `StreamLockBody` (строка 35)
- `BroadcastActualStartBody` (строка 43)
  - Docstring: Фактическое время начала эфира (когда картинка реально пошла). Без таймзоны — интерпретируется как МСК.
  - `naive_as_moscow(cls, v)` L50
- `DayAssignmentOut` (строка 56)
- `StreamEventUpdate` (строка 65)
  - `empty_content_url_to_none(cls, v)` L74
- `StreamDayLinkOut` (строка 80)
  - Docstring: День мероприятия и ссылка на трансляцию (для списка без захода в карточку).
- `StreamEventListOut` (строка 87)
- `BroadcastSessionOut` (строка 109)
- `StreamEventDetailOut` (строка 123)
- `SponsorMentionCreate` (строка 145)
- `SponsorMentionUpdate` (строка 149)
- `MentionAdjustmentOut` (строка 153)
- `SponsorMentionOut` (строка 163)

### Файл: `backend/app/schemas/templates.py`

| Свойство | Значение |
|----------|----------|
| Строк | 34 |
| Размер | 806 байт |
| Классы | 4 |

**Классы:**

- `StreamEventTemplateCreate` (строка 9)
- `StreamEventTemplateOut` (строка 16)
- `InstantiateTemplateBody` (строка 26)
- `TemplateFromEventBody` (строка 32)

### Файл: `backend/app/schemas/user.py`

| Свойство | Значение |
|----------|----------|
| Строк | 58 |
| Размер | 1,732 байт |
| Классы | 4 |

**Классы:**

- `UserOut` (строка 9)
  - `display_name(self)` L29
- `UserCreate` (строка 34)
- `UserCreatedOut` (строка 42)
- `UserUpdate` (строка 49)

### Файл: `backend/app/services/analytics_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 27 |
| Размер | 978 байт |
| Функции | 2 |

**Функции верхнего уровня:**

- `track_event(session)` L10
- `summary_last_days(session)` L17

### Файл: `backend/app/services/audit_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 79 |
| Размер | 2,435 байт |
| Функции | 4 |

**Функции верхнего уровня:**

- `list_audit_logs(session)` L12
- `write_audit(session)` L35
- `list_audit_logs_all(session)` L56
- `purge_audit_older_than(session)` L72

### Файл: `backend/app/services/auth_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 216 |
| Размер | 7,898 байт |
| Функции | 9 |

**Функции верхнего уровня:**

- `authenticate_user(session, email, password)` L20
- `_apply_last_login(user)` L30
- `login_user(session)` L35
- `refresh_access_token(session, refresh_token)` L70
- `create_fresh_session(session)` L91
- `logout_user(session)` L123
- `change_password(session)` L155
- `list_active_refresh_tokens(session)` L192
- `revoke_refresh_session_by_id(session)` L206

### Файл: `backend/app/services/broadcast_alert_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 149 |
| Размер | 5,362 байт |
| Функции | 5 |

**Функции верхнего уровня:**

- `_send_smtp_html_sync()` L25
- `_highest_reached_threshold(elapsed_hours)` L57
- `_send_long_broadcast_email()` L64
- `check_long_running_broadcasts(session)` L104
- `job_long_broadcast_alerts()` L141

### Файл: `backend/app/services/checklist_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 70 |
| Размер | 2,346 байт |
| Функции | 3 |

**Функции верхнего уровня:**

- `get_checklist_row(session)` L10
- `get_or_create_checklist(session)` L23
- `update_checklist(session)` L42

### Файл: `backend/app/services/dashboard_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 59 |
| Размер | 3,287 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `build_dashboard_summary(session)` L16

### Файл: `backend/app/services/email_html_layout.py`

| Свойство | Значение |
|----------|----------|
| Строк | 56 |
| Размер | 2,455 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `wrap_email_html()` L6

### Файл: `backend/app/services/email_report_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 192 |
| Размер | 7,277 байт |
| Функции | 8 |

**Функции верхнего уровня:**

- `_send_smtp_sync()` L23
- `_recipient_emails(session)` L60
- `_html_digest(session)` L70
- `send_period_report_email(session)` L112
- `previous_week_moscow_bounds(today)` L151
- `previous_month_bounds(today)` L159
- `job_weekly_report()` L166
- `job_monthly_report()` L180

### Файл: `backend/app/services/invite_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 84 |
| Размер | 3,177 байт |
| Функции | 2 |

**Функции верхнего уровня:**

- `create_invite(session)` L17
- `accept_invite(session, body)` L47

### Файл: `backend/app/services/logo_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 250 |
| Размер | 8,700 байт |
| Функции | 14 |

**Функции верхнего уровня:**

- `_safe_original_filename(name)` L34
- `logo_library_item(logo)` L42
- `_persist_one_logo(session)` L53
- `upload_logo(session)` L94
- `upload_logos_batch(session)` L101
- `list_library(session)` L119
- `_stream_logo_link(session)` L125
- `attach_logo_to_stream(session)` L137
- `detach_logo_from_stream(session)` L168
- `logo_file_abs_path(stored_path)` L188
- `get_logo_row(session, logo_id)` L193
- `assert_logo_on_stream(session)` L198
- `stream_zip_filename(title, moscow_date_str)` L208
- `build_stream_logos_zip(session)` L213

### Файл: `backend/app/services/notification_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 69 |
| Размер | 1,988 байт |
| Функции | 5 |

**Функции верхнего уровня:**

- `create_for_users_with_roles(session)` L11
- `count_unread(session)` L32
- `list_notifications(session)` L41
- `mark_read(session)` L54
- `mark_all_read(session)` L65

### Файл: `backend/app/services/password_reset_email_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 99 |
| Размер | 3,974 байт |
| Функции | 3 |

**Функции верхнего уровня:**

- `_send_password_reset_sync()` L16
- `send_password_reset_email()` L48
- `send_password_reset_email_task(to_email, reset_link, greeting_name)` L94

### Файл: `backend/app/services/password_reset_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 123 |
| Размер | 4,770 байт |
| Функции | 4 |

**Функции верхнего уровня:**

- `hash_reset_token(raw)` L19
- `request_password_reset(session)` L23
- `token_is_valid(session)` L68
- `reset_password_with_token(session)` L83

### Файл: `backend/app/services/profile_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 85 |
| Размер | 3,264 байт |
| Функции | 2 |

**Функции верхнего уровня:**

- `update_profile(session)` L15
- `save_avatar_file(session)` L56

### Файл: `backend/app/services/report_scheduler.py`

| Свойство | Значение |
|----------|----------|
| Строк | 45 |
| Размер | 1,543 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `setup_report_scheduler()` L16

### Файл: `backend/app/services/report_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 226 |
| Размер | 7,674 байт |
| Функции | 8 |

**Функции верхнего уровня:**

- `_range_utc_moscow_days(date_from, date_to)` L20
- `get_mentions_report(session)` L26
- `build_docx_report(rows)` L88
- `build_csv_report(rows)` L117
- `build_xlsx_report(rows)` L147
- `export_mentions_docx(session)` L180
- `export_mentions_csv(session)` L196
- `export_mentions_xlsx(session)` L212

### Файл: `backend/app/services/stats_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 151 |
| Размер | 5,704 байт |
| Функции | 7 |

**Функции верхнего уровня:**

- `_moscow_day_bounds_utc(d)` L19
- `_moscow_range_to_utc(day_from, day_to_inclusive)` L25
- `_week_mon_sun_moscow(d)` L31
- `_month_first_last(d)` L37
- `_count_broadcasts(session, operator_id, start_utc, end_utc)` L43
- `_count_mentions(session, operator_id, start_utc, end_utc)` L58
- `get_operator_stats_overview(session)` L74

### Файл: `backend/app/services/stream_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 1187 |
| Размер | 45,960 байт |
| Функции | 39 |

**Функции верхнего уровня:**

- `_mention_to_out(mention)` L46
- `_get_event(session, stream_id)` L71
- `_logos_for_stream(ev)` L87
- `assert_valid_stream_day(session, stream_id, day_index)` L108
- `_broadcast_restart_blocked_days(session)` L116
- `_day_blocked_for_new_broadcast(session)` L149
- `_assignment_operator_for_day(session, stream_id, day_index)` L156
- `_format_days_label(days)` L168
- `_assignment_summary_from_pairs(pairs)` L177
- `_load_assignment_pairs(session, stream_ids)` L192
- `_day_assignments_out(session, stream_id)` L210
- `_stream_has_assignments_to_other_than(session)` L223
- `_sync_legacy_locked_by(session, ev)` L237
- `_active_broadcast_ids(session)` L250
- `_ended_broadcast_ids(session)` L256
- `_ended_broadcast_days_by_event(session)` L262
- `_users_by_ids(session, user_ids)` L276
- `_locked_by_display_name(session, locked_by_user_id)` L283
- `list_stream_events(session)` L291
- `get_stream_event_detail(session, stream_id)` L357
- `_server_url_from_template_days(days_json)` L427
- `_sync_days(sess
---

## Статистика проекта

| Метрика | Значение |
|---------|----------|
| Файлов проанализировано | 144 |
| Директорий | 32 |
| HTTP маршрутов (оценка) | 52 |
| Python классов | 82 |
| Строк в reference | ~883,549 |
| Исходников включено полностью | 136 |

<p align="center"><i>Документация Ultra v2.0 · 2026-06-10</i></p>
