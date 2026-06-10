# Платформа эфиров MainStream — ИСЧЕРПЫВАЮЩАЯ ТЕХНИЧЕСКАЯ ДОКУМЕНТАЦИЯ

> **Версия документа:** 2.0 Ultra | **Дата:** 2026-06-10 23:46  
> **Проект:** Платформа для видеооператоров: стрим-события, блокировки, таймкоды спонсоров, WebSocket, отчёты Word  
> **Skill ID:** `streaming` | **Путь:** `/opt/streaming`  
> **Назначение:** полная передача заказчику + контекст AI-агента без повторного сканирования кода

---

# ЧАСТЬ I. EXECUTIVE SUMMARY

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

## 1.2 Статистика кодовой базы

| Метрика | Значение |
|---------|----------|
| Файлов проанализировано | 144 |
| Директорий | 32 |
| HTTP маршрутов (оценка) | 52 |
| Python классов | 82 |
| Строк в reference | ~883,549 |
| Исходников включено полностью | 136 |

## 1.3 Архитектурная схема

```
                    ┌─────────────────────────────────────┐
                    │  Клиент (браузер / Telegram / API)   │
                    └──────────────────┬──────────────────┘
                                       │ HTTPS
                    ┌──────────────────▼──────────────────┐
                    │  nginx :443 (streaming.mainstreamfs.ru)       │
                    └──────────────────┬──────────────────┘
                                       │ proxy_pass
                    ┌──────────────────▼──────────────────┐
                    │  127.0.0.1:8010 (Uvicorn) │
                    │  systemd: streaming-backend │
                    └──────────────────┬──────────────────┘
                                       │
                    ┌──────────────────▼──────────────────┐
                    │  /opt/streaming                              │
                    │  PostgreSQL: streaming                        │
                    └─────────────────────────────────────┘
```

---

# ЧАСТЬ II. ЗАВИСИМОСТИ И СТЕК

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

# ЧАСТЬ III. КАТАЛОГ ФАЙЛОВ (ПОЛНЫЙ)

| № | Директория | Файлов | Список |
|---|------------|--------|--------|
| 1 | `.` | 4 | `.env.example`, `README.md`, `docker-compose.yml`, `ТЗ-сервер.md` |
| 2 | `backend` | 4 | `Dockerfile`, `alembic.ini`, `pytest.ini`, `requirements.txt` |
| 3 | `backend/alembic` | 1 | `env.py` |
| 4 | `backend/app` | 2 | `__init__.py`, `main.py` |
| 5 | `backend/app/api` | 2 | `__init__.py`, `health.py` |
| 6 | `backend/app/api/v1` | 17 | `__init__.py`, `audit.py`, `auth.py`, `dashboard.py`, `event_templates.py`, `logos.py`, `mentions.py`, `notifications.py`… |
| 7 | `backend/app/core` | 6 | `__init__.py`, `config.py`, `deps.py`, `limiter.py`, `security.py`, `timezone.py` |
| 8 | `backend/app/db` | 3 | `__init__.py`, `base.py`, `session.py` |
| 9 | `backend/app/middleware` | 1 | `request_id.py` |
| 10 | `backend/app/models` | 7 | `__init__.py`, `audit.py`, `enums.py`, `logo.py`, `platform_extra.py`, `stream.py`, `user.py` |
| 11 | `backend/app/schemas` | 11 | `__init__.py`, `audit.py`, `auth.py`, `logo.py`, `platform.py`, `profile.py`, `report.py`, `stats.py`… |
| 12 | `backend/app/services` | 22 | `__init__.py`, `analytics_service.py`, `audit_service.py`, `auth_service.py`, `broadcast_alert_service.py`, `checklist_service.py`, `dashboard_service.py`, `email_html_layout.py`… |
| 13 | `backend/app/utils` | 6 | `__init__.py`, `client_ip.py`, `display_name.py`, `phone_ru.py`, `timecode.py`, `webhook.py` |
| 14 | `backend/app/websocket` | 2 | `__init__.py`, `hub.py` |
| 15 | `backend/scripts` | 3 | `__init__.py`, `seed.py`, `test_smtp.py` |
| 16 | `backend/tests` | 4 | `test_health.py`, `test_logo_zip.py`, `test_timecode.py`, `test_timezone_format.py` |
| 17 | `frontend` | 6 | `index.html`, `package-lock.json`, `package.json`, `tsconfig.json`, `tsconfig.node.json`, `vite.config.ts` |
| 18 | `frontend/.storybook` | 2 | `main.ts`, `preview.tsx` |
| 19 | `frontend/e2e` | 2 | `playwright.config.ts`, `smoke.spec.ts` |
| 20 | `frontend/src` | 4 | `App.tsx`, `main.tsx`, `theme.ts`, `vite-env.d.ts` |
| 21 | `frontend/src/api` | 2 | `client.ts`, `types.ts` |
| 22 | `frontend/src/api/generated` | 1 | `README.md` |
| 23 | `frontend/src/auth` | 1 | `AuthContext.tsx` |
| 24 | `frontend/src/components` | 7 | `AnalyticsTracker.tsx`, `BrandLogo.tsx`, `BroadcastActualStartPanel.tsx`, `NotificationBell.tsx`, `OperatorStatsPanel.tsx`, `ProtectedRoute.tsx`, `SuggestPasswordModal.tsx` |
| 25 | `frontend/src/content` | 1 | `onboardingRoleGuides.tsx` |
| 26 | `frontend/src/hooks` | 1 | `useStreamWs.ts` |
| 27 | `frontend/src/layouts` | 1 | `AppLayout.tsx` |
| 28 | `frontend/src/pages` | 13 | `DashboardPage.tsx`, `FirstLoginPasswordPage.tsx`, `ForgotPasswordPage.tsx`, `LoginPage.tsx`, `ManagerStreamPage.tsx`, `ManagerStreamsPage.tsx`, `OnboardingPage.tsx`, `OperatorEventPage.tsx`… |
| 29 | `frontend/src/stories` | 1 | `BrandLogo.stories.tsx` |
| 30 | `frontend/src/styles` | 1 | `global.css` |
| 31 | `frontend/src/utils` | 4 | `auditLabels.ts`, `datetime.ts`, `normalizeRuMobilePhone.ts`, `userDisplay.ts` |
| 32 | `nginx` | 2 | `Dockerfile`, `nginx.conf` |

---

# ЧАСТЬ IV. API И МАРШРУТЫ (ПОЛНЫЙ РЕЕСТР)

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

# ЧАСТЬ V. МОДЕЛИ И КЛАССЫ

### `AuditPurgeBody` (строка 81)

### `Settings` (строка 6)
- `cors_origins_list(self)` — строка 56

### `Base` (строка 4)

### `RequestIDMiddleware` (строка 12)
> Пробрасывает X-Request-ID: из заголовка или генерирует UUID, кладёт в request.state и ответ.

- `dispatch(self, request, call_next)` — строка 15

### `AuditLog` (строка 12)

### `UserRole` (строка 4)

### `AuditActionType` (строка 10)

### `Logo` (строка 11)
> Файл логотипа в медиатеке (переиспользуется между мероприятиями).


### `StreamEventLogo` (строка 30)
> Связь мероприятие ↔ логотип (многие-ко-многим с порядком).


### `Notification` (строка 13)

### `ProductAnalyticsEvent` (строка 25)

### `UserInvite` (строка 37)

### `BroadcastChecklist` (строка 55)

### `StreamEvent` (строка 13)

### `StreamDayAssignment` (строка 49)
> Какой оператор ведёт конкретный день многодневного эфира (уникально по событию и дню).


### `StreamDay` (строка 69)

### `BroadcastSession` (строка 85)

### `SponsorMention` (строка 115)

### `MentionAdjustment` (строка 132)

### `StreamEventTemplate` (строка 149)
> Шаблон события: название шаблона, заголовок эфира по умолчанию, дни (URL/ключи).


### `User` (строка 12)

### `PasswordResetToken` (строка 39)

### `RefreshToken` (строка 52)

### `AuditLogOut` (строка 8)

### `AuditLogPage` (строка 21)

### `LoginRequest` (строка 6)

### `ForgotPasswordIn` (строка 11)

### `ForgotPasswordOut` (строка 15)

### `PasswordResetValidateOut` (строка 21)

### `ResetPasswordIn` (строка 25)
- `passwords_match(self)` — строка 31

### `RefreshRequest` (строка 37)

### `TokenResponse` (строка 41)

### `MeOut` (строка 47)

### `StreamLogoItemOut` (строка 7)

### `LogoLibraryItemOut` (строка 15)

### `LogoAttachBody` (строка 23)

### `NotificationOut` (строка 9)

### `NotificationListOut` (строка 20)

### `AnalyticsIn` (строка 25)

### `InviteCreate` (строка 30)

### `InviteCreatedOut` (строка 35)

### `AcceptInviteIn` (строка 40)

### `ChecklistOut` (строка 47)

### `ChecklistUpdate` (строка 59)

### `AnalyticsRow` (строка 68)

### `AnalyticsSummaryOut` (строка 73)
> Агрегаты за последние 7 дней по имени события.


### `ProfileUpdate` (строка 9)

### `ChangePasswordIn` (строка 19)

### `SessionOut` (строка 24)

### `MyActivityPage` (строка 34)

### `DashboardSummaryOut` (строка 41)

### `ReportMentionRow` (строка 7)

### `ReportMentionsOut` (строка 21)

### `LockAssignmentOut` (строка 7)

### `OperatorDayStatsOut` (строка 13)

### `OperatorStatsOverviewOut` (строка 28)

### `StreamDayIn` (строка 9)

### `StreamDayOut` (строка 16)

### `StreamEventCreate` (строка 26)

### `StreamLockBody` (строка 35)

### `BroadcastActualStartBody` (строка 43)
> Фактическое время начала эфира (когда картинка реально пошла). Без таймзоны — интерпретируется как МСК.

- `naive_as_moscow(cls, v)` — строка 50

### `DayAssignmentOut` (строка 56)

### `StreamEventUpdate` (строка 65)
- `empty_content_url_to_none(cls, v)` — строка 74

### `StreamDayLinkOut` (строка 80)
> День мероприятия и ссылка на трансляцию (для списка без захода в карточку).


### `StreamEventListOut` (строка 87)

### `BroadcastSessionOut` (строка 109)

### `StreamEventDetailOut` (строка 123)

### `SponsorMentionCreate` (строка 145)

### `SponsorMentionUpdate` (строка 149)

### `MentionAdjustmentOut` (строка 153)

### `SponsorMentionOut` (строка 163)

### `StreamEventTemplateCreate` (строка 9)

### `StreamEventTemplateOut` (строка 16)

### `InstantiateTemplateBody` (строка 26)

### `TemplateFromEventBody` (строка 32)

### `UserOut` (строка 9)
- `display_name(self)` — строка 29

### `UserCreate` (строка 34)

### `UserCreatedOut` (строка 42)

### `UserUpdate` (строка 49)

### `WelcomeEmailPayload` (строка 22)

### `CreateUserOutcome` (строка 29)

### `StreamEventHub` (строка 8)
- `__init__(self, max_subscribers_per_room)` — строка 9
- `connect(self, stream_event_id, websocket)` — строка 13
- `disconnect(self, stream_event_id, websocket)` — строка 22
- `notify_presence(self, stream_event_id)` — строка 31
- `_publish_presence(self, stream_event_id)` — строка 34
- `publish(self, stream_event_id, message)` — строка 46


---

# ЧАСТЬ VI. ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ

| Переменная |
|------------|
| `DATABASE_URL` |
| `DATABASE_URL_SYNC` |
| `JWT_SECRET` |
| `JWT_ACCESS_EXPIRE_MINUTES` |
| `JWT_REFRESH_EXPIRE_DAYS` |
| `CORS_ORIGINS` |
| `REFRESH_COOKIE_NAME` |
| `REFRESH_COOKIE_SECURE` |
| `REFRESH_COOKIE_SAMESITE` |
| `TZ` |
| `APP_VERSION` |

```env
# Куда класть: для systemd/uvicorn — backend/.env (рабочий каталог backend).
# Docker Compose: те же переменные в .env в корне репозитория / в environment сервиса backend.

# PostgreSQL (async URL для приложения)
DATABASE_URL=postgresql+asyncpg://streaming:streaming@localhost:5432/streaming

# Для Alembic (синхронный драйвер)
DATABASE_URL_SYNC=postgresql://streaming:streaming@localhost:5432/streaming

JWT_SECRET=change-me-to-a-long-random-string-in-production
JWT_ACCESS_EXPIRE_MINUTES=30
JWT_REFRESH_EXPIRE_DAYS=7

# CORS: через запятую, для dev: http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Cookie refresh (в prod задать свой домен)
REFRESH_COOKIE_NAME=refresh_token
REFRESH_COOKIE_SECURE=false
REFRESH_COOKIE_SAMESITE=lax

TZ=Europe/Moscow

# Версия API (отдаётся в /health, для Sentry release)
APP_VERSION=1.0.0

# Каталог загрузок (аватары и т.д.). В проде лучше абсолютный путь, например /var/lib/streaming/uploads
# UPLOAD_DIR=uploads

# Публичный URL панели (обязательно для ссылок в письмах: вход, сброс пароля, логотип)
# Пример: https://ops.example.ru — в письме сброса будет {APP_PUBLIC_BASE_URL}/reset-password?token=...
# APP_PUBLIC_BASE_URL=

# Срок жизни ссылки сброса пароля (минуты), по умолчанию 10
# PASSWORD_RESET_EXPIRE_MINUTES=10

# Sentry (опционально): backend DSN — ошибки API; на фронте задайте VITE_SENTRY_DSN в frontend/.env
# SENTRY_DSN=
# SENTRY_ENVIRONMENT=production
# SENTRY_TRACES_SAMPLE_RATE=0.1

# Внешний webhook: JSON POST при старте/остановке эфира (опционально)
# EXTERNAL_WEBHOOK_URL=https://hooks.example.com/stream

# SMTP: приветственные письма при создании пользователя + еженедельные/ежемесячные отчёты (Word)
# Пустой SMTP_HOST — почта не отправляется (пользователь всё равно создаётся)
# SMTP_HOST=smtp.example.com
# SMTP_PORT=587
# SMTP_USER=
# SMTP_PASSWORD=
# SMTP_FROM=noreply@example.com
# SMTP_USE_TLS=true
# Для порта 465 (SSL сразу, часто Beget): SMTP_USE_SSL=true и SMTP_USE_TLS=false
# SMTP_USE_SSL=false

# --- Сид пользователей (только для python -m scripts.seed; в проде задайте свои почты)
# SEED_ADMIN_EMAIL=admin@example.com
# SEED_MANAGER_EMAIL=manager@example.com
# SEED_OPERATOR_EMAIL=operator@example.com
# SEED_PASSWORD=ChangeMe123!
# Только суперадмин, без демо-мероприятия: SEED_ONLY_SUPERADMIN=1

# --- Frontend (создайте frontend/.env при локальной разработке)
# VITE_SENTRY_DSN=

# --- Только для docker compose build (backend): если pip внутри образа не достучится до pypi.org ---
# (таймауты, SSL UNEXPECTED_EOF — часто DPI/антивирус/провайдер). Скопируйте в .env и раскомментируйте одну строку:
# PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
# PIP_INDEX_URL=https://pypi.mirrors.ustc.edu.cn/simple

```

---

# ЧАСТЬ VII. БАЗА ДАННЫХ

_SQLite/PostgreSQL схема — см. models в коде._

---

# ЧАСТЬ VIII. SYSTEMD (PRODUCTION)

### Unit: `streaming-backend.service`

```ini
[Unit]
Description=Streaming platform FastAPI (uvicorn)
After=network.target postgresql.service
[Service]
Type=simple
User=root
WorkingDirectory=/opt/streaming/backend
EnvironmentFile=/opt/streaming/backend/.env
ExecStart=/opt/streaming/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8010 --workers 2
Restart=on-failure
RestartSec=5
[Install]
WantedBy=multi-user.target
```

---

# ЧАСТЬ IX. NGINX (PRODUCTION)

### `streaming.conf`

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}
map $http_x_request_id $proxy_request_id {
    default $http_x_request_id;
    ''      $request_id;
}
server {
    server_name streaming.mainstreamfs.ru;
    include /etc/nginx/snippets/deny-sensitive.conf;
    root /opt/streaming/frontend/dist;
    index index.html;
    location /api/ {
        proxy_pass http://127.0.0.1:8010;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Request-ID $proxy_request_id;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_read_timeout 86400;
    }
    location /health {
        proxy_pass http://127.0.0.1:8010;
        proxy_set_header Host $host;
        proxy_set_header X-Request-ID $proxy_request_id;
    }
    location /openapi.json {
        proxy_pass http://127.0.0.1:8010;
        proxy_set_header Host $host;
    }
    location /uploads/ {
        proxy_pass http://127.0.0.1:8010;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location / {
        try_files $uri $uri/ /index.html;
    }
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self' ws: wss: http: https:; font-src 'self' data:; frame-ancestors 'self'; base-uri 'self'" always;

    listen [::]:443 ssl; # managed by Certbot
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/streaming.mainstreamfs.ru/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/streaming.mainstreamfs.ru/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

server {
    if ($host = streaming.mainstreamfs.ru) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    listen [::]:80;
    server_name streaming.mainstreamfs.ru;
    return 404; # managed by Certbot


}

```

---

# ЧАСТЬ X. GIT

| Поле | Значение |
|------|----------|
| Ветка | `master` |
| Remote | `origin	https://github.com/AndryshaDenisov1488/streamreportadvertising.git (fetch)<br>origin	https://github.com/AndryshaDenisov1488/streamreportadvertising.git (push)` |
| Последний коммит | `c8260dc fix(operator): improve idle reminder overlay text readability (AndryshaDenisov1488, 2026-06-09 16:51:15 +0300)` |

**Статус:**
```
On branch master
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.cursor/
	backups/

no changes added to commit (use "git add" and/or "git commit -a")
```

**История (30 коммитов):**
```
c8260dc fix(operator): improve idle reminder overlay text readability
18d5557 docs: ТЗ-сервер.md (размещение на хосте); бэкапы: хранение 7 дней там, где менялись скрипты
5688296 feat(operator): show completed broadcast days in status
a794152 feat(alerts): notify operators about overly long broadcasts
af53a56 feat(operator): show nearby events and ended broadcast status
af94daf фикс
72a66f8 feat(mentions): add mention deletion with confirmation
b39bd38 fix(stream): block superadmin lock/unlock when operators assigned
cf2b070 feat(stream): allow operator and manager to realign ended broadcast start
28fa4c8 feat(manager): realign ended broadcast start; fix report grouping for Word
c71f5c2 feat(operator): take all days, require assignment to start, block restart after long broadcast
75eae69 feat(auth): password reset email flow, link valid 10 minutes
e2cb703 fix(ui): explicit upload button for stream logos modal
3e9399e fix(auth): refresh access on 401, WS auth without query token
e59c1cb feat(manager): колонка копирования ссылок на трансляцию по дням в списке
bb916e7 feat(broadcast): фактическое время начала эфира и сдвиг таймкодов
dcedb29 fix(operator): копирование ссылок по клику с подсказкой и тостом
7d11f16 feat(logos): пакетная загрузка нескольких файлов (upload-batch)
f9d042a feat(logos): медиатека логотипов, content_url, ZIP и скачивание
b0cc6fb фикс
44c797a docs: server inventory for xkvlorcrjx (ports, paths, domains)
fc02940 feat(users): last login time and IP for admin list
77d852d docs(copy): replace federation wording with MainStream video operator service
aa18c30 docs(env): document SEED_ONLY_SUPERADMIN
c684dee feat(seed): SEED_ONLY_SUPERADMIN for single-admin deploy
a280983 feat(manager): template server URL in new event, checklist per day with 6 items
a7f8169 feat: email login+password block, RU phone normalize, onboarding phone
8cbbe80 feat(onboarding): detailed role training, remove duplicate role copy
78fff6b feat: HTML email layout, first-login password step, always auto-generated passwords
f6fd025 fix(smtp): use send_message for UTF-8 subject and body
```

**Контрибьюторы:**
```
40	Andrysha1488
     2	AndryshaDenisov1488
```

---

# ЧАСТЬ XI. ОПЕРАЦИИ

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

# ЧАСТЬ XII. ПОФАЙЛОВЫЙ АНАЛИЗ

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
- `_sync_days(session, stream_event_id, duration_days, days_input)` L439
- `create_stream_event(session)` L487
- `update_stream_event(session)` L521
- `delete_stream_event(session)` L557
- `lock_stream(session)` L579
- `unlock_stream(session)` L677
- `_can_control_broadcast(actor, ev, session_operator_id)` L724
- `_can_realign_broadcast_start(actor, ev, session_operator_id)` L732
- `_can_realign_ended_broadcast(actor, bs)` L742

### Файл: `backend/app/services/template_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 132 |
| Размер | 4,331 байт |
| Функции | 5 |

**Функции верхнего уровня:**

- `list_templates(session)` L17
- `create_template(session)` L22
- `template_from_event(session)` L57
- `delete_template(session)` L93
- `instantiate_template(session)` L111

### Файл: `backend/app/services/user_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 207 |
| Размер | 7,058 байт |
| Классы | 2 |
| Функции | 6 |

**Классы:**

- `WelcomeEmailPayload` (строка 22)
- `CreateUserOutcome` (строка 29)

**Функции верхнего уровня:**

- `list_users(session)` L35
- `get_user(session, user_id)` L40
- `create_user(session)` L48
- `send_welcome_email_task(payload)` L102
- `update_user(session)` L116
- `delete_user(session)` L185

### Файл: `backend/app/services/welcome_email_service.py`

| Свойство | Значение |
|----------|----------|
| Строк | 134 |
| Размер | 5,699 байт |
| Функции | 3 |

**Функции верхнего уровня:**

- `_role_label_ru(role)` L14
- `_send_welcome_sync()` L22
- `send_welcome_email()` L54

### Файл: `backend/app/utils/client_ip.py`

| Свойство | Значение |
|----------|----------|
| Строк | 18 |
| Размер | 555 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `client_ip_from_request(request)` L6

### Файл: `backend/app/utils/display_name.py`

| Свойство | Значение |
|----------|----------|
| Строк | 7 |
| Размер | 165 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `user_display_name(user)` L4

### Файл: `backend/app/utils/phone_ru.py`

| Свойство | Значение |
|----------|----------|
| Строк | 34 |
| Размер | 1,483 байт |
| Функции | 2 |

**Функции верхнего уровня:**

- `normalize_ru_mobile_phone(raw)` L4
- `normalize_ru_mobile_phone_or_empty(raw)` L26

### Файл: `backend/app/utils/timecode.py`

| Свойство | Значение |
|----------|----------|
| Строк | 6 |
| Размер | 171 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `seconds_to_hhmmss(total_sec)` L1

### Файл: `backend/app/utils/webhook.py`

| Свойство | Значение |
|----------|----------|
| Строк | 20 |
| Размер | 533 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `post_external_webhook(event_type, payload)` L10

### Файл: `backend/app/websocket/hub.py`

| Свойство | Значение |
|----------|----------|
| Строк | 56 |
| Размер | 2,079 байт |
| Классы | 1 |

**Классы:**

- `StreamEventHub` (строка 8)
  - `__init__(self, max_subscribers_per_room)` L9
  - `connect(self, stream_event_id, websocket)` L13
  - `disconnect(self, stream_event_id, websocket)` L22
  - `notify_presence(self, stream_event_id)` L31
  - `_publish_presence(self, stream_event_id)` L34
  - `publish(self, stream_event_id, message)` L46

### Файл: `backend/pytest.ini`

| Свойство | Значение |
|----------|----------|
| Строк | 4 |
| Размер | 47 байт |

### Файл: `backend/requirements.txt`

| Свойство | Значение |
|----------|----------|
| Строк | 23 |
| Размер | 448 байт |

### Файл: `backend/scripts/__init__.py`

| Свойство | Значение |
|----------|----------|
| Строк | 2 |
| Размер | 82 байт |

### Файл: `backend/scripts/seed.py`

| Свойство | Значение |
|----------|----------|
| Строк | 136 |
| Размер | 4,996 байт |
| Функции | 2 |

**Функции верхнего уровня:**

- `_seed_env()` L29
- `main()` L37

### Файл: `backend/scripts/test_smtp.py`

| Свойство | Значение |
|----------|----------|
| Строк | 79 |
| Размер | 3,154 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `main()` L21

### Файл: `backend/tests/test_health.py`

| Свойство | Значение |
|----------|----------|
| Строк | 16 |
| Размер | 440 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `test_health_ok()` L8

### Файл: `backend/tests/test_logo_zip.py`

| Свойство | Значение |
|----------|----------|
| Строк | 13 |
| Размер | 417 байт |
| Функции | 2 |

**Функции верхнего уровня:**

- `test_stream_zip_filename_uses_title_and_date()` L4
- `test_stream_zip_filename_empty_title_fallback()` L10

### Файл: `backend/tests/test_timecode.py`

| Свойство | Значение |
|----------|----------|
| Строк | 10 |
| Размер | 326 байт |
| Функции | 1 |

**Функции верхнего уровня:**

- `test_seconds_to_hhmmss()` L4

### Файл: `backend/tests/test_timezone_format.py`

| Свойство | Значение |
|----------|----------|
| Строк | 20 |
| Размер | 589 байт |
| Функции | 3 |

**Функции верхнего уровня:**

- `test_format_moscow_datetime_from_utc()` L7
- `test_format_moscow_date()` L12
- `test_to_moscow_naive_utc()` L16

### Файл: `docker-compose.yml`

| Свойство | Значение |
|----------|----------|
| Строк | 51 |
| Размер | 1,317 байт |

### Файл: `frontend/.storybook/main.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 25 |
| Размер | 613 байт |

### Файл: `frontend/.storybook/preview.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 22 |
| Размер | 484 байт |

### Файл: `frontend/e2e/playwright.config.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 21 |
| Размер | 533 байт |

### Файл: `frontend/e2e/smoke.spec.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 7 |
| Размер | 232 байт |

### Файл: `frontend/index.html`

| Свойство | Значение |
|----------|----------|
| Строк | 28 |
| Размер | 1,025 байт |

### Файл: `frontend/package-lock.json`

| Свойство | Значение |
|----------|----------|
| Строк | 9198 |
| Размер | 329,594 байт |

### Файл: `frontend/package.json`

| Свойство | Значение |
|----------|----------|
| Строк | 40 |
| Размер | 1,186 байт |

### Файл: `frontend/src/App.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 109 |
| Размер | 3,037 байт |

### Файл: `frontend/src/api/client.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 378 |
| Размер | 11,303 байт |

### Файл: `frontend/src/api/generated/README.md`

| Свойство | Значение |
|----------|----------|
| Строк | 8 |
| Размер | 309 байт |

### Файл: `frontend/src/api/types.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 197 |
| Размер | 4,968 байт |

### Файл: `frontend/src/auth/AuthContext.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 81 |
| Размер | 2,038 байт |

### Файл: `frontend/src/components/AnalyticsTracker.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 34 |
| Размер | 922 байт |

### Файл: `frontend/src/components/BrandLogo.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 32 |
| Размер | 828 байт |

### Файл: `frontend/src/components/BroadcastActualStartPanel.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 92 |
| Размер | 3,210 байт |

### Файл: `frontend/src/components/NotificationBell.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 107 |
| Размер | 3,330 байт |

### Файл: `frontend/src/components/OperatorStatsPanel.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 194 |
| Размер | 5,964 байт |

### Файл: `frontend/src/components/ProtectedRoute.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 48 |
| Размер | 1,254 байт |

### Файл: `frontend/src/components/SuggestPasswordModal.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 59 |
| Размер | 1,765 байт |

### Файл: `frontend/src/content/onboardingRoleGuides.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 194 |
| Размер | 11,440 байт |

### Файл: `frontend/src/hooks/useStreamWs.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 47 |
| Размер | 1,168 байт |

### Файл: `frontend/src/layouts/AppLayout.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 179 |
| Размер | 6,357 байт |

### Файл: `frontend/src/main.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 50 |
| Размер | 1,424 байт |

### Файл: `frontend/src/pages/DashboardPage.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 152 |
| Размер | 5,394 байт |

### Файл: `frontend/src/pages/FirstLoginPasswordPage.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 116 |
| Размер | 4,633 байт |

### Файл: `frontend/src/pages/ForgotPasswordPage.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 89 |
| Размер | 3,492 байт |

### Файл: `frontend/src/pages/LoginPage.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 79 |
| Размер | 2,912 байт |

### Файл: `frontend/src/pages/ManagerStreamPage.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 702 |
| Размер | 26,726 байт |

### Файл: `frontend/src/pages/ManagerStreamsPage.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 612 |
| Размер | 21,573 байт |

### Файл: `frontend/src/pages/OnboardingPage.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 259 |
| Размер | 10,580 байт |

### Файл: `frontend/src/pages/OperatorEventPage.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 1294 |
| Размер | 53,617 байт |

### Файл: `frontend/src/pages/OperatorHomePage.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 130 |
| Размер | 5,041 байт |

### Файл: `frontend/src/pages/ProfilePage.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 367 |
| Размер | 12,807 байт |

### Файл: `frontend/src/pages/ResetPasswordPage.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 160 |
| Размер | 5,749 байт |

### Файл: `frontend/src/pages/RoleHome.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 13 |
| Размер | 299 байт |

### Файл: `frontend/src/pages/SuperadminPage.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 514 |
| Размер | 16,851 байт |

### Файл: `frontend/src/stories/BrandLogo.stories.tsx`

| Свойство | Значение |
|----------|----------|
| Строк | 16 |
| Размер | 321 байт |

### Файл: `frontend/src/styles/global.css`

| Свойство | Значение |
|----------|----------|
| Строк | 102 |
| Размер | 2,355 байт |

### Файл: `frontend/src/theme.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 49 |
| Размер | 1,180 байт |

### Файл: `frontend/src/utils/auditLabels.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 96 |
| Размер | 3,812 байт |

### Файл: `frontend/src/utils/datetime.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 31 |
| Размер | 831 байт |

### Файл: `frontend/src/utils/normalizeRuMobilePhone.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 27 |
| Размер | 922 байт |

### Файл: `frontend/src/utils/userDisplay.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 16 |
| Размер | 544 байт |

### Файл: `frontend/src/vite-env.d.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 10 |
| Размер | 157 байт |

### Файл: `frontend/tsconfig.json`

| Свойство | Значение |
|----------|----------|
| Строк | 25 |
| Размер | 573 байт |

### Файл: `frontend/tsconfig.node.json`

| Свойство | Значение |
|----------|----------|
| Строк | 12 |
| Размер | 233 байт |

### Файл: `frontend/vite.config.ts`

| Свойство | Значение |
|----------|----------|
| Строк | 55 |
| Размер | 1,213 байт |

### Файл: `nginx/Dockerfile`

| Свойство | Значение |
|----------|----------|
| Строк | 12 |
| Размер | 302 байт |

### Файл: `nginx/nginx.conf`

| Свойство | Значение |
|----------|----------|
| Строк | 59 |
| Размер | 1,732 байт |

### Файл: `ТЗ-сервер.md`

| Свойство | Значение |
|----------|----------|
| Строк | 28 |
| Размер | 1,290 байт |

---

# ЧАСТЬ XIII. ПОЛНЫЙ ИСХОДНЫЙ КОД ВСЕХ ФАЙЛОВ



---

## Исходный код: `.env.example`

> 70 строк, 3,515 байт

```example
# Куда класть: для systemd/uvicorn — backend/.env (рабочий каталог backend).
# Docker Compose: те же переменные в .env в корне репозитория / в environment сервиса backend.

# PostgreSQL (async URL для приложения)
DATABASE_URL=postgresql+asyncpg://streaming:streaming@localhost:5432/streaming

# Для Alembic (синхронный драйвер)
DATABASE_URL_SYNC=postgresql://streaming:streaming@localhost:5432/streaming

JWT_SECRET=change-me-to-a-long-random-string-in-production
JWT_ACCESS_EXPIRE_MINUTES=30
JWT_REFRESH_EXPIRE_DAYS=7

# CORS: через запятую, для dev: http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Cookie refresh (в prod задать свой домен)
REFRESH_COOKIE_NAME=refresh_token
REFRESH_COOKIE_SECURE=false
REFRESH_COOKIE_SAMESITE=lax

TZ=Europe/Moscow

# Версия API (отдаётся в /health, для Sentry release)
APP_VERSION=1.0.0

# Каталог загрузок (аватары и т.д.). В проде лучше абсолютный путь, например /var/lib/streaming/uploads
# UPLOAD_DIR=uploads

# Публичный URL панели (обязательно для ссылок в письмах: вход, сброс пароля, логотип)
# Пример: https://ops.example.ru — в письме сброса будет {APP_PUBLIC_BASE_URL}/reset-password?token=...
# APP_PUBLIC_BASE_URL=

# Срок жизни ссылки сброса пароля (минуты), по умолчанию 10
# PASSWORD_RESET_EXPIRE_MINUTES=10

# Sentry (опционально): backend DSN — ошибки API; на фронте задайте VITE_SENTRY_DSN в frontend/.env
# SENTRY_DSN=
# SENTRY_ENVIRONMENT=production
# SENTRY_TRACES_SAMPLE_RATE=0.1

# Внешний webhook: JSON POST при старте/остановке эфира (опционально)
# EXTERNAL_WEBHOOK_URL=https://hooks.example.com/stream

# SMTP: приветственные письма при создании пользователя + еженедельные/ежемесячные отчёты (Word)
# Пустой SMTP_HOST — почта не отправляется (пользователь всё равно создаётся)
# SMTP_HOST=smtp.example.com
# SMTP_PORT=587
# SMTP_USER=
# SMTP_PASSWORD=
# SMTP_FROM=noreply@example.com
# SMTP_USE_TLS=true
# Для порта 465 (SSL сразу, часто Beget): SMTP_USE_SSL=true и SMTP_USE_TLS=false
# SMTP_USE_SSL=false

# --- Сид пользователей (только для python -m scripts.seed; в проде задайте свои почты)
# SEED_ADMIN_EMAIL=admin@example.com
# SEED_MANAGER_EMAIL=manager@example.com
# SEED_OPERATOR_EMAIL=operator@example.com
# SEED_PASSWORD=ChangeMe123!
# Только суперадмин, без демо-мероприятия: SEED_ONLY_SUPERADMIN=1

# --- Frontend (создайте frontend/.env при локальной разработке)
# VITE_SENTRY_DSN=

# --- Только для docker compose build (backend): если pip внутри образа не достучится до pypi.org ---
# (таймауты, SSL UNEXPECTED_EOF — часто DPI/антивирус/провайдер). Скопируйте в .env и раскомментируйте одну строку:
# PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
# PIP_INDEX_URL=https://pypi.mirrors.ustc.edu.cn/simple

```


---

## Исходный код: `README.md`

> 453 строк, 19,563 байт

```md
# Платформа эфиров MainStream

> Полная техническая документация: [.cursor/skills/streaming/reference.md](.cursor/skills/streaming/reference.md)  
> AI skill: [.cursor/skills/streaming/SKILL.md](.cursor/skills/streaming/SKILL.md)

---

## Содержание

- [О проекте](#о-проекте)
- [Архитектура](#архитектура)
- [Функциональность](#функциональность)
- [API](#api)
- [Установка и запуск](#установка-и-запуск)
- [Деплой на сервер](#деплой-на-сервер)
- [Переменные окружения](#переменные-окружения)
- [Структура каталогов](#структура-каталогов)
- [Бэкапы и безопасность](#бэкапы-и-безопасность)
- [Документация](#документация)

---

## О проекте

**Платформа эфиров MainStream** — Управление видеоэфирами и таймкодами.

| Параметр | Значение |
|----------|----------|
| Бренд / заказчик | MainStream |
| Production URL | https://streaming.mainstreamfs.ru |
| Backend порт (localhost) | 8010 |
| База данных | PostgreSQL: streaming |
| ОС сервера | Ubuntu 22.04 (VPS Beget) |
| Процесс-менеджер | systemd |
| Reverse proxy | nginx + Let's Encrypt |
| Пользователь сервиса | root |
| Файлов в репозитории (анализ) | 154 |
| Строк кода (оценка) | 13,256 |

### Назначение системы

Система развёрнута на сервере `xkvlorcrjx` (45.12.237.105) и обслуживается в составе экосистемы MainStream.
Все HTTP-сервисы слушают только `127.0.0.1`; внешний доступ — через nginx (443/SSL).

---

---

## Архитектура

### Стек технологий

alembic, antd, fastapi, pydantic, react, sqlalchemy, typescript, uvicorn, vite

### Структура верхнего уровня

```
.env.example
Mainstream_logo_Black and 1
```

---

---

## Функциональность

# Платформа эфиров и спонсорских упоминаний

Сервис для видеооператоров MainStream: управление стрим-событиями, блокировки операторов, таймкоды упоминаний (Europe/Moscow), аудит, отчёты в Word.

## Стек

- **Backend:** FastAPI, SQLAlchemy 2 async, PostgreSQL, Alembic, JWT (access + refresh cookie), WebSocket
- **Frontend:** React 18, Vite, TypeScript, Ant Design, TanStack Query
- **Инфра:** Docker Compose, Nginx

## Возможности платформы (обзор)

| Область | Что сделано |
|--------|-------------|
| Наблюдаемость | Заголовок `X-Request-ID`, опционально **Sentry** (backend + `VITE_SENTRY_DSN` на фронте) |
| Health | `GET /health` (liveness), `GET /health/ready` (БД + ревизия Alembic) |
| Безопасность | CSP в Nginx, проброс `X-Request-ID`; cookie refresh настраиваются через `REFRESH_COOKIE_*` |
| WebSocket | Лимит подписчиков на комнату, сообщения **presence** (число зрителей пульта) |
| Уведомления | Таблица `notifications`, API `/notifications`, колокольчик в шапке; при старте эфира — уведомления менеджерам/админам |
| Интеграции | `EXTERNAL_WEBHOOK_URL` — POST при start/stop эфира |
| Аудит | Выгрузка **CSV** (`GET /api/v1/audit-logs/export.csv`), очистка `POST /audit-logs/purge` |
| Продуктовая аналитика | `POST /analytics/events`, сводка `/analytics/summary` (суперадмин, вкладка «Продукт») |
| Приглашения | `POST /users/invites`, регистрация `POST /auth/accept-invite` |
| Чек-лист эфира | `GET/PUT /stream-events/{id}/days/{day}/checklist` (6 пунктов, отдельно на каждый день) |
| PWA | `vite-plugin-pwa` — офлайн-кэш статики |
| E2E | Playwright: `npm run test:e2e` в `frontend` (нужен стенд, см. ниже) |
| Storybook | `npm run storybook` — компонент `BrandLogo` |
| Кодоген API | `npm run codegen:api` (нужен запущенный backend с `/openapi.json`) |
| Масштаб | Рекомендации по воркерам: [docs/WORKERS_AND_SCALE.md](docs/WORKERS_AND_SCALE.md) |

## Быстрый старт (Docker)

```bash
cp .env.example .env
# При необходимости отредактируйте .env

docker compose up --build
```

Если при сборке **backend** `pip` ругается на **SSL** (`UNEXPECTED_EOF_WHILE_READING`) или **таймаут** до `pypi.org` — это сеть/фильтрация, не код. В корневом `.env` задайте зеркало и пересоберите:

```env
PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
```

Затем `docker compose build --no-cache backend` или снова `docker compose up --build`. Альтернатива: VPN или другая сеть; временно отключить «сканирование HTTPS» в антивирусе.

Откройте http://localhost — SPA, API: http://localhost/api/v1/...

Первичные пользователи и демо-событие:

```bash
docker compose exec backend python -m scripts.seed
```

## Локальная разработка

### База данных

Поднимите PostgreSQL 16 и создайте БД `streaming` (или используйте `docker compose up db`).

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
set DATABASE_URL=postgresql+asyncpg://streaming:streaming@localhost:5432/streaming
set DATABASE_URL_SYNC=postgresql://streaming:streaming@localhost:5432/streaming
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

По умолчанию Vite проксирует `/api`, `/health`, `/openapi.json` и `/ws` на `http://127.0.0.1:8000` (см. `frontend/vite.config.ts`).

### E2E (Playwright)

```bash
cd frontend
npx playwright install   # один раз, ставит браузеры
# Поднимите приложение (docker compose или dev), затем:
set E2E_BASE_URL=http://localhost
npm run test:e2e
```

### Тесты backend

```bash
cd backend
pytest -q
```

## Учётные записи после seed

По умолчанию создаются три пользователя с паролем `ChangeMe123!`. Почты и пароль сида можно задать в `backend/.env`: `SEED_ADMIN_EMAIL`, `SEED_MANAGER_EMAIL`, `SEED_OPERATOR_EMAIL`, `SEED_PASSWORD` (см. `.env.example`).

| Email (по умолчанию) | Роль |
|----------------------|------|
| admin@example.com | SUPERADMIN |
| manager@example.com | STREAM_MANAGER |
| operator@example.com | OPERATOR |

Смените пароли в продакшене. Полное пересоздание БД: [docs/DB_RESET.md](docs/DB_RESET.md).

**Суперадмин** в разделе «Администрирование» → «Пользователи» может создавать учётки (пароль можно не задавать — уйдёт на почту при настроенном SMTP). Смена email админа в БД: [docs/CHANGE_ADMIN_EMAIL.md](docs/CHANGE_ADMIN_EMAIL.md).

Новые пользователи проходят короткое интерактивное знакомство с панелью (имя, пароль, аватар, роли); демо-учётки из `scripts.seed` помечены как уже прошедшие ознакомление. Дополнительно после входа с временным паролем можно показать напоминание сменить пароль в «Профиль».

## Git

Рекомендуемые ветки: `main` (стабильная), `develop` (интеграция), feature-ветки от `develop`.

## Продакшен

Пошаговый выклад на VPS (PostgreSQL, сборка фронта, **systemd** + **nginx** + **Let’s Encrypt**): [docs/DEPLOY_PRODUCTION.md](docs/DEPLOY_PRODUCTION.md).  
Команды «с нуля» одним файлом: [docs/SERVER_COPYPASTE.md](docs/SERVER_COPYPASTE.md).  
Инвентаризация прод-сервера (порты, домены, пути проектов): [docs/SERVER_INVENTORY_XKVLORCRJX.md](docs/SERVER_INVENTORY_XKVLORCRJX.md).

---

## API

Всего обнаружено маршрутов: **51**

```
GET /health — `backend/app/api/health.py`
GET /health/ready — `backend/app/api/health.py`
GET /export.csv — `backend/app/api/v1/audit.py`
POST /purge — `backend/app/api/v1/audit.py`
POST /accept-invite — `backend/app/api/v1/auth.py`
POST /forgot-password — `backend/app/api/v1/auth.py`
GET /password-reset/validate — `backend/app/api/v1/auth.py`
POST /reset-password — `backend/app/api/v1/auth.py`
POST /login — `backend/app/api/v1/auth.py`
POST /refresh — `backend/app/api/v1/auth.py`
POST /logout — `backend/app/api/v1/auth.py`
GET /me — `backend/app/api/v1/auth.py`
POST /change-password — `backend/app/api/v1/auth.py`
GET /sessions — `backend/app/api/v1/auth.py`
DELETE /sessions/{session_id} — `backend/app/api/v1/auth.py`
DELETE /{template_id} — `backend/app/api/v1/event_templates.py`
POST /from-event/{stream_id} — `backend/app/api/v1/event_templates.py`
POST /{template_id}/instantiate — `backend/app/api/v1/event_templates.py`
POST /upload — `backend/app/api/v1/logos.py`
POST /upload-batch — `backend/app/api/v1/logos.py`
POST /broadcast-sessions/{session_id}/mentions — `backend/app/api/v1/mentions.py`
PATCH /sponsor-mentions/{mention_id} — `backend/app/api/v1/mentions.py`
DELETE /sponsor-mentions/{mention_id} — `backend/app/api/v1/mentions.py`
POST /{notification_id}/read — `backend/app/api/v1/notifications.py`
POST /read-all — `backend/app/api/v1/notifications.py`
POST /events — `backend/app/api/v1/product_analytics.py`
GET /summary — `backend/app/api/v1/product_analytics.py`
POST /avatar — `backend/app/api/v1/profile.py`
GET /activity — `backend/app/api/v1/profile.py`
GET /mentions — `backend/app/api/v1/reports.py`
GET /export.docx — `backend/app/api/v1/reports.py`
GET /export.csv — `backend/app/api/v1/reports.py`
GET /export.xlsx — `backend/app/api/v1/reports.py`
GET /operators — `backend/app/api/v1/stats.py`
GET /{stream_id} — `backend/app/api/v1/stream_events.py`
PATCH /{stream_id} — `backend/app/api/v1/stream_events.py`
DELETE /{stream_id} — `backend/app/api/v1/stream_events.py`
POST /{stream_id}/lock — `backend/app/api/v1/stream_events.py`
POST /{stream_id}/unlock — `backend/app/api/v1/stream_events.py`
POST /{stream_id}/days/{day_index}/broadcast/start — `backend/app/api/v1/stream_events.py`
POST /{stream_id}/days/{day_index}/broadcast/stop — `backend/app/api/v1/stream_events.py`
GET /{stream_id}/days/{day_index}/checklist — `backend/app/api/v1/stream_events.py`
PUT /{stream_id}/days/{day_index}/checklist — `backend/app/api/v1/stream_events.py`
GET /{stream_id}/days/{day_index}/mentions — `backend/app/api/v1/stream_events.py`
POST /{stream_id}/logos — `backend/app/api/v1/stream_logos.py`
DELETE /{stream_id}/logos/{logo_id} — `backend/app/api/v1/stream_logos.py`
GET /{stream_id}/logos/archive.zip — `backend/app/api/v1/stream_logos.py`
GET /{stream_id}/logos/{logo_id}/file — `backend/app/api/v1/stream_logos.py`
POST /invites — `backend/app/api/v1/users.py`
PATCH /{user_id} — `backend/app/api/v1/users.py`
DELETE /{user_id} — `backend/app/api/v1/users.py`
```

---

---

## Установка и запуск

### Локальная разработка

```bash
cd /opt/streaming
# Python-проекты
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt  # или backend/requirements.txt

# Node-проекты
npm ci && npm run dev
```

Скопируйте `env.example` → `.env` и заполните переменные.

---

## Деплой на сервер

### Перезапуск
```bash
systemctl restart streaming-backend
```

### Логи
```bash
journalctl -u streaming-backend -f --since "2 hours ago"
```

### Типовой деплой
1. `cd /opt/streaming`
2. `git pull`
3. Обновить зависимости (pip/npm)
4. Миграции БД (если есть)
5. Сборка frontend (если есть)
6. `systemctl restart ...`

---

### ТЗ размещения на сервере

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
  - `/api/`, `/health`, `/openapi.json`, `/uploads/` → backend **8010**;
  - длинный `proxy_read_timeout` для WebSocket.

## Связь с MainStream Shop
Тот же бренд в домене (**mainstreamfs**), но **другой код** и **другой systemd** на сервере.

## Данные
- Загрузки и БД приложения — внутри `/opt/streaming/backend` по конфигурации.


---

## Переменные окружения

**Переменные из env.example:**

| Переменная |
|------------|
| `DATABASE_URL` |
| `DATABASE_URL_SYNC` |
| `JWT_SECRET` |
| `JWT_ACCESS_EXPIRE_MINUTES` |
| `JWT_REFRESH_EXPIRE_DAYS` |
| `CORS_ORIGINS` |
| `REFRESH_COOKIE_NAME` |
| `REFRESH_COOKIE_SECURE` |
| `REFRESH_COOKIE_SAMESITE` |
| `TZ` |
| `APP_VERSION` |

```env
# Куда класть: для systemd/uvicorn — backend/.env (рабочий каталог backend).
# Docker Compose: те же переменные в .env в корне репозитория / в environment сервиса backend.

# PostgreSQL (async URL для приложения)
DATABASE_URL=postgresql+asyncpg://streaming:streaming@localhost:5432/streaming

# Для Alembic (синхронный драйвер)
DATABASE_URL_SYNC=postgresql://streaming:streaming@localhost:5432/streaming

JWT_SECRET=change-me-to-a-long-random-string-in-production
JWT_ACCESS_EXPIRE_MINUTES=30
JWT_REFRESH_EXPIRE_DAYS=7

# CORS: через запятую, для dev: http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Cookie refresh (в prod задать свой домен)
REFRESH_COOKIE_NAME=refresh_token
REFRESH_COOKIE_SECURE=false
REFRESH_COOKIE_SAMESITE=lax

TZ=Europe/Moscow

# Версия API (отдаётся в /health, для Sentry release)
APP_VERSION=1.0.0

# Каталог загрузок (аватары и т.д.). В проде лучше абсолютный путь, например /var/lib/streaming/uploads
# UPLOAD_DIR=uploads

# Публичный URL панели (обязательно для ссылок в письмах: вход, сброс пароля, логотип)
# Пример: https://ops.example.ru — в письме сброса будет {APP_PUBLIC_BASE_URL}/reset-password?token=...
# APP_PUBLIC_BASE_URL=

# Срок жизни ссылки сброса пароля (минуты), по умолчанию 10
# PASSWORD_RESET_EXPIRE_MINUTES=10

# Sentry (опционально): backend DSN — ошибки API; на фронте задайте VITE_SENTRY_DSN в frontend/.env
# SENTRY_DSN=
# SENTRY_ENVIRONMENT=production
# SENTRY_TRACES_SAMPLE_RATE=0.1

# Внешний webhook: JSON POST при старте/остановке эфира (опционально)
# EXTERNAL_WEBHOOK_URL=https://hooks.example.com/stream

# SMTP: приветственные письма при создании пользователя + еженедельные/ежемесячные отчёты (Word)
# Пустой SMTP_HOST — почта не отправляется (пользователь всё равно создаётся)
# SMTP_HOST=smtp.example.com
# SMTP_PORT=587
# SMTP_USER=
# SMTP_PASSWORD=
# SMTP_FROM=noreply@example.com
# SMTP_USE_TLS=true
# Для порта 465 (SSL сразу, часто Beget): SMTP_USE_SSL=true и SMTP_USE_TLS=false
# SMTP_USE_SSL=false

# --- Сид пользователей (только для python -m scripts.seed; в проде задайте свои почты)
# SEED_ADMIN_EMAIL=admin@example.com
# SEED_MANAGER_EMAIL=manager@example.com
# SEED_OPERATOR_EMAIL=operator@example.com
# SEED_PASSWORD=ChangeMe123!
# Только суперадмин, без демо-мероприятия: SEED_ONLY_SUPERADMIN=1

# --- Frontend (создайте frontend/.env при локальной разработке)
# VITE_SENTRY_DSN=

# --- Только для docker compose build (backend): если pip внутри образа не достучится до pypi.org ---
# (таймауты, SSL UNEXPECTED_EOF — часто DPI/антивирус/провайдер). Скопируйте в .env и раскомментируйте одну строку:
# PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
# PIP_I

> **Важно:** никогда не коммитьте `.env` в git. На production права `chmod 600 .env`.

---

## Структура каталогов

См. полный каталог файлов в [reference.md §4](.cursor/skills/streaming/reference.md#4-каталог-файлов).

---

## Бэкапы и безопасность

- Ежедневный бэкап БД: cron `04:00` → `/usr/local/sbin/ffkm-project-backups.sh`
- Приложение слушает только `127.0.0.1`, наружу — nginx + Let's Encrypt
- Логи: `journalctl -u <service> -f`
- Аудит сервера: `/root/server_audit_report_2026-06-10.docx`

---

## Документация

| Документ | Путь |
|----------|------|
| Полная техдокументация | `.cursor/skills/streaming/reference.md` |
| AI skill (навигация) | `.cursor/skills/streaming/SKILL.md` |
| ТЗ сервера | `ТЗ-сервер.md` |
| Серверный skill | `/root/.cursor/skills/ffkm-server/` |

---

*Обновлено автоматически. Для детального анализа каждого файла проекта — reference.md.*

```


---

## Исходный код: `backend/Dockerfile`

> 26 строк, 746 байт

```text
FROM python:3.12-slim-bookworm
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Таймаут и зеркало: при SSLError/EOF к pypi.org задайте build-arg (см. .env.example и README)
ENV PIP_DEFAULT_TIMEOUT=300
ARG PIP_INDEX_URL=https://pypi.org/simple
RUN pip install --no-cache-dir --retries 15 --default-timeout=120 \
    -i "${PIP_INDEX_URL}" \
    -r requirements.txt

COPY alembic.ini alembic.ini
COPY alembic ./alembic
COPY app ./app
COPY scripts ./scripts

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

```


---

## Исходный код: `backend/alembic.ini`

> 43 строк, 637 байт

```ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

sqlalchemy.url = driver://user:pass@localhost/dbname

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S

```


---

## Исходный код: `backend/alembic/env.py`

> 78 строк, 1,897 байт

```py
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import get_settings
from app.db.base import Base
from app.models import (  # noqa: F401
    AuditLog,
    BroadcastChecklist,
    BroadcastSession,
    Logo,
    MentionAdjustment,
    Notification,
    PasswordResetToken,
    ProductAnalyticsEvent,
    RefreshToken,
    SponsorMention,
    StreamDay,
    StreamDayAssignment,
    StreamEvent,
    StreamEventLogo,
    StreamEventTemplate,
    User,
    UserInvite,
)

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    return get_settings().database_url


def run_migrations_offline() -> None:
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        {**config.get_section(config.config_ini_section, {}), "sqlalchemy.url": get_url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```


---

## Исходный код: `backend/app/api/health.py`

> 38 строк, 1,173 байт

```py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_live() -> dict[str, str]:
    settings = get_settings()
    return {"status": "ok", "version": settings.app_version}


@router.get("/health/ready")
async def health_ready(session: AsyncSession = Depends(get_db)) -> dict[str, str | None]:
    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready", "database": str(exc)},
        ) from exc
    revision: str | None = None
    try:
        row = await session.execute(text("SELECT version_num FROM alembic_version LIMIT 1"))
        revision = row.scalar_one_or_none()
    except Exception:
        revision = None
    return {
        "status": "ready",
        "database": "ok",
        "alembic_revision": revision,
        "version": get_settings().app_version,
    }

```


---

## Исходный код: `backend/app/api/v1/audit.py`

> 93 строк, 2,817 байт

```py
import csv
import io
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import SuperAdminUser
from app.db.session import get_db
from app.schemas.audit import AuditLogOut, AuditLogPage
from app.services.audit_service import list_audit_logs, list_audit_logs_all, purge_audit_older_than

router = APIRouter(prefix="/audit-logs", tags=["audit"])


@router.get("", response_model=AuditLogPage)
async def list_logs(
    _: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    user_id: UUID | None = Query(default=None),
    action_type: str | None = Query(default=None),
) -> AuditLogPage:
    items, total = await list_audit_logs(
        session,
        page=page,
        page_size=page_size,
        user_id=user_id,
        action_type=action_type,
    )
    return AuditLogPage(
        items=[AuditLogOut.model_validate(x) for x in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/export.csv")
async def export_audit_csv(
    _: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
    user_id: UUID | None = Query(default=None),
    action_type: str | None = Query(default=None),
) -> Response:
    rows = await list_audit_logs_all(session, user_id=user_id, action_type=action_type, limit=50_000)
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(
        [
            "created_at",
            "action_type",
            "entity_type",
            "entity_id",
            "user_id",
            "payload_before",
            "payload_after",
        ]
    )
    for r in rows:
        w.writerow(
            [
                r.created_at.isoformat() if r.created_at else "",
                r.action_type,
                r.entity_type,
                r.entity_id or "",
                str(r.user_id) if r.user_id else "",
                str(r.payload_before) if r.payload_before is not None else "",
                str(r.payload_after) if r.payload_after is not None else "",
            ]
        )
    return Response(
        content="\ufeff" + buf.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=audit_export.csv"},
    )


class AuditPurgeBody(BaseModel):
    older_than_days: int = Field(ge=1, le=3650)


@router.post("/purge")
async def purge_audit(
    _: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
    body: AuditPurgeBody = AuditPurgeBody(older_than_days=365),
) -> dict[str, int]:
    deleted = await purge_audit_older_than(session, days=body.older_than_days)
    return {"deleted": deleted}

```


---

## Исходный код: `backend/app/api/v1/auth.py`

> 214 строк, 7,009 байт

```py
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.deps import AnyAuthenticated, RefreshJti
from app.core.limiter import limiter
from app.db.session import get_db
from app.schemas.auth import (
    ForgotPasswordIn,
    ForgotPasswordOut,
    LoginRequest,
    MeOut,
    PasswordResetValidateOut,
    RefreshRequest,
    ResetPasswordIn,
    TokenResponse,
)
from app.schemas.profile import ChangePasswordIn, SessionOut
from app.schemas.platform import AcceptInviteIn
from app.schemas.user import UserOut
from app.services import auth_service, invite_service, password_reset_service
from app.services.password_reset_email_service import send_password_reset_email_task
from app.utils.client_ip import client_ip_from_request

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/accept-invite", response_model=TokenResponse)
async def accept_invite_route(
    request: Request,
    response: Response,
    body: AcceptInviteIn,
    session: AsyncSession = Depends(get_db),
) -> TokenResponse:
    user = await invite_service.accept_invite(session, body)
    client_host = request.client.host if request.client else None
    ua = request.headers.get("user-agent")
    access, refresh, _exp = await auth_service.create_fresh_session(
        session,
        user=user,
        request_ip=client_host,
        user_agent=ua,
    )
    settings = get_settings()
    max_age = settings.jwt_refresh_expire_days * 24 * 60 * 60
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=refresh,
        httponly=True,
        secure=settings.refresh_cookie_secure,
        samesite=settings.refresh_cookie_samesite,
        max_age=max_age,
        path="/",
    )
    return TokenResponse(access_token=access, user=UserOut.model_validate(user))


@router.post("/forgot-password", response_model=ForgotPasswordOut)
@limiter.limit("5/minute")
async def forgot_password_route(
    request: Request,
    background_tasks: BackgroundTasks,
    body: ForgotPasswordIn,
    session: AsyncSession = Depends(get_db),
) -> ForgotPasswordOut:
    link, to_email, greeting = await password_reset_service.request_password_reset(session, email=str(body.email))
    if link and to_email:
        background_tasks.add_task(send_password_reset_email_task, to_email, link, greeting)
    return ForgotPasswordOut()


@router.get("/password-reset/validate", response_model=PasswordResetValidateOut)
@limiter.limit("60/minute")
async def password_reset_validate_route(
    request: Request,
    token: str | None = Query(None),
    session: AsyncSession = Depends(get_db),
) -> PasswordResetValidateOut:
    if not token:
        return PasswordResetValidateOut(ok=False)
    ok = await password_reset_service.token_is_valid(session, raw_token=token)
    return PasswordResetValidateOut(ok=ok)


@router.post("/reset-password", status_code=204)
@limiter.limit("20/minute")
async def reset_password_route(
    request: Request,
    body: ResetPasswordIn,
    session: AsyncSession = Depends(get_db),
) -> None:
    await password_reset_service.reset_password_with_token(
        session,
        raw_token=body.token,
        new_password=body.new_password,
    )


@router.post("/login", response_model=TokenResponse)
@limiter.limit("30/minute")
async def login(
    request: Request,
    response: Response,
    body: LoginRequest,
    session: AsyncSession = Depends(get_db),
) -> TokenResponse:
    settings = get_settings()
    client_host = client_ip_from_request(request)
    ua = request.headers.get("user-agent")
    user, access, refresh, _exp = await auth_service.login_user(
        session,
        email=body.email,
        password=body.password,
        request_ip=client_host,
        user_agent=ua,
    )
    max_age = settings.jwt_refresh_expire_days * 24 * 60 * 60
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=refresh,
        httponly=True,
        secure=settings.refresh_cookie_secure,
        samesite=settings.refresh_cookie_samesite,
        max_age=max_age,
        path="/",
    )
    return TokenResponse(access_token=access, user=UserOut.model_validate(user))


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db),
    body: RefreshRequest | None = None,
) -> TokenResponse:
    settings = get_settings()
    token = request.cookies.get(settings.refresh_cookie_name)
    if body and body.refresh_token:
        token = body.refresh_token
    if not token:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Нет refresh токена")
    user, access = await auth_service.refresh_access_token(session, token)
    return TokenResponse(access_token=access, user=UserOut.model_validate(user))


@router.post("/logout", status_code=204)
async def logout(
    request: Request,
    response: Response,
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
    body: RefreshRequest | None = None,
) -> None:
    settings = get_settings()
    token = request.cookies.get(settings.refresh_cookie_name)
    if body and body.refresh_token:
        token = body.refresh_token
    await auth_service.logout_user(session, user_id=user.id, refresh_token=token)
    response.delete_cookie(settings.refresh_cookie_name, path="/")


@router.get("/me", response_model=MeOut)
async def me(user: AnyAuthenticated) -> MeOut:
    return MeOut(user=UserOut.model_validate(user))


@router.post("/change-password", status_code=204)
async def change_password_route(
    body: ChangePasswordIn,
    user: AnyAuthenticated,
    current_jti: RefreshJti,
    session: AsyncSession = Depends(get_db),
) -> None:
    await auth_service.change_password(
        session,
        user_id=user.id,
        current_password=body.current_password,
        new_password=body.new_password,
        current_jti=current_jti,
    )


@router.get("/sessions", response_model=list[SessionOut])
async def list_sessions_route(
    user: AnyAuthenticated,
    current_jti: RefreshJti,
    session: AsyncSession = Depends(get_db),
) -> list[SessionOut]:
    rows = await auth_service.list_active_refresh_tokens(session, user_id=user.id)
    return [
        SessionOut(
            id=r.id,
            created_at=r.created_at,
            expires_at=r.expires_at,
            user_agent=r.user_agent,
            is_current=bool(current_jti and r.jti == current_jti),
        )
        for r in rows
    ]


@router.delete("/sessions/{session_id}", status_code=204)
async def revoke_session_route(
    session_id: UUID,
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> None:
    await auth_service.revoke_refresh_session_by_id(session, user_id=user.id, session_id=session_id)

```


---

## Исходный код: `backend/app/api/v1/dashboard.py`

> 19 строк, 627 байт

```py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import AnyAuthenticated
from app.db.session import get_db
from app.schemas.profile import DashboardSummaryOut
from app.services.dashboard_service import build_dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardSummaryOut)
async def dashboard_summary(
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> DashboardSummaryOut:
    data = await build_dashboard_summary(session, user=user)
    return DashboardSummaryOut(**data)

```


---

## Исходный код: `backend/app/api/v1/event_templates.py`

> 74 строк, 2,392 байт

```py
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin
from app.db.session import get_db
from app.schemas.stream import StreamEventDetailOut
from app.schemas.templates import (
    InstantiateTemplateBody,
    StreamEventTemplateCreate,
    StreamEventTemplateOut,
    TemplateFromEventBody,
)
from app.services import template_service

router = APIRouter(prefix="/stream-event-templates", tags=["stream-event-templates"])


@router.get("", response_model=list[StreamEventTemplateOut])
async def list_templates(
    _: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> list[StreamEventTemplateOut]:
    rows = await template_service.list_templates(session)
    return [StreamEventTemplateOut.model_validate(r) for r in rows]


@router.post("", response_model=StreamEventTemplateOut)
async def create_template(
    body: StreamEventTemplateCreate,
    user: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> StreamEventTemplateOut:
    t = await template_service.create_template(session, actor=user, body=body)
    return StreamEventTemplateOut.model_validate(t)


@router.delete("/{template_id}", status_code=204)
async def delete_template(
    template_id: UUID,
    user: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> None:
    await template_service.delete_template(session, actor=user, template_id=template_id)


@router.post("/from-event/{stream_id}", response_model=StreamEventTemplateOut)
async def template_from_event(
    stream_id: UUID,
    body: TemplateFromEventBody,
    user: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> StreamEventTemplateOut:
    t = await template_service.template_from_event(session, actor=user, stream_id=stream_id, body=body)
    return StreamEventTemplateOut.model_validate(t)


@router.post("/{template_id}/instantiate", response_model=StreamEventDetailOut)
async def instantiate_template(
    template_id: UUID,
    body: InstantiateTemplateBody,
    user: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> StreamEventDetailOut:
    return await template_service.instantiate_template(
        session,
        actor=user,
        template_id=template_id,
        title=body.title,
        start_date=body.start_date,
        duration_days=body.duration_days,
    )

```


---

## Исходный код: `backend/app/api/v1/logos.py`

> 36 строк, 1,209 байт

```py
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin, OperatorOrAbove
from app.db.session import get_db
from app.schemas.logo import LogoLibraryItemOut
from app.services import logo_service

router = APIRouter(prefix="/logos", tags=["logos"])


@router.post("/upload", response_model=LogoLibraryItemOut)
async def upload_logo_route(
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
) -> LogoLibraryItemOut:
    return await logo_service.upload_logo(session, actor=actor, file=file)


@router.post("/upload-batch", response_model=list[LogoLibraryItemOut])
async def upload_logos_batch_route(
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    files: list[UploadFile] = File(...),
) -> list[LogoLibraryItemOut]:
    return await logo_service.upload_logos_batch(session, actor=actor, files=files)


@router.get("", response_model=list[LogoLibraryItemOut])
async def list_logos_route(
    _: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> list[LogoLibraryItemOut]:
    return await logo_service.list_library(session)

```


---

## Исходный код: `backend/app/api/v1/mentions.py`

> 74 строк, 2,652 байт

```py
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import OperatorOrAbove
from app.db.session import get_db
from app.models.stream import BroadcastSession
from app.schemas.stream import SponsorMentionOut, SponsorMentionUpdate
from app.services import stream_service
from app.websocket.hub import StreamEventHub

router = APIRouter(tags=["mentions"])


@router.post("/broadcast-sessions/{session_id}/mentions", response_model=SponsorMentionOut)
async def add_mention(
    session_id: UUID,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> SponsorMentionOut:
    out = await stream_service.add_sponsor_mention(session, actor=actor, broadcast_session_id=session_id)
    res = await session.execute(
        select(BroadcastSession.stream_event_id).where(BroadcastSession.id == out.broadcast_session_id)
    )
    stream_event_id = res.scalar_one()
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(
        stream_event_id,
        {"type": "mention_created", "payload": out.model_dump(mode="json")},
    )
    return out


@router.patch("/sponsor-mentions/{mention_id}", response_model=SponsorMentionOut)
async def patch_mention(
    mention_id: UUID,
    body: SponsorMentionUpdate,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> SponsorMentionOut:
    out = await stream_service.update_sponsor_mention(
        session, actor=actor, mention_id=mention_id, new_adjusted_sec=body.adjusted_offset_sec
    )
    res = await session.execute(
        select(BroadcastSession.stream_event_id).where(BroadcastSession.id == out.broadcast_session_id)
    )
    stream_event_id = res.scalar_one()
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(
        stream_event_id,
        {"type": "mention_updated", "payload": out.model_dump(mode="json")},
    )
    return out


@router.delete("/sponsor-mentions/{mention_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mention(
    mention_id: UUID,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> Response:
    stream_event_id = await stream_service.delete_sponsor_mention(session, actor=actor, mention_id=mention_id)
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(
        stream_event_id,
        {"type": "mention_deleted", "payload": {"mention_id": str(mention_id)}},
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

```


---

## Исходный код: `backend/app/api/v1/notifications.py`

> 49 строк, 1,616 байт

```py
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import AnyAuthenticated
from app.db.session import get_db
from app.schemas.platform import NotificationListOut, NotificationOut
from app.services import notification_service

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=NotificationListOut)
async def list_my_notifications(
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> NotificationListOut:
    items = await notification_service.list_notifications(session, user_id=user.id)
    unread = await notification_service.count_unread(session, user_id=user.id)
    return NotificationListOut(
        items=[NotificationOut.model_validate(x) for x in items],
        unread_count=unread,
    )


@router.post("/{notification_id}/read", status_code=204)
async def mark_notification_read(
    notification_id: UUID,
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> None:
    ok = await notification_service.mark_read(session, user_id=user.id, notification_id=notification_id)
    if ok:
        await session.commit()
    else:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдено")


@router.post("/read-all", status_code=204)
async def mark_all_read(
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> None:
    await notification_service.mark_all_read(session, user_id=user.id)
    await session.commit()

```


---

## Исходный код: `backend/app/api/v1/product_analytics.py`

> 35 строк, 1,073 байт

```py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import AnyAuthenticated, SuperAdminUser
from app.db.session import get_db
from app.schemas.platform import AnalyticsIn, AnalyticsRow, AnalyticsSummaryOut
from app.services import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/events", status_code=204)
async def track_event(
    body: AnalyticsIn,
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> None:
    await analytics_service.track_event(
        session,
        user_id=user.id,
        event_name=body.event_name,
        meta=body.meta,
    )


@router.get("/summary", response_model=AnalyticsSummaryOut)
async def analytics_summary(
    _: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
) -> AnalyticsSummaryOut:
    rows = await analytics_service.summary_last_days(session, days=7)
    return AnalyticsSummaryOut(
        by_event=[AnalyticsRow(event_name=r["event_name"], count=r["count"]) for r in rows],
    )

```


---

## Исходный код: `backend/app/api/v1/profile.py`

> 61 строк, 1,897 байт

```py
from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import AnyAuthenticated
from app.db.session import get_db
from app.schemas.audit import AuditLogOut
from app.schemas.profile import MyActivityPage, ProfileUpdate
from app.schemas.user import UserOut
from app.services.audit_service import list_audit_logs
from app.services import profile_service

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=UserOut)
async def get_profile(user: AnyAuthenticated, session: AsyncSession = Depends(get_db)) -> UserOut:
    await session.refresh(user)
    return UserOut.model_validate(user)


@router.patch("", response_model=UserOut)
async def patch_profile(
    body: ProfileUpdate,
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
) -> UserOut:
    u = await profile_service.update_profile(session, user_id=user.id, data=body)
    return UserOut.model_validate(u)


@router.post("/avatar", response_model=UserOut)
async def post_avatar(
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
) -> UserOut:
    u = await profile_service.save_avatar_file(session, user_id=user.id, file=file)
    return UserOut.model_validate(u)


@router.get("/activity", response_model=MyActivityPage)
async def get_my_activity(
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> MyActivityPage:
    items, total = await list_audit_logs(
        session,
        page=page,
        page_size=page_size,
        user_id=user.id,
        action_type=None,
    )
    return MyActivityPage(
        items=[AuditLogOut.model_validate(x) for x in items],
        total=total,
        page=page,
        page_size=page_size,
    )

```


---

## Исходный код: `backend/app/api/v1/reports.py`

> 98 строк, 2,928 байт

```py
from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin
from app.db.session import get_db
from app.schemas.report import ReportMentionsOut
from app.services.report_service import (
    export_mentions_csv,
    export_mentions_docx,
    export_mentions_xlsx,
    get_mentions_report,
)

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/mentions", response_model=ReportMentionsOut)
async def report_mentions(
    _: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    stream_id: UUID | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
) -> ReportMentionsOut:
    return await get_mentions_report(
        session,
        stream_event_id=stream_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/export.docx")
async def export_docx(
    _: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    stream_id: UUID | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
) -> Response:
    data = await export_mentions_docx(
        session,
        stream_event_id=stream_id,
        date_from=date_from,
        date_to=date_to,
    )
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": 'attachment; filename="mentions_report.docx"'},
    )


@router.get("/export.csv")
async def export_csv(
    _: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    stream_id: UUID | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
) -> Response:
    data = await export_mentions_csv(
        session,
        stream_event_id=stream_id,
        date_from=date_from,
        date_to=date_to,
    )
    return Response(
        content=data,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="mentions_report.csv"'},
    )


@router.get("/export.xlsx")
async def export_xlsx(
    _: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    stream_id: UUID | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
) -> Response:
    data = await export_mentions_xlsx(
        session,
        stream_event_id=stream_id,
        date_from=date_from,
        date_to=date_to,
    )
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="mentions_report.xlsx"'},
    )

```


---

## Исходный код: `backend/app/api/v1/router.py`

> 37 строк, 953 байт

```py
from fastapi import APIRouter

from app.api.v1 import (
    audit,
    auth,
    dashboard,
    event_templates,
    logos,
    mentions,
    notifications,
    product_analytics,
    profile,
    reports,
    stats,
    stream_events,
    stream_logos,
    users,
    ws,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(profile.router)
api_router.include_router(dashboard.router)
api_router.include_router(event_templates.router)
api_router.include_router(users.router)
api_router.include_router(stream_events.router)
api_router.include_router(stream_logos.router)
api_router.include_router(logos.router)
api_router.include_router(mentions.router)
api_router.include_router(reports.router)
api_router.include_router(stats.router)
api_router.include_router(audit.router)
api_router.include_router(notifications.router)
api_router.include_router(product_analytics.router)
api_router.include_router(ws.router)

```


---

## Исходный код: `backend/app/api/v1/stats.py`

> 26 строк, 897 байт

```py
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin
from app.core.timezone import now_moscow
from app.db.session import get_db
from app.schemas.stats import OperatorStatsOverviewOut
from app.services.stats_service import get_operator_stats_overview

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/operators", response_model=OperatorStatsOverviewOut)
async def operator_stats(
    _: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    stat_date: date | None = Query(
        default=None,
        description="Календарный день по Москве; по умолчанию — сегодня",
    ),
) -> OperatorStatsOverviewOut:
    d = stat_date or now_moscow().date()
    return await get_operator_stats_overview(session, stat_date=d)

```


---

## Исходный код: `backend/app/api/v1/stream_events.py`

> 276 строк, 9,170 байт

```py
from uuid import UUID

from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin, OperatorOrAbove
from app.db.session import get_db
from app.schemas.platform import ChecklistOut, ChecklistUpdate
from app.schemas.stream import (
    BroadcastActualStartBody,
    BroadcastSessionOut,
    SponsorMentionOut,
    StreamEventCreate,
    StreamEventDetailOut,
    StreamEventListOut,
    StreamEventUpdate,
    StreamLockBody,
)
from app.services import checklist_service, stream_service
from app.utils.webhook import post_external_webhook
from app.websocket.hub import StreamEventHub

router = APIRouter(prefix="/stream-events", tags=["stream-events"])


@router.get("", response_model=list[StreamEventListOut])
async def list_streams(
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> list[StreamEventListOut]:
    return await stream_service.list_stream_events(session, viewer=actor)


@router.get("/{stream_id}", response_model=StreamEventDetailOut)
async def get_stream(
    stream_id: UUID,
    _: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> StreamEventDetailOut:
    return await stream_service.get_stream_event_detail(session, stream_id)


@router.post("", response_model=StreamEventDetailOut)
async def create_stream(
    body: StreamEventCreate,
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> StreamEventDetailOut:
    return await stream_service.create_stream_event(session, actor=actor, data=body)


@router.patch("/{stream_id}", response_model=StreamEventDetailOut)
async def update_stream(
    stream_id: UUID,
    body: StreamEventUpdate,
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> StreamEventDetailOut:
    return await stream_service.update_stream_event(session, actor=actor, stream_id=stream_id, data=body)


@router.delete("/{stream_id}", status_code=204)
async def delete_stream(
    stream_id: UUID,
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> None:
    await stream_service.delete_stream_event(session, actor=actor, stream_id=stream_id)


@router.post("/{stream_id}/lock", response_model=StreamEventDetailOut)
async def lock_stream_route(
    stream_id: UUID,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
    body: StreamLockBody | None = None,
) -> StreamEventDetailOut:
    assign = body.assign_user_id if body else None
    day_ix = body.day_indices if body else None
    detail = await stream_service.lock_stream(
        session,
        actor=actor,
        stream_id=stream_id,
        assign_user_id=assign,
        day_indices=day_ix,
    )
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(
        stream_id,
        {
            "type": "lock_changed",
            "payload": {"locked_by_user_id": str(detail.locked_by_user_id) if detail.locked_by_user_id else None},
        },
    )
    return detail


@router.post("/{stream_id}/unlock", response_model=StreamEventDetailOut)
async def unlock_stream_route(
    stream_id: UUID,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> StreamEventDetailOut:
    detail = await stream_service.unlock_stream(session, actor=actor, stream_id=stream_id)
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(stream_id, {"type": "lock_changed", "payload": {"locked_by_user_id": None}})
    return detail


@router.post("/{stream_id}/days/{day_index}/broadcast/start", response_model=BroadcastSessionOut)
async def start_broadcast_route(
    stream_id: UUID,
    day_index: int,
    request: Request,
    background_tasks: BackgroundTasks,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> BroadcastSessionOut:
    out = await stream_service.start_broadcast(session, actor=actor, stream_id=stream_id, day_index=day_index)
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(
        stream_id,
        {
            "type": "broadcast_started",
            "payload": {
                "session_id": str(out.id),
                "day_index": out.day_index,
                "started_at": out.started_at.isoformat(),
            },
        },
    )
    background_tasks.add_task(
        post_external_webhook,
        "broadcast_started",
        {
            "stream_event_id": str(stream_id),
            "day_index": day_index,
            "session_id": str(out.id),
            "started_at": out.started_at.isoformat(),
        },
    )
    return out


@router.post(
    "/{stream_id}/days/{day_index}/broadcast/actual-start",
    response_model=BroadcastSessionOut,
)
async def realign_broadcast_actual_start_route(
    stream_id: UUID,
    day_index: int,
    body: BroadcastActualStartBody,
    request: Request,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> BroadcastSessionOut:
    out = await stream_service.realign_broadcast_actual_start(
        session,
        actor=actor,
        stream_id=stream_id,
        day_index=day_index,
        actual_started_at=body.actual_started_at,
    )
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(
        stream_id,
        {
            "type": "broadcast_realigned",
            "payload": {"day_index": day_index, "started_at": out.started_at.isoformat()},
        },
    )
    return out


@router.post("/{stream_id}/days/{day_index}/broadcast/stop", status_code=204)
async def stop_broadcast_route(
    stream_id: UUID,
    day_index: int,
    request: Request,
    background_tasks: BackgroundTasks,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> None:
    await stream_service.stop_broadcast(session, actor=actor, stream_id=stream_id, day_index=day_index)
    hub: StreamEventHub = request.app.state.ws_hub
    await hub.publish(stream_id, {"type": "broadcast_stopped", "payload": {"day_index": day_index}})
    background_tasks.add_task(
        post_external_webhook,
        "broadcast_stopped",
        {"stream_event_id": str(stream_id), "day_index": day_index},
    )


@router.get("/{stream_id}/days/{day_index}/checklist", response_model=ChecklistOut)
async def get_checklist_route(
    stream_id: UUID,
    day_index: int,
    user: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> ChecklistOut:
    await stream_service.assert_valid_stream_day(session, stream_id, day_index)
    row = await checklist_service.get_checklist_row(
        session, stream_event_id=stream_id, user_id=user.id, day_index=day_index
    )
    if not row:
        return ChecklistOut(
            stream_event_id=stream_id,
            day_index=day_index,
            picture_exposure_ok=False,
            judges_stream_ok=False,
            splitter_socket_ok=False,
            key_stream_started_ok=False,
            kick_ok=False,
            mentions_four_ok=False,
            updated_at=datetime.now(timezone.utc),
        )
    return ChecklistOut(
        stream_event_id=row.stream_event_id,
        day_index=row.day_index,
        picture_exposure_ok=row.picture_exposure_ok,
        judges_stream_ok=row.judges_stream_ok,
        splitter_socket_ok=row.splitter_socket_ok,
        key_stream_started_ok=row.key_stream_started_ok,
        kick_ok=row.kick_ok,
        mentions_four_ok=row.mentions_four_ok,
        updated_at=row.updated_at,
    )


@router.put("/{stream_id}/days/{day_index}/checklist", response_model=ChecklistOut)
async def put_checklist_route(
    stream_id: UUID,
    day_index: int,
    body: ChecklistUpdate,
    user: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> ChecklistOut:
    await stream_service.assert_valid_stream_day(session, stream_id, day_index)
    row = await checklist_service.update_checklist(
        session,
        stream_event_id=stream_id,
        user=user,
        day_index=day_index,
        picture_exposure_ok=body.picture_exposure_ok,
        judges_stream_ok=body.judges_stream_ok,
        splitter_socket_ok=body.splitter_socket_ok,
        key_stream_started_ok=body.key_stream_started_ok,
        kick_ok=body.kick_ok,
        mentions_four_ok=body.mentions_four_ok,
    )
    return ChecklistOut(
        stream_event_id=row.stream_event_id,
        day_index=row.day_index,
        picture_exposure_ok=row.picture_exposure_ok,
        judges_stream_ok=row.judges_stream_ok,
        splitter_socket_ok=row.splitter_socket_ok,
        key_stream_started_ok=row.key_stream_started_ok,
        kick_ok=row.kick_ok,
        mentions_four_ok=row.mentions_four_ok,
        updated_at=row.updated_at,
    )


@router.get("/{stream_id}/days/{day_index}/mentions", response_model=list[SponsorMentionOut])
async def list_mentions_route(
    stream_id: UUID,
    day_index: int,
    _: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> list[SponsorMentionOut]:
    return await stream_service.list_mentions_for_event_day(session, stream_id=stream_id, day_index=day_index)

```


---

## Исходный код: `backend/app/api/v1/stream_logos.py`

> 78 строк, 2,807 байт

```py
import io
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin, OperatorOrAbove
from app.db.session import get_db
from app.models.enums import AuditActionType
from app.schemas.logo import LogoAttachBody
from app.services import logo_service
from app.services.audit_service import write_audit

router = APIRouter(prefix="/stream-events", tags=["stream-events"])


@router.post("/{stream_id}/logos", status_code=204)
async def attach_logo_route(
    stream_id: UUID,
    body: LogoAttachBody,
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> None:
    await logo_service.attach_logo_to_stream(session, actor=actor, stream_id=stream_id, logo_id=body.logo_id)


@router.delete("/{stream_id}/logos/{logo_id}", status_code=204)
async def detach_logo_route(
    stream_id: UUID,
    logo_id: UUID,
    actor: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
) -> None:
    await logo_service.detach_logo_from_stream(session, actor=actor, stream_id=stream_id, logo_id=logo_id)


@router.get("/{stream_id}/logos/archive.zip")
async def download_logos_zip_route(
    stream_id: UUID,
    actor: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    data, zip_name = await logo_service.build_stream_logos_zip(session, stream_id=stream_id)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.LOGO_DOWNLOAD_ARCHIVE,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before=None,
        payload_after={"zip_name": zip_name},
    )
    await session.commit()
    headers = {"Content-Disposition": f'attachment; filename="{zip_name}"'}
    return StreamingResponse(io.BytesIO(data), media_type="application/zip", headers=headers)


@router.get("/{stream_id}/logos/{logo_id}/file")
async def download_logo_file_route(
    stream_id: UUID,
    logo_id: UUID,
    _: OperatorOrAbove,
    session: AsyncSession = Depends(get_db),
) -> FileResponse:
    await logo_service.assert_logo_on_stream(session, stream_id=stream_id, logo_id=logo_id)
    logo = await logo_service.get_logo_row(session, logo_id)
    if not logo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Логотип не найден")
    path = logo_service.logo_file_abs_path(logo.stored_path)
    if not path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Файл на диске не найден")
    return FileResponse(
        path=str(path),
        filename=logo.filename_original,
        media_type="application/octet-stream",
    )

```


---

## Исходный код: `backend/app/api/v1/users.py`

> 72 строк, 2,464 байт

```py
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import SuperAdminUser
from app.db.session import get_db
from app.schemas.platform import InviteCreate, InviteCreatedOut
from app.schemas.user import UserCreate, UserCreatedOut, UserOut, UserUpdate
from app.services import invite_service, user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserOut])
async def list_users(
    _: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
) -> list[UserOut]:
    users = await user_service.list_users(session)
    return [UserOut.model_validate(u) for u in users]


@router.post("/invites", response_model=InviteCreatedOut)
async def create_invite(
    body: InviteCreate,
    actor: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
) -> InviteCreatedOut:
    token = await invite_service.create_invite(session, actor_id=actor.id, data=body)
    return InviteCreatedOut(
        token=token,
        invite_url_hint="POST /api/v1/auth/accept-invite с полями token, password, first_name, last_name",
    )


@router.post("", response_model=UserCreatedOut)
async def create_user(
    body: UserCreate,
    actor: SuperAdminUser,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db),
) -> UserCreatedOut:
    outcome = await user_service.create_user(session, actor_id=actor.id, data=body)
    if outcome.welcome_email_payload is not None:
        background_tasks.add_task(user_service.send_welcome_email_task, outcome.welcome_email_payload)
    return UserCreatedOut(
        user=UserOut.model_validate(outcome.user),
        welcome_email_queued=outcome.welcome_email_payload is not None,
        welcome_email_skipped_reason=outcome.welcome_email_skipped_reason,
    )


@router.patch("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: UUID,
    body: UserUpdate,
    actor: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
) -> UserOut:
    user = await user_service.update_user(session, actor_id=actor.id, user_id=user_id, data=body)
    return UserOut.model_validate(user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID,
    actor: SuperAdminUser,
    session: AsyncSession = Depends(get_db),
) -> None:
    await user_service.delete_user(session, actor_id=actor.id, user_id=user_id)

```


---

## Исходный код: `backend/app/api/v1/ws.py`

> 69 строк, 2,048 байт

```py
import asyncio
import json
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from app.core.security import decode_token_safe
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.websocket.hub import StreamEventHub

router = APIRouter()

_WS_AUTH_TIMEOUT_S = 15.0


@router.websocket("/ws/stream-events/{stream_event_id}")
async def stream_events_ws(
    websocket: WebSocket,
    stream_event_id: uuid.UUID,
) -> None:
    await websocket.accept()
    try:
        raw = await asyncio.wait_for(websocket.receive_text(), timeout=_WS_AUTH_TIMEOUT_S)
    except (asyncio.TimeoutError, WebSocketDisconnect):
        await websocket.close(code=4401)
        return
    try:
        msg = json.loads(raw)
    except json.JSONDecodeError:
        await websocket.close(code=4401)
        return
    token = msg.get("access_token") or msg.get("token")
    if not token or not isinstance(token, str):
        await websocket.close(code=4401)
        return
    payload = decode_token_safe(token)
    if not payload or payload.get("type") != "access":
        await websocket.close(code=4401)
        return
    sub = payload.get("sub")
    if not sub:
        await websocket.close(code=4401)
        return
    try:
        uid = uuid.UUID(sub)
    except ValueError:
        await websocket.close(code=4401)
        return
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == uid))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            await websocket.close(code=4401)
            return
    hub: StreamEventHub = websocket.app.state.ws_hub
    ok = await hub.connect(stream_event_id, websocket)
    if not ok:
        return
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        hub.disconnect(stream_event_id, websocket)
        await hub.notify_presence(stream_event_id)

```


---

## Исходный код: `backend/app/core/config.py`

> 63 строк, 2,216 байт

```py
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+asyncpg://streaming:streaming@localhost:5432/streaming"
    database_url_sync: str = "postgresql://streaming:streaming@localhost:5432/streaming"

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_expire_minutes: int = 30
    jwt_refresh_expire_days: int = 7

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    refresh_cookie_name: str = "refresh_token"
    refresh_cookie_secure: bool = False
    refresh_cookie_samesite: str = "lax"

    api_v1_prefix: str = "/api/v1"

    upload_dir: str = "uploads"

    app_version: str = "1.0.0"

    # Публичный URL панели (для ссылок в письмах), например https://streaming.example.ru
    app_public_base_url: str = ""

    # Срок жизни ссылки сброса пароля (минуты)
    password_reset_expire_minutes: int = 10

    sentry_dsn: str = ""
    sentry_environment: str = "development"
    sentry_traces_sample_rate: float = 0.1

    # Опционально: POST JSON при событиях эфира (начало/конец)
    external_webhook_url: str = ""

    # Дни хранения журнала аудита (0 = не удалять; фоновые задачи — вне HTTP)
    audit_retention_days: int = 0

    # SMTP для еженедельных/ежемесячных отчётов (пустой host — рассылка отключена)
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = "noreply@localhost"
    smtp_use_tls: bool = True
    # True — порт 465 (implicit SSL). False — обычный SMTP + STARTTLS (например 587)
    smtp_use_ssl: bool = False

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

```


---

## Исходный код: `backend/app/core/deps.py`

> 81 строк, 3,335 байт

```py
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import decode_token_safe, parse_uuid
from app.db.session import get_db
from app.models.enums import UserRole
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_db)],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> User:
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не авторизован")
    settings = get_settings()
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Сессия истекла — выполните вход снова или обновите страницу",
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен")
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен")
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен")
    try:
        uid = parse_uuid(sub)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен")
    result = await session.execute(select(User).where(User.id == uid))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
    return user


def require_roles(*roles: UserRole):
    async def _dep(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
        return user

    return _dep


SuperAdminUser = Annotated[User, Depends(require_roles(UserRole.SUPERADMIN))]
ManagerOrAdmin = Annotated[User, Depends(require_roles(UserRole.SUPERADMIN, UserRole.STREAM_MANAGER))]
OperatorOrAbove = Annotated[
    User, Depends(require_roles(UserRole.SUPERADMIN, UserRole.STREAM_MANAGER, UserRole.OPERATOR))
]
AnyAuthenticated = Annotated[User, Depends(get_current_user)]


async def get_refresh_jti(request: Request) -> str | None:
    settings = get_settings()
    token = request.cookies.get(settings.refresh_cookie_name)
    if not token:
        return None
    payload = decode_token_safe(token)
    return payload.get("jti") if payload else None


RefreshJti = Annotated[str | None, Depends(get_refresh_jti)]

```


---

## Исходный код: `backend/app/core/limiter.py`

> 5 строк, 120 байт

```py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

```


---

## Исходный код: `backend/app/core/security.py`

> 54 строк, 1,708 байт

```py
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

import bcrypt
from jose import JWTError, jwt

from app.core.config import get_settings


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(*, subject: str, role: str, expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.jwt_access_expire_minutes)
    )
    payload = {"sub": subject, "role": role, "exp": expire, "type": "access"}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_refresh_token_payload() -> tuple[str, str, datetime]:
    settings = get_settings()
    jti = str(uuid4())
    expire = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_expire_days)
    payload: dict[str, Any] = {"jti": jti, "exp": expire, "type": "refresh"}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, jti, expire


def decode_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])


def decode_token_safe(token: str) -> dict[str, Any] | None:
    try:
        return decode_token(token)
    except JWTError:
        return None


def parse_uuid(subject: str) -> UUID:
    return UUID(subject)

```


---

## Исходный код: `backend/app/core/timezone.py`

> 36 строк, 1,067 байт

```py
from datetime import date, datetime
from zoneinfo import ZoneInfo

MOSCOW_TZ = ZoneInfo("Europe/Moscow")


def now_moscow() -> datetime:
    return datetime.now(MOSCOW_TZ)


def utc_now() -> datetime:
    return datetime.now(ZoneInfo("UTC"))


def to_moscow(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(MOSCOW_TZ)


def format_moscow_datetime(dt: datetime) -> str:
    """Отображение даты и времени в часовом поясе МСК: dd.mm.yyyy HH:mm (24ч)."""
    return to_moscow(dt).strftime("%d.%m.%Y %H:%M")


def format_moscow_date(d: date) -> str:
    """Только дата в МСК-смысле (календарная дата события): dd.mm.yyyy."""
    return d.strftime("%d.%m.%Y")


def add_seconds_to_start(started_at: datetime, offset_sec: int) -> datetime:
    from datetime import timedelta

    base = started_at if started_at.tzinfo else started_at.replace(tzinfo=ZoneInfo("UTC"))
    return base + timedelta(seconds=offset_sec)

```


---

## Исходный код: `backend/app/db/base.py`

> 6 строк, 83 байт

```py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

```


---

## Исходный код: `backend/app/db/session.py`

> 14 строк, 486 байт

```py
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
settings = get_settings()
engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

```


---

## Исходный код: `backend/app/main.py`

> 67 строк, 2,182 байт

```py
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.health import router as health_router
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.services.report_scheduler import setup_report_scheduler
from app.core.limiter import limiter
from app.middleware.request_id import RequestIDMiddleware
from app.websocket.hub import StreamEventHub


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    app.state.ws_hub = StreamEventHub()
    app.state.report_scheduler = setup_report_scheduler()
    yield
    sched = getattr(app.state, "report_scheduler", None)
    if sched is not None:
        sched.shutdown(wait=False)


def create_app() -> FastAPI:
    settings = get_settings()
    if settings.sentry_dsn:
        try:
            import sentry_sdk

            sentry_sdk.init(
                dsn=settings.sentry_dsn,
                environment=settings.sentry_environment,
                release=settings.app_version,
                traces_sample_rate=settings.sentry_traces_sample_rate,
            )
        except ImportError:
            pass

    app = FastAPI(title="Stream Sponsor Platform API", lifespan=lifespan)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIDMiddleware)

    app.include_router(health_router)
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    upload_root = Path(settings.upload_dir)
    upload_root.mkdir(parents=True, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=str(upload_root)), name="uploads")
    return app


app = create_app()

```


---

## Исходный код: `backend/app/middleware/request_id.py`

> 21 строк, 774 байт

```py
import logging
import uuid
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("app.request")


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Пробрасывает X-Request-ID: из заголовка или генерирует UUID, кладёт в request.state и ответ."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        rid = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = rid
        response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        return response

```


---

## Исходный код: `backend/app/models/__init__.py`

> 37 строк, 914 байт

```py
from app.models.audit import AuditLog
from app.models.enums import AuditActionType, UserRole
from app.models.logo import Logo, StreamEventLogo
from app.models.platform_extra import BroadcastChecklist, Notification, ProductAnalyticsEvent, UserInvite
from app.models.stream import (
    BroadcastSession,
    MentionAdjustment,
    SponsorMention,
    StreamDay,
    StreamDayAssignment,
    StreamEvent,
    StreamEventTemplate,
)
from app.models.user import PasswordResetToken, RefreshToken, User

__all__ = [
    "AuditLog",
    "AuditActionType",
    "UserRole",
    "User",
    "PasswordResetToken",
    "RefreshToken",
    "StreamEvent",
    "Logo",
    "StreamEventLogo",
    "StreamEventTemplate",
    "StreamDayAssignment",
    "StreamDay",
    "BroadcastSession",
    "SponsorMention",
    "MentionAdjustment",
    "Notification",
    "ProductAnalyticsEvent",
    "UserInvite",
    "BroadcastChecklist",
]

```


---

## Исходный код: `backend/app/models/audit.py`

> 23 строк, 1,040 байт

```py
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    action_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    payload_before: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    payload_after: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

```


---

## Исходный код: `backend/app/models/enums.py`

> 30 строк, 851 байт

```py
import enum


class UserRole(str, enum.Enum):
    SUPERADMIN = "SUPERADMIN"
    STREAM_MANAGER = "STREAM_MANAGER"
    OPERATOR = "OPERATOR"


class AuditActionType(str, enum.Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    USER_CREATE = "USER_CREATE"
    USER_UPDATE = "USER_UPDATE"
    USER_DELETE = "USER_DELETE"
    STREAM_CREATE = "STREAM_CREATE"
    STREAM_UPDATE = "STREAM_UPDATE"
    STREAM_DELETE = "STREAM_DELETE"
    STREAM_LOCK = "STREAM_LOCK"
    STREAM_UNLOCK = "STREAM_UNLOCK"
    BROADCAST_START = "BROADCAST_START"
    BROADCAST_STOP = "BROADCAST_STOP"
    BROADCAST_ACTUAL_START = "BROADCAST_ACTUAL_START"
    MENTION_CREATE = "MENTION_CREATE"
    MENTION_UPDATE = "MENTION_UPDATE"
    LOGO_UPLOAD = "LOGO_UPLOAD"
    LOGO_ATTACH = "LOGO_ATTACH"
    LOGO_DETACH = "LOGO_DETACH"
    LOGO_DOWNLOAD_ARCHIVE = "LOGO_DOWNLOAD_ARCHIVE"

```


---

## Исходный код: `backend/app/models/logo.py`

> 47 строк, 2,131 байт

```py
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Logo(Base):
    """Файл логотипа в медиатеке (переиспользуется между мероприятиями)."""

    __tablename__ = "logos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename_original: Mapped[str] = mapped_column(String(500), nullable=False)
    stored_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    uploaded_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    uploaded_by = relationship("User", foreign_keys=[uploaded_by_id])
    stream_links: Mapped[list["StreamEventLogo"]] = relationship(
        "StreamEventLogo", back_populates="logo", cascade="all, delete-orphan"
    )


class StreamEventLogo(Base):
    """Связь мероприятие ↔ логотип (многие-ко-многим с порядком)."""

    __tablename__ = "stream_event_logos"
    __table_args__ = (UniqueConstraint("stream_event_id", "logo_id", name="uq_stream_event_logo"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stream_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stream_events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    logo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("logos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    sort_order: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)

    stream_event = relationship("StreamEvent", back_populates="event_logos")
    logo = relationship("Logo", back_populates="stream_links")

```


---

## Исходный код: `backend/app/models/platform_extra.py`

> 72 строк, 3,719 байт

```py
import uuid
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import UserRole


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column(Text(), default="")
    kind: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean(), default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProductAnalyticsEvent(Base):
    __tablename__ = "product_analytics_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    event_name: Mapped[str] = mapped_column(String(100), index=True)
    meta: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UserInvite(Base):
    __tablename__ = "user_invites"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(320))
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="userrole", create_constraint=False, native_enum=True),
        nullable=False,
    )
    created_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class BroadcastChecklist(Base):
    __tablename__ = "broadcast_checklists"
    __table_args__ = (UniqueConstraint("stream_event_id", "user_id", "day_index", name="uq_checklist_stream_user_day"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stream_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stream_events.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    day_index: Mapped[int] = mapped_column(Integer(), nullable=False, default=1)
    picture_exposure_ok: Mapped[bool] = mapped_column(Boolean(), default=False)
    judges_stream_ok: Mapped[bool] = mapped_column(Boolean(), default=False)
    splitter_socket_ok: Mapped[bool] = mapped_column(Boolean(), default=False)
    key_stream_started_ok: Mapped[bool] = mapped_column(Boolean(), default=False)
    kick_ok: Mapped[bool] = mapped_column(Boolean(), default=False)
    mentions_four_ok: Mapped[bool] = mapped_column(Boolean(), default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

```


---

## Исходный код: `backend/app/models/stream.py`

> 163 строк, 7,875 байт

```py
from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, SmallInteger, String, Text, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class StreamEvent(Base):
    __tablename__ = "stream_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    duration_days: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    locked_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    content_url: Mapped[str | None] = mapped_column(Text(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    days: Mapped[list["StreamDay"]] = relationship(
        "StreamDay", back_populates="stream_event", cascade="all, delete-orphan", order_by="StreamDay.day_index"
    )
    broadcast_sessions: Mapped[list["BroadcastSession"]] = relationship(
        "BroadcastSession", back_populates="stream_event", cascade="all, delete-orphan"
    )
    day_assignments: Mapped[list["StreamDayAssignment"]] = relationship(
        "StreamDayAssignment", back_populates="stream_event", cascade="all, delete-orphan"
    )
    event_logos: Mapped[list["StreamEventLogo"]] = relationship(
        "StreamEventLogo",
        back_populates="stream_event",
        cascade="all, delete-orphan",
        order_by="StreamEventLogo.sort_order",
    )


class StreamDayAssignment(Base):
    """Какой оператор ведёт конкретный день многодневного эфира (уникально по событию и дню)."""

    __tablename__ = "stream_day_assignments"
    __table_args__ = (
        UniqueConstraint("stream_event_id", "day_index", name="uq_stream_day_assignment_event_day"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stream_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stream_events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    day_index: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    operator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    stream_event: Mapped["StreamEvent"] = relationship("StreamEvent", back_populates="day_assignments")


class StreamDay(Base):
    __tablename__ = "stream_days"
    __table_args__ = (UniqueConstraint("stream_event_id", "day_index", name="uq_stream_day_event_idx"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stream_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stream_events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    day_index: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    stream_url: Mapped[str] = mapped_column(Text, default="", nullable=False)
    server_url: Mapped[str] = mapped_column(Text, default="", nullable=False)
    stream_key: Mapped[str] = mapped_column(Text, default="", nullable=False)

    stream_event: Mapped["StreamEvent"] = relationship("StreamEvent", back_populates="days")


class BroadcastSession(Base):
    __tablename__ = "broadcast_sessions"
    __table_args__ = (
        Index(
            "ix_broadcast_active_per_event_day",
            "stream_event_id",
            "day_index",
            unique=True,
            postgresql_where=text("ended_at IS NULL"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stream_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stream_events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    day_index: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    operator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_alert_last_sent_hour: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))

    stream_event: Mapped["StreamEvent"] = relationship("StreamEvent", back_populates="broadcast_sessions")
    mentions: Mapped[list["SponsorMention"]] = relationship(
        "SponsorMention", back_populates="broadcast_session", cascade="all, delete-orphan"
    )


class SponsorMention(Base):
    __tablename__ = "sponsor_mentions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    broadcast_session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("broadcast_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    original_offset_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    adjusted_offset_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    broadcast_session: Mapped["BroadcastSession"] = relationship("BroadcastSession", back_populates="mentions")
    adjustments: Mapped[list["MentionAdjustment"]] = relationship(
        "MentionAdjustment", back_populates="mention", cascade="all, delete-orphan"
    )


class MentionAdjustment(Base):
    __tablename__ = "mention_adjustments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mention_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sponsor_mentions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    editor_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=False
    )
    previous_adjusted_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    new_adjusted_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    mention: Mapped["SponsorMention"] = relationship("SponsorMention", back_populates="adjustments")


class StreamEventTemplate(Base):
    """Шаблон события: название шаблона, заголовок эфира по умолчанию, дни (URL/ключи)."""

    __tablename__ = "stream_event_templates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    duration_days: Mapped[int] = mapped_column(SmallInteger(), nullable=False)
    days_json: Mapped[list] = mapped_column(JSONB, nullable=False)
    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

```


---

## Исходный код: `backend/app/models/user.py`

> 66 строк, 3,501 байт

```py
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), default="", nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), default="", nullable=False)
    phone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    telegram: Mapped[str | None] = mapped_column(String(80), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="userrole"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    suggest_password_change: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_login_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan"
    )


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    jti: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")

```


---

## Исходный код: `backend/app/schemas/__init__.py`

> 36 строк, 834 байт

```py
from app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse
from app.schemas.stream import (
    BroadcastSessionOut,
    MentionAdjustmentOut,
    SponsorMentionCreate,
    SponsorMentionOut,
    SponsorMentionUpdate,
    StreamDayIn,
    StreamDayOut,
    StreamEventCreate,
    StreamEventDetailOut,
    StreamEventListOut,
    StreamEventUpdate,
)
from app.schemas.user import UserCreate, UserOut, UserUpdate

__all__ = [
    "LoginRequest",
    "RefreshRequest",
    "TokenResponse",
    "UserCreate",
    "UserOut",
    "UserUpdate",
    "StreamDayIn",
    "StreamDayOut",
    "StreamEventCreate",
    "StreamEventUpdate",
    "StreamEventListOut",
    "StreamEventDetailOut",
    "BroadcastSessionOut",
    "SponsorMentionCreate",
    "SponsorMentionOut",
    "SponsorMentionUpdate",
    "MentionAdjustmentOut",
]

```


---

## Исходный код: `backend/app/schemas/audit.py`

> 26 строк, 509 байт

```py
import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AuditLogOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    action_type: str
    entity_type: str
    entity_id: str | None
    payload_before: dict[str, Any] | None
    payload_after: dict[str, Any] | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AuditLogPage(BaseModel):
    items: list[AuditLogOut]
    total: int
    page: int
    page_size: int

```


---

## Исходный код: `backend/app/schemas/auth.py`

> 49 строк, 1,221 байт

```py
from pydantic import BaseModel, EmailStr, Field, model_validator

from app.schemas.user import UserOut


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordIn(BaseModel):
    email: EmailStr


class ForgotPasswordOut(BaseModel):
    message: str = (
        "Если указанный адрес зарегистрирован в системе, мы отправили на него ссылку для сброса пароля."
    )


class PasswordResetValidateOut(BaseModel):
    ok: bool


class ResetPasswordIn(BaseModel):
    token: str = Field(min_length=20, max_length=512)
    new_password: str = Field(min_length=8, max_length=128)
    new_password_confirm: str = Field(min_length=8, max_length=128)

    @model_validator(mode="after")
    def passwords_match(self) -> "ResetPasswordIn":
        if self.new_password != self.new_password_confirm:
            raise ValueError("Пароли должны совпадать")
        return self


class RefreshRequest(BaseModel):
    refresh_token: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class MeOut(BaseModel):
    user: UserOut

```


---

## Исходный код: `backend/app/schemas/logo.py`

> 25 строк, 538 байт

```py
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class StreamLogoItemOut(BaseModel):
    id: uuid.UUID
    filename_original: str
    public_url: str
    sort_order: int
    created_at: datetime


class LogoLibraryItemOut(BaseModel):
    id: uuid.UUID
    filename_original: str
    public_url: str
    created_at: datetime
    uploaded_by_id: uuid.UUID | None


class LogoAttachBody(BaseModel):
    logo_id: uuid.UUID = Field(description="Идентификатор файла из медиатеки")

```


---

## Исходный код: `backend/app/schemas/platform.py`

> 77 строк, 1,758 байт

```py
import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import UserRole


class NotificationOut(BaseModel):
    id: uuid.UUID
    title: str
    body: str
    kind: str | None
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationListOut(BaseModel):
    items: list[NotificationOut]
    unread_count: int


class AnalyticsIn(BaseModel):
    event_name: str = Field(min_length=1, max_length=100)
    meta: dict | None = None


class InviteCreate(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    role: UserRole


class InviteCreatedOut(BaseModel):
    token: str
    invite_url_hint: str


class AcceptInviteIn(BaseModel):
    token: str = Field(min_length=10, max_length=64)
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)


class ChecklistOut(BaseModel):
    stream_event_id: uuid.UUID
    day_index: int
    picture_exposure_ok: bool
    judges_stream_ok: bool
    splitter_socket_ok: bool
    key_stream_started_ok: bool
    kick_ok: bool
    mentions_four_ok: bool
    updated_at: datetime


class ChecklistUpdate(BaseModel):
    picture_exposure_ok: bool | None = None
    judges_stream_ok: bool | None = None
    splitter_socket_ok: bool | None = None
    key_stream_started_ok: bool | None = None
    kick_ok: bool | None = None
    mentions_four_ok: bool | None = None


class AnalyticsRow(BaseModel):
    event_name: str
    count: int


class AnalyticsSummaryOut(BaseModel):
    """Агрегаты за последние 7 дней по имени события."""

    by_event: list[AnalyticsRow]

```


---

## Исходный код: `backend/app/schemas/profile.py`

> 45 строк, 1,230 байт

```py
import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.audit import AuditLogOut


class ProfileUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=40)
    telegram: str | None = Field(default=None, max_length=80)
    onboarding_completed: bool | None = None
    # только false: отклонить экран смены пароля при первом входе (без смены пароля)
    suggest_password_change: bool | None = None


class ChangePasswordIn(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class SessionOut(BaseModel):
    id: uuid.UUID
    created_at: datetime
    expires_at: datetime
    user_agent: str | None
    is_current: bool

    model_config = {"from_attributes": True}


class MyActivityPage(BaseModel):
    items: list[AuditLogOut]
    total: int
    page: int
    page_size: int


class DashboardSummaryOut(BaseModel):
    role: str
    title: str
    cards: list[dict]

```


---

## Исходный код: `backend/app/schemas/report.py`

> 24 строк, 506 байт

```py
import uuid
from datetime import date, datetime

from pydantic import BaseModel


class ReportMentionRow(BaseModel):
    mention_id: uuid.UUID
    stream_event_id: uuid.UUID
    stream_title: str
    event_day_date: date
    day_index: int
    broadcast_session_id: uuid.UUID
    original_timecode: str
    adjusted_timecode: str
    absolute_moscow_adjusted: str
    is_adjusted: bool
    mention_created_at: datetime


class ReportMentionsOut(BaseModel):
    items: list[ReportMentionRow]
    total: int

```


---

## Исходный код: `backend/app/schemas/stats.py`

> 40 строк, 1,026 байт

```py
import uuid
from datetime import date

from pydantic import BaseModel, Field


class LockAssignmentOut(BaseModel):
    stream_event_id: uuid.UUID
    title: str
    summary: str


class OperatorDayStatsOut(BaseModel):
    operator_id: uuid.UUID
    email: str
    display_name: str
    role: str
    broadcasts_week: int = Field(ge=0)
    mentions_week: int = Field(ge=0)
    mentions_norm_week: int = Field(ge=0, description="Ожидаемо упоминаний: 4 на каждый эфир")
    mentions_met_week: bool
    broadcasts_month: int = Field(ge=0)
    mentions_month: int = Field(ge=0)
    mentions_norm_month: int = Field(ge=0)
    mentions_met_month: bool


class OperatorStatsOverviewOut(BaseModel):
    stat_date: date
    week_start: date
    week_end: date
    month_start: date
    month_end: date
    assignments: list[LockAssignmentOut]
    operators: list[OperatorDayStatsOut]
    total_broadcasts_week: int
    total_mentions_week: int
    total_broadcasts_month: int
    total_mentions_month: int

```


---

## Исходный код: `backend/app/schemas/stream.py`

> 177 строк, 5,883 байт

```py
import uuid
from datetime import date, datetime

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator

from app.core.timezone import MOSCOW_TZ
from app.schemas.logo import StreamLogoItemOut

class StreamDayIn(BaseModel):
    day_index: int = Field(ge=1, le=5)
    stream_url: str = ""
    server_url: str = ""
    stream_key: str = ""


class StreamDayOut(BaseModel):
    id: uuid.UUID
    day_index: int
    stream_url: str
    server_url: str
    stream_key: str

    model_config = {"from_attributes": True}


class StreamEventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    start_date: date
    duration_days: int = Field(ge=1, le=5)
    days: list[StreamDayIn] | None = None
    """Если задан template_id — из шаблона берётся только URL сервера во все дни; поле days игнорируется."""
    template_id: uuid.UUID | None = None


class StreamLockBody(BaseModel):
    assign_user_id: uuid.UUID | None = Field(default=None, description="Для SUPERADMIN: на кого повесить дни")
    day_indices: list[int] | None = Field(
        default=None,
        description="Если null или пусто — все дни 1..N; иначе только перечисленные дни",
    )


class BroadcastActualStartBody(BaseModel):
    """Фактическое время начала эфира (когда картинка реально пошла). Без таймзоны — интерпретируется как МСК."""

    actual_started_at: datetime

    @field_validator("actual_started_at", mode="after")
    @classmethod
    def naive_as_moscow(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=MOSCOW_TZ)
        return v


class DayAssignmentOut(BaseModel):
    day_index: int
    operator_id: uuid.UUID
    operator_display_name: str
    operator_email: str = ""

    model_config = {"from_attributes": False}


class StreamEventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    start_date: date | None = None
    duration_days: int | None = Field(default=None, ge=1, le=5)
    days: list[StreamDayIn] | None = None
    content_url: AnyHttpUrl | None = None

    @field_validator("content_url", mode="before")
    @classmethod
    def empty_content_url_to_none(cls, v: object) -> object:
        if v == "":
            return None
        return v


class StreamDayLinkOut(BaseModel):
    """День мероприятия и ссылка на трансляцию (для списка без захода в карточку)."""

    day_index: int
    stream_url: str


class StreamEventListOut(BaseModel):
    id: uuid.UUID
    title: str
    start_date: date
    duration_days: int
    locked_by_user_id: uuid.UUID | None
    locked_by_display_name: str | None = None
    """Устар.: один «кто в работе»; при нескольких операторах смотрите assignment_summary."""
    assignment_summary: str | None = None
    """Кратко: кто какие дни ведёт."""
    has_slot_for_me: bool = True
    """Для текущего пользователя: есть ли свободные дни или уже свои назначения."""
    has_active_broadcast: bool
    has_ended_broadcast: bool = False
    ended_day_indices: list[int] = []
    created_at: datetime
    day_stream_links: list[StreamDayLinkOut] = []
    """По дням: ссылки на трансляцию (копирование из списка)."""

    model_config = {"from_attributes": True}


class BroadcastSessionOut(BaseModel):
    id: uuid.UUID
    stream_event_id: uuid.UUID
    day_index: int
    operator_id: uuid.UUID
    started_at: datetime
    ended_at: datetime | None
    is_active: bool
    """Число упоминаний (только в деталке мероприятия для завершённых сессий)."""
    mentions_count: int | None = None

    model_config = {"from_attributes": True}


class StreamEventDetailOut(BaseModel):
    id: uuid.UUID
    title: str
    start_date: date
    duration_days: int
    locked_by_user_id: uuid.UUID | None
    locked_by_display_name: str | None = None
    day_assignments: list[DayAssignmentOut] = []
    """Назначения операторов по дням."""
    days: list[StreamDayOut]
    active_broadcasts: list[BroadcastSessionOut]
    ended_broadcasts: list[BroadcastSessionOut] = []
    """Завершённые эфиры (для сдвига фактического старта менеджером)."""
    broadcast_restart_blocked_days: list[int] = []
    """Дни, где после завершённого эфира >1 ч с таймкодами повторный «Начать эфир» недоступен."""
    content_url: str | None = None
    """Ссылка на материалы (например Яндекс.Диск)."""
    logos: list[StreamLogoItemOut] = []
    created_at: datetime
    updated_at: datetime


class SponsorMentionCreate(BaseModel):
    pass


class SponsorMentionUpdate(BaseModel):
    adjusted_offset_sec: int = Field(ge=0)


class MentionAdjustmentOut(BaseModel):
    id: uuid.UUID
    editor_user_id: uuid.UUID
    previous_adjusted_sec: int
    new_adjusted_sec: int
    created_at: datetime

    model_config = {"from_attributes": True}


class SponsorMentionOut(BaseModel):
    id: uuid.UUID
    broadcast_session_id: uuid.UUID
    original_offset_sec: int
    adjusted_offset_sec: int
    original_timecode: str
    adjusted_timecode: str
    absolute_moscow_original: str
    absolute_moscow_adjusted: str
    is_adjusted: bool
    created_at: datetime
    adjustments: list[MentionAdjustmentOut]

    model_config = {"from_attributes": True}

```


---

## Исходный код: `backend/app/schemas/templates.py`

> 34 строк, 806 байт

```py
import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field

from app.schemas.stream import StreamDayIn


class StreamEventTemplateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=500)
    duration_days: int = Field(ge=1, le=5)
    days: list[StreamDayIn] | None = None


class StreamEventTemplateOut(BaseModel):
    id: uuid.UUID
    name: str
    title: str
    duration_days: int
    created_at: datetime

    model_config = {"from_attributes": True}


class InstantiateTemplateBody(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    start_date: date
    duration_days: int = Field(ge=1, le=5)


class TemplateFromEventBody(BaseModel):
    name: str = Field(min_length=1, max_length=200)

```


---

## Исходный код: `backend/app/schemas/user.py`

> 58 строк, 1,732 байт

```py
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, computed_field

from app.models.enums import UserRole


class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone: str | None = None
    telegram: str | None = None
    avatar_url: str | None = None
    role: UserRole
    is_active: bool
    suggest_password_change: bool = False
    onboarding_completed: bool = False
    last_login_at: datetime | None = None
    last_login_ip: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def display_name(self) -> str:
        s = f"{self.last_name} {self.first_name}".strip()
        return s if s else str(self.email)


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    role: UserRole
    is_active: bool = True


class UserCreatedOut(BaseModel):
    user: UserOut
    """Письмо уходит в фоне после ответа; True если SMTP настроен и задача поставлена."""
    welcome_email_queued: bool = False
    welcome_email_skipped_reason: str | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=40)
    telegram: str | None = Field(default=None, max_length=80)
    password: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None

```


---

## Исходный код: `backend/app/services/analytics_service.py`

> 27 строк, 978 байт

```py
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.platform_extra import ProductAnalyticsEvent


async def track_event(
    session: AsyncSession, *, user_id: UUID | None, event_name: str, meta: dict | None
) -> None:
    session.add(ProductAnalyticsEvent(user_id=user_id, event_name=event_name, meta=meta))
    await session.commit()


async def summary_last_days(session: AsyncSession, *, days: int = 7) -> list[dict[str, int | str]]:
    since = datetime.now(timezone.utc) - timedelta(days=days)
    q = (
        select(ProductAnalyticsEvent.event_name, func.count().label("cnt"))
        .where(ProductAnalyticsEvent.created_at >= since)
        .group_by(ProductAnalyticsEvent.event_name)
        .order_by(func.count().desc())
    )
    result = await session.execute(q)
    return [{"event_name": r[0], "count": int(r[1])} for r in result.all()]

```


---

## Исходный код: `backend/app/services/audit_service.py`

> 79 строк, 2,435 байт

```py
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog
from app.models.enums import AuditActionType


async def list_audit_logs(
    session: AsyncSession,
    *,
    page: int,
    page_size: int,
    user_id: UUID | None,
    action_type: str | None,
) -> tuple[list[AuditLog], int]:
    q = select(AuditLog).order_by(AuditLog.created_at.desc())
    count_base = select(func.count()).select_from(AuditLog)
    if user_id is not None:
        q = q.where(AuditLog.user_id == user_id)
        count_base = count_base.where(AuditLog.user_id == user_id)
    if action_type:
        q = q.where(AuditLog.action_type == action_type)
        count_base = count_base.where(AuditLog.action_type == action_type)
    total_result = await session.execute(count_base)
    total = int(total_result.scalar_one())
    q = q.offset((page - 1) * page_size).limit(page_size)
    result = await session.execute(q)
    return list(result.scalars().all()), total


async def write_audit(
    session: AsyncSession,
    *,
    user_id: UUID | None,
    action_type: AuditActionType,
    entity_type: str,
    entity_id: str | None,
    payload_before: dict[str, Any] | None,
    payload_after: dict[str, Any] | None,
) -> None:
    log = AuditLog(
        user_id=user_id,
        action_type=action_type.value,
        entity_type=entity_type,
        entity_id=entity_id,
        payload_before=payload_before,
        payload_after=payload_after,
    )
    session.add(log)


async def list_audit_logs_all(
    session: AsyncSession,
    *,
    user_id: UUID | None,
    action_type: str | None,
    limit: int = 50_000,
) -> list[AuditLog]:
    q = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    if user_id is not None:
        q = q.where(AuditLog.user_id == user_id)
    if action_type:
        q = q.where(AuditLog.action_type == action_type)
    result = await session.execute(q)
    return list(result.scalars().all())


async def purge_audit_older_than(session: AsyncSession, *, days: int) -> int:
    if days <= 0:
        return 0
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    result = await session.execute(delete(AuditLog).where(AuditLog.created_at < cutoff))
    await session.commit()
    return int(result.rowcount or 0)

```


---

## Исходный код: `backend/app/services/auth_service.py`

> 216 строк, 7,898 байт

```py
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token_payload,
    decode_token_safe,
    hash_password,
    verify_password,
)
from app.models.enums import AuditActionType
from app.models.user import RefreshToken, User
from app.services.audit_service import write_audit


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def _apply_last_login(user: User, *, request_ip: str | None) -> None:
    user.last_login_at = datetime.now(timezone.utc)
    user.last_login_ip = (request_ip[:45] if request_ip else None)


async def login_user(
    session: AsyncSession,
    *,
    email: str,
    password: str,
    request_ip: str | None,
    user_agent: str | None = None,
) -> tuple[User, str, str, datetime]:
    user = await authenticate_user(session, email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")
    _apply_last_login(user, request_ip=request_ip)
    refresh_token, jti, exp = create_refresh_token_payload()
    session.add(
        RefreshToken(
            user_id=user.id,
            jti=jti,
            expires_at=exp,
            user_agent=(user_agent[:500] if user_agent else None),
        )
    )
    await write_audit(
        session,
        user_id=user.id,
        action_type=AuditActionType.LOGIN,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=None,
        payload_after={"email": user.email, "ip": request_ip},
    )
    await session.commit()
    access = create_access_token(subject=str(user.id), role=user.role.value)
    return user, access, refresh_token, exp


async def refresh_access_token(session: AsyncSession, refresh_token: str) -> tuple[User, str]:
    payload = decode_token_safe(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный refresh")
    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный refresh")
    result = await session.execute(select(RefreshToken).where(RefreshToken.jti == jti))
    row = result.scalar_one_or_none()
    if not row or row.revoked_at is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен отозван")
    if row.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истёк")
    user_result = await session.execute(select(User).where(User.id == row.user_id))
    user = user_result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
    access = create_access_token(subject=str(user.id), role=user.role.value)
    return user, access


async def create_fresh_session(
    session: AsyncSession,
    *,
    user: User,
    request_ip: str | None,
    user_agent: str | None = None,
) -> tuple[str, str, datetime]:
    """Выдать access + refresh после регистрации по приглашению (и записать LOGIN)."""
    _apply_last_login(user, request_ip=request_ip)
    refresh_token, jti, exp = create_refresh_token_payload()
    session.add(
        RefreshToken(
            user_id=user.id,
            jti=jti,
            expires_at=exp,
            user_agent=(user_agent[:500] if user_agent else None),
        )
    )
    await write_audit(
        session,
        user_id=user.id,
        action_type=AuditActionType.LOGIN,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=None,
        payload_after={"email": user.email, "ip": request_ip, "via": "accept_invite"},
    )
    await session.commit()
    access = create_access_token(subject=str(user.id), role=user.role.value)
    return access, refresh_token, exp


async def logout_user(session: AsyncSession, *, user_id: UUID, refresh_token: str | None) -> None:
    if not refresh_token:
        await write_audit(
            session,
            user_id=user_id,
            action_type=AuditActionType.LOGOUT,
            entity_type="user",
            entity_id=str(user_id),
            payload_before=None,
            payload_after=None,
        )
        await session.commit()
        return
    payload = decode_token_safe(refresh_token)
    jti = payload.get("jti") if payload else None
    if jti:
        result = await session.execute(select(RefreshToken).where(RefreshToken.jti == jti))
        row = result.scalar_one_or_none()
        if row and row.user_id == user_id:
            row.revoked_at = datetime.now(timezone.utc)
    await write_audit(
        session,
        user_id=user_id,
        action_type=AuditActionType.LOGOUT,
        entity_type="user",
        entity_id=str(user_id),
        payload_before=None,
        payload_after=None,
    )
    await session.commit()


async def change_password(
    session: AsyncSession,
    *,
    user_id: UUID,
    current_password: str,
    new_password: str,
    current_jti: str | None,
) -> None:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    if not verify_password(current_password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный текущий пароль")
    user.password_hash = hash_password(new_password)
    user.suggest_password_change = False
    await session.flush()
    now = datetime.now(timezone.utc)
    rt_result = await session.execute(
        select(RefreshToken).where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))
    )
    for row in rt_result.scalars().all():
        if current_jti and row.jti == current_jti:
            continue
        row.revoked_at = now
    await write_audit(
        session,
        user_id=user_id,
        action_type=AuditActionType.USER_UPDATE,
        entity_type="user",
        entity_id=str(user_id),
        payload_before=None,
        payload_after={"password_changed": True},
    )
    await session.commit()


async def list_active_refresh_tokens(session: AsyncSession, *, user_id: UUID) -> list[RefreshToken]:
    now = datetime.now(timezone.utc)
    result = await session.execute(
        select(RefreshToken)
        .where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked_at.is_(None),
            RefreshToken.expires_at > now,
        )
        .order_by(RefreshToken.created_at.desc())
    )
    return list(result.scalars().all())


async def revoke_refresh_session_by_id(session: AsyncSession, *, user_id: UUID, session_id: UUID) -> None:
    result = await session.execute(
        select(RefreshToken).where(RefreshToken.id == session_id, RefreshToken.user_id == user_id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сессия не найдена")
    if row.revoked_at is None:
        row.revoked_at = datetime.now(timezone.utc)
    await session.commit()

```


---

## Исходный код: `backend/app/services/broadcast_alert_service.py`

> 149 строк, 5,362 байт

```py
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
        sent_count += 1
    if sent_count > 0:
        await session.commit()
    return sent_count


async def job_long_broadcast_alerts() -> None:
    try:
        async with AsyncSessionLocal() as session:
            sent_count = await check_long_running_broadcasts(session)
            if sent_count > 0:
                logger.info("Отправлены предупреждения по длительным эфирам: %s", sent_count)
    except Exception:
        logger.exception("Ошибка фоновой проверки длительных эфиров")

```


---

## Исходный код: `backend/app/services/checklist_service.py`

> 70 строк, 2,346 байт

```py
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.platform_extra import BroadcastChecklist
from app.models.user import User


async def get_checklist_row(
    session: AsyncSession, *, stream_event_id: UUID, user_id: UUID, day_index: int
) -> BroadcastChecklist | None:
    result = await session.execute(
        select(BroadcastChecklist).where(
            BroadcastChecklist.stream_event_id == stream_event_id,
            BroadcastChecklist.user_id == user_id,
            BroadcastChecklist.day_index == day_index,
        )
    )
    return result.scalar_one_or_none()


async def get_or_create_checklist(
    session: AsyncSession, *, stream_event_id: UUID, user: User, day_index: int
) -> BroadcastChecklist:
    result = await session.execute(
        select(BroadcastChecklist).where(
            BroadcastChecklist.stream_event_id == stream_event_id,
            BroadcastChecklist.user_id == user.id,
            BroadcastChecklist.day_index == day_index,
        )
    )
    row = result.scalar_one_or_none()
    if row:
        return row
    row = BroadcastChecklist(stream_event_id=stream_event_id, user_id=user.id, day_index=day_index)
    session.add(row)
    await session.flush()
    return row


async def update_checklist(
    session: AsyncSession,
    *,
    stream_event_id: UUID,
    user: User,
    day_index: int,
    picture_exposure_ok: bool | None,
    judges_stream_ok: bool | None,
    splitter_socket_ok: bool | None,
    key_stream_started_ok: bool | None,
    kick_ok: bool | None,
    mentions_four_ok: bool | None,
) -> BroadcastChecklist:
    row = await get_or_create_checklist(session, stream_event_id=stream_event_id, user=user, day_index=day_index)
    if picture_exposure_ok is not None:
        row.picture_exposure_ok = picture_exposure_ok
    if judges_stream_ok is not None:
        row.judges_stream_ok = judges_stream_ok
    if splitter_socket_ok is not None:
        row.splitter_socket_ok = splitter_socket_ok
    if key_stream_started_ok is not None:
        row.key_stream_started_ok = key_stream_started_ok
    if kick_ok is not None:
        row.kick_ok = kick_ok
    if mentions_four_ok is not None:
        row.mentions_four_ok = mentions_four_ok
    await session.commit()
    await session.refresh(row)
    return row
```


---

## Исходный код: `backend/app/services/dashboard_service.py`

> 59 строк, 3,287 байт

```py
from datetime import date, datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog
from app.models.enums import UserRole
from app.models.stream import StreamEvent
from app.models.user import User
from app.models.platform_extra import Notification
from app.services.stats_service import get_operator_stats_overview


async def build_dashboard_summary(session: AsyncSession, *, user: User) -> dict[str, Any]:
    role = user.role.value
    cards: list[dict[str, Any]] = []

    if user.role == UserRole.OPERATOR:
        n_streams = await session.scalar(select(func.count()).select_from(StreamEvent))
        cards.append({"key": "events", "title": "Мероприятий в системе", "value": int(n_streams or 0), "hint": "Все запланированные эфиры"})
        today = date.today()
        try:
            overview = await get_operator_stats_overview(session, stat_date=today)
            my_mentions = 0
            for o in overview.operators:
                if o.operator_id == user.id:
                    my_mentions = o.mentions_week
                    break
            cards.append(
                {
                    "key": "mentions_week",
                    "title": "Ваши упоминания за неделю (МСК)",
                    "value": my_mentions,
                    "hint": f"Всего по операторам за неделю: {overview.total_mentions_week}",
                }
            )
        except Exception:
            cards.append({"key": "mentions_today", "title": "Упоминания сегодня", "value": "—", "hint": "Статистика недоступна"})
        return {"role": role, "title": "Пульт оператора", "cards": cards}

    if user.role == UserRole.STREAM_MANAGER:
        n_streams = await session.scalar(select(func.count()).select_from(StreamEvent))
        cards.append({"key": "streams", "title": "Мероприятий", "value": int(n_streams or 0), "hint": "В каталоге"})
        return {"role": role, "title": "Трансляции и мероприятия", "cards": cards}

    # SUPERADMIN
    n_users = await session.scalar(select(func.count()).select_from(User))
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    n_audit = await session.scalar(select(func.count()).select_from(AuditLog).where(AuditLog.created_at >= since))
    cards.append({"key": "users", "title": "Пользователей", "value": int(n_users or 0), "hint": "В системе"})
    cards.append({"key": "audit24", "title": "Записей аудита за 24 ч", "value": int(n_audit or 0), "hint": "Журнал действий"})
    n_unread_notifications = await session.scalar(
        select(func.count()).select_from(Notification).where(Notification.user_id == user.id, Notification.is_read.is_(False))
    )
    cards.append({"key": "notif", "title": "Непрочитанных уведомлений", "value": int(n_unread_notifications or 0), "hint": "Колокольчик в шапке"})
    return {"role": role, "title": "Администрирование", "cards": cards}

```


---

## Исходный код: `backend/app/services/email_html_layout.py`

> 56 строк, 2,455 байт

```py
"""Единая вёрстка писем (inline CSS, таблицы — для совместимости с клиентами почты)."""

import html


def wrap_email_html(
    *,
    headline: str,
    inner_html: str,
    public_base_url: str = "",
    footer_line: str = "MainStream Ops · Сервис для видеооператоров MainStream",
) -> str:
    """Оборачивает контент в шапку/подвал. headline и URL экранируются."""
    safe_headline = html.escape(headline.strip() or "MainStream Ops")
    base = (public_base_url or "").strip().rstrip("/")
    if base:
        logo_url = f"{base}/mainstream-logo.png"
        logo_block = (
            f'<img src="{html.escape(logo_url, quote=True)}" alt="MainStream" width="168" '
            'style="display:block;border:0;outline:none;height:auto;max-width:100%" />'
        )
    else:
        logo_block = (
            '<span style="font-size:20px;font-weight:700;color:#e8eef8;letter-spacing:0.02em">'
            "MainStream Ops</span>"
        )
    safe_footer = html.escape(footer_line)
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>{safe_headline}</title>
</head>
<body style="margin:0;padding:0;background:#0a0e14;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#0a0e14;padding:24px 12px;">
<tr><td align="center">
<table role="presentation" width="600" cellspacing="0" cellpadding="0" style="max-width:600px;width:100%;background:#111822;border:1px solid #1f2a3a;border-radius:12px;overflow:hidden;">
<tr><td style="padding:28px 28px 20px;background:linear-gradient(180deg,#152030 0%,#111822 100%);border-bottom:1px solid #1f2a3a;text-align:center;">
{logo_block}
</td></tr>
<tr><td style="padding:16px 28px 8px;">
<p style="margin:0;font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif;font-size:18px;color:#f0f4fa;line-height:1.45;font-weight:600;">{safe_headline}</p>
</td></tr>
<tr><td style="padding:8px 28px 28px;font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6;color:#c5d0e0;">
{inner_html}
</td></tr>
<tr><td style="padding:16px 28px 22px;border-top:1px solid #1f2a3a;font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif;font-size:12px;color:#6b7c93;line-height:1.5;">
{safe_footer}
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>"""

```


---

## Исходный код: `backend/app/services/email_report_service.py`

> 192 строк, 7,277 байт

```py
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

```


---

## Исходный код: `backend/app/services/invite_service.py`

> 84 строк, 3,177 байт

```py
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.enums import AuditActionType, UserRole
from app.models.platform_extra import UserInvite
from app.models.user import User
from app.schemas.platform import AcceptInviteIn, InviteCreate
from app.services.audit_service import write_audit


async def create_invite(
    session: AsyncSession, *, actor_id: UUID, data: InviteCreate, expires_days: int = 7
) -> str:
    exists = await session.execute(select(User.id).where(User.email == data.email))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с таким email уже есть")
    token = secrets.token_urlsafe(48)[:64]
    now = datetime.now(timezone.utc)
    inv = UserInvite(
        token=token,
        email=data.email,
        role=data.role,
        created_by_user_id=actor_id,
        expires_at=now + timedelta(days=expires_days),
    )
    session.add(inv)
    await session.flush()
    await write_audit(
        session,
        user_id=actor_id,
        action_type=AuditActionType.USER_CREATE,
        entity_type="user_invite",
        entity_id=str(inv.id),
        payload_before=None,
        payload_after={"email": data.email, "role": data.role.value},
    )
    await session.commit()
    return token


async def accept_invite(session: AsyncSession, body: AcceptInviteIn) -> User:
    result = await session.execute(select(UserInvite).where(UserInvite.token == body.token))
    inv = result.scalar_one_or_none()
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Приглашение не найдено")
    if inv.used_at is not None:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Приглашение уже использовано")
    if inv.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Срок приглашения истёк")
    exists = await session.execute(select(User.id).where(User.email == inv.email))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email уже зарегистрирован")
    user = User(
        email=inv.email,
        first_name=body.first_name,
        last_name=body.last_name,
        password_hash=hash_password(body.password),
        role=inv.role,
        is_active=True,
        suggest_password_change=False,
        onboarding_completed=False,
    )
    session.add(user)
    inv.used_at = datetime.now(timezone.utc)
    await session.flush()
    await write_audit(
        session,
        user_id=user.id,
        action_type=AuditActionType.USER_CREATE,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=None,
        payload_after={"email": user.email, "via": "invite"},
    )
    await session.commit()
    await session.refresh(user)
    return user

```


---

## Исходный код: `backend/app/services/logo_service.py`

> 250 строк, 8,700 байт

```py
"""Медиатека логотипов и связь с мероприятиями."""

import io
import re
import zipfile
from pathlib import Path
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.timezone import format_moscow_date
from app.models.enums import AuditActionType
from app.models.logo import Logo, StreamEventLogo
from app.models.stream import StreamEvent
from app.models.user import User
from app.schemas.logo import LogoLibraryItemOut
from app.services.audit_service import write_audit
from app.services.stream_service import _get_event

ALLOWED_LOGO_TYPES = {
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
    "image/svg+xml",
}
MAX_LOGO_BYTES = 15 * 1024 * 1024


def _safe_original_filename(name: str) -> str:
    base = Path(name).name
    if not base or base in (".", ".."):
        return "logo.bin"
    base = re.sub(r"[^\w.\- \u0400-\u04FF]", "_", base)
    return base[:240] if len(base) > 240 else base


def logo_library_item(logo: Logo) -> LogoLibraryItemOut:
    pub = f"/uploads/{logo.stored_path.lstrip('/')}"
    return LogoLibraryItemOut(
        id=logo.id,
        filename_original=logo.filename_original,
        public_url=pub,
        created_at=logo.created_at,
        uploaded_by_id=logo.uploaded_by_id,
    )


async def _persist_one_logo(session: AsyncSession, *, actor: User, file: UploadFile) -> Logo:
    ct = file.content_type or ""
    if ct not in ALLOWED_LOGO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Допустимы только PNG, JPEG, GIF, WebP, SVG",
        )
    raw_name = file.filename or "logo"
    filename_original = _safe_original_filename(raw_name)
    data = await file.read()
    if len(data) > MAX_LOGO_BYTES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл больше 15 МБ")

    settings = get_settings()
    logo = Logo(
        filename_original=filename_original,
        stored_path="",
        uploaded_by_id=actor.id,
    )
    session.add(logo)
    await session.flush()

    subdir = Path(settings.upload_dir) / "logos" / str(logo.id)
    subdir.mkdir(parents=True, exist_ok=True)
    dest_name = filename_original
    dest_path = subdir / dest_name
    dest_path.write_bytes(data)
    rel = f"logos/{logo.id}/{dest_name}"
    logo.stored_path = rel
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.LOGO_UPLOAD,
        entity_type="logo",
        entity_id=str(logo.id),
        payload_before=None,
        payload_after={"filename_original": filename_original, "stored_path": rel},
    )
    return logo


async def upload_logo(session: AsyncSession, *, actor: User, file: UploadFile) -> LogoLibraryItemOut:
    logo = await _persist_one_logo(session, actor=actor, file=file)
    await session.commit()
    await session.refresh(logo)
    return logo_library_item(logo)


async def upload_logos_batch(
    session: AsyncSession, *, actor: User, files: list[UploadFile]
) -> list[LogoLibraryItemOut]:
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нет файлов")
    if len(files) > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не более 50 файлов за раз")
    logos: list[Logo] = []
    for f in files:
        logos.append(await _persist_one_logo(session, actor=actor, file=f))
    await session.commit()
    out: list[LogoLibraryItemOut] = []
    for lg in logos:
        await session.refresh(lg)
        out.append(logo_library_item(lg))
    return out


async def list_library(session: AsyncSession) -> list[LogoLibraryItemOut]:
    result = await session.execute(select(Logo).order_by(Logo.created_at.desc()))
    rows = list(result.scalars().all())
    return [logo_library_item(x) for x in rows]


async def _stream_logo_link(
    session: AsyncSession, *, stream_id: UUID, logo_id: UUID
) -> StreamEventLogo | None:
    r = await session.execute(
        select(StreamEventLogo).where(
            StreamEventLogo.stream_event_id == stream_id,
            StreamEventLogo.logo_id == logo_id,
        )
    )
    return r.scalar_one_or_none()


async def attach_logo_to_stream(
    session: AsyncSession, *, actor: User, stream_id: UUID, logo_id: UUID
) -> None:
    await _get_event(session, stream_id)
    lr = await session.execute(select(Logo).where(Logo.id == logo_id))
    logo = lr.scalar_one_or_none()
    if not logo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Логотип не найден")
    if await _stream_logo_link(session, stream_id=stream_id, logo_id=logo_id):
        return
    max_r = await session.execute(
        select(StreamEventLogo.sort_order)
        .where(StreamEventLogo.stream_event_id == stream_id)
        .order_by(StreamEventLogo.sort_order.desc())
        .limit(1)
    )
    mx = max_r.scalar_one_or_none()
    nxt = (int(mx) + 1) if mx is not None else 0
    session.add(StreamEventLogo(stream_event_id=stream_id, logo_id=logo_id, sort_order=nxt))
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.LOGO_ATTACH,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before=None,
        payload_after={"logo_id": str(logo_id), "filename": logo.filename_original},
    )
    await session.commit()


async def detach_logo_from_stream(
    session: AsyncSession, *, actor: User, stream_id: UUID, logo_id: UUID
) -> None:
    await _get_event(session, stream_id)
    link = await _stream_logo_link(session, stream_id=stream_id, logo_id=logo_id)
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Связь не найдена")
    await session.delete(link)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.LOGO_DETACH,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before={"logo_id": str(logo_id)},
        payload_after=None,
    )
    await session.commit()


def logo_file_abs_path(stored_path: str) -> Path:
    settings = get_settings()
    return Path(settings.upload_dir) / stored_path


async def get_logo_row(session: AsyncSession, logo_id: UUID) -> Logo | None:
    r = await session.execute(select(Logo).where(Logo.id == logo_id))
    return r.scalar_one_or_none()


async def assert_logo_on_stream(session: AsyncSession, *, stream_id: UUID, logo_id: UUID) -> None:
    await _get_event(session, stream_id)
    link = await _stream_logo_link(session, stream_id=stream_id, logo_id=logo_id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Логотип не прикреплён к этому мероприятию",
        )


def stream_zip_filename(title: str, moscow_date_str: str) -> str:
    safe = re.sub(r"[^\w\-]+", "_", title).strip("_")[:60] or "stream"
    return f"{safe}_{moscow_date_str}_assets.zip"


async def build_stream_logos_zip(session: AsyncSession, *, stream_id: UUID) -> tuple[bytes, str]:
    ev = await _get_event(session, stream_id)
    result = await session.execute(
        select(StreamEventLogo)
        .options(selectinload(StreamEventLogo.logo))
        .where(StreamEventLogo.stream_event_id == stream_id)
        .order_by(StreamEventLogo.sort_order)
    )
    links = list(result.scalars().all())
    if not links:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Нет логотипов для выгрузки")

    date_str = format_moscow_date(ev.start_date)
    zip_name = stream_zip_filename(ev.title, date_str)

    buf = io.BytesIO()
    seen_counts: dict[str, int] = {}
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for link in links:
            lg = link.logo
            if not lg:
                continue
            path = logo_file_abs_path(lg.stored_path)
            if not path.is_file():
                continue
            orig = lg.filename_original
            n = seen_counts.get(orig, 0)
            seen_counts[orig] = n + 1
            if n == 0:
                inner = orig
            else:
                stem = Path(orig).stem
                suf = Path(orig).suffix
                inner = f"{stem}_{n}{suf}"
            zf.write(path, arcname=inner)
    buf.seek(0)
    return buf.getvalue(), zip_name

```


---

## Исходный код: `backend/app/services/notification_service.py`

> 69 строк, 1,988 байт

```py
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import UserRole
from app.models.platform_extra import Notification
from app.models.user import User


async def create_for_users_with_roles(
    session: AsyncSession,
    *,
    roles: list[UserRole],
    title: str,
    body: str,
    kind: str | None = None,
) -> None:
    q = select(User.id).where(User.role.in_(roles), User.is_active.is_(True))
    result = await session.execute(q)
    for (uid,) in result.all():
        session.add(
            Notification(
                user_id=uid,
                title=title,
                body=body,
                kind=kind,
            )
        )


async def count_unread(session: AsyncSession, *, user_id: UUID) -> int:
    q = select(func.count()).where(
        Notification.user_id == user_id,
        Notification.is_read.is_(False),
    )
    result = await session.execute(q)
    return int(result.scalar_one() or 0)


async def list_notifications(
    session: AsyncSession, *, user_id: UUID, limit: int = 50
) -> list[Notification]:
    q = (
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(q)
    return list(result.scalars().all())


async def mark_read(session: AsyncSession, *, user_id: UUID, notification_id: UUID) -> bool:
    result = await session.execute(
        select(Notification).where(Notification.id == notification_id, Notification.user_id == user_id)
    )
    n = result.scalar_one_or_none()
    if not n:
        return False
    n.is_read = True
    return True


async def mark_all_read(session: AsyncSession, *, user_id: UUID) -> None:
    result = await session.execute(select(Notification).where(Notification.user_id == user_id, Notification.is_read.is_(False)))
    for n in result.scalars().all():
        n.is_read = True

```


---

## Исходный код: `backend/app/services/password_reset_email_service.py`

> 99 строк, 3,974 байт

```py
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

```


---

## Исходный код: `backend/app/services/password_reset_service.py`

> 123 строк, 4,770 байт

```py
import hashlib
import logging
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import hash_password
from app.models.enums import AuditActionType
from app.models.user import PasswordResetToken, RefreshToken, User
from app.services.audit_service import write_audit

log = logging.getLogger(__name__)


def hash_reset_token(raw: str) -> str:
    return hashlib.sha256(raw.strip().encode("utf-8")).hexdigest()


async def request_password_reset(session: AsyncSession, *, email: str) -> tuple[str | None, str | None, str]:
    """
    При активном пользователе и настроенных SMTP + APP_PUBLIC_BASE_URL создаёт токен.
    Возвращает (reset_link, to_email, greeting_name) для фоновой отправки; link/email могут быть None.
    """
    settings = get_settings()
    normalized = (email or "").strip().lower()
    greeting = ""
    if not normalized:
        return None, None, greeting
    result = await session.execute(select(User).where(func.lower(User.email) == normalized))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        return None, None, greeting
    greeting = (user.first_name or "").strip() or user.email.split("@", 1)[0]
    base = (settings.app_public_base_url or "").strip().rstrip("/")
    smtp_ok = bool((settings.smtp_host or "").strip())
    if not smtp_ok or not base:
        log.warning(
            "Password reset skipped: need SMTP_HOST and APP_PUBLIC_BASE_URL (user_id=%s)",
            user.id,
        )
        return None, None, greeting
    await session.execute(
        delete(PasswordResetToken).where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        )
    )
    raw = secrets.token_urlsafe(40)
    token_hash = hash_reset_token(raw)
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.password_reset_expire_minutes)
    session.add(
        PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=exp,
        )
    )
    await session.commit()
    reset_link = f"{base}/reset-password?token={raw}"
    return reset_link, user.email, greeting


async def token_is_valid(session: AsyncSession, *, raw_token: str) -> bool:
    if not raw_token or len(raw_token) < 20:
        return False
    th = hash_reset_token(raw_token)
    now = datetime.now(timezone.utc)
    result = await session.execute(
        select(PasswordResetToken.id).where(
            PasswordResetToken.token_hash == th,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > now,
        )
    )
    return result.scalar_one_or_none() is not None


async def reset_password_with_token(session: AsyncSession, *, raw_token: str, new_password: str) -> None:
    if not raw_token or len(raw_token) < 20:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недействительная ссылка")
    th = hash_reset_token(raw_token)
    now = datetime.now(timezone.utc)
    result = await session.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == th,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > now,
        )
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ссылка недействительна или истекла. Запросите новую на странице входа.",
        )
    user_result = await session.execute(select(User).where(User.id == row.user_id))
    user = user_result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь не найден")
    user.password_hash = hash_password(new_password)
    user.suggest_password_change = False
    row.used_at = now
    rt_result = await session.execute(
        select(RefreshToken).where(RefreshToken.user_id == user.id, RefreshToken.revoked_at.is_(None))
    )
    for rt in rt_result.scalars().all():
        rt.revoked_at = now
    await write_audit(
        session,
        user_id=user.id,
        action_type=AuditActionType.USER_UPDATE,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=None,
        payload_after={"password_reset_via_email": True},
    )
    await session.commit()

```


---

## Исходный код: `backend/app/services/profile_service.py`

> 85 строк, 3,264 байт

```py
import uuid
from pathlib import Path
from typing import Any

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.user import User
from app.schemas.profile import ProfileUpdate
from app.utils.phone_ru import normalize_ru_mobile_phone


async def update_profile(session: AsyncSession, *, user_id: uuid.UUID, data: ProfileUpdate) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    if data.first_name is not None:
        user.first_name = data.first_name
    if data.last_name is not None:
        user.last_name = data.last_name
    if data.phone is not None:
        trimmed = (data.phone or "").strip()
        if not trimmed:
            user.phone = None
        else:
            try:
                user.phone = normalize_ru_mobile_phone(trimmed)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e) or "Некорректный номер телефона",
                ) from e
    if data.telegram is not None:
        user.telegram = data.telegram or None
    if data.onboarding_completed is not None:
        user.onboarding_completed = data.onboarding_completed
    if data.suggest_password_change is not None:
        if data.suggest_password_change:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Включить подсказку смены пароля через профиль нельзя",
            )
        user.suggest_password_change = False
    await session.commit()
    await session.refresh(user)
    return user


ALLOWED_AVATAR = {"image/jpeg", "image/png", "image/webp"}
EXT = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}


async def save_avatar_file(
    session: AsyncSession,
    *,
    user_id: uuid.UUID,
    file: UploadFile,
) -> User:
    if file.content_type not in ALLOWED_AVATAR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Допустимы только JPEG, PNG, WebP",
        )
    settings = get_settings()
    base = Path(settings.upload_dir) / "avatars"
    base.mkdir(parents=True, exist_ok=True)
    ext = EXT.get(file.content_type, ".bin")
    dest = base / f"{user_id}{ext}"
    data = await file.read()
    if len(data) > 2 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл больше 2 МБ")
    dest.write_bytes(data)
    public_path = f"/uploads/avatars/{user_id}{ext}"
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    user.avatar_url = public_path
    await session.commit()
    await session.refresh(user)
    return user

```


---

## Исходный код: `backend/app/services/report_scheduler.py`

> 45 строк, 1,543 байт

```py
"""Планировщик: пн 00:05 и 1-е число 00:10 (МСК) — отчёты на почту."""

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

```


---

## Исходный код: `backend/app/services/report_service.py`

> 226 строк, 7,674 байт

```py
import csv
import io
from datetime import date, datetime, time, timedelta, timezone
from io import BytesIO
from uuid import UUID

from docx import Document
from openpyxl import Workbook
from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.timezone import MOSCOW_TZ, add_seconds_to_start, format_moscow_date, format_moscow_datetime
from app.models.stream import BroadcastSession, SponsorMention, StreamEvent
from app.schemas.report import ReportMentionRow, ReportMentionsOut
from app.utils.timecode import seconds_to_hhmmss


def _range_utc_moscow_days(date_from: date, date_to: date) -> tuple[datetime, datetime]:
    start_local = datetime.combine(date_from, time.min, tzinfo=MOSCOW_TZ)
    end_exclusive_local = datetime.combine(date_to + timedelta(days=1), time.min, tzinfo=MOSCOW_TZ)
    return start_local.astimezone(timezone.utc), end_exclusive_local.astimezone(timezone.utc)


async def get_mentions_report(
    session: AsyncSession,
    *,
    stream_event_id: UUID | None,
    date_from: date | None,
    date_to: date | None,
) -> ReportMentionsOut:
    q = (
        select(SponsorMention)
        .join(BroadcastSession)
        .join(StreamEvent)
        .options(
            selectinload(SponsorMention.broadcast_session).selectinload(BroadcastSession.stream_event),
        )
    )
    conds = []
    if stream_event_id is not None:
        conds.append(StreamEvent.id == stream_event_id)
    if date_from is not None and date_to is not None:
        start_utc, end_exc = _range_utc_moscow_days(date_from, date_to)
        conds.append(and_(SponsorMention.created_at >= start_utc, SponsorMention.created_at < end_exc))
    elif date_from is not None or date_to is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Укажите обе даты диапазона (date_from и date_to)",
        )
    if conds:
        q = q.where(and_(*conds))
    # Сначала турнир (дата старта, id), затем день эфира, затем порядок упоминаний — без перемешивания турниров
    q = q.order_by(
        StreamEvent.start_date.asc(),
        StreamEvent.id.asc(),
        BroadcastSession.day_index.asc(),
        BroadcastSession.started_at.asc(),
        SponsorMention.created_at.asc(),
    )
    result = await session.execute(q)
    rows: list[ReportMentionRow] = []
    for m in result.scalars().all():
        bs = m.broadcast_session
        ev = bs.stream_event
        started = bs.started_at if bs.started_at.tzinfo else bs.started_at.replace(tzinfo=timezone.utc)
        abs_adj = add_seconds_to_start(started, m.adjusted_offset_sec)
        event_day_date = ev.start_date + timedelta(days=bs.day_index - 1)
        rows.append(
            ReportMentionRow(
                mention_id=m.id,
                stream_event_id=ev.id,
                stream_title=ev.title,
                event_day_date=event_day_date,
                day_index=bs.day_index,
                broadcast_session_id=bs.id,
                original_timecode=seconds_to_hhmmss(m.original_offset_sec),
                adjusted_timecode=seconds_to_hhmmss(m.adjusted_offset_sec),
                absolute_moscow_adjusted=format_moscow_datetime(abs_adj),
                is_adjusted=m.original_offset_sec != m.adjusted_offset_sec,
                mention_created_at=m.created_at,
            )
        )
    return ReportMentionsOut(items=rows, total=len(rows))


def build_docx_report(rows: list[ReportMentionRow]) -> bytes:
    doc = Document()
    rows_sorted = sorted(
        rows,
        key=lambda r: (r.stream_event_id, r.day_index, r.mention_created_at),
    )
    current_key: tuple[UUID, int] | None = None
    mention_idx = 0
    for row in rows_sorted:
        key = (row.stream_event_id, row.day_index)
        if key != current_key:
            if current_key is not None:
                doc.add_paragraph("")
            current_key = key
            mention_idx = 0
            doc.add_heading(row.stream_title, level=1)
            doc.add_paragraph(f"Дата: {format_moscow_date(row.event_day_date)}")
            doc.add_paragraph(f"День эфира: {row.day_index}")
        mention_idx += 1
        doc.add_paragraph(
            f"Упоминание {mention_idx} — таймкод {row.adjusted_timecode}, "
            f"абсолютное (МСК): {row.absolute_moscow_adjusted}, "
            f"запись: {format_moscow_datetime(row.mention_created_at)}",
        )
    buffer = BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def build_csv_report(rows: list[ReportMentionRow]) -> bytes:
    rows_sorted = sorted(rows, key=lambda r: (r.stream_event_id, r.day_index, r.mention_created_at))
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(
        [
            "stream_title",
            "event_day_date",
            "day_index",
            "original_timecode",
            "adjusted_timecode",
            "absolute_moscow_adjusted",
            "mention_created_at",
        ]
    )
    for row in rows_sorted:
        w.writerow(
            [
                row.stream_title,
                row.event_day_date.isoformat(),
                row.day_index,
                row.original_timecode,
                row.adjusted_timecode,
                row.absolute_moscow_adjusted,
                row.mention_created_at.isoformat(),
            ]
        )
    return buf.getvalue().encode("utf-8-sig")


def build_xlsx_report(rows: list[ReportMentionRow]) -> bytes:
    rows_sorted = sorted(rows, key=lambda r: (r.stream_event_id, r.day_index, r.mention_created_at))
    wb = Workbook()
    ws = wb.active
    ws.title = "mentions"
    ws.append(
        [
            "stream_title",
            "event_day_date",
            "day_index",
            "original_timecode",
            "adjusted_timecode",
            "absolute_moscow_adjusted",
            "mention_created_at",
        ]
    )
    for row in rows_sorted:
        ws.append(
            [
                row.stream_title,
                row.event_day_date.isoformat(),
                row.day_index,
                row.original_timecode,
                row.adjusted_timecode,
                row.absolute_moscow_adjusted,
                row.mention_created_at.isoformat(),
            ]
        )
    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


async def export_mentions_docx(
    session: AsyncSession,
    *,
    stream_event_id: UUID | None,
    date_from: date | None,
    date_to: date | None,
) -> bytes:
    data = await get_mentions_report(
        session,
        stream_event_id=stream_event_id,
        date_from=date_from,
        date_to=date_to,
    )
    return build_docx_report(data.items)


async def export_mentions_csv(
    session: AsyncSession,
    *,
    stream_event_id: UUID | None,
    date_from: date | None,
    date_to: date | None,
) -> bytes:
    data = await get_mentions_report(
        session,
        stream_event_id=stream_event_id,
        date_from=date_from,
        date_to=date_to,
    )
    return build_csv_report(data.items)


async def export_mentions_xlsx(
    session: AsyncSession,
    *,
    stream_event_id: UUID | None,
    date_from: date | None,
    date_to: date | None,
) -> bytes:
    data = await get_mentions_report(
        session,
        stream_event_id=stream_event_id,
        date_from=date_from,
        date_to=date_to,
    )
    return build_xlsx_report(data.items)

```


---

## Исходный код: `backend/app/services/stats_service.py`

> 151 строк, 5,704 байт

```py
import calendar
from datetime import date, datetime, time, timedelta, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.timezone import MOSCOW_TZ
from app.models.enums import UserRole
from app.models.stream import BroadcastSession, SponsorMention, StreamDayAssignment, StreamEvent
from app.models.user import User
from app.schemas.stats import LockAssignmentOut, OperatorDayStatsOut, OperatorStatsOverviewOut
from app.services.stream_service import _assignment_summary_from_pairs, _load_assignment_pairs
from app.utils.display_name import user_display_name

MENTIONS_PER_BROADCAST = 4


def _moscow_day_bounds_utc(d: date) -> tuple[datetime, datetime]:
    start_local = datetime.combine(d, time.min, tzinfo=MOSCOW_TZ)
    end_local = start_local + timedelta(days=1)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)


def _moscow_range_to_utc(day_from: date, day_to_inclusive: date) -> tuple[datetime, datetime]:
    start_local = datetime.combine(day_from, time.min, tzinfo=MOSCOW_TZ)
    end_local = datetime.combine(day_to_inclusive + timedelta(days=1), time.min, tzinfo=MOSCOW_TZ)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)


def _week_mon_sun_moscow(d: date) -> tuple[date, date]:
    mon = d - timedelta(days=d.weekday())
    sun = mon + timedelta(days=6)
    return mon, sun


def _month_first_last(d: date) -> tuple[date, date]:
    first = d.replace(day=1)
    last = d.replace(day=calendar.monthrange(d.year, d.month)[1])
    return first, last


async def _count_broadcasts(
    session: AsyncSession, operator_id: UUID, start_utc: datetime, end_utc: datetime
) -> int:
    r = await session.execute(
        select(func.count())
        .select_from(BroadcastSession)
        .where(
            BroadcastSession.operator_id == operator_id,
            BroadcastSession.started_at >= start_utc,
            BroadcastSession.started_at < end_utc,
        )
    )
    return int(r.scalar_one() or 0)


async def _count_mentions(
    session: AsyncSession, operator_id: UUID, start_utc: datetime, end_utc: datetime
) -> int:
    r = await session.execute(
        select(func.count())
        .select_from(SponsorMention)
        .join(BroadcastSession, SponsorMention.broadcast_session_id == BroadcastSession.id)
        .where(
            BroadcastSession.operator_id == operator_id,
            SponsorMention.created_at >= start_utc,
            SponsorMention.created_at < end_utc,
        )
    )
    return int(r.scalar_one() or 0)


async def get_operator_stats_overview(session: AsyncSession, *, stat_date: date) -> OperatorStatsOverviewOut:
    week_start, week_end = _week_mon_sun_moscow(stat_date)
    month_start, month_end = _month_first_last(stat_date)
    w0, w1 = _moscow_range_to_utc(week_start, week_end)
    m0, m1 = _moscow_range_to_utc(month_start, month_end)

    # Назначения по дням (сводка по событиям)
    sid_rows = await session.execute(select(StreamDayAssignment.stream_event_id.distinct()))
    stream_ids = list(sid_rows.scalars().all())
    pairs_by = await _load_assignment_pairs(session, stream_ids)
    assignments: list[LockAssignmentOut] = []
    if stream_ids:
        evs = (await session.execute(select(StreamEvent).where(StreamEvent.id.in_(stream_ids)))).scalars().all()
        by_ev = {e.id: e for e in evs}
        for seid in sorted(stream_ids, key=lambda x: (by_ev.get(x).title if by_ev.get(x) else "", str(x))):
            ev = by_ev.get(seid)
            if not ev:
                continue
            summary = _assignment_summary_from_pairs(pairs_by.get(seid, [])) or "—"
            assignments.append(
                LockAssignmentOut(
                    stream_event_id=seid,
                    title=ev.title,
                    summary=summary,
                )
            )

    users_result = await session.execute(
        select(User).where(User.role == UserRole.OPERATOR, User.is_active.is_(True)).order_by(User.email)
    )
    operators_list = list(users_result.scalars().all())

    operators: list[OperatorDayStatsOut] = []
    tb_w = tm_w = tb_m = tm_m = 0
    for u in operators_list:
        bw = await _count_broadcasts(session, u.id, w0, w1)
        mw = await _count_mentions(session, u.id, w0, w1)
        bm = await _count_broadcasts(session, u.id, m0, m1)
        mm = await _count_mentions(session, u.id, m0, m1)
        tb_w += bw
        tm_w += mw
        tb_m += bm
        tm_m += mm
        norm_w = MENTIONS_PER_BROADCAST * bw
        norm_m = MENTIONS_PER_BROADCAST * bm
        met_w = mw >= norm_w if bw > 0 else True
        met_m = mm >= norm_m if bm > 0 else True
        operators.append(
            OperatorDayStatsOut(
                operator_id=u.id,
                email=u.email,
                display_name=user_display_name(u),
                role=u.role.value,
                broadcasts_week=bw,
                mentions_week=mw,
                mentions_norm_week=norm_w,
                mentions_met_week=met_w,
                broadcasts_month=bm,
                mentions_month=mm,
                mentions_norm_month=norm_m,
                mentions_met_month=met_m,
            )
        )

    return OperatorStatsOverviewOut(
        stat_date=stat_date,
        week_start=week_start,
        week_end=week_end,
        month_start=month_start,
        month_end=month_end,
        assignments=assignments,
        operators=operators,
        total_broadcasts_week=tb_w,
        total_mentions_week=tm_w,
        total_broadcasts_month=tb_m,
        total_mentions_month=tm_m,
    )

```


---

## Исходный код: `backend/app/services/stream_service.py`

> 1187 строк, 45,960 байт

```py
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import and_, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.timezone import MOSCOW_TZ, add_seconds_to_start, format_moscow_datetime, utc_now
from app.models.enums import AuditActionType, UserRole
from app.models.logo import StreamEventLogo
from app.models.stream import (
    BroadcastSession,
    MentionAdjustment,
    SponsorMention,
    StreamDay,
    StreamDayAssignment,
    StreamEvent,
    StreamEventTemplate,
)
from app.models.user import User
from app.schemas.logo import StreamLogoItemOut
from app.schemas.stream import (
    BroadcastSessionOut,
    DayAssignmentOut,
    MentionAdjustmentOut,
    SponsorMentionOut,
    StreamDayIn,
    StreamDayOut,
    StreamEventCreate,
    StreamDayLinkOut,
    StreamEventDetailOut,
    StreamEventListOut,
    StreamEventUpdate,
)
from app.services.audit_service import write_audit
from app.services.notification_service import create_for_users_with_roles
from app.utils.display_name import user_display_name
from app.utils.timecode import seconds_to_hhmmss

# Повторный старт эфира запрещён, если был завершённый эфир дольше этого порога и с упоминаниями (таймкодами)
BROADCAST_RESTART_BLOCK_MIN_DURATION = timedelta(hours=1)


def _mention_to_out(mention: SponsorMention) -> SponsorMentionOut:
    bs = mention.broadcast_session
    started = bs.started_at
    if started.tzinfo is None:
        started = started.replace(tzinfo=timezone.utc)
    abs_orig = add_seconds_to_start(started, mention.original_offset_sec)
    abs_adj = add_seconds_to_start(started, mention.adjusted_offset_sec)
    adjustments = [
        MentionAdjustmentOut.model_validate(a) for a in sorted(mention.adjustments, key=lambda x: x.created_at)
    ]
    return SponsorMentionOut(
        id=mention.id,
        broadcast_session_id=mention.broadcast_session_id,
        original_offset_sec=mention.original_offset_sec,
        adjusted_offset_sec=mention.adjusted_offset_sec,
        original_timecode=seconds_to_hhmmss(mention.original_offset_sec),
        adjusted_timecode=seconds_to_hhmmss(mention.adjusted_offset_sec),
        absolute_moscow_original=format_moscow_datetime(abs_orig),
        absolute_moscow_adjusted=format_moscow_datetime(abs_adj),
        is_adjusted=mention.original_offset_sec != mention.adjusted_offset_sec,
        created_at=mention.created_at,
        adjustments=adjustments,
    )


async def _get_event(session: AsyncSession, stream_id: UUID) -> StreamEvent:
    result = await session.execute(
        select(StreamEvent)
        .options(
            selectinload(StreamEvent.days),
            selectinload(StreamEvent.broadcast_sessions),
            selectinload(StreamEvent.event_logos).selectinload(StreamEventLogo.logo),
        )
        .where(StreamEvent.id == stream_id)
    )
    ev = result.scalar_one_or_none()
    if not ev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Мероприятие не найдено")
    return ev


def _logos_for_stream(ev: StreamEvent) -> list[StreamLogoItemOut]:
    if not ev.event_logos:
        return []
    items: list[StreamLogoItemOut] = []
    for link in sorted(ev.event_logos, key=lambda x: x.sort_order):
        lg = link.logo
        if not lg:
            continue
        pub = f"/uploads/{lg.stored_path.lstrip('/')}"
        items.append(
            StreamLogoItemOut(
                id=lg.id,
                filename_original=lg.filename_original,
                public_url=pub,
                sort_order=link.sort_order,
                created_at=lg.created_at,
            )
        )
    return items


async def assert_valid_stream_day(session: AsyncSession, stream_id: UUID, day_index: int) -> None:
    if day_index < 1 or day_index > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный день")
    ev = await _get_event(session, stream_id)
    if day_index > ev.duration_days:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="День вне длительности мероприятия")


async def _broadcast_restart_blocked_days(
    session: AsyncSession, *, stream_id: UUID, duration_days: int
) -> list[int]:
    """Дни, для которых нельзя снова начать эфир (уже был длинный эфир с таймкодами)."""
    result = await session.execute(
        select(BroadcastSession.id, BroadcastSession.day_index, BroadcastSession.started_at, BroadcastSession.ended_at).where(
            BroadcastSession.stream_event_id == stream_id,
            BroadcastSession.ended_at.isnot(None),
        )
    )
    long_with_mentions: list[tuple[UUID, int]] = []
    for sid, d_idx, started, ended in result.all():
        if d_idx < 1 or d_idx > duration_days or not started or not ended:
            continue
        if ended - started <= BROADCAST_RESTART_BLOCK_MIN_DURATION:
            continue
        long_with_mentions.append((sid, d_idx))
    if not long_with_mentions:
        return []
    session_ids = [x[0] for x in long_with_mentions]
    cnt_r = await session.execute(
        select(SponsorMention.broadcast_session_id, func.count())
        .where(SponsorMention.broadcast_session_id.in_(session_ids))
        .group_by(SponsorMention.broadcast_session_id)
    )
    with_counts = {row[0]: int(row[1]) for row in cnt_r.all()}
    blocked: set[int] = set()
    for sid, d_idx in long_with_mentions:
        if with_counts.get(sid, 0) > 0:
            blocked.add(d_idx)
    return sorted(blocked)


async def _day_blocked_for_new_broadcast(
    session: AsyncSession, *, stream_id: UUID, day_index: int, duration_days: int
) -> bool:
    blocked = await _broadcast_restart_blocked_days(session, stream_id=stream_id, duration_days=duration_days)
    return day_index in blocked


async def _assignment_operator_for_day(
    session: AsyncSession, stream_id: UUID, day_index: int
) -> UUID | None:
    r = await session.execute(
        select(StreamDayAssignment.operator_id).where(
            StreamDayAssignment.stream_event_id == stream_id,
            StreamDayAssignment.day_index == day_index,
        )
    )
    return r.scalar_one_or_none()


def _format_days_label(days: list[int]) -> str:
    days = sorted(days)
    if len(days) == 1:
        return str(days[0])
    if days == list(range(days[0], days[-1] + 1)):
        return f"{days[0]}–{days[-1]}"
    return ", ".join(str(d) for d in days)


def _assignment_summary_from_pairs(pairs: list[tuple[int, User]]) -> str | None:
    if not pairs:
        return None
    by_op: dict[UUID, list[int]] = defaultdict(list)
    users: dict[UUID, User] = {}
    for day_idx, u in pairs:
        by_op[u.id].append(day_idx)
        users[u.id] = u
    parts: list[str] = []
    for uid in sorted(users.keys(), key=lambda x: str(x)):
        u = users[uid]
        parts.append(f"{user_display_name(u)}: дни {_format_days_label(by_op[uid])}")
    return "; ".join(parts)


async def _load_assignment_pairs(
    session: AsyncSession, stream_ids: list[UUID]
) -> dict[UUID, list[tuple[int, User]]]:
    if not stream_ids:
        return {}
    q = (
        select(StreamDayAssignment, User)
        .join(User, StreamDayAssignment.operator_id == User.id)
        .where(StreamDayAssignment.stream_event_id.in_(stream_ids))
        .order_by(StreamDayAssignment.stream_event_id, StreamDayAssignment.day_index)
    )
    rows = (await session.execute(q)).all()
    out: dict[UUID, list[tuple[int, User]]] = defaultdict(list)
    for a, u in rows:
        out[a.stream_event_id].append((a.day_index, u))
    return out


async def _day_assignments_out(session: AsyncSession, stream_id: UUID) -> list[DayAssignmentOut]:
    pairs = (await _load_assignment_pairs(session, [stream_id])).get(stream_id, [])
    return [
        DayAssignmentOut(
            day_index=d,
            operator_id=u.id,
            operator_display_name=user_display_name(u),
            operator_email=u.email,
        )
        for d, u in pairs
    ]


async def _stream_has_assignments_to_other_than(
    session: AsyncSession, *, stream_event_id: UUID, user_id: UUID
) -> bool:
    r = await session.execute(
        select(func.count())
        .select_from(StreamDayAssignment)
        .where(
            StreamDayAssignment.stream_event_id == stream_event_id,
            StreamDayAssignment.operator_id != user_id,
        )
    )
    return int(r.scalar_one() or 0) > 0


async def _sync_legacy_locked_by(session: AsyncSession, ev: StreamEvent) -> None:
    r = await session.execute(
        select(StreamDayAssignment.operator_id)
        .where(StreamDayAssignment.stream_event_id == ev.id)
        .distinct()
    )
    ids = list(r.scalars().all())
    if len(ids) == 1:
        ev.locked_by_user_id = ids[0]
    else:
        ev.locked_by_user_id = None


async def _active_broadcast_ids(session: AsyncSession) -> set[UUID]:
    q = select(BroadcastSession.stream_event_id).where(BroadcastSession.ended_at.is_(None))
    result = await session.execute(q)
    return set(result.scalars().all())


async def _ended_broadcast_ids(session: AsyncSession) -> set[UUID]:
    q = select(BroadcastSession.stream_event_id).where(BroadcastSession.ended_at.isnot(None))
    result = await session.execute(q)
    return set(result.scalars().all())


async def _ended_broadcast_days_by_event(session: AsyncSession) -> dict[UUID, list[int]]:
    q = (
        select(BroadcastSession.stream_event_id, BroadcastSession.day_index)
        .where(BroadcastSession.ended_at.isnot(None))
        .distinct()
        .order_by(BroadcastSession.stream_event_id, BroadcastSession.day_index)
    )
    result = await session.execute(q)
    out: dict[UUID, list[int]] = defaultdict(list)
    for stream_event_id, day_index in result.all():
        out[stream_event_id].append(day_index)
    return out


async def _users_by_ids(session: AsyncSession, user_ids: set[UUID]) -> dict[UUID, User]:
    if not user_ids:
        return {}
    result = await session.execute(select(User).where(User.id.in_(list(user_ids))))
    return {u.id: u for u in result.scalars().all()}


async def _locked_by_display_name(session: AsyncSession, locked_by_user_id: UUID | None) -> str | None:
    if locked_by_user_id is None:
        return None
    result = await session.execute(select(User).where(User.id == locked_by_user_id))
    u = result.scalar_one_or_none()
    return user_display_name(u) if u else None


async def list_stream_events(
    session: AsyncSession,
    *,
    viewer: User | None = None,
) -> list[StreamEventListOut]:
    active_ids = await _active_broadcast_ids(session)
    ended_ids = await _ended_broadcast_ids(session)
    ended_days_by_event = await _ended_broadcast_days_by_event(session)
    result = await session.execute(select(StreamEvent).order_by(StreamEvent.start_date.desc(), StreamEvent.created_at.desc()))
    events = list(result.scalars().all())
    eids = [e.id for e in events]
    days_by_event: dict[UUID, list[StreamDay]] = defaultdict(list)
    if eids:
        dr = await session.execute(
            select(StreamDay)
            .where(StreamDay.stream_event_id.in_(eids))
            .order_by(StreamDay.stream_event_id, StreamDay.day_index)
        )
        for row in dr.scalars().all():
            days_by_event[row.stream_event_id].append(row)
    pairs_by = await _load_assignment_pairs(session, eids)
    lock_ids = {e.locked_by_user_id for e in events if e.locked_by_user_id}
    users_map = await _users_by_ids(session, lock_ids)
    items: list[StreamEventListOut] = []
    for ev in events:
        lock_u = users_map.get(ev.locked_by_user_id) if ev.locked_by_user_id else None
        locked_by_display_name = user_display_name(lock_u) if lock_u else None
        summary = _assignment_summary_from_pairs(pairs_by.get(ev.id, []))
        pairs = pairs_by.get(ev.id, [])
        assigned_days = {d for d, _ in pairs}
        has_slot = True
        if viewer is not None:
            if viewer.role == UserRole.SUPERADMIN:
                has_slot = True
            elif not assigned_days:
                has_slot = True
            elif any(u.id == viewer.id for _, u in pairs):
                has_slot = True
            elif len(assigned_days) < ev.duration_days:
                has_slot = True
            else:
                has_slot = False
        day_links = [
            StreamDayLinkOut(day_index=d.day_index, stream_url=d.stream_url or "")
            for d in days_by_event.get(ev.id, [])
        ]
        items.append(
            StreamEventListOut(
                id=ev.id,
                title=ev.title,
                start_date=ev.start_date,
                duration_days=ev.duration_days,
                locked_by_user_id=ev.locked_by_user_id,
                locked_by_display_name=locked_by_display_name,
                assignment_summary=summary,
                has_slot_for_me=has_slot,
                has_active_broadcast=ev.id in active_ids,
                has_ended_broadcast=ev.id in ended_ids,
                ended_day_indices=ended_days_by_event.get(ev.id, []),
                created_at=ev.created_at,
                day_stream_links=day_links,
            )
        )
    return items


async def get_stream_event_detail(session: AsyncSession, stream_id: UUID) -> StreamEventDetailOut:
    ev = await _get_event(session, stream_id)
    ev.days.sort(key=lambda d: d.day_index)
    locked_by_display_name = await _locked_by_display_name(session, ev.locked_by_user_id)
    day_assignments = await _day_assignments_out(session, stream_id)
    active_broadcasts = [
        BroadcastSessionOut(
            id=b.id,
            stream_event_id=b.stream_event_id,
            day_index=b.day_index,
            operator_id=b.operator_id,
            started_at=b.started_at,
            ended_at=b.ended_at,
            is_active=True,
        )
        for b in ev.broadcast_sessions
        if b.ended_at is None
    ]
    ended_raw = [b for b in ev.broadcast_sessions if b.ended_at is not None]
    ended_ids = [b.id for b in ended_raw]
    mention_counts: dict[UUID, int] = {}
    if ended_ids:
        cr = await session.execute(
            select(SponsorMention.broadcast_session_id, func.count())
            .where(SponsorMention.broadcast_session_id.in_(ended_ids))
            .group_by(SponsorMention.broadcast_session_id)
        )
        mention_counts = {row[0]: int(row[1]) for row in cr.all()}
    ended_sorted = sorted(
        ended_raw,
        key=lambda b: (
            b.day_index,
            -(b.ended_at.timestamp() if b.ended_at else 0.0),
        ),
    )
    ended_broadcasts = [
        BroadcastSessionOut(
            id=b.id,
            stream_event_id=b.stream_event_id,
            day_index=b.day_index,
            operator_id=b.operator_id,
            started_at=b.started_at,
            ended_at=b.ended_at,
            is_active=False,
            mentions_count=mention_counts.get(b.id, 0),
        )
        for b in ended_sorted
    ]
    restart_blocked = await _broadcast_restart_blocked_days(
        session, stream_id=stream_id, duration_days=ev.duration_days
    )
    return StreamEventDetailOut(
        id=ev.id,
        title=ev.title,
        start_date=ev.start_date,
        duration_days=ev.duration_days,
        locked_by_user_id=ev.locked_by_user_id,
        locked_by_display_name=locked_by_display_name,
        day_assignments=day_assignments,
        days=[StreamDayOut.model_validate(d) for d in ev.days],
        active_broadcasts=active_broadcasts,
        ended_broadcasts=ended_broadcasts,
        broadcast_restart_blocked_days=restart_blocked,
        content_url=ev.content_url,
        logos=_logos_for_stream(ev),
        created_at=ev.created_at,
        updated_at=ev.updated_at,
    )


def _server_url_from_template_days(days_json: list | None) -> str:
    if not days_json:
        return ""
    for item in days_json:
        if not isinstance(item, dict):
            continue
        u = (item.get("server_url") or "").strip()
        if u:
            return u
    return ""


async def _sync_days(
    session: AsyncSession,
    stream_event_id: UUID,
    duration_days: int,
    days_input: list[StreamDayIn] | None,
) -> None:
    result = await session.execute(select(StreamDay).where(StreamDay.stream_event_id == stream_event_id))
    existing = {d.day_index: d for d in result.scalars().all()}
    for idx in range(1, duration_days + 1):
        if idx not in existing:
            session.add(
                StreamDay(
                    stream_event_id=stream_event_id,
                    day_index=idx,
                    stream_url="",
                    server_url="",
                    stream_key="",
                )
            )
    to_remove = [d for d in existing.values() if d.day_index > duration_days]
    for d in to_remove:
        sess_count = await session.execute(
            select(func.count())
            .select_from(BroadcastSession)
            .where(
                and_(
                    BroadcastSession.stream_event_id == stream_event_id,
                    BroadcastSession.day_index == d.day_index,
                )
            )
        )
        if sess_count.scalar_one() > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Нельзя уменьшить длительность: есть эфир для дня {d.day_index}",
            )
        await session.delete(d)
    if days_input:
        by_idx = {x.day_index: x for x in days_input}
        result2 = await session.execute(select(StreamDay).where(StreamDay.stream_event_id == stream_event_id))
        for row in result2.scalars().all():
            inc = by_idx.get(row.day_index)
            if inc:
                row.stream_url = inc.stream_url
                row.server_url = inc.server_url
                row.stream_key = inc.stream_key


async def create_stream_event(session: AsyncSession, *, actor: User, data: StreamEventCreate) -> StreamEventDetailOut:
    days_for_sync = data.days
    if data.template_id is not None:
        res_tpl = await session.execute(select(StreamEventTemplate).where(StreamEventTemplate.id == data.template_id))
        tpl = res_tpl.scalar_one_or_none()
        if tpl is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Шаблон не найден")
        server_url = _server_url_from_template_days(tpl.days_json)
        days_for_sync = [
            StreamDayIn(day_index=i, stream_url="", server_url=server_url, stream_key="")
            for i in range(1, data.duration_days + 1)
        ]
    ev = StreamEvent(
        title=data.title,
        start_date=data.start_date,
        duration_days=data.duration_days,
        created_by_id=actor.id,
    )
    session.add(ev)
    await session.flush()
    await _sync_days(session, ev.id, data.duration_days, days_for_sync)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_CREATE,
        entity_type="stream_event",
        entity_id=str(ev.id),
        payload_before=None,
        payload_after={"title": ev.title, "start_date": str(ev.start_date), "duration_days": ev.duration_days},
    )
    await session.commit()
    return await get_stream_event_detail(session, ev.id)


async def update_stream_event(session: AsyncSession, *, actor: User, stream_id: UUID, data: StreamEventUpdate) -> StreamEventDetailOut:
    ev = await _get_event(session, stream_id)
    before = {
        "title": ev.title,
        "start_date": str(ev.start_date),
        "duration_days": ev.duration_days,
        "content_url": ev.content_url,
    }
    if data.title is not None:
        ev.title = data.title
    if data.start_date is not None:
        ev.start_date = data.start_date
    new_duration = data.duration_days if data.duration_days is not None else ev.duration_days
    if data.duration_days is not None:
        ev.duration_days = data.duration_days
    if "content_url" in data.model_fields_set:
        ev.content_url = str(data.content_url) if data.content_url is not None else None
    await _sync_days(session, ev.id, new_duration, data.days)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_UPDATE,
        entity_type="stream_event",
        entity_id=str(ev.id),
        payload_before=before,
        payload_after={
            "title": ev.title,
            "start_date": str(ev.start_date),
            "duration_days": ev.duration_days,
            "content_url": ev.content_url,
        },
    )
    await session.commit()
    return await get_stream_event_detail(session, stream_id)


async def delete_stream_event(session: AsyncSession, *, actor: User, stream_id: UUID) -> None:
    ev = await _get_event(session, stream_id)
    active_ids = await _active_broadcast_ids(session)
    if stream_id in active_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить мероприятие с активным эфиром. Сначала остановите эфир.",
        )
    before = {"title": ev.title}
    await session.delete(ev)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_DELETE,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before=before,
        payload_after=None,
    )
    await session.commit()


async def lock_stream(
    session: AsyncSession,
    *,
    actor: User,
    stream_id: UUID,
    assign_user_id: UUID | None,
    day_indices: list[int] | None,
) -> StreamEventDetailOut:
    ev = await _get_event(session, stream_id)
    if actor.role == UserRole.STREAM_MANAGER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

    target_operator_id: UUID
    if actor.role == UserRole.SUPERADMIN:
        if assign_user_id is not None:
            ures = await session.execute(select(User).where(User.id == assign_user_id))
            target = ures.scalar_one_or_none()
            if not target or target.role != UserRole.OPERATOR:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нужен оператор")
            target_operator_id = assign_user_id
        else:
            target_operator_id = actor.id
    else:
        target_operator_id = actor.id

    if actor.role == UserRole.SUPERADMIN and assign_user_id is None:
        if target_operator_id == actor.id and await _stream_has_assignments_to_other_than(
            session, stream_event_id=ev.id, user_id=actor.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Дни назначены операторам — «взять в работу» с пульта суперадмином недоступен",
            )

    want_days: list[int]
    if day_indices is None or len(day_indices) == 0:
        want_days = list(range(1, ev.duration_days + 1))
    else:
        want_days = sorted(set(day_indices))
        for d in want_days:
            if d < 1 or d > ev.duration_days:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"День {d} вне длительности мероприятия")

    before_lock = ev.locked_by_user_id
    for d in want_days:
        cur = await session.execute(
            select(StreamDayAssignment).where(
                StreamDayAssignment.stream_event_id == ev.id,
                StreamDayAssignment.day_index == d,
            )
        )
        row = cur.scalar_one_or_none()
        if row is not None and row.operator_id != target_operator_id:
            ures = await session.execute(select(User).where(User.id == row.operator_id))
            other = ures.scalar_one_or_none()
            who = user_display_name(other) if other else "оператор"
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"День {d} уже назначен: {who}",
            )

    for d in want_days:
        cur = await session.execute(
            select(StreamDayAssignment).where(
                StreamDayAssignment.stream_event_id == ev.id,
                StreamDayAssignment.day_index == d,
            )
        )
        row = cur.scalar_one_or_none()
        if row is None:
            session.add(
                StreamDayAssignment(
                    stream_event_id=ev.id,
                    day_index=d,
                    operator_id=target_operator_id,
                )
            )
        else:
            row.operator_id = target_operator_id

    await _sync_legacy_locked_by(session, ev)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_LOCK,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before={"locked_by": str(before_lock) if before_lock else None},
        payload_after={
            "locked_by": str(ev.locked_by_user_id) if ev.locked_by_user_id else None,
            "days": want_days,
            "operator": str(target_operator_id),
        },
    )
    await session.commit()
    return await get_stream_event_detail(session, stream_id)


async def unlock_stream(session: AsyncSession, *, actor: User, stream_id: UUID) -> StreamEventDetailOut:
    ev = await _get_event(session, stream_id)
    if actor.role == UserRole.STREAM_MANAGER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    prev = ev.locked_by_user_id
    if actor.role == UserRole.SUPERADMIN:
        if await _stream_has_assignments_to_other_than(session, stream_event_id=ev.id, user_id=actor.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Дни назначены операторам — снять назначения может сам оператор",
            )
        await session.execute(delete(StreamDayAssignment).where(StreamDayAssignment.stream_event_id == ev.id))
    else:
        cnt_r = await session.execute(
            select(func.count())
            .select_from(StreamDayAssignment)
            .where(
                StreamDayAssignment.stream_event_id == ev.id,
                StreamDayAssignment.operator_id == actor.id,
            )
        )
        my_days = int(cnt_r.scalar_one() or 0)
        if my_days == 0 and ev.locked_by_user_id != actor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас нет назначенных дней на этом мероприятии",
            )
        await session.execute(
            delete(StreamDayAssignment).where(
                StreamDayAssignment.stream_event_id == ev.id,
                StreamDayAssignment.operator_id == actor.id,
            )
        )
    await _sync_legacy_locked_by(session, ev)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_UNLOCK,
        entity_type="stream_event",
        entity_id=str(stream_id),
        payload_before={"locked_by": str(prev) if prev else None},
        payload_after={"locked_by": str(ev.locked_by_user_id) if ev.locked_by_user_id else None},
    )
    await session.commit()
    return await get_stream_event_detail(session, stream_id)


def _can_control_broadcast(actor: User, ev: StreamEvent, session_operator_id: UUID) -> bool:
    if actor.role == UserRole.SUPERADMIN:
        return True
    if actor.role != UserRole.OPERATOR:
        return False
    return session_operator_id == actor.id


def _can_realign_broadcast_start(actor: User, ev: StreamEvent, session_operator_id: UUID) -> bool:
    if actor.role == UserRole.SUPERADMIN:
        return True
    if actor.role == UserRole.STREAM_MANAGER:
        return True
    if actor.role == UserRole.OPERATOR:
        return session_operator_id == actor.id
    return False


def _can_realign_ended_broadcast(actor: User, bs: BroadcastSession) -> bool:
    """Завершённый эфир: менеджер, суперадмин или оператор, который вёл эту сессию."""
    if actor.role == UserRole.SUPERADMIN:
        return True
    if actor.role == UserRole.STREAM_MANAGER:
        return True
    if actor.role == UserRole.OPERATOR:
        return bs.operator_id == actor.id
    return False


def _can_edit_mentions_on_broadcast_session(actor: User, ev: StreamEvent, bs: BroadcastSession) -> bool:
    if bs.ended_at is None:
        return _can_control_broadcast(actor, ev, bs.operator_id)
    return _can_realign_ended_broadcast(actor, bs)


def _datetime_to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=MOSCOW_TZ)
    return dt.astimezone(timezone.utc)


async def start_broadcast(session: AsyncSession, *, actor: User, stream_id: UUID, day_index: int) -> BroadcastSessionOut:
    if day_index < 1 or day_index > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный день")
    ev = await _get_event(session, stream_id)
    if day_index > ev.duration_days:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="День вне длительности мероприятия")
    if await _day_blocked_for_new_broadcast(
        session, stream_id=stream_id, day_index=day_index, duration_days=ev.duration_days
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Этот день уже был в эфире более часа с таймкодами — повторный старт недоступен",
        )
    day_op = await _assignment_operator_for_day(session, stream_id, day_index)
    if day_op is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Сначала назначьте день на оператора: «Взять в работу» (весь турнир или выбранные дни)",
        )
    if actor.role == UserRole.OPERATOR:
        if day_op != actor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет назначения на этот день — возьмите этот день в работу",
            )
    elif actor.role != UserRole.SUPERADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    active = await session.execute(
        select(BroadcastSession).where(
            and_(
                BroadcastSession.stream_event_id == stream_id,
                BroadcastSession.day_index == day_index,
                BroadcastSession.ended_at.is_(None),
            )
        )
    )
    if active.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Эфир для этого дня уже идёт")
    started = utc_now()
    if actor.role == UserRole.OPERATOR:
        operator_id = actor.id
    else:
        operator_id = day_op
    bs = BroadcastSession(
        stream_event_id=stream_id,
        day_index=day_index,
        operator_id=operator_id,
        started_at=started,
    )
    session.add(bs)
    await session.flush()
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.BROADCAST_START,
        entity_type="broadcast_session",
        entity_id=str(bs.id),
        payload_after={"stream_event_id": str(stream_id), "day_index": day_index, "started_at": started.isoformat()},
        payload_before=None,
    )
    await create_for_users_with_roles(
        session,
        roles=[UserRole.STREAM_MANAGER, UserRole.SUPERADMIN],
        title="Начало эфира",
        body=f"{ev.title} — день {day_index}",
        kind="broadcast_start",
    )
    await session.commit()
    await session.refresh(bs)
    return BroadcastSessionOut(
        id=bs.id,
        stream_event_id=bs.stream_event_id,
        day_index=bs.day_index,
        operator_id=bs.operator_id,
        started_at=bs.started_at,
        ended_at=bs.ended_at,
        is_active=True,
    )


async def stop_broadcast(session: AsyncSession, *, actor: User, stream_id: UUID, day_index: int) -> None:
    ev = await _get_event(session, stream_id)
    result = await session.execute(
        select(BroadcastSession).where(
            and_(
                BroadcastSession.stream_event_id == stream_id,
                BroadcastSession.day_index == day_index,
                BroadcastSession.ended_at.is_(None),
            )
        )
    )
    bs = result.scalar_one_or_none()
    if not bs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Активный эфир не найден")
    if not _can_control_broadcast(actor, ev, bs.operator_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    bs.ended_at = utc_now()
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.BROADCAST_STOP,
        entity_type="broadcast_session",
        entity_id=str(bs.id),
        payload_before={"ended_at": None},
        payload_after={"ended_at": bs.ended_at.isoformat()},
    )
    await session.commit()


async def realign_broadcast_actual_start(
    session: AsyncSession,
    *,
    actor: User,
    stream_id: UUID,
    day_index: int,
    actual_started_at: datetime,
) -> BroadcastSessionOut:
    """Сдвигает started_at на фактическое время и добавляет дельту ко всем таймкодам упоминаний."""
    if day_index < 1 or day_index > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный день")
    ev = await _get_event(session, stream_id)
    if day_index > ev.duration_days:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="День вне длительности мероприятия")

    result = await session.execute(
        select(BroadcastSession)
        .options(selectinload(BroadcastSession.mentions).selectinload(SponsorMention.adjustments))
        .where(
            and_(
                BroadcastSession.stream_event_id == stream_id,
                BroadcastSession.day_index == day_index,
                BroadcastSession.ended_at.is_(None),
            )
        )
    )
    bs = result.scalar_one_or_none()
    if bs is None:
        result_ended = await session.execute(
            select(BroadcastSession)
            .options(selectinload(BroadcastSession.mentions).selectinload(SponsorMention.adjustments))
            .where(
                and_(
                    BroadcastSession.stream_event_id == stream_id,
                    BroadcastSession.day_index == day_index,
                    BroadcastSession.ended_at.isnot(None),
                )
            )
            .order_by(BroadcastSession.ended_at.desc())
            .limit(1)
        )
        bs = result_ended.scalar_one_or_none()
    if not bs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Эфир для этого дня не найден",
        )

    if bs.ended_at is not None:
        if not _can_realign_ended_broadcast(actor, bs):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для правки времени начала этого завершённого эфира",
            )
    elif not _can_realign_broadcast_start(actor, ev, bs.operator_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

    new_started_utc = _datetime_to_utc(actual_started_at)
    old_started = bs.started_at
    if old_started.tzinfo is None:
        old_started = old_started.replace(tzinfo=timezone.utc)
    else:
        old_started = old_started.astimezone(timezone.utc)

    delta_sec = int((old_started - new_started_utc).total_seconds())

    if new_started_utc > utc_now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Время начала не может быть в будущем",
        )

    if delta_sec == 0:
        return BroadcastSessionOut(
            id=bs.id,
            stream_event_id=bs.stream_event_id,
            day_index=bs.day_index,
            operator_id=bs.operator_id,
            started_at=bs.started_at,
            ended_at=bs.ended_at,
            is_active=bs.ended_at is None,
        )

    mentions = list(bs.mentions)
    latest_allowed_start_utc: datetime | None = None
    for m in mentions:
        # new_start <= old_start + offset_sec, иначе offset станет отрицательным
        c1 = old_started + timedelta(seconds=m.original_offset_sec)
        c2 = old_started + timedelta(seconds=m.adjusted_offset_sec)
        cand = c1 if c1 <= c2 else c2
        if latest_allowed_start_utc is None or cand < latest_allowed_start_utc:
            latest_allowed_start_utc = cand
    for m in mentions:
        for adj in m.adjustments:
            c1 = old_started + timedelta(seconds=adj.previous_adjusted_sec)
            c2 = old_started + timedelta(seconds=adj.new_adjusted_sec)
            cand = c1 if c1 <= c2 else c2
            if latest_allowed_start_utc is None or cand < latest_allowed_start_utc:
                latest_allowed_start_utc = cand
    if latest_allowed_start_utc is not None and new_started_utc > latest_allowed_start_utc:
        latest_allowed_msk = format_moscow_datetime(latest_allowed_start_utc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Указанное время делает таймкоды отрицательными. "
                f"Можно поставить старт не позже {latest_allowed_msk}."
            ),
        )

    for m in mentions:
        m.original_offset_sec += delta_sec
        m.adjusted_offset_sec += delta_sec
        for adj in m.adjustments:
            adj.previous_adjusted_sec += delta_sec
            adj.new_adjusted_sec += delta_sec

    bs.started_at = new_started_utc

    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.BROADCAST_ACTUAL_START,
        entity_type="broadcast_session",
        entity_id=str(bs.id),
        payload_before={"started_at": old_started.isoformat()},
        payload_after={
            "started_at": new_started_utc.isoformat(),
            "delta_sec": delta_sec,
            "day_index": day_index,
        },
    )
    await session.commit()
    await session.refresh(bs)
    return BroadcastSessionOut(
        id=bs.id,
        stream_event_id=bs.stream_event_id,
        day_index=bs.day_index,
        operator_id=bs.operator_id,
        started_at=bs.started_at,
        ended_at=bs.ended_at,
        is_active=bs.ended_at is None,
    )


async def add_sponsor_mention(session: AsyncSession, *, actor: User, broadcast_session_id: UUID) -> SponsorMentionOut:
    result = await session.execute(
        select(BroadcastSession)
        .options(selectinload(BroadcastSession.stream_event), selectinload(BroadcastSession.mentions))
        .where(BroadcastSession.id == broadcast_session_id)
    )
    bs = result.scalar_one_or_none()
    if not bs or bs.ended_at is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Сессия эфира неактивна")
    ev = bs.stream_event
    if not _can_control_broadcast(actor, ev, bs.operator_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    start = bs.started_at if bs.started_at.tzinfo else bs.started_at.replace(tzinfo=timezone.utc)
    now = utc_now()
    offset = int((now - start).total_seconds())
    if offset < 0:
        offset = 0
    mention = SponsorMention(
        broadcast_session_id=bs.id,
        original_offset_sec=offset,
        adjusted_offset_sec=offset,
    )
    session.add(mention)
    await session.flush()
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.MENTION_CREATE,
        entity_type="sponsor_mention",
        entity_id=str(mention.id),
        payload_before=None,
        payload_after={"offset_sec": offset, "broadcast_session_id": str(bs.id)},
    )
    await session.commit()
    await session.refresh(mention)
    mres = await session.execute(
        select(SponsorMention)
        .options(
            selectinload(SponsorMention.adjustments),
            selectinload(SponsorMention.broadcast_session),
        )
        .where(SponsorMention.id == mention.id)
    )
    mention = mres.scalar_one()
    return _mention_to_out(mention)


async def update_sponsor_mention(
    session: AsyncSession,
    *,
    actor: User,
    mention_id: UUID,
    new_adjusted_sec: int,
) -> SponsorMentionOut:
    result = await session.execute(
        select(SponsorMention)
        .options(
            selectinload(SponsorMention.adjustments),
            selectinload(SponsorMention.broadcast_session).selectinload(BroadcastSession.stream_event),
        )
        .where(SponsorMention.id == mention_id)
    )
    mention = result.scalar_one_or_none()
    if not mention:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Упоминание не найдено")
    bs = mention.broadcast_session
    ev = bs.stream_event
    if not _can_edit_mentions_on_broadcast_session(actor, ev, bs):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")
    prev = mention.adjusted_offset_sec
    if prev == new_adjusted_sec:
        return _mention_to_out(mention)
    adj = MentionAdjustment(
        mention_id=mention.id,
        editor_user_id=actor.id,
        previous_adjusted_sec=prev,
        new_adjusted_sec=new_adjusted_sec,
    )
    session.add(adj)
    mention.adjusted_offset_sec = new_adjusted_sec
    await session.flush()
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.MENTION_UPDATE,
        entity_type="sponsor_mention",
        entity_id=str(mention.id),
        payload_before={"adjusted_offset_sec": prev},
        payload_after={"adjusted_offset_sec": new_adjusted_sec},
    )
    await session.commit()
    await session.refresh(mention)
    mres = await session.execute(
        select(SponsorMention)
        .options(
            selectinload(SponsorMention.adjustments),
            selectinload(SponsorMention.broadcast_session),
        )
        .where(SponsorMention.id == mention_id)
    )
    mention = mres.scalar_one()
    return _mention_to_out(mention)


async def delete_sponsor_mention(
    session: AsyncSession,
    *,
    actor: User,
    mention_id: UUID,
) -> UUID:
    result = await session.execute(
        select(SponsorMention)
        .options(selectinload(SponsorMention.broadcast_session).selectinload(BroadcastSession.stream_event))
        .where(SponsorMention.id == mention_id)
    )
    mention = result.scalar_one_or_none()
    if not mention:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Упоминание не найдено")
    bs = mention.broadcast_session
    ev = bs.stream_event
    if not _can_edit_mentions_on_broadcast_session(actor, ev, bs):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

    stream_event_id = bs.stream_event_id
    mention_id_str = str(mention.id)
    before = {
        "broadcast_session_id": str(mention.broadcast_session_id),
        "original_offset_sec": mention.original_offset_sec,
        "adjusted_offset_sec": mention.adjusted_offset_sec,
    }
    await session.delete(mention)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.MENTION_UPDATE,
        entity_type="sponsor_mention",
        entity_id=mention_id_str,
        payload_before=before,
        payload_after=None,
    )
    await session.commit()
    return stream_event_id


async def list_mentions_for_event_day(
    session: AsyncSession,
    *,
    stream_id: UUID,
    day_index: int,
) -> list[SponsorMentionOut]:
    ev = await _get_event(session, stream_id)
    if day_index > ev.duration_days:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный день")
    result = await session.execute(
        select(SponsorMention)
        .join(BroadcastSession)
        .options(
            selectinload(SponsorMention.adjustments),
            selectinload(SponsorMention.broadcast_session),
        )
        .where(
            and_(
                BroadcastSession.stream_event_id == stream_id,
                BroadcastSession.day_index == day_index,
            )
        )
        .order_by(SponsorMention.created_at.asc())
    )
    return [_mention_to_out(m) for m in result.scalars().all()]

```


---

## Исходный код: `backend/app/services/template_service.py`

> 132 строк, 4,331 байт

```py
import uuid
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import AuditActionType
from app.models.stream import StreamEventTemplate
from app.models.user import User
from app.schemas.stream import StreamEventCreate
from app.schemas.templates import StreamEventTemplateCreate, TemplateFromEventBody
from app.services.audit_service import write_audit
from app.services.stream_service import create_stream_event, get_stream_event_detail


async def list_templates(session: AsyncSession) -> list[StreamEventTemplate]:
    result = await session.execute(select(StreamEventTemplate).order_by(StreamEventTemplate.created_at.desc()))
    return list(result.scalars().all())


async def create_template(
    session: AsyncSession, *, actor: User, body: StreamEventTemplateCreate
) -> StreamEventTemplate:
    days_data: list[dict] = []
    if body.days:
        for d in body.days:
            days_data.append(
                {"day_index": d.day_index, "stream_url": d.stream_url, "server_url": d.server_url, "stream_key": d.stream_key}
            )
    else:
        for i in range(1, body.duration_days + 1):
            days_data.append({"day_index": i, "stream_url": "", "server_url": "", "stream_key": ""})
    t = StreamEventTemplate(
        name=body.name,
        title=body.title,
        duration_days=body.duration_days,
        days_json=days_data,
        created_by_id=actor.id,
    )
    session.add(t)
    await session.flush()
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_CREATE,
        entity_type="stream_event_template",
        entity_id=str(t.id),
        payload_before=None,
        payload_after={"name": t.name},
    )
    await session.commit()
    await session.refresh(t)
    return t


async def template_from_event(
    session: AsyncSession, *, actor: User, stream_id: uuid.UUID, body: TemplateFromEventBody
) -> StreamEventTemplate:
    detail = await get_stream_event_detail(session, stream_id)
    days_data = [
        {
            "day_index": d.day_index,
            "stream_url": d.stream_url,
            "server_url": d.server_url,
            "stream_key": d.stream_key,
        }
        for d in detail.days
    ]
    t = StreamEventTemplate(
        name=body.name,
        title=detail.title,
        duration_days=detail.duration_days,
        days_json=days_data,
        created_by_id=actor.id,
    )
    session.add(t)
    await session.flush()
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_CREATE,
        entity_type="stream_event_template",
        entity_id=str(t.id),
        payload_before=None,
        payload_after={"name": t.name, "from_event": str(stream_id)},
    )
    await session.commit()
    await session.refresh(t)
    return t


async def delete_template(session: AsyncSession, *, actor: User, template_id: uuid.UUID) -> None:
    result = await session.execute(select(StreamEventTemplate).where(StreamEventTemplate.id == template_id))
    t = result.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Шаблон не найден")
    await session.delete(t)
    await write_audit(
        session,
        user_id=actor.id,
        action_type=AuditActionType.STREAM_DELETE,
        entity_type="stream_event_template",
        entity_id=str(template_id),
        payload_before={"name": t.name},
        payload_after=None,
    )
    await session.commit()


async def instantiate_template(
    session: AsyncSession,
    *,
    actor: User,
    template_id: uuid.UUID,
    title: str,
    start_date: date,
    duration_days: int,
):
    result = await session.execute(select(StreamEventTemplate).where(StreamEventTemplate.id == template_id))
    t = result.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Шаблон не найден")
    data = StreamEventCreate(
        title=title,
        start_date=start_date,
        duration_days=duration_days,
        template_id=template_id,
        days=None,
    )
    return await create_stream_event(session, actor=actor, data=data)

```


---

## Исходный код: `backend/app/services/user_service.py`

> 207 строк, 7,058 байт

```py
import logging
import secrets
from typing import NamedTuple
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import hash_password
from app.models.enums import AuditActionType, UserRole
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.audit_service import write_audit
from app.services.welcome_email_service import send_welcome_email
from app.utils.phone_ru import normalize_ru_mobile_phone

log = logging.getLogger(__name__)


class WelcomeEmailPayload(NamedTuple):
    to_email: str
    first_name: str
    role: UserRole
    plain_password: str


class CreateUserOutcome(NamedTuple):
    user: User
    welcome_email_payload: WelcomeEmailPayload | None
    welcome_email_skipped_reason: str | None


async def list_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).order_by(User.created_at.desc()))
    return list(result.scalars().all())


async def get_user(session: AsyncSession, user_id: UUID) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user


async def create_user(session: AsyncSession, *, actor_id: UUID, data: UserCreate) -> CreateUserOutcome:
    exists = await session.execute(select(User.id).where(User.email == data.email))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email уже занят")

    plain_password = secrets.token_urlsafe(14)

    user = User(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        password_hash=hash_password(plain_password),
        role=data.role,
        is_active=data.is_active,
        suggest_password_change=True,
        onboarding_completed=False,
    )
    session.add(user)
    await session.flush()
    await write_audit(
        session,
        user_id=actor_id,
        action_type=AuditActionType.USER_CREATE,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=None,
        payload_after={
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role.value,
            "password_auto_generated": True,
        },
    )
    await session.commit()
    await session.refresh(user)

    settings = get_settings()
    if not settings.smtp_host.strip():
        return CreateUserOutcome(
            user,
            None,
            "SMTP не настроен (smtp_host пустой в backend/.env) — письма не отправляются",
        )

    payload = WelcomeEmailPayload(
        to_email=user.email,
        first_name=user.first_name,
        role=user.role,
        plain_password=plain_password,
    )
    return CreateUserOutcome(user, payload, None)


async def send_welcome_email_task(payload: WelcomeEmailPayload) -> None:
    """Фоновая отправка после HTTP-ответа (не блокирует создание пользователя)."""
    try:
        await send_welcome_email(
            to_email=payload.to_email,
            first_name=payload.first_name,
            role=payload.role,
            plain_password=payload.plain_password,
        )
        log.info("Welcome email sent to %s", payload.to_email)
    except Exception:
        log.exception("Welcome email failed for %s", payload.to_email)


async def update_user(session: AsyncSession, *, actor_id: UUID, user_id: UUID, data: UserUpdate) -> User:
    user = await get_user(session, user_id)
    before = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "telegram": user.telegram,
        "role": user.role.value,
        "is_active": user.is_active,
    }
    if data.email is not None and data.email != user.email:
        exists = await session.execute(select(User.id).where(User.email == data.email))
        if exists.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email уже занят")
        user.email = data.email
    if data.first_name is not None:
        user.first_name = data.first_name
    if data.last_name is not None:
        user.last_name = data.last_name
    if data.phone is not None:
        trimmed = (data.phone or "").strip()
        if not trimmed:
            user.phone = None
        else:
            try:
                user.phone = normalize_ru_mobile_phone(trimmed)
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e) or "Некорректный номер телефона",
                ) from e
    if data.telegram is not None:
        user.telegram = data.telegram or None
    if data.password is not None:
        if len(data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароль не короче 8 символов",
            )
        user.password_hash = hash_password(data.password)
        user.suggest_password_change = False
    if data.role is not None:
        user.role = data.role
    if data.is_active is not None:
        user.is_active = data.is_active
    await session.flush()
    await write_audit(
        session,
        user_id=actor_id,
        action_type=AuditActionType.USER_UPDATE,
        entity_type="user",
        entity_id=str(user.id),
        payload_before=before,
        payload_after={
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "telegram": user.telegram,
            "role": user.role.value,
            "is_active": user.is_active,
        },
    )
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, *, actor_id: UUID, user_id: UUID) -> None:
    user = await get_user(session, user_id)
    if user.id == actor_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Нельзя удалить себя")
    before = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role.value,
    }
    await session.delete(user)
    await session.flush()
    await write_audit(
        session,
        user_id=actor_id,
        action_type=AuditActionType.USER_DELETE,
        entity_type="user",
        entity_id=str(user_id),
        payload_before=before,
        payload_after=None,
    )
    await session.commit()

```


---

## Исходный код: `backend/app/services/welcome_email_service.py`

> 134 строк, 5,699 байт

```py
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

```


---

## Исходный код: `backend/app/utils/client_ip.py`

> 18 строк, 555 байт

```py
"""Клиентский IP за reverse-proxy (nginx): X-Forwarded-For, затем X-Real-IP, затем peer."""

from fastapi import Request


def client_ip_from_request(request: Request) -> str | None:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        first = xff.split(",")[0].strip()
        if first:
            return first[:45]
    xri = request.headers.get("x-real-ip")
    if xri:
        return xri.strip()[:45]
    if request.client:
        return request.client.host[:45] if request.client.host else None
    return None

```


---

## Исходный код: `backend/app/utils/display_name.py`

> 7 строк, 165 байт

```py
from app.models.user import User


def user_display_name(user: User) -> str:
    s = f"{user.last_name} {user.first_name}".strip()
    return s if s else user.email

```


---

## Исходный код: `backend/app/utils/phone_ru.py`

> 34 строк, 1,483 байт

```py
"""Нормализация российских мобильных номеров в вид +7 (XXX) XXX XX XX."""


def normalize_ru_mobile_phone(raw: str) -> str:
    """
    Принимает ввод в любом распространённом виде: 79060943936, 89060943936, +7 906 094-39-36 и т.д.
    Возвращает канонический формат. Только мобильные РФ (вторая цифра 9).
    """
    s = (raw or "").strip()
    if not s:
        raise ValueError("Пустой номер")
    digits = "".join(c for c in s if c.isdigit())
    if len(digits) == 11 and digits[0] == "8":
        digits = "7" + digits[1:]
    elif len(digits) == 10 and digits[0] == "9":
        digits = "7" + digits
    if len(digits) != 11 or digits[0] != "7":
        raise ValueError("Нужен российский мобильный: 10 цифр с 9 или 11 с 7/8")
    if digits[1] != "9":
        raise ValueError("Поддерживаются только мобильные номера (9XXXXXXXXX)")
    rest = digits[1:]
    a, b, c, d = rest[:3], rest[3:6], rest[6:8], rest[8:10]
    return f"+7 ({a}) {b} {c} {d}"


def normalize_ru_mobile_phone_or_empty(raw: str | None) -> str | None:
    """Пустая строка → None. Иначе нормализация или ValueError."""
    if raw is None:
        return None
    s = raw.strip()
    if not s:
        return None
    return normalize_ru_mobile_phone(s)

```


---

## Исходный код: `backend/app/utils/timecode.py`

> 6 строк, 171 байт

```py
def seconds_to_hhmmss(total_sec: int) -> str:
    sec = max(0, int(total_sec))
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

```


---

## Исходный код: `backend/app/utils/webhook.py`

> 20 строк, 533 байт

```py
import logging

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)


async def post_external_webhook(event_type: str, payload: dict) -> None:
    settings = get_settings()
    url = (settings.external_webhook_url or "").strip()
    if not url:
        return
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json={"type": event_type, "payload": payload}, timeout=8.0)
    except Exception as exc:
        logger.warning("webhook_failed %s", exc)

```


---

## Исходный код: `backend/app/websocket/hub.py`

> 56 строк, 2,079 байт

```py
import uuid
from typing import Any

from fastapi import WebSocket
from starlette.websockets import WebSocketState


class StreamEventHub:
    def __init__(self, max_subscribers_per_room: int = 80) -> None:
        self._rooms: dict[uuid.UUID, list[WebSocket]] = {}
        self._max_subscribers_per_room = max_subscribers_per_room

    async def connect(self, stream_event_id: uuid.UUID, websocket: WebSocket) -> bool:
        room = self._rooms.setdefault(stream_event_id, [])
        if len(room) >= self._max_subscribers_per_room:
            await websocket.close(code=4429)
            return False
        room.append(websocket)
        await self._publish_presence(stream_event_id)
        return True

    def disconnect(self, stream_event_id: uuid.UUID, websocket: WebSocket) -> None:
        room = self._rooms.get(stream_event_id)
        if not room:
            return
        if websocket in room:
            room.remove(websocket)
        if not room:
            del self._rooms[stream_event_id]

    async def notify_presence(self, stream_event_id: uuid.UUID) -> None:
        await self._publish_presence(stream_event_id)

    async def _publish_presence(self, stream_event_id: uuid.UUID) -> None:
        room = list(self._rooms.get(stream_event_id, []))
        n = len(room)
        msg: dict[str, Any] = {"type": "presence", "payload": {"viewers": n}}
        for ws in room:
            if ws.client_state != WebSocketState.CONNECTED:
                continue
            try:
                await ws.send_json(msg)
            except Exception:
                self.disconnect(stream_event_id, ws)

    async def publish(self, stream_event_id: uuid.UUID, message: dict[str, Any]) -> None:
        room = list(self._rooms.get(stream_event_id, []))
        for ws in room:
            if ws.client_state != WebSocketState.CONNECTED:
                self.disconnect(stream_event_id, ws)
                continue
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(stream_event_id, ws)

```


---

## Исходный код: `backend/pytest.ini`

> 4 строк, 47 байт

```ini
[pytest]
asyncio_mode = auto
testpaths = tests

```


---

## Исходный код: `backend/requirements.txt`

> 23 строк, 448 байт

```txt
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlalchemy[asyncio]>=2.0.25
asyncpg>=0.29.0
alembic>=1.13.0
pydantic>=2.5.0
email-validator>=2.0.0
pydantic-settings>=2.1.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
bcrypt>=4.1.0
python-multipart>=0.0.6
httpx>=0.26.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
slowapi>=0.1.9
python-docx>=1.1.0
openpyxl>=3.1.0
apscheduler>=3.10.0
greenlet>=3.0.0
psycopg2-binary>=2.9.9
sentry-sdk[fastapi]>=2.0.0

```


---

## Исходный код: `backend/scripts/__init__.py`

> 2 строк, 82 байт

```py
"""Утилиты и одноразовые скрипты (сид и т.д.)."""

```


---

## Исходный код: `backend/scripts/seed.py`

> 136 строк, 4,996 байт

```py
"""Сид начальных пользователей и демо-события. Запуск: python -m scripts.seed (из каталога backend, PYTHONPATH=.).

Почты и пароль задаются через переменные окружения (удобно для прода):
  SEED_ADMIN_EMAIL, SEED_MANAGER_EMAIL, SEED_OPERATOR_EMAIL, SEED_PASSWORD
Значения по умолчанию — как в демо (example.com).

Чистый прод (только суперадмин, без демо-мероприятия и без менеджера/оператора):
  SEED_ONLY_SUPERADMIN=1
"""

import asyncio
import os
import uuid
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import select

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.enums import UserRole
from app.models.stream import StreamDay, StreamEvent
from app.models.user import User


def _seed_env() -> tuple[str, str, str, str]:
    admin = os.getenv("SEED_ADMIN_EMAIL", "admin@example.com").strip()
    manager = os.getenv("SEED_MANAGER_EMAIL", "manager@example.com").strip()
    operator = os.getenv("SEED_OPERATOR_EMAIL", "operator@example.com").strip()
    password = os.getenv("SEED_PASSWORD", "ChangeMe123!")
    return admin, manager, operator, password


async def main() -> None:
    admin_email, manager_email, operator_email, seed_password = _seed_env()
    only_superadmin = os.getenv("SEED_ONLY_SUPERADMIN", "").strip().lower() in ("1", "true", "yes", "on")

    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User.id).where(User.email == admin_email))
        if res.scalar_one_or_none():
            print(f"Сид уже выполнен (найден {admin_email}).")
            return

        pwd_hash = hash_password(seed_password)
        if only_superadmin:
            users = [
                User(
                    id=uuid.uuid4(),
                    email=admin_email,
                    first_name="Администратор",
                    last_name="Системный",
                    password_hash=pwd_hash,
                    role=UserRole.SUPERADMIN,
                    is_active=True,
                    suggest_password_change=False,
                    onboarding_completed=True,
                ),
            ]
            for u in users:
                session.add(u)
            await session.commit()
            print(f"Сид (только суперадмин): {admin_email} / пароль из SEED_PASSWORD")
            return

        users = [
            User(
                id=uuid.uuid4(),
                email=admin_email,
                first_name="Администратор",
                last_name="Системный",
                password_hash=pwd_hash,
                role=UserRole.SUPERADMIN,
                is_active=True,
                suggest_password_change=False,
                onboarding_completed=True,
            ),
            User(
                id=uuid.uuid4(),
                email=manager_email,
                first_name="Михаил",
                last_name="Петров",
                password_hash=pwd_hash,
                role=UserRole.STREAM_MANAGER,
                is_active=True,
                suggest_password_change=False,
                onboarding_completed=True,
            ),
            User(
                id=uuid.uuid4(),
                email=operator_email,
                first_name="Алексей",
                last_name="Сидоров",
                password_hash=pwd_hash,
                role=UserRole.OPERATOR,
                is_active=True,
                suggest_password_change=False,
                onboarding_completed=True,
            ),
        ]
        for u in users:
            session.add(u)
        await session.flush()

        mgr_id = next(u.id for u in users if u.role == UserRole.STREAM_MANAGER)
        ev = StreamEvent(
            title="Демо: чемпионат",
            start_date=date.today(),
            duration_days=3,
            created_by_id=mgr_id,
        )
        session.add(ev)
        await session.flush()
        for i in range(1, 4):
            session.add(
                StreamDay(
                    stream_event_id=ev.id,
                    day_index=i,
                    stream_url=f"rtmp://demo.example/live/day{i}",
                    server_url="https://demo-cdn.example",
                    stream_key=f"key-day-{i}",
                )
            )

        await session.commit()
        print(
            f"Сид выполнен: {admin_email}, {manager_email}, {operator_email} / пароль из SEED_PASSWORD "
            f"(по умолчанию ChangeMe123!)"
        )


if __name__ == "__main__":
    asyncio.run(main())

```


---

## Исходный код: `backend/scripts/test_smtp.py`

> 79 строк, 3,154 байт

```py
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
    from app.services.email_html_layout import wrap_email_html
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

    base = (settings.app_public_base_url or "").strip().rstrip("/")
    body_html = wrap_email_html(
        headline="Тест SMTP",
        inner_html='<p style="margin:0">Если вы видите это письмо, SMTP настроен верно.</p>',
        public_base_url=base,
    )
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
            body_html=body_html,
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

```


---

## Исходный код: `backend/tests/test_health.py`

> 16 строк, 440 байт

```py
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_health_ok() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data

```


---

## Исходный код: `backend/tests/test_logo_zip.py`

> 13 строк, 417 байт

```py
from app.services.logo_service import stream_zip_filename


def test_stream_zip_filename_uses_title_and_date() -> None:
    name = stream_zip_filename("Турнир Весна", "19.03.2026")
    assert name.endswith("_assets.zip")
    assert "19.03.2026" in name


def test_stream_zip_filename_empty_title_fallback() -> None:
    name = stream_zip_filename("   ", "01.01.2026")
    assert name.startswith("stream_")

```


---

## Исходный код: `backend/tests/test_timecode.py`

> 10 строк, 326 байт

```py
from app.utils.timecode import seconds_to_hhmmss


def test_seconds_to_hhmmss() -> None:
    assert seconds_to_hhmmss(0) == "00:00:00"
    assert seconds_to_hhmmss(10) == "00:00:10"
    assert seconds_to_hhmmss(600) == "00:10:00"
    assert seconds_to_hhmmss(3661) == "01:01:01"
    assert seconds_to_hhmmss(-5) == "00:00:00"

```


---

## Исходный код: `backend/tests/test_timezone_format.py`

> 20 строк, 589 байт

```py
from datetime import date, datetime
from zoneinfo import ZoneInfo

from app.core.timezone import format_moscow_date, format_moscow_datetime, to_moscow


def test_format_moscow_datetime_from_utc() -> None:
    dt = datetime(2026, 3, 19, 18, 4, 28, tzinfo=ZoneInfo("UTC"))
    assert format_moscow_datetime(dt) == "19.03.2026 21:04"


def test_format_moscow_date() -> None:
    assert format_moscow_date(date(2026, 3, 7)) == "07.03.2026"


def test_to_moscow_naive_utc() -> None:
    dt = datetime(2026, 1, 1, 12, 0, 0)
    m = to_moscow(dt)
    assert m.tzinfo == ZoneInfo("Europe/Moscow")

```


---

## Исходный код: `docker-compose.yml`

> 51 строк, 1,317 байт

```yml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: streaming
      POSTGRES_PASSWORD: streaming
      POSTGRES_DB: streaming
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U streaming -d streaming"]
      interval: 5s
      timeout: 5s
      retries: 10

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      args:
        PIP_INDEX_URL: ${PIP_INDEX_URL:-https://pypi.org/simple}
    environment:
      DATABASE_URL: postgresql+asyncpg://streaming:streaming@db:5432/streaming
      DATABASE_URL_SYNC: postgresql://streaming:streaming@db:5432/streaming
      APP_VERSION: ${APP_VERSION:-1.0.0}
      JWT_SECRET: ${JWT_SECRET:-change-me-in-production-use-long-random}
      JWT_ACCESS_EXPIRE_MINUTES: "30"
      JWT_REFRESH_EXPIRE_DAYS: "7"
      CORS_ORIGINS: http://localhost,http://127.0.0.1,http://localhost:5173,http://127.0.0.1:5173
      REFRESH_COOKIE_SECURE: "false"
      REFRESH_COOKIE_SAMESITE: lax
    depends_on:
      db:
        condition: service_healthy
    expose:
      - "8000"

  nginx:
    build:
      context: .
      dockerfile: nginx/Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres-data:

```


---

## Исходный код: `frontend/.storybook/main.ts`

> 25 строк, 613 байт

```ts
import path from 'node:path'
import { fileURLToPath } from 'node:url'

import type { StorybookConfig } from '@storybook/react-vite'
import { mergeConfig } from 'vite'

const dirname = path.dirname(fileURLToPath(import.meta.url))

const config: StorybookConfig = {
  stories: ['../src/**/*.stories.@(ts|tsx)'],
  addons: ['@storybook/addon-essentials'],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  async viteFinal(viteConfig) {
    return mergeConfig(viteConfig, {
      resolve: {
        alias: { '@': path.resolve(dirname, '../src') },
      },
    })
  },
}
export default config

```


---

## Исходный код: `frontend/.storybook/preview.tsx`

> 22 строк, 484 байт

```tsx
import type { Preview } from '@storybook/react'
import React from 'react'

import { ConfigProvider } from 'antd'
import ruRU from 'antd/locale/ru_RU'

import { appTheme } from '../src/theme'

const preview: Preview = {
  decorators: [
    (Story) => (
      <ConfigProvider locale={ruRU} theme={appTheme}>
        <div style={{ background: '#f4f6f9', minHeight: '100vh', padding: 24 }}>
          <Story />
        </div>
      </ConfigProvider>
    ),
  ],
}

export default preview

```


---

## Исходный код: `frontend/e2e/playwright.config.ts`

> 21 строк, 533 байт

```ts
import path from 'node:path'
import { fileURLToPath } from 'node:url'

import { defineConfig, devices } from '@playwright/test'

const e2eDir = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  testDir: e2eDir,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'list',
  use: {
    baseURL: process.env.E2E_BASE_URL ?? 'http://127.0.0.1',
    trace: 'on-first-retry',
    ...devices['Desktop Chrome'],
  },
})

```


---

## Исходный код: `frontend/e2e/smoke.spec.ts`

> 7 строк, 232 байт

```ts
import { expect, test } from '@playwright/test'

test('страница входа отображается', async ({ page }) => {
  await page.goto('/login')
  await expect(page.locator('input[type="password"]')).toBeVisible()
})

```


---

## Исходный код: `frontend/index.html`

> 28 строк, 1,025 байт

```html
<!doctype html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, viewport-fit=cover"
    />
    <meta name="theme-color" content="#070b10" />
    <meta name="mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <link rel="icon" type="image/png" href="/mainstream-logo.png" />
    <link rel="apple-touch-icon" href="/mainstream-logo.png" />
    <title>MainStream — панель эфиров</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
      rel="stylesheet"
    />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>

```


---

## Исходный код: `frontend/package-lock.json`

> 9198 строк, 329,594 байт

```json
{
  "name": "stream-sponsor-frontend",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "stream-sponsor-frontend",
      "version": "1.0.0",
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
    },
    "node_modules/@ant-design/colors": {
      "version": "7.2.1",
      "resolved": "https://registry.npmjs.org/@ant-design/colors/-/colors-7.2.1.tgz",
      "integrity": "sha512-lCHDcEzieu4GA3n8ELeZ5VQ8pKQAWcGGLRTQ50aQM2iqPpq2evTxER84jfdPvsPAtEcZ7m44NI45edFMo8oOYQ==",
      "license": "MIT",
      "dependencies": {
        "@ant-design/fast-color": "^2.0.6"
      }
    },
    "node_modules/@ant-design/cssinjs": {
      "version": "1.24.0",
      "resolved": "https://registry.npmjs.org/@ant-design/cssinjs/-/cssinjs-1.24.0.tgz",
      "integrity": "sha512-K4cYrJBsgvL+IoozUXYjbT6LHHNt+19a9zkvpBPxLjFHas1UpPM2A5MlhROb0BT8N8WoavM5VsP9MeSeNK/3mg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.11.1",
        "@emotion/hash": "^0.8.0",
        "@emotion/unitless": "^0.7.5",
        "classnames": "^2.3.1",
        "csstype": "^3.1.3",
        "rc-util": "^5.35.0",
        "stylis": "^4.3.4"
      },
      "peerDependencies": {
        "react": ">=16.0.0",
        "react-dom": ">=16.0.0"
      }
    },
    "node_modules/@ant-design/cssinjs-utils": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/@ant-design/cssinjs-utils/-/cssinjs-utils-1.1.3.tgz",
      "integrity": "sha512-nOoQMLW1l+xR1Co8NFVYiP8pZp3VjIIzqV6D6ShYF2ljtdwWJn5WSsH+7kvCktXL/yhEtWURKOfH5Xz/gzlwsg==",
      "license": "MIT",
      "dependencies": {
        "@ant-design/cssinjs": "^1.21.0",
        "@babel/runtime": "^7.23.2",
        "rc-util": "^5.38.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/@ant-design/fast-color": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/@ant-design/fast-color/-/fast-color-2.0.6.tgz",
      "integrity": "sha512-y2217gk4NqL35giHl72o6Zzqji9O7vHh9YmhUVkPtAOpoTCH4uWxo/pr4VE8t0+ChEPs0qo4eJRC5Q1eXWo3vA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.24.7"
      },
      "engines": {
        "node": ">=8.x"
      }
    },
    "node_modules/@ant-design/icons": {
      "version": "5.6.1",
      "resolved": "https://registry.npmjs.org/@ant-design/icons/-/icons-5.6.1.tgz",
      "integrity": "sha512-0/xS39c91WjPAZOWsvi1//zjx6kAp4kxWwctR6kuU6p133w8RU0D2dSCvZC19uQyharg/sAvYxGYWl01BbZZfg==",
      "license": "MIT",
      "dependencies": {
        "@ant-design/colors": "^7.0.0",
        "@ant-design/icons-svg": "^4.4.0",
        "@babel/runtime": "^7.24.8",
        "classnames": "^2.2.6",
        "rc-util": "^5.31.1"
      },
      "engines": {
        "node": ">=8"
      },
      "peerDependencies": {
        "react": ">=16.0.0",
        "react-dom": ">=16.0.0"
      }
    },
    "node_modules/@ant-design/icons-svg": {
      "version": "4.4.2",
      "resolved": "https://registry.npmjs.org/@ant-design/icons-svg/-/icons-svg-4.4.2.tgz",
      "integrity": "sha512-vHbT+zJEVzllwP+CM+ul7reTEfBR0vgxFe7+lREAsAA7YGsYpboiq2sQNeQeRvh09GfQgs/GyFEvZpJ9cLXpXA==",
      "license": "MIT"
    },
    "node_modules/@ant-design/react-slick": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/@ant-design/react-slick/-/react-slick-1.1.2.tgz",
      "integrity": "sha512-EzlvzE6xQUBrZuuhSAFTdsr4P2bBBHGZwKFemEfq8gIGyIQCxalYfZW/T2ORbtQx5rU69o+WycP3exY/7T1hGA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.4",
        "classnames": "^2.2.5",
        "json2mq": "^0.2.0",
        "resize-observer-polyfill": "^1.5.1",
        "throttle-debounce": "^5.0.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0"
      }
    },
    "node_modules/@apideck/better-ajv-errors": {
      "version": "0.3.6",
      "resolved": "https://registry.npmjs.org/@apideck/better-ajv-errors/-/better-ajv-errors-0.3.6.tgz",
      "integrity": "sha512-P+ZygBLZtkp0qqOAJJVX4oX/sFo5JR3eBWwwuqHHhK0GIgQOKWrAfiAaWX0aArHkRWHMuggFEgAZNxVPwPZYaA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "json-schema": "^0.4.0",
        "jsonpointer": "^5.0.0",
        "leven": "^3.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "peerDependencies": {
        "ajv": ">=8"
      }
    },
    "node_modules/@babel/code-frame": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/code-frame/-/code-frame-7.29.0.tgz",
      "integrity": "sha512-9NhCeYjq9+3uxgdtp20LSiJXJvN0FeCtNGpJxuMFZ1Kv3cWUNb6DOhJwUvcVCzKGR66cw4njwM6hrJLqgOwbcw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-validator-identifier": "^7.28.5",
        "js-tokens": "^4.0.0",
        "picocolors": "^1.1.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/compat-data": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/compat-data/-/compat-data-7.29.0.tgz",
      "integrity": "sha512-T1NCJqT/j9+cn8fvkt7jtwbLBfLC/1y1c7NtCeXFRgzGTsafi68MRv8yzkYSapBnFA6L3U2VSc02ciDzoAJhJg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/core": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/core/-/core-7.29.0.tgz",
      "integrity": "sha512-CGOfOJqWjg2qW/Mb6zNsDm+u5vFQ8DxXfbM09z69p5Z6+mE1ikP2jUXw+j42Pf1XTYED2Rni5f95npYeuwMDQA==",
      "dev": true,
      "license": "MIT",
      "peer": true,
      "dependencies": {
        "@babel/code-frame": "^7.29.0",
        "@babel/generator": "^7.29.0",
        "@babel/helper-compilation-targets": "^7.28.6",
        "@babel/helper-module-transforms": "^7.28.6",
        "@babel/helpers": "^7.28.6",
        "@babel/parser": "^7.29.0",
        "@babel/template": "^7.28.6",
        "@babel/traverse": "^7.29.0",
        "@babel/types": "^7.29.0",
        "@jridgewell/remapping": "^2.3.5",
        "convert-source-map": "^2.0.0",
        "debug": "^4.1.0",
        "gensync": "^1.0.0-beta.2",
        "json5": "^2.2.3",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/babel"
      }
    },
    "node_modules/@babel/generator": {
      "version": "7.29.1",
      "resolved": "https://registry.npmjs.org/@babel/generator/-/generator-7.29.1.tgz",
      "integrity": "sha512-qsaF+9Qcm2Qv8SRIMMscAvG4O3lJ0F1GuMo5HR/Bp02LopNgnZBC/EkbevHFeGs4ls/oPz9v+Bsmzbkbe+0dUw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.29.0",
        "@babel/types": "^7.29.0",
        "@jridgewell/gen-mapping": "^0.3.12",
        "@jridgewell/trace-mapping": "^0.3.28",
        "jsesc": "^3.0.2"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-annotate-as-pure": {
      "version": "7.27.3",
      "resolved": "https://registry.npmjs.org/@babel/helper-annotate-as-pure/-/helper-annotate-as-pure-7.27.3.tgz",
      "integrity": "sha512-fXSwMQqitTGeHLBC08Eq5yXz2m37E4pJX1qAU1+2cNedz/ifv/bVXft90VeSav5nFO61EcNgwr0aJxbyPaWBPg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.27.3"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-compilation-targets": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-compilation-targets/-/helper-compilation-targets-7.28.6.tgz",
      "integrity": "sha512-JYtls3hqi15fcx5GaSNL7SCTJ2MNmjrkHXg4FSpOA/grxK8KwyZ5bubHsCq8FXCkua6xhuaaBit+3b7+VZRfcA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/compat-data": "^7.28.6",
        "@babel/helper-validator-option": "^7.27.1",
        "browserslist": "^4.24.0",
        "lru-cache": "^5.1.1",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-create-class-features-plugin": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-create-class-features-plugin/-/helper-create-class-features-plugin-7.28.6.tgz",
      "integrity": "sha512-dTOdvsjnG3xNT9Y0AUg1wAl38y+4Rl4sf9caSQZOXdNqVn+H+HbbJ4IyyHaIqNR6SW9oJpA/RuRjsjCw2IdIow==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "@babel/helper-member-expression-to-functions": "^7.28.5",
        "@babel/helper-optimise-call-expression": "^7.27.1",
        "@babel/helper-replace-supers": "^7.28.6",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1",
        "@babel/traverse": "^7.28.6",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-create-regexp-features-plugin": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/helper-create-regexp-features-plugin/-/helper-create-regexp-features-plugin-7.28.5.tgz",
      "integrity": "sha512-N1EhvLtHzOvj7QQOUCCS3NrPJP8c5W6ZXCHDn7Yialuy1iu4r5EmIYkXlKNqT99Ciw+W0mDqWoR6HWMZlFP3hw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "regexpu-core": "^6.3.1",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-define-polyfill-provider": {
      "version": "0.6.8",
      "resolved": "https://registry.npmjs.org/@babel/helper-define-polyfill-provider/-/helper-define-polyfill-provider-0.6.8.tgz",
      "integrity": "sha512-47UwBLPpQi1NoWzLuHNjRoHlYXMwIJoBf7MFou6viC/sIHWYygpvr0B6IAyh5sBdA2nr2LPIRww8lfaUVQINBA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-compilation-targets": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "debug": "^4.4.3",
        "lodash.debounce": "^4.0.8",
        "resolve": "^1.22.11"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/@babel/helper-globals": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@babel/helper-globals/-/helper-globals-7.28.0.tgz",
      "integrity": "sha512-+W6cISkXFa1jXsDEdYA8HeevQT/FULhxzR99pxphltZcVaugps53THCeiWA8SguxxpSp3gKPiuYfSWopkLQ4hw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-member-expression-to-functions": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/helper-member-expression-to-functions/-/helper-member-expression-to-functions-7.28.5.tgz",
      "integrity": "sha512-cwM7SBRZcPCLgl8a7cY0soT1SptSzAlMH39vwiRpOQkJlh53r5hdHwLSCZpQdVLT39sZt+CRpNwYG4Y2v77atg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/traverse": "^7.28.5",
        "@babel/types": "^7.28.5"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-module-imports": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-module-imports/-/helper-module-imports-7.28.6.tgz",
      "integrity": "sha512-l5XkZK7r7wa9LucGw9LwZyyCUscb4x37JWTPz7swwFE/0FMQAGpiWUZn8u9DzkSBWEcK25jmvubfpw2dnAMdbw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/traverse": "^7.28.6",
        "@babel/types": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-module-transforms": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-module-transforms/-/helper-module-transforms-7.28.6.tgz",
      "integrity": "sha512-67oXFAYr2cDLDVGLXTEABjdBJZ6drElUSI7WKp70NrpyISso3plG9SAGEF6y7zbha/wOzUByWWTJvEDVNIUGcA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.28.6",
        "@babel/helper-validator-identifier": "^7.28.5",
        "@babel/traverse": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-optimise-call-expression": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-optimise-call-expression/-/helper-optimise-call-expression-7.27.1.tgz",
      "integrity": "sha512-URMGH08NzYFhubNSGJrpUEphGKQwMQYBySzat5cAByY1/YgIRkULnIy3tAMeszlL/so2HbeilYloUmSpd7GdVw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-plugin-utils": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-plugin-utils/-/helper-plugin-utils-7.28.6.tgz",
      "integrity": "sha512-S9gzZ/bz83GRysI7gAD4wPT/AI3uCnY+9xn+Mx/KPs2JwHJIz1W8PZkg2cqyt3RNOBM8ejcXhV6y8Og7ly/Dug==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-remap-async-to-generator": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-remap-async-to-generator/-/helper-remap-async-to-generator-7.27.1.tgz",
      "integrity": "sha512-7fiA521aVw8lSPeI4ZOD3vRFkoqkJcS+z4hFo82bFSH/2tNd6eJ5qCVMS5OzDmZh/kaHQeBaeyxK6wljcPtveA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.1",
        "@babel/helper-wrap-function": "^7.27.1",
        "@babel/traverse": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-replace-supers": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-replace-supers/-/helper-replace-supers-7.28.6.tgz",
      "integrity": "sha512-mq8e+laIk94/yFec3DxSjCRD2Z0TAjhVbEJY3UQrlwVo15Lmt7C2wAUbK4bjnTs4APkwsYLTahXRraQXhb1WCg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-member-expression-to-functions": "^7.28.5",
        "@babel/helper-optimise-call-expression": "^7.27.1",
        "@babel/traverse": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-skip-transparent-expression-wrappers": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-skip-transparent-expression-wrappers/-/helper-skip-transparent-expression-wrappers-7.27.1.tgz",
      "integrity": "sha512-Tub4ZKEXqbPjXgWLl2+3JpQAYBJ8+ikpQ2Ocj/q/r0LwE3UhENh7EUabyHjz2kCEsrRY83ew2DQdHluuiDQFzg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/traverse": "^7.27.1",
        "@babel/types": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-string-parser": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-string-parser/-/helper-string-parser-7.27.1.tgz",
      "integrity": "sha512-qMlSxKbpRlAridDExk92nSobyDdpPijUq2DW6oDnUqd0iOGxmQjyqhMIihI9+zv4LPyZdRje2cavWPbCbWm3eA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-identifier": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-identifier/-/helper-validator-identifier-7.28.5.tgz",
      "integrity": "sha512-qSs4ifwzKJSV39ucNjsvc6WVHs6b7S03sOh2OcHF9UHfVPqWWALUsNUVzhSBiItjRZoLHx7nIarVjqKVusUZ1Q==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-option": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-option/-/helper-validator-option-7.27.1.tgz",
      "integrity": "sha512-YvjJow9FxbhFFKDSuFnVCe2WxXk1zWc22fFePVNEaWJEu8IrZVlda6N0uHwzZrUM1il7NC9Mlp4MaJYbYd9JSg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-wrap-function": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/helper-wrap-function/-/helper-wrap-function-7.28.6.tgz",
      "integrity": "sha512-z+PwLziMNBeSQJonizz2AGnndLsP2DeGHIxDAn+wdHOGuo4Fo1x1HBPPXeE9TAOPHNNWQKCSlA2VZyYyyibDnQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/template": "^7.28.6",
        "@babel/traverse": "^7.28.6",
        "@babel/types": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helpers": {
      "version": "7.29.2",
      "resolved": "https://registry.npmjs.org/@babel/helpers/-/helpers-7.29.2.tgz",
      "integrity": "sha512-HoGuUs4sCZNezVEKdVcwqmZN8GoHirLUcLaYVNBK2J0DadGtdcqgr3BCbvH8+XUo4NGjNl3VOtSjEKNzqfFgKw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/template": "^7.28.6",
        "@babel/types": "^7.29.0"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/parser": {
      "version": "7.29.2",
      "resolved": "https://registry.npmjs.org/@babel/parser/-/parser-7.29.2.tgz",
      "integrity": "sha512-4GgRzy/+fsBa72/RZVJmGKPmZu9Byn8o4MoLpmNe1m8ZfYnz5emHLQz3U4gLud6Zwl0RZIcgiLD7Uq7ySFuDLA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.29.0"
      },
      "bin": {
        "parser": "bin/babel-parser.js"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-firefox-class-in-computed-class-key": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-firefox-class-in-computed-class-key/-/plugin-bugfix-firefox-class-in-computed-class-key-7.28.5.tgz",
      "integrity": "sha512-87GDMS3tsmMSi/3bWOte1UblL+YUTFMV8SZPZ2eSEL17s74Cw/l63rR6NmGVKMYW2GYi85nE+/d6Hw5N0bEk2Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/traverse": "^7.28.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-safari-class-field-initializer-scope": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-safari-class-field-initializer-scope/-/plugin-bugfix-safari-class-field-initializer-scope-7.27.1.tgz",
      "integrity": "sha512-qNeq3bCKnGgLkEXUuFry6dPlGfCdQNZbn7yUAPCInwAJHMU7THJfrBSozkcWq5sNM6RcF3S8XyQL2A52KNR9IA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-safari-id-destructuring-collision-in-function-expression": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-safari-id-destructuring-collision-in-function-expression/-/plugin-bugfix-safari-id-destructuring-collision-in-function-expression-7.27.1.tgz",
      "integrity": "sha512-g4L7OYun04N1WyqMNjldFwlfPCLVkgB54A/YCXICZYBsvJJE3kByKv9c9+R/nAfmIfjl2rKYLNyMHboYbZaWaA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-v8-spread-parameters-in-optional-chaining": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-v8-spread-parameters-in-optional-chaining/-/plugin-bugfix-v8-spread-parameters-in-optional-chaining-7.27.1.tgz",
      "integrity": "sha512-oO02gcONcD5O1iTLi/6frMJBIwWEHceWGSGqrpCmEL8nogiS6J9PBlE48CaK20/Jx1LuRml9aDftLgdjXT8+Cw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1",
        "@babel/plugin-transform-optional-chaining": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.13.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-v8-static-class-fields-redefine-readonly": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-v8-static-class-fields-redefine-readonly/-/plugin-bugfix-v8-static-class-fields-redefine-readonly-7.28.6.tgz",
      "integrity": "sha512-a0aBScVTlNaiUe35UtfxAN7A/tehvvG4/ByO6+46VPKTRSlfnAFsgKy0FUh+qAkQrDTmhDkT+IBOKlOoMUxQ0g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/traverse": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-proposal-private-property-in-object": {
      "version": "7.21.0-placeholder-for-preset-env.2",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-private-property-in-object/-/plugin-proposal-private-property-in-object-7.21.0-placeholder-for-preset-env.2.tgz",
      "integrity": "sha512-SOSkfJDddaM7mak6cPEpswyTRnuRltl429hMraQEglW+OkovnCzsiszTmsrlY//qLFjCpQDFRvjdm2wA5pPm9w==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-import-assertions": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-import-assertions/-/plugin-syntax-import-assertions-7.28.6.tgz",
      "integrity": "sha512-pSJUpFHdx9z5nqTSirOCMtYVP2wFgoWhP0p3g8ONK/4IHhLIBd0B9NYqAvIUAhq+OkhO4VM1tENCt0cjlsNShw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-import-attributes": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-import-attributes/-/plugin-syntax-import-attributes-7.28.6.tgz",
      "integrity": "sha512-jiLC0ma9XkQT3TKJ9uYvlakm66Pamywo+qwL+oL8HJOvc6TWdZXVfhqJr8CCzbSGUAbDOzlGHJC1U+vRfLQDvw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-unicode-sets-regex": {
      "version": "7.18.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-unicode-sets-regex/-/plugin-syntax-unicode-sets-regex-7.18.6.tgz",
      "integrity": "sha512-727YkEAPwSIQTv5im8QHz3upqp92JTWhidIC81Tdx4VJYIte/VndKf1qKrfnnhPLiPghStWfvC/iFaMCQu7Nqg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.18.6",
        "@babel/helper-plugin-utils": "^7.18.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-arrow-functions": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-arrow-functions/-/plugin-transform-arrow-functions-7.27.1.tgz",
      "integrity": "sha512-8Z4TGic6xW70FKThA5HYEKKyBpOOsucTOD1DjU3fZxDg+K3zBJcXMFnt/4yQiZnf5+MiOMSXQ9PaEK/Ilh1DeA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-async-generator-functions": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-async-generator-functions/-/plugin-transform-async-generator-functions-7.29.0.tgz",
      "integrity": "sha512-va0VdWro4zlBr2JsXC+ofCPB2iG12wPtVGTWFx2WLDOM3nYQZZIGP82qku2eW/JR83sD+k2k+CsNtyEbUqhU6w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-remap-async-to-generator": "^7.27.1",
        "@babel/traverse": "^7.29.0"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-async-to-generator": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-async-to-generator/-/plugin-transform-async-to-generator-7.28.6.tgz",
      "integrity": "sha512-ilTRcmbuXjsMmcZ3HASTe4caH5Tpo93PkTxF9oG2VZsSWsahydmcEHhix9Ik122RcTnZnUzPbmux4wh1swfv7g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-remap-async-to-generator": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-block-scoped-functions": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-block-scoped-functions/-/plugin-transform-block-scoped-functions-7.27.1.tgz",
      "integrity": "sha512-cnqkuOtZLapWYZUYM5rVIdv1nXYuFVIltZ6ZJ7nIj585QsjKM5dhL2Fu/lICXZ1OyIAFc7Qy+bvDAtTXqGrlhg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-block-scoping": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-block-scoping/-/plugin-transform-block-scoping-7.28.6.tgz",
      "integrity": "sha512-tt/7wOtBmwHPNMPu7ax4pdPz6shjFrmHDghvNC+FG9Qvj7D6mJcoRQIF5dy4njmxR941l6rgtvfSB2zX3VlUIw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-class-properties": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-class-properties/-/plugin-transform-class-properties-7.28.6.tgz",
      "integrity": "sha512-dY2wS3I2G7D697VHndN91TJr8/AAfXQNt5ynCTI/MpxMsSzHp+52uNivYT5wCPax3whc47DR8Ba7cmlQMg24bw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-class-static-block": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-class-static-block/-/plugin-transform-class-static-block-7.28.6.tgz",
      "integrity": "sha512-rfQ++ghVwTWTqQ7w8qyDxL1XGihjBss4CmTgGRCTAC9RIbhVpyp4fOeZtta0Lbf+dTNIVJer6ych2ibHwkZqsQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.12.0"
      }
    },
    "node_modules/@babel/plugin-transform-classes": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-classes/-/plugin-transform-classes-7.28.6.tgz",
      "integrity": "sha512-EF5KONAqC5zAqT783iMGuM2ZtmEBy+mJMOKl2BCvPZ2lVrwvXnB6o+OBWCS+CoeCCpVRF2sA2RBKUxvT8tQT5Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "@babel/helper-compilation-targets": "^7.28.6",
        "@babel/helper-globals": "^7.28.0",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-replace-supers": "^7.28.6",
        "@babel/traverse": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-computed-properties": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-computed-properties/-/plugin-transform-computed-properties-7.28.6.tgz",
      "integrity": "sha512-bcc3k0ijhHbc2lEfpFHgx7eYw9KNXqOerKWfzbxEHUGKnS3sz9C4CNL9OiFN1297bDNfUiSO7DaLzbvHQQQ1BQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/template": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-destructuring": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-destructuring/-/plugin-transform-destructuring-7.28.5.tgz",
      "integrity": "sha512-Kl9Bc6D0zTUcFUvkNuQh4eGXPKKNDOJQXVyyM4ZAQPMveniJdxi8XMJwLo+xSoW3MIq81bD33lcUe9kZpl0MCw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/traverse": "^7.28.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-dotall-regex": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-dotall-regex/-/plugin-transform-dotall-regex-7.28.6.tgz",
      "integrity": "sha512-SljjowuNKB7q5Oayv4FoPzeB74g3QgLt8IVJw9ADvWy3QnUb/01aw8I4AVv8wYnPvQz2GDDZ/g3GhcNyDBI4Bg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.28.5",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-duplicate-keys": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-duplicate-keys/-/plugin-transform-duplicate-keys-7.27.1.tgz",
      "integrity": "sha512-MTyJk98sHvSs+cvZ4nOauwTTG1JeonDjSGvGGUNHreGQns+Mpt6WX/dVzWBHgg+dYZhkC4X+zTDfkTU+Vy9y7Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-duplicate-named-capturing-groups-regex": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-duplicate-named-capturing-groups-regex/-/plugin-transform-duplicate-named-capturing-groups-regex-7.29.0.tgz",
      "integrity": "sha512-zBPcW2lFGxdiD8PUnPwJjag2J9otbcLQzvbiOzDxpYXyCuYX9agOwMPGn1prVH0a4qzhCKu24rlH4c1f7yA8rw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.28.5",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-dynamic-import": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-dynamic-import/-/plugin-transform-dynamic-import-7.27.1.tgz",
      "integrity": "sha512-MHzkWQcEmjzzVW9j2q8LGjwGWpG2mjwaaB0BNQwst3FIjqsg8Ct/mIZlvSPJvfi9y2AC8mi/ktxbFVL9pZ1I4A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-explicit-resource-management": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-explicit-resource-management/-/plugin-transform-explicit-resource-management-7.28.6.tgz",
      "integrity": "sha512-Iao5Konzx2b6g7EPqTy40UZbcdXE126tTxVFr/nAIj+WItNxjKSYTEw3RC+A2/ZetmdJsgueL1KhaMCQHkLPIg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/plugin-transform-destructuring": "^7.28.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-exponentiation-operator": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-exponentiation-operator/-/plugin-transform-exponentiation-operator-7.28.6.tgz",
      "integrity": "sha512-WitabqiGjV/vJ0aPOLSFfNY1u9U3R7W36B03r5I2KoNix+a3sOhJ3pKFB3R5It9/UiK78NiO0KE9P21cMhlPkw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-export-namespace-from": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-export-namespace-from/-/plugin-transform-export-namespace-from-7.27.1.tgz",
      "integrity": "sha512-tQvHWSZ3/jH2xuq/vZDy0jNn+ZdXJeM8gHvX4lnJmsc3+50yPlWdZXIc5ay+umX+2/tJIqHqiEqcJvxlmIvRvQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-for-of": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-for-of/-/plugin-transform-for-of-7.27.1.tgz",
      "integrity": "sha512-BfbWFFEJFQzLCQ5N8VocnCtA8J1CLkNTe2Ms2wocj75dd6VpiqS5Z5quTYcUoo4Yq+DN0rtikODccuv7RU81sw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-function-name": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-function-name/-/plugin-transform-function-name-7.27.1.tgz",
      "integrity": "sha512-1bQeydJF9Nr1eBCMMbC+hdwmRlsv5XYOMu03YSWFwNs0HsAmtSxxF1fyuYPqemVldVyFmlCU7w8UE14LupUSZQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-compilation-targets": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/traverse": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-json-strings": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-json-strings/-/plugin-transform-json-strings-7.28.6.tgz",
      "integrity": "sha512-Nr+hEN+0geQkzhbdgQVPoqr47lZbm+5fCUmO70722xJZd0Mvb59+33QLImGj6F+DkK3xgDi1YVysP8whD6FQAw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-literals": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-literals/-/plugin-transform-literals-7.27.1.tgz",
      "integrity": "sha512-0HCFSepIpLTkLcsi86GG3mTUzxV5jpmbv97hTETW3yzrAij8aqlD36toB1D0daVFJM8NK6GvKO0gslVQmm+zZA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-logical-assignment-operators": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-logical-assignment-operators/-/plugin-transform-logical-assignment-operators-7.28.6.tgz",
      "integrity": "sha512-+anKKair6gpi8VsM/95kmomGNMD0eLz1NQ8+Pfw5sAwWH9fGYXT50E55ZpV0pHUHWf6IUTWPM+f/7AAff+wr9A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-member-expression-literals": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-member-expression-literals/-/plugin-transform-member-expression-literals-7.27.1.tgz",
      "integrity": "sha512-hqoBX4dcZ1I33jCSWcXrP+1Ku7kdqXf1oeah7ooKOIiAdKQ+uqftgCFNOSzA5AMS2XIHEYeGFg4cKRCdpxzVOQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-modules-amd": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-modules-amd/-/plugin-transform-modules-amd-7.27.1.tgz",
      "integrity": "sha512-iCsytMg/N9/oFq6n+gFTvUYDZQOMK5kEdeYxmxt91fcJGycfxVP9CnrxoliM0oumFERba2i8ZtwRUCMhvP1LnA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-transforms": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-modules-commonjs": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-modules-commonjs/-/plugin-transform-modules-commonjs-7.28.6.tgz",
      "integrity": "sha512-jppVbf8IV9iWWwWTQIxJMAJCWBuuKx71475wHwYytrRGQ2CWiDvYlADQno3tcYpS/T2UUWFQp3nVtYfK/YBQrA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-transforms": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-modules-systemjs": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-modules-systemjs/-/plugin-transform-modules-systemjs-7.29.0.tgz",
      "integrity": "sha512-PrujnVFbOdUpw4UHiVwKvKRLMMic8+eC0CuNlxjsyZUiBjhFdPsewdXCkveh2KqBA9/waD0W1b4hXSOBQJezpQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-transforms": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-validator-identifier": "^7.28.5",
        "@babel/traverse": "^7.29.0"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-modules-umd": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-modules-umd/-/plugin-transform-modules-umd-7.27.1.tgz",
      "integrity": "sha512-iQBE/xC5BV1OxJbp6WG7jq9IWiD+xxlZhLrdwpPkTX3ydmXdvoCpyfJN7acaIBZaOqTfr76pgzqBJflNbeRK+w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-transforms": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-named-capturing-groups-regex": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-named-capturing-groups-regex/-/plugin-transform-named-capturing-groups-regex-7.29.0.tgz",
      "integrity": "sha512-1CZQA5KNAD6ZYQLPw7oi5ewtDNxH/2vuCh+6SmvgDfhumForvs8a1o9n0UrEoBD8HU4djO2yWngTQlXl1NDVEQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.28.5",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-new-target": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-new-target/-/plugin-transform-new-target-7.27.1.tgz",
      "integrity": "sha512-f6PiYeqXQ05lYq3TIfIDu/MtliKUbNwkGApPUvyo6+tc7uaR4cPjPe7DFPr15Uyycg2lZU6btZ575CuQoYh7MQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-nullish-coalescing-operator": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-nullish-coalescing-operator/-/plugin-transform-nullish-coalescing-operator-7.28.6.tgz",
      "integrity": "sha512-3wKbRgmzYbw24mDJXT7N+ADXw8BC/imU9yo9c9X9NKaLF1fW+e5H1U5QjMUBe4Qo4Ox/o++IyUkl1sVCLgevKg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-numeric-separator": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-numeric-separator/-/plugin-transform-numeric-separator-7.28.6.tgz",
      "integrity": "sha512-SJR8hPynj8outz+SlStQSwvziMN4+Bq99it4tMIf5/Caq+3iOc0JtKyse8puvyXkk3eFRIA5ID/XfunGgO5i6w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-object-rest-spread": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-object-rest-spread/-/plugin-transform-object-rest-spread-7.28.6.tgz",
      "integrity": "sha512-5rh+JR4JBC4pGkXLAcYdLHZjXudVxWMXbB6u6+E9lRL5TrGVbHt1TjxGbZ8CkmYw9zjkB7jutzOROArsqtncEA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-compilation-targets": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/plugin-transform-destructuring": "^7.28.5",
        "@babel/plugin-transform-parameters": "^7.27.7",
        "@babel/traverse": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-object-super": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-object-super/-/plugin-transform-object-super-7.27.1.tgz",
      "integrity": "sha512-SFy8S9plRPbIcxlJ8A6mT/CxFdJx/c04JEctz4jf8YZaVS2px34j7NXRrlGlHkN/M2gnpL37ZpGRGVFLd3l8Ng==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-replace-supers": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-optional-catch-binding": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-optional-catch-binding/-/plugin-transform-optional-catch-binding-7.28.6.tgz",
      "integrity": "sha512-R8ja/Pyrv0OGAvAXQhSTmWyPJPml+0TMqXlO5w+AsMEiwb2fg3WkOvob7UxFSL3OIttFSGSRFKQsOhJ/X6HQdQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-optional-chaining": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-optional-chaining/-/plugin-transform-optional-chaining-7.28.6.tgz",
      "integrity": "sha512-A4zobikRGJTsX9uqVFdafzGkqD30t26ck2LmOzAuLL8b2x6k3TIqRiT2xVvA9fNmFeTX484VpsdgmKNA0bS23w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-parameters": {
      "version": "7.27.7",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-parameters/-/plugin-transform-parameters-7.27.7.tgz",
      "integrity": "sha512-qBkYTYCb76RRxUM6CcZA5KRu8K4SM8ajzVeUgVdMVO9NN9uI/GaVmBg/WKJJGnNokV9SY8FxNOVWGXzqzUidBg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-private-methods": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-private-methods/-/plugin-transform-private-methods-7.28.6.tgz",
      "integrity": "sha512-piiuapX9CRv7+0st8lmuUlRSmX6mBcVeNQ1b4AYzJxfCMuBfB0vBXDiGSmm03pKJw1v6cZ8KSeM+oUnM6yAExg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-private-property-in-object": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-private-property-in-object/-/plugin-transform-private-property-in-object-7.28.6.tgz",
      "integrity": "sha512-b97jvNSOb5+ehyQmBpmhOCiUC5oVK4PMnpRvO7+ymFBoqYjeDHIU9jnrNUuwHOiL9RpGDoKBpSViarV+BU+eVA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "@babel/helper-create-class-features-plugin": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-property-literals": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-property-literals/-/plugin-transform-property-literals-7.27.1.tgz",
      "integrity": "sha512-oThy3BCuCha8kDZ8ZkgOg2exvPYUlprMukKQXI1r1pJ47NCvxfkEy8vK+r/hT9nF0Aa4H1WUPZZjHTFtAhGfmQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-jsx-self": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-jsx-self/-/plugin-transform-react-jsx-self-7.27.1.tgz",
      "integrity": "sha512-6UzkCs+ejGdZ5mFFC/OCUrv028ab2fp1znZmCZjAOBKiBK2jXD1O+BPSfX8X2qjJ75fZBMSnQn3Rq2mrBJK2mw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-jsx-source": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-jsx-source/-/plugin-transform-react-jsx-source-7.27.1.tgz",
      "integrity": "sha512-zbwoTsBruTeKB9hSq73ha66iFeJHuaFkUbwvqElnygoNbj/jHRsSeokowZFN3CZ64IvEqcmmkVe89OPXc7ldAw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-regenerator": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-regenerator/-/plugin-transform-regenerator-7.29.0.tgz",
      "integrity": "sha512-FijqlqMA7DmRdg/aINBSs04y8XNTYw/lr1gJ2WsmBnnaNw1iS43EPkJW+zK7z65auG3AWRFXWj+NcTQwYptUog==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-regexp-modifiers": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-regexp-modifiers/-/plugin-transform-regexp-modifiers-7.28.6.tgz",
      "integrity": "sha512-QGWAepm9qxpaIs7UM9FvUSnCGlb8Ua1RhyM4/veAxLwt3gMat/LSGrZixyuj4I6+Kn9iwvqCyPTtbdxanYoWYg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.28.5",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-reserved-words": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-reserved-words/-/plugin-transform-reserved-words-7.27.1.tgz",
      "integrity": "sha512-V2ABPHIJX4kC7HegLkYoDpfg9PVmuWy/i6vUM5eGK22bx4YVFD3M5F0QQnWQoDs6AGsUWTVOopBiMFQgHaSkVw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-shorthand-properties": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-shorthand-properties/-/plugin-transform-shorthand-properties-7.27.1.tgz",
      "integrity": "sha512-N/wH1vcn4oYawbJ13Y/FxcQrWk63jhfNa7jef0ih7PHSIHX2LB7GWE1rkPrOnka9kwMxb6hMl19p7lidA+EHmQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-spread": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-spread/-/plugin-transform-spread-7.28.6.tgz",
      "integrity": "sha512-9U4QObUC0FtJl05AsUcodau/RWDytrU6uKgkxu09mLR9HLDAtUMoPuuskm5huQsoktmsYpI+bGmq+iapDcriKA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-sticky-regex": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-sticky-regex/-/plugin-transform-sticky-regex-7.27.1.tgz",
      "integrity": "sha512-lhInBO5bi/Kowe2/aLdBAawijx+q1pQzicSgnkB6dUPc1+RC8QmJHKf2OjvU+NZWitguJHEaEmbV6VWEouT58g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-template-literals": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-template-literals/-/plugin-transform-template-literals-7.27.1.tgz",
      "integrity": "sha512-fBJKiV7F2DxZUkg5EtHKXQdbsbURW3DZKQUWphDum0uRP6eHGGa/He9mc0mypL680pb+e/lDIthRohlv8NCHkg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-typeof-symbol": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-typeof-symbol/-/plugin-transform-typeof-symbol-7.27.1.tgz",
      "integrity": "sha512-RiSILC+nRJM7FY5srIyc4/fGIwUhyDuuBSdWn4y6yT6gm652DpCHZjIipgn6B7MQ1ITOUnAKWixEUjQRIBIcLw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-unicode-escapes": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-unicode-escapes/-/plugin-transform-unicode-escapes-7.27.1.tgz",
      "integrity": "sha512-Ysg4v6AmF26k9vpfFuTZg8HRfVWzsh1kVfowA23y9j/Gu6dOuahdUVhkLqpObp3JIv27MLSii6noRnuKN8H0Mg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-unicode-property-regex": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-unicode-property-regex/-/plugin-transform-unicode-property-regex-7.28.6.tgz",
      "integrity": "sha512-4Wlbdl/sIZjzi/8St0evF0gEZrgOswVO6aOzqxh1kDZOl9WmLrHq2HtGhnOJZmHZYKP8WZ1MDLCt5DAWwRo57A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.28.5",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-unicode-regex": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-unicode-regex/-/plugin-transform-unicode-regex-7.27.1.tgz",
      "integrity": "sha512-xvINq24TRojDuyt6JGtHmkVkrfVV3FPT16uytxImLeBZqW3/H52yN+kM1MGuyPkIQxrzKwPHs5U/MP3qKyzkGw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-unicode-sets-regex": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-unicode-sets-regex/-/plugin-transform-unicode-sets-regex-7.28.6.tgz",
      "integrity": "sha512-/wHc/paTUmsDYN7SZkpWxogTOBNnlx7nBQYfy6JJlCT7G3mVhltk3e++N7zV0XfgGsrqBxd4rJQt9H16I21Y1Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.28.5",
        "@babel/helper-plugin-utils": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/preset-env": {
      "version": "7.29.2",
      "resolved": "https://registry.npmjs.org/@babel/preset-env/-/preset-env-7.29.2.tgz",
      "integrity": "sha512-DYD23veRYGvBFhcTY1iUvJnDNpuqNd/BzBwCvzOTKUnJjKg5kpUBh3/u9585Agdkgj+QuygG7jLfOPWMa2KVNw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/compat-data": "^7.29.0",
        "@babel/helper-compilation-targets": "^7.28.6",
        "@babel/helper-plugin-utils": "^7.28.6",
        "@babel/helper-validator-option": "^7.27.1",
        "@babel/plugin-bugfix-firefox-class-in-computed-class-key": "^7.28.5",
        "@babel/plugin-bugfix-safari-class-field-initializer-scope": "^7.27.1",
        "@babel/plugin-bugfix-safari-id-destructuring-collision-in-function-expression": "^7.27.1",
        "@babel/plugin-bugfix-v8-spread-parameters-in-optional-chaining": "^7.27.1",
        "@babel/plugin-bugfix-v8-static-class-fields-redefine-readonly": "^7.28.6",
        "@babel/plugin-proposal-private-property-in-object": "7.21.0-placeholder-for-preset-env.2",
        "@babel/plugin-syntax-import-assertions": "^7.28.6",
        "@babel/plugin-syntax-import-attributes": "^7.28.6",
        "@babel/plugin-syntax-unicode-sets-regex": "^7.18.6",
        "@babel/plugin-transform-arrow-functions": "^7.27.1",
        "@babel/plugin-transform-async-generator-functions": "^7.29.0",
        "@babel/plugin-transform-async-to-generator": "^7.28.6",
        "@babel/plugin-transform-block-scoped-functions": "^7.27.1",
        "@babel/plugin-transform-block-scoping": "^7.28.6",
        "@babel/plugin-transform-class-properties": "^7.28.6",
        "@babel/plugin-transform-class-static-block": "^7.28.6",
        "@babel/plugin-transform-classes": "^7.28.6",
        "@babel/plugin-transform-computed-properties": "^7.28.6",
        "@babel/plugin-transform-destructuring": "^7.28.5",
        "@babel/plugin-transform-dotall-regex": "^7.28.6",
        "@babel/plugin-transform-duplicate-keys": "^7.27.1",
        "@babel/plugin-transform-duplicate-named-capturing-groups-regex": "^7.29.0",
        "@babel/plugin-transform-dynamic-import": "^7.27.1",
        "@babel/plugin-transform-explicit-resource-management": "^7.28.6",
        "@babel/plugin-transform-exponentiation-operator": "^7.28.6",
        "@babel/plugin-transform-export-namespace-from": "^7.27.1",
        "@babel/plugin-transform-for-of": "^7.27.1",
        "@babel/plugin-transform-function-name": "^7.27.1",
        "@babel/plugin-transform-json-strings": "^7.28.6",
        "@babel/plugin-transform-literals": "^7.27.1",
        "@babel/plugin-transform-logical-assignment-operators": "^7.28.6",
        "@babel/plugin-transform-member-expression-literals": "^7.27.1",
        "@babel/plugin-transform-modules-amd": "^7.27.1",
        "@babel/plugin-transform-modules-commonjs": "^7.28.6",
        "@babel/plugin-transform-modules-systemjs": "^7.29.0",
        "@babel/plugin-transform-modules-umd": "^7.27.1",
        "@babel/plugin-transform-named-capturing-groups-regex": "^7.29.0",
        "@babel/plugin-transform-new-target": "^7.27.1",
        "@babel/plugin-transform-nullish-coalescing-operator": "^7.28.6",
        "@babel/plugin-transform-numeric-separator": "^7.28.6",
        "@babel/plugin-transform-object-rest-spread": "^7.28.6",
        "@babel/plugin-transform-object-super": "^7.27.1",
        "@babel/plugin-transform-optional-catch-binding": "^7.28.6",
        "@babel/plugin-transform-optional-chaining": "^7.28.6",
        "@babel/plugin-transform-parameters": "^7.27.7",
        "@babel/plugin-transform-private-methods": "^7.28.6",
        "@babel/plugin-transform-private-property-in-object": "^7.28.6",
        "@babel/plugin-transform-property-literals": "^7.27.1",
        "@babel/plugin-transform-regenerator": "^7.29.0",
        "@babel/plugin-transform-regexp-modifiers": "^7.28.6",
        "@babel/plugin-transform-reserved-words": "^7.27.1",
        "@babel/plugin-transform-shorthand-properties": "^7.27.1",
        "@babel/plugin-transform-spread": "^7.28.6",
        "@babel/plugin-transform-sticky-regex": "^7.27.1",
        "@babel/plugin-transform-template-literals": "^7.27.1",
        "@babel/plugin-transform-typeof-symbol": "^7.27.1",
        "@babel/plugin-transform-unicode-escapes": "^7.27.1",
        "@babel/plugin-transform-unicode-property-regex": "^7.28.6",
        "@babel/plugin-transform-unicode-regex": "^7.27.1",
        "@babel/plugin-transform-unicode-sets-regex": "^7.28.6",
        "@babel/preset-modules": "0.1.6-no-external-plugins",
        "babel-plugin-polyfill-corejs2": "^0.4.15",
        "babel-plugin-polyfill-corejs3": "^0.14.0",
        "babel-plugin-polyfill-regenerator": "^0.6.6",
        "core-js-compat": "^3.48.0",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/preset-modules": {
      "version": "0.1.6-no-external-plugins",
      "resolved": "https://registry.npmjs.org/@babel/preset-modules/-/preset-modules-0.1.6-no-external-plugins.tgz",
      "integrity": "sha512-HrcgcIESLm9aIR842yhJ5RWan/gebQUJ6E/E5+rf0y9o6oj7w0Br+sWuL6kEQ/o/AdfvR1Je9jG18/gnpwjEyA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.0.0",
        "@babel/types": "^7.4.4",
        "esutils": "^2.0.2"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/@babel/runtime": {
      "version": "7.29.2",
      "resolved": "https://registry.npmjs.org/@babel/runtime/-/runtime-7.29.2.tgz",
      "integrity": "sha512-JiDShH45zKHWyGe4ZNVRrCjBz8Nh9TMmZG1kh4QTK8hCBTWBi8Da+i7s1fJw7/lYpM4ccepSNfqzZ/QvABBi5g==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/template": {
      "version": "7.28.6",
      "resolved": "https://registry.npmjs.org/@babel/template/-/template-7.28.6.tgz",
      "integrity": "sha512-YA6Ma2KsCdGb+WC6UpBVFJGXL58MDA6oyONbjyF/+5sBgxY/dwkhLogbMT2GXXyU84/IhRw/2D1Os1B/giz+BQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.28.6",
        "@babel/parser": "^7.28.6",
        "@babel/types": "^7.28.6"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/traverse": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/traverse/-/traverse-7.29.0.tgz",
      "integrity": "sha512-4HPiQr0X7+waHfyXPZpWPfWL/J7dcN1mx9gL6WdQVMbPnF3+ZhSMs8tCxN7oHddJE9fhNE7+lxdnlyemKfJRuA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.29.0",
        "@babel/generator": "^7.29.0",
        "@babel/helper-globals": "^7.28.0",
        "@babel/parser": "^7.29.0",
        "@babel/template": "^7.28.6",
        "@babel/types": "^7.29.0",
        "debug": "^4.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/types": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/types/-/types-7.29.0.tgz",
      "integrity": "sha512-LwdZHpScM4Qz8Xw2iKSzS+cfglZzJGvofQICy7W7v4caru4EaAmyUuO6BGrbyQ2mYV11W0U8j5mBhd14dd3B0A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-string-parser": "^7.27.1",
        "@babel/helper-validator-identifier": "^7.28.5"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@emotion/hash": {
      "version": "0.8.0",
      "resolved": "https://registry.npmjs.org/@emotion/hash/-/hash-0.8.0.tgz",
      "integrity": "sha512-kBJtf7PH6aWwZ6fka3zQ0p6SBYzx4fl1LoZXE2RrnYST9Xljm7WfKJrU4g/Xr3Beg72MLrp1AWNUmuYJTL7Cow==",
      "license": "MIT"
    },
    "node_modules/@emotion/unitless": {
      "version": "0.7.5",
      "resolved": "https://registry.npmjs.org/@emotion/unitless/-/unitless-0.7.5.tgz",
      "integrity": "sha512-OWORNpfjMsSSUBVrRBVGECkhWcULOAJz9ZW8uK9qgxD+87M7jHRcvh/A96XXNhXTLmKcoYSQtBEX7lHMO7YRwg==",
      "license": "MIT"
    },
    "node_modules/@esbuild/aix-ppc64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/aix-ppc64/-/aix-ppc64-0.21.5.tgz",
      "integrity": "sha512-1SDgH6ZSPTlggy1yI6+Dbkiz8xzpHJEVAlF/AM1tHPLsf5STom9rwtjE4hKAF20FfXXNTFqEYXyJNWh1GiZedQ==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "aix"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/android-arm": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/android-arm/-/android-arm-0.21.5.tgz",
      "integrity": "sha512-vCPvzSjpPHEi1siZdlvAlsPxXl7WbOVUBBAowWug4rJHb68Ox8KualB+1ocNvT5fjv6wpkX6o/iEpbDrf68zcg==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/android-arm64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/android-arm64/-/android-arm64-0.21.5.tgz",
      "integrity": "sha512-c0uX9VAUBQ7dTDCjq+wdyGLowMdtR/GoC2U5IYk/7D1H1JYC0qseD7+11iMP2mRLN9RcCMRcjC4YMclCzGwS/A==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/android-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/android-x64/-/android-x64-0.21.5.tgz",
      "integrity": "sha512-D7aPRUUNHRBwHxzxRvp856rjUHRFW1SdQATKXH2hqA0kAZb1hKmi02OpYRacl0TxIGz/ZmXWlbZgjwWYaCakTA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/darwin-arm64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/darwin-arm64/-/darwin-arm64-0.21.5.tgz",
      "integrity": "sha512-DwqXqZyuk5AiWWf3UfLiRDJ5EDd49zg6O9wclZ7kUMv2WRFr4HKjXp/5t8JZ11QbQfUS6/cRCKGwYhtNAY88kQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/darwin-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/darwin-x64/-/darwin-x64-0.21.5.tgz",
      "integrity": "sha512-se/JjF8NlmKVG4kNIuyWMV/22ZaerB+qaSi5MdrXtd6R08kvs2qCN4C09miupktDitvh8jRFflwGFBQcxZRjbw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/freebsd-arm64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/freebsd-arm64/-/freebsd-arm64-0.21.5.tgz",
      "integrity": "sha512-5JcRxxRDUJLX8JXp/wcBCy3pENnCgBR9bN6JsY4OmhfUtIHe3ZW0mawA7+RDAcMLrMIZaf03NlQiX9DGyB8h4g==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/freebsd-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/freebsd-x64/-/freebsd-x64-0.21.5.tgz",
      "integrity": "sha512-J95kNBj1zkbMXtHVH29bBriQygMXqoVQOQYA+ISs0/2l3T9/kj42ow2mpqerRBxDJnmkUDCaQT/dfNXWX/ZZCQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-arm": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-arm/-/linux-arm-0.21.5.tgz",
      "integrity": "sha512-bPb5AHZtbeNGjCKVZ9UGqGwo8EUu4cLq68E95A53KlxAPRmUyYv2D6F0uUI65XisGOL1hBP5mTronbgo+0bFcA==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-arm64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-arm64/-/linux-arm64-0.21.5.tgz",
      "integrity": "sha512-ibKvmyYzKsBeX8d8I7MH/TMfWDXBF3db4qM6sy+7re0YXya+K1cem3on9XgdT2EQGMu4hQyZhan7TeQ8XkGp4Q==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-ia32": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-ia32/-/linux-ia32-0.21.5.tgz",
      "integrity": "sha512-YvjXDqLRqPDl2dvRODYmmhz4rPeVKYvppfGYKSNGdyZkA01046pLWyRKKI3ax8fbJoK5QbxblURkwK/MWY18Tg==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-loong64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-loong64/-/linux-loong64-0.21.5.tgz",
      "integrity": "sha512-uHf1BmMG8qEvzdrzAqg2SIG/02+4/DHB6a9Kbya0XDvwDEKCoC8ZRWI5JJvNdUjtciBGFQ5PuBlpEOXQj+JQSg==",
      "cpu": [
        "loong64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-mips64el": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-mips64el/-/linux-mips64el-0.21.5.tgz",
      "integrity": "sha512-IajOmO+KJK23bj52dFSNCMsz1QP1DqM6cwLUv3W1QwyxkyIWecfafnI555fvSGqEKwjMXVLokcV5ygHW5b3Jbg==",
      "cpu": [
        "mips64el"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-ppc64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-ppc64/-/linux-ppc64-0.21.5.tgz",
      "integrity": "sha512-1hHV/Z4OEfMwpLO8rp7CvlhBDnjsC3CttJXIhBi+5Aj5r+MBvy4egg7wCbe//hSsT+RvDAG7s81tAvpL2XAE4w==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-riscv64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-riscv64/-/linux-riscv64-0.21.5.tgz",
      "integrity": "sha512-2HdXDMd9GMgTGrPWnJzP2ALSokE/0O5HhTUvWIbD3YdjME8JwvSCnNGBnTThKGEB91OZhzrJ4qIIxk/SBmyDDA==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-s390x": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-s390x/-/linux-s390x-0.21.5.tgz",
      "integrity": "sha512-zus5sxzqBJD3eXxwvjN1yQkRepANgxE9lgOW2qLnmr8ikMTphkjgXu1HR01K4FJg8h1kEEDAqDcZQtbrRnB41A==",
      "cpu": [
        "s390x"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/linux-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-x64/-/linux-x64-0.21.5.tgz",
      "integrity": "sha512-1rYdTpyv03iycF1+BhzrzQJCdOuAOtaqHTWJZCWvijKD2N5Xu0TtVC8/+1faWqcP9iBCWOmjmhoH94dH82BxPQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/netbsd-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/netbsd-x64/-/netbsd-x64-0.21.5.tgz",
      "integrity": "sha512-Woi2MXzXjMULccIwMnLciyZH4nCIMpWQAs049KEeMvOcNADVxo0UBIQPfSmxB3CWKedngg7sWZdLvLczpe0tLg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "netbsd"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/openbsd-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/openbsd-x64/-/openbsd-x64-0.21.5.tgz",
      "integrity": "sha512-HLNNw99xsvx12lFBUwoT8EVCsSvRNDVxNpjZ7bPn947b8gJPzeHWyNVhFsaerc0n3TsbOINvRP2byTZ5LKezow==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/sunos-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/sunos-x64/-/sunos-x64-0.21.5.tgz",
      "integrity": "sha512-6+gjmFpfy0BHU5Tpptkuh8+uw3mnrvgs+dSPQXQOv3ekbordwnzTVEb4qnIvQcYXq6gzkyTnoZ9dZG+D4garKg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "sunos"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/win32-arm64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-arm64/-/win32-arm64-0.21.5.tgz",
      "integrity": "sha512-Z0gOTd75VvXqyq7nsl93zwahcTROgqvuAcYDUr+vOv8uHhNSKROyU961kgtCD1e95IqPKSQKH7tBTslnS3tA8A==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/win32-ia32": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-ia32/-/win32-ia32-0.21.5.tgz",
      "integrity": "sha512-SWXFF1CL2RVNMaVs+BBClwtfZSvDgtL//G/smwAc5oVK/UPu2Gu9tIaRgFmYFFKrmg3SyAjSrElf0TiJ1v8fYA==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@esbuild/win32-x64": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-x64/-/win32-x64-0.21.5.tgz",
      "integrity": "sha512-tQd/1efJuzPC6rCFwEvLtci/xNFcTZknmXs98FYDfGE4wP9ClFV98nyKrzJKVPMhdDnjzLhdUyMX4PsQAPjwIw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@isaacs/cliui": {
      "version": "8.0.2",
      "resolved": "https://registry.npmjs.org/@isaacs/cliui/-/cliui-8.0.2.tgz",
      "integrity": "sha512-O8jcjabXaleOG9DQ0+ARXWZBTfnP4WNAqzuiJK7ll44AmxGKv/J2M4TPjxjY3znBCfvBXFzucm1twdyFybFqEA==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "string-width": "^5.1.2",
        "string-width-cjs": "npm:string-width@^4.2.0",
        "strip-ansi": "^7.0.1",
        "strip-ansi-cjs": "npm:strip-ansi@^6.0.1",
        "wrap-ansi": "^8.1.0",
        "wrap-ansi-cjs": "npm:wrap-ansi@^7.0.0"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@joshwooding/vite-plugin-react-docgen-typescript": {
      "version": "0.5.0",
      "resolved": "https://registry.npmjs.org/@joshwooding/vite-plugin-react-docgen-typescript/-/vite-plugin-react-docgen-typescript-0.5.0.tgz",
      "integrity": "sha512-qYDdL7fPwLRI+bJNurVcis+tNgJmvWjH4YTBGXTA8xMuxFrnAz6E5o35iyzyKbq5J5Lr8mJGfrR5GXl+WGwhgQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "glob": "^10.0.0",
        "magic-string": "^0.27.0",
        "react-docgen-typescript": "^2.2.2"
      },
      "peerDependencies": {
        "typescript": ">= 4.3.x",
        "vite": "^3.0.0 || ^4.0.0 || ^5.0.0 || ^6.0.0"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/@joshwooding/vite-plugin-react-docgen-typescript/node_modules/magic-string": {
      "version": "0.27.0",
      "resolved": "https://registry.npmjs.org/magic-string/-/magic-string-0.27.0.tgz",
      "integrity": "sha512-8UnnX2PeRAPZuN12svgR9j7M1uWMovg/CEnIwIG0LFkXSJJe4PdfUGiTGl8V9bsBHFUtfVINcSyYxd7q+kx9fA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/sourcemap-codec": "^1.4.13"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@jridgewell/gen-mapping": {
      "version": "0.3.13",
      "resolved": "https://registry.npmjs.org/@jridgewell/gen-mapping/-/gen-mapping-0.3.13.tgz",
      "integrity": "sha512-2kkt/7niJ6MgEPxF0bYdQ6etZaA+fQvDcLKckhy1yIQOzaoKjBBjSj63/aLVjYE3qhRt5dvM+uUyfCg6UKCBbA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/sourcemap-codec": "^1.5.0",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/remapping": {
      "version": "2.3.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/remapping/-/remapping-2.3.5.tgz",
      "integrity": "sha512-LI9u/+laYG4Ds1TDKSJW2YPrIlcVYOwi2fUC6xB43lueCjgxV4lffOCZCtYFiH6TNOX+tQKXx97T4IKHbhyHEQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.5",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/resolve-uri": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/@jridgewell/resolve-uri/-/resolve-uri-3.1.2.tgz",
      "integrity": "sha512-bRISgCIjP20/tbWSPWMEi54QVPRZExkuD9lJL+UIxUKtwVJA8wW1Trb1jMs1RFXo1CBTNZ/5hpC9QvmKWdopKw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@jridgewell/source-map": {
      "version": "0.3.11",
      "resolved": "https://registry.npmjs.org/@jridgewell/source-map/-/source-map-0.3.11.tgz",
      "integrity": "sha512-ZMp1V8ZFcPG5dIWnQLr3NSI1MiCU7UETdS/A0G8V/XWHvJv3ZsFqutJn1Y5RPmAPX6F3BiE397OqveU/9NCuIA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.5",
        "@jridgewell/trace-mapping": "^0.3.25"
      }
    },
    "node_modules/@jridgewell/sourcemap-codec": {
      "version": "1.5.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/sourcemap-codec/-/sourcemap-codec-1.5.5.tgz",
      "integrity": "sha512-cYQ9310grqxueWbl+WuIUIaiUaDcj7WOq5fVhEljNVgRfOUhY9fy2zTvfoqWsnebh8Sl70VScFbICvJnLKB0Og==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@jridgewell/trace-mapping": {
      "version": "0.3.31",
      "resolved": "https://registry.npmjs.org/@jridgewell/trace-mapping/-/trace-mapping-0.3.31.tgz",
      "integrity": "sha512-zzNR+SdQSDJzc8joaeP8QQoCQr8NuYx2dIIytl1QeBEZHJ9uW6hebsrYgbz8hJwUQao3TWCMtmfV8Nu1twOLAw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/resolve-uri": "^3.1.0",
        "@jridgewell/sourcemap-codec": "^1.4.14"
      }
    },
    "node_modules/@mdx-js/react": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/@mdx-js/react/-/react-3.1.1.tgz",
      "integrity": "sha512-f++rKLQgUVYDAtECQ6fn/is15GkEH9+nZPM3MS0RcxVqoTfawHvDlSCH7JbMhAM6uJ32v3eXLvLmLvjGu7PTQw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@types/mdx": "^2.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/unified"
      },
      "peerDependencies": {
        "@types/react": ">=16",
        "react": ">=16"
      }
    },
    "node_modules/@pkgjs/parseargs": {
      "version": "0.11.0",
      "resolved": "https://registry.npmjs.org/@pkgjs/parseargs/-/parseargs-0.11.0.tgz",
      "integrity": "sha512-+1VkjdD0QBLPodGrJUeqarH8VAIvQODIbwh9XpP5Syisf7YoQgsJKPNFoqqLQlu+VQ/tVSshMR6loPMn8U+dPg==",
      "dev": true,
      "license": "MIT",
      "optional": true,
      "engines": {
        "node": ">=14"
      }
    },
    "node_modules/@playwright/test": {
      "version": "1.58.2",
      "resolved": "https://registry.npmjs.org/@playwright/test/-/test-1.58.2.tgz",
      "integrity": "sha512-akea+6bHYBBfA9uQqSYmlJXn61cTa+jbO87xVLCWbTqbWadRVmhxlXATaOjOgcBaWU4ePo0wB41KMFv3o35IXA==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "playwright": "1.58.2"
      },
      "bin": {
        "playwright": "cli.js"
      },
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@rc-component/async-validator": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/@rc-component/async-validator/-/async-validator-5.1.0.tgz",
      "integrity": "sha512-n4HcR5siNUXRX23nDizbZBQPO0ZM/5oTtmKZ6/eqL0L2bo747cklFdZGRN2f+c9qWGICwDzrhW0H7tE9PptdcA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.24.4"
      },
      "engines": {
        "node": ">=14.x"
      }
    },
    "node_modules/@rc-component/color-picker": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/@rc-component/color-picker/-/color-picker-2.0.1.tgz",
      "integrity": "sha512-WcZYwAThV/b2GISQ8F+7650r5ZZJ043E57aVBFkQ+kSY4C6wdofXgB0hBx+GPGpIU0Z81eETNoDUJMr7oy/P8Q==",
      "license": "MIT",
      "dependencies": {
        "@ant-design/fast-color": "^2.0.6",
        "@babel/runtime": "^7.23.6",
        "classnames": "^2.2.6",
        "rc-util": "^5.38.1"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/@rc-component/context": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/@rc-component/context/-/context-1.4.0.tgz",
      "integrity": "sha512-kFcNxg9oLRMoL3qki0OMxK+7g5mypjgaaJp/pkOis/6rVxma9nJBF/8kCIuTYHUQNr0ii7MxqE33wirPZLJQ2w==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "rc-util": "^5.27.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/@rc-component/mini-decimal": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/@rc-component/mini-decimal/-/mini-decimal-1.1.3.tgz",
      "integrity": "sha512-bk/FJ09fLf+NLODMAFll6CfYrHPBioTedhW6lxDBuuWucJEqFUd4l/D/5JgIi3dina6sYahB8iuPAZTNz2pMxw==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.18.0"
      },
      "engines": {
        "node": ">=8.x"
      }
    },
    "node_modules/@rc-component/mutate-observer": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/@rc-component/mutate-observer/-/mutate-observer-1.1.0.tgz",
      "integrity": "sha512-QjrOsDXQusNwGZPf4/qRQasg7UFEj06XiCJ8iuiq/Io7CrHrgVi6Uuetw60WAMG1799v+aM8kyc+1L/GBbHSlw==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.18.0",
        "classnames": "^2.3.2",
        "rc-util": "^5.24.4"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/@rc-component/portal": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/@rc-component/portal/-/portal-1.1.2.tgz",
      "integrity": "sha512-6f813C0IsasTZms08kfA8kPAGxbbkYToa8ALaiDIGGECU4i9hj8Plgbx0sNJDrey3EtHO30hmdaxtT0138xZcg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.18.0",
        "classnames": "^2.3.2",
        "rc-util": "^5.24.4"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/@rc-component/qrcode": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/@rc-component/qrcode/-/qrcode-1.1.1.tgz",
      "integrity": "sha512-LfLGNymzKdUPjXUbRP+xOhIWY4jQ+YMj5MmWAcgcAq1Ij8XP7tRmAXqyuv96XvLUBE/5cA8hLFl9eO1JQMujrA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.24.7"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/@rc-component/tour": {
      "version": "1.15.1",
      "resolved": "https://registry.npmjs.org/@rc-component/tour/-/tour-1.15.1.tgz",
      "integrity": "sha512-Tr2t7J1DKZUpfJuDZWHxyxWpfmj8EZrqSgyMZ+BCdvKZ6r1UDsfU46M/iWAAFBy961Ssfom2kv5f3UcjIL2CmQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.18.0",
        "@rc-component/portal": "^1.0.0-9",
        "@rc-component/trigger": "^2.0.0",
        "classnames": "^2.3.2",
        "rc-util": "^5.24.4"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/@rc-component/trigger": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/@rc-component/trigger/-/trigger-2.3.1.tgz",
      "integrity": "sha512-ORENF39PeXTzM+gQEshuk460Z8N4+6DkjpxlpE7Q3gYy1iBpLrx0FOJz3h62ryrJZ/3zCAUIkT1Pb/8hHWpb3A==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.23.2",
        "@rc-component/portal": "^1.1.0",
        "classnames": "^2.3.2",
        "rc-motion": "^2.0.0",
        "rc-resize-observer": "^1.3.1",
        "rc-util": "^5.44.0"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/@redocly/ajv": {
      "version": "8.11.2",
      "resolved": "https://registry.npmjs.org/@redocly/ajv/-/ajv-8.11.2.tgz",
      "integrity": "sha512-io1JpnwtIcvojV7QKDUSIuMN/ikdOUd1ReEnUnMKGfDVridQZ31J0MmIuqwuRjWDZfmvr+Q0MqCcfHM2gTivOg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.1",
        "json-schema-traverse": "^1.0.0",
        "require-from-string": "^2.0.2",
        "uri-js-replace": "^1.0.1"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/@redocly/config": {
      "version": "0.22.0",
      "resolved": "https://registry.npmjs.org/@redocly/config/-/config-0.22.0.tgz",
      "integrity": "sha512-gAy93Ddo01Z3bHuVdPWfCwzgfaYgMdaZPcfL7JZ7hWJoK9V0lXDbigTWkhiPFAaLWzbOJ+kbUQG1+XwIm0KRGQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@redocly/openapi-core": {
      "version": "1.34.11",
      "resolved": "https://registry.npmjs.org/@redocly/openapi-core/-/openapi-core-1.34.11.tgz",
      "integrity": "sha512-V09ayfnb5GyysmvARbt+voFZAjGcf7hSYxOYxSkCc4fbH/DTfq5YWoec8cflvmHHqyIFbqvmGKmYFzqhr9zxDg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@redocly/ajv": "8.11.2",
        "@redocly/config": "0.22.0",
        "colorette": "1.4.0",
        "https-proxy-agent": "7.0.6",
        "js-levenshtein": "1.1.6",
        "js-yaml": "4.1.1",
        "minimatch": "5.1.9",
        "pluralize": "8.0.0",
        "yaml-ast-parser": "0.0.43"
      },
      "engines": {
        "node": ">=18.17.0",
        "npm": ">=9.5.0"
      }
    },
    "node_modules/@redocly/openapi-core/node_modules/minimatch": {
      "version": "5.1.9",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-5.1.9.tgz",
      "integrity": "sha512-7o1wEA2RyMP7Iu7GNba9vc0RWWGACJOCZBJX2GJWip0ikV+wcOsgVuY9uE8CPiyQhkGFSlhuSkZPavN7u1c2Fw==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "brace-expansion": "^2.0.1"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/@remix-run/router": {
      "version": "1.23.2",
      "resolved": "https://registry.npmjs.org/@remix-run/router/-/router-1.23.2.tgz",
      "integrity": "sha512-Ic6m2U/rMjTkhERIa/0ZtXJP17QUi2CbWE7cqx4J58M8aA3QTfW+2UlQ4psvTX9IO1RfNVhK3pcpdjej7L+t2w==",
      "license": "MIT",
      "engines": {
        "node": ">=14.0.0"
      }
    },
    "node_modules/@rolldown/pluginutils": {
      "version": "1.0.0-beta.27",
      "resolved": "https://registry.npmjs.org/@rolldown/pluginutils/-/pluginutils-1.0.0-beta.27.tgz",
      "integrity": "sha512-+d0F4MKMCbeVUJwG96uQ4SgAznZNSq93I3V+9NHA4OpvqG8mRCpGdKmK8l/dl02h2CCDHwW2FqilnTyDcAnqjA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@rollup/plugin-node-resolve": {
      "version": "15.3.1",
      "resolved": "https://registry.npmjs.org/@rollup/plugin-node-resolve/-/plugin-node-resolve-15.3.1.tgz",
      "integrity": "sha512-tgg6b91pAybXHJQMAAwW9VuWBO6Thi+q7BCNARLwSqlmsHz0XYURtGvh/AuwSADXSI4h/2uHbs7s4FzlZDGSGA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@rollup/pluginutils": "^5.0.1",
        "@types/resolve": "1.20.2",
        "deepmerge": "^4.2.2",
        "is-module": "^1.0.0",
        "resolve": "^1.22.1"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "rollup": "^2.78.0||^3.0.0||^4.0.0"
      },
      "peerDependenciesMeta": {
        "rollup": {
          "optional": true
        }
      }
    },
    "node_modules/@rollup/plugin-node-resolve/node_modules/@types/resolve": {
      "version": "1.20.2",
      "resolved": "https://registry.npmjs.org/@types/resolve/-/resolve-1.20.2.tgz",
      "integrity": "sha512-60BCwRFOZCQhDncwQdxxeOEEkbc5dIMccYLwbxsS4TUNeVECQ/pBJ0j09mrHOl/JJvpRPGwO9SvE4nR2Nb/a4Q==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@rollup/plugin-terser": {
      "version": "0.4.4",
      "resolved": "https://registry.npmjs.org/@rollup/plugin-terser/-/plugin-terser-0.4.4.tgz",
      "integrity": "sha512-XHeJC5Bgvs8LfukDwWZp7yeqin6ns8RTl2B9avbejt6tZqsqvVoWI7ZTQrcNsfKEDWBTnTxM8nMDkO2IFFbd0A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "serialize-javascript": "^6.0.1",
        "smob": "^1.0.0",
        "terser": "^5.17.4"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "rollup": "^2.0.0||^3.0.0||^4.0.0"
      },
      "peerDependenciesMeta": {
        "rollup": {
          "optional": true
        }
      }
    },
    "node_modules/@rollup/pluginutils": {
      "version": "5.3.0",
      "resolved": "https://registry.npmjs.org/@rollup/pluginutils/-/pluginutils-5.3.0.tgz",
      "integrity": "sha512-5EdhGZtnu3V88ces7s53hhfK5KSASnJZv8Lulpc04cWO3REESroJXg73DFsOmgbU2BhwV0E20bu2IDZb3VKW4Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@types/estree": "^1.0.0",
        "estree-walker": "^2.0.2",
        "picomatch": "^4.0.2"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "rollup": "^1.20.0||^2.0.0||^3.0.0||^4.0.0"
      },
      "peerDependenciesMeta": {
        "rollup": {
          "optional": true
        }
      }
    },
    "node_modules/@rollup/rollup-android-arm-eabi": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm-eabi/-/rollup-android-arm-eabi-4.59.0.tgz",
      "integrity": "sha512-upnNBkA6ZH2VKGcBj9Fyl9IGNPULcjXRlg0LLeaioQWueH30p6IXtJEbKAgvyv+mJaMxSm1l6xwDXYjpEMiLMg==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-android-arm64": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm64/-/rollup-android-arm64-4.59.0.tgz",
      "integrity": "sha512-hZ+Zxj3SySm4A/DylsDKZAeVg0mvi++0PYVceVyX7hemkw7OreKdCvW2oQ3T1FMZvCaQXqOTHb8qmBShoqk69Q==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-darwin-arm64": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-darwin-arm64/-/rollup-darwin-arm64-4.59.0.tgz",
      "integrity": "sha512-W2Psnbh1J8ZJw0xKAd8zdNgF9HRLkdWwwdWqubSVk0pUuQkoHnv7rx4GiF9rT4t5DIZGAsConRE3AxCdJ4m8rg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ]
    },
    "node_modules/@rollup/rollup-darwin-x64": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-darwin-x64/-/rollup-darwin-x64-4.59.0.tgz",
      "integrity": "sha512-ZW2KkwlS4lwTv7ZVsYDiARfFCnSGhzYPdiOU4IM2fDbL+QGlyAbjgSFuqNRbSthybLbIJ915UtZBtmuLrQAT/w==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ]
    },
    "node_modules/@rollup/rollup-freebsd-arm64": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-freebsd-arm64/-/rollup-freebsd-arm64-4.59.0.tgz",
      "integrity": "sha512-EsKaJ5ytAu9jI3lonzn3BgG8iRBjV4LxZexygcQbpiU0wU0ATxhNVEpXKfUa0pS05gTcSDMKpn3Sx+QB9RlTTA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ]
    },
    "node_modules/@rollup/rollup-freebsd-x64": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-freebsd-x64/-/rollup-freebsd-x64-4.59.0.tgz",
      "integrity": "sha512-d3DuZi2KzTMjImrxoHIAODUZYoUUMsuUiY4SRRcJy6NJoZ6iIqWnJu9IScV9jXysyGMVuW+KNzZvBLOcpdl3Vg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ]
    },
    "node_modules/@rollup/rollup-linux-arm-gnueabihf": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-arm-gnueabihf/-/rollup-linux-arm-gnueabihf-4.59.0.tgz",
      "integrity": "sha512-t4ONHboXi/3E0rT6OZl1pKbl2Vgxf9vJfWgmUoCEVQVxhW6Cw/c8I6hbbu7DAvgp82RKiH7TpLwxnJeKv2pbsw==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-arm-musleabihf": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-arm-musleabihf/-/rollup-linux-arm-musleabihf-4.59.0.tgz",
      "integrity": "sha512-CikFT7aYPA2ufMD086cVORBYGHffBo4K8MQ4uPS/ZnY54GKj36i196u8U+aDVT2LX4eSMbyHtyOh7D7Zvk2VvA==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-arm64-gnu": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-arm64-gnu/-/rollup-linux-arm64-gnu-4.59.0.tgz",
      "integrity": "sha512-jYgUGk5aLd1nUb1CtQ8E+t5JhLc9x5WdBKew9ZgAXg7DBk0ZHErLHdXM24rfX+bKrFe+Xp5YuJo54I5HFjGDAA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-arm64-musl": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-arm64-musl/-/rollup-linux-arm64-musl-4.59.0.tgz",
      "integrity": "sha512-peZRVEdnFWZ5Bh2KeumKG9ty7aCXzzEsHShOZEFiCQlDEepP1dpUl/SrUNXNg13UmZl+gzVDPsiCwnV1uI0RUA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-loong64-gnu": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-loong64-gnu/-/rollup-linux-loong64-gnu-4.59.0.tgz",
      "integrity": "sha512-gbUSW/97f7+r4gHy3Jlup8zDG190AuodsWnNiXErp9mT90iCy9NKKU0Xwx5k8VlRAIV2uU9CsMnEFg/xXaOfXg==",
      "cpu": [
        "loong64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-loong64-musl": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-loong64-musl/-/rollup-linux-loong64-musl-4.59.0.tgz",
      "integrity": "sha512-yTRONe79E+o0FWFijasoTjtzG9EBedFXJMl888NBEDCDV9I2wGbFFfJQQe63OijbFCUZqxpHz1GzpbtSFikJ4Q==",
      "cpu": [
        "loong64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-ppc64-gnu": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-ppc64-gnu/-/rollup-linux-ppc64-gnu-4.59.0.tgz",
      "integrity": "sha512-sw1o3tfyk12k3OEpRddF68a1unZ5VCN7zoTNtSn2KndUE+ea3m3ROOKRCZxEpmT9nsGnogpFP9x6mnLTCaoLkA==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-ppc64-musl": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-ppc64-musl/-/rollup-linux-ppc64-musl-4.59.0.tgz",
      "integrity": "sha512-+2kLtQ4xT3AiIxkzFVFXfsmlZiG5FXYW7ZyIIvGA7Bdeuh9Z0aN4hVyXS/G1E9bTP/vqszNIN/pUKCk/BTHsKA==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-riscv64-gnu": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-riscv64-gnu/-/rollup-linux-riscv64-gnu-4.59.0.tgz",
      "integrity": "sha512-NDYMpsXYJJaj+I7UdwIuHHNxXZ/b/N2hR15NyH3m2qAtb/hHPA4g4SuuvrdxetTdndfj9b1WOmy73kcPRoERUg==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-riscv64-musl": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-riscv64-musl/-/rollup-linux-riscv64-musl-4.59.0.tgz",
      "integrity": "sha512-nLckB8WOqHIf1bhymk+oHxvM9D3tyPndZH8i8+35p/1YiVoVswPid2yLzgX7ZJP0KQvnkhM4H6QZ5m0LzbyIAg==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-s390x-gnu": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-s390x-gnu/-/rollup-linux-s390x-gnu-4.59.0.tgz",
      "integrity": "sha512-oF87Ie3uAIvORFBpwnCvUzdeYUqi2wY6jRFWJAy1qus/udHFYIkplYRW+wo+GRUP4sKzYdmE1Y3+rY5Gc4ZO+w==",
      "cpu": [
        "s390x"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-x64-gnu": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-x64-gnu/-/rollup-linux-x64-gnu-4.59.0.tgz",
      "integrity": "sha512-3AHmtQq/ppNuUspKAlvA8HtLybkDflkMuLK4DPo77DfthRb71V84/c4MlWJXixZz4uruIH4uaa07IqoAkG64fg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-linux-x64-musl": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-linux-x64-musl/-/rollup-linux-x64-musl-4.59.0.tgz",
      "integrity": "sha512-2UdiwS/9cTAx7qIUZB/fWtToJwvt0Vbo0zmnYt7ED35KPg13Q0ym1g442THLC7VyI6JfYTP4PiSOWyoMdV2/xg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ]
    },
    "node_modules/@rollup/rollup-openbsd-x64": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-openbsd-x64/-/rollup-openbsd-x64-4.59.0.tgz",
      "integrity": "sha512-M3bLRAVk6GOwFlPTIxVBSYKUaqfLrn8l0psKinkCFxl4lQvOSz8ZrKDz2gxcBwHFpci0B6rttydI4IpS4IS/jQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ]
    },
    "node_modules/@rollup/rollup-openharmony-arm64": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-openharmony-arm64/-/rollup-openharmony-arm64-4.59.0.tgz",
      "integrity": "sha512-tt9KBJqaqp5i5HUZzoafHZX8b5Q2Fe7UjYERADll83O4fGqJ49O1FsL6LpdzVFQcpwvnyd0i+K/VSwu/o/nWlA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openharmony"
      ]
    },
    "node_modules/@rollup/rollup-win32-arm64-msvc": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-win32-arm64-msvc/-/rollup-win32-arm64-msvc-4.59.0.tgz",
      "integrity": "sha512-V5B6mG7OrGTwnxaNUzZTDTjDS7F75PO1ae6MJYdiMu60sq0CqN5CVeVsbhPxalupvTX8gXVSU9gq+Rx1/hvu6A==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@rollup/rollup-win32-ia32-msvc": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-win32-ia32-msvc/-/rollup-win32-ia32-msvc-4.59.0.tgz",
      "integrity": "sha512-UKFMHPuM9R0iBegwzKF4y0C4J9u8C6MEJgFuXTBerMk7EJ92GFVFYBfOZaSGLu6COf7FxpQNqhNS4c4icUPqxA==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@rollup/rollup-win32-x64-gnu": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-win32-x64-gnu/-/rollup-win32-x64-gnu-4.59.0.tgz",
      "integrity": "sha512-laBkYlSS1n2L8fSo1thDNGrCTQMmxjYY5G0WFWjFFYZkKPjsMBsgJfGf4TLxXrF6RyhI60L8TMOjBMvXiTcxeA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@rollup/rollup-win32-x64-msvc": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-win32-x64-msvc/-/rollup-win32-x64-msvc-4.59.0.tgz",
      "integrity": "sha512-2HRCml6OztYXyJXAvdDXPKcawukWY2GpR5/nxKp4iBgiO3wcoEGkAaqctIbZcNB6KlUQBIqt8VYkNSj2397EfA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ]
    },
    "node_modules/@sentry-internal/browser-utils": {
      "version": "8.55.0",
      "resolved": "https://registry.npmjs.org/@sentry-internal/browser-utils/-/browser-utils-8.55.0.tgz",
      "integrity": "sha512-ROgqtQfpH/82AQIpESPqPQe0UyWywKJsmVIqi3c5Fh+zkds5LUxnssTj3yNd1x+kxaPDVB023jAP+3ibNgeNDw==",
      "license": "MIT",
      "dependencies": {
        "@sentry/core": "8.55.0"
      },
      "engines": {
        "node": ">=14.18"
      }
    },
    "node_modules/@sentry-internal/feedback": {
      "version": "8.55.0",
      "resolved": "https://registry.npmjs.org/@sentry-internal/feedback/-/feedback-8.55.0.tgz",
      "integrity": "sha512-cP3BD/Q6pquVQ+YL+rwCnorKuTXiS9KXW8HNKu4nmmBAyf7urjs+F6Hr1k9MXP5yQ8W3yK7jRWd09Yu6DHWOiw==",
      "license": "MIT",
      "dependencies": {
        "@sentry/core": "8.55.0"
      },
      "engines": {
        "node": ">=14.18"
      }
    },
    "node_modules/@sentry-internal/replay": {
      "version": "8.55.0",
      "resolved": "https://registry.npmjs.org/@sentry-internal/replay/-/replay-8.55.0.tgz",
      "integrity": "sha512-roCDEGkORwolxBn8xAKedybY+Jlefq3xYmgN2fr3BTnsXjSYOPC7D1/mYqINBat99nDtvgFvNfRcZPiwwZ1hSw==",
      "license": "MIT",
      "dependencies": {
        "@sentry-internal/browser-utils": "8.55.0",
        "@sentry/core": "8.55.0"
      },
      "engines": {
        "node": ">=14.18"
      }
    },
    "node_modules/@sentry-internal/replay-canvas": {
      "version": "8.55.0",
      "resolved": "https://registry.npmjs.org/@sentry-internal/replay-canvas/-/replay-canvas-8.55.0.tgz",
      "integrity": "sha512-nIkfgRWk1091zHdu4NbocQsxZF1rv1f7bbp3tTIlZYbrH62XVZosx5iHAuZG0Zc48AETLE7K4AX9VGjvQj8i9w==",
      "license": "MIT",
      "dependencies": {
        "@sentry-internal/replay": "8.55.0",
        "@sentry/core": "8.55.0"
      },
      "engines": {
        "node": ">=14.18"
      }
    },
    "node_modules/@sentry/browser": {
      "version": "8.55.0",
      "resolved": "https://registry.npmjs.org/@sentry/browser/-/browser-8.55.0.tgz",
      "integrity": "sha512-1A31mCEWCjaMxJt6qGUK+aDnLDcK6AwLAZnqpSchNysGni1pSn1RWSmk9TBF8qyTds5FH8B31H480uxMPUJ7Cw==",
      "license": "MIT",
      "dependencies": {
        "@sentry-internal/browser-utils": "8.55.0",
        "@sentry-internal/feedback": "8.55.0",
        "@sentry-internal/replay": "8.55.0",
        "@sentry-internal/replay-canvas": "8.55.0",
        "@sentry/core": "8.55.0"
      },
      "engines": {
        "node": ">=14.18"
      }
    },
    "node_modules/@sentry/core": {
      "version": "8.55.0",
      "resolved": "https://registry.npmjs.org/@sentry/core/-/core-8.55.0.tgz",
      "integrity": "sha512-6g7jpbefjHYs821Z+EBJ8r4Z7LT5h80YSWRJaylGS4nW5W5Z2KXzpdnyFarv37O7QjauzVC2E+PABmpkw5/JGA==",
      "license": "MIT",
      "engines": {
        "node": ">=14.18"
      }
    },
    "node_modules/@sentry/react": {
      "version": "8.55.0",
      "resolved": "https://registry.npmjs.org/@sentry/react/-/react-8.55.0.tgz",
      "integrity": "sha512-/qNBvFLpvSa/Rmia0jpKfJdy16d4YZaAnH/TuKLAtm0BWlsPQzbXCU4h8C5Hsst0Do0zG613MEtEmWpWrVOqWA==",
      "license": "MIT",
      "dependencies": {
        "@sentry/browser": "8.55.0",
        "@sentry/core": "8.55.0",
        "hoist-non-react-statics": "^3.3.2"
      },
      "engines": {
        "node": ">=14.18"
      },
      "peerDependencies": {
        "react": "^16.14.0 || 17.x || 18.x || 19.x"
      }
    },
    "node_modules/@storybook/addon-actions": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/addon-actions/-/addon-actions-8.6.14.tgz",
      "integrity": "sha512-mDQxylxGGCQSK7tJPkD144J8jWh9IU9ziJMHfB84PKpI/V5ZgqMDnpr2bssTrUaGDqU5e1/z8KcRF+Melhs9pQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@storybook/global": "^5.0.0",
        "@types/uuid": "^9.0.1",
        "dequal": "^2.0.2",
        "polished": "^4.2.2",
        "uuid": "^9.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.14"
      }
    },
    "node_modules/@storybook/addon-backgrounds": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/addon-backgrounds/-/addon-backgrounds-8.6.14.tgz",
      "integrity": "sha512-l9xS8qWe5n4tvMwth09QxH2PmJbCctEvBAc1tjjRasAfrd69f7/uFK4WhwJAstzBTNgTc8VXI4w8ZR97i1sFbg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@storybook/global": "^5.0.0",
        "memoizerific": "^1.11.3",
        "ts-dedent": "^2.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.14"
      }
    },
    "node_modules/@storybook/addon-controls": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/addon-controls/-/addon-controls-8.6.14.tgz",
      "integrity": "sha512-IiQpkNJdiRyA4Mq9mzjZlvQugL/aE7hNgVxBBGPiIZG6wb6Ht9hNnBYpap5ZXXFKV9p2qVI0FZK445ONmAa+Cw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@storybook/global": "^5.0.0",
        "dequal": "^2.0.2",
        "ts-dedent": "^2.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.14"
      }
    },
    "node_modules/@storybook/addon-docs": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/addon-docs/-/addon-docs-8.6.14.tgz",
      "integrity": "sha512-Obpd0OhAF99JyU5pp5ci17YmpcQtMNgqW2pTXV8jAiiipWpwO++hNDeQmLmlSXB399XjtRDOcDVkoc7rc6JzdQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@mdx-js/react": "^3.0.0",
        "@storybook/blocks": "8.6.14",
        "@storybook/csf-plugin": "8.6.14",
        "@storybook/react-dom-shim": "8.6.14",
        "react": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0",
        "react-dom": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0",
        "ts-dedent": "^2.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.14"
      }
    },
    "node_modules/@storybook/addon-essentials": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/addon-essentials/-/addon-essentials-8.6.14.tgz",
      "integrity": "sha512-5ZZSHNaW9mXMOFkoPyc3QkoNGdJHETZydI62/OASR0lmPlJ1065TNigEo5dJddmZNn0/3bkE8eKMAzLnO5eIdA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@storybook/addon-actions": "8.6.14",
        "@storybook/addon-backgrounds": "8.6.14",
        "@storybook/addon-controls": "8.6.14",
        "@storybook/addon-docs": "8.6.14",
        "@storybook/addon-highlight": "8.6.14",
        "@storybook/addon-measure": "8.6.14",
        "@storybook/addon-outline": "8.6.14",
        "@storybook/addon-toolbars": "8.6.14",
        "@storybook/addon-viewport": "8.6.14",
        "ts-dedent": "^2.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.14"
      }
    },
    "node_modules/@storybook/addon-highlight": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/addon-highlight/-/addon-highlight-8.6.14.tgz",
      "integrity": "sha512-4H19OJlapkofiE9tM6K/vsepf4ir9jMm9T+zw5L85blJZxhKZIbJ6FO0TCG9PDc4iPt3L6+aq5B0X29s9zicNQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@storybook/global": "^5.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.14"
      }
    },
    "node_modules/@storybook/addon-measure": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/addon-measure/-/addon-measure-8.6.14.tgz",
      "integrity": "sha512-1Tlyb72NX8aAqm6I6OICsUuGOP6hgnXcuFlXucyhKomPa6j3Eu2vKu561t/f0oGtAK2nO93Z70kVaEh5X+vaGw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@storybook/global": "^5.0.0",
        "tiny-invariant": "^1.3.1"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.14"
      }
    },
    "node_modules/@storybook/addon-outline": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/addon-outline/-/addon-outline-8.6.14.tgz",
      "integrity": "sha512-CW857JvN6OxGWElqjlzJO2S69DHf+xO3WsEfT5mT3ZtIjmsvRDukdWfDU9bIYUFyA2lFvYjncBGjbK+I91XR7w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@storybook/global": "^5.0.0",
        "ts-dedent": "^2.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.14"
      }
    },
    "node_modules/@storybook/addon-toolbars": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/addon-toolbars/-/addon-toolbars-8.6.14.tgz",
      "integrity": "sha512-W/wEXT8h3VyZTVfWK/84BAcjAxTdtRiAkT2KAN0nbSHxxB5KEM1MjKpKu2upyzzMa3EywITqbfy4dP6lpkVTwQ==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.14"
      }
    },
    "node_modules/@storybook/addon-viewport": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/addon-viewport/-/addon-viewport-8.6.14.tgz",
      "integrity": "sha512-gNzVQbMqRC+/4uQTPI2ZrWuRHGquTMZpdgB9DrD88VTEjNudP+J6r8myLfr2VvGksBbUMHkGHMXHuIhrBEnXYA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "memoizerific": "^1.11.3"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.14"
      }
    },
    "node_modules/@storybook/blocks": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/blocks/-/blocks-8.6.14.tgz",
      "integrity": "sha512-rBMHAfA39AGHgkrDze4RmsnQTMw1ND5fGWobr9pDcJdnDKWQWNRD7Nrlxj0gFlN3n4D9lEZhWGdFrCbku7FVAQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@storybook/icons": "^1.2.12",
        "ts-dedent": "^2.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "react": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0",
        "react-dom": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0",
        "storybook": "^8.6.14"
      },
      "peerDependenciesMeta": {
        "react": {
          "optional": true
        },
        "react-dom": {
          "optional": true
        }
      }
    },
    "node_modules/@storybook/builder-vite": {
      "version": "8.6.18",
      "resolved": "https://registry.npmjs.org/@storybook/builder-vite/-/builder-vite-8.6.18.tgz",
      "integrity": "sha512-XLqnOv4C36jlTd4uC8xpWBxv+7GV4/05zWJ0wAcU4qflorropUTirt4UQPGkwIzi+BVAhs9pJj+m4k0IWJtpHg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@storybook/csf-plugin": "8.6.18",
        "browser-assert": "^1.2.1",
        "ts-dedent": "^2.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.18",
        "vite": "^4.0.0 || ^5.0.0 || ^6.0.0"
      }
    },
    "node_modules/@storybook/builder-vite/node_modules/@storybook/csf-plugin": {
      "version": "8.6.18",
      "resolved": "https://registry.npmjs.org/@storybook/csf-plugin/-/csf-plugin-8.6.18.tgz",
      "integrity": "sha512-x1ioz/L0CwaelCkHci3P31YtvwayN3FBftvwQOPbvRh9qeb4Cpz5IdVDmyvSxxYwXN66uAORNoqgjTi7B4/y5Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "unplugin": "^1.3.1"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.18"
      }
    },
    "node_modules/@storybook/components": {
      "version": "8.6.18",
      "resolved": "https://registry.npmjs.org/@storybook/components/-/components-8.6.18.tgz",
      "integrity": "sha512-55yViiZzPS/cPBuOeW4QGxGqrusjXVyxuknmbYCIwDtFyyvI/CgbjXRHdxNBaIjz+IlftxvBmmSaOqFG5+/dkA==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.2.0 || ^8.3.0-0 || ^8.4.0-0 || ^8.5.0-0 || ^8.6.0-0"
      }
    },
    "node_modules/@storybook/core": {
      "version": "8.6.18",
      "resolved": "https://registry.npmjs.org/@storybook/core/-/core-8.6.18.tgz",
      "integrity": "sha512-dRBP2TnX6fGdS0T2mXBHjkS/3Nlu1ra1huovZVFuM67CYMzrhM/3hX/zru1vWSC5rqY93ZaAhjMciPW4pK5mMQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@storybook/theming": "8.6.18",
        "better-opn": "^3.0.2",
        "browser-assert": "^1.2.1",
        "esbuild": "^0.18.0 || ^0.19.0 || ^0.20.0 || ^0.21.0 || ^0.22.0 || ^0.23.0 || ^0.24.0 || ^0.25.0",
        "esbuild-register": "^3.5.0",
        "jsdoc-type-pratt-parser": "^4.0.0",
        "process": "^0.11.10",
        "recast": "^0.23.5",
        "semver": "^7.6.2",
        "util": "^0.12.5",
        "ws": "^8.2.3"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "prettier": "^2 || ^3"
      },
      "peerDependenciesMeta": {
        "prettier": {
          "optional": true
        }
      }
    },
    "node_modules/@storybook/core/node_modules/semver": {
      "version": "7.7.4",
      "resolved": "https://registry.npmjs.org/semver/-/semver-7.7.4.tgz",
      "integrity": "sha512-vFKC2IEtQnVhpT78h1Yp8wzwrf8CM+MzKMHGJZfBtzhZNycRFnXsHk6E5TxIkkMsgNS7mdX3AGB7x2QM2di4lA==",
      "dev": true,
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/@storybook/csf-plugin": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/csf-plugin/-/csf-plugin-8.6.14.tgz",
      "integrity": "sha512-dErtc9teAuN+eelN8FojzFE635xlq9cNGGGEu0WEmMUQ4iJ8pingvBO1N8X3scz4Ry7KnxX++NNf3J3gpxS8qQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "unplugin": "^1.3.1"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.6.14"
      }
    },
    "node_modules/@storybook/global": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/@storybook/global/-/global-5.0.0.tgz",
      "integrity": "sha512-FcOqPAXACP0I3oJ/ws6/rrPT9WGhu915Cg8D02a9YxLo0DE9zI+a9A5gRGvmQ09fiWPukqI8ZAEoQEdWUKMQdQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@storybook/icons": {
      "version": "1.6.0",
      "resolved": "https://registry.npmjs.org/@storybook/icons/-/icons-1.6.0.tgz",
      "integrity": "sha512-hcFZIjW8yQz8O8//2WTIXylm5Xsgc+lW9ISLgUk1xGmptIJQRdlhVIXCpSyLrQaaRiyhQRaVg7l3BD9S216BHw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "react": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0-beta",
        "react-dom": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0-beta"
      }
    },
    "node_modules/@storybook/manager-api": {
      "version": "8.6.18",
      "resolved": "https://registry.npmjs.org/@storybook/manager-api/-/manager-api-8.6.18.tgz",
      "integrity": "sha512-BjIp12gEMgzFkEsgKpDIbZdnSWTZpm2dlws8WiPJCpgJtG+HWSxZ0/Ms30Au9yfwzQEKRSbV/5zpsKMGc2SIJw==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.2.0 || ^8.3.0-0 || ^8.4.0-0 || ^8.5.0-0 || ^8.6.0-0"
      }
    },
    "node_modules/@storybook/preview-api": {
      "version": "8.6.18",
      "resolved": "https://registry.npmjs.org/@storybook/preview-api/-/preview-api-8.6.18.tgz",
      "integrity": "sha512-joXRXh3GdVvzhbfIgmix1xs90p8Q/nja7AhEAC2egn5Pl7SKsIYZUCYI6UdrQANb2myg9P552LKXfPect8llKg==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.2.0 || ^8.3.0-0 || ^8.4.0-0 || ^8.5.0-0 || ^8.6.0-0"
      }
    },
    "node_modules/@storybook/react": {
      "version": "8.6.18",
      "resolved": "https://registry.npmjs.org/@storybook/react/-/react-8.6.18.tgz",
      "integrity": "sha512-BuLpzMkKtF+UCQCbi+lYVX9cdcAMG86Lu2dDn7UFkPi5HRNFq/zHPSvlz1XDgL0OYMtcqB1aoVzFzcyzUBhhjw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@storybook/components": "8.6.18",
        "@storybook/global": "^5.0.0",
        "@storybook/manager-api": "8.6.18",
        "@storybook/preview-api": "8.6.18",
        "@storybook/react-dom-shim": "8.6.18",
        "@storybook/theming": "8.6.18"
      },
      "engines": {
        "node": ">=18.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "@storybook/test": "8.6.18",
        "react": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0-beta",
        "react-dom": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0-beta",
        "storybook": "^8.6.18",
        "typescript": ">= 4.2.x"
      },
      "peerDependenciesMeta": {
        "@storybook/test": {
          "optional": true
        },
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/@storybook/react-dom-shim": {
      "version": "8.6.14",
      "resolved": "https://registry.npmjs.org/@storybook/react-dom-shim/-/react-dom-shim-8.6.14.tgz",
      "integrity": "sha512-0hixr3dOy3f3M+HBofp3jtMQMS+sqzjKNgl7Arfuj3fvjmyXOks/yGjDImySR4imPtEllvPZfhiQNlejheaInw==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "react": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0-beta",
        "react-dom": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0-beta",
        "storybook": "^8.6.14"
      }
    },
    "node_modules/@storybook/react-vite": {
      "version": "8.6.18",
      "resolved": "https://registry.npmjs.org/@storybook/react-vite/-/react-vite-8.6.18.tgz",
      "integrity": "sha512-qpSYyH2IizlEsI95MJTdIL6xpLSgiNCMoJpHu+IEqLnyvmecRR/YEZvcHalgdtawuXlimH0bAYuwIu3l8Vo6FQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@joshwooding/vite-plugin-react-docgen-typescript": "0.5.0",
        "@rollup/pluginutils": "^5.0.2",
        "@storybook/builder-vite": "8.6.18",
        "@storybook/react": "8.6.18",
        "find-up": "^5.0.0",
        "magic-string": "^0.30.0",
        "react-docgen": "^7.0.0",
        "resolve": "^1.22.8",
        "tsconfig-paths": "^4.2.0"
      },
      "engines": {
        "node": ">=18.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "@storybook/test": "8.6.18",
        "react": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0-beta",
        "react-dom": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0-beta",
        "storybook": "^8.6.18",
        "vite": "^4.0.0 || ^5.0.0 || ^6.0.0"
      },
      "peerDependenciesMeta": {
        "@storybook/test": {
          "optional": true
        }
      }
    },
    "node_modules/@storybook/react/node_modules/@storybook/react-dom-shim": {
      "version": "8.6.18",
      "resolved": "https://registry.npmjs.org/@storybook/react-dom-shim/-/react-dom-shim-8.6.18.tgz",
      "integrity": "sha512-N4xULcAWZQTUv4jy1/d346Tyb4gufuC3UaLCuU/iVSZ1brYF4OW3ANr+096btbMxY8pR/65lmtoqr5CTGwnBvA==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "react": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0-beta",
        "react-dom": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0-beta",
        "storybook": "^8.6.18"
      }
    },
    "node_modules/@storybook/theming": {
      "version": "8.6.18",
      "resolved": "https://registry.npmjs.org/@storybook/theming/-/theming-8.6.18.tgz",
      "integrity": "sha512-n6OEjEtHupa2PdTwWzRepr7cO8NkDd4rgF6BKLitRbujOspLxzMBEqdphs+QLcuiCIgf33SqmEA64QWnbSMhPw==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "storybook": "^8.2.0 || ^8.3.0-0 || ^8.4.0-0 || ^8.5.0-0 || ^8.6.0-0"
      }
    },
    "node_modules/@surma/rollup-plugin-off-main-thread": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/@surma/rollup-plugin-off-main-thread/-/rollup-plugin-off-main-thread-2.2.3.tgz",
      "integrity": "sha512-lR8q/9W7hZpMWweNiAKU7NQerBnzQQLvi8qnTDU/fxItPhtZVMbPV3lbCwjhIlNBe9Bbr5V+KHshvWmVSG9cxQ==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "ejs": "^3.1.6",
        "json5": "^2.2.0",
        "magic-string": "^0.25.0",
        "string.prototype.matchall": "^4.0.6"
      }
    },
    "node_modules/@surma/rollup-plugin-off-main-thread/node_modules/magic-string": {
      "version": "0.25.9",
      "resolved": "https://registry.npmjs.org/magic-string/-/magic-string-0.25.9.tgz",
      "integrity": "sha512-RmF0AsMzgt25qzqqLc1+MbHmhdx0ojF2Fvs4XnOqz2ZOBXzzkEwc/dJQZCYHAn7v1jbVOjAZfK8msRn4BxO4VQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "sourcemap-codec": "^1.4.8"
      }
    },
    "node_modules/@tanstack/query-core": {
      "version": "5.91.2",
      "resolved": "https://registry.npmjs.org/@tanstack/query-core/-/query-core-5.91.2.tgz",
      "integrity": "sha512-Uz2pTgPC1mhqrrSGg18RKCWT/pkduAYtxbcyIyKBhw7dTWjXZIzqmpzO2lBkyWr4hlImQgpu1m1pei3UnkFRWw==",
      "license": "MIT",
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/tannerlinsley"
      }
    },
    "node_modules/@tanstack/react-query": {
      "version": "5.91.2",
      "resolved": "https://registry.npmjs.org/@tanstack/react-query/-/react-query-5.91.2.tgz",
      "integrity": "sha512-GClLPzbM57iFXv+FlvOUL56XVe00PxuTaVEyj1zAObhRiKF008J5vedmaq7O6ehs+VmPHe8+PUQhMuEyv8d9wQ==",
      "license": "MIT",
      "dependencies": {
        "@tanstack/query-core": "5.91.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/tannerlinsley"
      },
      "peerDependencies": {
        "react": "^18 || ^19"
      }
    },
    "node_modules/@types/babel__core": {
      "version": "7.20.5",
      "resolved": "https://registry.npmjs.org/@types/babel__core/-/babel__core-7.20.5.tgz",
      "integrity": "sha512-qoQprZvz5wQFJwMDqeseRXWv3rqMvhgpbXFfVyWhbx9X47POIA6i/+dXefEmZKoAgOaTdaIgNSMqMIU61yRyzA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.20.7",
        "@babel/types": "^7.20.7",
        "@types/babel__generator": "*",
        "@types/babel__template": "*",
        "@types/babel__traverse": "*"
      }
    },
    "node_modules/@types/babel__generator": {
      "version": "7.27.0",
      "resolved": "https://registry.npmjs.org/@types/babel__generator/-/babel__generator-7.27.0.tgz",
      "integrity": "sha512-ufFd2Xi92OAVPYsy+P4n7/U7e68fex0+Ee8gSG9KX7eo084CWiQ4sdxktvdl0bOPupXtVJPY19zk6EwWqUQ8lg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.0.0"
      }
    },
    "node_modules/@types/babel__template": {
      "version": "7.4.4",
      "resolved": "https://registry.npmjs.org/@types/babel__template/-/babel__template-7.4.4.tgz",
      "integrity": "sha512-h/NUaSyG5EyxBIp8YRxo4RMe2/qQgvyowRwVMzhYhBCONbW8PUsg4lkFMrhgZhUe5z3L3MiLDuvyJ/CaPa2A8A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.1.0",
        "@babel/types": "^7.0.0"
      }
    },
    "node_modules/@types/babel__traverse": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@types/babel__traverse/-/babel__traverse-7.28.0.tgz",
      "integrity": "sha512-8PvcXf70gTDZBgt9ptxJ8elBeBjcLOAcOtoO/mPJjtji1+CdGbHgm77om1GrsPxsiE+uXIpNSK64UYaIwQXd4Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.28.2"
      }
    },
    "node_modules/@types/doctrine": {
      "version": "0.0.9",
      "resolved": "https://registry.npmjs.org/@types/doctrine/-/doctrine-0.0.9.tgz",
      "integrity": "sha512-eOIHzCUSH7SMfonMG1LsC2f8vxBFtho6NGBznK41R84YzPuvSBzrhEps33IsQiOW9+VL6NQ9DbjQJznk/S4uRA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/estree": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/@types/estree/-/estree-1.0.8.tgz",
      "integrity": "sha512-dWHzHa2WqEXI/O1E9OjrocMTKJl2mSrEolh1Iomrv6U+JuNwaHXsXx9bLu5gG7BUWFIN0skIQJQ/L1rIex4X6w==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/mdx": {
      "version": "2.0.13",
      "resolved": "https://registry.npmjs.org/@types/mdx/-/mdx-2.0.13.tgz",
      "integrity": "sha512-+OWZQfAYyio6YkJb3HLxDrvnx6SWWDbC0zVPfBRzUk0/nqoDyf6dNxQi3eArPe8rJ473nobTMQ/8Zk+LxJ+Yuw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/prop-types": {
      "version": "15.7.15",
      "resolved": "https://registry.npmjs.org/@types/prop-types/-/prop-types-15.7.15.tgz",
      "integrity": "sha512-F6bEyamV9jKGAFBEmlQnesRPGOQqS2+Uwi0Em15xenOxHaf2hv6L8YCVn3rPdPJOiJfPiCnLIRyvwVaqMY3MIw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/react": {
      "version": "18.3.28",
      "resolved": "https://registry.npmjs.org/@types/react/-/react-18.3.28.tgz",
      "integrity": "sha512-z9VXpC7MWrhfWipitjNdgCauoMLRdIILQsAEV+ZesIzBq/oUlxk0m3ApZuMFCXdnS4U7KrI+l3WRUEGQ8K1QKw==",
      "dev": true,
      "license": "MIT",
      "peer": true,
      "dependencies": {
        "@types/prop-types": "*",
        "csstype": "^3.2.2"
      }
    },
    "node_modules/@types/react-dom": {
      "version": "18.3.7",
      "resolved": "https://registry.npmjs.org/@types/react-dom/-/react-dom-18.3.7.tgz",
      "integrity": "sha512-MEe3UeoENYVFXzoXEWsvcpg6ZvlrFNlOQ7EOsvhI3CfAXwzPfO8Qwuxd40nepsYKqyyVQnTdEfv68q91yLcKrQ==",
      "dev": true,
      "license": "MIT",
      "peerDependencies": {
        "@types/react": "^18.0.0"
      }
    },
    "node_modules/@types/resolve": {
      "version": "1.20.6",
      "resolved": "https://registry.npmjs.org/@types/resolve/-/resolve-1.20.6.tgz",
      "integrity": "sha512-A4STmOXPhMUtHH+S6ymgE2GiBSMqf4oTvcQZMcHzokuTLVYzXTB8ttjcgxOVaAp2lGwEdzZ0J+cRbbeevQj1UQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/trusted-types": {
      "version": "2.0.7",
      "resolved": "https://registry.npmjs.org/@types/trusted-types/-/trusted-types-2.0.7.tgz",
      "integrity": "sha512-ScaPdn1dQczgbl0QFTeTOmVHFULt394XJgOQNoyVhZ6r2vLnMLJfBPd53SB52T/3G36VI1/g2MZaX0cwDuXsfw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/uuid": {
      "version": "9.0.8",
      "resolved": "https://registry.npmjs.org/@types/uuid/-/uuid-9.0.8.tgz",
      "integrity": "sha512-jg+97EGIcY9AGHJJRaaPVgetKDsrTgbRjQ5Msgjh/DQKEFl0DtyRr/VCOyD1T2R1MNeWPK/u7JoGhlDZnKBAfA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@vitejs/plugin-react": {
      "version": "4.7.0",
      "resolved": "https://registry.npmjs.org/@vitejs/plugin-react/-/plugin-react-4.7.0.tgz",
      "integrity": "sha512-gUu9hwfWvvEDBBmgtAowQCojwZmJ5mcLn3aufeCsitijs3+f2NsrPtlAWIR6OPiqljl96GVCUbLe0HyqIpVaoA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.28.0",
        "@babel/plugin-transform-react-jsx-self": "^7.27.1",
        "@babel/plugin-transform-react-jsx-source": "^7.27.1",
        "@rolldown/pluginutils": "1.0.0-beta.27",
        "@types/babel__core": "^7.20.5",
        "react-refresh": "^0.17.0"
      },
      "engines": {
        "node": "^14.18.0 || >=16.0.0"
      },
      "peerDependencies": {
        "vite": "^4.2.0 || ^5.0.0 || ^6.0.0 || ^7.0.0"
      }
    },
    "node_modules/acorn": {
      "version": "8.16.0",
      "resolved": "https://registry.npmjs.org/acorn/-/acorn-8.16.0.tgz",
      "integrity": "sha512-UVJyE9MttOsBQIDKw1skb9nAwQuR5wuGD3+82K6JgJlm/Y+KI92oNsMNGZCYdDsVtRHSak0pcV5Dno5+4jh9sw==",
      "dev": true,
      "license": "MIT",
      "bin": {
        "acorn": "bin/acorn"
      },
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/agent-base": {
      "version": "7.1.4",
      "resolved": "https://registry.npmjs.org/agent-base/-/agent-base-7.1.4.tgz",
      "integrity": "sha512-MnA+YT8fwfJPgBx3m60MNqakm30XOkyIoH1y6huTQvC0PwZG7ki8NacLBcrPbNoo8vEZy7Jpuk7+jMO+CUovTQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 14"
      }
    },
    "node_modules/ajv": {
      "version": "8.18.0",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-8.18.0.tgz",
      "integrity": "sha512-PlXPeEWMXMZ7sPYOHqmDyCJzcfNrUr3fGNKtezX14ykXOEIvyK81d+qydx89KY5O71FKMPaQ2vBfBFI5NHR63A==",
      "dev": true,
      "license": "MIT",
      "peer": true,
      "dependencies": {
        "fast-deep-equal": "^3.1.3",
        "fast-uri": "^3.0.1",
        "json-schema-traverse": "^1.0.0",
        "require-from-string": "^2.0.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/ansi-colors": {
      "version": "4.1.3",
      "resolved": "https://registry.npmjs.org/ansi-colors/-/ansi-colors-4.1.3.tgz",
      "integrity": "sha512-/6w/C21Pm1A7aZitlI5Ni/2J6FFQN8i1Cvz3kHABAAbw93v/NlvKdVOqz7CCWz/3iv/JplRSEEZ83XION15ovw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/ansi-regex": {
      "version": "6.2.2",
      "resolved": "https://registry.npmjs.org/ansi-regex/-/ansi-regex-6.2.2.tgz",
      "integrity": "sha512-Bq3SmSpyFHaWjPk8If9yc6svM8c56dB5BAtW4Qbw5jHTwwXXcTLoRMkpDJp6VL0XzlWaCHTXrkFURMYmD0sLqg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-regex?sponsor=1"
      }
    },
    "node_modules/ansi-styles": {
      "version": "6.2.3",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-6.2.3.tgz",
      "integrity": "sha512-4Dj6M28JB+oAH8kFkTLUo+a2jwOFkuqb3yucU0CANcRRUbxS0cP0nZYCGjcc3BNXwRIsUVmDGgzawme7zvJHvg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-styles?sponsor=1"
      }
    },
    "node_modules/antd": {
      "version": "5.29.3",
      "resolved": "https://registry.npmjs.org/antd/-/antd-5.29.3.tgz",
      "integrity": "sha512-3DdbGCa9tWAJGcCJ6rzR8EJFsv2CtyEbkVabZE14pfgUHfCicWCj0/QzQVLDYg8CPfQk9BH7fHCoTXHTy7MP/A==",
      "license": "MIT",
      "dependencies": {
        "@ant-design/colors": "^7.2.1",
        "@ant-design/cssinjs": "^1.23.0",
        "@ant-design/cssinjs-utils": "^1.1.3",
        "@ant-design/fast-color": "^2.0.6",
        "@ant-design/icons": "^5.6.1",
        "@ant-design/react-slick": "~1.1.2",
        "@babel/runtime": "^7.26.0",
        "@rc-component/color-picker": "~2.0.1",
        "@rc-component/mutate-observer": "^1.1.0",
        "@rc-component/qrcode": "~1.1.0",
        "@rc-component/tour": "~1.15.1",
        "@rc-component/trigger": "^2.3.0",
        "classnames": "^2.5.1",
        "copy-to-clipboard": "^3.3.3",
        "dayjs": "^1.11.11",
        "rc-cascader": "~3.34.0",
        "rc-checkbox": "~3.5.0",
        "rc-collapse": "~3.9.0",
        "rc-dialog": "~9.6.0",
        "rc-drawer": "~7.3.0",
        "rc-dropdown": "~4.2.1",
        "rc-field-form": "~2.7.1",
        "rc-image": "~7.12.0",
        "rc-input": "~1.8.0",
        "rc-input-number": "~9.5.0",
        "rc-mentions": "~2.20.0",
        "rc-menu": "~9.16.1",
        "rc-motion": "^2.9.5",
        "rc-notification": "~5.6.4",
        "rc-pagination": "~5.1.0",
        "rc-picker": "~4.11.3",
        "rc-progress": "~4.0.0",
        "rc-rate": "~2.13.1",
        "rc-resize-observer": "^1.4.3",
        "rc-segmented": "~2.7.0",
        "rc-select": "~14.16.8",
        "rc-slider": "~11.1.9",
        "rc-steps": "~6.0.1",
        "rc-switch": "~4.1.0",
        "rc-table": "~7.54.0",
        "rc-tabs": "~15.7.0",
        "rc-textarea": "~1.10.2",
        "rc-tooltip": "~6.4.0",
        "rc-tree": "~5.13.1",
        "rc-tree-select": "~5.27.0",
        "rc-upload": "~4.11.0",
        "rc-util": "^5.44.4",
        "scroll-into-view-if-needed": "^3.1.0",
        "throttle-debounce": "^5.0.2"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/ant-design"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/argparse": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/argparse/-/argparse-2.0.1.tgz",
      "integrity": "sha512-8+9WqebbFzpX9OR+Wa6O29asIogeRMzcGtAINdpMHHyAg10f05aSFVBbcEqGf/PXw1EjAZ+q2/bEBg3DvurK3Q==",
      "dev": true,
      "license": "Python-2.0"
    },
    "node_modules/array-buffer-byte-length": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/array-buffer-byte-length/-/array-buffer-byte-length-1.0.2.tgz",
      "integrity": "sha512-LHE+8BuR7RYGDKvnrmcuSq3tDcKv9OFEXQt/HpbZhY7V6h0zlUXutnAD82GiFx9rdieCMjkvtcsPqBwgUl1Iiw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "is-array-buffer": "^3.0.5"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/arraybuffer.prototype.slice": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/arraybuffer.prototype.slice/-/arraybuffer.prototype.slice-1.0.4.tgz",
      "integrity": "sha512-BNoCY6SXXPQ7gF2opIP4GBE+Xw7U+pHMYKuzjgCN3GwiaIR09UUeKfheyIry77QtrCBlC0KK0q5/TER/tYh3PQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "array-buffer-byte-length": "^1.0.1",
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6",
        "is-array-buffer": "^3.0.4"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/ast-types": {
      "version": "0.16.1",
      "resolved": "https://registry.npmjs.org/ast-types/-/ast-types-0.16.1.tgz",
      "integrity": "sha512-6t10qk83GOG8p0vKmaCr8eiilZwO171AvbROMtvvNiwrTly62t+7XkA8RdIIVbpMhCASAsxgAzdRSwh6nw/5Dg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "tslib": "^2.0.1"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/async": {
      "version": "3.2.6",
      "resolved": "https://registry.npmjs.org/async/-/async-3.2.6.tgz",
      "integrity": "sha512-htCUDlxyyCLMgaM3xXg0C0LW2xqfuQ6p05pCEIsXuyQ+a1koYKTuBMzRNwmybfLgvJDMd0r1LTn4+E0Ti6C2AA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/async-function": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/async-function/-/async-function-1.0.0.tgz",
      "integrity": "sha512-hsU18Ae8CDTR6Kgu9DYf0EbCr/a5iGL0rytQDobUcdpYOKokk8LEjVphnXkDkgpi0wYVsqrXuP0bZxJaTqdgoA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/at-least-node": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/at-least-node/-/at-least-node-1.0.0.tgz",
      "integrity": "sha512-+q/t7Ekv1EDY2l6Gda6LLiX14rU9TV20Wa3ofeQmwPFZbOMo9DXrLbOjFaaclkXKWidIaopwAObQDqwWtGUjqg==",
      "dev": true,
      "license": "ISC",
      "engines": {
        "node": ">= 4.0.0"
      }
    },
    "node_modules/available-typed-arrays": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/available-typed-arrays/-/available-typed-arrays-1.0.7.tgz",
      "integrity": "sha512-wvUjBtSGN7+7SjNpq/9M2Tg350UZD3q62IFZLbRAR1bSMlCo1ZaeW+BJ+D090e4hIIZLBcTDWe4Mh4jvUDajzQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "possible-typed-array-names": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/babel-plugin-polyfill-corejs2": {
      "version": "0.4.17",
      "resolved": "https://registry.npmjs.org/babel-plugin-polyfill-corejs2/-/babel-plugin-polyfill-corejs2-0.4.17.tgz",
      "integrity": "sha512-aTyf30K/rqAsNwN76zYrdtx8obu0E4KoUME29B1xj+B3WxgvWkp943vYQ+z8Mv3lw9xHXMHpvSPOBxzAkIa94w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/compat-data": "^7.28.6",
        "@babel/helper-define-polyfill-provider": "^0.6.8",
        "semver": "^6.3.1"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/babel-plugin-polyfill-corejs3": {
      "version": "0.14.2",
      "resolved": "https://registry.npmjs.org/babel-plugin-polyfill-corejs3/-/babel-plugin-polyfill-corejs3-0.14.2.tgz",
      "integrity": "sha512-coWpDLJ410R781Npmn/SIBZEsAetR4xVi0SxLMXPaMO4lSf1MwnkGYMtkFxew0Dn8B3/CpbpYxN0JCgg8mn67g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-define-polyfill-provider": "^0.6.8",
        "core-js-compat": "^3.48.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/babel-plugin-polyfill-regenerator": {
      "version": "0.6.8",
      "resolved": "https://registry.npmjs.org/babel-plugin-polyfill-regenerator/-/babel-plugin-polyfill-regenerator-0.6.8.tgz",
      "integrity": "sha512-M762rNHfSF1EV3SLtnCJXFoQbbIIz0OyRwnCmV0KPC7qosSfCO0QLTSuJX3ayAebubhE6oYBAYPrBA5ljowaZg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-define-polyfill-provider": "^0.6.8"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/balanced-match": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/balanced-match/-/balanced-match-1.0.2.tgz",
      "integrity": "sha512-3oSeUO0TMV67hN1AmbXsK4yaqU7tjiHlbxRDZOpH0KW9+CeX4bRAaX0Anxt0tx2MrpRpWwQaPwIlISEJhYU5Pw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/baseline-browser-mapping": {
      "version": "2.10.9",
      "resolved": "https://registry.npmjs.org/baseline-browser-mapping/-/baseline-browser-mapping-2.10.9.tgz",
      "integrity": "sha512-OZd0e2mU11ClX8+IdXe3r0dbqMEznRiT4TfbhYIbcRPZkqJ7Qwer8ij3GZAmLsRKa+II9V1v5czCkvmHH3XZBg==",
      "dev": true,
      "license": "Apache-2.0",
      "bin": {
        "baseline-browser-mapping": "dist/cli.cjs"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/better-opn": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/better-opn/-/better-opn-3.0.2.tgz",
      "integrity": "sha512-aVNobHnJqLiUelTaHat9DZ1qM2w0C0Eym4LPI/3JxOnSokGVdsl1T1kN7TFvsEAD8G47A6VKQ0TVHqbBnYMJlQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "open": "^8.0.4"
      },
      "engines": {
        "node": ">=12.0.0"
      }
    },
    "node_modules/brace-expansion": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-2.0.2.tgz",
      "integrity": "sha512-Jt0vHyM+jmUBqojB7E1NIYadt0vI0Qxjxd2TErW94wDz+E2LAm5vKMXXwg6ZZBTHPuUlDgQHKXvjGBdfcF1ZDQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "balanced-match": "^1.0.0"
      }
    },
    "node_modules/browser-assert": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/browser-assert/-/browser-assert-1.2.1.tgz",
      "integrity": "sha512-nfulgvOR6S4gt9UKCeGJOuSGBPGiFT6oQ/2UBnvTY/5aQ1PnksW72fhZkM30DzoRRv2WpwZf1vHHEr3mtuXIWQ==",
      "dev": true
    },
    "node_modules/browserslist": {
      "version": "4.28.1",
      "resolved": "https://registry.npmjs.org/browserslist/-/browserslist-4.28.1.tgz",
      "integrity": "sha512-ZC5Bd0LgJXgwGqUknZY/vkUQ04r8NXnJZ3yYi4vDmSiZmC/pdSN0NbNRPxZpbtO4uAfDUAFffO8IZoM3Gj8IkA==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "peer": true,
      "dependencies": {
        "baseline-browser-mapping": "^2.9.0",
        "caniuse-lite": "^1.0.30001759",
        "electron-to-chromium": "^1.5.263",
        "node-releases": "^2.0.27",
        "update-browserslist-db": "^1.2.0"
      },
      "bin": {
        "browserslist": "cli.js"
      },
      "engines": {
        "node": "^6 || ^7 || ^8 || ^9 || ^10 || ^11 || ^12 || >=13.7"
      }
    },
    "node_modules/buffer-from": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/buffer-from/-/buffer-from-1.1.2.tgz",
      "integrity": "sha512-E+XQCRwSbaaiChtv6k6Dwgc+bx+Bs6vuKJHHl5kox/BaKbhiXzqQOwK4cO22yElGp2OCmjwVhT3HmxgyPGnJfQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/call-bind": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/call-bind/-/call-bind-1.0.8.tgz",
      "integrity": "sha512-oKlSFMcMwpUg2ednkhQ454wfWiU/ul3CkJe/PEHcTKuiX6RpbehUiFMXu13HalGZxfUwCQzZG747YXBn1im9ww==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.0",
        "es-define-property": "^1.0.0",
        "get-intrinsic": "^1.2.4",
        "set-function-length": "^1.2.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/call-bind-apply-helpers": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/call-bind-apply-helpers/-/call-bind-apply-helpers-1.0.2.tgz",
      "integrity": "sha512-Sp1ablJ0ivDkSzjcaJdxEunN5/XvksFJ2sMBFfq6x0ryhQV/2b/KwFe21cMpmHtPOSij8K99/wSfoEuTObmuMQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/call-bound": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/call-bound/-/call-bound-1.0.4.tgz",
      "integrity": "sha512-+ys997U96po4Kx/ABpBCqhA9EuxJaQWDQg7295H4hBphv3IZg0boBKuwYpt4YXp6MZ5AmZQnU/tyMTlRpaSejg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "get-intrinsic": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/caniuse-lite": {
      "version": "1.0.30001780",
      "resolved": "https://registry.npmjs.org/caniuse-lite/-/caniuse-lite-1.0.30001780.tgz",
      "integrity": "sha512-llngX0E7nQci5BPJDqoZSbuZ5Bcs9F5db7EtgfwBerX9XGtkkiO4NwfDDIRzHTTwcYC8vC7bmeUEPGrKlR/TkQ==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/caniuse-lite"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "CC-BY-4.0"
    },
    "node_modules/change-case": {
      "version": "5.4.4",
      "resolved": "https://registry.npmjs.org/change-case/-/change-case-5.4.4.tgz",
      "integrity": "sha512-HRQyTk2/YPEkt9TnUPbOpr64Uw3KOicFWPVBb+xiHvd6eBx/qPr9xqfBFDT8P2vWsvvz4jbEkfDe71W3VyNu2w==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/classnames": {
      "version": "2.5.1",
      "resolved": "https://registry.npmjs.org/classnames/-/classnames-2.5.1.tgz",
      "integrity": "sha512-saHYOzhIQs6wy2sVxTM6bUDsQO4F50V9RQ22qBpEdCW+I+/Wmke2HOl6lS6dTpdxVhb88/I6+Hs+438c3lfUow==",
      "license": "MIT"
    },
    "node_modules/color-convert": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/color-convert/-/color-convert-2.0.1.tgz",
      "integrity": "sha512-RRECPsj7iu/xb5oKYcsFHSppFNnsj/52OVTRKb4zP5onXwVF3zVmmToNcOfGC+CRDpfK/U584fMg38ZHCaElKQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "color-name": "~1.1.4"
      },
      "engines": {
        "node": ">=7.0.0"
      }
    },
    "node_modules/color-name": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/color-name/-/color-name-1.1.4.tgz",
      "integrity": "sha512-dOy+3AuW3a2wNbZHIuMZpTcgjGuLU/uBL/ubcZF9OXbDo8ff4O8yVp5Bf0efS8uEoYo5q4Fx7dY9OgQGXgAsQA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/colorette": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/colorette/-/colorette-1.4.0.tgz",
      "integrity": "sha512-Y2oEozpomLn7Q3HFP7dpww7AtMJplbM9lGZP6RDfHqmbeRjiwRg4n6VM6j4KLmRke85uWEI7JqF17f3pqdRA0g==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/commander": {
      "version": "2.20.3",
      "resolved": "https://registry.npmjs.org/commander/-/commander-2.20.3.tgz",
      "integrity": "sha512-GpVkmM8vF2vQUkj2LvZmD35JxeJOLCwJ9cUkugyk2nuhbv3+mJvpLYYt+0+USMxE+oj+ey/lJEnhZw75x/OMcQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/common-tags": {
      "version": "1.8.2",
      "resolved": "https://registry.npmjs.org/common-tags/-/common-tags-1.8.2.tgz",
      "integrity": "sha512-gk/Z852D2Wtb//0I+kRFNKKE9dIIVirjoqPoA1wJU+XePVXZfGeBpk45+A1rKO4Q43prqWBNY/MiIeRLbPWUaA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=4.0.0"
      }
    },
    "node_modules/compute-scroll-into-view": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/compute-scroll-into-view/-/compute-scroll-into-view-3.1.1.tgz",
      "integrity": "sha512-VRhuHOLoKYOy4UbilLbUzbYg93XLjv2PncJC50EuTWPA3gaja1UjBsUP/D/9/juV3vQFr6XBEzn9KCAHdUvOHw==",
      "license": "MIT"
    },
    "node_modules/convert-source-map": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-2.0.0.tgz",
      "integrity": "sha512-Kvp459HrV2FEJ1CAsi1Ku+MY3kasH19TFykTz2xWmMeq6bk2NU3XXvfJ+Q61m0xktWwt+1HSYf3JZsTms3aRJg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/copy-to-clipboard": {
      "version": "3.3.3",
      "resolved": "https://registry.npmjs.org/copy-to-clipboard/-/copy-to-clipboard-3.3.3.tgz",
      "integrity": "sha512-2KV8NhB5JqC3ky0r9PMCAZKbUHSwtEo4CwCs0KXgruG43gX5PMqDEBbVU4OUzw2MuAWUfsuFmWvEKG5QRfSnJA==",
      "license": "MIT",
      "dependencies": {
        "toggle-selection": "^1.0.6"
      }
    },
    "node_modules/core-js-compat": {
      "version": "3.49.0",
      "resolved": "https://registry.npmjs.org/core-js-compat/-/core-js-compat-3.49.0.tgz",
      "integrity": "sha512-VQXt1jr9cBz03b331DFDCCP90b3fanciLkgiOoy8SBHy06gNf+vQ1A3WFLqG7I8TipYIKeYK9wxd0tUrvHcOZA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.28.1"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/core-js"
      }
    },
    "node_modules/cross-spawn": {
      "version": "7.0.6",
      "resolved": "https://registry.npmjs.org/cross-spawn/-/cross-spawn-7.0.6.tgz",
      "integrity": "sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "path-key": "^3.1.0",
        "shebang-command": "^2.0.0",
        "which": "^2.0.1"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/crypto-random-string": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/crypto-random-string/-/crypto-random-string-2.0.0.tgz",
      "integrity": "sha512-v1plID3y9r/lPhviJ1wrXpLeyUIGAZ2SHNYTEapm7/8A9nLPoyvVp3RK/EPFqn5kEznyWgYZNsRtYYIWbuG8KA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/csstype": {
      "version": "3.2.3",
      "resolved": "https://registry.npmjs.org/csstype/-/csstype-3.2.3.tgz",
      "integrity": "sha512-z1HGKcYy2xA8AGQfwrn0PAy+PB7X/GSj3UVJW9qKyn43xWa+gl5nXmU4qqLMRzWVLFC8KusUX8T/0kCiOYpAIQ==",
      "license": "MIT"
    },
    "node_modules/data-view-buffer": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/data-view-buffer/-/data-view-buffer-1.0.2.tgz",
      "integrity": "sha512-EmKO5V3OLXh1rtK2wgXRansaK1/mtVdTUEiEI0W8RkvgT05kfxaH29PliLnpLP73yYO6142Q72QNa8Wx/A5CqQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "is-data-view": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/data-view-byte-length": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/data-view-byte-length/-/data-view-byte-length-1.0.2.tgz",
      "integrity": "sha512-tuhGbE6CfTM9+5ANGf+oQb72Ky/0+s3xKUpHvShfiz2RxMFgFPjsXuRLBVMtvMs15awe45SRb83D6wH4ew6wlQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "is-data-view": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/inspect-js"
      }
    },
    "node_modules/data-view-byte-offset": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/data-view-byte-offset/-/data-view-byte-offset-1.0.1.tgz",
      "integrity": "sha512-BS8PfmtDGnrgYdOonGZQdLZslWIeCGFP9tpan0hi1Co2Zr2NKADsvGYA8XxuG/4UWgJ6Cjtv+YJnB6MM69QGlQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "is-data-view": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/dayjs": {
      "version": "1.11.20",
      "resolved": "https://registry.npmjs.org/dayjs/-/dayjs-1.11.20.tgz",
      "integrity": "sha512-YbwwqR/uYpeoP4pu043q+LTDLFBLApUP6VxRihdfNTqu4ubqMlGDLd6ErXhEgsyvY0K6nCs7nggYumAN+9uEuQ==",
      "license": "MIT",
      "peer": true
    },
    "node_modules/debug": {
      "version": "4.4.3",
      "resolved": "https://registry.npmjs.org/debug/-/debug-4.4.3.tgz",
      "integrity": "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.3"
      },
      "engines": {
        "node": ">=6.0"
      },
      "peerDependenciesMeta": {
        "supports-color": {
          "optional": true
        }
      }
    },
    "node_modules/deepmerge": {
      "version": "4.3.1",
      "resolved": "https://registry.npmjs.org/deepmerge/-/deepmerge-4.3.1.tgz",
      "integrity": "sha512-3sUqbMEc77XqpdNO7FRyRog+eW3ph+GYCbj+rK+uYyRMuwsVy0rMiVtPn+QJlKFvWP/1PYpapqYn0Me2knFn+A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/define-data-property": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/define-data-property/-/define-data-property-1.1.4.tgz",
      "integrity": "sha512-rBMvIzlpA8v6E+SJZoo++HAYqsLrkg7MSfIinMPFhmkorw7X+dOXVJQs+QT69zGkzMyfDnIMN2Wid1+NbL3T+A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-define-property": "^1.0.0",
        "es-errors": "^1.3.0",
        "gopd": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/define-lazy-prop": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/define-lazy-prop/-/define-lazy-prop-2.0.0.tgz",
      "integrity": "sha512-Ds09qNh8yw3khSjiJjiUInaGX9xlqZDY7JVryGxdxV7NPeuqQfplOpQ66yJFZut3jLa5zOwkXw1g9EI2uKh4Og==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/define-properties": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/define-properties/-/define-properties-1.2.1.tgz",
      "integrity": "sha512-8QmQKqEASLd5nx0U1B1okLElbUuuttJ/AnYmRXbbbGDWh6uS208EjD4Xqq/I9wK7u0v6O08XhTWnt5XtEbR6Dg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "define-data-property": "^1.0.1",
        "has-property-descriptors": "^1.0.0",
        "object-keys": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/dequal": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/dequal/-/dequal-2.0.3.tgz",
      "integrity": "sha512-0je+qPKHEMohvfRTCEo3CrPG6cAzAYgmzKyxRiYSSDkS6eGJdyVJm7WaYA5ECaAD9wLB2T4EEeymA5aFVcYXCA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/doctrine": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/doctrine/-/doctrine-3.0.0.tgz",
      "integrity": "sha512-yS+Q5i3hBf7GBkd4KG8a7eBNNWNGLTaEwwYWUijIYM7zrlYDM0BFXHjjPWlWZ1Rg7UaddZeIDmi9jF3HmqiQ2w==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "esutils": "^2.0.2"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/dunder-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/dunder-proto/-/dunder-proto-1.0.1.tgz",
      "integrity": "sha512-KIN/nDJBQRcXw0MLVhZE9iQHmG68qAVIBg9CqmUYjmQIhgij9U5MFvrqkUL5FbtyyzZuOeOt0zdeRe4UY7ct+A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.1",
        "es-errors": "^1.3.0",
        "gopd": "^1.2.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/eastasianwidth": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/eastasianwidth/-/eastasianwidth-0.2.0.tgz",
      "integrity": "sha512-I88TYZWc9XiYHRQ4/3c5rjjfgkjhLyW2luGIheGERbNQ6OY7yTybanSpDXZa8y7VUP9YmDcYa+eyq4ca7iLqWA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/ejs": {
      "version": "3.1.10",
      "resolved": "https://registry.npmjs.org/ejs/-/ejs-3.1.10.tgz",
      "integrity": "sha512-UeJmFfOrAQS8OJWPZ4qtgHyWExa088/MtK5UEyoJGFH67cDEXkZSviOiKRCZ4Xij0zxI3JECgYs3oKx+AizQBA==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "jake": "^10.8.5"
      },
      "bin": {
        "ejs": "bin/cli.js"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/electron-to-chromium": {
      "version": "1.5.321",
      "resolved": "https://registry.npmjs.org/electron-to-chromium/-/electron-to-chromium-1.5.321.tgz",
      "integrity": "sha512-L2C7Q279W2D/J4PLZLk7sebOILDSWos7bMsMNN06rK482umHUrh/3lM8G7IlHFOYip2oAg5nha1rCMxr/rs6ZQ==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/emoji-regex": {
      "version": "9.2.2",
      "resolved": "https://registry.npmjs.org/emoji-regex/-/emoji-regex-9.2.2.tgz",
      "integrity": "sha512-L18DaJsXSUk2+42pv8mLs5jJT2hqFkFE4j21wOmgbUqsZ2hL72NsUU785g9RXgo3s0ZNgVl42TiHp3ZtOv/Vyg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/es-abstract": {
      "version": "1.24.1",
      "resolved": "https://registry.npmjs.org/es-abstract/-/es-abstract-1.24.1.tgz",
      "integrity": "sha512-zHXBLhP+QehSSbsS9Pt23Gg964240DPd6QCf8WpkqEXxQ7fhdZzYsocOr5u7apWonsS5EjZDmTF+/slGMyasvw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "array-buffer-byte-length": "^1.0.2",
        "arraybuffer.prototype.slice": "^1.0.4",
        "available-typed-arrays": "^1.0.7",
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "data-view-buffer": "^1.0.2",
        "data-view-byte-length": "^1.0.2",
        "data-view-byte-offset": "^1.0.1",
        "es-define-property": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "es-set-tostringtag": "^2.1.0",
        "es-to-primitive": "^1.3.0",
        "function.prototype.name": "^1.1.8",
        "get-intrinsic": "^1.3.0",
        "get-proto": "^1.0.1",
        "get-symbol-description": "^1.1.0",
        "globalthis": "^1.0.4",
        "gopd": "^1.2.0",
        "has-property-descriptors": "^1.0.2",
        "has-proto": "^1.2.0",
        "has-symbols": "^1.1.0",
        "hasown": "^2.0.2",
        "internal-slot": "^1.1.0",
        "is-array-buffer": "^3.0.5",
        "is-callable": "^1.2.7",
        "is-data-view": "^1.0.2",
        "is-negative-zero": "^2.0.3",
        "is-regex": "^1.2.1",
        "is-set": "^2.0.3",
        "is-shared-array-buffer": "^1.0.4",
        "is-string": "^1.1.1",
        "is-typed-array": "^1.1.15",
        "is-weakref": "^1.1.1",
        "math-intrinsics": "^1.1.0",
        "object-inspect": "^1.13.4",
        "object-keys": "^1.1.1",
        "object.assign": "^4.1.7",
        "own-keys": "^1.0.1",
        "regexp.prototype.flags": "^1.5.4",
        "safe-array-concat": "^1.1.3",
        "safe-push-apply": "^1.0.0",
        "safe-regex-test": "^1.1.0",
        "set-proto": "^1.0.0",
        "stop-iteration-iterator": "^1.1.0",
        "string.prototype.trim": "^1.2.10",
        "string.prototype.trimend": "^1.0.9",
        "string.prototype.trimstart": "^1.0.8",
        "typed-array-buffer": "^1.0.3",
        "typed-array-byte-length": "^1.0.3",
        "typed-array-byte-offset": "^1.0.4",
        "typed-array-length": "^1.0.7",
        "unbox-primitive": "^1.1.0",
        "which-typed-array": "^1.1.19"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/es-define-property": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/es-define-property/-/es-define-property-1.0.1.tgz",
      "integrity": "sha512-e3nRfgfUZ4rNGL232gUgX06QNyyez04KdjFrF+LTRoOXmrOgFKDg4BCdsjW8EnT69eqdYGmRpJwiPVYNrCaW3g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-errors": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-errors/-/es-errors-1.3.0.tgz",
      "integrity": "sha512-Zf5H2Kxt2xjTvbJvP2ZWLEICxA6j+hAmMzIlypy4xcBg1vKVnx89Wy0GbS+kf5cwCVFFzdCFh2XSCFNULS6csw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-object-atoms": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/es-object-atoms/-/es-object-atoms-1.1.1.tgz",
      "integrity": "sha512-FGgH2h8zKNim9ljj7dankFPcICIK9Cp5bm+c2gQSYePhpaG5+esrLODihIorn+Pe6FGJzWhXQotPv73jTaldXA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-set-tostringtag": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/es-set-tostringtag/-/es-set-tostringtag-2.1.0.tgz",
      "integrity": "sha512-j6vWzfrGVfyXxge+O0x5sh6cvxAog0a/4Rdd2K36zCMV5eJ+/+tOAngRO8cODMNWbVRdVlmGZQL2YS3yR8bIUA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6",
        "has-tostringtag": "^1.0.2",
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-to-primitive": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-to-primitive/-/es-to-primitive-1.3.0.tgz",
      "integrity": "sha512-w+5mJ3GuFL+NjVtJlvydShqE1eN3h3PbI7/5LAsYJP/2qtuMXjfL2LpHSRqo4b4eSF5K/DH1JXKUAHSB2UW50g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-callable": "^1.2.7",
        "is-date-object": "^1.0.5",
        "is-symbol": "^1.0.4"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/esbuild": {
      "version": "0.21.5",
      "resolved": "https://registry.npmjs.org/esbuild/-/esbuild-0.21.5.tgz",
      "integrity": "sha512-mg3OPMV4hXywwpoDxu3Qda5xCKQi+vCTZq8S9J/EpkhB2HzKXq4SNFZE3+NK93JYxc8VMSep+lOUSC/RVKaBqw==",
      "dev": true,
      "hasInstallScript": true,
      "license": "MIT",
      "peer": true,
      "bin": {
        "esbuild": "bin/esbuild"
      },
      "engines": {
        "node": ">=12"
      },
      "optionalDependencies": {
        "@esbuild/aix-ppc64": "0.21.5",
        "@esbuild/android-arm": "0.21.5",
        "@esbuild/android-arm64": "0.21.5",
        "@esbuild/android-x64": "0.21.5",
        "@esbuild/darwin-arm64": "0.21.5",
        "@esbuild/darwin-x64": "0.21.5",
        "@esbuild/freebsd-arm64": "0.21.5",
        "@esbuild/freebsd-x64": "0.21.5",
        "@esbuild/linux-arm": "0.21.5",
        "@esbuild/linux-arm64": "0.21.5",
        "@esbuild/linux-ia32": "0.21.5",
        "@esbuild/linux-loong64": "0.21.5",
        "@esbuild/linux-mips64el": "0.21.5",
        "@esbuild/linux-ppc64": "0.21.5",
        "@esbuild/linux-riscv64": "0.21.5",
        "@esbuild/linux-s390x": "0.21.5",
        "@esbuild/linux-x64": "0.21.5",
        "@esbuild/netbsd-x64": "0.21.5",
        "@esbuild/openbsd-x64": "0.21.5",
        "@esbuild/sunos-x64": "0.21.5",
        "@esbuild/win32-arm64": "0.21.5",
        "@esbuild/win32-ia32": "0.21.5",
        "@esbuild/win32-x64": "0.21.5"
      }
    },
    "node_modules/esbuild-register": {
      "version": "3.6.0",
      "resolved": "https://registry.npmjs.org/esbuild-register/-/esbuild-register-3.6.0.tgz",
      "integrity": "sha512-H2/S7Pm8a9CL1uhp9OvjwrBh5Pvx0H8qVOxNu8Wed9Y7qv56MPtq+GGM8RJpq6glYJn9Wspr8uw7l55uyinNeg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "debug": "^4.3.4"
      },
      "peerDependencies": {
        "esbuild": ">=0.12 <1"
      }
    },
    "node_modules/escalade": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/escalade/-/escalade-3.2.0.tgz",
      "integrity": "sha512-WUj2qlxaQtO4g6Pq5c29GTcWGDyd8itL8zTlipgECz3JesAiiOKotd8JU6otB3PACgG6xkJUyVhboMS+bje/jA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/esprima": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/esprima/-/esprima-4.0.1.tgz",
      "integrity": "sha512-eGuFFw7Upda+g4p+QHvnW0RyTX/SVeJBDM/gCtMARO0cLuT2HcEKnTPvhjV6aGeqrCB/sbNop0Kszm0jsaWU4A==",
      "dev": true,
      "license": "BSD-2-Clause",
      "bin": {
        "esparse": "bin/esparse.js",
        "esvalidate": "bin/esvalidate.js"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/estree-walker": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/estree-walker/-/estree-walker-2.0.2.tgz",
      "integrity": "sha512-Rfkk/Mp/DL7JVje3u18FxFujQlTNR2q6QfMSMB7AvCBx91NGj/ba3kCfza0f6dVDbw7YlRf/nDrn7pQrCCyQ/w==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/esutils": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/esutils/-/esutils-2.0.3.tgz",
      "integrity": "sha512-kVscqXk4OCp68SZ0dkgEKVi6/8ij300KBWTJq32P/dYeWTSwK41WyTxalN1eRmA5Z9UU/LX9D7FWSmV9SAYx6g==",
      "dev": true,
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/fast-deep-equal": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/fast-deep-equal/-/fast-deep-equal-3.1.3.tgz",
      "integrity": "sha512-f3qQ9oQy9j2AhBe/H9VC91wLmKBCCU/gDOnKNAYG5hswO7BLKj09Hc5HYNz9cGI++xlpDCIgDaitVs03ATR84Q==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/fast-json-stable-stringify": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/fast-json-stable-stringify/-/fast-json-stable-stringify-2.1.0.tgz",
      "integrity": "sha512-lhd/wF+Lk98HZoTCtlVraHtfh5XYijIjalXck7saUtuanSDyLMxnHhSXEDJqHxD7msR8D0uCmqlkwjCV8xvwHw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/fast-uri": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/fast-uri/-/fast-uri-3.1.0.tgz",
      "integrity": "sha512-iPeeDKJSWf4IEOasVVrknXpaBV0IApz/gp7S2bb7Z4Lljbl2MGJRqInZiUrQwV16cpzw/D3S5j5Julj/gT52AA==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/fastify"
        },
        {
          "type": "opencollective",
          "url": "https://opencollective.com/fastify"
        }
      ],
      "license": "BSD-3-Clause"
    },
    "node_modules/fdir": {
      "version": "6.5.0",
      "resolved": "https://registry.npmjs.org/fdir/-/fdir-6.5.0.tgz",
      "integrity": "sha512-tIbYtZbucOs0BRGqPJkshJUYdL+SDH7dVM8gjy+ERp3WAUjLEFJE+02kanyHtwjWOnwrKYBiwAmM0p4kLJAnXg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12.0.0"
      },
      "peerDependencies": {
        "picomatch": "^3 || ^4"
      },
      "peerDependenciesMeta": {
        "picomatch": {
          "optional": true
        }
      }
    },
    "node_modules/filelist": {
      "version": "1.0.6",
      "resolved": "https://registry.npmjs.org/filelist/-/filelist-1.0.6.tgz",
      "integrity": "sha512-5giy2PkLYY1cP39p17Ech+2xlpTRL9HLspOfEgm0L6CwBXBTgsK5ou0JtzYuepxkaQ/tvhCFIJ5uXo0OrM2DxA==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "minimatch": "^5.0.1"
      }
    },
    "node_modules/filelist/node_modules/minimatch": {
      "version": "5.1.9",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-5.1.9.tgz",
      "integrity": "sha512-7o1wEA2RyMP7Iu7GNba9vc0RWWGACJOCZBJX2GJWip0ikV+wcOsgVuY9uE8CPiyQhkGFSlhuSkZPavN7u1c2Fw==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "brace-expansion": "^2.0.1"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/find-up": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/find-up/-/find-up-5.0.0.tgz",
      "integrity": "sha512-78/PXT1wlLLDgTzDs7sjq9hzz0vXD+zn+7wypEe4fXQxCmdmqfGsEPQxmiCSQI3ajFV91bVSsvNtrJRiW6nGng==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "locate-path": "^6.0.0",
        "path-exists": "^4.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/for-each": {
      "version": "0.3.5",
      "resolved": "https://registry.npmjs.org/for-each/-/for-each-0.3.5.tgz",
      "integrity": "sha512-dKx12eRCVIzqCxFGplyFKJMPvLEWgmNtUrpTiJIR5u97zEhRG8ySrtboPHZXx7daLxQVrl643cTzbab2tkQjxg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-callable": "^1.2.7"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/foreground-child": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/foreground-child/-/foreground-child-3.3.1.tgz",
      "integrity": "sha512-gIXjKqtFuWEgzFRJA9WCQeSJLZDjgJUOMCMzxtvFq/37KojM1BFGufqsCy0r4qSQmYLsZYMeyRqzIWOMup03sw==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "cross-spawn": "^7.0.6",
        "signal-exit": "^4.0.1"
      },
      "engines": {
        "node": ">=14"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/fs-extra": {
      "version": "9.1.0",
      "resolved": "https://registry.npmjs.org/fs-extra/-/fs-extra-9.1.0.tgz",
      "integrity": "sha512-hcg3ZmepS30/7BSFqRvoo3DOMQu7IjqxO5nCDt+zM9XWjb33Wg7ziNT+Qvqbuc3+gWpzO02JubVyk2G4Zvo1OQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "at-least-node": "^1.0.0",
        "graceful-fs": "^4.2.0",
        "jsonfile": "^6.0.1",
        "universalify": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/fsevents": {
      "version": "2.3.3",
      "resolved": "https://registry.npmjs.org/fsevents/-/fsevents-2.3.3.tgz",
      "integrity": "sha512-5xoDfX+fL7faATnagmWPpbFtwh/R77WmMMqqHGS65C3vvB0YHrgF+B1YmZ3441tMj5n63k0212XNoJwzlhffQw==",
      "dev": true,
      "hasInstallScript": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^8.16.0 || ^10.6.0 || >=11.0.0"
      }
    },
    "node_modules/function-bind": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/function-bind/-/function-bind-1.1.2.tgz",
      "integrity": "sha512-7XHNxH7qX9xG5mIwxkhumTox/MIRNcOgDrxWsMt2pAr23WHp6MrRlN7FBSFpCpr+oVO0F744iUgR82nJMfG2SA==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/function.prototype.name": {
      "version": "1.1.8",
      "resolved": "https://registry.npmjs.org/function.prototype.name/-/function.prototype.name-1.1.8.tgz",
      "integrity": "sha512-e5iwyodOHhbMr/yNrc7fDYG4qlbIvI5gajyzPnb5TCwyhjApznQh1BMFou9b30SevY43gCJKXycoCBjMbsuW0Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "functions-have-names": "^1.2.3",
        "hasown": "^2.0.2",
        "is-callable": "^1.2.7"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/functions-have-names": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/functions-have-names/-/functions-have-names-1.2.3.tgz",
      "integrity": "sha512-xckBUXyTIqT97tq2x2AMb+g163b5JFysYk0x4qxNFwbfQkmNZoiRHb6sPzI9/QV33WeuvVYBUIiD4NzNIyqaRQ==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/generator-function": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/generator-function/-/generator-function-2.0.1.tgz",
      "integrity": "sha512-SFdFmIJi+ybC0vjlHN0ZGVGHc3lgE0DxPAT0djjVg+kjOnSqclqmj0KQ7ykTOLP6YxoqOvuAODGdcHJn+43q3g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/gensync": {
      "version": "1.0.0-beta.2",
      "resolved": "https://registry.npmjs.org/gensync/-/gensync-1.0.0-beta.2.tgz",
      "integrity": "sha512-3hN7NaskYvMDLQY55gnW3NQ+mesEAepTqlg+VEbj7zzqEMBVNhzcGYYeqFo/TlYz6eQiFcp1HcsCZO+nGgS8zg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/get-intrinsic": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/get-intrinsic/-/get-intrinsic-1.3.0.tgz",
      "integrity": "sha512-9fSjSaos/fRIVIp+xSJlE6lfwhES7LNtKaCBIamHsjr2na1BiABJPo0mOjjz8GJDURarmCPGqaiVg5mfjb98CQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "es-define-property": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "function-bind": "^1.1.2",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "has-symbols": "^1.1.0",
        "hasown": "^2.0.2",
        "math-intrinsics": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/get-own-enumerable-property-symbols": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/get-own-enumerable-property-symbols/-/get-own-enumerable-property-symbols-3.0.2.tgz",
      "integrity": "sha512-I0UBV/XOz1XkIJHEUDMZAbzCThU/H8DxmSfmdGcKPnVhu2VfFqr34jr9777IyaTYvxjedWhqVIilEDsCdP5G6g==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/get-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/get-proto/-/get-proto-1.0.1.tgz",
      "integrity": "sha512-sTSfBjoXBp89JvIKIefqw7U2CCebsc74kiY6awiGogKtoSGbgjYE/G/+l9sF3MWFPNc9IcoOC4ODfKHfxFmp0g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/get-symbol-description": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/get-symbol-description/-/get-symbol-description-1.1.0.tgz",
      "integrity": "sha512-w9UMqWwJxHNOvoNzSJ2oPF5wvYcvP7jUvYzhp67yEhTi17ZDBBC1z9pTdGuzjD+EFIqLSYRweZjqfiPzQ06Ebg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/glob": {
      "version": "10.5.0",
      "resolved": "https://registry.npmjs.org/glob/-/glob-10.5.0.tgz",
      "integrity": "sha512-DfXN8DfhJ7NH3Oe7cFmu3NCu1wKbkReJ8TorzSAFbSKrlNaQSKfIzqYqVY8zlbs2NLBbWpRiU52GX2PbaBVNkg==",
      "deprecated": "Old versions of glob are not supported, and contain widely publicized security vulnerabilities, which have been fixed in the current version. Please update. Support for old versions may be purchased (at exorbitant rates) by contacting i@izs.me",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "foreground-child": "^3.1.0",
        "jackspeak": "^3.1.2",
        "minimatch": "^9.0.4",
        "minipass": "^7.1.2",
        "package-json-from-dist": "^1.0.0",
        "path-scurry": "^1.11.1"
      },
      "bin": {
        "glob": "dist/esm/bin.mjs"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/globalthis": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/globalthis/-/globalthis-1.0.4.tgz",
      "integrity": "sha512-DpLKbNU4WylpxJykQujfCcwYWiV/Jhm50Goo0wrVILAv5jOr9d+H+UR3PhSCD2rCCEIg0uc+G+muBTwD54JhDQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "define-properties": "^1.2.1",
        "gopd": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/gopd": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/gopd/-/gopd-1.2.0.tgz",
      "integrity": "sha512-ZUKRh6/kUFoAiTAtTYPZJ3hw9wNxx+BIBOijnlG9PnrJsCcSjs1wyyD6vJpaYtgnzDrKYRSqf3OO6Rfa93xsRg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/graceful-fs": {
      "version": "4.2.11",
      "resolved": "https://registry.npmjs.org/graceful-fs/-/graceful-fs-4.2.11.tgz",
      "integrity": "sha512-RbJ5/jmFcNNCcDV5o9eTnBLJ/HszWV0P73bc+Ff4nS/rJj+YaS6IGyiOL0VoBYX+l1Wrl3k63h/KrH+nhJ0XvQ==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/has-bigints": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/has-bigints/-/has-bigints-1.1.0.tgz",
      "integrity": "sha512-R3pbpkcIqv2Pm3dUwgjclDRVmWpTJW2DcMzcIhEXEx1oh/CEMObMm3KLmRJOdvhM7o4uQBnwr8pzRK2sJWIqfg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-property-descriptors": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/has-property-descriptors/-/has-property-descriptors-1.0.2.tgz",
      "integrity": "sha512-55JNKuIW+vq4Ke1BjOTjM2YctQIvCT7GFzHwmfZPGo5wnrgkid0YQtnAleFSqumZm4az3n2BS+erby5ipJdgrg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-define-property": "^1.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-proto": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/has-proto/-/has-proto-1.2.0.tgz",
      "integrity": "sha512-KIL7eQPfHQRC8+XluaIw7BHUwwqL19bQn4hzNgdr+1wXoU0KKj6rufu47lhY7KbJR2C6T6+PfyN0Ea7wkSS+qQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-symbols": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/has-symbols/-/has-symbols-1.1.0.tgz",
      "integrity": "sha512-1cDNdwJ2Jaohmb3sg4OmKaMBwuC48sYni5HUw2DvsC8LjGTLK9h+eb1X6RyuOHe4hT0ULCW68iomhjUoKUqlPQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-tostringtag": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/has-tostringtag/-/has-tostringtag-1.0.2.tgz",
      "integrity": "sha512-NqADB8VjPFLM2V0VvHUewwwsw0ZWBaIdgo+ieHtK3hasLz4qeCRjYcqfB6AQrBggRKppKF8L52/VqdVsO47Dlw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "has-symbols": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/hasown": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/hasown/-/hasown-2.0.2.tgz",
      "integrity": "sha512-0hJU9SCPvmMzIBdZFqNPXWa6dqh7WdH0cII9y+CyS8rG3nL48Bclra9HmKhVVUHyPWNH5Y7xDwAB7bfgSjkUMQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/hoist-non-react-statics": {
      "version": "3.3.2",
      "resolved": "https://registry.npmjs.org/hoist-non-react-statics/-/hoist-non-react-statics-3.3.2.tgz",
      "integrity": "sha512-/gGivxi8JPKWNm/W0jSmzcMPpfpPLc3dY/6GxhX2hQ9iGj3aDfklV4ET7NjKpSinLpJ5vafa9iiGIEZg10SfBw==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "react-is": "^16.7.0"
      }
    },
    "node_modules/hoist-non-react-statics/node_modules/react-is": {
      "version": "16.13.1",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-16.13.1.tgz",
      "integrity": "sha512-24e6ynE2H+OKt4kqsOvNd8kBpV65zoxbA4BVsEOB3ARVWQki/DHzaUoC5KuON/BiccDaCCTZBuOcfZs70kR8bQ==",
      "license": "MIT"
    },
    "node_modules/https-proxy-agent": {
      "version": "7.0.6",
      "resolved": "https://registry.npmjs.org/https-proxy-agent/-/https-proxy-agent-7.0.6.tgz",
      "integrity": "sha512-vK9P5/iUfdl95AI+JVyUuIcVtd4ofvtrOr3HNtM2yxC9bnMbEdp3x01OhQNnjb8IJYi38VlTE3mBXwcfvywuSw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "agent-base": "^7.1.2",
        "debug": "4"
      },
      "engines": {
        "node": ">= 14"
      }
    },
    "node_modules/idb": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/idb/-/idb-7.1.1.tgz",
      "integrity": "sha512-gchesWBzyvGHRO9W8tzUWFDycow5gwjvFKfyV9FF32Y7F50yZMp7mP+T2mJIWFx49zicqyC4uefHM17o6xKIVQ==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/index-to-position": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/index-to-position/-/index-to-position-1.2.0.tgz",
      "integrity": "sha512-Yg7+ztRkqslMAS2iFaU+Oa4KTSidr63OsFGlOrJoW981kIYO3CGCS3wA95P1mUi/IVSJkn0D479KTJpVpvFNuw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/inherits": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/inherits/-/inherits-2.0.4.tgz",
      "integrity": "sha512-k/vGaX4/Yla3WzyMCvTQOXYeIHvqOKtnqBduzTHpzpQZzAskKMhZ2K+EnBiSM9zGSoIFeMpXKxa4dYeZIQqewQ==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/internal-slot": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/internal-slot/-/internal-slot-1.1.0.tgz",
      "integrity": "sha512-4gd7VpWNQNB4UKKCFFVcp1AVv+FMOgs9NKzjHKusc8jTMhd5eL1NqQqOpE0KzMds804/yHlglp3uxgluOqAPLw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "hasown": "^2.0.2",
        "side-channel": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/is-arguments": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/is-arguments/-/is-arguments-1.2.0.tgz",
      "integrity": "sha512-7bVbi0huj/wrIAOzb8U1aszg9kdi3KN/CyU19CTI7tAoZYEZoL9yCDXpbXN+uPsuWnP02cyug1gleqq+TU+YCA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-array-buffer": {
      "version": "3.0.5",
      "resolved": "https://registry.npmjs.org/is-array-buffer/-/is-array-buffer-3.0.5.tgz",
      "integrity": "sha512-DDfANUiiG2wC1qawP66qlTugJeL5HyzMpfr8lLK+jMQirGzNod0B12cFB/9q838Ru27sBwfw78/rdoU7RERz6A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "get-intrinsic": "^1.2.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-async-function": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/is-async-function/-/is-async-function-2.1.1.tgz",
      "integrity": "sha512-9dgM/cZBnNvjzaMYHVoxxfPj2QXt22Ev7SuuPrs+xav0ukGB0S6d4ydZdEiM48kLx5kDV+QBPrpVnFyefL8kkQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "async-function": "^1.0.0",
        "call-bound": "^1.0.3",
        "get-proto": "^1.0.1",
        "has-tostringtag": "^1.0.2",
        "safe-regex-test": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-bigint": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/is-bigint/-/is-bigint-1.1.0.tgz",
      "integrity": "sha512-n4ZT37wG78iz03xPRKJrHTdZbe3IicyucEtdRsV5yglwc3GyUfbAfpSeD0FJ41NbUNSt5wbhqfp1fS+BgnvDFQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "has-bigints": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-boolean-object": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/is-boolean-object/-/is-boolean-object-1.2.2.tgz",
      "integrity": "sha512-wa56o2/ElJMYqjCjGkXri7it5FbebW5usLw/nPmCMs5DeZ7eziSYZhSmPRn0txqeW4LnAmQQU7FgqLpsEFKM4A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-callable": {
      "version": "1.2.7",
      "resolved": "https://registry.npmjs.org/is-callable/-/is-callable-1.2.7.tgz",
      "integrity": "sha512-1BC0BVFhS/p0qtw6enp8e+8OD0UrK0oFLztSjNzhcKA3WDuJxxAPXzPuPtKkjEY9UUoEWlX/8fgKeu2S8i9JTA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-core-module": {
      "version": "2.16.1",
      "resolved": "https://registry.npmjs.org/is-core-module/-/is-core-module-2.16.1.tgz",
      "integrity": "sha512-UfoeMA6fIJ8wTYFEUjelnaGI67v6+N7qXJEvQuIGa99l4xsCruSYOVSQ0uPANn4dAzm8lkYPaKLrrijLq7x23w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-data-view": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/is-data-view/-/is-data-view-1.0.2.tgz",
      "integrity": "sha512-RKtWF8pGmS87i2D6gqQu/l7EYRlVdfzemCJN/P3UOs//x1QE7mfhvzHIApBTRf7axvT6DMGwSwBXYCT0nfB9xw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "get-intrinsic": "^1.2.6",
        "is-typed-array": "^1.1.13"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-date-object": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/is-date-object/-/is-date-object-1.1.0.tgz",
      "integrity": "sha512-PwwhEakHVKTdRNVOw+/Gyh0+MzlCl4R6qKvkhuvLtPMggI1WAHt9sOwZxQLSGpUaDnrdyDsomoRgNnCfKNSXXg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-docker": {
      "version": "2.2.1",
      "resolved": "https://registry.npmjs.org/is-docker/-/is-docker-2.2.1.tgz",
      "integrity": "sha512-F+i2BKsFrH66iaUFc0woD8sLy8getkwTwtOBjvs56Cx4CgJDeKQeqfz8wAYiSb8JOprWhHH5p77PbmYCvvUuXQ==",
      "dev": true,
      "license": "MIT",
      "bin": {
        "is-docker": "cli.js"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/is-finalizationregistry": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-finalizationregistry/-/is-finalizationregistry-1.1.1.tgz",
      "integrity": "sha512-1pC6N8qWJbWoPtEjgcL2xyhQOP491EQjeUo3qTKcmV8YSDDJrOepfG8pcC7h/QgnQHYSv0mJ3Z/ZWxmatVrysg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-fullwidth-code-point": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/is-fullwidth-code-point/-/is-fullwidth-code-point-3.0.0.tgz",
      "integrity": "sha512-zymm5+u+sCsSWyD9qNaejV3DFvhCKclKdizYaJUuHA83RLjb7nSuGnddCHGv0hk+KY7BMAlsWeK4Ueg6EV6XQg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/is-generator-function": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/is-generator-function/-/is-generator-function-1.1.2.tgz",
      "integrity": "sha512-upqt1SkGkODW9tsGNG5mtXTXtECizwtS2kA161M+gJPc1xdb/Ax629af6YrTwcOeQHbewrPNlE5Dx7kzvXTizA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.4",
        "generator-function": "^2.0.0",
        "get-proto": "^1.0.1",
        "has-tostringtag": "^1.0.2",
        "safe-regex-test": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-map": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/is-map/-/is-map-2.0.3.tgz",
      "integrity": "sha512-1Qed0/Hr2m+YqxnM09CjA2d/i6YZNfF6R2oRAOj36eUdS6qIV/huPJNSEpKbupewFs+ZsJlxsjjPbc0/afW6Lw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-module": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/is-module/-/is-module-1.0.0.tgz",
      "integrity": "sha512-51ypPSPCoTEIN9dy5Oy+h4pShgJmPCygKfyRCISBI+JoWT/2oJvK8QPxmwv7b/p239jXrm9M1mlQbyKJ5A152g==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/is-negative-zero": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/is-negative-zero/-/is-negative-zero-2.0.3.tgz",
      "integrity": "sha512-5KoIu2Ngpyek75jXodFvnafB6DJgr3u8uuK0LEZJjrU19DrMD3EVERaR8sjz8CCGgpZvxPl9SuE1GMVPFHx1mw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-number-object": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-number-object/-/is-number-object-1.1.1.tgz",
      "integrity": "sha512-lZhclumE1G6VYD8VHe35wFaIif+CTy5SJIi5+3y4psDgWu4wPDoBhF8NxUOinEc7pHgiTsT6MaBb92rKhhD+Xw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-obj": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/is-obj/-/is-obj-1.0.1.tgz",
      "integrity": "sha512-l4RyHgRqGN4Y3+9JHVrNqO+tN0rV5My76uW5/nuO4K1b6vw5G8d/cmFjP9tRfEsdhZNt0IFdZuK/c2Vr4Nb+Qg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-regex": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/is-regex/-/is-regex-1.2.1.tgz",
      "integrity": "sha512-MjYsKHO5O7mCsmRGxWcLWheFqN9DJ/2TmngvjKXihe6efViPqc274+Fx/4fYj/r03+ESvBdTXK0V6tA3rgez1g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "gopd": "^1.2.0",
        "has-tostringtag": "^1.0.2",
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-regexp": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/is-regexp/-/is-regexp-1.0.0.tgz",
      "integrity": "sha512-7zjFAPO4/gwyQAAgRRmqeEeyIICSdmCqa3tsVHMdBzaXXRiqopZL4Cyghg/XulGWrtABTpbnYYzzIRffLkP4oA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-set": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/is-set/-/is-set-2.0.3.tgz",
      "integrity": "sha512-iPAjerrse27/ygGLxw+EBR9agv9Y6uLeYVJMu+QNCoouJ1/1ri0mGrcWpfCqFZuzzx3WjtwxG098X+n4OuRkPg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-shared-array-buffer": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/is-shared-array-buffer/-/is-shared-array-buffer-1.0.4.tgz",
      "integrity": "sha512-ISWac8drv4ZGfwKl5slpHG9OwPNty4jOWPRIhBpxOoD+hqITiwuipOQ2bNthAzwA3B4fIjO4Nln74N0S9byq8A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-stream": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/is-stream/-/is-stream-2.0.1.tgz",
      "integrity": "sha512-hFoiJiTl63nn+kstHGBtewWSKnQLpyb155KHheA1l39uvtO9nWIop1p3udqPcUd/xbF1VLMO4n7OI6p7RbngDg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/is-string": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-string/-/is-string-1.1.1.tgz",
      "integrity": "sha512-BtEeSsoaQjlSPBemMQIrY1MY0uM6vnS1g5fmufYOtnxLGUZM2178PKbhsk7Ffv58IX+ZtcvoGwccYsh0PglkAA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-symbol": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-symbol/-/is-symbol-1.1.1.tgz",
      "integrity": "sha512-9gGx6GTtCQM73BgmHQXfDmLtfjjTUDSyoxTCbp5WtoixAhfgsDirWIcVQ/IHpvI5Vgd5i/J5F7B9cN/WlVbC/w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "has-symbols": "^1.1.0",
        "safe-regex-test": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-typed-array": {
      "version": "1.1.15",
      "resolved": "https://registry.npmjs.org/is-typed-array/-/is-typed-array-1.1.15.tgz",
      "integrity": "sha512-p3EcsicXjit7SaskXHs1hA91QxgTw46Fv6EFKKGS5DRFLD8yKnohjF3hxoju94b/OcMZoQukzpPpBE9uLVKzgQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "which-typed-array": "^1.1.16"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-weakmap": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/is-weakmap/-/is-weakmap-2.0.2.tgz",
      "integrity": "sha512-K5pXYOm9wqY1RgjpL3YTkF39tni1XajUIkawTLUo9EZEVUFga5gSQJF8nNS7ZwJQ02y+1YCNYcMh+HIf1ZqE+w==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-weakref": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-weakref/-/is-weakref-1.1.1.tgz",
      "integrity": "sha512-6i9mGWSlqzNMEqpCp93KwRS1uUOodk2OJ6b+sq7ZPDSy2WuI5NFIxp/254TytR8ftefexkWn5xNiHUNpPOfSew==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-weakset": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/is-weakset/-/is-weakset-2.0.4.tgz",
      "integrity": "sha512-mfcwb6IzQyOKTs84CQMrOwW4gQcaTOAWJ0zzJCl2WSPDrWk/OzDaImWFH3djXhb24g4eudZfLRozAvPGw4d9hQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "get-intrinsic": "^1.2.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-wsl": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/is-wsl/-/is-wsl-2.2.0.tgz",
      "integrity": "sha512-fKzAra0rGJUUBwGBgNkHZuToZcn+TtXHpeCgmkMJMMYx1sQDYaCSyjJBSCa2nH1DGm7s3n1oBnohoVTBaN7Lww==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-docker": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/isarray": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/isarray/-/isarray-2.0.5.tgz",
      "integrity": "sha512-xHjhDr3cNBK0BzdUJSPXZntQUx/mwMS5Rw4A7lPJ90XGAO6ISP/ePDNuo0vhqOZU+UD5JoodwCAAoZQd3FeAKw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/isexe": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/isexe/-/isexe-2.0.0.tgz",
      "integrity": "sha512-RHxMLp9lnKHGHRng9QFhRCMbYAcVpn69smSGcq3f36xjgVVWThj4qqLbTLlq7Ssj8B+fIQ1EuCEGI2lKsyQeIw==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/jackspeak": {
      "version": "3.4.3",
      "resolved": "https://registry.npmjs.org/jackspeak/-/jackspeak-3.4.3.tgz",
      "integrity": "sha512-OGlZQpz2yfahA/Rd1Y8Cd9SIEsqvXkLVoSw/cgwhnhFMDbsQFeZYoJJ7bIZBS9BcamUW96asq/npPWugM+RQBw==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "@isaacs/cliui": "^8.0.2"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      },
      "optionalDependencies": {
        "@pkgjs/parseargs": "^0.11.0"
      }
    },
    "node_modules/jake": {
      "version": "10.9.4",
      "resolved": "https://registry.npmjs.org/jake/-/jake-10.9.4.tgz",
      "integrity": "sha512-wpHYzhxiVQL+IV05BLE2Xn34zW1S223hvjtqk0+gsPrwd/8JNLXJgZZM/iPFsYc1xyphF+6M6EvdE5E9MBGkDA==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "async": "^3.2.6",
        "filelist": "^1.0.4",
        "picocolors": "^1.1.1"
      },
      "bin": {
        "jake": "bin/cli.js"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/js-levenshtein": {
      "version": "1.1.6",
      "resolved": "https://registry.npmjs.org/js-levenshtein/-/js-levenshtein-1.1.6.tgz",
      "integrity": "sha512-X2BB11YZtrRqY4EnQcLX5Rh373zbK4alC1FW7D7MBhL2gtcC17cTnr6DmfHZeS0s2rTHjUTMMHfG7gO8SSdw+g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/js-tokens": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/js-tokens/-/js-tokens-4.0.0.tgz",
      "integrity": "sha512-RdJUflcE3cUzKiMqQgsCu06FPu9UdIJO0beYbPhHN4k6apgJtifcoCtT9bcxOpYBtpD2kCM6Sbzg4CausW/PKQ==",
      "license": "MIT"
    },
    "node_modules/js-yaml": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/js-yaml/-/js-yaml-4.1.1.tgz",
      "integrity": "sha512-qQKT4zQxXl8lLwBtHMWwaTcGfFOZviOJet3Oy/xmGk2gZH677CJM9EvtfdSkgWcATZhj/55JZ0rmy3myCT5lsA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "argparse": "^2.0.1"
      },
      "bin": {
        "js-yaml": "bin/js-yaml.js"
      }
    },
    "node_modules/jsdoc-type-pratt-parser": {
      "version": "4.8.0",
      "resolved": "https://registry.npmjs.org/jsdoc-type-pratt-parser/-/jsdoc-type-pratt-parser-4.8.0.tgz",
      "integrity": "sha512-iZ8Bdb84lWRuGHamRXFyML07r21pcwBrLkHEuHgEY5UbCouBwv7ECknDRKzsQIXMiqpPymqtIf8TC/shYKB5rw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12.0.0"
      }
    },
    "node_modules/jsesc": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/jsesc/-/jsesc-3.1.0.tgz",
      "integrity": "sha512-/sM3dO2FOzXjKQhJuo0Q173wf2KOo8t4I8vHy6lF9poUp7bKT0/NHE8fPX23PwfhnykfqnC2xRxOnVw5XuGIaA==",
      "dev": true,
      "license": "MIT",
      "bin": {
        "jsesc": "bin/jsesc"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/json-schema": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/json-schema/-/json-schema-0.4.0.tgz",
      "integrity": "sha512-es94M3nTIfsEPisRafak+HDLfHXnKBhV3vU5eqPcS3flIWqcxJWgXHXiey3YrpaNsanY5ei1VoYEbOzijuq9BA==",
      "dev": true,
      "license": "(AFL-2.1 OR BSD-3-Clause)"
    },
    "node_modules/json-schema-traverse": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-1.0.0.tgz",
      "integrity": "sha512-NM8/P9n3XjXhIZn1lLhkFaACTOURQXjWhV4BA/RnOv8xvgqtqpAX9IO4mRQxSx1Rlo4tqzeqb0sOlruaOy3dug==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/json2mq": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/json2mq/-/json2mq-0.2.0.tgz",
      "integrity": "sha512-SzoRg7ux5DWTII9J2qkrZrqV1gt+rTaoufMxEzXbS26Uid0NwaJd123HcoB80TgubEppxxIGdNxCx50fEoEWQA==",
      "license": "MIT",
      "dependencies": {
        "string-convert": "^0.2.0"
      }
    },
    "node_modules/json5": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/json5/-/json5-2.2.3.tgz",
      "integrity": "sha512-XmOWe7eyHYH14cLdVPoyg+GOH3rYX++KpzrylJwSW98t3Nk+U8XOl8FWKOgwtzdb8lXGf6zYwDUzeHMWfxasyg==",
      "dev": true,
      "license": "MIT",
      "bin": {
        "json5": "lib/cli.js"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/jsonfile": {
      "version": "6.2.0",
      "resolved": "https://registry.npmjs.org/jsonfile/-/jsonfile-6.2.0.tgz",
      "integrity": "sha512-FGuPw30AdOIUTRMC2OMRtQV+jkVj2cfPqSeWXv1NEAJ1qZ5zb1X6z1mFhbfOB/iy3ssJCD+3KuZ8r8C3uVFlAg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "universalify": "^2.0.0"
      },
      "optionalDependencies": {
        "graceful-fs": "^4.1.6"
      }
    },
    "node_modules/jsonpointer": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/jsonpointer/-/jsonpointer-5.0.1.tgz",
      "integrity": "sha512-p/nXbhSEcu3pZRdkW1OfJhpsVtW1gd4Wa1fnQc9YLiTfAjn0312eMKimbdIQzuZl9aa9xUGaRlP9T/CJE/ditQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/leven": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/leven/-/leven-3.1.0.tgz",
      "integrity": "sha512-qsda+H8jTaUaN/x5vzW2rzc+8Rw4TAQ/4KjB46IwK5VH+IlVeeeje/EoZRpiXvIqjFgK84QffqPztGI3VBLG1A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/locate-path": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/locate-path/-/locate-path-6.0.0.tgz",
      "integrity": "sha512-iPZK6eYjbxRu3uB4/WZ3EsEIMJFMqAoopl3R+zuq0UjcAm/MO6KCweDgPfP3elTztoKP3KtnVHxTn2NHBSDVUw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "p-locate": "^5.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/lodash": {
      "version": "4.17.23",
      "resolved": "https://registry.npmjs.org/lodash/-/lodash-4.17.23.tgz",
      "integrity": "sha512-LgVTMpQtIopCi79SJeDiP0TfWi5CNEc/L/aRdTh3yIvmZXTnheWpKjSZhnvMl8iXbC1tFg9gdHHDMLoV7CnG+w==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/lodash.debounce": {
      "version": "4.0.8",
      "resolved": "https://registry.npmjs.org/lodash.debounce/-/lodash.debounce-4.0.8.tgz",
      "integrity": "sha512-FT1yDzDYEoYWhnSGnpE/4Kj1fLZkDFyqRb7fNt6FdYOSxlUWAtp42Eh6Wb0rGIv/m9Bgo7x4GhQbm5Ys4SG5ow==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/lodash.sortby": {
      "version": "4.7.0",
      "resolved": "https://registry.npmjs.org/lodash.sortby/-/lodash.sortby-4.7.0.tgz",
      "integrity": "sha512-HDWXG8isMntAyRF5vZ7xKuEvOhT4AhlRt/3czTSjvGUxjYCBVRQY48ViDHyfYz9VIoBkW4TMGQNapx+l3RUwdA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/loose-envify": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/loose-envify/-/loose-envify-1.4.0.tgz",
      "integrity": "sha512-lyuxPGr/Wfhrlem2CL/UcnUc1zcqKAImBDzukY7Y5F/yQiNdko6+fRLevlw1HgMySw7f611UIY408EtxRSoK3Q==",
      "license": "MIT",
      "dependencies": {
        "js-tokens": "^3.0.0 || ^4.0.0"
      },
      "bin": {
        "loose-envify": "cli.js"
      }
    },
    "node_modules/lru-cache": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/lru-cache/-/lru-cache-5.1.1.tgz",
      "integrity": "sha512-KpNARQA3Iwv+jTA0utUVVbrh+Jlrr1Fv0e56GGzAFOXN7dk/FviaDW8LHmK52DlcH4WP2n6gI8vN1aesBFgo9w==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "yallist": "^3.0.2"
      }
    },
    "node_modules/magic-string": {
      "version": "0.30.21",
      "resolved": "https://registry.npmjs.org/magic-string/-/magic-string-0.30.21.tgz",
      "integrity": "sha512-vd2F4YUyEXKGcLHoq+TEyCjxueSeHnFxyyjNp80yg0XV4vUhnDer/lvvlqM/arB5bXQN5K2/3oinyCRyx8T2CQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/sourcemap-codec": "^1.5.5"
      }
    },
    "node_modules/map-or-similar": {
      "version": "1.5.0",
      "resolved": "https://registry.npmjs.org/map-or-similar/-/map-or-similar-1.5.0.tgz",
      "integrity": "sha512-0aF7ZmVon1igznGI4VS30yugpduQW3y3GkcgGJOp7d8x8QrizhigUxjI/m2UojsXXto+jLAH3KSz+xOJTiORjg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/math-intrinsics": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/math-intrinsics/-/math-intrinsics-1.1.0.tgz",
      "integrity": "sha512-/IXtbwEk5HTPyEwyKX6hGkYXxM9nbj64B+ilVJnC/R6B0pH5G4V3b0pVbL7DBj4tkhBAppbQUlf6F6Xl9LHu1g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/memoizerific": {
      "version": "1.11.3",
      "resolved": "https://registry.npmjs.org/memoizerific/-/memoizerific-1.11.3.tgz",
      "integrity": "sha512-/EuHYwAPdLtXwAwSZkh/Gutery6pD2KYd44oQLhAvQp/50mpyduZh8Q7PYHXTCJ+wuXxt7oij2LXyIJOOYFPog==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "map-or-similar": "^1.5.0"
      }
    },
    "node_modules/minimatch": {
      "version": "9.0.9",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-9.0.9.tgz",
      "integrity": "sha512-OBwBN9AL4dqmETlpS2zasx+vTeWclWzkblfZk7KTA5j3jeOONz/tRCnZomUyvNg83wL5Zv9Ss6HMJXAgL8R2Yg==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "brace-expansion": "^2.0.2"
      },
      "engines": {
        "node": ">=16 || 14 >=14.17"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/minimist": {
      "version": "1.2.8",
      "resolved": "https://registry.npmjs.org/minimist/-/minimist-1.2.8.tgz",
      "integrity": "sha512-2yyAR8qBkN3YuheJanUpWC5U3bb5osDywNB8RzDVlDwDHbocAJveqqj1u8+SVD7jkWT4yvsHCpWqqWqAxb0zCA==",
      "dev": true,
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/minipass": {
      "version": "7.1.3",
      "resolved": "https://registry.npmjs.org/minipass/-/minipass-7.1.3.tgz",
      "integrity": "sha512-tEBHqDnIoM/1rXME1zgka9g6Q2lcoCkxHLuc7ODJ5BxbP5d4c2Z5cGgtXAku59200Cx7diuHTOYfSBD8n6mm8A==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "engines": {
        "node": ">=16 || 14 >=14.17"
      }
    },
    "node_modules/ms": {
      "version": "2.1.3",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.1.3.tgz",
      "integrity": "sha512-6FlzubTLZG3J2a/NVCAleEhjzq5oxgHyaCU9yYXvcLsvoVaHJq/s5xXI6/XXP6tz7R9xAOtHnSO/tXtF3WRTlA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/nanoid": {
      "version": "3.3.11",
      "resolved": "https://registry.npmjs.org/nanoid/-/nanoid-3.3.11.tgz",
      "integrity": "sha512-N8SpfPUnUp1bK+PMYW8qSWdl9U+wwNWI4QKxOYDy9JAro3WMX7p2OeVRF9v+347pnakNevPmiHhNmZ2HbFA76w==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "bin": {
        "nanoid": "bin/nanoid.cjs"
      },
      "engines": {
        "node": "^10 || ^12 || ^13.7 || ^14 || >=15.0.1"
      }
    },
    "node_modules/node-releases": {
      "version": "2.0.36",
      "resolved": "https://registry.npmjs.org/node-releases/-/node-releases-2.0.36.tgz",
      "integrity": "sha512-TdC8FSgHz8Mwtw9g5L4gR/Sh9XhSP/0DEkQxfEFXOpiul5IiHgHan2VhYYb6agDSfp4KuvltmGApc8HMgUrIkA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/object-inspect": {
      "version": "1.13.4",
      "resolved": "https://registry.npmjs.org/object-inspect/-/object-inspect-1.13.4.tgz",
      "integrity": "sha512-W67iLl4J2EXEGTbfeHCffrjDfitvLANg0UlX3wFUUSTx92KXRFegMHUVgSqE+wvhAbi4WqjGg9czysTV2Epbew==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/object-keys": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/object-keys/-/object-keys-1.1.1.tgz",
      "integrity": "sha512-NuAESUOUMrlIXOfHKzD6bpPu3tYt3xvjNdRIQ+FeT0lNb4K8WR70CaDxhuNguS2XG+GjkyMwOzsN5ZktImfhLA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/object.assign": {
      "version": "4.1.7",
      "resolved": "https://registry.npmjs.org/object.assign/-/object.assign-4.1.7.tgz",
      "integrity": "sha512-nK28WOo+QIjBkDduTINE4JkF/UJJKyf2EJxvJKfblDpyg0Q+pkOHNTL0Qwy6NP6FhE/EnzV73BxxqcJaXY9anw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0",
        "has-symbols": "^1.1.0",
        "object-keys": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/open": {
      "version": "8.4.2",
      "resolved": "https://registry.npmjs.org/open/-/open-8.4.2.tgz",
      "integrity": "sha512-7x81NCL719oNbsq/3mh+hVrAWmFuEYUqrq/Iw3kUzH8ReypT9QQ0BLoJS7/G9k6N81XjW4qHWtjWwe/9eLy1EQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "define-lazy-prop": "^2.0.0",
        "is-docker": "^2.1.1",
        "is-wsl": "^2.2.0"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/openapi-typescript": {
      "version": "7.13.0",
      "resolved": "https://registry.npmjs.org/openapi-typescript/-/openapi-typescript-7.13.0.tgz",
      "integrity": "sha512-EFP392gcqXS7ntPvbhBzbF8TyBA+baIYEm791Hy5YkjDYKTnk/Tn5OQeKm5BIZvJihpp8Zzr4hzx0Irde1LNGQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@redocly/openapi-core": "^1.34.6",
        "ansi-colors": "^4.1.3",
        "change-case": "^5.4.4",
        "parse-json": "^8.3.0",
        "supports-color": "^10.2.2",
        "yargs-parser": "^21.1.1"
      },
      "bin": {
        "openapi-typescript": "bin/cli.js"
      },
      "peerDependencies": {
        "typescript": "^5.x"
      }
    },
    "node_modules/own-keys": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/own-keys/-/own-keys-1.0.1.tgz",
      "integrity": "sha512-qFOyK5PjiWZd+QQIh+1jhdb9LpxTF0qs7Pm8o5QHYZ0M3vKqSqzsZaEB6oWlxZ+q2sJBMI/Ktgd2N5ZwQoRHfg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "get-intrinsic": "^1.2.6",
        "object-keys": "^1.1.1",
        "safe-push-apply": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/p-limit": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/p-limit/-/p-limit-3.1.0.tgz",
      "integrity": "sha512-TYOanM3wGwNGsZN2cVTYPArw454xnXj5qmWF1bEoAc4+cU/ol7GVh7odevjp1FNHduHc3KZMcFduxU5Xc6uJRQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "yocto-queue": "^0.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/p-locate": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/p-locate/-/p-locate-5.0.0.tgz",
      "integrity": "sha512-LaNjtRWUBY++zB5nE/NwcaoMylSPk+S+ZHNB1TzdbMJMny6dynpAGt7X/tl/QYq3TIeE6nxHppbo2LGymrG5Pw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "p-limit": "^3.0.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/package-json-from-dist": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/package-json-from-dist/-/package-json-from-dist-1.0.1.tgz",
      "integrity": "sha512-UEZIS3/by4OC8vL3P2dTXRETpebLI2NiI5vIrjaD/5UtrkFX/tNbwjTSRAGC/+7CAo2pIcBaRgWmcBBHcsaCIw==",
      "dev": true,
      "license": "BlueOak-1.0.0"
    },
    "node_modules/parse-json": {
      "version": "8.3.0",
      "resolved": "https://registry.npmjs.org/parse-json/-/parse-json-8.3.0.tgz",
      "integrity": "sha512-ybiGyvspI+fAoRQbIPRddCcSTV9/LsJbf0e/S85VLowVGzRmokfneg2kwVW/KU5rOXrPSbF1qAKPMgNTqqROQQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.26.2",
        "index-to-position": "^1.1.0",
        "type-fest": "^4.39.1"
      },
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/path-exists": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/path-exists/-/path-exists-4.0.0.tgz",
      "integrity": "sha512-ak9Qy5Q7jYb2Wwcey5Fpvg2KoAc/ZIhLSLOSBmRmygPsGwkVVt0fZa0qrtMz+m6tJTAHfZQ8FnmB4MG4LWy7/w==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-key": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/path-key/-/path-key-3.1.1.tgz",
      "integrity": "sha512-ojmeN0qd+y0jszEtoY48r0Peq5dwMEkIlCOu6Q5f41lfkswXuKtYrhgoTpLnyIcHm24Uhqx+5Tqm2InSwLhE6Q==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-parse": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/path-parse/-/path-parse-1.0.7.tgz",
      "integrity": "sha512-LDJzPVEEEPR+y48z93A0Ed0yXb8pAByGWo/k5YYdYgpY2/2EsOsksJrq7lOHxryrVOn1ejG6oAp8ahvOIQD8sw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/path-scurry": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/path-scurry/-/path-scurry-1.11.1.tgz",
      "integrity": "sha512-Xa4Nw17FS9ApQFJ9umLiJS4orGjm7ZzwUrwamcGQuHSzDyth9boKDaycYdDcZDuqYATXw4HFXgaqWTctW/v1HA==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "lru-cache": "^10.2.0",
        "minipass": "^5.0.0 || ^6.0.2 || ^7.0.0"
      },
      "engines": {
        "node": ">=16 || 14 >=14.18"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/path-scurry/node_modules/lru-cache": {
      "version": "10.4.3",
      "resolved": "https://registry.npmjs.org/lru-cache/-/lru-cache-10.4.3.tgz",
      "integrity": "sha512-JNAzZcXrCt42VGLuYz0zfAzDfAvJWW6AfYlDBQyDV5DClI2m5sAmK+OIO7s59XfsRsWHp02jAJrRadPRGTt6SQ==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/picocolors": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-1.1.1.tgz",
      "integrity": "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/picomatch": {
      "version": "4.0.3",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-4.0.3.tgz",
      "integrity": "sha512-5gTmgEY/sqK6gFXLIsQNH19lWb4ebPDLA4SdLP7dsWkIXHWlG66oPuVvXSGFPppYZz8ZDZq0dYYrbHfBCVUb1Q==",
      "dev": true,
      "license": "MIT",
      "peer": true,
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/playwright": {
      "version": "1.58.2",
      "resolved": "https://registry.npmjs.org/playwright/-/playwright-1.58.2.tgz",
      "integrity": "sha512-vA30H8Nvkq/cPBnNw4Q8TWz1EJyqgpuinBcHET0YVJVFldr8JDNiU9LaWAE1KqSkRYazuaBhTpB5ZzShOezQ6A==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "playwright-core": "1.58.2"
      },
      "bin": {
        "playwright": "cli.js"
      },
      "engines": {
        "node": ">=18"
      },
      "optionalDependencies": {
        "fsevents": "2.3.2"
      }
    },
    "node_modules/playwright-core": {
      "version": "1.58.2",
      "resolved": "https://registry.npmjs.org/playwright-core/-/playwright-core-1.58.2.tgz",
      "integrity": "sha512-yZkEtftgwS8CsfYo7nm0KE8jsvm6i/PTgVtB8DL726wNf6H2IMsDuxCpJj59KDaxCtSnrWan2AeDqM7JBaultg==",
      "dev": true,
      "license": "Apache-2.0",
      "bin": {
        "playwright-core": "cli.js"
      },
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/playwright/node_modules/fsevents": {
      "version": "2.3.2",
      "resolved": "https://registry.npmjs.org/fsevents/-/fsevents-2.3.2.tgz",
      "integrity": "sha512-xiqMQR4xAeHTuB9uWm+fFRcIOgKBMiOBP+eXiyT7jsgVCq1bkVygt00oASowB7EdtpOHaaPgKt812P9ab+DDKA==",
      "dev": true,
      "hasInstallScript": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^8.16.0 || ^10.6.0 || >=11.0.0"
      }
    },
    "node_modules/pluralize": {
      "version": "8.0.0",
      "resolved": "https://registry.npmjs.org/pluralize/-/pluralize-8.0.0.tgz",
      "integrity": "sha512-Nc3IT5yHzflTfbjgqWcCPpo7DaKy4FnpB0l/zCAW0Tc7jxAiuqSxHasntB3D7887LSrA93kDJ9IXovxJYxyLCA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/polished": {
      "version": "4.3.1",
      "resolved": "https://registry.npmjs.org/polished/-/polished-4.3.1.tgz",
      "integrity": "sha512-OBatVyC/N7SCW/FaDHrSd+vn0o5cS855TOmYi4OkdWUMSJCET/xip//ch8xGUvtr3i44X9LVyWwQlRMTN3pwSA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.17.8"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/possible-typed-array-names": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/possible-typed-array-names/-/possible-typed-array-names-1.1.0.tgz",
      "integrity": "sha512-/+5VFTchJDoVj3bhoqi6UeymcD00DAwb1nJwamzPvHEszJ4FpF6SNNbUbOS8yI56qHzdV8eK0qEfOSiodkTdxg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/postcss": {
      "version": "8.5.8",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-8.5.8.tgz",
      "integrity": "sha512-OW/rX8O/jXnm82Ey1k44pObPtdblfiuWnrd8X7GJ7emImCOstunGbXUpp7HdBrFQX6rJzn3sPT397Wp5aCwCHg==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/postcss"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "nanoid": "^3.3.11",
        "picocolors": "^1.1.1",
        "source-map-js": "^1.2.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      }
    },
    "node_modules/pretty-bytes": {
      "version": "6.1.1",
      "resolved": "https://registry.npmjs.org/pretty-bytes/-/pretty-bytes-6.1.1.tgz",
      "integrity": "sha512-mQUvGU6aUFQ+rNvTIAcZuWGRT9a6f6Yrg9bHs4ImKF+HZCEK+plBvnAZYSIQztknZF2qnzNtr6F8s0+IuptdlQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^14.13.1 || >=16.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/process": {
      "version": "0.11.10",
      "resolved": "https://registry.npmjs.org/process/-/process-0.11.10.tgz",
      "integrity": "sha512-cdGef/drWFoydD1JsMzuFf8100nZl+GT+yacc2bEced5f9Rjk4z+WtFUTBu9PhOi9j/jfmBPu0mMEY4wIdAF8A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.6.0"
      }
    },
    "node_modules/punycode": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/punycode/-/punycode-2.3.1.tgz",
      "integrity": "sha512-vYt7UD1U9Wg6138shLtLOvdAu+8DsC/ilFtEVHcH+wydcSpNE20AfSOduf6MkRFahL5FY7X1oU7nKVZFtfq8Fg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/randombytes": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/randombytes/-/randombytes-2.1.0.tgz",
      "integrity": "sha512-vYl3iOX+4CKUWuxGi9Ukhie6fsqXqS9FE2Zaic4tNFD2N2QQaXOMFbuKK4QmDHC0JO6B1Zp41J0LpT0oR68amQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "safe-buffer": "^5.1.0"
      }
    },
    "node_modules/rc-cascader": {
      "version": "3.34.0",
      "resolved": "https://registry.npmjs.org/rc-cascader/-/rc-cascader-3.34.0.tgz",
      "integrity": "sha512-KpXypcvju9ptjW9FaN2NFcA2QH9E9LHKq169Y0eWtH4e/wHQ5Wh5qZakAgvb8EKZ736WZ3B0zLLOBsrsja5Dag==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.25.7",
        "classnames": "^2.3.1",
        "rc-select": "~14.16.2",
        "rc-tree": "~5.13.0",
        "rc-util": "^5.43.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-checkbox": {
      "version": "3.5.0",
      "resolved": "https://registry.npmjs.org/rc-checkbox/-/rc-checkbox-3.5.0.tgz",
      "integrity": "sha512-aOAQc3E98HteIIsSqm6Xk2FPKIER6+5vyEFMZfo73TqM+VVAIqOkHoPjgKLqSNtVLWScoaM7vY2ZrGEheI79yg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "classnames": "^2.3.2",
        "rc-util": "^5.25.2"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-collapse": {
      "version": "3.9.0",
      "resolved": "https://registry.npmjs.org/rc-collapse/-/rc-collapse-3.9.0.tgz",
      "integrity": "sha512-swDdz4QZ4dFTo4RAUMLL50qP0EY62N2kvmk2We5xYdRwcRn8WcYtuetCJpwpaCbUfUt5+huLpVxhvmnK+PHrkA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "classnames": "2.x",
        "rc-motion": "^2.3.4",
        "rc-util": "^5.27.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-dialog": {
      "version": "9.6.0",
      "resolved": "https://registry.npmjs.org/rc-dialog/-/rc-dialog-9.6.0.tgz",
      "integrity": "sha512-ApoVi9Z8PaCQg6FsUzS8yvBEQy0ZL2PkuvAgrmohPkN3okps5WZ5WQWPc1RNuiOKaAYv8B97ACdsFU5LizzCqg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "@rc-component/portal": "^1.0.0-8",
        "classnames": "^2.2.6",
        "rc-motion": "^2.3.0",
        "rc-util": "^5.21.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-drawer": {
      "version": "7.3.0",
      "resolved": "https://registry.npmjs.org/rc-drawer/-/rc-drawer-7.3.0.tgz",
      "integrity": "sha512-DX6CIgiBWNpJIMGFO8BAISFkxiuKitoizooj4BDyee8/SnBn0zwO2FHrNDpqqepj0E/TFTDpmEBCyFuTgC7MOg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.23.9",
        "@rc-component/portal": "^1.1.1",
        "classnames": "^2.2.6",
        "rc-motion": "^2.6.1",
        "rc-util": "^5.38.1"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-dropdown": {
      "version": "4.2.1",
      "resolved": "https://registry.npmjs.org/rc-dropdown/-/rc-dropdown-4.2.1.tgz",
      "integrity": "sha512-YDAlXsPv3I1n42dv1JpdM7wJ+gSUBfeyPK59ZpBD9jQhK9jVuxpjj3NmWQHOBceA1zEPVX84T2wbdb2SD0UjmA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.18.3",
        "@rc-component/trigger": "^2.0.0",
        "classnames": "^2.2.6",
        "rc-util": "^5.44.1"
      },
      "peerDependencies": {
        "react": ">=16.11.0",
        "react-dom": ">=16.11.0"
      }
    },
    "node_modules/rc-field-form": {
      "version": "2.7.1",
      "resolved": "https://registry.npmjs.org/rc-field-form/-/rc-field-form-2.7.1.tgz",
      "integrity": "sha512-vKeSifSJ6HoLaAB+B8aq/Qgm8a3dyxROzCtKNCsBQgiverpc4kWDQihoUwzUj+zNWJOykwSY4dNX3QrGwtVb9A==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.18.0",
        "@rc-component/async-validator": "^5.0.3",
        "rc-util": "^5.32.2"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-image": {
      "version": "7.12.0",
      "resolved": "https://registry.npmjs.org/rc-image/-/rc-image-7.12.0.tgz",
      "integrity": "sha512-cZ3HTyyckPnNnUb9/DRqduqzLfrQRyi+CdHjdqgsyDpI3Ln5UX1kXnAhPBSJj9pVRzwRFgqkN7p9b6HBDjmu/Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.11.2",
        "@rc-component/portal": "^1.0.2",
        "classnames": "^2.2.6",
        "rc-dialog": "~9.6.0",
        "rc-motion": "^2.6.2",
        "rc-util": "^5.34.1"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-input": {
      "version": "1.8.0",
      "resolved": "https://registry.npmjs.org/rc-input/-/rc-input-1.8.0.tgz",
      "integrity": "sha512-KXvaTbX+7ha8a/k+eg6SYRVERK0NddX8QX7a7AnRvUa/rEH0CNMlpcBzBkhI0wp2C8C4HlMoYl8TImSN+fuHKA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.11.1",
        "classnames": "^2.2.1",
        "rc-util": "^5.18.1"
      },
      "peerDependencies": {
        "react": ">=16.0.0",
        "react-dom": ">=16.0.0"
      }
    },
    "node_modules/rc-input-number": {
      "version": "9.5.0",
      "resolved": "https://registry.npmjs.org/rc-input-number/-/rc-input-number-9.5.0.tgz",
      "integrity": "sha512-bKaEvB5tHebUURAEXw35LDcnRZLq3x1k7GxfAqBMzmpHkDGzjAtnUL8y4y5N15rIFIg5IJgwr211jInl3cipag==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "@rc-component/mini-decimal": "^1.0.1",
        "classnames": "^2.2.5",
        "rc-input": "~1.8.0",
        "rc-util": "^5.40.1"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-mentions": {
      "version": "2.20.0",
      "resolved": "https://registry.npmjs.org/rc-mentions/-/rc-mentions-2.20.0.tgz",
      "integrity": "sha512-w8HCMZEh3f0nR8ZEd466ATqmXFCMGMN5UFCzEUL0bM/nGw/wOS2GgRzKBcm19K++jDyuWCOJOdgcKGXU3fXfbQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.22.5",
        "@rc-component/trigger": "^2.0.0",
        "classnames": "^2.2.6",
        "rc-input": "~1.8.0",
        "rc-menu": "~9.16.0",
        "rc-textarea": "~1.10.0",
        "rc-util": "^5.34.1"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-menu": {
      "version": "9.16.1",
      "resolved": "https://registry.npmjs.org/rc-menu/-/rc-menu-9.16.1.tgz",
      "integrity": "sha512-ghHx6/6Dvp+fw8CJhDUHFHDJ84hJE3BXNCzSgLdmNiFErWSOaZNsihDAsKq9ByTALo/xkNIwtDFGIl6r+RPXBg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "@rc-component/trigger": "^2.0.0",
        "classnames": "2.x",
        "rc-motion": "^2.4.3",
        "rc-overflow": "^1.3.1",
        "rc-util": "^5.27.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-motion": {
      "version": "2.9.5",
      "resolved": "https://registry.npmjs.org/rc-motion/-/rc-motion-2.9.5.tgz",
      "integrity": "sha512-w+XTUrfh7ArbYEd2582uDrEhmBHwK1ZENJiSJVb7uRxdE7qJSYjbO2eksRXmndqyKqKoYPc9ClpPh5242mV1vA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.11.1",
        "classnames": "^2.2.1",
        "rc-util": "^5.44.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-notification": {
      "version": "5.6.4",
      "resolved": "https://registry.npmjs.org/rc-notification/-/rc-notification-5.6.4.tgz",
      "integrity": "sha512-KcS4O6B4qzM3KH7lkwOB7ooLPZ4b6J+VMmQgT51VZCeEcmghdeR4IrMcFq0LG+RPdnbe/ArT086tGM8Snimgiw==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "classnames": "2.x",
        "rc-motion": "^2.9.0",
        "rc-util": "^5.20.1"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-overflow": {
      "version": "1.5.0",
      "resolved": "https://registry.npmjs.org/rc-overflow/-/rc-overflow-1.5.0.tgz",
      "integrity": "sha512-Lm/v9h0LymeUYJf0x39OveU52InkdRXqnn2aYXfWmo8WdOonIKB2kfau+GF0fWq6jPgtdO9yMqveGcK6aIhJmg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.11.1",
        "classnames": "^2.2.1",
        "rc-resize-observer": "^1.0.0",
        "rc-util": "^5.37.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-pagination": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/rc-pagination/-/rc-pagination-5.1.0.tgz",
      "integrity": "sha512-8416Yip/+eclTFdHXLKTxZvn70duYVGTvUUWbckCCZoIl3jagqke3GLsFrMs0bsQBikiYpZLD9206Ej4SOdOXQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "classnames": "^2.3.2",
        "rc-util": "^5.38.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-picker": {
      "version": "4.11.3",
      "resolved": "https://registry.npmjs.org/rc-picker/-/rc-picker-4.11.3.tgz",
      "integrity": "sha512-MJ5teb7FlNE0NFHTncxXQ62Y5lytq6sh5nUw0iH8OkHL/TjARSEvSHpr940pWgjGANpjCwyMdvsEV55l5tYNSg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.24.7",
        "@rc-component/trigger": "^2.0.0",
        "classnames": "^2.2.1",
        "rc-overflow": "^1.3.2",
        "rc-resize-observer": "^1.4.0",
        "rc-util": "^5.43.0"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "date-fns": ">= 2.x",
        "dayjs": ">= 1.x",
        "luxon": ">= 3.x",
        "moment": ">= 2.x",
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      },
      "peerDependenciesMeta": {
        "date-fns": {
          "optional": true
        },
        "dayjs": {
          "optional": true
        },
        "luxon": {
          "optional": true
        },
        "moment": {
          "optional": true
        }
      }
    },
    "node_modules/rc-progress": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/rc-progress/-/rc-progress-4.0.0.tgz",
      "integrity": "sha512-oofVMMafOCokIUIBnZLNcOZFsABaUw8PPrf1/y0ZBvKZNpOiu5h4AO9vv11Sw0p4Hb3D0yGWuEattcQGtNJ/aw==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "classnames": "^2.2.6",
        "rc-util": "^5.16.1"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-rate": {
      "version": "2.13.1",
      "resolved": "https://registry.npmjs.org/rc-rate/-/rc-rate-2.13.1.tgz",
      "integrity": "sha512-QUhQ9ivQ8Gy7mtMZPAjLbxBt5y9GRp65VcUyGUMF3N3fhiftivPHdpuDIaWIMOTEprAjZPC08bls1dQB+I1F2Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "classnames": "^2.2.5",
        "rc-util": "^5.0.1"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-resize-observer": {
      "version": "1.4.3",
      "resolved": "https://registry.npmjs.org/rc-resize-observer/-/rc-resize-observer-1.4.3.tgz",
      "integrity": "sha512-YZLjUbyIWox8E9i9C3Tm7ia+W7euPItNWSPX5sCcQTYbnwDb5uNpnLHQCG1f22oZWUhLw4Mv2tFmeWe68CDQRQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.20.7",
        "classnames": "^2.2.1",
        "rc-util": "^5.44.1",
        "resize-observer-polyfill": "^1.5.1"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-segmented": {
      "version": "2.7.1",
      "resolved": "https://registry.npmjs.org/rc-segmented/-/rc-segmented-2.7.1.tgz",
      "integrity": "sha512-izj1Nw/Dw2Vb7EVr+D/E9lUTkBe+kKC+SAFSU9zqr7WV2W5Ktaa9Gc7cB2jTqgk8GROJayltaec+DBlYKc6d+g==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.11.1",
        "classnames": "^2.2.1",
        "rc-motion": "^2.4.4",
        "rc-util": "^5.17.0"
      },
      "peerDependencies": {
        "react": ">=16.0.0",
        "react-dom": ">=16.0.0"
      }
    },
    "node_modules/rc-select": {
      "version": "14.16.8",
      "resolved": "https://registry.npmjs.org/rc-select/-/rc-select-14.16.8.tgz",
      "integrity": "sha512-NOV5BZa1wZrsdkKaiK7LHRuo5ZjZYMDxPP6/1+09+FB4KoNi8jcG1ZqLE3AVCxEsYMBe65OBx71wFoHRTP3LRg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "@rc-component/trigger": "^2.1.1",
        "classnames": "2.x",
        "rc-motion": "^2.0.1",
        "rc-overflow": "^1.3.1",
        "rc-util": "^5.16.1",
        "rc-virtual-list": "^3.5.2"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": "*",
        "react-dom": "*"
      }
    },
    "node_modules/rc-slider": {
      "version": "11.1.9",
      "resolved": "https://registry.npmjs.org/rc-slider/-/rc-slider-11.1.9.tgz",
      "integrity": "sha512-h8IknhzSh3FEM9u8ivkskh+Ef4Yo4JRIY2nj7MrH6GQmrwV6mcpJf5/4KgH5JaVI1H3E52yCdpOlVyGZIeph5A==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "classnames": "^2.2.5",
        "rc-util": "^5.36.0"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-steps": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/rc-steps/-/rc-steps-6.0.1.tgz",
      "integrity": "sha512-lKHL+Sny0SeHkQKKDJlAjV5oZ8DwCdS2hFhAkIjuQt1/pB81M0cA0ErVFdHq9+jmPmFw1vJB2F5NBzFXLJxV+g==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.16.7",
        "classnames": "^2.2.3",
        "rc-util": "^5.16.1"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-switch": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/rc-switch/-/rc-switch-4.1.0.tgz",
      "integrity": "sha512-TI8ufP2Az9oEbvyCeVE4+90PDSljGyuwix3fV58p7HV2o4wBnVToEyomJRVyTaZeqNPAp+vqeo4Wnj5u0ZZQBg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.21.0",
        "classnames": "^2.2.1",
        "rc-util": "^5.30.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-table": {
      "version": "7.54.0",
      "resolved": "https://registry.npmjs.org/rc-table/-/rc-table-7.54.0.tgz",
      "integrity": "sha512-/wDTkki6wBTjwylwAGjpLKYklKo9YgjZwAU77+7ME5mBoS32Q4nAwoqhA2lSge6fobLW3Tap6uc5xfwaL2p0Sw==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "@rc-component/context": "^1.4.0",
        "classnames": "^2.2.5",
        "rc-resize-observer": "^1.1.0",
        "rc-util": "^5.44.3",
        "rc-virtual-list": "^3.14.2"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-tabs": {
      "version": "15.7.0",
      "resolved": "https://registry.npmjs.org/rc-tabs/-/rc-tabs-15.7.0.tgz",
      "integrity": "sha512-ZepiE+6fmozYdWf/9gVp7k56PKHB1YYoDsKeQA1CBlJ/POIhjkcYiv0AGP0w2Jhzftd3AVvZP/K+V+Lpi2ankA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.11.2",
        "classnames": "2.x",
        "rc-dropdown": "~4.2.0",
        "rc-menu": "~9.16.0",
        "rc-motion": "^2.6.2",
        "rc-resize-observer": "^1.0.0",
        "rc-util": "^5.34.1"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-textarea": {
      "version": "1.10.2",
      "resolved": "https://registry.npmjs.org/rc-textarea/-/rc-textarea-1.10.2.tgz",
      "integrity": "sha512-HfaeXiaSlpiSp0I/pvWpecFEHpVysZ9tpDLNkxQbMvMz6gsr7aVZ7FpWP9kt4t7DB+jJXesYS0us1uPZnlRnwQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "classnames": "^2.2.1",
        "rc-input": "~1.8.0",
        "rc-resize-observer": "^1.0.0",
        "rc-util": "^5.27.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-tooltip": {
      "version": "6.4.0",
      "resolved": "https://registry.npmjs.org/rc-tooltip/-/rc-tooltip-6.4.0.tgz",
      "integrity": "sha512-kqyivim5cp8I5RkHmpsp1Nn/Wk+1oeloMv9c7LXNgDxUpGm+RbXJGL+OPvDlcRnx9DBeOe4wyOIl4OKUERyH1g==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.11.2",
        "@rc-component/trigger": "^2.0.0",
        "classnames": "^2.3.1",
        "rc-util": "^5.44.3"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-tree": {
      "version": "5.13.1",
      "resolved": "https://registry.npmjs.org/rc-tree/-/rc-tree-5.13.1.tgz",
      "integrity": "sha512-FNhIefhftobCdUJshO7M8uZTA9F4OPGVXqGfZkkD/5soDeOhwO06T/aKTrg0WD8gRg/pyfq+ql3aMymLHCTC4A==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.10.1",
        "classnames": "2.x",
        "rc-motion": "^2.0.1",
        "rc-util": "^5.16.1",
        "rc-virtual-list": "^3.5.1"
      },
      "engines": {
        "node": ">=10.x"
      },
      "peerDependencies": {
        "react": "*",
        "react-dom": "*"
      }
    },
    "node_modules/rc-tree-select": {
      "version": "5.27.0",
      "resolved": "https://registry.npmjs.org/rc-tree-select/-/rc-tree-select-5.27.0.tgz",
      "integrity": "sha512-2qTBTzwIT7LRI1o7zLyrCzmo5tQanmyGbSaGTIf7sYimCklAToVVfpMC6OAldSKolcnjorBYPNSKQqJmN3TCww==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.25.7",
        "classnames": "2.x",
        "rc-select": "~14.16.2",
        "rc-tree": "~5.13.0",
        "rc-util": "^5.43.0"
      },
      "peerDependencies": {
        "react": "*",
        "react-dom": "*"
      }
    },
    "node_modules/rc-upload": {
      "version": "4.11.0",
      "resolved": "https://registry.npmjs.org/rc-upload/-/rc-upload-4.11.0.tgz",
      "integrity": "sha512-ZUyT//2JAehfHzjWowqROcwYJKnZkIUGWaTE/VogVrepSl7AFNbQf4+zGfX4zl9Vrj/Jm8scLO0R6UlPDKK4wA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.18.3",
        "classnames": "^2.2.5",
        "rc-util": "^5.2.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-util": {
      "version": "5.44.4",
      "resolved": "https://registry.npmjs.org/rc-util/-/rc-util-5.44.4.tgz",
      "integrity": "sha512-resueRJzmHG9Q6rI/DfK6Kdv9/Lfls05vzMs1Sk3M2P+3cJa+MakaZyWY8IPfehVuhPJFKrIY1IK4GqbiaiY5w==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.18.3",
        "react-is": "^18.2.0"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/rc-virtual-list": {
      "version": "3.19.2",
      "resolved": "https://registry.npmjs.org/rc-virtual-list/-/rc-virtual-list-3.19.2.tgz",
      "integrity": "sha512-Ys6NcjwGkuwkeaWBDqfI3xWuZ7rDiQXlH1o2zLfFzATfEgXcqpk8CkgMfbJD81McqjcJVez25a3kPxCR807evA==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.20.0",
        "classnames": "^2.2.6",
        "rc-resize-observer": "^1.0.0",
        "rc-util": "^5.36.0"
      },
      "engines": {
        "node": ">=8.x"
      },
      "peerDependencies": {
        "react": ">=16.9.0",
        "react-dom": ">=16.9.0"
      }
    },
    "node_modules/react": {
      "version": "18.3.1",
      "resolved": "https://registry.npmjs.org/react/-/react-18.3.1.tgz",
      "integrity": "sha512-wS+hAgJShR0KhEvPJArfuPVN1+Hz1t0Y6n5jLrGQbkb4urgPE/0Rve+1kMB1v/oWgHgm4WIcV+i7F2pTVj+2iQ==",
      "license": "MIT",
      "peer": true,
      "dependencies": {
        "loose-envify": "^1.1.0"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react-docgen": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/react-docgen/-/react-docgen-7.1.1.tgz",
      "integrity": "sha512-hlSJDQ2synMPKFZOsKo9Hi8WWZTC7POR8EmWvTSjow+VDgKzkmjQvFm2fk0tmRw+f0vTOIYKlarR0iL4996pdg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.18.9",
        "@babel/traverse": "^7.18.9",
        "@babel/types": "^7.18.9",
        "@types/babel__core": "^7.18.0",
        "@types/babel__traverse": "^7.18.0",
        "@types/doctrine": "^0.0.9",
        "@types/resolve": "^1.20.2",
        "doctrine": "^3.0.0",
        "resolve": "^1.22.1",
        "strip-indent": "^4.0.0"
      },
      "engines": {
        "node": ">=16.14.0"
      }
    },
    "node_modules/react-docgen-typescript": {
      "version": "2.4.0",
      "resolved": "https://registry.npmjs.org/react-docgen-typescript/-/react-docgen-typescript-2.4.0.tgz",
      "integrity": "sha512-ZtAp5XTO5HRzQctjPU0ybY0RRCQO19X/8fxn3w7y2VVTUbGHDKULPTL4ky3vB05euSgG5NpALhEhDPvQ56wvXg==",
      "dev": true,
      "license": "MIT",
      "peerDependencies": {
        "typescript": ">= 4.3.x"
      }
    },
    "node_modules/react-dom": {
      "version": "18.3.1",
      "resolved": "https://registry.npmjs.org/react-dom/-/react-dom-18.3.1.tgz",
      "integrity": "sha512-5m4nQKp+rZRb09LNH59GM4BxTh9251/ylbKIbpe7TpGxfJ+9kv6BLkLBXIjjspbgbnIBNqlI23tRnTWT0snUIw==",
      "license": "MIT",
      "peer": true,
      "dependencies": {
        "loose-envify": "^1.1.0",
        "scheduler": "^0.23.2"
      },
      "peerDependencies": {
        "react": "^18.3.1"
      }
    },
    "node_modules/react-is": {
      "version": "18.3.1",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-18.3.1.tgz",
      "integrity": "sha512-/LLMVyas0ljjAtoYiPqYiL8VWXzUUdThrmU5+n20DZv+a+ClRoevUzw5JxU+Ieh5/c87ytoTBV9G1FiKfNJdmg==",
      "license": "MIT"
    },
    "node_modules/react-refresh": {
      "version": "0.17.0",
      "resolved": "https://registry.npmjs.org/react-refresh/-/react-refresh-0.17.0.tgz",
      "integrity": "sha512-z6F7K9bV85EfseRCp2bzrpyQ0Gkw1uLoCel9XBVWPg/TjRj94SkJzUTGfOa4bs7iJvBWtQG0Wq7wnI0syw3EBQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react-router": {
      "version": "6.30.3",
      "resolved": "https://registry.npmjs.org/react-router/-/react-router-6.30.3.tgz",
      "integrity": "sha512-XRnlbKMTmktBkjCLE8/XcZFlnHvr2Ltdr1eJX4idL55/9BbORzyZEaIkBFDhFGCEWBBItsVrDxwx3gnisMitdw==",
      "license": "MIT",
      "dependencies": {
        "@remix-run/router": "1.23.2"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "react": ">=16.8"
      }
    },
    "node_modules/react-router-dom": {
      "version": "6.30.3",
      "resolved": "https://registry.npmjs.org/react-router-dom/-/react-router-dom-6.30.3.tgz",
      "integrity": "sha512-pxPcv1AczD4vso7G4Z3TKcvlxK7g7TNt3/FNGMhfqyntocvYKj+GCatfigGDjbLozC4baguJ0ReCigoDJXb0ag==",
      "license": "MIT",
      "dependencies": {
        "@remix-run/router": "1.23.2",
        "react-router": "6.30.3"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "react": ">=16.8",
        "react-dom": ">=16.8"
      }
    },
    "node_modules/recast": {
      "version": "0.23.11",
      "resolved": "https://registry.npmjs.org/recast/-/recast-0.23.11.tgz",
      "integrity": "sha512-YTUo+Flmw4ZXiWfQKGcwwc11KnoRAYgzAE2E7mXKCjSviTKShtxBsN6YUUBB2gtaBzKzeKunxhUwNHQuRryhWA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ast-types": "^0.16.1",
        "esprima": "~4.0.0",
        "source-map": "~0.6.1",
        "tiny-invariant": "^1.3.3",
        "tslib": "^2.0.1"
      },
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/reflect.getprototypeof": {
      "version": "1.0.10",
      "resolved": "https://registry.npmjs.org/reflect.getprototypeof/-/reflect.getprototypeof-1.0.10.tgz",
      "integrity": "sha512-00o4I+DVrefhv+nX0ulyi3biSHCPDe+yLv5o/p6d/UVlirijB8E16FtfwSAi4g3tcqrQ4lRAqQSoFEZJehYEcw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.9",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0",
        "get-intrinsic": "^1.2.7",
        "get-proto": "^1.0.1",
        "which-builtin-type": "^1.2.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/regenerate": {
      "version": "1.4.2",
      "resolved": "https://registry.npmjs.org/regenerate/-/regenerate-1.4.2.tgz",
      "integrity": "sha512-zrceR/XhGYU/d/opr2EKO7aRHUeiBI8qjtfHqADTwZd6Szfy16la6kqD0MIUs5z5hx6AaKa+PixpPrR289+I0A==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/regenerate-unicode-properties": {
      "version": "10.2.2",
      "resolved": "https://registry.npmjs.org/regenerate-unicode-properties/-/regenerate-unicode-properties-10.2.2.tgz",
      "integrity": "sha512-m03P+zhBeQd1RGnYxrGyDAPpWX/epKirLrp8e3qevZdVkKtnCrjjWczIbYc8+xd6vcTStVlqfycTx1KR4LOr0g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "regenerate": "^1.4.2"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/regexp.prototype.flags": {
      "version": "1.5.4",
      "resolved": "https://registry.npmjs.org/regexp.prototype.flags/-/regexp.prototype.flags-1.5.4.tgz",
      "integrity": "sha512-dYqgNSZbDwkaJ2ceRd9ojCGjBq+mOm9LmtXnAnEGyHhN/5R7iDW2TRw3h+o/jCFxus3P2LfWIIiwowAjANm7IA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-errors": "^1.3.0",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "set-function-name": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/regexpu-core": {
      "version": "6.4.0",
      "resolved": "https://registry.npmjs.org/regexpu-core/-/regexpu-core-6.4.0.tgz",
      "integrity": "sha512-0ghuzq67LI9bLXpOX/ISfve/Mq33a4aFRzoQYhnnok1JOFpmE/A2TBGkNVenOGEeSBCjIiWcc6MVOG5HEQv0sA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "regenerate": "^1.4.2",
        "regenerate-unicode-properties": "^10.2.2",
        "regjsgen": "^0.8.0",
        "regjsparser": "^0.13.0",
        "unicode-match-property-ecmascript": "^2.0.0",
        "unicode-match-property-value-ecmascript": "^2.2.1"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/regjsgen": {
      "version": "0.8.0",
      "resolved": "https://registry.npmjs.org/regjsgen/-/regjsgen-0.8.0.tgz",
      "integrity": "sha512-RvwtGe3d7LvWiDQXeQw8p5asZUmfU1G/l6WbUXeHta7Y2PEIvBTwH6E2EfmYUK8pxcxEdEmaomqyp0vZZ7C+3Q==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/regjsparser": {
      "version": "0.13.0",
      "resolved": "https://registry.npmjs.org/regjsparser/-/regjsparser-0.13.0.tgz",
      "integrity": "sha512-NZQZdC5wOE/H3UT28fVGL+ikOZcEzfMGk/c3iN9UGxzWHMa1op7274oyiUVrAG4B2EuFhus8SvkaYnhvW92p9Q==",
      "dev": true,
      "license": "BSD-2-Clause",
      "dependencies": {
        "jsesc": "~3.1.0"
      },
      "bin": {
        "regjsparser": "bin/parser"
      }
    },
    "node_modules/require-from-string": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/require-from-string/-/require-from-string-2.0.2.tgz",
      "integrity": "sha512-Xf0nWe6RseziFMu+Ap9biiUbmplq6S9/p+7w7YXP/JBHhrUDDUhwa+vANyubuqfZWTveU//DYVGsDG7RKL/vEw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/resize-observer-polyfill": {
      "version": "1.5.1",
      "resolved": "https://registry.npmjs.org/resize-observer-polyfill/-/resize-observer-polyfill-1.5.1.tgz",
      "integrity": "sha512-LwZrotdHOo12nQuZlHEmtuXdqGoOD0OhaxopaNFxWzInpEgaLWoVuAMbTzixuosCx2nEG58ngzW3vxdWoxIgdg==",
      "license": "MIT"
    },
    "node_modules/resolve": {
      "version": "1.22.11",
      "resolved": "https://registry.npmjs.org/resolve/-/resolve-1.22.11.tgz",
      "integrity": "sha512-RfqAvLnMl313r7c9oclB1HhUEAezcpLjz95wFH4LVuhk9JF/r22qmVP9AMmOU4vMX7Q8pN8jwNg/CSpdFnMjTQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-core-module": "^2.16.1",
        "path-parse": "^1.0.7",
        "supports-preserve-symlinks-flag": "^1.0.0"
      },
      "bin": {
        "resolve": "bin/resolve"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/rollup": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/rollup/-/rollup-4.59.0.tgz",
      "integrity": "sha512-2oMpl67a3zCH9H79LeMcbDhXW/UmWG/y2zuqnF2jQq5uq9TbM9TVyXvA4+t+ne2IIkBdrLpAaRQAvo7YI/Yyeg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@types/estree": "1.0.8"
      },
      "bin": {
        "rollup": "dist/bin/rollup"
      },
      "engines": {
        "node": ">=18.0.0",
        "npm": ">=8.0.0"
      },
      "optionalDependencies": {
        "@rollup/rollup-android-arm-eabi": "4.59.0",
        "@rollup/rollup-android-arm64": "4.59.0",
        "@rollup/rollup-darwin-arm64": "4.59.0",
        "@rollup/rollup-darwin-x64": "4.59.0",
        "@rollup/rollup-freebsd-arm64": "4.59.0",
        "@rollup/rollup-freebsd-x64": "4.59.0",
        "@rollup/rollup-linux-arm-gnueabihf": "4.59.0",
        "@rollup/rollup-linux-arm-musleabihf": "4.59.0",
        "@rollup/rollup-linux-arm64-gnu": "4.59.0",
        "@rollup/rollup-linux-arm64-musl": "4.59.0",
        "@rollup/rollup-linux-loong64-gnu": "4.59.0",
        "@rollup/rollup-linux-loong64-musl": "4.59.0",
        "@rollup/rollup-linux-ppc64-gnu": "4.59.0",
        "@rollup/rollup-linux-ppc64-musl": "4.59.0",
        "@rollup/rollup-linux-riscv64-gnu": "4.59.0",
        "@rollup/rollup-linux-riscv64-musl": "4.59.0",
        "@rollup/rollup-linux-s390x-gnu": "4.59.0",
        "@rollup/rollup-linux-x64-gnu": "4.59.0",
        "@rollup/rollup-linux-x64-musl": "4.59.0",
        "@rollup/rollup-openbsd-x64": "4.59.0",
        "@rollup/rollup-openharmony-arm64": "4.59.0",
        "@rollup/rollup-win32-arm64-msvc": "4.59.0",
        "@rollup/rollup-win32-ia32-msvc": "4.59.0",
        "@rollup/rollup-win32-x64-gnu": "4.59.0",
        "@rollup/rollup-win32-x64-msvc": "4.59.0",
        "fsevents": "~2.3.2"
      }
    },
    "node_modules/safe-array-concat": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/safe-array-concat/-/safe-array-concat-1.1.3.tgz",
      "integrity": "sha512-AURm5f0jYEOydBj7VQlVvDrjeFgthDdEF5H1dP+6mNpoXOMo1quQqJ4wvJDyRZ9+pO3kGWoOdmV08cSv2aJV6Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.2",
        "get-intrinsic": "^1.2.6",
        "has-symbols": "^1.1.0",
        "isarray": "^2.0.5"
      },
      "engines": {
        "node": ">=0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/safe-buffer": {
      "version": "5.2.1",
      "resolved": "https://registry.npmjs.org/safe-buffer/-/safe-buffer-5.2.1.tgz",
      "integrity": "sha512-rp3So07KcdmmKbGvgaNxQSJr7bGVSVk5S9Eq1F+ppbRo70+YeaDxkw5Dd8NPN+GD6bjnYm2VuPuCXmpuYvmCXQ==",
      "dev": true,
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "license": "MIT"
    },
    "node_modules/safe-push-apply": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/safe-push-apply/-/safe-push-apply-1.0.0.tgz",
      "integrity": "sha512-iKE9w/Z7xCzUMIZqdBsp6pEQvwuEebH4vdpjcDWnyzaI6yl6O9FHvVpmGelvEHNsoY6wGblkxR6Zty/h00WiSA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "isarray": "^2.0.5"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/safe-regex-test": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/safe-regex-test/-/safe-regex-test-1.1.0.tgz",
      "integrity": "sha512-x/+Cz4YrimQxQccJf5mKEbIa1NzeCRNI5Ecl/ekmlYaampdNLPalVyIcCZNNH3MvmqBugV5TMYZXv0ljslUlaw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "is-regex": "^1.2.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/scheduler": {
      "version": "0.23.2",
      "resolved": "https://registry.npmjs.org/scheduler/-/scheduler-0.23.2.tgz",
      "integrity": "sha512-UOShsPwz7NrMUqhR6t0hWjFduvOzbtv7toDH1/hIrfRNIDBnnBWd0CwJTGvTpngVlmwGCdP9/Zl/tVrDqcuYzQ==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.1.0"
      }
    },
    "node_modules/scroll-into-view-if-needed": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/scroll-into-view-if-needed/-/scroll-into-view-if-needed-3.1.0.tgz",
      "integrity": "sha512-49oNpRjWRvnU8NyGVmUaYG4jtTkNonFZI86MmGRDqBphEK2EXT9gdEUoQPZhuBM8yWHxCWbobltqYO5M4XrUvQ==",
      "license": "MIT",
      "dependencies": {
        "compute-scroll-into-view": "^3.0.2"
      }
    },
    "node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "dev": true,
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/serialize-javascript": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/serialize-javascript/-/serialize-javascript-6.0.2.tgz",
      "integrity": "sha512-Saa1xPByTTq2gdeFZYLLo+RFE35NHZkAbqZeWNd3BpzppeVisAqpDjcp8dyf6uIvEqJRd46jemmyA4iFIeVk8g==",
      "dev": true,
      "license": "BSD-3-Clause",
      "dependencies": {
        "randombytes": "^2.1.0"
      }
    },
    "node_modules/set-function-length": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/set-function-length/-/set-function-length-1.2.2.tgz",
      "integrity": "sha512-pgRc4hJ4/sNjWCSS9AmnS40x3bNMDTknHgL5UaMBTMyJnU90EgWh1Rz+MC9eFu4BuN/UwZjKQuY/1v3rM7HMfg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "define-data-property": "^1.1.4",
        "es-errors": "^1.3.0",
        "function-bind": "^1.1.2",
        "get-intrinsic": "^1.2.4",
        "gopd": "^1.0.1",
        "has-property-descriptors": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/set-function-name": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/set-function-name/-/set-function-name-2.0.2.tgz",
      "integrity": "sha512-7PGFlmtwsEADb0WYyvCMa1t+yke6daIG4Wirafur5kcf+MhUnPms1UeR0CKQdTZD81yESwMHbtn+TR+dMviakQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "define-data-property": "^1.1.4",
        "es-errors": "^1.3.0",
        "functions-have-names": "^1.2.3",
        "has-property-descriptors": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/set-proto": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/set-proto/-/set-proto-1.0.0.tgz",
      "integrity": "sha512-RJRdvCo6IAnPdsvP/7m6bsQqNnn1FCBX5ZNtFL98MmFF/4xAIJTIg1YbHW5DC2W5SKZanrC6i4HsJqlajw/dZw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/shebang-command": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/shebang-command/-/shebang-command-2.0.0.tgz",
      "integrity": "sha512-kHxr2zZpYtdmrN1qDjrrX/Z1rR1kG8Dx+gkpK1G4eXmvXswmcE1hTWBWYUzlraYw1/yZp6YuDY77YtvbN0dmDA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "shebang-regex": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/shebang-regex": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/shebang-regex/-/shebang-regex-3.0.0.tgz",
      "integrity": "sha512-7++dFhtcx3353uBaq8DDR4NuxBetBzC7ZQOhmTQInHEd6bSrXdiEyzCvG07Z44UYdLShWUyXt5M/yhz8ekcb1A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/side-channel": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/side-channel/-/side-channel-1.1.0.tgz",
      "integrity": "sha512-ZX99e6tRweoUXqR+VBrslhda51Nh5MTQwou5tnUDgbtyM0dBgmhEDtWGP/xbKn6hqfPRHujUNwz5fy/wbbhnpw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "object-inspect": "^1.13.3",
        "side-channel-list": "^1.0.0",
        "side-channel-map": "^1.0.1",
        "side-channel-weakmap": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-list": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/side-channel-list/-/side-channel-list-1.0.0.tgz",
      "integrity": "sha512-FCLHtRD/gnpCiCHEiJLOwdmFP+wzCmDEkc9y7NsYxeF4u7Btsn1ZuwgwJGxImImHicJArLP4R0yX4c2KCrMrTA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "object-inspect": "^1.13.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-map": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/side-channel-map/-/side-channel-map-1.0.1.tgz",
      "integrity": "sha512-VCjCNfgMsby3tTdo02nbjtM/ewra6jPHmpThenkTYh8pG9ucZ/1P8So4u4FGBek/BjpOVsDCMoLA/iuBKIFXRA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.5",
        "object-inspect": "^1.13.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-weakmap": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/side-channel-weakmap/-/side-channel-weakmap-1.0.2.tgz",
      "integrity": "sha512-WPS/HvHQTYnHisLo9McqBHOJk2FkHO/tlpvldyrnem4aeQp4hai3gythswg6p01oSoTl58rcpiFAjF2br2Ak2A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.5",
        "object-inspect": "^1.13.3",
        "side-channel-map": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/signal-exit": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/signal-exit/-/signal-exit-4.1.0.tgz",
      "integrity": "sha512-bzyZ1e88w9O1iNJbKnOlvYTrWPDl46O1bG0D3XInv+9tkPrxrN8jUUTiFlDkkmKWgn1M6CfIA13SuGqOa9Korw==",
      "dev": true,
      "license": "ISC",
      "engines": {
        "node": ">=14"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/smob": {
      "version": "1.6.1",
      "resolved": "https://registry.npmjs.org/smob/-/smob-1.6.1.tgz",
      "integrity": "sha512-KAkBqZl3c2GvNgNhcoyJae1aKldDW0LO279wF9bk1PnluRTETKBq0WyzRXxEhoQLk56yHaOY4JCBEKDuJIET5g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=20.0.0"
      }
    },
    "node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "dev": true,
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/source-map-js": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/source-map-js/-/source-map-js-1.2.1.tgz",
      "integrity": "sha512-UXWMKhLOwVKb728IUtQPXxfYU+usdybtUrK/8uGE8CQMvrhOpwvzDBwj0QhSL7MQc7vIsISBG8VQ8+IDQxpfQA==",
      "dev": true,
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/source-map-support": {
      "version": "0.5.21",
      "resolved": "https://registry.npmjs.org/source-map-support/-/source-map-support-0.5.21.tgz",
      "integrity": "sha512-uBHU3L3czsIyYXKX88fdrGovxdSCoTGDRZ6SYXtSRxLZUzHg5P/66Ht6uoUlHu9EZod+inXhKo3qQgwXUT/y1w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "buffer-from": "^1.0.0",
        "source-map": "^0.6.0"
      }
    },
    "node_modules/sourcemap-codec": {
      "version": "1.4.8",
      "resolved": "https://registry.npmjs.org/sourcemap-codec/-/sourcemap-codec-1.4.8.tgz",
      "integrity": "sha512-9NykojV5Uih4lgo5So5dtw+f0JgJX30KCNI8gwhz2J9A15wD0Ml6tjHKwf6fTSa6fAdVBdZeNOs9eJ71qCk8vA==",
      "deprecated": "Please use @jridgewell/sourcemap-codec instead",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/stop-iteration-iterator": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/stop-iteration-iterator/-/stop-iteration-iterator-1.1.0.tgz",
      "integrity": "sha512-eLoXW/DHyl62zxY4SCaIgnRhuMr6ri4juEYARS8E6sCEqzKpOiE521Ucofdx+KnDZl5xmvGYaaKCk5FEOxJCoQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "internal-slot": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/storybook": {
      "version": "8.6.18",
      "resolved": "https://registry.npmjs.org/storybook/-/storybook-8.6.18.tgz",
      "integrity": "sha512-p8seiSI6FiVY6P3V0pG+5v7c8pDMehMAFRWEhG5XqIBSQszzOjDnW2rNvm3odoLKfo3V3P6Cs6Hv9ILzymULyQ==",
      "dev": true,
      "license": "MIT",
      "peer": true,
      "dependencies": {
        "@storybook/core": "8.6.18"
      },
      "bin": {
        "getstorybook": "bin/index.cjs",
        "sb": "bin/index.cjs",
        "storybook": "bin/index.cjs"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/storybook"
      },
      "peerDependencies": {
        "prettier": "^2 || ^3"
      },
      "peerDependenciesMeta": {
        "prettier": {
          "optional": true
        }
      }
    },
    "node_modules/string-convert": {
      "version": "0.2.1",
      "resolved": "https://registry.npmjs.org/string-convert/-/string-convert-0.2.1.tgz",
      "integrity": "sha512-u/1tdPl4yQnPBjnVrmdLo9gtuLvELKsAoRapekWggdiQNvvvum+jYF329d84NAa660KQw7pB2n36KrIKVoXa3A==",
      "license": "MIT"
    },
    "node_modules/string-width": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/string-width/-/string-width-5.1.2.tgz",
      "integrity": "sha512-HnLOCR3vjcY8beoNLtcjZ5/nxn2afmME6lhrDrebokqMap+XbeW8n9TXpPDOqdGK5qcI3oT0GKTW6wC7EMiVqA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "eastasianwidth": "^0.2.0",
        "emoji-regex": "^9.2.2",
        "strip-ansi": "^7.0.1"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/string-width-cjs": {
      "name": "string-width",
      "version": "4.2.3",
      "resolved": "https://registry.npmjs.org/string-width/-/string-width-4.2.3.tgz",
      "integrity": "sha512-wKyQRQpjJ0sIp62ErSZdGsjMJWsap5oRNihHhu6G7JVO/9jIB6UyevL+tXuOqrng8j/cxKTWyWUwvSTriiZz/g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "emoji-regex": "^8.0.0",
        "is-fullwidth-code-point": "^3.0.0",
        "strip-ansi": "^6.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/string-width-cjs/node_modules/ansi-regex": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/ansi-regex/-/ansi-regex-5.0.1.tgz",
      "integrity": "sha512-quJQXlTSUGL2LH9SUXo8VwsY4soanhgo6LNSm84E1LBcE8s3O0wpdiRzyR9z/ZZJMlMWv37qOOb9pdJlMUEKFQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/string-width-cjs/node_modules/emoji-regex": {
      "version": "8.0.0",
      "resolved": "https://registry.npmjs.org/emoji-regex/-/emoji-regex-8.0.0.tgz",
      "integrity": "sha512-MSjYzcWNOA0ewAHpz0MxpYFvwg6yjy1NG3xteoqz644VCo/RPgnr1/GGt+ic3iJTzQ8Eu3TdM14SawnVUmGE6A==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/string-width-cjs/node_modules/strip-ansi": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-6.0.1.tgz",
      "integrity": "sha512-Y38VPSHcqkFrCpFnQ9vuSXmquuv5oXOKpGeT6aGrr3o3Gc9AlVa6JBfUSOCnbxGGZF+/0ooI7KrPuUSztUdU5A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/string.prototype.matchall": {
      "version": "4.0.12",
      "resolved": "https://registry.npmjs.org/string.prototype.matchall/-/string.prototype.matchall-4.0.12.tgz",
      "integrity": "sha512-6CC9uyBL+/48dYizRf7H7VAYCMCNTBeM78x/VTUe9bFEaxBepPJDa1Ow99LqI/1yF7kuy7Q3cQsYMrcjGUcskA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.6",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0",
        "get-intrinsic": "^1.2.6",
        "gopd": "^1.2.0",
        "has-symbols": "^1.1.0",
        "internal-slot": "^1.1.0",
        "regexp.prototype.flags": "^1.5.3",
        "set-function-name": "^2.0.2",
        "side-channel": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/string.prototype.trim": {
      "version": "1.2.10",
      "resolved": "https://registry.npmjs.org/string.prototype.trim/-/string.prototype.trim-1.2.10.tgz",
      "integrity": "sha512-Rs66F0P/1kedk5lyYyH9uBzuiI/kNRmwJAR9quK6VOtIpZ2G+hMZd+HQbbv25MgCA6gEffoMZYxlTod4WcdrKA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.2",
        "define-data-property": "^1.1.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-object-atoms": "^1.0.0",
        "has-property-descriptors": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/string.prototype.trimend": {
      "version": "1.0.9",
      "resolved": "https://registry.npmjs.org/string.prototype.trimend/-/string.prototype.trimend-1.0.9.tgz",
      "integrity": "sha512-G7Ok5C6E/j4SGfyLCloXTrngQIQU3PWtXGst3yM7Bea9FRURf1S42ZHlZZtsNque2FN2PoUhfZXYLNWwEr4dLQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.2",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/string.prototype.trimstart": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/string.prototype.trimstart/-/string.prototype.trimstart-1.0.8.tgz",
      "integrity": "sha512-UXSH262CSZY1tfu3G3Secr6uGLCFVPMhIqHjlgCUtCCcgihYc/xKs9djMTMUOb2j1mVSeU8EU6NWc/iQKU6Gfg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/stringify-object": {
      "version": "3.3.0",
      "resolved": "https://registry.npmjs.org/stringify-object/-/stringify-object-3.3.0.tgz",
      "integrity": "sha512-rHqiFh1elqCQ9WPLIC8I0Q/g/wj5J1eMkyoiD6eoQApWHP0FtlK7rqnhmabL5VUY9JQCcqwwvlOaSuutekgyrw==",
      "dev": true,
      "license": "BSD-2-Clause",
      "dependencies": {
        "get-own-enumerable-property-symbols": "^3.0.0",
        "is-obj": "^1.0.1",
        "is-regexp": "^1.0.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/strip-ansi": {
      "version": "7.2.0",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-7.2.0.tgz",
      "integrity": "sha512-yDPMNjp4WyfYBkHnjIRLfca1i6KMyGCtsVgoKe/z1+6vukgaENdgGBZt+ZmKPc4gavvEZ5OgHfHdrazhgNyG7w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^6.2.2"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/strip-ansi?sponsor=1"
      }
    },
    "node_modules/strip-ansi-cjs": {
      "name": "strip-ansi",
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-6.0.1.tgz",
      "integrity": "sha512-Y38VPSHcqkFrCpFnQ9vuSXmquuv5oXOKpGeT6aGrr3o3Gc9AlVa6JBfUSOCnbxGGZF+/0ooI7KrPuUSztUdU5A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/strip-ansi-cjs/node_modules/ansi-regex": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/ansi-regex/-/ansi-regex-5.0.1.tgz",
      "integrity": "sha512-quJQXlTSUGL2LH9SUXo8VwsY4soanhgo6LNSm84E1LBcE8s3O0wpdiRzyR9z/ZZJMlMWv37qOOb9pdJlMUEKFQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/strip-bom": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/strip-bom/-/strip-bom-3.0.0.tgz",
      "integrity": "sha512-vavAMRXOgBVNF6nyEEmL3DBK19iRpDcoIwW+swQ+CbGiu7lju6t+JklA1MHweoWtadgt4ISVUsXLyDq34ddcwA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/strip-comments": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/strip-comments/-/strip-comments-2.0.1.tgz",
      "integrity": "sha512-ZprKx+bBLXv067WTCALv8SSz5l2+XhpYCsVtSqlMnkAXMWDq+/ekVbl1ghqP9rUHTzv6sm/DwCOiYutU/yp1fw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/strip-indent": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/strip-indent/-/strip-indent-4.1.1.tgz",
      "integrity": "sha512-SlyRoSkdh1dYP0PzclLE7r0M9sgbFKKMFXpFRUMNuKhQSbC6VQIGzq3E0qsfvGJaUFJPGv6Ws1NZ/haTAjfbMA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/stylis": {
      "version": "4.3.6",
      "resolved": "https://registry.npmjs.org/stylis/-/stylis-4.3.6.tgz",
      "integrity": "sha512-yQ3rwFWRfwNUY7H5vpU0wfdkNSnvnJinhF9830Swlaxl03zsOjCfmX0ugac+3LtK0lYSgwL/KXc8oYL3mG4YFQ==",
      "license": "MIT"
    },
    "node_modules/supports-color": {
      "version": "10.2.2",
      "resolved": "https://registry.npmjs.org/supports-color/-/supports-color-10.2.2.tgz",
      "integrity": "sha512-SS+jx45GF1QjgEXQx4NJZV9ImqmO2NPz5FNsIHrsDjh2YsHnawpan7SNQ1o8NuhrbHZy9AZhIoCUiCeaW/C80g==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=18"
      },
      "funding": {
        "url": "https://github.com/chalk/supports-color?sponsor=1"
      }
    },
    "node_modules/supports-preserve-symlinks-flag": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/supports-preserve-symlinks-flag/-/supports-preserve-symlinks-flag-1.0.0.tgz",
      "integrity": "sha512-ot0WnXS9fgdkgIcePe6RHNk1WA8+muPa6cSjeR3V8K27q9BB1rTE3R1p7Hv0z1ZyAc8s6Vvv8DIyWf681MAt0w==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/temp-dir": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/temp-dir/-/temp-dir-2.0.0.tgz",
      "integrity": "sha512-aoBAniQmmwtcKp/7BzsH8Cxzv8OL736p7v1ihGb5e9DJ9kTwGWHrQrVB5+lfVDzfGrdRzXch+ig7LHaY1JTOrg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/tempy": {
      "version": "0.6.0",
      "resolved": "https://registry.npmjs.org/tempy/-/tempy-0.6.0.tgz",
      "integrity": "sha512-G13vtMYPT/J8A4X2SjdtBTphZlrp1gKv6hZiOjw14RCWg6GbHuQBGtjlx75xLbYV/wEc0D7G5K4rxKP/cXk8Bw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-stream": "^2.0.0",
        "temp-dir": "^2.0.0",
        "type-fest": "^0.16.0",
        "unique-string": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/tempy/node_modules/type-fest": {
      "version": "0.16.0",
      "resolved": "https://registry.npmjs.org/type-fest/-/type-fest-0.16.0.tgz",
      "integrity": "sha512-eaBzG6MxNzEn9kiwvtre90cXaNLkmadMWa1zQMs3XORCXNbsH/OewwbxC5ia9dCxIxnTAsSxXJaa/p5y8DlvJg==",
      "dev": true,
      "license": "(MIT OR CC0-1.0)",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/terser": {
      "version": "5.46.1",
      "resolved": "https://registry.npmjs.org/terser/-/terser-5.46.1.tgz",
      "integrity": "sha512-vzCjQO/rgUuK9sf8VJZvjqiqiHFaZLnOiimmUuOKODxWL8mm/xua7viT7aqX7dgPY60otQjUotzFMmCB4VdmqQ==",
      "dev": true,
      "license": "BSD-2-Clause",
      "peer": true,
      "dependencies": {
        "@jridgewell/source-map": "^0.3.3",
        "acorn": "^8.15.0",
        "commander": "^2.20.0",
        "source-map-support": "~0.5.20"
      },
      "bin": {
        "terser": "bin/terser"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/throttle-debounce": {
      "version": "5.0.2",
      "resolved": "https://registry.npmjs.org/throttle-debounce/-/throttle-debounce-5.0.2.tgz",
      "integrity": "sha512-B71/4oyj61iNH0KeCamLuE2rmKuTO5byTOSVwECM5FA7TiAiAW+UqTKZ9ERueC4qvgSttUhdmq1mXC3kJqGX7A==",
      "license": "MIT",
      "engines": {
        "node": ">=12.22"
      }
    },
    "node_modules/tiny-invariant": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/tiny-invariant/-/tiny-invariant-1.3.3.tgz",
      "integrity": "sha512-+FbBPE1o9QAYvviau/qC5SE3caw21q3xkvWKBtja5vgqOWIHHJ3ioaq1VPfn/Szqctz2bU/oYeKd9/z5BL+PVg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/tinyglobby": {
      "version": "0.2.15",
      "resolved": "https://registry.npmjs.org/tinyglobby/-/tinyglobby-0.2.15.tgz",
      "integrity": "sha512-j2Zq4NyQYG5XMST4cbs02Ak8iJUdxRM0XI5QyxXuZOzKOINmWurp3smXu3y5wDcJrptwpSjgXHzIQxR0omXljQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "fdir": "^6.5.0",
        "picomatch": "^4.0.3"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/SuperchupuDev"
      }
    },
    "node_modules/toggle-selection": {
      "version": "1.0.6",
      "resolved": "https://registry.npmjs.org/toggle-selection/-/toggle-selection-1.0.6.tgz",
      "integrity": "sha512-BiZS+C1OS8g/q2RRbJmy59xpyghNBqrr6k5L/uKBGRsTfxmu3ffiRnd8mlGPUVayg8pvfi5urfnu8TU7DVOkLQ==",
      "license": "MIT"
    },
    "node_modules/tr46": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/tr46/-/tr46-1.0.1.tgz",
      "integrity": "sha512-dTpowEjclQ7Kgx5SdBkqRzVhERQXov8/l9Ft9dVM9fmg0W0KQSVaXX9T4i6twCPNtYiZM53lpSSUAwJbFPOHxA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "punycode": "^2.1.0"
      }
    },
    "node_modules/ts-dedent": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/ts-dedent/-/ts-dedent-2.2.0.tgz",
      "integrity": "sha512-q5W7tVM71e2xjHZTlgfTDoPF/SmqKG5hddq9SzR49CH2hayqRKJtQ4mtRlSxKaJlR/+9rEM+mnBHf7I2/BQcpQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.10"
      }
    },
    "node_modules/tsconfig-paths": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/tsconfig-paths/-/tsconfig-paths-4.2.0.tgz",
      "integrity": "sha512-NoZ4roiN7LnbKn9QqE1amc9DJfzvZXxF4xDavcOWt1BPkdx+m+0gJuPM+S0vCe7zTJMYUP0R8pO2XMr+Y8oLIg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "json5": "^2.2.2",
        "minimist": "^1.2.6",
        "strip-bom": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/tslib": {
      "version": "2.8.1",
      "resolved": "https://registry.npmjs.org/tslib/-/tslib-2.8.1.tgz",
      "integrity": "sha512-oJFu94HQb+KVduSUQL7wnpmqnfmLsOA/nAh6b6EH0wCEoK0/mPeXU6c3wKDV83MkOuHPRHtSXKKU99IBazS/2w==",
      "dev": true,
      "license": "0BSD"
    },
    "node_modules/type-fest": {
      "version": "4.41.0",
      "resolved": "https://registry.npmjs.org/type-fest/-/type-fest-4.41.0.tgz",
      "integrity": "sha512-TeTSQ6H5YHvpqVwBRcnLDCBnDOHWYu7IvGbHT6N8AOymcr9PJGjc1GTtiWZTYg0NCgYwvnYWEkVChQAr9bjfwA==",
      "dev": true,
      "license": "(MIT OR CC0-1.0)",
      "engines": {
        "node": ">=16"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/typed-array-buffer": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/typed-array-buffer/-/typed-array-buffer-1.0.3.tgz",
      "integrity": "sha512-nAYYwfY3qnzX30IkA6AQZjVbtK6duGontcQm1WSG1MD94YLqK0515GNApXkoxKOWMusVssAHWLh9SeaoefYFGw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "is-typed-array": "^1.1.14"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/typed-array-byte-length": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/typed-array-byte-length/-/typed-array-byte-length-1.0.3.tgz",
      "integrity": "sha512-BaXgOuIxz8n8pIq3e7Atg/7s+DpiYrxn4vdot3w9KbnBhcRQq6o3xemQdIfynqSeXeDrF32x+WvfzmOjPiY9lg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "for-each": "^0.3.3",
        "gopd": "^1.2.0",
        "has-proto": "^1.2.0",
        "is-typed-array": "^1.1.14"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/typed-array-byte-offset": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/typed-array-byte-offset/-/typed-array-byte-offset-1.0.4.tgz",
      "integrity": "sha512-bTlAFB/FBYMcuX81gbL4OcpH5PmlFHqlCCpAl8AlEzMz5k53oNDvN8p1PNOWLEmI2x4orp3raOFB51tv9X+MFQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "available-typed-arrays": "^1.0.7",
        "call-bind": "^1.0.8",
        "for-each": "^0.3.3",
        "gopd": "^1.2.0",
        "has-proto": "^1.2.0",
        "is-typed-array": "^1.1.15",
        "reflect.getprototypeof": "^1.0.9"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/typed-array-length": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/typed-array-length/-/typed-array-length-1.0.7.tgz",
      "integrity": "sha512-3KS2b+kL7fsuk/eJZ7EQdnEmQoaho/r6KUef7hxvltNA5DR8NAUM+8wJMbJyZ4G9/7i3v5zPBIMN5aybAh2/Jg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "for-each": "^0.3.3",
        "gopd": "^1.0.1",
        "is-typed-array": "^1.1.13",
        "possible-typed-array-names": "^1.0.0",
        "reflect.getprototypeof": "^1.0.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/typescript": {
      "version": "5.6.3",
      "resolved": "https://registry.npmjs.org/typescript/-/typescript-5.6.3.tgz",
      "integrity": "sha512-hjcS1mhfuyi4WW8IWtjP7brDrG2cuDZukyrYrSauoXGNgx0S7zceP07adYkJycEr56BOUTNPzbInooiN3fn1qw==",
      "dev": true,
      "license": "Apache-2.0",
      "peer": true,
      "bin": {
        "tsc": "bin/tsc",
        "tsserver": "bin/tsserver"
      },
      "engines": {
        "node": ">=14.17"
      }
    },
    "node_modules/unbox-primitive": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/unbox-primitive/-/unbox-primitive-1.1.0.tgz",
      "integrity": "sha512-nWJ91DjeOkej/TA8pXQ3myruKpKEYgqvpw9lz4OPHj/NWFNluYrjbz9j01CJ8yKQd2g4jFoOkINCTW2I5LEEyw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-bigints": "^1.0.2",
        "has-symbols": "^1.1.0",
        "which-boxed-primitive": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/unicode-canonical-property-names-ecmascript": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/unicode-canonical-property-names-ecmascript/-/unicode-canonical-property-names-ecmascript-2.0.1.tgz",
      "integrity": "sha512-dA8WbNeb2a6oQzAQ55YlT5vQAWGV9WXOsi3SskE3bcCdM0P4SDd+24zS/OCacdRq5BkdsRj9q3Pg6YyQoxIGqg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/unicode-match-property-ecmascript": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/unicode-match-property-ecmascript/-/unicode-match-property-ecmascript-2.0.0.tgz",
      "integrity": "sha512-5kaZCrbp5mmbz5ulBkDkbY0SsPOjKqVS35VpL9ulMPfSl0J0Xsm+9Evphv9CoIZFwre7aJoa94AY6seMKGVN5Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "unicode-canonical-property-names-ecmascript": "^2.0.0",
        "unicode-property-aliases-ecmascript": "^2.0.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/unicode-match-property-value-ecmascript": {
      "version": "2.2.1",
      "resolved": "https://registry.npmjs.org/unicode-match-property-value-ecmascript/-/unicode-match-property-value-ecmascript-2.2.1.tgz",
      "integrity": "sha512-JQ84qTuMg4nVkx8ga4A16a1epI9H6uTXAknqxkGF/aFfRLw1xC/Bp24HNLaZhHSkWd3+84t8iXnp1J0kYcZHhg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/unicode-property-aliases-ecmascript": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/unicode-property-aliases-ecmascript/-/unicode-property-aliases-ecmascript-2.2.0.tgz",
      "integrity": "sha512-hpbDzxUY9BFwX+UeBnxv3Sh1q7HFxj48DTmXchNgRa46lO8uj3/1iEn3MiNUYTg1g9ctIqXCCERn8gYZhHC5lQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/unique-string": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/unique-string/-/unique-string-2.0.0.tgz",
      "integrity": "sha512-uNaeirEPvpZWSgzwsPGtU2zVSTrn/8L5q/IexZmH0eH6SA73CmAA5U4GwORTxQAZs95TAXLNqeLoPPNO5gZfWg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "crypto-random-string": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/universalify": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/universalify/-/universalify-2.0.1.tgz",
      "integrity": "sha512-gptHNQghINnc/vTGIk0SOFGFNXw7JVrlRUtConJRlvaw6DuX0wO5Jeko9sWrMBhh+PsYAZ7oXAiOnf/UKogyiw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 10.0.0"
      }
    },
    "node_modules/unplugin": {
      "version": "1.16.1",
      "resolved": "https://registry.npmjs.org/unplugin/-/unplugin-1.16.1.tgz",
      "integrity": "sha512-4/u/j4FrCKdi17jaxuJA0jClGxB1AvU2hw/IuayPc4ay1XGaJs/rbb4v5WKwAjNifjmXK9PIFyuPiaK8azyR9w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "acorn": "^8.14.0",
        "webpack-virtual-modules": "^0.6.2"
      },
      "engines": {
        "node": ">=14.0.0"
      }
    },
    "node_modules/upath": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/upath/-/upath-1.2.0.tgz",
      "integrity": "sha512-aZwGpamFO61g3OlfT7OQCHqhGnW43ieH9WZeP7QxN/G/jS4jfqUkZxoryvJgVPEcrl5NL/ggHsSmLMHuH64Lhg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=4",
        "yarn": "*"
      }
    },
    "node_modules/update-browserslist-db": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/update-browserslist-db/-/update-browserslist-db-1.2.3.tgz",
      "integrity": "sha512-Js0m9cx+qOgDxo0eMiFGEueWztz+d4+M3rGlmKPT+T4IS/jP4ylw3Nwpu6cpTTP8R1MAC1kF4VbdLt3ARf209w==",
      "dev": true,
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "escalade": "^3.2.0",
        "picocolors": "^1.1.1"
      },
      "bin": {
        "update-browserslist-db": "cli.js"
      },
      "peerDependencies": {
        "browserslist": ">= 4.21.0"
      }
    },
    "node_modules/uri-js-replace": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/uri-js-replace/-/uri-js-replace-1.0.1.tgz",
      "integrity": "sha512-W+C9NWNLFOoBI2QWDp4UT9pv65r2w5Cx+3sTYFvtMdDBxkKt1syCqsUdSFAChbEe1uK5TfS04wt/nGwmaeIQ0g==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/util": {
      "version": "0.12.5",
      "resolved": "https://registry.npmjs.org/util/-/util-0.12.5.tgz",
      "integrity": "sha512-kZf/K6hEIrWHI6XqOFUiiMa+79wE/D8Q+NCNAWclkyg3b4d2k7s0QGepNjiABc+aR3N1PAyHL7p6UcLY6LmrnA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "inherits": "^2.0.3",
        "is-arguments": "^1.0.4",
        "is-generator-function": "^1.0.7",
        "is-typed-array": "^1.1.3",
        "which-typed-array": "^1.1.2"
      }
    },
    "node_modules/uuid": {
      "version": "9.0.1",
      "resolved": "https://registry.npmjs.org/uuid/-/uuid-9.0.1.tgz",
      "integrity": "sha512-b+1eJOlsR9K8HJpow9Ok3fiWOWSIcIzXodvv0rQjVoOVNpWMpxf1wZNpt4y9h10odCNrqnYp1OBzRktckBe3sA==",
      "dev": true,
      "funding": [
        "https://github.com/sponsors/broofa",
        "https://github.com/sponsors/ctavan"
      ],
      "license": "MIT",
      "bin": {
        "uuid": "dist/bin/uuid"
      }
    },
    "node_modules/vite": {
      "version": "5.4.21",
      "resolved": "https://registry.npmjs.org/vite/-/vite-5.4.21.tgz",
      "integrity": "sha512-o5a9xKjbtuhY6Bi5S3+HvbRERmouabWbyUcpXXUA1u+GNUKoROi9byOJ8M0nHbHYHkYICiMlqxkg1KkYmm25Sw==",
      "dev": true,
      "license": "MIT",
      "peer": true,
      "dependencies": {
        "esbuild": "^0.21.3",
        "postcss": "^8.4.43",
        "rollup": "^4.20.0"
      },
      "bin": {
        "vite": "bin/vite.js"
      },
      "engines": {
        "node": "^18.0.0 || >=20.0.0"
      },
      "funding": {
        "url": "https://github.com/vitejs/vite?sponsor=1"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.3"
      },
      "peerDependencies": {
        "@types/node": "^18.0.0 || >=20.0.0",
        "less": "*",
        "lightningcss": "^1.21.0",
        "sass": "*",
        "sass-embedded": "*",
        "stylus": "*",
        "sugarss": "*",
        "terser": "^5.4.0"
      },
      "peerDependenciesMeta": {
        "@types/node": {
          "optional": true
        },
        "less": {
          "optional": true
        },
        "lightningcss": {
          "optional": true
        },
        "sass": {
          "optional": true
        },
        "sass-embedded": {
          "optional": true
        },
        "stylus": {
          "optional": true
        },
        "sugarss": {
          "optional": true
        },
        "terser": {
          "optional": true
        }
      }
    },
    "node_modules/vite-plugin-pwa": {
      "version": "0.21.2",
      "resolved": "https://registry.npmjs.org/vite-plugin-pwa/-/vite-plugin-pwa-0.21.2.tgz",
      "integrity": "sha512-vFhH6Waw8itNu37hWUJxL50q+CBbNcMVzsKaYHQVrfxTt3ihk3PeLO22SbiP1UNWzcEPaTQv+YVxe4G0KOjAkg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "debug": "^4.3.6",
        "pretty-bytes": "^6.1.1",
        "tinyglobby": "^0.2.10",
        "workbox-build": "^7.3.0",
        "workbox-window": "^7.3.0"
      },
      "engines": {
        "node": ">=16.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/antfu"
      },
      "peerDependencies": {
        "@vite-pwa/assets-generator": "^0.2.6",
        "vite": "^3.1.0 || ^4.0.0 || ^5.0.0 || ^6.0.0",
        "workbox-build": "^7.3.0",
        "workbox-window": "^7.3.0"
      },
      "peerDependenciesMeta": {
        "@vite-pwa/assets-generator": {
          "optional": true
        }
      }
    },
    "node_modules/webidl-conversions": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/webidl-conversions/-/webidl-conversions-4.0.2.tgz",
      "integrity": "sha512-YQ+BmxuTgd6UXZW3+ICGfyqRyHXVlD5GtQr5+qjiNW7bF0cqrzX500HVXPBOvgXb5YnzDd+h0zqyv61KUD7+Sg==",
      "dev": true,
      "license": "BSD-2-Clause"
    },
    "node_modules/webpack-virtual-modules": {
      "version": "0.6.2",
      "resolved": "https://registry.npmjs.org/webpack-virtual-modules/-/webpack-virtual-modules-0.6.2.tgz",
      "integrity": "sha512-66/V2i5hQanC51vBQKPH4aI8NMAcBW59FVBs+rC7eGHupMyfn34q7rZIE+ETlJ+XTevqfUhVVBgSUNSW2flEUQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/whatwg-url": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/whatwg-url/-/whatwg-url-7.1.0.tgz",
      "integrity": "sha512-WUu7Rg1DroM7oQvGWfOiAK21n74Gg+T4elXEQYkOhtyLeWiJFoOGLXPKI/9gzIie9CtwVLm8wtw6YJdKyxSjeg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "lodash.sortby": "^4.7.0",
        "tr46": "^1.0.1",
        "webidl-conversions": "^4.0.2"
      }
    },
    "node_modules/which": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/which/-/which-2.0.2.tgz",
      "integrity": "sha512-BLI3Tl1TW3Pvl70l3yq3Y64i+awpwXqsGBYWkkqMtnbXgrMD+yj7rhW0kuEDxzJaYXGjEW5ogapKNMEKNMjibA==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "isexe": "^2.0.0"
      },
      "bin": {
        "node-which": "bin/node-which"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/which-boxed-primitive": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/which-boxed-primitive/-/which-boxed-primitive-1.1.1.tgz",
      "integrity": "sha512-TbX3mj8n0odCBFVlY8AxkqcHASw3L60jIuF8jFP78az3C2YhmGvqbHBpAjTRH2/xqYunrJ9g1jSyjCjpoWzIAA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-bigint": "^1.1.0",
        "is-boolean-object": "^1.2.1",
        "is-number-object": "^1.1.1",
        "is-string": "^1.1.1",
        "is-symbol": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/which-builtin-type": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/which-builtin-type/-/which-builtin-type-1.2.1.tgz",
      "integrity": "sha512-6iBczoX+kDQ7a3+YJBnh3T+KZRxM/iYNPXicqk66/Qfm1b93iu+yOImkg0zHbj5LNOcNv1TEADiZ0xa34B4q6Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "function.prototype.name": "^1.1.6",
        "has-tostringtag": "^1.0.2",
        "is-async-function": "^2.0.0",
        "is-date-object": "^1.1.0",
        "is-finalizationregistry": "^1.1.0",
        "is-generator-function": "^1.0.10",
        "is-regex": "^1.2.1",
        "is-weakref": "^1.0.2",
        "isarray": "^2.0.5",
        "which-boxed-primitive": "^1.1.0",
        "which-collection": "^1.0.2",
        "which-typed-array": "^1.1.16"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/which-collection": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/which-collection/-/which-collection-1.0.2.tgz",
      "integrity": "sha512-K4jVyjnBdgvc86Y6BkaLZEN933SwYOuBFkdmBu9ZfkcAbdVbpITnDmjvZ/aQjRXQrv5EPkTnD1s39GiiqbngCw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "is-map": "^2.0.3",
        "is-set": "^2.0.3",
        "is-weakmap": "^2.0.2",
        "is-weakset": "^2.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/which-typed-array": {
      "version": "1.1.20",
      "resolved": "https://registry.npmjs.org/which-typed-array/-/which-typed-array-1.1.20.tgz",
      "integrity": "sha512-LYfpUkmqwl0h9A2HL09Mms427Q1RZWuOHsukfVcKRq9q95iQxdw0ix1JQrqbcDR9PH1QDwf5Qo8OZb5lksZ8Xg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "available-typed-arrays": "^1.0.7",
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "for-each": "^0.3.5",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/workbox-background-sync": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-background-sync/-/workbox-background-sync-7.4.0.tgz",
      "integrity": "sha512-8CB9OxKAgKZKyNMwfGZ1XESx89GryWTfI+V5yEj8sHjFH8MFelUwYXEyldEK6M6oKMmn807GoJFUEA1sC4XS9w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "idb": "^7.0.1",
        "workbox-core": "7.4.0"
      }
    },
    "node_modules/workbox-broadcast-update": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-broadcast-update/-/workbox-broadcast-update-7.4.0.tgz",
      "integrity": "sha512-+eZQwoktlvo62cI0b+QBr40v5XjighxPq3Fzo9AWMiAosmpG5gxRHgTbGGhaJv/q/MFVxwFNGh/UwHZ/8K88lA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "workbox-core": "7.4.0"
      }
    },
    "node_modules/workbox-build": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-build/-/workbox-build-7.4.0.tgz",
      "integrity": "sha512-Ntk1pWb0caOFIvwz/hfgrov/OJ45wPEhI5PbTywQcYjyZiVhT3UrwwUPl6TRYbTm4moaFYithYnl1lvZ8UjxcA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@apideck/better-ajv-errors": "^0.3.1",
        "@babel/core": "^7.24.4",
        "@babel/preset-env": "^7.11.0",
        "@babel/runtime": "^7.11.2",
        "@rollup/plugin-babel": "^5.2.0",
        "@rollup/plugin-node-resolve": "^15.2.3",
        "@rollup/plugin-replace": "^2.4.1",
        "@rollup/plugin-terser": "^0.4.3",
        "@surma/rollup-plugin-off-main-thread": "^2.2.3",
        "ajv": "^8.6.0",
        "common-tags": "^1.8.0",
        "fast-json-stable-stringify": "^2.1.0",
        "fs-extra": "^9.0.1",
        "glob": "^11.0.1",
        "lodash": "^4.17.20",
        "pretty-bytes": "^5.3.0",
        "rollup": "^2.79.2",
        "source-map": "^0.8.0-beta.0",
        "stringify-object": "^3.3.0",
        "strip-comments": "^2.0.1",
        "tempy": "^0.6.0",
        "upath": "^1.2.0",
        "workbox-background-sync": "7.4.0",
        "workbox-broadcast-update": "7.4.0",
        "workbox-cacheable-response": "7.4.0",
        "workbox-core": "7.4.0",
        "workbox-expiration": "7.4.0",
        "workbox-google-analytics": "7.4.0",
        "workbox-navigation-preload": "7.4.0",
        "workbox-precaching": "7.4.0",
        "workbox-range-requests": "7.4.0",
        "workbox-recipes": "7.4.0",
        "workbox-routing": "7.4.0",
        "workbox-strategies": "7.4.0",
        "workbox-streams": "7.4.0",
        "workbox-sw": "7.4.0",
        "workbox-window": "7.4.0"
      },
      "engines": {
        "node": ">=20.0.0"
      }
    },
    "node_modules/workbox-build/node_modules/@isaacs/cliui": {
      "version": "9.0.0",
      "resolved": "https://registry.npmjs.org/@isaacs/cliui/-/cliui-9.0.0.tgz",
      "integrity": "sha512-AokJm4tuBHillT+FpMtxQ60n8ObyXBatq7jD2/JA9dxbDDokKQm8KMht5ibGzLVU9IJDIKK4TPKgMHEYMn3lMg==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/workbox-build/node_modules/@rollup/plugin-babel": {
      "version": "5.3.1",
      "resolved": "https://registry.npmjs.org/@rollup/plugin-babel/-/plugin-babel-5.3.1.tgz",
      "integrity": "sha512-WFfdLWU/xVWKeRQnKmIAQULUI7Il0gZnBIH/ZFO069wYIfPu+8zrfp/KMW0atmELoRDq8FbiP3VCss9MhCut7Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.10.4",
        "@rollup/pluginutils": "^3.1.0"
      },
      "engines": {
        "node": ">= 10.0.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0",
        "@types/babel__core": "^7.1.9",
        "rollup": "^1.20.0||^2.0.0"
      },
      "peerDependenciesMeta": {
        "@types/babel__core": {
          "optional": true
        }
      }
    },
    "node_modules/workbox-build/node_modules/@rollup/plugin-replace": {
      "version": "2.4.2",
      "resolved": "https://registry.npmjs.org/@rollup/plugin-replace/-/plugin-replace-2.4.2.tgz",
      "integrity": "sha512-IGcu+cydlUMZ5En85jxHH4qj2hta/11BHq95iHEyb2sbgiN0eCdzvUcHw5gt9pBL5lTi4JDYJ1acCoMGpTvEZg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@rollup/pluginutils": "^3.1.0",
        "magic-string": "^0.25.7"
      },
      "peerDependencies": {
        "rollup": "^1.20.0 || ^2.0.0"
      }
    },
    "node_modules/workbox-build/node_modules/@rollup/pluginutils": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/@rollup/pluginutils/-/pluginutils-3.1.0.tgz",
      "integrity": "sha512-GksZ6pr6TpIjHm8h9lSQ8pi8BE9VeubNT0OMJ3B5uZJ8pz73NPiqOtCog/x2/QzM1ENChPKxMDhiQuRHsqc+lg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@types/estree": "0.0.39",
        "estree-walker": "^1.0.1",
        "picomatch": "^2.2.2"
      },
      "engines": {
        "node": ">= 8.0.0"
      },
      "peerDependencies": {
        "rollup": "^1.20.0||^2.0.0"
      }
    },
    "node_modules/workbox-build/node_modules/@types/estree": {
      "version": "0.0.39",
      "resolved": "https://registry.npmjs.org/@types/estree/-/estree-0.0.39.tgz",
      "integrity": "sha512-EYNwp3bU+98cpU4lAWYYL7Zz+2gryWH1qbdDTidVd6hkiR6weksdbMadyXKXNPEkQFhXM+hVO9ZygomHXp+AIw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/workbox-build/node_modules/balanced-match": {
      "version": "4.0.4",
      "resolved": "https://registry.npmjs.org/balanced-match/-/balanced-match-4.0.4.tgz",
      "integrity": "sha512-BLrgEcRTwX2o6gGxGOCNyMvGSp35YofuYzw9h1IMTRmKqttAZZVU67bdb9Pr2vUHA8+j3i2tJfjO6C6+4myGTA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "18 || 20 || >=22"
      }
    },
    "node_modules/workbox-build/node_modules/brace-expansion": {
      "version": "5.0.4",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-5.0.4.tgz",
      "integrity": "sha512-h+DEnpVvxmfVefa4jFbCf5HdH5YMDXRsmKflpf1pILZWRFlTbJpxeU55nJl4Smt5HQaGzg1o6RHFPJaOqnmBDg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "balanced-match": "^4.0.2"
      },
      "engines": {
        "node": "18 || 20 || >=22"
      }
    },
    "node_modules/workbox-build/node_modules/estree-walker": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/estree-walker/-/estree-walker-1.0.1.tgz",
      "integrity": "sha512-1fMXF3YP4pZZVozF8j/ZLfvnR8NSIljt56UhbZ5PeeDmmGHpgpdwQt7ITlGvYaQukCvuBRMLEiKiYC+oeIg4cg==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/workbox-build/node_modules/glob": {
      "version": "11.1.0",
      "resolved": "https://registry.npmjs.org/glob/-/glob-11.1.0.tgz",
      "integrity": "sha512-vuNwKSaKiqm7g0THUBu2x7ckSs3XJLXE+2ssL7/MfTGPLLcrJQ/4Uq1CjPTtO5cCIiRxqvN6Twy1qOwhL0Xjcw==",
      "deprecated": "Old versions of glob are not supported, and contain widely publicized security vulnerabilities, which have been fixed in the current version. Please update. Support for old versions may be purchased (at exorbitant rates) by contacting i@izs.me",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "foreground-child": "^3.3.1",
        "jackspeak": "^4.1.1",
        "minimatch": "^10.1.1",
        "minipass": "^7.1.2",
        "package-json-from-dist": "^1.0.0",
        "path-scurry": "^2.0.0"
      },
      "bin": {
        "glob": "dist/esm/bin.mjs"
      },
      "engines": {
        "node": "20 || >=22"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/workbox-build/node_modules/jackspeak": {
      "version": "4.2.3",
      "resolved": "https://registry.npmjs.org/jackspeak/-/jackspeak-4.2.3.tgz",
      "integrity": "sha512-ykkVRwrYvFm1nb2AJfKKYPr0emF6IiXDYUaFx4Zn9ZuIH7MrzEZ3sD5RlqGXNRpHtvUHJyOnCEFxOlNDtGo7wg==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "@isaacs/cliui": "^9.0.0"
      },
      "engines": {
        "node": "20 || >=22"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/workbox-build/node_modules/lru-cache": {
      "version": "11.2.7",
      "resolved": "https://registry.npmjs.org/lru-cache/-/lru-cache-11.2.7.tgz",
      "integrity": "sha512-aY/R+aEsRelme17KGQa/1ZSIpLpNYYrhcrepKTZgE+W3WM16YMCaPwOHLHsmopZHELU0Ojin1lPVxKR0MihncA==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "engines": {
        "node": "20 || >=22"
      }
    },
    "node_modules/workbox-build/node_modules/magic-string": {
      "version": "0.25.9",
      "resolved": "https://registry.npmjs.org/magic-string/-/magic-string-0.25.9.tgz",
      "integrity": "sha512-RmF0AsMzgt25qzqqLc1+MbHmhdx0ojF2Fvs4XnOqz2ZOBXzzkEwc/dJQZCYHAn7v1jbVOjAZfK8msRn4BxO4VQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "sourcemap-codec": "^1.4.8"
      }
    },
    "node_modules/workbox-build/node_modules/minimatch": {
      "version": "10.2.4",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-10.2.4.tgz",
      "integrity": "sha512-oRjTw/97aTBN0RHbYCdtF1MQfvusSIBQM0IZEgzl6426+8jSC0nF1a/GmnVLpfB9yyr6g6FTqWqiZVbxrtaCIg==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "brace-expansion": "^5.0.2"
      },
      "engines": {
        "node": "18 || 20 || >=22"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/workbox-build/node_modules/path-scurry": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/path-scurry/-/path-scurry-2.0.2.tgz",
      "integrity": "sha512-3O/iVVsJAPsOnpwWIeD+d6z/7PmqApyQePUtCndjatj/9I5LylHvt5qluFaBT3I5h3r1ejfR056c+FCv+NnNXg==",
      "dev": true,
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "lru-cache": "^11.0.0",
        "minipass": "^7.1.2"
      },
      "engines": {
        "node": "18 || 20 || >=22"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/workbox-build/node_modules/picomatch": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-2.3.1.tgz",
      "integrity": "sha512-JU3teHTNjmE2VCGFzuY8EXzCDVwEqB2a8fsIvwaStHhAWJEeVd1o1QD80CU6+ZdEXXSLbSsuLwJjkCBWqRQUVA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/workbox-build/node_modules/pretty-bytes": {
      "version": "5.6.0",
      "resolved": "https://registry.npmjs.org/pretty-bytes/-/pretty-bytes-5.6.0.tgz",
      "integrity": "sha512-FFw039TmrBqFK8ma/7OL3sDz/VytdtJr044/QUJtH0wK9lb9jLq9tJyIxUwtQJHwar2BqtiA4iCWSwo9JLkzFg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/workbox-build/node_modules/rollup": {
      "version": "2.80.0",
      "resolved": "https://registry.npmjs.org/rollup/-/rollup-2.80.0.tgz",
      "integrity": "sha512-cIFJOD1DESzpjOBl763Kp1AH7UE/0fcdHe6rZXUdQ9c50uvgigvW97u3IcSeBwOkgqL/PXPBktBCh0KEu5L8XQ==",
      "dev": true,
      "license": "MIT",
      "peer": true,
      "bin": {
        "rollup": "dist/bin/rollup"
      },
      "engines": {
        "node": ">=10.0.0"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.2"
      }
    },
    "node_modules/workbox-build/node_modules/source-map": {
      "version": "0.8.0-beta.0",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.8.0-beta.0.tgz",
      "integrity": "sha512-2ymg6oRBpebeZi9UUNsgQ89bhx01TcTkmNTGnNO88imTmbSgy4nfujrgVEFKWpMTEGA11EDkTt7mqObTPdigIA==",
      "deprecated": "The work that was done in this beta branch won't be included in future versions",
      "dev": true,
      "license": "BSD-3-Clause",
      "dependencies": {
        "whatwg-url": "^7.0.0"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/workbox-cacheable-response": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-cacheable-response/-/workbox-cacheable-response-7.4.0.tgz",
      "integrity": "sha512-0Fb8795zg/x23ISFkAc7lbWes6vbw34DGFIMw31cwuHPgDEC/5EYm6m/ZkylLX0EnEbbOyOCLjKgFS/Z5g0HeQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "workbox-core": "7.4.0"
      }
    },
    "node_modules/workbox-core": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-core/-/workbox-core-7.4.0.tgz",
      "integrity": "sha512-6BMfd8tYEnN4baG4emG9U0hdXM4gGuDU3ectXuVHnj71vwxTFI7WOpQJC4siTOlVtGqCUtj0ZQNsrvi6kZZTAQ==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/workbox-expiration": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-expiration/-/workbox-expiration-7.4.0.tgz",
      "integrity": "sha512-V50p4BxYhtA80eOvulu8xVfPBgZbkxJ1Jr8UUn0rvqjGhLDqKNtfrDfjJKnLz2U8fO2xGQJTx/SKXNTzHOjnHw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "idb": "^7.0.1",
        "workbox-core": "7.4.0"
      }
    },
    "node_modules/workbox-google-analytics": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-google-analytics/-/workbox-google-analytics-7.4.0.tgz",
      "integrity": "sha512-MVPXQslRF6YHkzGoFw1A4GIB8GrKym/A5+jYDUSL+AeJw4ytQGrozYdiZqUW1TPQHW8isBCBtyFJergUXyNoWQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "workbox-background-sync": "7.4.0",
        "workbox-core": "7.4.0",
        "workbox-routing": "7.4.0",
        "workbox-strategies": "7.4.0"
      }
    },
    "node_modules/workbox-navigation-preload": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-navigation-preload/-/workbox-navigation-preload-7.4.0.tgz",
      "integrity": "sha512-etzftSgdQfjMcfPgbfaZCfM2QuR1P+4o8uCA2s4rf3chtKTq/Om7g/qvEOcZkG6v7JZOSOxVYQiOu6PbAZgU6w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "workbox-core": "7.4.0"
      }
    },
    "node_modules/workbox-precaching": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-precaching/-/workbox-precaching-7.4.0.tgz",
      "integrity": "sha512-VQs37T6jDqf1rTxUJZXRl3yjZMf5JX/vDPhmx2CPgDDKXATzEoqyRqhYnRoxl6Kr0rqaQlp32i9rtG5zTzIlNg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "workbox-core": "7.4.0",
        "workbox-routing": "7.4.0",
        "workbox-strategies": "7.4.0"
      }
    },
    "node_modules/workbox-range-requests": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-range-requests/-/workbox-range-requests-7.4.0.tgz",
      "integrity": "sha512-3Vq854ZNuP6Y0KZOQWLaLC9FfM7ZaE+iuQl4VhADXybwzr4z/sMmnLgTeUZLq5PaDlcJBxYXQ3U91V7dwAIfvw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "workbox-core": "7.4.0"
      }
    },
    "node_modules/workbox-recipes": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-recipes/-/workbox-recipes-7.4.0.tgz",
      "integrity": "sha512-kOkWvsAn4H8GvAkwfJTbwINdv4voFoiE9hbezgB1sb/0NLyTG4rE7l6LvS8lLk5QIRIto+DjXLuAuG3Vmt3cxQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "workbox-cacheable-response": "7.4.0",
        "workbox-core": "7.4.0",
        "workbox-expiration": "7.4.0",
        "workbox-precaching": "7.4.0",
        "workbox-routing": "7.4.0",
        "workbox-strategies": "7.4.0"
      }
    },
    "node_modules/workbox-routing": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-routing/-/workbox-routing-7.4.0.tgz",
      "integrity": "sha512-C/ooj5uBWYAhAqwmU8HYQJdOjjDKBp9MzTQ+otpMmd+q0eF59K+NuXUek34wbL0RFrIXe/KKT+tUWcZcBqxbHQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "workbox-core": "7.4.0"
      }
    },
    "node_modules/workbox-strategies": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-strategies/-/workbox-strategies-7.4.0.tgz",
      "integrity": "sha512-T4hVqIi5A4mHi92+5EppMX3cLaVywDp8nsyUgJhOZxcfSV/eQofcOA6/EMo5rnTNmNTpw0rUgjAI6LaVullPpg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "workbox-core": "7.4.0"
      }
    },
    "node_modules/workbox-streams": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-streams/-/workbox-streams-7.4.0.tgz",
      "integrity": "sha512-QHPBQrey7hQbnTs5GrEVoWz7RhHJXnPT+12qqWM378orDMo5VMJLCkCM1cnCk+8Eq92lccx/VgRZ7WAzZWbSLg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "workbox-core": "7.4.0",
        "workbox-routing": "7.4.0"
      }
    },
    "node_modules/workbox-sw": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-sw/-/workbox-sw-7.4.0.tgz",
      "integrity": "sha512-ltU+Kr3qWR6BtbdlMnCjobZKzeV1hN+S6UvDywBrwM19TTyqA03X66dzw1tEIdJvQ4lYKkBFox6IAEhoSEZ8Xw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/workbox-window": {
      "version": "7.4.0",
      "resolved": "https://registry.npmjs.org/workbox-window/-/workbox-window-7.4.0.tgz",
      "integrity": "sha512-/bIYdBLAVsNR3v7gYGaV4pQW3M3kEPx5E8vDxGvxo6khTrGtSSCS7QiFKv9ogzBgZiy0OXLP9zO28U/1nF1mfw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@types/trusted-types": "^2.0.2",
        "workbox-core": "7.4.0"
      }
    },
    "node_modules/wrap-ansi": {
      "version": "8.1.0",
      "resolved": "https://registry.npmjs.org/wrap-ansi/-/wrap-ansi-8.1.0.tgz",
      "integrity": "sha512-si7QWI6zUMq56bESFvagtmzMdGOtoxfR+Sez11Mobfc7tm+VkUckk9bW2UeffTGVUbOksxmSw0AA2gs8g71NCQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^6.1.0",
        "string-width": "^5.0.1",
        "strip-ansi": "^7.0.1"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/wrap-ansi?sponsor=1"
      }
    },
    "node_modules/wrap-ansi-cjs": {
      "name": "wrap-ansi",
      "version": "7.0.0",
      "resolved": "https://registry.npmjs.org/wrap-ansi/-/wrap-ansi-7.0.0.tgz",
      "integrity": "sha512-YVGIj2kamLSTxw6NsZjoBxfSwsn0ycdesmc4p+Q21c5zPuZ1pl+NfxVdxPtdHvmNVOQ6XSYG4AUtyt/Fi7D16Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^4.0.0",
        "string-width": "^4.1.0",
        "strip-ansi": "^6.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/wrap-ansi?sponsor=1"
      }
    },
    "node_modules/wrap-ansi-cjs/node_modules/ansi-regex": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/ansi-regex/-/ansi-regex-5.0.1.tgz",
      "integrity": "sha512-quJQXlTSUGL2LH9SUXo8VwsY4soanhgo6LNSm84E1LBcE8s3O0wpdiRzyR9z/ZZJMlMWv37qOOb9pdJlMUEKFQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/wrap-ansi-cjs/node_modules/ansi-styles": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-4.3.0.tgz",
      "integrity": "sha512-zbB9rCJAT1rbjiVDb2hqKFHNYLxgtk8NURxZ3IZwD3F6NtxbXZQCnnSi1Lkx+IDohdPlFp222wVALIheZJQSEg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "color-convert": "^2.0.1"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-styles?sponsor=1"
      }
    },
    "node_modules/wrap-ansi-cjs/node_modules/emoji-regex": {
      "version": "8.0.0",
      "resolved": "https://registry.npmjs.org/emoji-regex/-/emoji-regex-8.0.0.tgz",
      "integrity": "sha512-MSjYzcWNOA0ewAHpz0MxpYFvwg6yjy1NG3xteoqz644VCo/RPgnr1/GGt+ic3iJTzQ8Eu3TdM14SawnVUmGE6A==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/wrap-ansi-cjs/node_modules/string-width": {
      "version": "4.2.3",
      "resolved": "https://registry.npmjs.org/string-width/-/string-width-4.2.3.tgz",
      "integrity": "sha512-wKyQRQpjJ0sIp62ErSZdGsjMJWsap5oRNihHhu6G7JVO/9jIB6UyevL+tXuOqrng8j/cxKTWyWUwvSTriiZz/g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "emoji-regex": "^8.0.0",
        "is-fullwidth-code-point": "^3.0.0",
        "strip-ansi": "^6.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/wrap-ansi-cjs/node_modules/strip-ansi": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-6.0.1.tgz",
      "integrity": "sha512-Y38VPSHcqkFrCpFnQ9vuSXmquuv5oXOKpGeT6aGrr3o3Gc9AlVa6JBfUSOCnbxGGZF+/0ooI7KrPuUSztUdU5A==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/ws": {
      "version": "8.19.0",
      "resolved": "https://registry.npmjs.org/ws/-/ws-8.19.0.tgz",
      "integrity": "sha512-blAT2mjOEIi0ZzruJfIhb3nps74PRWTCz1IjglWEEpQl5XS/UNama6u2/rjFkDDouqr4L67ry+1aGIALViWjDg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=10.0.0"
      },
      "peerDependencies": {
        "bufferutil": "^4.0.1",
        "utf-8-validate": ">=5.0.2"
      },
      "peerDependenciesMeta": {
        "bufferutil": {
          "optional": true
        },
        "utf-8-validate": {
          "optional": true
        }
      }
    },
    "node_modules/yallist": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/yallist/-/yallist-3.1.1.tgz",
      "integrity": "sha512-a4UGQaWPH59mOXUYnAG2ewncQS4i4F43Tv3JoAM+s2VDAmS9NsK8GpDMLrCHPksFT7h3K6TOoUNn2pb7RoXx4g==",
      "dev": true,
      "license": "ISC"
    },
    "node_modules/yaml-ast-parser": {
      "version": "0.0.43",
      "resolved": "https://registry.npmjs.org/yaml-ast-parser/-/yaml-ast-parser-0.0.43.tgz",
      "integrity": "sha512-2PTINUwsRqSd+s8XxKaJWQlUuEMHJQyEuh2edBbW8KNJz0SJPwUSD2zRWqezFEdN7IzAgeuYHFUCF7o8zRdZ0A==",
      "dev": true,
      "license": "Apache-2.0"
    },
    "node_modules/yargs-parser": {
      "version": "21.1.1",
      "resolved": "https://registry.npmjs.org/yargs-parser/-/yargs-parser-21.1.1.tgz",
      "integrity": "sha512-tVpsJW7DdjecAiFpbIB1e3qxIQsE6NoPc5/eTdrbbIC4h0LVsWhnoa3g+m2HclBIujHzsxZ4VJVA+GUuc2/LBw==",
      "dev": true,
      "license": "ISC",
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/yocto-queue": {
      "version": "0.1.0",
      "resolved": "https://registry.npmjs.org/yocto-queue/-/yocto-queue-0.1.0.tgz",
      "integrity": "sha512-rVksvsnNCdJ/ohGc6xgPwyN8eheCxsiLM8mxuE/t/mOVqJewPuO1miLpTHQiRgTKCLexL4MeAFVagts7HmNZ2Q==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    }
  }
}

```


---

## Исходный код: `frontend/package.json`

> 40 строк, 1,186 байт

```json
{
  "name": "stream-sponsor-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview",
    "codegen:api": "openapi-typescript http://127.0.0.1:8000/openapi.json -o src/api/generated/schema.ts",
    "test:e2e": "playwright test -c e2e/playwright.config.ts",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build -o storybook-static"
  },
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

## Исходный код: `frontend/src/App.tsx`

> 109 строк, 3,037 байт

```tsx
import React from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'

import { ProtectedRoute } from '@/components/ProtectedRoute'
import { DashboardPage } from '@/pages/DashboardPage'
import { ForgotPasswordPage } from '@/pages/ForgotPasswordPage'
import { LoginPage } from '@/pages/LoginPage'
import { ResetPasswordPage } from '@/pages/ResetPasswordPage'
import { ProfilePage } from '@/pages/ProfilePage'
import { ManagerStreamPage } from '@/pages/ManagerStreamPage'
import { ManagerStreamsPage } from '@/pages/ManagerStreamsPage'
import { OperatorEventPage } from '@/pages/OperatorEventPage'
import { OperatorHomePage } from '@/pages/OperatorHomePage'
import { RoleHome } from '@/pages/RoleHome'
import { FirstLoginPasswordPage } from '@/pages/FirstLoginPasswordPage'
import { OnboardingPage } from '@/pages/OnboardingPage'
import { SuperadminPage } from '@/pages/SuperadminPage'

export const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />
      <Route
        path="/first-login"
        element={
          <ProtectedRoute>
            <FirstLoginPasswordPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/onboarding"
        element={
          <ProtectedRoute>
            <OnboardingPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <RoleHome />
          </ProtectedRoute>
        }
      />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <ProfilePage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/operator"
        element={
          <ProtectedRoute roles={['OPERATOR', 'SUPERADMIN']}>
            <OperatorHomePage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/operator/:id"
        element={
          <ProtectedRoute roles={['OPERATOR', 'SUPERADMIN']}>
            <OperatorEventPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/manager"
        element={
          <ProtectedRoute roles={['STREAM_MANAGER', 'SUPERADMIN']}>
            <ManagerStreamsPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/manager/:id"
        element={
          <ProtectedRoute roles={['STREAM_MANAGER', 'SUPERADMIN']}>
            <ManagerStreamPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin"
        element={
          <ProtectedRoute roles={['SUPERADMIN']}>
            <SuperadminPage />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

```


---

## Исходный код: `frontend/src/api/client.ts`

> 378 строк, 11,303 байт

```ts
const API_BASE = import.meta.env.VITE_API_BASE ?? '/api/v1'

const ACCESS_KEY = 'access_token'

export const getAccessToken = (): string | null => localStorage.getItem(ACCESS_KEY)

export const setAccessToken = (token: string | null) => {
  if (!token) {
    localStorage.removeItem(ACCESS_KEY)
    return
  }
  localStorage.setItem(ACCESS_KEY, token)
}

type FetchOptions = RequestInit & { skipAuth?: boolean }

export const getOrCreateRequestId = (): string => {
  try {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
      return crypto.randomUUID()
    }
  } catch {
    /* ignore */
  }
  return `${Date.now()}-${Math.random().toString(36).slice(2, 11)}`
}

const buildHeaders = (init?: HeadersInit, token?: string | null): HeadersInit => {
  const h = new Headers(init ?? {})
  if (token) {
    h.set('Authorization', `Bearer ${token}`)
  }
  if (!h.has('X-Request-ID')) {
    h.set('X-Request-ID', getOrCreateRequestId())
  }
  if (!h.has('Content-Type') && init && 'body' in (init as object)) {
    /* empty */
  }
  return h
}

let refreshInFlight: Promise<boolean> | null = null

/** Обновляет access JWT по httpOnly refresh-cookie; дедупликация параллельных вызовов */
export const tryRefreshAccessToken = async (): Promise<boolean> => {
  if (refreshInFlight) {
    return refreshInFlight
  }
  refreshInFlight = (async () => {
    try {
      const res = await fetch(`${API_BASE}/auth/refresh`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-Request-ID': getOrCreateRequestId(),
        },
        body: '{}',
      })
      if (!res.ok) {
        return false
      }
      const data = (await res.json()) as { access_token?: string }
      if (!data.access_token) {
        return false
      }
      setAccessToken(data.access_token)
      return true
    } catch {
      return false
    }
  })().finally(() => {
    refreshInFlight = null
  })
  return refreshInFlight
}

const fetchWithAuthRetry = async (url: string, init: RequestInit): Promise<Response> => {
  const run = async () => {
    const token = getAccessToken()
    const h = new Headers(init.headers)
    if (!h.has('X-Request-ID')) {
      h.set('X-Request-ID', getOrCreateRequestId())
    }
    if (token) {
      h.set('Authorization', `Bearer ${token}`)
    }
    return fetch(url, { ...init, credentials: 'include', headers: h })
  }
  let res = await run()
  if (res.status === 401) {
    const ok = await tryRefreshAccessToken()
    if (ok) {
      res = await run()
    }
  }
  return res
}

/** Скачивание бинарного ответа с авторизацией (ZIP, файлы) */
export const fetchAuthorizedBlob = async (path: string): Promise<{ blob: Blob; filename: string }> => {
  const res = await fetchWithAuthRetry(`${API_BASE}${path}`, { method: 'GET' })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const errJson = (await res.json()) as { detail?: unknown }
      if (errJson?.detail) {
        detail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail)
      }
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  const blob = await res.blob()
  let filename = 'download'
  const cd = res.headers.get('Content-Disposition')
  if (cd) {
    const star = /filename\*=UTF-8''([^;\n]+)/i.exec(cd)
    const plain = /filename="([^"]+)"/i.exec(cd)
    if (star?.[1]) {
      filename = decodeURIComponent(star[1].trim())
    } else if (plain?.[1]) {
      filename = plain[1].trim()
    }
  }
  return { blob, filename }
}

export const triggerBlobDownload = (blob: Blob, filename: string) => {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.rel = 'noopener'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

export const uploadLogoRequest = async (file: File) => {
  const form = new FormData()
  form.append('file', file)
  const res = await fetchWithAuthRetry(`${API_BASE}/logos/upload`, {
    method: 'POST',
    body: form,
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const errJson = (await res.json()) as { detail?: unknown }
      if (errJson?.detail) {
        detail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail)
      }
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  return (await res.json()) as import('@/api/types').LogoLibraryItemOut
}

/** Несколько файлов за один запрос (медиатека логотипов) */
export const uploadLogosBatchRequest = async (files: File[]) => {
  if (!files.length) {
    throw new Error('Не выбраны файлы')
  }
  const form = new FormData()
  for (const f of files) {
    form.append('files', f)
  }
  const res = await fetchWithAuthRetry(`${API_BASE}/logos/upload-batch`, {
    method: 'POST',
    body: form,
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const errJson = (await res.json()) as { detail?: unknown }
      if (errJson?.detail) {
        detail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail)
      }
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  return (await res.json()) as import('@/api/types').LogoLibraryItemOut[]
}

export const apiFetch = async (path: string, options: FetchOptions = {}) => {
  const { skipAuth, headers, body, ...rest } = options
  const url = `${API_BASE}${path}`
  const pathOnly = path.split('?')[0]
  const allowRefreshOn401 = !skipAuth && pathOnly !== '/auth/login'
  const execute = async (): Promise<Response> => {
    const token = skipAuth ? null : getAccessToken()
    const merged = new Headers(buildHeaders(headers, token))
    if (body && typeof body === 'string' && !merged.has('Content-Type')) {
      merged.set('Content-Type', 'application/json')
    }
    return fetch(url, {
      ...rest,
      body,
      credentials: 'include',
      headers: merged,
    })
  }
  let res = await execute()
  if (res.status === 401 && allowRefreshOn401) {
    const refreshed = await tryRefreshAccessToken()
    if (refreshed) {
      res = await execute()
    }
  }
  if (!res.ok) {
    let detail = res.statusText
    try {
      const errJson = await res.json()
      if (errJson?.detail) {
        detail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail)
      }
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  if (res.status === 204) {
    return null
  }
  const ct = res.headers.get('content-type')
  if (ct?.includes('application/json')) {
    return res.json()
  }
  return res.blob()
}

export const loginRequest = async (email: string, password: string) => {
  const data = (await apiFetch('/auth/login', {
    method: 'POST',
    skipAuth: true,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })) as { access_token: string; user: import('@/api/types').UserOut }
  setAccessToken(data.access_token)
  return data
}

export const forgotPasswordRequest = async (email: string) => {
  return (await apiFetch('/auth/forgot-password', {
    method: 'POST',
    skipAuth: true,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  })) as { message: string }
}

export const validatePasswordResetTokenRequest = async (token: string) => {
  const q = new URLSearchParams({ token })
  return (await apiFetch(`/auth/password-reset/validate?${q.toString()}`, {
    skipAuth: true,
  })) as { ok: boolean }
}

export const resetPasswordRequest = async (payload: {
  token: string
  new_password: string
  new_password_confirm: string
}) => {
  await apiFetch('/auth/reset-password', {
    method: 'POST',
    skipAuth: true,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export const logoutRequest = async () => {
  await apiFetch('/auth/logout', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })
  setAccessToken(null)
}

export const meRequest = async () => {
  return (await apiFetch('/auth/me')) as { user: import('@/api/types').UserOut }
}

export const getDashboardSummary = async () => {
  return (await apiFetch('/dashboard')) as import('@/api/types').DashboardSummaryOut
}

export const patchProfileRequest = async (body: {
  first_name?: string
  last_name?: string
  phone?: string
  telegram?: string
  onboarding_completed?: boolean
  /** только false — отклонить подсказку смены пароля */
  suggest_password_change?: boolean
}) => {
  return (await apiFetch('/profile', {
    method: 'PATCH',
    body: JSON.stringify(body),
  })) as import('@/api/types').UserOut
}

export const uploadAvatarRequest = async (file: File) => {
  const form = new FormData()
  form.append('file', file)
  const res = await fetchWithAuthRetry(`${API_BASE}/profile/avatar`, {
    method: 'POST',
    body: form,
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const errJson = await res.json()
      if (errJson?.detail) {
        detail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail)
      }
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }
  return (await res.json()) as import('@/api/types').UserOut
}

export const getMyActivityPage = async (page: number, pageSize: number) => {
  const q = new URLSearchParams({ page: String(page), page_size: String(pageSize) })
  return (await apiFetch(`/profile/activity?${q.toString()}`)) as {
    items: import('@/api/types').AuditLogOut[]
    total: number
    page: number
    page_size: number
  }
}

export const changePasswordRequest = async (current_password: string, new_password: string) => {
  await apiFetch('/auth/change-password', {
    method: 'POST',
    body: JSON.stringify({ current_password, new_password }),
  })
}

export const listSessionsRequest = async () => {
  return (await apiFetch('/auth/sessions')) as import('@/api/types').SessionOut[]
}

export const revokeSessionRequest = async (sessionId: string) => {
  await apiFetch(`/auth/sessions/${sessionId}`, { method: 'DELETE' })
}

export const listEventTemplatesRequest = async () => {
  return (await apiFetch('/stream-event-templates')) as import('@/api/types').StreamEventTemplateOut[]
}

export const deleteEventTemplateRequest = async (id: string) => {
  await apiFetch(`/stream-event-templates/${id}`, { method: 'DELETE' })
}

export const instantiateTemplateRequest = async (
  templateId: string,
  body: { title: string; start_date: string; duration_days: number },
) => {
  return (await apiFetch(`/stream-event-templates/${templateId}/instantiate`, {
    method: 'POST',
    body: JSON.stringify(body),
  })) as import('@/api/types').StreamEventDetailOut
}

export const createTemplateFromEventRequest = async (streamId: string, name: string) => {
  return (await apiFetch(`/stream-event-templates/from-event/${streamId}`, {
    method: 'POST',
    body: JSON.stringify({ name }),
  })) as import('@/api/types').StreamEventTemplateOut
}

```


---

## Исходный код: `frontend/src/api/generated/README.md`

> 8 строк, 309 байт

```md
Сгенерированные типы OpenAPI: выполните из каталога `frontend` при запущенном backend:

```bash
npm run codegen:api
```

Файл `schema.ts` создаётся автоматически (при необходимости добавьте в `.gitignore`).

```


---

## Исходный код: `frontend/src/api/types.ts`

> 197 строк, 4,968 байт

```ts
export type UserRole = 'SUPERADMIN' | 'STREAM_MANAGER' | 'OPERATOR'

export type UserOut = {
  id: string
  email: string
  first_name: string
  last_name: string
  /** «Фамилия Имя», для обращения в интерфейсе */
  display_name?: string
  phone?: string | null
  telegram?: string | null
  avatar_url?: string | null
  role: UserRole
  is_active: boolean
  /** Рекомендация сменить пароль после входа с временным паролем */
  suggest_password_change?: boolean
  /** false — показать интерактивное знакомство при первом входе */
  onboarding_completed?: boolean
  /** Последний вход по паролю / accept-invite (UTC с бэкенда) */
  last_login_at?: string | null
  last_login_ip?: string | null
  created_at: string
}

export type UserCreatedOut = {
  user: UserOut
  welcome_email_queued: boolean
  welcome_email_skipped_reason: string | null
}

export type DashboardSummaryOut = {
  role: string
  title: string
  cards: { key: string; title: string; value: string | number; hint: string }[]
}

export type SessionOut = {
  id: string
  created_at: string
  expires_at: string
  user_agent: string | null
  is_current: boolean
}

export type StreamEventTemplateOut = {
  id: string
  name: string
  title: string
  duration_days: number
  created_at: string
}

export type DayAssignmentOut = {
  day_index: number
  operator_id: string
  operator_display_name: string
  operator_email: string
}

export type StreamDayLinkOut = {
  day_index: number
  stream_url: string
}

export type StreamEventListOut = {
  id: string
  title: string
  start_date: string
  duration_days: number
  locked_by_user_id: string | null
  /** Устар.: один оператор; при нескольких — assignment_summary */
  locked_by_display_name: string | null
  assignment_summary: string | null
  has_slot_for_me: boolean
  has_active_broadcast: boolean
  has_ended_broadcast?: boolean
  ended_day_indices?: number[]
  created_at: string
  /** Ссылки на трансляцию по дням (список мероприятий) */
  day_stream_links?: StreamDayLinkOut[]
}

export type StreamDayOut = {
  id: string
  day_index: number
  stream_url: string
  server_url: string
  stream_key: string
}

export type BroadcastSessionOut = {
  id: string
  stream_event_id: string
  day_index: number
  operator_id: string
  started_at: string
  ended_at: string | null
  is_active: boolean
  mentions_count?: number | null
}

export type BroadcastChecklistOut = {
  stream_event_id: string
  day_index: number
  picture_exposure_ok: boolean
  judges_stream_ok: boolean
  splitter_socket_ok: boolean
  key_stream_started_ok: boolean
  kick_ok: boolean
  mentions_four_ok: boolean
  updated_at: string
}

export type StreamLogoItemOut = {
  id: string
  filename_original: string
  public_url: string
  sort_order: number
  created_at: string
}

export type LogoLibraryItemOut = {
  id: string
  filename_original: string
  public_url: string
  created_at: string
  uploaded_by_id: string | null
}

export type StreamEventDetailOut = {
  id: string
  title: string
  start_date: string
  duration_days: number
  locked_by_user_id: string | null
  locked_by_display_name: string | null
  day_assignments: DayAssignmentOut[]
  days: StreamDayOut[]
  active_broadcasts: BroadcastSessionOut[]
  ended_broadcasts?: BroadcastSessionOut[]
  /** Дни без повторного старта после длинного эфира с таймкодами */
  broadcast_restart_blocked_days?: number[]
  /** С бэкенда v2+; при старых ответах может отсутствовать */
  content_url?: string | null
  logos?: StreamLogoItemOut[]
  created_at: string
  updated_at: string
}

export type SponsorMentionOut = {
  id: string
  broadcast_session_id: string
  original_offset_sec: number
  adjusted_offset_sec: number
  original_timecode: string
  adjusted_timecode: string
  absolute_moscow_original: string
  absolute_moscow_adjusted: string
  is_adjusted: boolean
  created_at: string
  adjustments: {
    id: string
    editor_user_id: string
    previous_adjusted_sec: number
    new_adjusted_sec: number
    created_at: string
  }[]
}

export type AuditLogOut = {
  id: string
  user_id: string | null
  action_type: string
  entity_type: string
  entity_id: string | null
  payload_before: Record<string, unknown> | null
  payload_after: Record<string, unknown> | null
  created_at: string
}

export type ReportMentionsOut = {
  items: {
    mention_id: string
    stream_event_id: string
    stream_title: string
    event_day_date: string
    day_index: number
    broadcast_session_id: string
    original_timecode: string
    adjusted_timecode: string
    absolute_moscow_adjusted: string
    is_adjusted: boolean
    mention_created_at: string
  }[]
  total: number
}

```


---

## Исходный код: `frontend/src/auth/AuthContext.tsx`

> 81 строк, 2,038 байт

```tsx
import { message } from 'antd'
import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'

import type { UserOut } from '@/api/types'
import { getAccessToken, loginRequest, logoutRequest, meRequest, setAccessToken } from '@/api/client'
import { userDisplayName } from '@/utils/userDisplay'

type AuthState = {
  user: UserOut | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  refreshMe: () => Promise<void>
}

const AuthContext = createContext<AuthState | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserOut | null>(null)
  const [loading, setLoading] = useState(true)

  const refreshMe = useCallback(async () => {
    const token = getAccessToken()
    if (!token) {
      setUser(null)
      setLoading(false)
      return
    }
    try {
      const data = await meRequest()
      setUser(data.user)
    } catch {
      setAccessToken(null)
      setUser(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void refreshMe()
  }, [refreshMe])

  const login = useCallback(async (email: string, password: string) => {
    const data = await loginRequest(email, password)
    setUser(data.user)
    message.success(`Здравствуйте, ${userDisplayName(data.user)}`)
  }, [])

  const logout = useCallback(async () => {
    try {
      await logoutRequest()
    } catch {
      setAccessToken(null)
    }
    setUser(null)
    message.info('Вы вышли')
  }, [])

  const value = useMemo(
    () => ({
      user,
      loading,
      login,
      logout,
      refreshMe,
    }),
    [user, loading, login, logout, refreshMe],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = (): AuthState => {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth вне AuthProvider')
  }
  return ctx
}

```


---

## Исходный код: `frontend/src/components/AnalyticsTracker.tsx`

> 34 строк, 922 байт

```tsx
import { useEffect, useRef } from 'react'
import { useLocation } from 'react-router-dom'

import { useAuth } from '@/auth/AuthContext'
import { apiFetch } from '@/api/client'

/** Лёгкая продуктовая аналитика: записи page_view на смене маршрута. */
export const AnalyticsTracker = () => {
  const loc = useLocation()
  const { user } = useAuth()
  const lastPath = useRef<string | null>(null)

  useEffect(() => {
    if (!user || loc.pathname === '/login') {
      return
    }
    if (lastPath.current === loc.pathname) {
      return
    }
    lastPath.current = loc.pathname
    void apiFetch('/analytics/events', {
      method: 'POST',
      body: JSON.stringify({
        event_name: 'page_view',
        meta: { path: loc.pathname },
      }),
    }).catch(() => {
      /* offline / 401 — не мешаем UX */
    })
  }, [loc.pathname, user])

  return null
}

```


---

## Исходный код: `frontend/src/components/BrandLogo.tsx`

> 32 строк, 828 байт

```tsx
import React from 'react'

/** Статика из `public/` — попадает в корень `dist` при сборке */
export const MAINSTREAM_LOGO_SRC = '/mainstream-logo.png'

type BrandLogoProps = {
  /** Высота логотипа, ширина подбирается автоматически */
  height?: number
  className?: string
  style?: React.CSSProperties
}

export const BrandLogo: React.FC<BrandLogoProps> = ({ height = 32, className, style }) => (
  <img
    className={className}
    src={MAINSTREAM_LOGO_SRC}
    alt="MainStream"
    height={height}
    decoding="async"
    draggable={false}
    style={{
      display: 'block',
      objectFit: 'contain',
      objectPosition: 'left center',
      width: 'auto',
      maxWidth: 'min(100%, 280px)',
      height,
      ...style,
    }}
  />
)

```


---

## Исходный код: `frontend/src/components/BroadcastActualStartPanel.tsx`

> 92 строк, 3,210 байт

```tsx
import { App as AntApp, Button, DatePicker, Space, Typography } from 'antd'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import React, { useEffect, useState } from 'react'

import { apiFetch } from '@/api/client'

dayjs.extend(utc)
dayjs.extend(timezone)

const toMoscowDayjs = (v: dayjs.Dayjs) =>
  dayjs.tz(v.format('YYYY-MM-DD HH:mm'), 'YYYY-MM-DD HH:mm', 'Europe/Moscow')

type BroadcastActualStartPanelProps = {
  streamId: string
  dayIndex: number
  startedAtIso: string
  disabled?: boolean
}

export const BroadcastActualStartPanel: React.FC<BroadcastActualStartPanelProps> = ({
  streamId,
  dayIndex,
  startedAtIso,
  disabled,
}) => {
  const { message } = AntApp.useApp()
  const qc = useQueryClient()
  const [pick, setPick] = useState(() => dayjs.utc(startedAtIso).tz('Europe/Moscow'))

  useEffect(() => {
    setPick(dayjs.utc(startedAtIso).tz('Europe/Moscow'))
  }, [startedAtIso])

  const mut = useMutation({
    mutationFn: async (value: dayjs.Dayjs) => {
      const msk = toMoscowDayjs(value)
      const iso = msk.utc().toISOString()
      await apiFetch(`/stream-events/${streamId}/days/${dayIndex}/broadcast/actual-start`, {
        method: 'POST',
        body: JSON.stringify({ actual_started_at: iso }),
      })
    },
    onSuccess: async () => {
      message.success('Время начала эфира обновлено, таймкоды сдвинуты')
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
      await qc.invalidateQueries({ queryKey: ['mentions', streamId, dayIndex] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  return (
    <div
      style={{
        padding: 12,
        borderRadius: 10,
        border: '1px solid #fde68a',
        background: '#fffbeb',
      }}
    >
      <Typography.Text strong style={{ display: 'block', marginBottom: 8 }}>
        Фактическое начало эфира (МСК)
      </Typography.Text>
      <Typography.Paragraph type="secondary" style={{ fontSize: 12, marginBottom: 10 }}>
        Если нажали «Начать эфир» позже, чем реально пошла картинка (например в 18:13 вместо 18:00), укажите время,
        когда эфир реально начался. Все таймкоды упоминаний и абсолютные времена сдвинутся; расстояния между отметками
        не изменятся.
      </Typography.Paragraph>
      <Space wrap style={{ width: '100%' }} align="center">
        <DatePicker
          showTime
          format="DD.MM.YYYY HH:mm"
          minuteStep={1}
          value={pick}
          onChange={(v) => {
            if (v) {
              setPick(toMoscowDayjs(v))
            }
          }}
          disabled={disabled || mut.isPending}
          style={{ minWidth: 240 }}
        />
        <Button type="primary" loading={mut.isPending} disabled={disabled} onClick={() => mut.mutate(pick)}>
          Применить
        </Button>
      </Space>
    </div>
  )
}

```


---

## Исходный код: `frontend/src/components/NotificationBell.tsx`

> 107 строк, 3,330 байт

```tsx
import { BellOutlined } from '@ant-design/icons'
import { Badge, Button, Dropdown, List, Space, Typography } from 'antd'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import React from 'react'

import { apiFetch } from '@/api/client'
import { formatDateTimeRu } from '@/utils/datetime'

type NotificationItem = {
  id: string
  title: string
  body: string
  kind: string | null
  is_read: boolean
  created_at: string
}

type NotificationResponse = {
  items: NotificationItem[]
  unread_count: number
}

export const NotificationBell: React.FC = () => {
  const qc = useQueryClient()
  const q = useQuery({
    queryKey: ['notifications'],
    queryFn: async () => (await apiFetch('/notifications')) as NotificationResponse,
    refetchInterval: 60_000,
  })

  const markRead = useMutation({
    mutationFn: async (id: string) => {
      await apiFetch(`/notifications/${id}/read`, { method: 'POST', body: '{}' })
    },
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ['notifications'] })
    },
  })

  const markAll = useMutation({
    mutationFn: async () => {
      await apiFetch('/notifications/read-all', { method: 'POST', body: '{}' })
    },
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ['notifications'] })
    },
  })

  const unread = q.data?.unread_count ?? 0
  const items = q.data?.items ?? []

  const dropdownContent = (
    <div style={{ width: 320, maxHeight: 360, overflow: 'auto', background: '#ffffff', padding: 8 }}>
      <Space style={{ width: '100%', justifyContent: 'space-between', marginBottom: 8 }}>
        <Typography.Text strong style={{ color: '#0f172a' }}>
          Уведомления
        </Typography.Text>
        {unread > 0 ? (
          <Typography.Link onClick={() => void markAll.mutate()} style={{ fontSize: 12 }}>
            Прочитать все
          </Typography.Link>
        ) : null}
      </Space>
      <List
        size="small"
        dataSource={items}
        locale={{ emptyText: 'Пока пусто' }}
        renderItem={(n) => (
          <List.Item
            style={{
              opacity: n.is_read ? 0.65 : 1,
              cursor: n.is_read ? 'default' : 'pointer',
            }}
            onClick={() => {
              if (!n.is_read) {
                void markRead.mutate(n.id)
              }
            }}
          >
            <div style={{ width: '100%' }}>
              <Typography.Text strong style={{ fontSize: 13, color: '#0f172a' }}>
                {n.title}
              </Typography.Text>
              <div>
                <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                  {n.body}
                </Typography.Text>
              </div>
              <Typography.Text type="secondary" style={{ fontSize: 11 }}>
                {formatDateTimeRu(n.created_at)}
              </Typography.Text>
            </div>
          </List.Item>
        )}
      />
    </div>
  )

  return (
    <Dropdown dropdownRender={() => dropdownContent} trigger={['click']} placement="bottomRight">
      <Badge count={unread} size="small" offset={[-2, 2]}>
        <Button type="text" icon={<BellOutlined />} aria-label="Уведомления" style={{ color: '#475569' }} />
      </Badge>
    </Dropdown>
  )
}

```


---

## Исходный код: `frontend/src/components/OperatorStatsPanel.tsx`

> 194 строк, 5,964 байт

```tsx
import { Card, DatePicker, Space, Table, Typography } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useQuery } from '@tanstack/react-query'
import dayjs from 'dayjs'
import React, { useState } from 'react'
import { Link } from 'react-router-dom'

import { apiFetch } from '@/api/client'

export type OperatorStatsOverview = {
  stat_date: string
  week_start: string
  week_end: string
  month_start: string
  month_end: string
  assignments: {
    stream_event_id: string
    title: string
    summary: string
  }[]
  operators: {
    operator_id: string
    email: string
    display_name: string
    role: string
    broadcasts_week: number
    mentions_week: number
    mentions_norm_week: number
    mentions_met_week: boolean
    broadcasts_month: number
    mentions_month: number
    mentions_norm_month: number
    mentions_met_month: boolean
  }[]
  total_broadcasts_week: number
  total_mentions_week: number
  total_broadcasts_month: number
  total_mentions_month: number
}

const roleRu = (r: string) => {
  const m: Record<string, string> = {
    OPERATOR: 'Оператор',
    STREAM_MANAGER: 'Менеджер',
    SUPERADMIN: 'Суперадмин',
  }
  return m[r] ?? r
}

const mentionCell = (v: number, met: boolean) => (
  <span
    style={{
      color: met ? '#52c41a' : '#ff7875',
      fontWeight: 600,
    }}
  >
    {v}
  </span>
)

export const OperatorStatsPanel: React.FC<{ compact?: boolean }> = ({ compact }) => {
  const [statDay, setStatDay] = useState(() => dayjs())

  const statsQuery = useQuery({
    queryKey: ['stats-operators', statDay.format('YYYY-MM-DD')],
    queryFn: async () =>
      (await apiFetch(`/stats/operators?stat_date=${statDay.format('YYYY-MM-DD')}`)) as OperatorStatsOverview,
  })

  const data = statsQuery.data

  const opColumns: ColumnsType<OperatorStatsOverview['operators'][0]> = [
    {
      title: 'Оператор',
      key: 'op',
      ellipsis: true,
      render: (_, r) => (
        <div>
          <div>{r.display_name || r.email}</div>
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            {r.email}
          </Typography.Text>
        </div>
      ),
    },
    {
      title: 'Роль',
      dataIndex: 'role',
      key: 'role',
      width: 140,
      render: (r: string) => roleRu(r),
    },
    {
      title: 'Эфиров за неделю',
      dataIndex: 'broadcasts_week',
      key: 'bw',
      width: 130,
      align: 'center',
    },
    {
      title: 'Упоминаний (нед.)',
      key: 'mw',
      width: 150,
      align: 'center',
      render: (_, r) => mentionCell(r.mentions_week, r.mentions_met_week),
    },
    {
      title: 'Эфиров за месяц',
      dataIndex: 'broadcasts_month',
      key: 'bm',
      width: 130,
      align: 'center',
    },
    {
      title: 'Упоминаний (мес.)',
      key: 'mm',
      width: 150,
      align: 'center',
      render: (_, r) => mentionCell(r.mentions_month, r.mentions_met_month),
    },
  ]

  const assignColumns: ColumnsType<OperatorStatsOverview['assignments'][0]> = [
    {
      title: 'Мероприятие',
      dataIndex: 'title',
      key: 'title',
      ellipsis: true,
      render: (t: string, r) => (
        <Link to={`/manager/${r.stream_event_id}`} style={{ color: '#0284c7' }}>
          {t}
        </Link>
      ),
    },
    {
      title: 'Операторы по дням',
      dataIndex: 'summary',
      key: 'summary',
      ellipsis: true,
    },
  ]

  return (
    <Space direction="vertical" size={16} style={{ width: '100%' }}>
      <Space wrap align="center">
        <Typography.Text type="secondary">Опорная дата (МСК, для границ недели и месяца):</Typography.Text>
        <DatePicker value={statDay} onChange={(d) => d && setStatDay(d)} format="DD.MM.YYYY" allowClear={false} />
      </Space>
      {data ? (
        <Space direction="vertical" size={12} style={{ width: '100%' }}>
          <Typography.Text type="secondary">
            Неделя {dayjs(data.week_start).format('DD.MM')} — {dayjs(data.week_end).format('DD.MM.YYYY')}: эфиров{' '}
            {data.total_broadcasts_week}, упоминаний {data.total_mentions_week}. Месяц{' '}
            {dayjs(data.month_start).format('MM.YYYY')}: эфиров {data.total_broadcasts_month}, упоминаний{' '}
            {data.total_mentions_month}. Норма упоминаний: 4 на каждый эфир — зелёный цвет, если выполнено.
          </Typography.Text>
          <Card
            size={compact ? 'small' : 'default'}
            title="Кто на каких мероприятиях (по дням)"
            style={{ borderColor: '#e2e8f0', background: '#ffffff' }}
          >
            <Table
              rowKey="stream_event_id"
              size="small"
              loading={statsQuery.isLoading}
              dataSource={data.assignments}
              columns={assignColumns}
              pagination={false}
              locale={{ emptyText: 'Нет назначений по дням' }}
            />
          </Card>
          <Card
            size={compact ? 'small' : 'default'}
            title="Операторы: эфиры и упоминания (неделя и месяц)"
            style={{ borderColor: '#e2e8f0', background: '#ffffff' }}
          >
            <Table
              rowKey="operator_id"
              size="small"
              dataSource={data.operators}
              columns={opColumns}
              pagination={false}
              locale={{ emptyText: 'Нет операторов' }}
              scroll={{ x: 900 }}
            />
          </Card>
        </Space>
      ) : (
        <Typography.Text type="secondary">{statsQuery.isLoading ? 'Загрузка…' : 'Нет данных'}</Typography.Text>
      )}
    </Space>
  )
}

```


---

## Исходный код: `frontend/src/components/ProtectedRoute.tsx`

> 48 строк, 1,254 байт

```tsx
import { Spin } from 'antd'
import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'

import type { UserRole } from '@/api/types'
import { useAuth } from '@/auth/AuthContext'

type Props = {
  children: React.ReactNode
  roles?: UserRole[]
}

export const ProtectedRoute: React.FC<Props> = ({ children, roles }) => {
  const { user, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div style={{ display: 'grid', placeItems: 'center', minHeight: '60vh' }}>
        <Spin size="large" />
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (location.pathname === '/first-login' && !user.suggest_password_change) {
    return <Navigate to={user.onboarding_completed ? '/dashboard' : '/onboarding'} replace />
  }

  if (!user.onboarding_completed) {
    if (user.suggest_password_change && location.pathname !== '/first-login') {
      return <Navigate to="/first-login" replace />
    }
    if (!user.suggest_password_change && location.pathname !== '/onboarding') {
      return <Navigate to="/onboarding" replace />
    }
  }

  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/" replace />
  }

  return <>{children}</>
}

```


---

## Исходный код: `frontend/src/components/SuggestPasswordModal.tsx`

> 59 строк, 1,765 байт

```tsx
import { Button, Modal, Typography } from 'antd'
import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { useAuth } from '@/auth/AuthContext'

const dismissKey = (userId: string) => `streaming_ops_suggest_pwd_dismiss_${userId}`

export const SuggestPasswordModal: React.FC = () => {
  const { user } = useAuth()
  const nav = useNavigate()
  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (!user?.suggest_password_change || !user?.onboarding_completed) {
      setOpen(false)
      return
    }
    if (typeof localStorage !== 'undefined' && localStorage.getItem(dismissKey(user.id))) {
      setOpen(false)
      return
    }
    setOpen(true)
  }, [user?.id, user?.suggest_password_change, user?.onboarding_completed])

  const handleLater = () => {
    if (user) {
      localStorage.setItem(dismissKey(user.id), '1')
    }
    setOpen(false)
  }

  const handleGoProfile = () => {
    setOpen(false)
    nav('/profile')
  }

  return (
    <Modal
      title="Рекомендуем сменить пароль"
      open={open}
      onCancel={handleLater}
      footer={[
        <Button key="later" onClick={handleLater}>
          Позже
        </Button>,
        <Button key="go" type="primary" onClick={handleGoProfile}>
          Открыть профиль
        </Button>,
      ]}
    >
      <Typography.Paragraph style={{ marginBottom: 0 }}>
        Вы вошли с временным или начальным паролем. Для безопасности лучше задать свой пароль в разделе «Профиль» —
        смена по желанию, можно отложить.
      </Typography.Paragraph>
    </Modal>
  )
}

```


---

## Исходный код: `frontend/src/content/onboardingRoleGuides.tsx`

> 194 строк, 11,440 байт

```tsx
import { Typography } from 'antd'
import React from 'react'

import type { UserRole } from '@/api/types'

const listStyle: React.CSSProperties = {
  margin: '10px 0 0',
  paddingLeft: 22,
  color: '#334155',
  lineHeight: 1.7,
}

const subListStyle: React.CSSProperties = {
  margin: '6px 0 0',
  paddingLeft: 18,
  color: '#64748b',
  lineHeight: 1.6,
  fontSize: 13,
}

const Kbd: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <Typography.Text strong style={{ color: '#0284c7' }}>{children}</Typography.Text>
)

/** Детальное обучение под роль текущего пользователя (без тавтологии с «другими ролями»). */
export const PrimaryRoleTraining: React.FC<{ role: UserRole }> = ({ role }) => {
  if (role === 'OPERATOR') {
    return (
      <div>
        <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
          Ниже — порядок действий в интерфейсе: те же подписи кнопок, что в панели.
        </Typography.Paragraph>
        <ol style={listStyle}>
          <li>
            В шапке откройте раздел <Kbd>Оператор</Kbd> (маршрут <Typography.Text code>/operator</Typography.Text>) —
            список мероприятий, где вас назначили. Нажмите на строку турнира.
          </li>
          <li>
            Откроется <strong>Пульт оператора</strong>. Вверху — название мероприятия и длительность в днях.
          </li>
          <li>
            <strong>Статус и дни:</strong> если день свободен, нажмите <Kbd>Взять в работу</Kbd>, в модальном окне
            отметьте нужные дни и подтвердите. Тогда этот день закрепляется за вами. Кнопка{' '}
            <Kbd>Снять с работы</Kbd> снимает ваши назначения (когда нужно передать смену).
          </li>
          <li>
            Блок <strong>Чек-лист перед эфиром</strong> (для выбранного дня) — шесть пунктов перед стартом; у каждого дня свой
            набор галочек.
          </li>
          <li>
            В <strong>Управление эфиром</strong> выберите <Kbd>День</Kbd> в выпадающем списке. Раскройте{' '}
            <Kbd>Показать</Kbd> у «Параметры дня» — там ссылка на трансляцию, URL сервера и ключ. У каждого поля есть
            копирование (иконка «копировать» / подсказка «Скопировано») — вставьте в OBS или другой энкодер.
          </li>
          <li>
            Нажмите <Kbd>Начать эфир</Kbd> — фиксируется время старта, запускается <strong>таймер эфира</strong>. Без
            активного эфира кнопка <Kbd>Добавить упоминание</Kbd> недоступна.
          </li>
          <li>
            Во время эфира нажимайте <Kbd>Добавить упоминание</Kbd>, когда в эфире произошло спонсорское упоминание.
            Ориентируйтесь на план из четырёх слотов: «Начало эфира», две середины, «Конец эфира» — блок под кнопками
            показывает, какие шаги уже отмечены.
          </li>
          <li>
            Справа в списке <strong>Упоминания</strong> видны таймкоды и время (МСК). У записи нажмите{' '}
            <Kbd>Корректировка</Kbd> — в модалке задайте смещение от старта эфира (минуты и секунды 0–59) и{' '}
            <Kbd>Сохранить</Kbd>, если нужно поправить таймкод после эфира.
          </li>
          <li>
            По окончании дня нажмите <Kbd>Остановить эфир</Kbd> и подтвердите в диалоге. После остановки новые упоминания
            для этого дня до следующего старта создать нельзя.
          </li>
        </ol>
        <Typography.Paragraph type="secondary" style={{ marginTop: 14, marginBottom: 0, fontSize: 13 }}>
          Если день назначен другому оператору, пульт для него заблокирован — это видно по статусу над кнопками.
        </Typography.Paragraph>
      </div>
    )
  }

  if (role === 'STREAM_MANAGER') {
    return (
      <div>
        <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
          Как завести эфир и подготовить дни для операторов.
        </Typography.Paragraph>
        <ol style={listStyle}>
          <li>
            В шапке откройте раздел трансляций — <Kbd>Перейти к трансляциям</Kbd> (
            <Typography.Text code>/manager</Typography.Text>).
          </li>
          <li>
            Нажмите <Kbd>Новое мероприятие</Kbd>: укажите <strong>название</strong>, <strong>дату старта</strong> и{' '}
            <strong>длительность в днях</strong> (1–5), затем <Kbd>Создать</Kbd>.
          </li>
          <li>
            В таблице «Мероприятия» нажмите на строку или ссылку открытия — попадёте в <strong>карточку мероприятия</strong>{' '}
            (редактирование).
          </li>
          <li>
            В карточке заполните <strong>Название</strong>, <strong>дату старта</strong> и <strong>число дней</strong>.
            Ниже для каждого <strong>Дня 1…N</strong> введите: ссылку на трансляцию, URL сервера и ключ — их операторы
            увидят в пульте (с копированием). Нажмите <Kbd>Сохранить</Kbd>.
          </li>
          <li>
            Блок <strong>Упоминания оператора</strong> — тот же список отметок, что видит оператор во время эфира
            (удобно контролировать без входа в пульт).
          </li>
          <li>
            На странице менеджера доступны <strong>Шаблоны мероприятий</strong>: можно сохранить типовую структуру и кнопкой{' '}
            <Kbd>Создать мероприятие</Kbd> развернуть новый турнир из шаблона.
          </li>
          <li>
            Кнопка <Kbd>Экспорт отчёта</Kbd> открывает выгрузку упоминаний (Word, CSV, Excel) за период или по мероприятию —
            для отчётности спонсорам.
          </li>
        </ol>
        <Typography.Paragraph type="secondary" style={{ marginTop: 14, marginBottom: 0, fontSize: 13 }}>
          Назначение операторов на конкретные дни согласуется вне этой панели; в пульте оператор затем жмёт{' '}
          <Kbd>Взять в работу</Kbd> по свободным дням.
        </Typography.Paragraph>
      </div>
    )
  }

  return (
    <div>
      <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
        У вас доступ ко всем разделам панели: как у менеджера и оператора, плюс администрирование.
      </Typography.Paragraph>
      <ol style={listStyle}>
        <li>
          <Kbd>Перейти к трансляциям</Kbd> — создание мероприятий, дни, URL/ключи, шаблоны, экспорт отчётов (см. инструкцию для
          менеджера выше по смыслу).
        </li>
        <li>
          <Kbd>Оператор</Kbd> — пульт эфира: эфир, упоминания, корректировка таймкодов (см. инструкцию для оператора).
        </li>
        <li>
          В пульте оператора суперадмин может работать с любыми днями без ограничения «взять день».
        </li>
        <li>
          Раздел <Kbd>Администрирование</Kbd> (<Typography.Text code>/admin</Typography.Text>) — пользователи, аудит,
          продуктовая аналитика.
        </li>
      </ol>
      <ul style={subListStyle}>
        <li>Создание учётных записей и приветственные письма с временным паролем.</li>
        <li>Журнал действий и сводки по действиям в интерфейсе (аналитика).</li>
      </ul>
    </div>
  )
}

/** Кратко о других ролях — одна строка, без повторения текста «вашей» роли. */
export const OtherRolesHint: React.FC<{ currentRole: UserRole }> = ({ currentRole }) => {
  const items: { key: string; title: string; body: string }[] = []
  if (currentRole !== 'OPERATOR') {
    items.push({
      key: 'op',
      title: 'Оператор',
      body:
        'Пульт эфира: взять день, чек-лист, копирование ссылок/ключа, Начать/Остановить эфир, Добавить упоминание, Корректировка таймкода.',
    })
  }
  if (currentRole !== 'STREAM_MANAGER') {
    items.push({
      key: 'mgr',
      title: 'Менеджер',
      body:
        'Создание мероприятий и дней, заполнение URL/ключей, шаблоны, экспорт отчётов, просмотр упоминаний в карточке мероприятия.',
    })
  }
  if (currentRole !== 'SUPERADMIN') {
    items.push({
      key: 'adm',
      title: 'Суперадминистратор',
      body: 'Пользователи, аудит, аналитика, полный доступ к мероприятиям и пульту.',
    })
  }
  if (items.length === 0) {
    return null
  }
  return (
    <>
      {items.map((it) => (
        <Typography.Paragraph key={it.key} type="secondary" style={{ marginBottom: 10 }}>
          <Typography.Text strong style={{ color: '#0f172a' }}>{it.title}:</Typography.Text> {it.body}
        </Typography.Paragraph>
      ))}
    </>
  )
}

```


---

## Исходный код: `frontend/src/hooks/useStreamWs.ts`

> 47 строк, 1,168 байт

```ts
import { useEffect, useRef } from 'react'

import { getAccessToken } from '@/api/client'

const apiBase = import.meta.env.VITE_API_BASE ?? '/api/v1'

export const useStreamWs = (
  streamId: string | undefined,
  onEvent: (msg: Record<string, unknown>) => void,
  enabled = true,
) => {
  const cb = useRef(onEvent)
  cb.current = onEvent

  useEffect(() => {
    if (!streamId || !enabled) {
      return
    }
    const token = getAccessToken()
    if (!token) {
      return
    }
    const proto = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const url = `${proto}://${window.location.host}${apiBase}/ws/stream-events/${streamId}`
    const ws = new WebSocket(url)
    ws.onopen = () => {
      const t = getAccessToken()
      if (!t || ws.readyState !== WebSocket.OPEN) {
        ws.close()
        return
      }
      ws.send(JSON.stringify({ type: 'auth', access_token: t }))
    }
    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data as string) as Record<string, unknown>
        cb.current(data)
      } catch {
        /* ignore */
      }
    }
    return () => {
      ws.close()
    }
  }, [streamId, enabled])
}

```


---

## Исходный код: `frontend/src/layouts/AppLayout.tsx`

> 179 строк, 6,357 байт

```tsx
import { LogoutOutlined } from '@ant-design/icons'
import { Button, Grid, Layout, Space, Tooltip, Typography } from 'antd'
import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { BrandLogo } from '@/components/BrandLogo'
import { NotificationBell } from '@/components/NotificationBell'
import { SuggestPasswordModal } from '@/components/SuggestPasswordModal'
import { useAuth } from '@/auth/AuthContext'
import { userDisplayName } from '@/utils/userDisplay'

const { Header, Content, Footer } = Layout

export const AppLayout: React.FC<{ children: React.ReactNode; nav?: React.ReactNode }> = ({
  children,
  nav,
}) => {
  const { user, logout } = useAuth()
  const navHook = useNavigate()
  const screens = Grid.useBreakpoint()
  const isNarrow = !screens.md

  const handleLogout = async () => {
    await logout()
    navHook('/login')
  }

  const headerPad = isNarrow ? 12 : 20
  const safePad = {
    paddingLeft: `max(${headerPad}px, env(safe-area-inset-left, 0px))`,
    paddingRight: `max(${headerPad}px, env(safe-area-inset-right, 0px))`,
  }

  return (
    <Layout style={{ minHeight: '100%', background: '#f5f7fa', display: 'flex', flexDirection: 'column' }}>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: isNarrow ? 'wrap' : 'nowrap',
          gap: isNarrow ? 8 : 16,
          background: '#ffffff',
          boxShadow: '0 1px 0 rgba(15, 23, 42, 0.06)',
          borderBottom: '1px solid #e2e8f0',
          ...safePad,
          height: 'auto',
          minHeight: 64,
          lineHeight: isNarrow ? '1.35' : '64px',
          paddingBlock: isNarrow ? 10 : 0,
        }}
      >
        <Space
          size={isNarrow ? 'small' : 'large'}
          align="start"
          wrap
          style={{ flex: isNarrow ? '1 1 100%' : undefined, minWidth: 0 }}
        >
          <Link
            to="/dashboard"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: isNarrow ? 8 : 12,
              color: '#0f172a',
              fontWeight: 600,
              fontSize: isNarrow ? 15 : undefined,
              textDecoration: 'none',
            }}
            aria-label="MainStream — дашборд"
          >
            <BrandLogo height={isNarrow ? 22 : 30} />
            <span style={{ whiteSpace: 'nowrap' }}>Ops</span>
          </Link>
          <Link to="/dashboard" style={{ color: '#475569', fontSize: isNarrow ? 14 : 13 }}>
            Дашборд
          </Link>
          <Link to="/profile" style={{ color: '#475569', fontSize: isNarrow ? 14 : 13 }}>
            Профиль
          </Link>
          {user?.role === 'SUPERADMIN' ? (
            <Space size="small" wrap>
              <Link to="/admin" style={{ color: '#475569', fontSize: isNarrow ? 14 : 13 }}>
                Админ
              </Link>
              <Link to="/manager" style={{ color: '#475569', fontSize: isNarrow ? 14 : 13 }}>
                Менеджер
              </Link>
              <Link to="/operator" style={{ color: '#475569', fontSize: isNarrow ? 14 : 13 }}>
                Оператор
              </Link>
            </Space>
          ) : null}
          {nav ? (
            <div style={{ width: isNarrow ? '100%' : 'auto' }}>{nav}</div>
          ) : null}
        </Space>
        <Space
          align="center"
          wrap
          size="small"
          style={{
            flexShrink: 0,
            marginLeft: isNarrow ? 'auto' : undefined,
          }}
        >
          {!isNarrow ? (
            <>
              <div style={{ textAlign: 'right' as const }}>
                <Typography.Text strong style={{ display: 'block', maxWidth: 260 }} ellipsis>
                  {user ? userDisplayName(user) : ''}
                </Typography.Text>
                <Typography.Text type="secondary" ellipsis style={{ fontSize: 12, display: 'block', maxWidth: 260 }}>
                  {user?.email}
                </Typography.Text>
                <Typography.Text type="secondary" style={{ fontSize: 11 }}>
                  {user?.role === 'SUPERADMIN'
                    ? 'Суперадмин'
                    : user?.role === 'STREAM_MANAGER'
                      ? 'Менеджер'
                      : user?.role === 'OPERATOR'
                        ? 'Оператор'
                        : user?.role}
                </Typography.Text>
              </div>
            </>
          ) : (
            <Tooltip title={`${user ? userDisplayName(user) : ''} · ${user?.email ?? ''}`}>
              <Typography.Text strong ellipsis style={{ maxWidth: 100, fontSize: 12, display: 'block' }}>
                {user ? userDisplayName(user) : ''}
              </Typography.Text>
            </Tooltip>
          )}
          {user ? <NotificationBell /> : null}
          <Tooltip title="Выйти">
            <Button
              type="default"
              icon={<LogoutOutlined />}
              onClick={() => void handleLogout()}
              aria-label="Выйти из аккаунта"
            >
              {!isNarrow ? 'Выйти' : null}
            </Button>
          </Tooltip>
        </Space>
      </Header>
      <Content
        style={{
          flex: 1,
          padding: isNarrow ? 12 : 20,
          paddingBottom: `max(${isNarrow ? 12 : 20}px, env(safe-area-inset-bottom, 0px))`,
        }}
      >
        {children}
      </Content>
      <Footer
        style={{
          marginTop: 'auto',
          padding: isNarrow ? '14px 12px' : '16px 20px',
          paddingBottom: `max(${isNarrow ? 14 : 16}px, env(safe-area-inset-bottom, 0px))`,
          background: 'transparent',
          borderTop: '1px solid #e2e8f0',
          textAlign: 'center',
        }}
      >
        <Space direction="vertical" size={6} style={{ width: '100%' }}>
          <div style={{ display: 'flex', justifyContent: 'center', opacity: 0.9 }}>
            <BrandLogo height={18} />
          </div>
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            Панель эфиров · Москва
          </Typography.Text>
        </Space>
      </Footer>
      <SuggestPasswordModal />
    </Layout>
  )
}

```


---

## Исходный код: `frontend/src/main.tsx`

> 50 строк, 1,424 байт

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ConfigProvider, App as AntApp } from 'antd'
import ruRU from 'antd/locale/ru_RU'
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'

import { AuthProvider } from '@/auth/AuthContext'
import { App } from '@/App'
import { AnalyticsTracker } from '@/components/AnalyticsTracker'
import { appTheme } from '@/theme'
import '@/styles/global.css'

if (import.meta.env.VITE_SENTRY_DSN) {
  void import('@sentry/react')
    .then((Sentry) => {
      Sentry.init({
        dsn: import.meta.env.VITE_SENTRY_DSN,
        environment: import.meta.env.MODE,
        tracesSampleRate: 0.15,
      })
    })
    .catch(() => {
      /* пакет не установлен — пропускаем */
    })
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, refetchOnWindowFocus: false },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ConfigProvider locale={ruRU} theme={appTheme}>
        <AntApp>
          <BrowserRouter>
            <AuthProvider>
              <AnalyticsTracker />
              <App />
            </AuthProvider>
          </BrowserRouter>
        </AntApp>
      </ConfigProvider>
    </QueryClientProvider>
  </React.StrictMode>,
)

```


---

## Исходный код: `frontend/src/pages/DashboardPage.tsx`

> 152 строк, 5,394 байт

```tsx
import {
  BarChartOutlined,
  CalendarOutlined,
  ControlOutlined,
  SettingOutlined,
  TeamOutlined,
} from '@ant-design/icons'
import { App as AntApp, Button, Card, Col, Row, Space, Statistic, Typography } from 'antd'
import { useQuery } from '@tanstack/react-query'
import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'

import { getDashboardSummary } from '@/api/client'
import { useAuth } from '@/auth/AuthContext'
import { AppLayout } from '@/layouts/AppLayout'
import { userDisplayName } from '@/utils/userDisplay'

const cardIcon = (key: string) => {
  if (key.includes('mention')) {
    return <BarChartOutlined style={{ fontSize: 22, opacity: 0.85 }} />
  }
  if (key.includes('stream') || key.includes('event')) {
    return <CalendarOutlined style={{ fontSize: 22, opacity: 0.85 }} />
  }
  if (key.includes('user')) {
    return <TeamOutlined style={{ fontSize: 22, opacity: 0.85 }} />
  }
  if (key.includes('audit')) {
    return <ControlOutlined style={{ fontSize: 22, opacity: 0.85 }} />
  }
  if (key.includes('notif')) {
    return <SettingOutlined style={{ fontSize: 22, opacity: 0.85 }} />
  }
  return <BarChartOutlined style={{ fontSize: 22, opacity: 0.85 }} />
}

export const DashboardPage: React.FC = () => {
  const { user } = useAuth()
  const { message } = AntApp.useApp()

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: getDashboardSummary,
  })

  useEffect(() => {
    if (isError && error) {
      message.error(error instanceof Error ? error.message : 'Ошибка загрузки')
    }
  }, [isError, error, message])

  const role = user?.role

  return (
    <AppLayout
      nav={
        <Typography.Text type="secondary" style={{ fontSize: 13 }}>
          Обзор
        </Typography.Text>
      }
    >
      <Space direction="vertical" size={20} style={{ width: '100%' }}>
        <div>
          <Typography.Title level={3} style={{ marginTop: 0, marginBottom: 4 }}>
            {data?.title ?? 'Панель'}
          </Typography.Title>
          <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
            {user ? userDisplayName(user) : ''} · краткая сводка по вашей роли и быстрые переходы.
          </Typography.Paragraph>
        </div>

        <Card
          loading={isLoading}
          style={{
            borderColor: '#e2e8f0',
            background: 'linear-gradient(145deg, #ffffff 0%, #f1f5f9 100%)',
            borderRadius: 12,
          }}
          styles={{ body: { padding: 20 } }}
        >
          <Typography.Text strong style={{ color: '#64748b', fontSize: 12, letterSpacing: 0.6 }}>
            ПОКАЗАТЕЛИ
          </Typography.Text>
          <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
            {(data?.cards ?? []).map((c) => (
              <Col xs={24} sm={12} lg={8} key={c.key}>
                <div
                  style={{
                    border: '1px solid #e2e8f0',
                    borderRadius: 10,
                    padding: 16,
                    background: 'rgba(241, 245, 249, 0.98)',
                    minHeight: 112,
                    display: 'flex',
                    gap: 14,
                    alignItems: 'flex-start',
                  }}
                >
                  <div style={{ color: '#0284c7', marginTop: 2 }}>{cardIcon(c.key)}</div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <Typography.Text type="secondary" style={{ fontSize: 12, display: 'block' }}>
                      {c.title}
                    </Typography.Text>
                    <Statistic
                      value={c.value}
                      valueStyle={{ color: '#0f172a', fontSize: 26, lineHeight: 1.2 }}
                    />
                    <Typography.Text type="secondary" style={{ fontSize: 11, display: 'block', marginTop: 6 }}>
                      {c.hint}
                    </Typography.Text>
                  </div>
                </div>
              </Col>
            ))}
          </Row>
        </Card>

        <Card
          title="Рабочие разделы"
          style={{ borderColor: '#e2e8f0', background: '#ffffff', borderRadius: 12 }}
          styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
        >
          <Space wrap size="middle">
            {role === 'OPERATOR' || role === 'SUPERADMIN' ? (
              <Link to="/operator">
                <Button type="primary" size="large">
                  Мероприятия оператора
                </Button>
              </Link>
            ) : null}
            {role === 'STREAM_MANAGER' || role === 'SUPERADMIN' ? (
              <Link to="/manager">
                <Button type="primary" size="large" ghost>
                  Перейти к трансляциям
                </Button>
              </Link>
            ) : null}
            {role === 'SUPERADMIN' ? (
              <Link to="/admin">
                <Button size="large">Администрирование</Button>
              </Link>
            ) : null}
            <Link to="/profile">
              <Button size="large">Профиль и безопасность</Button>
            </Link>
          </Space>
        </Card>
      </Space>
    </AppLayout>
  )
}

```


---

## Исходный код: `frontend/src/pages/FirstLoginPasswordPage.tsx`

> 116 строк, 4,633 байт

```tsx
import { SafetyOutlined } from '@ant-design/icons'
import { App as AntApp, Button, Card, Form, Input, Space, Typography } from 'antd'
import React from 'react'
import { useNavigate } from 'react-router-dom'

import { changePasswordRequest, patchProfileRequest } from '@/api/client'
import { useAuth } from '@/auth/AuthContext'
import { BrandLogo } from '@/components/BrandLogo'

export const FirstLoginPasswordPage: React.FC = () => {
  const { message } = AntApp.useApp()
  const { user, refreshMe } = useAuth()
  const nav = useNavigate()
  const [form] = Form.useForm()
  const [skipping, setSkipping] = React.useState(false)
  const [submitting, setSubmitting] = React.useState(false)

  if (!user) {
    return null
  }

  const handleSkip = async () => {
    setSkipping(true)
    try {
      await patchProfileRequest({ suggest_password_change: false })
      await refreshMe()
      message.info('Можно сменить пароль позже в разделе «Профиль»')
      nav('/onboarding', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Ошибка')
    } finally {
      setSkipping(false)
    }
  }

  const handleFinish = async (v: { current_password: string; new_password: string; new_password2: string }) => {
    setSubmitting(true)
    try {
      await changePasswordRequest(v.current_password, v.new_password)
      await refreshMe()
      message.success('Пароль обновлён — далее короткое знакомство с панелью')
      nav('/onboarding', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Ошибка')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div
      style={{
        minHeight: '100dvh',
        padding: 24,
        paddingTop: 'max(24px, env(safe-area-inset-top, 0px))',
        background:
          'radial-gradient(1200px 600px at 20% 0%, rgba(61,126,255,0.18), transparent), #f5f7fa',
      }}
    >
      <div style={{ maxWidth: 480, margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 20 }}>
          <BrandLogo height={36} />
        </div>

        <Card style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
          <Typography.Title
            level={4}
            style={{ marginTop: 0, color: '#0f172a', display: 'flex', alignItems: 'center', gap: 8 }}
          >
            <SafetyOutlined /> Первый вход: пароль
          </Typography.Title>
          <Typography.Paragraph type="secondary" style={{ marginBottom: 20 }}>
            В письме вам пришёл <strong>временный пароль</strong>. Рекомендуем задать свой — так безопаснее. Затем
            начнётся короткое знакомство с панелью.
          </Typography.Paragraph>

          <Form form={form} layout="vertical" onFinish={handleFinish}>
            <Form.Item name="current_password" label="Текущий пароль (из письма)" rules={[{ required: true }]}>
              <Input.Password autoComplete="current-password" size="large" />
            </Form.Item>
            <Form.Item name="new_password" label="Новый пароль" rules={[{ required: true, min: 8 }]}>
              <Input.Password autoComplete="new-password" size="large" />
            </Form.Item>
            <Form.Item
              name="new_password2"
              label="Повтор нового пароля"
              dependencies={['new_password']}
              rules={[
                { required: true },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('new_password') === value) {
                      return Promise.resolve()
                    }
                    return Promise.reject(new Error('Пароли не совпадают'))
                  },
                }),
              ]}
            >
              <Input.Password autoComplete="new-password" size="large" />
            </Form.Item>
            <Space wrap style={{ marginTop: 8 }}>
              <Button onClick={() => void handleSkip()} disabled={submitting} loading={skipping}>
                Сменить позже
              </Button>
              <Button type="primary" htmlType="submit" size="large" loading={submitting}>
                Сохранить и продолжить
              </Button>
            </Space>
          </Form>
        </Card>
      </div>
    </div>
  )
}

```


---

## Исходный код: `frontend/src/pages/ForgotPasswordPage.tsx`

> 89 строк, 3,492 байт

```tsx
import { MailOutlined } from '@ant-design/icons'
import { App as AntApp, Button, Card, Form, Input, Typography } from 'antd'
import React, { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'

import { useAuth } from '@/auth/AuthContext'
import { forgotPasswordRequest } from '@/api/client'
import { BrandLogo } from '@/components/BrandLogo'

export const ForgotPasswordPage: React.FC = () => {
  const { user } = useAuth()
  const nav = useNavigate()
  const { message } = AntApp.useApp()
  const [done, setDone] = useState(false)
  const [loading, setLoading] = useState(false)

  if (user) {
    return <Navigate to="/" replace />
  }

  const handleFinish = async (values: { email: string }) => {
    setLoading(true)
    try {
      const res = await forgotPasswordRequest(values.email.trim())
      message.success(res.message)
      setDone(true)
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Не удалось отправить запрос')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      style={{
        minHeight: '100dvh',
        display: 'grid',
        placeItems: 'center',
        padding: 24,
        paddingTop: 'max(24px, env(safe-area-inset-top, 0px))',
        paddingBottom: 'max(24px, env(safe-area-inset-bottom, 0px))',
        background: 'radial-gradient(1200px 600px at 20% 0%, rgba(61,126,255,0.18), transparent), #f5f7fa',
      }}
    >
      <Card
        style={{ width: 420, maxWidth: '100%', borderColor: '#e2e8f0', background: '#ffffff' }}
        bordered
      >
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 20 }}>
          <BrandLogo height={40} style={{ maxWidth: 'min(100%, 260px)' }} />
        </div>
        <Typography.Title level={3} style={{ marginTop: 0, color: '#0f172a', textAlign: 'center' }}>
          Забыли пароль?
        </Typography.Title>
        <Typography.Paragraph type="secondary" style={{ marginBottom: 24 }}>
          Укажите email учётной записи. Если он есть в системе, мы отправим ссылку для сброса пароля.
        </Typography.Paragraph>
        {done ? (
          <>
            <Typography.Paragraph>
              Проверьте почту (в том числе папку «Спам»). Ссылка для сброса активна 10 минут — откройте её сразу.
            </Typography.Paragraph>
            <Button type="primary" block size="large" onClick={() => nav('/login', { replace: true })}>
              Вернуться ко входу
            </Button>
          </>
        ) : (
          <Form layout="vertical" onFinish={handleFinish} requiredMark="optional">
            <Form.Item
              name="email"
              label="Email"
              rules={[{ required: true, type: 'email', message: 'Укажите email' }]}
            >
              <Input size="large" prefix={<MailOutlined />} placeholder="you@example.com" autoComplete="email" />
            </Form.Item>
            <Button type="primary" htmlType="submit" size="large" block loading={loading}>
              Отправить ссылку
            </Button>
            <div style={{ marginTop: 16, textAlign: 'center' }}>
              <Link to="/login">Назад ко входу</Link>
            </div>
          </Form>
        )}
      </Card>
    </div>
  )
}

```


---

## Исходный код: `frontend/src/pages/LoginPage.tsx`

> 79 строк, 2,912 байт

```tsx
import { LockOutlined, UserOutlined } from '@ant-design/icons'
import { App as AntApp, Button, Card, Form, Input, Typography } from 'antd'
import React from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'

import { BrandLogo } from '@/components/BrandLogo'
import { useAuth } from '@/auth/AuthContext'

export const LoginPage: React.FC = () => {
  const { user, login } = useAuth()
  const nav = useNavigate()
  const { message } = AntApp.useApp()

  if (user) {
    return <Navigate to="/" replace />
  }

  const handleFinish = async (values: { email: string; password: string }) => {
    try {
      await login(values.email, values.password)
      nav('/', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Ошибка входа')
    }
  }

  return (
    <div
      style={{
        minHeight: '100dvh',
        display: 'grid',
        placeItems: 'center',
        padding: 24,
        paddingTop: 'max(24px, env(safe-area-inset-top, 0px))',
        paddingBottom: 'max(24px, env(safe-area-inset-bottom, 0px))',
        background: 'radial-gradient(1200px 600px at 20% 0%, rgba(61,126,255,0.18), transparent), #f5f7fa',
      }}
    >
      <Card
        style={{ width: 420, maxWidth: '100%', borderColor: '#e2e8f0', background: '#ffffff' }}
        bordered
      >
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 20 }}>
          <BrandLogo height={40} style={{ maxWidth: 'min(100%, 260px)' }} />
        </div>
        <Typography.Title level={3} style={{ marginTop: 0, color: '#0f172a', textAlign: 'center' }}>
          Панель эфиров
        </Typography.Title>
        <Typography.Paragraph type="secondary" style={{ marginBottom: 24 }}>
          Войдите для продолжения.
        </Typography.Paragraph>
        <Form layout="vertical" onFinish={handleFinish} requiredMark="optional">
          <Form.Item
            name="email"
            label="Email"
            rules={[{ required: true, type: 'email', message: 'Укажите email' }]}
          >
            <Input size="large" prefix={<UserOutlined />} placeholder="you@fed.ru" autoComplete="username" />
          </Form.Item>
          <Form.Item name="password" label="Пароль" rules={[{ required: true, message: 'Введите пароль' }]}>
            <Input.Password
              size="large"
              prefix={<LockOutlined />}
              placeholder="••••••••"
              autoComplete="current-password"
            />
          </Form.Item>
          <Button type="primary" htmlType="submit" size="large" block>
            Войти
          </Button>
          <div style={{ marginTop: 16, textAlign: 'center' }}>
            <Link to="/forgot-password">Забыли пароль?</Link>
          </div>
        </Form>
      </Card>
    </div>
  )
}

```


---

## Исходный код: `frontend/src/pages/ManagerStreamPage.tsx`

> 702 строк, 26,726 байт

```tsx
import {
  ArrowLeftOutlined,
  CopyOutlined,
  DeleteOutlined,
  DownloadOutlined,
  FileZipOutlined,
  LinkOutlined,
  PlusOutlined,
  SaveOutlined,
} from '@ant-design/icons'
import {
  App as AntApp,
  Badge,
  Button,
  Card,
  Col,
  DatePicker,
  Form,
  Grid,
  Input,
  List,
  Modal,
  Row,
  Select,
  Space,
  Spin,
  Tabs,
  Typography,
  Upload,
} from 'antd'
import type { UploadFile } from 'antd/es/upload/interface'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import dayjs from 'dayjs'
import React, { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import type { LogoLibraryItemOut, SponsorMentionOut, StreamEventDetailOut } from '@/api/types'
import { apiFetch, fetchAuthorizedBlob, triggerBlobDownload, uploadLogosBatchRequest } from '@/api/client'
import { BroadcastActualStartPanel } from '@/components/BroadcastActualStartPanel'
import { useStreamWs } from '@/hooks/useStreamWs'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateTimeRu } from '@/utils/datetime'

const formatElapsed = (totalSec: number) => {
  const sec = Math.max(0, Math.floor(totalSec))
  const h = Math.floor(sec / 3600)
  const m = Math.floor((sec % 3600) / 60)
  const s = sec % 60
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

const LOGO_UPLOAD_MAX_FILES = 30
const LOGO_UPLOAD_MAX_BYTES = 15 * 1024 * 1024

export const ManagerStreamPage: React.FC = () => {
  const { id } = useParams()
  const streamId = id as string
  const screens = Grid.useBreakpoint()
  const isNarrow = !screens.sm
  const { message } = AntApp.useApp()
  const qc = useQueryClient()
  const [form] = Form.useForm()
  const [mentionDay, setMentionDay] = useState(1)
  const [addLogoOpen, setAddLogoOpen] = useState(false)
  const [logoModalUploadList, setLogoModalUploadList] = useState<UploadFile[]>([])
  const [logoBatchBusy, setLogoBatchBusy] = useState(false)

  const { data, isLoading } = useQuery({
    queryKey: ['stream', streamId],
    enabled: Boolean(streamId),
    queryFn: async () => (await apiFetch(`/stream-events/${streamId}`)) as StreamEventDetailOut,
  })

  useEffect(() => {
    if (!data) {
      return
    }
    const daysVals: Record<string, string> = {}
    for (const d of data.days) {
      daysVals[`day_${d.day_index}_stream_url`] = d.stream_url
      daysVals[`day_${d.day_index}_server_url`] = d.server_url
      daysVals[`day_${d.day_index}_stream_key`] = d.stream_key
    }
    form.setFieldsValue({
      title: data.title,
      start_date: dayjs(data.start_date),
      duration_days: data.duration_days,
      content_url: data.content_url ?? '',
      ...daysVals,
    })
  }, [data, form])

  useEffect(() => {
    if (!data) {
      return
    }
    if (mentionDay > data.duration_days) {
      setMentionDay(1)
    }
  }, [data, mentionDay])

  useEffect(() => {
    if (!addLogoOpen) {
      setLogoModalUploadList([])
      setLogoBatchBusy(false)
    }
  }, [addLogoOpen])

  const handleConfirmLogoUpload = async () => {
    const raw: File[] = []
    for (const f of logoModalUploadList) {
      if (f.originFileObj) {
        raw.push(f.originFileObj as File)
      }
    }
    if (!raw.length) {
      message.warning('Выберите файлы, затем нажмите «Загрузить к эфиру»')
      return
    }
    if (raw.length > LOGO_UPLOAD_MAX_FILES) {
      message.warning(`Не больше ${LOGO_UPLOAD_MAX_FILES} файлов за раз`)
      return
    }
    for (const f of raw) {
      if (f.size > LOGO_UPLOAD_MAX_BYTES) {
        message.error(`Файл «${f.name}» больше 15 МБ`)
        return
      }
    }
    setLogoBatchBusy(true)
    try {
      const items = await uploadLogosBatchRequest(raw)
      for (const item of items) {
        await apiFetch(`/stream-events/${streamId}/logos`, {
          method: 'POST',
          body: JSON.stringify({ logo_id: item.id }),
        })
      }
      message.success(`Добавлено файлов: ${items.length}`)
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
      await qc.invalidateQueries({ queryKey: ['logos-library'] })
      setLogoModalUploadList([])
      setAddLogoOpen(false)
    } catch (e) {
      message.error((e as Error).message)
    } finally {
      setLogoBatchBusy(false)
    }
  }

  const mentionsQuery = useQuery({
    queryKey: ['mentions', streamId, mentionDay],
    enabled: Boolean(streamId) && Boolean(data),
    queryFn: async () =>
      (await apiFetch(`/stream-events/${streamId}/days/${mentionDay}/mentions`)) as SponsorMentionOut[],
  })

  useStreamWs(
    streamId,
    () => {
      void qc.invalidateQueries({ queryKey: ['mentions', streamId] })
      void qc.invalidateQueries({ queryKey: ['stream', streamId] })
    },
    Boolean(data),
  )

  const logosLibraryQuery = useQuery({
    queryKey: ['logos-library'],
    enabled: addLogoOpen,
    queryFn: async () => (await apiFetch('/logos')) as LogoLibraryItemOut[],
  })

  const attachLogoMut = useMutation({
    mutationFn: async (logoId: string) => {
      await apiFetch(`/stream-events/${streamId}/logos`, {
        method: 'POST',
        body: JSON.stringify({ logo_id: logoId }),
      })
    },
    onSuccess: async () => {
      message.success('Логотип добавлен к мероприятию')
      setAddLogoOpen(false)
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
      await qc.invalidateQueries({ queryKey: ['logos-library'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const detachLogoMut = useMutation({
    mutationFn: async (logoId: string) => {
      await apiFetch(`/stream-events/${streamId}/logos/${logoId}`, { method: 'DELETE' })
    },
    onSuccess: async () => {
      message.success('Логотип откреплён')
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const downloadZipMut = useMutation({
    mutationFn: async () => {
      const { blob, filename } = await fetchAuthorizedBlob(`/stream-events/${streamId}/logos/archive.zip`)
      triggerBlobDownload(blob, filename)
    },
    onError: (e: Error) => message.error(e.message),
  })

  const downloadOneMut = useMutation({
    mutationFn: async (logoId: string) => {
      const { blob, filename } = await fetchAuthorizedBlob(`/stream-events/${streamId}/logos/${logoId}/file`)
      triggerBlobDownload(blob, filename)
    },
    onError: (e: Error) => message.error(e.message),
  })

  const saveMut = useMutation({
    mutationFn: async (values: Record<string, unknown>) => {
      const duration = Number(values.duration_days)
      const days = Array.from({ length: duration }, (_, i) => {
        const idx = i + 1
        return {
          day_index: idx,
          stream_url: String(values[`day_${idx}_stream_url`] ?? ''),
          server_url: String(values[`day_${idx}_server_url`] ?? ''),
          stream_key: String(values[`day_${idx}_stream_key`] ?? ''),
        }
      })
      const rawUrl = values.content_url
      const content_url =
        rawUrl == null || String(rawUrl).trim() === '' ? null : String(rawUrl).trim()
      await apiFetch(`/stream-events/${streamId}`, {
        method: 'PATCH',
        body: JSON.stringify({
          title: values.title,
          start_date: (values.start_date as dayjs.Dayjs).format('YYYY-MM-DD'),
          duration_days: duration,
          days,
          content_url,
        }),
      })
    },
    onSuccess: async () => {
      message.success('Сохранено')
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
      await qc.invalidateQueries({ queryKey: ['streams'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const handleCopyContentUrl = async () => {
    const v = form.getFieldValue('content_url') as string | undefined
    if (!v || !String(v).trim()) {
      message.warning('Ссылка пустая')
      return
    }
    await navigator.clipboard.writeText(String(v).trim())
    message.success('Скопировано')
  }

  const handleOpenContentUrl = () => {
    const v = form.getFieldValue('content_url') as string | undefined
    if (!v || !String(v).trim()) {
      message.warning('Ссылка пустая')
      return
    }
    window.open(String(v).trim(), '_blank', 'noopener,noreferrer')
  }

  const endedLatestPerDay = useMemo(() => {
    const list = data?.ended_broadcasts ?? []
    const seen = new Set<number>()
    const pick: typeof list = []
    for (const b of list) {
      if (seen.has(b.day_index)) {
        continue
      }
      seen.add(b.day_index)
      pick.push(b)
    }
    return pick.sort((a, b) => a.day_index - b.day_index)
  }, [data?.ended_broadcasts])

  return (
    <AppLayout
      nav={
        <Space>
          <Link to="/manager">
            <Button type="link" icon={<ArrowLeftOutlined />}>
              Назад
            </Button>
          </Link>
          <Typography.Text type="secondary">Карточка мероприятия</Typography.Text>
        </Space>
      }
    >
      <Typography.Title level={3} style={{ marginTop: 0 }}>
        Редактирование
      </Typography.Title>

      {data && data.active_broadcasts.length > 0 ? (
        <Card
          size="small"
          title="Активный эфир — фактическое время начала"
          style={{ marginBottom: 16, borderColor: '#e2e8f0', background: '#ffffff' }}
          styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
        >
          <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
            Если оператор нажал «Начать эфир» позже, чем реально пошла картинка, укажите время старта в МСК — таймкоды
            сдвинутся.
          </Typography.Paragraph>
          <Space direction="vertical" size={16} style={{ width: '100%' }}>
            {data.active_broadcasts.map((b) => (
              <div key={b.id}>
                <Typography.Text strong style={{ display: 'block', marginBottom: 8 }}>
                  День {b.day_index}
                </Typography.Text>
                <BroadcastActualStartPanel streamId={streamId} dayIndex={b.day_index} startedAtIso={b.started_at} />
              </div>
            ))}
          </Space>
        </Card>
      ) : null}

      {data && endedLatestPerDay.length > 0 ? (
        <Card
          size="small"
          title="Завершённые эфиры — фактическое время начала"
          style={{ marginBottom: 16, borderColor: '#e2e8f0', background: '#ffffff' }}
          styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
        >
          <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
            Менеджер и суперадмин могут править любой завершённый эфир; оператор — последний завершённый эфир того дня,
            если он его вёл. Сдвиг времени старта сдвигает все таймкоды упоминаний этого эфира. По каждому дню
            используется последний завершённый эфир.
          </Typography.Paragraph>
          <Space direction="vertical" size={16} style={{ width: '100%' }}>
            {endedLatestPerDay.map((b) => (
              <div key={b.id}>
                <Typography.Text strong style={{ display: 'block', marginBottom: 8 }}>
                  День {b.day_index}
                  {b.mentions_count != null && b.mentions_count > 0 ? (
                    <Typography.Text type="secondary">
                      {' '}
                      · упоминаний: {b.mentions_count}
                    </Typography.Text>
                  ) : (
                    <Typography.Text type="secondary"> · упоминаний нет</Typography.Text>
                  )}
                </Typography.Text>
                <BroadcastActualStartPanel streamId={streamId} dayIndex={b.day_index} startedAtIso={b.started_at} />
              </div>
            ))}
          </Space>
        </Card>
      ) : null}

      <Card
        title="Упоминания оператора"
        style={{ marginBottom: 16, borderColor: '#e2e8f0', background: '#ffffff' }}
        styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
      >
        <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
          То же, что видит оператор в пульте: отметки по ходу эфира. Список обновляется при появлении новых записей
          (WebSocket).
        </Typography.Paragraph>
        {data ? (
          <>
            <Typography.Text type="secondary">День эфира</Typography.Text>
            <Select
              style={{ width: '100%', maxWidth: 360, marginTop: 8, marginBottom: 16, display: 'block' }}
              value={mentionDay}
              options={data.days.map((d) => ({ label: `День ${d.day_index}`, value: d.day_index }))}
              onChange={(v) => setMentionDay(v)}
            />
            <List
              loading={mentionsQuery.isLoading}
              dataSource={mentionsQuery.data ?? []}
              locale={{ emptyText: 'Пока нет упоминаний за этот день' }}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={
                      <Space wrap>
                        <Typography.Text strong>{item.adjusted_timecode}</Typography.Text>
                        {item.is_adjusted ? <Badge status="warning" text="Скорректировано" /> : null}
                      </Space>
                    }
                    description={
                      <Space direction="vertical" size={4}>
                        <Typography.Text type="secondary">
                          Время: {item.absolute_moscow_adjusted}
                        </Typography.Text>
                        <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                          Таймкод трансляции: {item.original_timecode}
                        </Typography.Text>
                        {item.adjustments && item.adjustments.length > 0 ? (
                          <div style={{ marginTop: 8 }}>
                            <Typography.Text
                              type="secondary"
                              style={{ fontSize: 12, display: 'block', marginBottom: 4 }}
                            >
                              Лог
                            </Typography.Text>
                            {item.adjustments.map((a) => (
                              <Typography.Text
                                key={a.id}
                                type="secondary"
                                style={{ fontSize: 12, display: 'block' }}
                              >
                                Запись: {formatDateTimeRu(a.created_at)} · {formatElapsed(a.previous_adjusted_sec)} →{' '}
                                {formatElapsed(a.new_adjusted_sec)}
                              </Typography.Text>
                            ))}
                          </div>
                        ) : null}
                      </Space>
                    }
                  />
                </List.Item>
              )}
            />
          </>
        ) : (
          <Typography.Text type="secondary">Загрузка мероприятия…</Typography.Text>
        )}
      </Card>

      <Card
        title="Логотипы"
        style={{ marginBottom: 16, borderColor: '#e2e8f0', background: '#ffffff' }}
        styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
        extra={
          <Space wrap>
            <Button
              icon={<FileZipOutlined />}
              onClick={() => downloadZipMut.mutate()}
              loading={downloadZipMut.isPending}
              disabled={!(data?.logos ?? []).length}
            >
              Скачать ZIP
            </Button>
            <Button type="primary" icon={<PlusOutlined />} onClick={() => setAddLogoOpen(true)}>
              Добавить логотип
            </Button>
          </Space>
        }
      >
        {!data ? (
          <Typography.Text type="secondary">Загрузка…</Typography.Text>
        ) : (data.logos ?? []).length === 0 ? (
          <Typography.Text type="secondary">Нет логотипов — нажмите «Добавить логотип»</Typography.Text>
        ) : (
          <Row gutter={[12, 12]}>
            {(data.logos ?? []).map((lg) => (
              <Col xs={12} sm={8} md={6} key={lg.id}>
                <Card
                  size="small"
                  cover={
                    <img
                      alt={lg.filename_original}
                      src={lg.public_url}
                      style={{ maxHeight: 120, objectFit: 'contain', padding: 8 }}
                    />
                  }
                >
                  <Space direction="vertical" size={4} style={{ width: '100%' }}>
                    <Typography.Text ellipsis style={{ fontSize: 12 }} title={lg.filename_original}>
                      {lg.filename_original}
                    </Typography.Text>
                    <Space wrap>
                      <Button
                        size="small"
                        icon={<DownloadOutlined />}
                        loading={downloadOneMut.isPending}
                        onClick={() => downloadOneMut.mutate(lg.id)}
                        aria-label={`Скачать ${lg.filename_original}`}
                      />
                      <Button
                        size="small"
                        danger
                        icon={<DeleteOutlined />}
                        loading={detachLogoMut.isPending}
                        onClick={() => detachLogoMut.mutate(lg.id)}
                        aria-label="Открепить логотип"
                      />
                    </Space>
                  </Space>
                </Card>
              </Col>
            ))}
          </Row>
        )}
      </Card>

      <Modal
        title="Добавить логотип"
        open={addLogoOpen}
        onCancel={() => setAddLogoOpen(false)}
        footer={null}
        destroyOnClose
        width={720}
      >
        <Tabs
          items={[
            {
              key: 'lib',
              label: 'Из медиатеки',
              children: (
                <div style={{ minHeight: 200 }}>
                  {logosLibraryQuery.isLoading ? (
                    <Typography.Text type="secondary">Загрузка списка…</Typography.Text>
                  ) : (
                    <Row gutter={[12, 12]}>
                      {(logosLibraryQuery.data ?? []).map((item) => (
                        <Col xs={12} sm={8} key={item.id}>
                          <Card
                            size="small"
                            hoverable
                            onClick={() => attachLogoMut.mutate(item.id)}
                            cover={
                              <img
                                alt={item.filename_original}
                                src={item.public_url}
                                style={{ maxHeight: 100, objectFit: 'contain', padding: 8 }}
                              />
                            }
                          >
                            <Typography.Text ellipsis style={{ fontSize: 12 }} title={item.filename_original}>
                              {item.filename_original}
                            </Typography.Text>
                          </Card>
                        </Col>
                      ))}
                    </Row>
                  )}
                </div>
              ),
            },
            {
              key: 'up',
              label: 'Загрузить файл',
              children: (
                <Spin spinning={logoBatchBusy} tip="Загрузка…">
                  <Space direction="vertical" style={{ width: '100%' }} size="middle">
                    <Upload.Dragger
                      multiple
                      maxCount={LOGO_UPLOAD_MAX_FILES}
                      accept="image/png,image/jpeg,image/gif,image/webp,image/svg+xml"
                      fileList={logoModalUploadList}
                      disabled={logoBatchBusy}
                      beforeUpload={() => false}
                      onChange={({ fileList }) => setLogoModalUploadList(fileList)}
                    >
                      <p className="ant-upload-text">Перетащите файлы или нажмите для выбора</p>
                      <p className="ant-upload-hint" style={{ color: '#64748b' }}>
                        Можно выбрать несколько файлов сразу. PNG, JPEG, GIF, WebP, SVG до 15 МБ каждый, не более{' '}
                        {LOGO_UPLOAD_MAX_FILES} за раз. После выбора нажмите кнопку ниже.
                      </p>
                    </Upload.Dragger>
                    <Button
                      type="primary"
                      block
                      loading={logoBatchBusy}
                      disabled={logoModalUploadList.length === 0 || logoBatchBusy}
                      onClick={() => void handleConfirmLogoUpload()}
                    >
                      Загрузить к эфиру
                    </Button>
                  </Space>
                </Spin>
              ),
            },
          ]}
        />
      </Modal>

      <Card loading={isLoading} style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
        <Form
          layout="vertical"
          form={form}
          onFinish={async (v) => {
            await saveMut.mutateAsync(v)
          }}
        >
          <Form.Item name="title" label="Название" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12}>
              <Form.Item name="start_date" label="Дата старта" rules={[{ required: true }]}>
                <DatePicker format="DD.MM.YYYY" style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24} sm={12}>
              <Form.Item name="duration_days" label="Дней" rules={[{ required: true }]}>
                <Select
                  style={{ width: '100%', minWidth: isNarrow ? undefined : 160 }}
                  options={[
                    { label: '1', value: 1 },
                    { label: '2', value: 2 },
                    { label: '3', value: 3 },
                    { label: '4', value: 4 },
                    { label: '5', value: 5 },
                  ]}
                />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="content_url"
            label="Ссылка на материалы (контент, например Яндекс.Диск)"
            rules={[
              {
                validator: async (_, v) => {
                  if (v == null || String(v).trim() === '') {
                    return Promise.resolve()
                  }
                  try {
                    // eslint-disable-next-line no-new
                    new URL(String(v))
                    return Promise.resolve()
                  } catch {
                    return Promise.reject(new Error('Введите корректный URL'))
                  }
                },
              },
            ]}
          >
            <Input
              placeholder="https://..."
              addonAfter={
                <Space size={0}>
                  <Button
                    type="text"
                    size="small"
                    icon={<CopyOutlined />}
                    onClick={(e) => {
                      e.preventDefault()
                      void handleCopyContentUrl()
                    }}
                    aria-label="Копировать ссылку"
                  />
                  <Button
                    type="text"
                    size="small"
                    icon={<LinkOutlined />}
                    onClick={(e) => {
                      e.preventDefault()
                      handleOpenContentUrl()
                    }}
                    aria-label="Открыть в новой вкладке"
                  />
                </Space>
              }
            />
          </Form.Item>

          <Typography.Title level={5}>Дни (URL и ключи)</Typography.Title>
          <Form.Item shouldUpdate noStyle>
            {() => {
              const n = Number(form.getFieldValue('duration_days') ?? data?.duration_days ?? 1)
              return Array.from({ length: n }, (_, i) => {
                const idx = i + 1
                return (
                  <Card
                    key={idx}
                    size="small"
                    title={`День ${idx}`}
                    style={{ marginBottom: 12, borderColor: '#e2e8f0', background: '#f8fafc' }}
                  >
                    <Form.Item name={`day_${idx}_stream_url`} label="Ссылка на трансляцию">
                      <Input />
                    </Form.Item>
                    <Form.Item name={`day_${idx}_server_url`} label="URL сервера трансляции">
                      <Input />
                    </Form.Item>
                    <Form.Item name={`day_${idx}_stream_key`} label="Ключ трансляции">
                      <Input />
                    </Form.Item>
                  </Card>
                )
              })
            }}
          </Form.Item>

          <Button
            type="primary"
            htmlType="submit"
            icon={<SaveOutlined />}
            loading={saveMut.isPending}
            size="large"
            block={isNarrow}
          >
            Сохранить
          </Button>
        </Form>
      </Card>
    </AppLayout>
  )
}

```


---

## Исходный код: `frontend/src/pages/ManagerStreamsPage.tsx`

> 612 строк, 21,573 байт

```tsx
import { CopyOutlined, DeleteOutlined, DownloadOutlined, PlusOutlined, SaveOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Button,
  Card,
  DatePicker,
  Form,
  Grid,
  Input,
  Modal,
  Select,
  Space,
  Table,
  Tooltip,
  Typography,
} from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import dayjs from 'dayjs'
import 'dayjs/locale/ru'
import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import type { StreamEventListOut, StreamEventTemplateOut } from '@/api/types'
import {
  apiFetch,
  createTemplateFromEventRequest,
  deleteEventTemplateRequest,
  instantiateTemplateRequest,
  listEventTemplatesRequest,
} from '@/api/client'
import { OperatorStatsPanel } from '@/components/OperatorStatsPanel'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateRu } from '@/utils/datetime'

dayjs.locale('ru')

const buildReportPath = (
  format: 'docx' | 'csv' | 'xlsx',
  v: { stream_id?: string; range?: [dayjs.Dayjs, dayjs.Dayjs] },
) => {
  const params = new URLSearchParams()
  if (v.stream_id) {
    params.set('stream_id', v.stream_id)
  }
  if (v.range?.[0] && v.range?.[1]) {
    params.set('date_from', v.range[0].format('YYYY-MM-DD'))
    params.set('date_to', v.range[1].format('YYYY-MM-DD'))
  }
  const qs = params.toString()
  const ext = format === 'docx' ? 'export.docx' : format === 'csv' ? 'export.csv' : 'export.xlsx'
  return `/reports/${ext}${qs ? `?${qs}` : ''}`
}

export const ManagerStreamsPage: React.FC = () => {
  const { message, modal } = AntApp.useApp()
  const qc = useQueryClient()
  const nav = useNavigate()
  const screens = Grid.useBreakpoint()
  const isNarrow = !screens.md
  const [open, setOpen] = useState(false)
  const [reportOpen, setReportOpen] = useState(false)
  const [tplNameOpen, setTplNameOpen] = useState(false)
  const [tplStreamId, setTplStreamId] = useState<string | null>(null)
  const [instantiateOpen, setInstantiateOpen] = useState(false)
  const [createForm] = Form.useForm()
  const [reportForm] = Form.useForm()
  const [tplNameForm] = Form.useForm()
  const [instantiateForm] = Form.useForm()

  const { data, isLoading } = useQuery({
    queryKey: ['streams'],
    queryFn: async () => (await apiFetch('/stream-events')) as StreamEventListOut[],
  })

  const { data: templates, isLoading: tplLoading } = useQuery({
    queryKey: ['stream-event-templates'],
    queryFn: listEventTemplatesRequest,
  })

  const createMut = useMutation({
    mutationFn: async (values: {
      title: string
      start_date: dayjs.Dayjs
      duration_days: number
      template_id?: string
    }) => {
      if (values.template_id) {
        await apiFetch('/stream-events', {
          method: 'POST',
          body: JSON.stringify({
            title: values.title,
            start_date: values.start_date.format('YYYY-MM-DD'),
            duration_days: values.duration_days,
            template_id: values.template_id,
          }),
        })
        return
      }
      const days = Array.from({ length: values.duration_days }, (_, i) => ({
        day_index: i + 1,
        stream_url: '',
        server_url: '',
        stream_key: '',
      }))
      await apiFetch('/stream-events', {
        method: 'POST',
        body: JSON.stringify({
          title: values.title,
          start_date: values.start_date.format('YYYY-MM-DD'),
          duration_days: values.duration_days,
          days,
        }),
      })
    },
    onSuccess: async () => {
      message.success('Мероприятие создано')
      setOpen(false)
      createForm.resetFields()
      await qc.invalidateQueries({ queryKey: ['streams'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const downloadExport = async (format: 'docx' | 'csv' | 'xlsx') => {
    const v = reportForm.getFieldsValue() as {
      stream_id?: string
      range?: [dayjs.Dayjs, dayjs.Dayjs]
    }
    const path = buildReportPath(format, v)
    const blob = (await apiFetch(path)) as Blob
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download =
      format === 'docx' ? 'mentions_report.docx' : format === 'csv' ? 'mentions_report.csv' : 'mentions_report.xlsx'
    a.click()
    URL.revokeObjectURL(url)
    message.success('Файл скачан')
  }

  const saveTplMut = useMutation({
    mutationFn: async ({ streamId, name }: { streamId: string; name: string }) =>
      createTemplateFromEventRequest(streamId, name),
    onSuccess: async () => {
      message.success('Шаблон сохранён')
      setTplNameOpen(false)
      setTplStreamId(null)
      tplNameForm.resetFields()
      await qc.invalidateQueries({ queryKey: ['stream-event-templates'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const delTplMut = useMutation({
    mutationFn: deleteEventTemplateRequest,
    onSuccess: async () => {
      message.success('Шаблон удалён')
      await qc.invalidateQueries({ queryKey: ['stream-event-templates'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const instMut = useMutation({
    mutationFn: async (values: {
      template_id: string
      title: string
      start_date: dayjs.Dayjs
      duration_days: number
    }) =>
      instantiateTemplateRequest(values.template_id, {
        title: values.title,
        start_date: values.start_date.format('YYYY-MM-DD'),
        duration_days: values.duration_days,
      }),
    onSuccess: async (detail) => {
      message.success('Мероприятие создано из шаблона')
      setInstantiateOpen(false)
      instantiateForm.resetFields()
      await qc.invalidateQueries({ queryKey: ['streams'] })
      nav(`/manager/${detail.id}`)
    },
    onError: (e: Error) => message.error(e.message),
  })

  const deleteStreamMut = useMutation({
    mutationFn: async (id: string) => {
      await apiFetch(`/stream-events/${id}`, { method: 'DELETE' })
    },
    onSuccess: async () => {
      message.success('Мероприятие удалено')
      await qc.invalidateQueries({ queryKey: ['streams'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const columns: ColumnsType<StreamEventListOut> = [
    { title: 'Название', dataIndex: 'title', key: 'title' },
    {
      title: 'Старт',
      dataIndex: 'start_date',
      key: 'start_date',
      width: 120,
      render: (v: string) => formatDateRu(v),
    },
    { title: 'Дней', dataIndex: 'duration_days', key: 'duration_days', width: 90 },
    {
      title: 'Статус',
      key: 'status',
      render: (_, r) => (
        <Space direction="vertical" size={0}>
          <Typography.Text type="secondary">
            {r.has_active_broadcast ? 'Эфир активен' : 'Нет эфира'}
          </Typography.Text>
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            {r.assignment_summary
              ? r.assignment_summary
              : r.locked_by_user_id
                ? r.locked_by_display_name
                  ? `В работе: ${r.locked_by_display_name}`
                  : 'В работе у оператора'
                : 'Свободно'}
          </Typography.Text>
        </Space>
      ),
    },
    {
      title: 'Трансляция',
      key: 'stream_links',
      width: 260,
      render: (_, r) => (
        <Space direction="vertical" size={6} style={{ maxWidth: 280 }}>
          {(r.day_stream_links ?? []).length === 0 ? (
            <Typography.Text type="secondary" style={{ fontSize: 12 }}>
              —
            </Typography.Text>
          ) : (
            (r.day_stream_links ?? []).map((d) => (
              <Space key={d.day_index} size={8} wrap align="center">
                <Typography.Text type="secondary" style={{ fontSize: 12, whiteSpace: 'nowrap' }}>
                  День {d.day_index}
                </Typography.Text>
                {d.stream_url ? (
                  <Tooltip title={d.stream_url}>
                    <Button
                      type="link"
                      size="small"
                      icon={<CopyOutlined />}
                      style={{ padding: 0 }}
                      onClick={async () => {
                        await navigator.clipboard.writeText(d.stream_url)
                        message.success(`День ${d.day_index}: ссылка скопирована`)
                      }}
                      aria-label={`Скопировать ссылку трансляции, день ${d.day_index}`}
                    >
                      Копировать
                    </Button>
                  </Tooltip>
                ) : (
                  <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                    нет ссылки
                  </Typography.Text>
                )}
              </Space>
            ))
          )}
        </Space>
      ),
    },
    {
      title: '',
      key: 'actions',
      width: 280,
      render: (_, r) => (
        <Space wrap size="small">
          <Link to={`/manager/${r.id}`}>
            <Button type="link">Подробнее</Button>
          </Link>
          <Button
            type="link"
            icon={<SaveOutlined />}
            onClick={() => {
              setTplStreamId(r.id)
              tplNameForm.setFieldsValue({ name: `${r.title} (шаблон)` })
              setTplNameOpen(true)
            }}
          >
            В шаблон
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            loading={deleteStreamMut.isPending}
            onClick={() => {
              if (r.has_active_broadcast) {
                message.warning('Сначала остановите активный эфир — иначе удаление заблокировано')
                return
              }
              modal.confirm({
                title: 'Удалить мероприятие?',
                content: `«${r.title}»: будут удалены дни, записи эфиров и упоминания. Действие необратимо.`,
                okText: 'Удалить',
                okButtonProps: { danger: true },
                cancelText: 'Отмена',
                onOk: async () => {
                  await deleteStreamMut.mutateAsync(r.id)
                },
              })
            }}
          >
            Удалить
          </Button>
        </Space>
      ),
    },
  ]

  const tplColumns: ColumnsType<StreamEventTemplateOut> = [
    { title: 'Имя шаблона', dataIndex: 'name', key: 'name' },
    { title: 'Заголовок', dataIndex: 'title', key: 'title' },
    { title: 'Дней', dataIndex: 'duration_days', key: 'duration_days', width: 72 },
    {
      title: '',
      key: 'act',
      width: 200,
      render: (_, r) => (
        <Space>
          <Button
            type="link"
            onClick={() => {
              instantiateForm.setFieldsValue({
                template_id: r.id,
                title: '',
                start_date: dayjs(),
                duration_days: r.duration_days,
              })
              setInstantiateOpen(true)
            }}
          >
            Создать мероприятие
          </Button>
          <Button
            type="text"
            danger
            icon={<DeleteOutlined />}
            onClick={() => void delTplMut.mutateAsync(r.id)}
            loading={delTplMut.isPending}
          />
        </Space>
      ),
    },
  ]

  return (
    <AppLayout
      nav={
        <Typography.Text type="secondary" style={{ fontSize: 13 }}>
          Перейти к трансляциям
        </Typography.Text>
      }
    >
      <Card
        title="Статистика операторов"
        style={{ marginBottom: 16, borderColor: '#e2e8f0', background: '#ffffff' }}
        styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
      >
        <OperatorStatsPanel compact />
      </Card>

      <Card
        title="Шаблоны мероприятий"
        style={{ marginBottom: 16, borderColor: '#e2e8f0', background: '#ffffff' }}
        styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
        extra={
          <Typography.Text type="secondary" style={{ fontSize: 12 }}>
            Шаблон запоминает URL сервера — при создании мероприятия он подставляется во все дни; название, даты и
            остальные поля вводятся заново
          </Typography.Text>
        }
      >
        <Table
          rowKey="id"
          loading={tplLoading}
          dataSource={templates ?? []}
          columns={tplColumns}
          pagination={{ pageSize: 6 }}
          size="small"
          scroll={{ x: 640 }}
        />
      </Card>

      <Space
        style={{ width: '100%', justifyContent: 'space-between', marginBottom: 16 }}
        align="start"
        direction={isNarrow ? 'vertical' : 'horizontal'}
        size="middle"
      >
        <div>
          <Typography.Title level={3} style={{ marginTop: 0 }}>
            Мероприятия
          </Typography.Title>
          <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
            Создание, шаблоны, отчёты — Word, CSV и Excel. Колонка «Трансляция» — копирование ссылки на трансляцию по
            дням без захода в карточку.
          </Typography.Paragraph>
        </div>
        <Space wrap style={{ width: isNarrow ? '100%' : undefined }}>
          <Button icon={<DownloadOutlined />} onClick={() => setReportOpen(true)} block={isNarrow} size="large">
            Экспорт отчёта
          </Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={() => setOpen(true)} block={isNarrow} size="large">
            Новое мероприятие
          </Button>
        </Space>
      </Space>

      <Card style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
        <Table
          rowKey="id"
          loading={isLoading}
          dataSource={data ?? []}
          columns={columns}
          pagination={{ pageSize: 10 }}
          scroll={{ x: 1000 }}
          size={isNarrow ? 'small' : 'middle'}
        />
      </Card>

      <Modal
        title="Новое мероприятие"
        open={open}
        okText="Создать"
        cancelText="Отмена"
        confirmLoading={createMut.isPending}
        onCancel={() => setOpen(false)}
        onOk={async () => {
          const v = await createForm.validateFields()
          await createMut.mutateAsync(v)
        }}
      >
        <Form form={createForm} layout="vertical">
          <Form.Item name="title" label="Название" rules={[{ required: true, message: 'Обязательно' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="start_date" label="Дата старта" rules={[{ required: true, message: 'Обязательно' }]}>
            <DatePicker style={{ width: '100%' }} format="DD.MM.YYYY" />
          </Form.Item>
          <Form.Item
            name="duration_days"
            label="Длительность (дней)"
            initialValue={3}
            rules={[{ required: true }]}
          >
            <Select
              options={[
                { label: '1', value: 1 },
                { label: '2', value: 2 },
                { label: '3', value: 3 },
                { label: '4', value: 4 },
                { label: '5', value: 5 },
              ]}
            />
          </Form.Item>
          <Form.Item
            name="template_id"
            label="Шаблон (необязательно)"
            extra="Подставит один и тот же URL сервера трансляции во все дни. Ссылку, ключ и прочее вводите в карточке мероприятия отдельно."
          >
            <Select
              allowClear
              showSearch
              optionFilterProp="label"
              placeholder="Без шаблона"
              options={(templates ?? []).map((t) => ({ label: `${t.name} · ${t.title}`, value: t.id }))}
            />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Имя шаблона"
        open={tplNameOpen}
        okText="Сохранить"
        onCancel={() => {
          setTplNameOpen(false)
          setTplStreamId(null)
        }}
        confirmLoading={saveTplMut.isPending}
        onOk={async () => {
          const v = await tplNameForm.validateFields()
          if (!tplStreamId) {
            return
          }
          await saveTplMut.mutateAsync({ streamId: tplStreamId, name: v.name as string })
        }}
      >
        <Form form={tplNameForm} layout="vertical">
          <Form.Item name="name" label="Название шаблона" rules={[{ required: true, message: 'Обязательно' }]}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Мероприятие из шаблона"
        open={instantiateOpen}
        okText="Создать"
        onCancel={() => setInstantiateOpen(false)}
        confirmLoading={instMut.isPending}
        onOk={async () => {
          const v = await instantiateForm.validateFields()
          await instMut.mutateAsync(
            v as {
              template_id: string
              title: string
              start_date: dayjs.Dayjs
              duration_days: number
            },
          )
        }}
      >
        <Form form={instantiateForm} layout="vertical">
          <Form.Item name="template_id" hidden>
            <Input />
          </Form.Item>
          <Form.Item name="title" label="Название мероприятия" rules={[{ required: true, message: 'Обязательно' }]}>
            <Input placeholder="Новое название турнира" />
          </Form.Item>
          <Form.Item name="start_date" label="Дата старта" rules={[{ required: true }]}>
            <DatePicker style={{ width: '100%' }} format="DD.MM.YYYY" />
          </Form.Item>
          <Form.Item name="duration_days" label="Длительность (дней)" rules={[{ required: true }]}>
            <Select
              options={[
                { label: '1', value: 1 },
                { label: '2', value: 2 },
                { label: '3', value: 3 },
                { label: '4', value: 4 },
                { label: '5', value: 5 },
              ]}
            />
          </Form.Item>
          <Typography.Paragraph type="secondary" style={{ marginBottom: 0, fontSize: 12 }}>
            Из шаблона подставится только URL сервера во все дни; ссылки и ключи заполните в карточке.
          </Typography.Paragraph>
        </Form>
      </Modal>

      <Modal
        title="Экспорт отчёта по упоминаниям"
        open={reportOpen}
        onCancel={() => setReportOpen(false)}
        footer={null}
      >
        <Form form={reportForm} layout="vertical">
          <Form.Item name="stream_id" label="Фильтр: мероприятие (необязательно)">
            <Select
              allowClear
              placeholder="Все мероприятия"
              options={(data ?? []).map((s) => ({ label: s.title, value: s.id }))}
            />
          </Form.Item>
          <Form.Item name="range" label="Диапазон дат (по времени создания упоминания, МСК)">
            <DatePicker.RangePicker style={{ width: '100%' }} format="DD.MM.YYYY" />
          </Form.Item>
          <Space wrap>
            <Button
              type="primary"
              icon={<DownloadOutlined />}
              onClick={async () => {
                try {
                  await downloadExport('docx')
                  setReportOpen(false)
                } catch (e) {
                  message.error(e instanceof Error ? e.message : 'Ошибка')
                }
              }}
            >
              Скачать Word (.docx)
            </Button>
            <Button
              onClick={async () => {
                try {
                  await downloadExport('csv')
                  setReportOpen(false)
                } catch (e) {
                  message.error(e instanceof Error ? e.message : 'Ошибка')
                }
              }}
            >
              Скачать CSV
            </Button>
            <Button
              onClick={async () => {
                try {
                  await downloadExport('xlsx')
                  setReportOpen(false)
                } catch (e) {
                  message.error(e instanceof Error ? e.message : 'Ошибка')
                }
              }}
            >
              Скачать Excel (.xlsx)
            </Button>
          </Space>
        </Form>
      </Modal>
    </AppLayout>
  )
}

```


---

## Исходный код: `frontend/src/pages/OnboardingPage.tsx`

> 259 строк, 10,580 байт

```tsx
import { RocketOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Button,
  Card,
  Divider,
  Form,
  Input,
  Space,
  Steps,
  Tag,
  Typography,
  Upload,
} from 'antd'
import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { patchProfileRequest, uploadAvatarRequest } from '@/api/client'
import type { UserRole } from '@/api/types'
import { useAuth } from '@/auth/AuthContext'
import { BrandLogo } from '@/components/BrandLogo'
import { OtherRolesHint, PrimaryRoleTraining } from '@/content/onboardingRoleGuides'
import { normalizeRuMobilePhone } from '@/utils/normalizeRuMobilePhone'

const roleTitle: Record<UserRole, string> = {
  SUPERADMIN: 'Суперадминистратор',
  STREAM_MANAGER: 'Менеджер',
  OPERATOR: 'Оператор',
}

export const OnboardingPage: React.FC = () => {
  const { message } = AntApp.useApp()
  const { user, refreshMe } = useAuth()
  const nav = useNavigate()
  const [step, setStep] = useState(0)
  const [nameForm] = Form.useForm()
  const [finishing, setFinishing] = useState(false)

  useEffect(() => {
    if (user?.onboarding_completed) {
      nav('/dashboard', { replace: true })
    }
  }, [user?.onboarding_completed, user, nav])

  if (!user) {
    return null
  }

  const currentRole = user.role as UserRole

  const handleSkipTour = async () => {
    setFinishing(true)
    try {
      await patchProfileRequest({ onboarding_completed: true })
      await refreshMe()
      message.info('Ознакомление пропущено — всё можно настроить позже в «Профиль»')
      nav('/dashboard', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Ошибка')
    } finally {
      setFinishing(false)
    }
  }

  const handleFinish = async () => {
    setFinishing(true)
    try {
      await patchProfileRequest({ onboarding_completed: true })
      await refreshMe()
      message.success('Добро пожаловать в панель')
      nav('/dashboard', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Ошибка')
    } finally {
      setFinishing(false)
    }
  }

  const steps = [
    { title: 'Старт', icon: <RocketOutlined /> },
    { title: 'Профиль', icon: <UserOutlined /> },
    { title: 'Аватар', icon: <UserOutlined /> },
    { title: 'Роли', icon: <TeamOutlined /> },
  ]

  return (
    <div
      style={{
        minHeight: '100dvh',
        padding: 24,
        paddingTop: 'max(24px, env(safe-area-inset-top, 0px))',
        background:
          'radial-gradient(1200px 600px at 20% 0%, rgba(61,126,255,0.18), transparent), #f5f7fa',
      }}
    >
      <div style={{ maxWidth: step === 3 ? 760 : 640, margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <BrandLogo height={36} />
          <Button type="link" onClick={() => void handleSkipTour()} disabled={finishing}>
            Пропустить ознакомление
          </Button>
        </div>

        <Steps current={step} items={steps} responsive style={{ marginBottom: 28 }} />

        <Card style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
          {step === 0 && (
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              <Typography.Title level={4} style={{ marginTop: 0, color: '#0f172a' }}>
                Добро пожаловать в MainStream Ops
              </Typography.Title>
              <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
                Сервис для видеооператоров MainStream: расписание эфиров, таймкоды спонсорских упоминаний, роли операторов и
                менеджеров. Сейчас коротко настроим профиль и покажем, что доступно именно вам.
              </Typography.Paragraph>
              <Button type="primary" size="large" block onClick={() => setStep(1)}>
                Начать
              </Button>
            </Space>
          )}

          {step === 1 && (
            <Form
              form={nameForm}
              layout="vertical"
              initialValues={{
                first_name: user.first_name,
                last_name: user.last_name,
                phone: user.phone ?? '',
              }}
              onFinish={async (v) => {
                try {
                  await patchProfileRequest({
                    first_name: v.first_name,
                    last_name: v.last_name,
                    phone: v.phone,
                  })
                  await refreshMe()
                  message.success('Сохранено')
                  setStep(2)
                } catch (e) {
                  message.error(e instanceof Error ? e.message : 'Ошибка')
                }
              }}
            >
              <Typography.Title level={4} style={{ marginTop: 0, color: '#0f172a' }}>
                Как к вам обращаться
              </Typography.Title>
              <Typography.Paragraph type="secondary">
                Имя, фамилия и мобильный телефон (Россия) — отображаются в панели и отчётах. Потом всё можно изменить в
                «Профиль». Телефон можно ввести как <Typography.Text code>79060943936</Typography.Text>,{' '}
                <Typography.Text code>89060943936</Typography.Text> или с пробелами — сохранится в едином формате.
              </Typography.Paragraph>
              <Form.Item name="last_name" label="Фамилия" rules={[{ required: true, whitespace: true }]}>
                <Input autoComplete="family-name" />
              </Form.Item>
              <Form.Item name="first_name" label="Имя" rules={[{ required: true, whitespace: true }]}>
                <Input autoComplete="given-name" />
              </Form.Item>
              <Form.Item
                name="phone"
                label="Мобильный телефон"
                rules={[
                  { required: true, message: 'Укажите телефон' },
                  {
                    validator: async (_, value: string) => {
                      const t = (value ?? '').trim()
                      if (!t) {
                        return Promise.reject(new Error('Укажите телефон'))
                      }
                      try {
                        normalizeRuMobilePhone(t)
                        return Promise.resolve()
                      } catch {
                        return Promise.reject(
                          new Error('Нужен российский мобильный: с 7, 8 или 9 (10 или 11 цифр)'),
                        )
                      }
                    },
                  },
                ]}
              >
                <Input placeholder="Например 79060943936 или 8 906 094-39-36" autoComplete="tel" inputMode="tel" />
              </Form.Item>
              <Space wrap>
                <Button onClick={() => setStep(0)}>Назад</Button>
                <Button type="primary" htmlType="submit">
                  Далее
                </Button>
              </Space>
            </Form>
          )}

          {step === 2 && (
            <div>
              <Typography.Title level={4} style={{ marginTop: 0, color: '#0f172a' }}>
                Аватар
              </Typography.Title>
              <Typography.Paragraph type="secondary">
                По желанию загрузите фото профиля (JPEG, PNG или WebP, до 2 МБ). Это можно сделать и позже в «Профиль».
              </Typography.Paragraph>
              <Upload
                accept="image/jpeg,image/png,image/webp"
                showUploadList={false}
                beforeUpload={(file) => {
                  void (async () => {
                    try {
                      await uploadAvatarRequest(file as File)
                      await refreshMe()
                      message.success('Аватар загружен')
                    } catch (e) {
                      message.error(e instanceof Error ? e.message : 'Ошибка загрузки')
                    }
                  })()
                  return false
                }}
              >
                <Button type="default">Выбрать файл</Button>
              </Upload>
              <div style={{ marginTop: 20 }}>
                <Space wrap>
                  <Button onClick={() => setStep(1)}>Назад</Button>
                  <Button type="primary" onClick={() => setStep(3)}>
                    Далее
                  </Button>
                </Space>
              </div>
            </div>
          )}

          {step === 3 && (
            <div>
              <Typography.Title level={4} style={{ marginTop: 0, color: '#0f172a' }}>
                Как пользоваться панелью
              </Typography.Title>
              <Typography.Paragraph type="secondary" style={{ marginBottom: 16 }}>
                Ваша роль: <Tag color="blue">{roleTitle[currentRole]}</Tag> — ниже пошаговая инструкция под неё (без
                повторов).
              </Typography.Paragraph>
              <PrimaryRoleTraining role={currentRole} />
              <Divider style={{ borderColor: '#e2e8f0', margin: '20px 0' }} />
              <Typography.Text strong style={{ display: 'block', marginBottom: 8, color: '#334155' }}>
                Остальные роли — кратко
              </Typography.Text>
              <OtherRolesHint currentRole={currentRole} />
              <Space wrap style={{ marginTop: 24 }}>
                <Button onClick={() => setStep(2)}>Назад</Button>
                <Button type="primary" size="large" loading={finishing} onClick={() => void handleFinish()}>
                  Перейти в панель
                </Button>
              </Space>
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}

```


---

## Исходный код: `frontend/src/pages/OperatorEventPage.tsx`

> 1294 строк, 53,617 байт

```tsx
import {
  ArrowLeftOutlined,
  CheckOutlined,
  CopyOutlined,
  DeleteOutlined,
  DownloadOutlined,
  FileZipOutlined,
  LinkOutlined,
  PlusOutlined,
  PlayCircleOutlined,
  StopOutlined,
} from '@ant-design/icons'
import {
  App as AntApp,
  Badge,
  Button,
  Card,
  Checkbox,
  Col,
  Divider,
  Grid,
  Row,
  InputNumber,
  List,
  Modal,
  Select,
  Space,
  Tooltip,
  Typography,
} from 'antd'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import type { BroadcastChecklistOut, SponsorMentionOut, StreamEventDetailOut } from '@/api/types'
import { apiFetch, fetchAuthorizedBlob, triggerBlobDownload } from '@/api/client'
import { useAuth } from '@/auth/AuthContext'
import { BroadcastActualStartPanel } from '@/components/BroadcastActualStartPanel'
import { useStreamWs } from '@/hooks/useStreamWs'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateRu, formatDateTimeRu } from '@/utils/datetime'

const formatElapsed = (totalSec: number) => {
  const sec = Math.max(0, Math.floor(totalSec))
  const h = Math.floor(sec / 3600)
  const m = Math.floor((sec % 3600) / 60)
  const s = sec % 60
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

const IDLE_REMINDER_MS = 2 * 60 * 60 * 1000

const MENTION_SLOT_LABELS = ['Начало эфира', 'Середина 1', 'Середина 2', 'Конец эфира'] as const

export const OperatorEventPage: React.FC = () => {
  const { id } = useParams()
  const streamId = id as string
  const { user } = useAuth()
  const { message, modal } = AntApp.useApp()
  const handleCopyLinkField = useCallback(
    async (text: string) => {
      const t = text.trim()
      if (!t) {
        return
      }
      try {
        await navigator.clipboard.writeText(t)
        message.success('Скопировано в буфер обмена')
      } catch {
        message.error('Не удалось скопировать')
      }
    },
    [message],
  )
  const qc = useQueryClient()
  const screens = Grid.useBreakpoint()
  const isComfortable = Boolean(screens.md)
  const [day, setDay] = useState(1)
  const [tick, setTick] = useState(0)
  const [adjustTarget, setAdjustTarget] = useState<SponsorMentionOut | null>(null)
  const [adjustMinutes, setAdjustMinutes] = useState(0)
  const [adjustSecondsPart, setAdjustSecondsPart] = useState(0)

  const detailQuery = useQuery({
    queryKey: ['stream', streamId],
    enabled: Boolean(streamId),
    queryFn: async () => (await apiFetch(`/stream-events/${streamId}`)) as StreamEventDetailOut,
  })

  const checklistQuery = useQuery({
    queryKey: ['checklist', streamId, day],
    enabled: Boolean(streamId) && detailQuery.isSuccess,
    queryFn: async () =>
      (await apiFetch(`/stream-events/${streamId}/days/${day}/checklist`)) as BroadcastChecklistOut,
  })

  const checklistMut = useMutation({
    mutationFn: async (patch: {
      picture_exposure_ok?: boolean
      judges_stream_ok?: boolean
      splitter_socket_ok?: boolean
      key_stream_started_ok?: boolean
      kick_ok?: boolean
      mentions_four_ok?: boolean
    }) => {
      await apiFetch(`/stream-events/${streamId}/days/${day}/checklist`, {
        method: 'PUT',
        body: JSON.stringify(patch),
      })
    },
    onSuccess: async () => {
      await qc.invalidateQueries({ queryKey: ['checklist', streamId] })
    },
  })

  const [wsViewers, setWsViewers] = useState<number | null>(null)

  useStreamWs(
    streamId,
    (msg) => {
      if (msg.type === 'presence') {
        const p = msg.payload as { viewers?: number } | undefined
        if (p?.viewers != null) {
          setWsViewers(p.viewers)
        }
        return
      }
      void qc.invalidateQueries({ queryKey: ['stream', streamId] })
      void qc.invalidateQueries({ queryKey: ['mentions', streamId, day] })
    },
    detailQuery.isSuccess,
  )

  const mentionsQuery = useQuery({
    queryKey: ['mentions', streamId, day],
    enabled: Boolean(streamId),
    queryFn: async () =>
      (await apiFetch(`/stream-events/${streamId}/days/${day}/mentions`)) as SponsorMentionOut[],
  })

  const data = detailQuery.data

  useEffect(() => {
    if (!data) {
      return
    }
    if (day > data.duration_days) {
      setDay(1)
    }
  }, [data, day])

  useEffect(() => {
    const t = window.setInterval(() => setTick((x) => x + 1), 1000)
    return () => window.clearInterval(t)
  }, [])

  const activeSession = useMemo(
    () => data?.active_broadcasts.find((b) => b.day_index === day),
    [data, day, tick],
  )

  const elapsedSec = useMemo(() => {
    if (!activeSession) {
      return 0
    }
    const start = new Date(activeSession.started_at).getTime()
    return Math.floor((Date.now() - start) / 1000)
  }, [activeSession, tick])

  const takenDays = useMemo(
    () => new Set((data?.day_assignments ?? []).map((a) => a.day_index)),
    [data?.day_assignments],
  )

  const freeDays = useMemo(() => {
    if (!data) {
      return [] as number[]
    }
    return Array.from({ length: data.duration_days }, (_, i) => i + 1).filter((d) => !takenDays.has(d))
  }, [data, takenDays])

  const myDayIndices = useMemo(
    () =>
      (data?.day_assignments ?? [])
        .filter((a) => a.operator_id === user?.id)
        .map((a) => a.day_index)
        .sort((a, b) => a - b),
    [data?.day_assignments, user?.id],
  )

  const operatorForSelectedDay = useMemo(() => {
    const a = (data?.day_assignments ?? []).find((x) => x.day_index === day)
    return a?.operator_id
  }, [data?.day_assignments, day])

  const foreignLock = Boolean(
    user?.role !== 'SUPERADMIN' && operatorForSelectedDay && operatorForSelectedDay !== user?.id,
  )

  const superadminLockActionsBlocked = useMemo(
    () =>
      Boolean(
        user?.role === 'SUPERADMIN' &&
          (data?.day_assignments ?? []).some((a) => a.operator_id !== user.id),
      ),
    [user?.role, user?.id, data?.day_assignments],
  )

  const iHaveLock = Boolean(
    user &&
      ((user.role === 'OPERATOR' && myDayIndices.length > 0) ||
        (user.role === 'SUPERADMIN' && !superadminLockActionsBlocked)),
  )

  const dayIsAssigned = operatorForSelectedDay != null
  const iAmAssignedOperator = Boolean(operatorForSelectedDay != null && operatorForSelectedDay === user?.id)
  /** Суперадмин или назначенный на день оператор (упоминания, таймер простоя) */
  const iOperateThisDay = Boolean(
    user?.role === 'SUPERADMIN' || (!foreignLock && iAmAssignedOperator),
  )
  const canStartBroadcast = Boolean(
    !foreignLock && dayIsAssigned && (user?.role === 'SUPERADMIN' || iAmAssignedOperator),
  )
  const restartBlocked = Boolean(data?.broadcast_restart_blocked_days?.includes(day))

  const canRealignBroadcast = useMemo(() => {
    if (!activeSession) {
      return false
    }
    if (user?.role === 'SUPERADMIN' || user?.role === 'STREAM_MANAGER') {
      return true
    }
    if (user?.role === 'OPERATOR') {
      return Boolean(!foreignLock && iAmAssignedOperator)
    }
    return false
  }, [activeSession, user?.role, foreignLock, iAmAssignedOperator])

  const latestEndedForSelectedDay = useMemo(() => {
    const list = data?.ended_broadcasts ?? []
    return list.find((b) => b.day_index === day) ?? null
  }, [data?.ended_broadcasts, day])

  const canShowEndedRealignPanel = useMemo(() => {
    const b = latestEndedForSelectedDay
    if (!b) {
      return false
    }
    if (user?.role === 'SUPERADMIN' || user?.role === 'STREAM_MANAGER') {
      return true
    }
    if (user?.role === 'OPERATOR') {
      return b.operator_id === user?.id
    }
    return false
  }, [latestEndedForSelectedDay, user?.role, user?.id])

  /** Активный эфир — как раньше; после остановки — те же права, что у сдвига фактического старта */
  const canEditMentionsForSelectedDay = useMemo(() => {
    if (activeSession) {
      if (foreignLock) {
        return false
      }
      return iOperateThisDay
    }
    return canShowEndedRealignPanel
  }, [activeSession, foreignLock, iOperateThisDay, canShowEndedRealignPanel])

  const canTakeLock = useMemo(() => {
    if (!data || !user) {
      return false
    }
    if (user.role === 'SUPERADMIN' && superadminLockActionsBlocked) {
      return false
    }
    return freeDays.length > 0
  }, [data, user, freeDays.length, superadminLockActionsBlocked])

  const [lockModalOpen, setLockModalOpen] = useState(false)
  const [lockDayPick, setLockDayPick] = useState<number[]>([])

  const selectedDayRow = useMemo(() => data?.days.find((d) => d.day_index === day), [data, day])

  const [streamCredsVisible, setStreamCredsVisible] = useState(true)
  const lastIdleDismissAtRef = useRef(0)
  const [idleDismissVersion, setIdleDismissVersion] = useState(0)

  const orderedMentionsForPlan = useMemo(() => {
    const list = [...(mentionsQuery.data ?? [])]
    list.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
    return list
  }, [mentionsQuery.data])

  const lastMentionMs = useMemo(() => {
    const list = mentionsQuery.data ?? []
    if (!list.length) {
      return null
    }
    return Math.max(...list.map((m) => new Date(m.created_at).getTime()))
  }, [mentionsQuery.data])

  useEffect(() => {
    lastIdleDismissAtRef.current = 0
    setIdleDismissVersion((v) => v + 1)
  }, [activeSession?.id, day])

  const idleAnchorMs = useMemo(() => {
    if (!activeSession) {
      return null
    }
    const t0 = new Date(activeSession.started_at).getTime()
    const dismiss = lastIdleDismissAtRef.current
    const parts = [t0, dismiss]
    if (lastMentionMs) {
      parts.push(lastMentionMs)
    }
    return Math.max(...parts)
  }, [activeSession, lastMentionMs, idleDismissVersion, tick])

  const showIdleReminder = useMemo(() => {
    if (!idleAnchorMs || !activeSession || foreignLock || !iOperateThisDay) {
      return false
    }
    if (user?.role !== 'OPERATOR') {
      return false
    }
    return Date.now() - idleAnchorMs >= IDLE_REMINDER_MS
  }, [idleAnchorMs, activeSession, foreignLock, iOperateThisDay, tick, user?.role])

  const handleIdleReminderDismiss = () => {
    lastIdleDismissAtRef.current = Date.now()
    setIdleDismissVersion((v) => v + 1)
  }

  const adjustTotalSec = useMemo(
    () => Math.max(0, adjustMinutes * 60 + adjustSecondsPart),
    [adjustMinutes, adjustSecondsPart],
  )

  const lockMut = useMutation({
    mutationFn: async (day_indices: number[]) => {
      await apiFetch(`/stream-events/${streamId}/lock`, {
        method: 'POST',
        body: JSON.stringify({ day_indices }),
      })
    },
    onSuccess: async () => {
      message.success('Дни назначены')
      setLockModalOpen(false)
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const unlockMut = useMutation({
    mutationFn: async () => {
      await apiFetch(`/stream-events/${streamId}/unlock`, { method: 'POST', body: '{}' })
    },
    onSuccess: async () => {
      message.success('Снято с работы')
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const startMut = useMutation({
    mutationFn: async () => {
      await apiFetch(`/stream-events/${streamId}/days/${day}/broadcast/start`, { method: 'POST' })
    },
    onSuccess: async () => {
      message.success('Эфир начат (время старта зафиксировано)')
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const downloadZipMut = useMutation({
    mutationFn: async () => {
      const { blob, filename } = await fetchAuthorizedBlob(`/stream-events/${streamId}/logos/archive.zip`)
      triggerBlobDownload(blob, filename)
    },
    onError: (e: Error) => message.error(e.message),
  })

  const downloadOneLogoMut = useMutation({
    mutationFn: async (logoId: string) => {
      const { blob, filename } = await fetchAuthorizedBlob(`/stream-events/${streamId}/logos/${logoId}/file`)
      triggerBlobDownload(blob, filename)
    },
    onError: (e: Error) => message.error(e.message),
  })

  const stopMut = useMutation({
    mutationFn: async () => {
      await apiFetch(`/stream-events/${streamId}/days/${day}/broadcast/stop`, { method: 'POST' })
    },
    onSuccess: async () => {
      message.success('Эфир остановлен')
      await qc.invalidateQueries({ queryKey: ['stream', streamId] })
      await qc.invalidateQueries({ queryKey: ['mentions', streamId, day] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const mentionMut = useMutation({
    mutationFn: async (sessionId: string) => {
      await apiFetch(`/broadcast-sessions/${sessionId}/mentions`, { method: 'POST', body: '{}' })
    },
    onSuccess: async () => {
      message.success('Упоминание добавлено')
      await qc.invalidateQueries({ queryKey: ['mentions', streamId, day] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const adjustMut = useMutation({
    mutationFn: async (payload: { id: string; sec: number }) => {
      await apiFetch(`/sponsor-mentions/${payload.id}`, {
        method: 'PATCH',
        body: JSON.stringify({ adjusted_offset_sec: payload.sec }),
      })
    },
    onSuccess: async () => {
      message.success('Таймкод обновлён')
      setAdjustTarget(null)
      await qc.invalidateQueries({ queryKey: ['mentions', streamId, day] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const deleteMentionMut = useMutation({
    mutationFn: async (mentionId: string) => {
      await apiFetch(`/sponsor-mentions/${mentionId}`, { method: 'DELETE' })
    },
    onSuccess: async () => {
      message.success('Упоминание удалено')
      await qc.invalidateQueries({ queryKey: ['mentions', streamId, day] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const handleAddMention = () => {
    if (!activeSession) {
      message.warning('Сначала начните эфир')
      return
    }
    if (foreignLock) {
      message.warning('Этот день у другого оператора')
      return
    }
    if (!iOperateThisDay) {
      message.warning('Добавлять упоминания может назначенный на день оператор (или суперадмин)')
      return
    }
    mentionMut.mutate(activeSession.id)
  }

  const handleDeleteMention = (mention: SponsorMentionOut) => {
    modal.confirm({
      title: 'Удалить упоминание?',
      content: `Это действие удалит отметку ${mention.adjusted_timecode} и историю её корректировок. Продолжить?`,
      okText: 'Удалить',
      cancelText: 'Отмена',
      okButtonProps: { danger: true },
      onOk: async () => {
        await deleteMentionMut.mutateAsync(mention.id)
      },
    })
  }

  const handleStart = () => {
    if (foreignLock) {
      message.warning('Этот день назначен другому оператору')
      return
    }
    if (!dayIsAssigned) {
      message.warning(
        'Сначала назначьте день: «Взять в работу» — все свободные дни или отметьте нужные в списке',
      )
      return
    }
    if (user?.role === 'OPERATOR' && !iAmAssignedOperator) {
      message.warning('Чтобы вести эфир этого дня, возьмите его в работу на себя')
      return
    }
    if (restartBlocked) {
      message.warning(
        'Повторный старт недоступен: по этому дню уже был эфир дольше часа с таймкодами',
      )
      return
    }
    startMut.mutate()
  }

  const handleStop = () => {
    modal.confirm({
      title: 'Остановить эфир?',
      content: 'Новые упоминания для этого дня будут невозможны до нового старта.',
      okText: 'Остановить',
      cancelText: 'Отмена',
      onOk: async () => {
        await stopMut.mutateAsync()
      },
    })
  }

  const dayOptions =
    data?.days.map((d) => ({ label: `День ${d.day_index}`, value: d.day_index })) ??
    Array.from({ length: 5 }, (_, i) => ({ label: `День ${i + 1}`, value: i + 1 }))

  return (
    <AppLayout
      nav={
        <Space direction={isComfortable ? 'horizontal' : 'vertical'} size="small" style={{ width: '100%' }}>
          <Link to="/operator">
            <Button type="link" icon={<ArrowLeftOutlined />} style={{ paddingInline: 0 }}>
              К списку
            </Button>
          </Link>
          <Typography.Text type="secondary" style={{ fontSize: isComfortable ? undefined : 13 }}>
            Пульт оператора
          </Typography.Text>
        </Space>
      }
    >
      {!data ? (
        <Typography.Paragraph>Загрузка…</Typography.Paragraph>
      ) : (
        <Space direction="vertical" size={16} style={{ width: '100%' }}>
          <div>
            <Typography.Title level={3} style={{ marginBottom: 4 }}>
              {data.title}
            </Typography.Title>
            <Typography.Text type="secondary">
              Старт: {formatDateRu(data.start_date)} · {data.duration_days} дн. · Москва
              {wsViewers != null ? (
                <>
                  {' '}
                  · Сейчас с пультом: {wsViewers}
                </>
              ) : null}
            </Typography.Text>
          </div>

          <Card size="small" style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
            <Space direction={isComfortable ? 'horizontal' : 'vertical'} size="middle" style={{ width: '100%' }}>
              <Typography.Text>Статус (день {day}):</Typography.Text>
              {!dayIsAssigned ? (
                <Badge status="warning" text="День не назначен — «Начать эфир» недоступен, пока кто-то не возьмёт день" />
              ) : user?.role === 'SUPERADMIN' && superadminLockActionsBlocked ? (
                <Badge
                  status="default"
                  text="Дни у операторов — назначения меняет только оператор (суперадмин: без «Взять/Снять»)"
                />
              ) : user?.role === 'SUPERADMIN' ? (
                <Badge status="warning" text="Суперадмин — можно начать эфир по назначенному дню" />
              ) : foreignLock ? (
                <Badge status="error" text="Этот день у другого оператора" />
              ) : operatorForSelectedDay === user?.id ? (
                <Badge status="processing" text="Этот день у вас" />
              ) : freeDays.length > 0 ? (
                <Badge status="success" text="Есть свободные дни — возьмите в работу" />
              ) : (
                <Badge status="default" text="Все дни распределены" />
              )}
              <Space
                direction={isComfortable ? 'horizontal' : 'vertical'}
                style={{ width: isComfortable ? 'auto' : '100%' }}
                size="middle"
              >
                <Tooltip
                  title={
                    superadminLockActionsBlocked
                      ? 'Пока дни назначены операторам, взять дни в работу может только оператор'
                      : !canTakeLock
                        ? 'Нет свободных дней для назначения'
                        : undefined
                  }
                >
                  <span style={{ display: 'block', width: isComfortable ? 'auto' : '100%' }}>
                    <Button
                      type={canTakeLock ? 'primary' : 'default'}
                      disabled={!canTakeLock}
                      loading={lockMut.isPending}
                      onClick={() => {
                        if (freeDays.length === 0) {
                          message.info('Нет свободных дней для назначения')
                          return
                        }
                        setLockDayPick(freeDays)
                        setLockModalOpen(true)
                      }}
                      block={!isComfortable}
                      size="large"
                    >
                      Взять в работу
                    </Button>
                  </span>
                </Tooltip>
                <Tooltip
                  title={
                    superadminLockActionsBlocked
                      ? 'Пока дни назначены операторам, снять назначение может сам оператор'
                      : !iHaveLock && user?.role === 'OPERATOR'
                        ? 'Нет назначенных вам дней на этом мероприятии'
                        : undefined
                  }
                >
                  <span style={{ display: 'block', width: isComfortable ? 'auto' : '100%' }}>
                    <Button
                      danger
                      disabled={!iHaveLock}
                      loading={unlockMut.isPending}
                      onClick={() => unlockMut.mutate()}
                      block={!isComfortable}
                      size="large"
                    >
                      Снять с работы
                    </Button>
                  </span>
                </Tooltip>
              </Space>
            </Space>
            {data.day_assignments.length > 0 ? (
              <Typography.Paragraph type="secondary" style={{ marginBottom: 0, marginTop: 12, fontSize: 12 }}>
                Назначения:{' '}
                {[...data.day_assignments]
                  .sort((a, b) => a.day_index - b.day_index)
                  .map((a) => `день ${a.day_index} — ${a.operator_display_name || a.operator_email}`)
                  .join('; ')}
              </Typography.Paragraph>
            ) : null}
          </Card>

          <Card size="small" style={{ borderColor: '#e2e8f0', background: '#ffffff' }} title="Материалы и логотипы">
            <Space direction="vertical" size={12} style={{ width: '100%' }}>
              <div>
                <Typography.Text type="secondary" style={{ display: 'block', marginBottom: 6 }}>
                  Ссылка на материалы (контент)
                </Typography.Text>
                {data.content_url ? (
                  <Space wrap align="start">
                    <Tooltip title="Нажмите, чтобы скопировать в буфер обмена">
                      <Typography.Text
                        role="button"
                        tabIndex={0}
                        style={{
                          wordBreak: 'break-all',
                          cursor: 'pointer',
                          color: '#1677ff',
                          textDecoration: 'underline',
                        }}
                        onClick={() => void handleCopyLinkField(data.content_url as string)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault()
                            void handleCopyLinkField(data.content_url as string)
                          }
                        }}
                        aria-label="Скопировать ссылку на материалы"
                      >
                        {data.content_url}
                      </Typography.Text>
                    </Tooltip>
                    <Button
                      size="small"
                      icon={<CopyOutlined />}
                      onClick={() => void handleCopyLinkField(data.content_url as string)}
                    >
                      Копировать
                    </Button>
                    <Button
                      size="small"
                      icon={<LinkOutlined />}
                      onClick={() =>
                        window.open(data.content_url as string, '_blank', 'noopener,noreferrer')
                      }
                    >
                      Открыть
                    </Button>
                  </Space>
                ) : (
                  <Typography.Text type="secondary">Не указана</Typography.Text>
                )}
              </div>
              <Divider style={{ margin: '8px 0' }} />
              <div>
                <Space wrap style={{ marginBottom: 8 }}>
                  <Typography.Text strong>Логотипы</Typography.Text>
                  <Button
                    size="small"
                    icon={<FileZipOutlined />}
                    disabled={!(data.logos ?? []).length}
                    loading={downloadZipMut.isPending}
                    onClick={() => downloadZipMut.mutate()}
                  >
                    Скачать все (ZIP)
                  </Button>
                </Space>
                {!(data.logos ?? []).length ? (
                  <Typography.Text type="secondary">Нет прикреплённых логотипов</Typography.Text>
                ) : (
                  <Row gutter={[12, 12]}>
                    {(data.logos ?? []).map((lg) => (
                      <Col xs={12} sm={8} md={6} key={lg.id}>
                        <Card
                          size="small"
                          cover={
                            <img
                              alt={lg.filename_original}
                              src={lg.public_url}
                              style={{ maxHeight: 100, objectFit: 'contain', padding: 8 }}
                            />
                          }
                        >
                          <Typography.Text ellipsis style={{ fontSize: 12 }} title={lg.filename_original}>
                            {lg.filename_original}
                          </Typography.Text>
                          <Button
                            size="small"
                            block
                            style={{ marginTop: 8 }}
                            icon={<DownloadOutlined />}
                            loading={downloadOneLogoMut.isPending}
                            onClick={() => downloadOneLogoMut.mutate(lg.id)}
                          >
                            Скачать
                          </Button>
                        </Card>
                      </Col>
                    ))}
                  </Row>
                )}
              </div>
            </Space>
          </Card>

          <Modal
            title="Взять дни в работу"
            open={lockModalOpen}
            onCancel={() => setLockModalOpen(false)}
            okText="Подтвердить"
            onOk={() => {
              if (lockDayPick.length === 0) {
                message.warning('Выберите хотя бы один день')
                return Promise.reject(new Error('no days'))
              }
              return lockMut.mutateAsync(lockDayPick)
            }}
            confirmLoading={lockMut.isPending}
          >
            <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
              Можно взять сразу все свободные дни или только выбранные — так разные операторы могут делить турнир по
              дням.
            </Typography.Paragraph>
            <Space style={{ marginBottom: 12 }} wrap>
              <Button
                type="link"
                style={{ paddingInline: 0 }}
                onClick={() => setLockDayPick([...freeDays])}
                disabled={freeDays.length === 0}
              >
                Выбрать все свободные дни ({freeDays.length})
              </Button>
            </Space>
            <Checkbox.Group
              style={{ display: 'flex', flexDirection: 'column', gap: 8 }}
              options={freeDays.map((d) => ({ label: `День ${d}`, value: d }))}
              value={lockDayPick}
              onChange={(v) => setLockDayPick(v as number[])}
            />
          </Modal>

          <Row gutter={[16, 16]}>
            <Col xs={24} lg={10}>
              <Card
                title="Управление эфиром"
                style={{ borderColor: '#e2e8f0', background: '#ffffff' }}
                styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
              >
                <Space direction="vertical" size={16} style={{ width: '100%' }}>
                  <div>
                    <Typography.Text type="secondary">День</Typography.Text>
                    <Select
                      style={{ width: '100%', marginTop: 8 }}
                      value={day}
                      options={dayOptions.filter((o) => o.value <= data.duration_days)}
                      onChange={(v) => setDay(v)}
                    />
                    {selectedDayRow ? (
                      <>
                        <div
                          style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            marginTop: 14,
                            gap: 8,
                            flexWrap: 'wrap',
                          }}
                        >
                          <Typography.Text style={{ color: '#0f172a' }}>
                            Параметры дня {day}
                          </Typography.Text>
                          <Button
                            type="link"
                            size="small"
                            onClick={() => setStreamCredsVisible((v) => !v)}
                            aria-expanded={streamCredsVisible}
                            aria-label={streamCredsVisible ? 'Скрыть параметры трансляции' : 'Показать параметры трансляции'}
                          >
                            {streamCredsVisible ? 'Скрыть' : 'Показать'}
                          </Button>
                        </div>
                        {streamCredsVisible ? (
                          <div
                            style={{
                              marginTop: 10,
                              padding: 12,
                              borderRadius: 10,
                              border: '1px solid #e2e8f0',
                              background: '#f8fafc',
                            }}
                          >
                            {(
                              [
                                {
                                  label: 'Ссылка на трансляцию',
                                  value: selectedDayRow.stream_url,
                                },
                                {
                                  label: 'URL сервера трансляции',
                                  value: selectedDayRow.server_url,
                                },
                                {
                                  label: 'Ключ трансляции',
                                  value: selectedDayRow.stream_key,
                                },
                              ] as const
                            ).map((row, idx, arr) => (
                              <div
                                key={row.label}
                                style={{ marginBottom: idx < arr.length - 1 ? 12 : 0 }}
                              >
                                <Typography.Text type="secondary" style={{ fontSize: 12, display: 'block' }}>
                                  {row.label}
                                </Typography.Text>
                                <Tooltip
                                  title={row.value ? 'Нажмите, чтобы скопировать в буфер обмена' : undefined}
                                >
                                  <Typography.Paragraph
                                    role={row.value ? 'button' : undefined}
                                    tabIndex={row.value ? 0 : undefined}
                                    style={{
                                      marginBottom: 0,
                                      wordBreak: 'break-all',
                                      cursor: row.value ? 'pointer' : 'default',
                                      color: row.value ? '#1677ff' : undefined,
                                      textDecoration: row.value ? 'underline' : undefined,
                                    }}
                                    onClick={() => row.value && void handleCopyLinkField(row.value)}
                                    onKeyDown={(e) => {
                                      if (!row.value) {
                                        return
                                      }
                                      if (e.key === 'Enter' || e.key === ' ') {
                                        e.preventDefault()
                                        void handleCopyLinkField(row.value)
                                      }
                                    }}
                                    aria-label={
                                      row.value ? `Скопировать: ${row.label}` : undefined
                                    }
                                  >
                                    {row.value || '—'}
                                  </Typography.Paragraph>
                                </Tooltip>
                              </div>
                            ))}
                          </div>
                        ) : null}
                      </>
                    ) : null}
                  </div>
                  <Divider style={{ margin: '4px 0' }} />
                  <div>
                    <Typography.Text strong style={{ display: 'block', marginBottom: 8 }}>
                      Чек-лист перед эфиром · день {day}
                    </Typography.Text>
                    <Space direction="vertical" size="small" style={{ width: '100%' }}>
                      <Checkbox
                        checked={checklistQuery.data?.picture_exposure_ok ?? false}
                        disabled={checklistMut.isPending || checklistQuery.isLoading}
                        onChange={(e) => checklistMut.mutate({ picture_exposure_ok: e.target.checked })}
                      >
                        Картинка, баланс белого и экспозиция (чтобы не в норме, но и не слепило)
                      </Checkbox>
                      <Checkbox
                        checked={checklistQuery.data?.judges_stream_ok ?? false}
                        disabled={checklistMut.isPending || checklistQuery.isLoading}
                        onChange={(e) => checklistMut.mutate({ judges_stream_ok: e.target.checked })}
                      >
                        Поток судьям
                      </Checkbox>
                      <Checkbox
                        checked={checklistQuery.data?.splitter_socket_ok ?? false}
                        disabled={checklistMut.isPending || checklistQuery.isLoading}
                        onChange={(e) => checklistMut.mutate({ splitter_socket_ok: e.target.checked })}
                      >
                        Сплиттер и сокет
                      </Checkbox>
                      <Checkbox
                        checked={checklistQuery.data?.key_stream_started_ok ?? false}
                        disabled={checklistMut.isPending || checklistQuery.isLoading}
                        onChange={(e) => checklistMut.mutate({ key_stream_started_ok: e.target.checked })}
                      >
                        Ключ скопирован, поток запущен
                      </Checkbox>
                      <Checkbox
                        checked={checklistQuery.data?.kick_ok ?? false}
                        disabled={checklistMut.isPending || checklistQuery.isLoading}
                        onChange={(e) => checklistMut.mutate({ kick_ok: e.target.checked })}
                      >
                        Кик стоит, у тебя тоже
                      </Checkbox>
                      <Checkbox
                        checked={checklistQuery.data?.mentions_four_ok ?? false}
                        disabled={checklistMut.isPending || checklistQuery.isLoading}
                        onChange={(e) => checklistMut.mutate({ mentions_four_ok: e.target.checked })}
                      >
                        4 упоминания
                      </Checkbox>
                    </Space>
                  </div>
                  <div
                    style={{
                      padding: 16,
                      borderRadius: 12,
                      border: '1px solid #e2e8f0',
                      background: '#f8fafc',
                      textAlign: 'center',
                    }}
                  >
                    <Typography.Text type="secondary">Таймер эфира</Typography.Text>
                    <Typography.Title level={2} style={{ margin: '8px 0 0', letterSpacing: 2 }}>
                      {activeSession ? formatElapsed(elapsedSec) : '— : — : —'}
                    </Typography.Title>
                  </div>
                  <Tooltip
                    title={
                      restartBlocked
                        ? 'Этот день уже был в эфире более часа с таймкодами — новый старт недоступен'
                        : !dayIsAssigned
                          ? 'Сначала нажмите «Взять в работу» и назначьте этот день (или весь турнир)'
                          : user?.role === 'OPERATOR' && !iAmAssignedOperator
                            ? 'Этот день у другого оператора — возьмите свободный день или согласуйте переназначение'
                            : undefined
                    }
                  >
                    <span style={{ display: 'block', width: '100%' }}>
                      <Button
                        type="primary"
                        size="large"
                        block
                        icon={<PlayCircleOutlined />}
                        disabled={Boolean(
                          activeSession || foreignLock || !canStartBroadcast || restartBlocked,
                        )}
                        loading={startMut.isPending}
                        onClick={() => handleStart()}
                      >
                        Начать эфир
                      </Button>
                    </span>
                  </Tooltip>
                  {restartBlocked ? (
                    <Typography.Text type="secondary" style={{ fontSize: 12, display: 'block', marginTop: 4 }}>
                      Повторный старт отключён: был завершённый эфир &gt; 1 ч с упоминаниями.
                    </Typography.Text>
                  ) : null}
                  <Button
                    size="large"
                    block
                    danger
                    icon={<StopOutlined />}
                    disabled={!activeSession || foreignLock}
                    loading={stopMut.isPending}
                    onClick={() => handleStop()}
                  >
                    Остановить эфир
                  </Button>
                  {activeSession ? (
                    <BroadcastActualStartPanel
                      streamId={streamId}
                      dayIndex={day}
                      startedAtIso={activeSession.started_at}
                      disabled={!canRealignBroadcast}
                    />
                  ) : null}
                  {!activeSession && canShowEndedRealignPanel && latestEndedForSelectedDay ? (
                    <BroadcastActualStartPanel
                      streamId={streamId}
                      dayIndex={day}
                      startedAtIso={latestEndedForSelectedDay.started_at}
                    />
                  ) : null}
                  <Button
                    type="default"
                    size="large"
                    block
                    icon={<PlusOutlined />}
                    disabled={!activeSession || foreignLock || !iOperateThisDay}
                    loading={mentionMut.isPending}
                    onClick={() => handleAddMention()}
                  >
                    Добавить упоминание
                  </Button>
                  <div
                    style={{
                      padding: 12,
                      borderRadius: 10,
                      border: '1px solid #e2e8f0',
                      background: '#f8fafc',
                    }}
                  >
                    <Typography.Text strong style={{ display: 'block', marginBottom: 10 }}>
                      План: 4 упоминания за эфир
                    </Typography.Text>
                    <Typography.Paragraph type="secondary" style={{ fontSize: 12, marginBottom: 10 }}>
                      Добавляйте по порядку: начало → две середины → конец. Ниже отмечается, какие из четырёх шагов уже
                      есть.
                    </Typography.Paragraph>
                    {MENTION_SLOT_LABELS.map((label, i) => {
                      const done = Boolean(orderedMentionsForPlan[i])
                      return (
                        <div
                          key={label}
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            gap: 8,
                            padding: '8px 0',
                            borderTop: i === 0 ? undefined : '1px solid #e2e8f0',
                          }}
                        >
                          <Typography.Text style={{ fontSize: 13 }}>
                            {i + 1}. {label}
                          </Typography.Text>
                          {done ? (
                            <CheckOutlined style={{ color: '#52c41a', fontSize: 16 }} aria-label="Отмечено" />
                          ) : (
                            <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                              нет
                            </Typography.Text>
                          )}
                        </div>
                      )
                    })}
                  </div>
                </Space>
              </Card>
            </Col>
            <Col xs={24} lg={14}>
              <Card
                title="Упоминания"
                style={{ borderColor: '#e2e8f0', background: '#ffffff' }}
                styles={{ header: { borderBottom: '1px solid #e2e8f0' } }}
              >
                <List
                  itemLayout={isComfortable ? 'horizontal' : 'vertical'}
                  loading={mentionsQuery.isLoading}
                  dataSource={mentionsQuery.data ?? []}
                  locale={{ emptyText: 'Пока нет упоминаний' }}
                  renderItem={(item) => (
                    <List.Item
                      actions={[
                        <Button
                          key="adj"
                          type={isComfortable ? 'link' : 'default'}
                          disabled={!canEditMentionsForSelectedDay}
                          block={!isComfortable}
                          size={isComfortable ? 'middle' : 'large'}
                          onClick={() => {
                            setAdjustTarget(item)
                            const t = Math.max(0, item.adjusted_offset_sec)
                            setAdjustMinutes(Math.floor(t / 60))
                            setAdjustSecondsPart(t % 60)
                          }}
                        >
                          Корректировка
                        </Button>,
                        <Button
                          key="delete"
                          danger
                          icon={<DeleteOutlined />}
                          type={isComfortable ? 'link' : 'default'}
                          disabled={!canEditMentionsForSelectedDay || deleteMentionMut.isPending}
                          block={!isComfortable}
                          size={isComfortable ? 'middle' : 'large'}
                          onClick={() => handleDeleteMention(item)}
                        >
                          Удалить
                        </Button>,
                      ]}
                    >
                      <List.Item.Meta
                        title={
                          <Space>
                            <Typography.Text strong>{item.adjusted_timecode}</Typography.Text>
                            {item.is_adjusted ? <Badge status="warning" text="Скорректировано" /> : null}
                          </Space>
                        }
                        description={
                          <Space direction="vertical" size={0}>
                            <Typography.Text type="secondary">
                              Время: {item.absolute_moscow_adjusted}
                            </Typography.Text>
                            <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                              Таймкод трансляции: {item.original_timecode}
                            </Typography.Text>
                            {item.adjustments && item.adjustments.length > 0 ? (
                              <div style={{ marginTop: 8 }}>
                                <Typography.Text
                                  type="secondary"
                                  style={{ fontSize: 12, display: 'block', marginBottom: 4 }}
                                >
                                  Лог
                                </Typography.Text>
                                {item.adjustments.map((a) => (
                                  <Typography.Text
                                    key={a.id}
                                    type="secondary"
                                    style={{ fontSize: 12, display: 'block' }}
                                  >
                                    Запись: {formatDateTimeRu(a.created_at)} · {formatElapsed(a.previous_adjusted_sec)}{' '}
                                    → {formatElapsed(a.new_adjusted_sec)}
                                  </Typography.Text>
                                ))}
                              </div>
                            ) : null}
                          </Space>
                        }
                      />
                    </List.Item>
                  )}
                />
              </Card>
            </Col>
          </Row>
        </Space>
      )}

      <Modal
        title="Корректировка таймкода"
        open={Boolean(adjustTarget)}
        okText="Сохранить"
        cancelText="Отмена"
        confirmLoading={adjustMut.isPending}
        onCancel={() => setAdjustTarget(null)}
        onOk={async () => {
          if (!adjustTarget) {
            return
          }
          await adjustMut.mutateAsync({ id: adjustTarget.id, sec: adjustTotalSec })
        }}
      >
        <Typography.Paragraph type="secondary" style={{ marginBottom: 12 }}>
          Смещение от старта эфира: введите минуты и секунды (секунды — от 0 до 59).
        </Typography.Paragraph>
        <div
          style={{
            border: '1px solid #e2e8f0',
            borderRadius: 10,
            overflow: 'hidden',
            background: '#f8fafc',
          }}
        >
          <Row
            wrap={false}
            style={{
              borderBottom: '1px solid #e2e8f0',
              background: '#f1f5f9',
              color: '#64748b',
              fontSize: 13,
              fontWeight: 500,
            }}
          >
            <Col flex="1" style={{ padding: '10px 12px' }}>
              Минуты
            </Col>
            <Col
              flex="1"
              style={{
                padding: '10px 12px',
                borderLeft: '1px solid #e2e8f0',
              }}
            >
              Секунды
            </Col>
          </Row>
          <Row wrap={false}>
            <Col flex="1" style={{ padding: 12 }}>
              <InputNumber
                min={0}
                max={99999}
                step={1}
                controls
                size="large"
                style={{ width: '100%' }}
                value={adjustMinutes}
                onChange={(v) => setAdjustMinutes(Math.max(0, Math.floor(Number(v ?? 0))))}
                aria-label="Минуты от старта эфира"
              />
            </Col>
            <Col
              flex="1"
              style={{
                padding: 12,
                borderLeft: '1px solid #e2e8f0',
              }}
            >
              <InputNumber
                min={0}
                max={59}
                step={1}
                controls
                size="large"
                style={{ width: '100%' }}
                value={adjustSecondsPart}
                onChange={(v) => setAdjustSecondsPart(Math.min(59, Math.max(0, Math.floor(Number(v ?? 0)))))}
                aria-label="Секунды от старта эфира, 0–59"
              />
            </Col>
          </Row>
        </div>
        <Typography.Paragraph type="secondary" style={{ marginTop: 14, marginBottom: 0 }}>
          Итого от старта эфира:{' '}
          <Typography.Text strong style={{ color: '#0f172a' }}>
            {formatElapsed(adjustTotalSec)}
          </Typography.Text>
          <Typography.Text type="secondary" style={{ fontSize: 12, marginLeft: 8 }}>
            ({adjustTotalSec} с)
          </Typography.Text>
        </Typography.Paragraph>
      </Modal>

      {showIdleReminder ? (
        <div
          role="alertdialog"
          aria-modal="true"
          aria-labelledby="idle-reminder-title"
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 1100,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 24,
            paddingTop: 'max(24px, env(safe-area-inset-top))',
            paddingBottom: 'max(24px, env(safe-area-inset-bottom))',
            background: 'rgba(7, 11, 16, 0.97)',
            backdropFilter: 'blur(6px)',
          }}
        >
          <div
            style={{
              maxWidth: 440,
              width: '100%',
              textAlign: 'center',
              background: '#ffffff',
              borderRadius: 10,
              padding: '28px 24px',
              boxShadow: '0 20px 48px rgba(0, 0, 0, 0.35)',
            }}
          >
            <Typography.Title level={3} id="idle-reminder-title" style={{ color: '#0f172a', marginTop: 0 }}>
              Не забудьте про напоминалки
            </Typography.Title>
            <Typography.Paragraph type="secondary" style={{ marginBottom: 24, fontSize: 15 }}>
              Прошло больше двух часов с последнего упоминания (или с того момента, как вы закрыли это сообщение).
              Проверьте план из четырёх отметок и спонсорские вставки.
            </Typography.Paragraph>
            <Button type="primary" size="large" block onClick={handleIdleReminderDismiss}>
              Понятно, скрыть
            </Button>
          </div>
        </div>
      ) : null}
    </AppLayout>
  )
}

```


---

## Исходный код: `frontend/src/pages/OperatorHomePage.tsx`

> 130 строк, 5,041 байт

```tsx
import { PlayCircleOutlined } from '@ant-design/icons'
import { App as AntApp, Card, Col, Empty, Row, Space, Tag, Typography } from 'antd'
import { useQuery } from '@tanstack/react-query'
import React from 'react'
import { Link } from 'react-router-dom'

import type { StreamEventListOut } from '@/api/types'
import { apiFetch } from '@/api/client'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateRu } from '@/utils/datetime'

const endedDaysStatusLabel = (dayIndices: number[] | undefined) => {
  const list = (dayIndices ?? []).filter((d) => Number.isInteger(d)).sort((a, b) => a - b)
  if (list.length === 0) {
    return 'Есть завершенные эфиры'
  }
  if (list.length === 1) {
    return `Завершен день ${list[0]}`
  }
  return `Завершены дни ${list.join(', ')}`
}

export const OperatorHomePage: React.FC = () => {
  const { message } = AntApp.useApp()

  const { data, isLoading } = useQuery({
    queryKey: ['streams'],
    queryFn: async () => (await apiFetch('/stream-events')) as StreamEventListOut[],
  })

  const handleCardClick = (ev: StreamEventListOut) => {
    if (!ev.has_slot_for_me) {
      message.warning('Все дни этого мероприятия уже распределены между операторами')
    }
  }

  const today = new Date()
  const todayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate())
  const rangeStart = new Date(todayStart)
  rangeStart.setDate(rangeStart.getDate() - 3)
  const rangeEnd = new Date(todayStart)
  rangeEnd.setDate(rangeEnd.getDate() + 7)
  rangeEnd.setHours(23, 59, 59, 999)

  const visibleEvents = (data ?? []).filter((ev) => {
    const eventStart = new Date(`${ev.start_date}T00:00:00`)
    const eventEnd = new Date(eventStart)
    eventEnd.setDate(eventEnd.getDate() + ev.duration_days - 1)
    eventEnd.setHours(23, 59, 59, 999)
    return eventEnd >= rangeStart && eventStart <= rangeEnd
  })

  return (
    <AppLayout
      nav={
        <Typography.Text type="secondary" style={{ fontSize: 13 }}>
          Оператор
        </Typography.Text>
      }
    >
      <Typography.Title level={3} style={{ marginTop: 0 }}>
        Мероприятия
      </Typography.Title>
      <Typography.Paragraph type="secondary">
        Выберите мероприятие. Можно взять свободные дни турнира; если все дни заняты — карточка приглушена.
      </Typography.Paragraph>
      {!isLoading && visibleEvents.length === 0 ? (
        <Empty description="Нет мероприятий" />
      ) : (
        <Row gutter={[16, 16]}>
          {visibleEvents.map((ev) => {
            const blocked = ev.has_slot_for_me === false
            return (
              <Col xs={24} md={12} lg={8} key={ev.id}>
                <Link
                  to={`/operator/${ev.id}`}
                  onClick={(e) => {
                    if (blocked) {
                      e.preventDefault()
                      handleCardClick(ev)
                    }
                  }}
                >
                  <Card
                    hoverable={!blocked}
                    loading={isLoading}
                    style={{
                      opacity: blocked ? 0.55 : 1,
                      borderColor: '#e2e8f0',
                      background: '#ffffff',
                    }}
                  >
                    <Space direction="vertical" size={8} style={{ width: '100%' }}>
                      <Typography.Title level={5} style={{ margin: 0, color: '#0f172a' }}>
                        {ev.title}
                      </Typography.Title>
                      <Typography.Text type="secondary">
                        Старт: {formatDateRu(ev.start_date)} · {ev.duration_days} дн.
                      </Typography.Text>
                      <Space wrap>
                        {ev.has_active_broadcast ? (
                          <Tag color="green">Эфир</Tag>
                        ) : ev.has_ended_broadcast ? (
                          <Tag color="orange">{endedDaysStatusLabel(ev.ended_day_indices)}</Tag>
                        ) : (
                          <Tag>Нет эфира</Tag>
                        )}
                        {blocked ? (
                          <Tag color="red">Нет свободных дней</Tag>
                        ) : ev.assignment_summary ? (
                          <Tag color="blue">{ev.assignment_summary}</Tag>
                        ) : (
                          <Tag>Свободные дни</Tag>
                        )}
                      </Space>
                      <Typography.Link>
                        <PlayCircleOutlined /> Открыть пульт
                      </Typography.Link>
                    </Space>
                  </Card>
                </Link>
              </Col>
            )
          })}
        </Row>
      )}
    </AppLayout>
  )
}

```


---

## Исходный код: `frontend/src/pages/ProfilePage.tsx`

> 367 строк, 12,807 байт

```tsx
import { HistoryOutlined, SafetyOutlined, UserOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Avatar,
  Button,
  Card,
  Form,
  Input,
  Space,
  Table,
  Tabs,
  Tag,
  Typography,
  Upload,
} from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'

import type { AuditLogOut, SessionOut } from '@/api/types'
import {
  changePasswordRequest,
  getMyActivityPage,
  listSessionsRequest,
  patchProfileRequest,
  revokeSessionRequest,
  uploadAvatarRequest,
} from '@/api/client'
import { useAuth } from '@/auth/AuthContext'
import { AppLayout } from '@/layouts/AppLayout'
import { formatDateTimeRu } from '@/utils/datetime'
import { normalizeRuMobilePhone } from '@/utils/normalizeRuMobilePhone'
import { userDisplayName } from '@/utils/userDisplay'

export const ProfilePage: React.FC = () => {
  const { message } = AntApp.useApp()
  const { user, refreshMe } = useAuth()
  const qc = useQueryClient()
  const [profileForm] = Form.useForm()
  const [passwordForm] = Form.useForm()
  const [activityPage, setActivityPage] = React.useState(1)

  useEffect(() => {
    if (user) {
      profileForm.setFieldsValue({
        first_name: user.first_name,
        last_name: user.last_name,
        phone: user.phone ?? '',
        telegram: user.telegram ?? '',
      })
    }
  }, [user, profileForm])

  const profileMut = useMutation({
    mutationFn: patchProfileRequest,
    onSuccess: async () => {
      message.success('Профиль сохранён')
      await refreshMe()
      await qc.invalidateQueries({ queryKey: ['auth', 'me'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const avatarMut = useMutation({
    mutationFn: uploadAvatarRequest,
    onSuccess: async () => {
      message.success('Аватар обновлён')
      await refreshMe()
    },
    onError: (e: Error) => message.error(e.message),
  })

  const passwordMut = useMutation({
    mutationFn: (v: { current_password: string; new_password: string }) =>
      changePasswordRequest(v.current_password, v.new_password),
    onSuccess: async () => {
      message.success('Пароль изменён. Другие сессии завершены.')
      passwordForm.resetFields()
      void qc.invalidateQueries({ queryKey: ['sessions'] })
      await refreshMe()
    },
    onError: (e: Error) => message.error(e.message),
  })

  const { data: sessions, refetch: refetchSessions } = useQuery({
    queryKey: ['sessions'],
    queryFn: listSessionsRequest,
  })

  const revokeMut = useMutation({
    mutationFn: revokeSessionRequest,
    onSuccess: async () => {
      message.success('Сессия завершена')
      await refetchSessions()
    },
    onError: (e: Error) => message.error(e.message),
  })

  const { data: activityData, isLoading: activityLoading } = useQuery({
    queryKey: ['my-activity', activityPage],
    queryFn: () => getMyActivityPage(activityPage, 15),
  })

  const avatarSrc =
    user?.avatar_url && user.avatar_url.length > 0
      ? user.avatar_url.startsWith('http')
        ? user.avatar_url
        : user.avatar_url
      : undefined

  const sessionColumns: ColumnsType<SessionOut> = [
    {
      title: 'Создана',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (v: string) => formatDateTimeRu(v),
    },
    {
      title: 'До',
      dataIndex: 'expires_at',
      key: 'expires_at',
      width: 160,
      render: (v: string) => formatDateTimeRu(v),
    },
    {
      title: 'Клиент',
      dataIndex: 'user_agent',
      key: 'user_agent',
      ellipsis: true,
      render: (v: string | null) => v || '—',
    },
    {
      title: '',
      key: 'cur',
      width: 100,
      render: (_, r) => (r.is_current ? <Tag color="blue">Текущая</Tag> : null),
    },
    {
      title: '',
      key: 'act',
      width: 120,
      render: (_, r) =>
        r.is_current ? null : (
          <Button
            size="small"
            danger
            loading={revokeMut.isPending}
            onClick={() => void revokeMut.mutateAsync(r.id)}
          >
            Завершить
          </Button>
        ),
    },
  ]

  const activityColumns: ColumnsType<AuditLogOut> = [
    {
      title: 'Время',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 160,
      render: (v: string) => formatDateTimeRu(v),
    },
    { title: 'Действие', dataIndex: 'action_type', key: 'action_type', width: 140 },
    { title: 'Сущность', dataIndex: 'entity_type', key: 'entity_type', width: 140 },
    {
      title: 'Детали',
      key: 'after',
      ellipsis: true,
      render: (_, r) => (
        <Typography.Text type="secondary" style={{ fontSize: 12 }}>
          {r.payload_after ? JSON.stringify(r.payload_after).slice(0, 120) : '—'}
        </Typography.Text>
      ),
    },
  ]

  return (
    <AppLayout
      nav={
        <Space>
          <Link to="/dashboard" style={{ color: '#0284c7', fontSize: 13 }}>
            ← На дашборд
          </Link>
          <Typography.Text type="secondary" style={{ fontSize: 13 }}>
            Профиль
          </Typography.Text>
        </Space>
      }
    >
      <Typography.Title level={3} style={{ marginTop: 0 }}>
        {user ? userDisplayName(user) : 'Профиль'}
      </Typography.Title>

      <Tabs
        defaultActiveKey="info"
        items={[
          {
            key: 'info',
            label: (
              <span>
                <UserOutlined /> Контакты и аватар
              </span>
            ),
            children: (
              <Card style={{ borderColor: '#e2e8f0', background: '#ffffff', maxWidth: 560 }}>
                <Space align="start" size={24} wrap>
                  <Avatar size={96} src={avatarSrc} style={{ background: '#e2e8f0' }}>
                    {user ? (user.last_name || user.email).slice(0, 1).toUpperCase() : '?'}
                  </Avatar>
                  <div>
                    <Upload
                      accept="image/jpeg,image/png,image/webp"
                      showUploadList={false}
                      beforeUpload={(file) => {
                        void avatarMut.mutateAsync(file as File)
                        return false
                      }}
                    >
                      <Button loading={avatarMut.isPending}>Загрузить аватар</Button>
                    </Upload>
                    <Typography.Paragraph type="secondary" style={{ marginTop: 8, marginBottom: 0, fontSize: 12 }}>
                      JPEG, PNG или WebP, до 2 МБ.
                    </Typography.Paragraph>
                  </div>
                </Space>
                <Form
                  form={profileForm}
                  layout="vertical"
                  style={{ marginTop: 24 }}
                  onFinish={(v) => void profileMut.mutateAsync(v)}
                >
                  <Form.Item name="last_name" label="Фамилия" rules={[{ required: true, message: 'Обязательно' }]}>
                    <Input />
                  </Form.Item>
                  <Form.Item name="first_name" label="Имя" rules={[{ required: true, message: 'Обязательно' }]}>
                    <Input />
                  </Form.Item>
                  <Form.Item
                    name="phone"
                    label="Мобильный телефон (Россия)"
                    extra="Можно 7906… или 8906… — сохранится как +7 (906) …"
                    rules={[
                      {
                        validator: async (_, value: string) => {
                          const t = (value ?? '').trim()
                          if (!t) {
                            return Promise.resolve()
                          }
                          try {
                            normalizeRuMobilePhone(t)
                            return Promise.resolve()
                          } catch {
                            return Promise.reject(new Error('Некорректный российский мобильный номер'))
                          }
                        },
                      },
                    ]}
                  >
                    <Input placeholder="79060943936" autoComplete="tel" inputMode="tel" />
                  </Form.Item>
                  <Form.Item name="telegram" label="Telegram">
                    <Input placeholder="@username" />
                  </Form.Item>
                  <Button type="primary" htmlType="submit" loading={profileMut.isPending}>
                    Сохранить
                  </Button>
                </Form>
              </Card>
            ),
          },
          {
            key: 'security',
            label: (
              <span>
                <SafetyOutlined /> Пароль и сессии
              </span>
            ),
            children: (
              <Space direction="vertical" size={24} style={{ width: '100%' }}>
                <Card title="Смена пароля" style={{ borderColor: '#e2e8f0', background: '#ffffff', maxWidth: 480 }}>
                  <Form
                    form={passwordForm}
                    layout="vertical"
                    onFinish={(v: { current_password: string; new_password: string; new_password2: string }) => {
                      if (v.new_password !== v.new_password2) {
                        message.error('Новые пароли не совпадают')
                        return
                      }
                      void passwordMut.mutateAsync({
                        current_password: v.current_password,
                        new_password: v.new_password,
                      })
                    }}
                  >
                    <Form.Item
                      name="current_password"
                      label="Текущий пароль"
                      rules={[{ required: true, message: 'Обязательно' }]}
                    >
                      <Input.Password autoComplete="current-password" />
                    </Form.Item>
                    <Form.Item
                      name="new_password"
                      label="Новый пароль"
                      rules={[{ required: true }, { min: 8, message: 'Не короче 8 символов' }]}
                    >
                      <Input.Password autoComplete="new-password" />
                    </Form.Item>
                    <Form.Item
                      name="new_password2"
                      label="Повтор нового пароля"
                      rules={[{ required: true, message: 'Обязательно' }]}
                    >
                      <Input.Password autoComplete="new-password" />
                    </Form.Item>
                    <Button type="primary" htmlType="submit" loading={passwordMut.isPending}>
                      Сменить пароль
                    </Button>
                  </Form>
                </Card>
                <Card title="Активные сессии (по refresh-токену)" style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
                  <Table
                    rowKey="id"
                    size="small"
                    columns={sessionColumns}
                    dataSource={sessions ?? []}
                    pagination={false}
                    scroll={{ x: 720 }}
                  />
                </Card>
              </Space>
            ),
          },
          {
            key: 'activity',
            label: (
              <span>
                <HistoryOutlined /> История активности
              </span>
            ),
            children: (
              <Card style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
                <Table
                  rowKey="id"
                  loading={activityLoading}
                  columns={activityColumns}
                  dataSource={activityData?.items ?? []}
                  pagination={{
                    current: activityPage,
                    pageSize: activityData?.page_size ?? 15,
                    total: activityData?.total ?? 0,
                    onChange: (p) => setActivityPage(p),
                    showSizeChanger: false,
                  }}
                  scroll={{ x: 900 }}
                />
              </Card>
            ),
          },
        ]}
      />
    </AppLayout>
  )
}

```


---

## Исходный код: `frontend/src/pages/ResetPasswordPage.tsx`

> 160 строк, 5,749 байт

```tsx
import { LockOutlined, SafetyOutlined } from '@ant-design/icons'
import { App as AntApp, Button, Card, Form, Input, Spin, Typography } from 'antd'
import React, { useEffect, useState } from 'react'
import { Link, Navigate, useNavigate, useSearchParams } from 'react-router-dom'

import { useAuth } from '@/auth/AuthContext'
import { resetPasswordRequest, validatePasswordResetTokenRequest } from '@/api/client'
import { BrandLogo } from '@/components/BrandLogo'

export const ResetPasswordPage: React.FC = () => {
  const { user } = useAuth()
  const { message } = AntApp.useApp()
  const nav = useNavigate()
  const [searchParams] = useSearchParams()
  const token = (searchParams.get('token') ?? '').trim()
  const [form] = Form.useForm()
  const [checking, setChecking] = useState(true)
  const [tokenOk, setTokenOk] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  if (user) {
    return <Navigate to="/" replace />
  }

  useEffect(() => {
    if (!token) {
      setTokenOk(false)
      setChecking(false)
      return
    }
    let cancelled = false
    const run = async () => {
      setChecking(true)
      try {
        const { ok } = await validatePasswordResetTokenRequest(token)
        if (!cancelled) {
          setTokenOk(ok)
        }
      } catch {
        if (!cancelled) {
          setTokenOk(false)
        }
      } finally {
        if (!cancelled) {
          setChecking(false)
        }
      }
    }
    void run()
    return () => {
      cancelled = true
    }
  }, [token])

  const handleFinish = async (v: { new_password: string; new_password2: string }) => {
    setSubmitting(true)
    try {
      await resetPasswordRequest({
        token,
        new_password: v.new_password,
        new_password_confirm: v.new_password2,
      })
      message.success('Пароль обновлён. Войдите с новым паролем.')
      nav('/login', { replace: true })
    } catch (e) {
      message.error(e instanceof Error ? e.message : 'Не удалось сменить пароль')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div
      style={{
        minHeight: '100dvh',
        padding: 24,
        paddingTop: 'max(24px, env(safe-area-inset-top, 0px))',
        background:
          'radial-gradient(1200px 600px at 20% 0%, rgba(61,126,255,0.18), transparent), #f5f7fa',
      }}
    >
      <div style={{ maxWidth: 480, margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 20 }}>
          <BrandLogo height={36} />
        </div>
        <Card style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
          <Typography.Title
            level={4}
            style={{ marginTop: 0, color: '#0f172a', display: 'flex', alignItems: 'center', gap: 8 }}
          >
            <SafetyOutlined /> Новый пароль
          </Typography.Title>
          {checking ? (
            <div style={{ display: 'grid', placeItems: 'center', padding: 32 }}>
              <Spin size="large" />
            </div>
          ) : !token || !tokenOk ? (
            <>
              <Typography.Paragraph type="secondary">
                Ссылка недействительна или срок её действия истёк. Запросите новую на странице «Забыли пароль?».
              </Typography.Paragraph>
              <Link to="/forgot-password">
                <Button type="primary" block size="large">
                  Запросить ссылку снова
                </Button>
              </Link>
              <div style={{ marginTop: 12, textAlign: 'center' }}>
                <Link to="/login">Вход</Link>
              </div>
            </>
          ) : (
            <>
              <Typography.Paragraph type="secondary" style={{ marginBottom: 20 }}>
                Придумайте новый пароль и введите его дважды.
              </Typography.Paragraph>
              <Form form={form} layout="vertical" onFinish={handleFinish}>
                <Form.Item name="new_password" label="Новый пароль" rules={[{ required: true, min: 8 }]}>
                  <Input.Password
                    prefix={<LockOutlined />}
                    autoComplete="new-password"
                    size="large"
                  />
                </Form.Item>
                <Form.Item
                  name="new_password2"
                  label="Повторите пароль"
                  dependencies={['new_password']}
                  rules={[
                    { required: true },
                    ({ getFieldValue }) => ({
                      validator(_, value) {
                        if (!value || getFieldValue('new_password') === value) {
                          return Promise.resolve()
                        }
                        return Promise.reject(new Error('Пароли не совпадают'))
                      },
                    }),
                  ]}
                >
                  <Input.Password
                    prefix={<LockOutlined />}
                    autoComplete="new-password"
                    size="large"
                  />
                </Form.Item>
                <Button type="primary" htmlType="submit" size="large" block loading={submitting}>
                  Сохранить пароль
                </Button>
                <div style={{ marginTop: 12, textAlign: 'center' }}>
                  <Link to="/login">Назад ко входу</Link>
                </div>
              </Form>
            </>
          )}
        </Card>
      </div>
    </div>
  )
}

```


---

## Исходный код: `frontend/src/pages/RoleHome.tsx`

> 13 строк, 299 байт

```tsx
import React from 'react'
import { Navigate } from 'react-router-dom'

import { useAuth } from '@/auth/AuthContext'

export const RoleHome: React.FC = () => {
  const { user } = useAuth()
  if (!user) {
    return <Navigate to="/login" replace />
  }
  return <Navigate to="/dashboard" replace />
}

```


---

## Исходный код: `frontend/src/pages/SuperadminPage.tsx`

> 514 строк, 16,851 байт

```tsx
import { BarChartOutlined, DeleteOutlined, DownloadOutlined, PlusOutlined } from '@ant-design/icons'
import {
  App as AntApp,
  Button,
  Card,
  Form,
  Grid,
  Input,
  Modal,
  Select,
  Space,
  Switch,
  Table,
  Tabs,
  Typography,
} from 'antd'
import type { ColumnsType } from 'antd/es/table'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import React, { useEffect, useState } from 'react'

import type { AuditLogOut, UserCreatedOut, UserOut } from '@/api/types'
import { apiFetch, getAccessToken } from '@/api/client'
import { OperatorStatsPanel } from '@/components/OperatorStatsPanel'
import { AppLayout } from '@/layouts/AppLayout'
import { auditActionLabel, auditEntityLabel, formatAuditPayloadRu } from '@/utils/auditLabels'
import { formatDateTimeRu } from '@/utils/datetime'
import { userDisplayName } from '@/utils/userDisplay'

type AuditPage = {
  items: AuditLogOut[]
  total: number
  page: number
  page_size: number
}

type AnalyticsSummary = {
  by_event: { event_name: string; count: number }[]
}

const API_BASE = import.meta.env.VITE_API_BASE ?? '/api/v1'

export const SuperadminPage: React.FC = () => {
  const { message, modal } = AntApp.useApp()
  const qc = useQueryClient()
  const screens = Grid.useBreakpoint()
  const isNarrow = !screens.md
  const [userOpen, setUserOpen] = useState(false)
  const [editUser, setEditUser] = useState<UserOut | null>(null)
  const [createForm] = Form.useForm()
  const [editForm] = Form.useForm()
  const [auditPage, setAuditPage] = useState(1)

  const usersQuery = useQuery({
    queryKey: ['users'],
    queryFn: async () => (await apiFetch('/users')) as UserOut[],
  })

  const auditQuery = useQuery({
    queryKey: ['audit', auditPage],
    queryFn: async () =>
      (await apiFetch(`/audit-logs?page=${auditPage}&page_size=25`)) as AuditPage,
  })

  const analyticsQuery = useQuery({
    queryKey: ['analytics-summary'],
    queryFn: async () => (await apiFetch('/analytics/summary')) as AnalyticsSummary,
  })

  const handleExportAuditCsv = async () => {
    const token = getAccessToken()
    const res = await fetch(`${API_BASE}/audit-logs/export.csv`, {
      credentials: 'include',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })
    if (!res.ok) {
      message.error('Не удалось выгрузить CSV')
      return
    }
    const blob = await res.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'audit_export.csv'
    a.click()
    URL.revokeObjectURL(url)
    message.success('Файл скачан')
  }

  useEffect(() => {
    if (!editUser) {
      return
    }
    editForm.setFieldsValue({
      email: editUser.email,
      last_name: editUser.last_name,
      first_name: editUser.first_name,
      role: editUser.role,
      is_active: editUser.is_active,
      password: '',
    })
  }, [editUser, editForm])

  const createMut = useMutation({
    mutationFn: async (values: {
      email: string
      last_name: string
      first_name: string
      role: string
      is_active: boolean
    }) => {
      const body = {
        email: values.email,
        last_name: values.last_name,
        first_name: values.first_name,
        role: values.role,
        is_active: values.is_active,
      }
      return (await apiFetch('/users', {
        method: 'POST',
        body: JSON.stringify(body),
      })) as UserCreatedOut
    },
    onSuccess: async (data) => {
      if (data.welcome_email_queued) {
        message.success('Пользователь создан. Приветственное письмо отправляется на email — подождите 1–2 минуты')
      } else if (data.welcome_email_skipped_reason) {
        message.warning(
          `Пользователь создан. ${data.welcome_email_skipped_reason}`,
          10,
        )
      } else {
        message.success('Пользователь создан')
      }
      setUserOpen(false)
      createForm.resetFields()
      await qc.invalidateQueries({ queryKey: ['users'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const updateMut = useMutation({
    mutationFn: async (payload: { id: string; values: Record<string, unknown> }) => {
      await apiFetch(`/users/${payload.id}`, {
        method: 'PATCH',
        body: JSON.stringify(payload.values),
      })
    },
    onSuccess: async () => {
      message.success('Сохранено')
      setEditUser(null)
      await qc.invalidateQueries({ queryKey: ['users'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const deleteMut = useMutation({
    mutationFn: async (id: string) => {
      await apiFetch(`/users/${id}`, { method: 'DELETE' })
    },
    onSuccess: async () => {
      message.success('Удалено')
      await qc.invalidateQueries({ queryKey: ['users'] })
    },
    onError: (e: Error) => message.error(e.message),
  })

  const userColumns: ColumnsType<UserOut> = [
    {
      title: 'Фамилия и имя',
      key: 'display_name',
      width: 200,
      ellipsis: true,
      render: (_, u) => userDisplayName(u),
    },
    { title: 'Email', dataIndex: 'email', key: 'email', ellipsis: true },
    {
      title: 'Роль',
      dataIndex: 'role',
      key: 'role',
      width: 160,
      render: (r: string) =>
        ({ OPERATOR: 'Оператор', STREAM_MANAGER: 'Менеджер', SUPERADMIN: 'Суперадмин' } as Record<
          string,
          string
        >)[r] ?? r,
    },
    {
      title: 'Активен',
      dataIndex: 'is_active',
      key: 'is_active',
      width: 100,
      render: (v: boolean) => (v ? 'да' : 'нет'),
    },
    {
      title: 'Последний вход',
      dataIndex: 'last_login_at',
      key: 'last_login_at',
      width: 170,
      ellipsis: true,
      render: (v: string | undefined) => (v ? formatDateTimeRu(v) : '—'),
    },
    {
      title: 'IP при входе',
      dataIndex: 'last_login_ip',
      key: 'last_login_ip',
      width: 140,
      ellipsis: true,
      render: (v: string | null | undefined) => v || '—',
    },
    {
      title: '',
      key: 'actions',
      width: 200,
      render: (_, u) => (
        <Space>
          <Button type="link" onClick={() => setEditUser(u)}>
            Изменить
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => {
              modal.confirm({
                title: 'Удалить пользователя?',
                okText: 'Удалить',
                cancelText: 'Отмена',
                okButtonProps: { danger: true },
                onOk: async () => {
                  await deleteMut.mutateAsync(u.id)
                },
              })
            }}
          >
            Удалить
          </Button>
        </Space>
      ),
    },
  ]

  const auditColumns: ColumnsType<AuditLogOut> = [
    {
      title: 'Время',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 160,
      render: (v: string) => formatDateTimeRu(v),
    },
    {
      title: 'Действие',
      dataIndex: 'action_type',
      key: 'action_type',
      width: 200,
      render: (v: string) => auditActionLabel(v),
    },
    {
      title: 'Сущность',
      dataIndex: 'entity_type',
      key: 'entity_type',
      width: 160,
      render: (v: string) => auditEntityLabel(v),
    },
    { title: 'ID', dataIndex: 'entity_id', key: 'entity_id', ellipsis: true },
    {
      title: 'Детали',
      key: 'details',
      width: 320,
      render: (_, r) => {
        const text = formatAuditPayloadRu({
          ...(r.payload_before != null ? { было: r.payload_before as Record<string, unknown> } : {}),
          ...(r.payload_after != null ? { стало: r.payload_after as Record<string, unknown> } : {}),
        })
        return (
          <Typography.Paragraph type="secondary" style={{ fontSize: 12, marginBottom: 0, maxWidth: 400 }}>
            {text || '—'}
          </Typography.Paragraph>
        )
      },
    },
  ]

  return (
    <AppLayout
      nav={
        <Typography.Text type="secondary" style={{ fontSize: 13 }}>
          Суперадмин
        </Typography.Text>
      }
    >
      <Typography.Title level={3} style={{ marginTop: 0 }}>
        Администрирование
      </Typography.Title>

      <Tabs
        items={[
          {
            key: 'users',
            label: 'Пользователи',
            children: (
              <Card
                style={{ borderColor: '#e2e8f0', background: '#ffffff' }}
                extra={
                  <Button
                    type="primary"
                    icon={<PlusOutlined />}
                    onClick={() => setUserOpen(true)}
                    size="large"
                    block={isNarrow}
                  >
                    Новый пользователь
                  </Button>
                }
              >
                <Table
                  rowKey="id"
                  loading={usersQuery.isLoading}
                  dataSource={usersQuery.data ?? []}
                  columns={userColumns}
                  scroll={{ x: 1100 }}
                  size={isNarrow ? 'small' : 'middle'}
                />
              </Card>
            ),
          },
          {
            key: 'stats',
            label: 'Статистика',
            children: (
              <Card style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
                <Typography.Paragraph type="secondary">
                  Назначения операторов на мероприятия, число эфиров и упоминаний за выбранный календарный день (МСК).
                  Карточки мероприятий открываются как у менеджера.
                </Typography.Paragraph>
                <OperatorStatsPanel />
              </Card>
            ),
          },
          {
            key: 'analytics',
            label: (
              <span>
                <BarChartOutlined /> Продукт
              </span>
            ),
            children: (
              <Card style={{ borderColor: '#e2e8f0', background: '#ffffff' }}>
                <Typography.Paragraph type="secondary">
                  Данные аналитики за 7 дней (page_view и др.), накопленные через{' '}
                  <Typography.Text code>/analytics/events</Typography.Text>.
                </Typography.Paragraph>
                <Table
                  rowKey="event_name"
                  loading={analyticsQuery.isLoading}
                  dataSource={analyticsQuery.data?.by_event ?? []}
                  pagination={false}
                  size="small"
                  columns={[
                    { title: 'Ключ', dataIndex: 'event_name', key: 'e' },
                    { title: 'Раз', dataIndex: 'count', key: 'c', width: 100 },
                  ]}
                />
              </Card>
            ),
          },
          {
            key: 'audit',
            label: 'Аудит',
            children: (
              <Card
                style={{ borderColor: '#e2e8f0', background: '#ffffff' }}
                extra={
                  <Button icon={<DownloadOutlined />} onClick={() => void handleExportAuditCsv()}>
                    Выгрузить CSV
                  </Button>
                }
              >
                <Table
                  rowKey="id"
                  loading={auditQuery.isLoading}
                  dataSource={auditQuery.data?.items ?? []}
                  columns={auditColumns}
                  scroll={{ x: 900 }}
                  size={isNarrow ? 'small' : 'middle'}
                  pagination={{
                    current: auditPage,
                    pageSize: 25,
                    total: auditQuery.data?.total ?? 0,
                    onChange: (p) => setAuditPage(p),
                    size: isNarrow ? 'small' : 'default',
                    showSizeChanger: false,
                  }}
                />
              </Card>
            ),
          },
        ]}
      />

      <Modal
        title="Новый пользователь"
        open={userOpen}
        okText="Создать"
        cancelText="Отмена"
        confirmLoading={createMut.isPending}
        onCancel={() => setUserOpen(false)}
        onOk={async () => {
          const v = await createForm.validateFields()
          await createMut.mutateAsync({
            email: v.email,
            last_name: v.last_name,
            first_name: v.first_name,
            role: v.role,
            is_active: v.is_active ?? true,
          })
        }}
      >
        <Form form={createForm} layout="vertical" initialValues={{ is_active: true, role: 'OPERATOR' }}>
          <Form.Item name="email" label="Email" rules={[{ required: true, type: 'email' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="last_name" label="Фамилия" rules={[{ required: true, whitespace: true }]}>
            <Input autoComplete="family-name" />
          </Form.Item>
          <Form.Item name="first_name" label="Имя" rules={[{ required: true, whitespace: true }]}>
            <Input autoComplete="given-name" />
          </Form.Item>
          <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
            Пароль генерируется автоматически и отправляется на email (если на сервере настроен SMTP).
          </Typography.Paragraph>
          <Form.Item name="role" label="Роль" rules={[{ required: true }]}>
            <Select
              options={[
                { label: 'SUPERADMIN', value: 'SUPERADMIN' },
                { label: 'STREAM_MANAGER', value: 'STREAM_MANAGER' },
                { label: 'OPERATOR', value: 'OPERATOR' },
              ]}
            />
          </Form.Item>
          <Form.Item name="is_active" label="Активен" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Изменить пользователя"
        open={Boolean(editUser)}
        okText="Сохранить"
        cancelText="Отмена"
        confirmLoading={updateMut.isPending}
        onCancel={() => setEditUser(null)}
        onOk={async () => {
          if (!editUser) {
            return
          }
          const v = await editForm.validateFields()
          const payload: Record<string, unknown> = {
            email: v.email,
            last_name: v.last_name,
            first_name: v.first_name,
            role: v.role,
            is_active: v.is_active,
          }
          if (v.password) {
            payload.password = v.password
          }
          await updateMut.mutateAsync({ id: editUser.id, values: payload })
        }}
      >
        <Form form={editForm} layout="vertical">
          <Form.Item name="email" label="Email" rules={[{ required: true, type: 'email' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="last_name" label="Фамилия" rules={[{ required: true, whitespace: true }]}>
            <Input autoComplete="family-name" />
          </Form.Item>
          <Form.Item name="first_name" label="Имя" rules={[{ required: true, whitespace: true }]}>
            <Input autoComplete="given-name" />
          </Form.Item>
          <Form.Item
            name="password"
            label="Новый пароль (необязательно)"
            rules={[
              {
                validator: async (_, v: string) => {
                  if (!v || v.length >= 8) {
                    return
                  }
                  throw new Error('Минимум 8 символов')
                },
              },
            ]}
          >
            <Input.Password />
          </Form.Item>
          <Form.Item name="role" label="Роль" rules={[{ required: true }]}>
            <Select
              options={[
                { label: 'SUPERADMIN', value: 'SUPERADMIN' },
                { label: 'STREAM_MANAGER', value: 'STREAM_MANAGER' },
                { label: 'OPERATOR', value: 'OPERATOR' },
              ]}
            />
          </Form.Item>
          <Form.Item name="is_active" label="Активен" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </AppLayout>
  )
}

```


---

## Исходный код: `frontend/src/stories/BrandLogo.stories.tsx`

> 16 строк, 321 байт

```tsx
import type { Meta, StoryObj } from '@storybook/react'

import { BrandLogo } from '@/components/BrandLogo'

const meta: Meta<typeof BrandLogo> = {
  title: 'Brand/BrandLogo',
  component: BrandLogo,
}
export default meta

type Story = StoryObj<typeof BrandLogo>

export const Default: Story = {
  args: { height: 32 },
}

```


---

## Исходный код: `frontend/src/styles/global.css`

> 102 строк, 2,355 байт

```css
* {
  box-sizing: border-box;
}

html {
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
}

html,
body,
#root {
  height: 100%;
  margin: 0;
}

body {
  font-family: Inter, system-ui, -apple-system, Segoe UI, sans-serif;
  background: #f4f6f9;
  color: #0f172a;
  padding-left: env(safe-area-inset-left, 0px);
  padding-right: env(safe-area-inset-right, 0px);
  touch-action: manipulation;
}

/* Доступность: явный фокус с клавиатуры */
:focus:not(:focus-visible) {
  outline: none;
}

:focus-visible {
  outline: 2px solid rgba(2, 132, 199, 0.55);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* iOS: поля <16px при фокусе вызывают зум — на телефоне держим минимум 16px */
@media (max-width: 576px) {
  input,
  textarea,
  select,
  .ant-input,
  .ant-input-number-input,
  .ant-select-selection-search-input {
    font-size: 16px !important;
  }
}

/* Таблицы: горизонтальный скролл без «ломания» вёрстки */
.ant-table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* Модалки на узком экране — почти на всю ширину + отступы под safe area */
@media (max-width: 576px) {
  .ant-modal-root .ant-modal {
    max-width: calc(100vw - 16px - env(safe-area-inset-left) - env(safe-area-inset-right));
    margin: 12px auto;
    padding-bottom: env(safe-area-inset-bottom, 12px);
  }

  .ant-modal-root .ant-modal-body {
    max-height: min(70vh, calc(100dvh - 200px));
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
  }
}

/* Карточки: заголовок и extra в колонку на узком экране */
@media (max-width: 576px) {
  .ant-card .ant-card-head-wrapper {
    flex-direction: column;
    align-items: stretch;
  }

  .ant-card-extra {
    margin-inline-start: 0 !important;
    padding-top: 8px;
  }
}

/* Drawer / dropdown удобнее на тач-экране */
@media (pointer: coarse) {
  .ant-btn:not(.ant-btn-sm) {
    min-height: 44px;
  }

  .ant-list-item-action > li {
    padding-inline: 4px;
  }
}

```


---

## Исходный код: `frontend/src/theme.ts`

> 49 строк, 1,180 байт

```ts
import { theme } from 'antd'

/** Светлая тема: белый фон, акценты в духе логотипа (лазурь / тёмно-синий) */
export const appTheme = {
  algorithm: theme.defaultAlgorithm,
  token: {
    colorPrimary: '#0284c7',
    colorInfo: '#0891b2',
    colorLink: '#0284c7',
    colorBgLayout: '#f4f6f9',
    colorBgContainer: '#ffffff',
    colorBorder: '#e2e8f0',
    borderRadius: 10,
    fontFamily: '"Inter", system-ui, -apple-system, "Segoe UI", sans-serif',
    colorText: '#0f172a',
    colorTextSecondary: '#64748b',
    fontSize: 15,
    fontSizeLG: 16,
    controlHeight: 40,
    controlHeightLG: 52,
    paddingContentHorizontalLG: 20,
  },
  components: {
    Layout: {
      headerBg: '#ffffff',
      bodyBg: '#f4f6f9',
      footerBg: 'transparent',
    },
    Table: {
      headerBg: '#f1f5f9',
      headerColor: '#334155',
      cellPaddingBlockMD: 12,
      cellPaddingInlineMD: 10,
    },
    Button: {
      controlHeightLG: 52,
      fontSizeLG: 17,
      paddingInlineLG: 20,
    },
    Card: {
      paddingLG: 16,
    },
    List: {
      itemPaddingSM: '12px 0',
      itemPaddingLG: '14px 0',
    },
  },
}

```


---

## Исходный код: `frontend/src/utils/auditLabels.ts`

> 96 строк, 3,812 байт

```ts
/** Человекочитаемые подписи для журнала аудита */

export const auditActionLabel = (code: string): string => {
  const m: Record<string, string> = {
    LOGIN: 'Вход в систему',
    LOGOUT: 'Выход',
    USER_CREATE: 'Создание пользователя',
    USER_UPDATE: 'Изменение пользователя',
    USER_DELETE: 'Удаление пользователя',
    STREAM_CREATE: 'Создание мероприятия',
    STREAM_UPDATE: 'Изменение мероприятия',
    STREAM_DELETE: 'Удаление мероприятия',
    STREAM_LOCK: 'Мероприятие взято в работу',
    STREAM_UNLOCK: 'Мероприятие снято с работы',
    BROADCAST_START: 'Начало эфира',
    BROADCAST_STOP: 'Остановка эфира',
    BROADCAST_ACTUAL_START: 'Уточнение фактического времени начала эфира',
    MENTION_CREATE: 'Добавлено упоминание',
    MENTION_UPDATE: 'Изменено упоминание',
    LOGO_UPLOAD: 'Загрузка логотипа в медиатеку',
    LOGO_ATTACH: 'Логотип прикреплён к мероприятию',
    LOGO_DETACH: 'Логотип откреплён от мероприятия',
    LOGO_DOWNLOAD_ARCHIVE: 'Скачивание архива логотипов',
  }
  return m[code] ?? code
}

export const auditEntityLabel = (code: string): string => {
  const m: Record<string, string> = {
    user: 'Пользователь',
    stream_event: 'Мероприятие',
    broadcast_session: 'Сессия эфира',
    sponsor_mention: 'Упоминание спонсора',
    logo: 'Логотип',
  }
  return m[code] ?? code
}

const payloadKeyLabel = (key: string): string => {
  const m: Record<string, string> = {
    before: 'было',
    after: 'стало',
    stream_event_id: 'мероприятие',
    broadcast_session_id: 'сессия эфира',
    sponsor_mention_id: 'упоминание',
    mention_id: 'упоминание',
    day_index: 'день',
    started_at: 'начало',
    ended_at: 'окончание',
    title: 'название',
    start_date: 'дата старта',
    duration_days: 'дней',
    offset_sec: 'смещение, с',
    original_offset_sec: 'исходное смещение, с',
    adjusted_offset_sec: 'скорректировано, с',
    email: 'email',
    first_name: 'имя',
    last_name: 'фамилия',
    ip: 'IP',
    locked_by_user_id: 'заблокировал',
    entity_type: 'тип сущности',
    entity_id: 'id сущности',
  }
  return m[key] ?? key
}

const formatPayloadValue = (v: unknown): string => {
  if (v === null || v === undefined) {
    return '—'
  }
  if (typeof v === 'object' && v !== null && !Array.isArray(v)) {
    return formatAuditPayloadRu(v as Record<string, unknown>)
  }
  if (typeof v === 'string' && v.length > 120) {
    return `${v.slice(0, 120)}…`
  }
  return String(v)
}

/** Короткое русскоязычное описание JSON полезной нагрузки аудита */
export const formatAuditPayloadRu = (obj: Record<string, unknown> | null | undefined): string => {
  if (!obj || typeof obj !== 'object') {
    return '—'
  }
  const parts: string[] = []
  for (const [k, val] of Object.entries(obj)) {
    const label = payloadKeyLabel(k)
    if (val !== null && val !== undefined && typeof val === 'object' && !Array.isArray(val)) {
      parts.push(`${label}: { ${formatAuditPayloadRu(val as Record<string, unknown>)} }`)
      continue
    }
    parts.push(`${label}: ${formatPayloadValue(val)}`)
  }
  return parts.join('; ')
}

```


---

## Исходный код: `frontend/src/utils/datetime.ts`

> 31 строк, 831 байт

```ts
import dayjs from 'dayjs'
import timezone from 'dayjs/plugin/timezone'
import utc from 'dayjs/plugin/utc'

dayjs.extend(utc)
dayjs.extend(timezone)

/** Отображение: dd.mm.yyyy HH:mm (24ч), время в Europe/Moscow */
export const formatDateTimeRu = (value: string | undefined | null): string => {
  if (value == null || value === '') {
    return '—'
  }
  const d = dayjs(value)
  if (!d.isValid()) {
    return value
  }
  return d.tz('Europe/Moscow').format('DD.MM.YYYY HH:mm')
}

/** Только дата: dd.mm.yyyy (поля даты с API в виде YYYY-MM-DD) */
export const formatDateRu = (value: string | undefined | null): string => {
  if (value == null || value === '') {
    return '—'
  }
  const d = dayjs(value)
  if (!d.isValid()) {
    return value
  }
  return d.format('DD.MM.YYYY')
}

```


---

## Исходный код: `frontend/src/utils/normalizeRuMobilePhone.ts`

> 27 строк, 922 байт

```ts
/** Совпадает с backend app.utils.phone_ru.normalize_ru_mobile_phone */

export const normalizeRuMobilePhone = (raw: string): string => {
  const s = raw.trim()
  if (!s) {
    throw new Error('Пустой номер')
  }
  let digits = s.replace(/\D/g, '')
  if (digits.length === 11 && digits[0] === '8') {
    digits = `7${digits.slice(1)}`
  } else if (digits.length === 10 && digits[0] === '9') {
    digits = `7${digits}`
  }
  if (digits.length !== 11 || digits[0] !== '7') {
    throw new Error('Нужен российский мобильный: 10 цифр с 9 или 11 с 7/8')
  }
  if (digits[1] !== '9') {
    throw new Error('Поддерживаются только мобильные номера')
  }
  const rest = digits.slice(1)
  const a = rest.slice(0, 3)
  const b = rest.slice(3, 6)
  const c = rest.slice(6, 8)
  const d = rest.slice(8, 10)
  return `+7 (${a}) ${b} ${c} ${d}`
}

```


---

## Исходный код: `frontend/src/utils/userDisplay.ts`

> 16 строк, 544 байт

```ts
import type { UserOut } from '@/api/types'

/** Обращение по ФИО; если с бэка нет полей — собираем из частей или email */
export const userDisplayName = (
  user: Pick<UserOut, 'display_name' | 'last_name' | 'first_name' | 'email'> | null | undefined,
): string => {
  if (!user) {
    return ''
  }
  if (user.display_name && user.display_name.trim()) {
    return user.display_name.trim()
  }
  const s = `${user.last_name ?? ''} ${user.first_name ?? ''}`.trim()
  return s || user.email
}

```


---

## Исходный код: `frontend/src/vite-env.d.ts`

> 10 строк, 157 байт

```ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

```


---

## Исходный код: `frontend/tsconfig.json`

> 25 строк, 573 байт

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "useDefineForClassFields": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"]
}

```


---

## Исходный код: `frontend/tsconfig.node.json`

> 12 строк, 233 байт

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}

```


---

## Исходный код: `frontend/vite.config.ts`

> 55 строк, 1,213 байт

```ts
import { fileURLToPath, URL } from 'node:url'

import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico'],
      manifest: {
        name: 'MainStream Ops',
        short_name: 'MainStream',
        theme_color: '#070b10',
        background_color: '#070b10',
        display: 'standalone',
        start_url: '/',
        icons: [],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
      },
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        ws: true,
      },
      '/health': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/openapi.json': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/uploads': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})

```


---

## Исходный код: `nginx/Dockerfile`

> 12 строк, 302 байт

```text
FROM node:20-alpine AS frontend-build
WORKDIR /build
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=frontend-build /build/dist /usr/share/nginx/html
EXPOSE 80

```


---

## Исходный код: `nginx/nginx.conf`

> 59 строк, 1,732 байт

```conf
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    sendfile on;
    keepalive_timeout 65;
    client_max_body_size 20m;

    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    map $http_x_request_id $proxy_request_id {
        default $http_x_request_id;
        ''      $request_id;
    }

    server {
        listen 80;
        server_name _;

        root /usr/share/nginx/html;
        index index.html;

        location /api/ {
            proxy_pass http://backend:8000;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Request-ID $proxy_request_id;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_read_timeout 86400;
        }

        location /health {
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Request-ID $proxy_request_id;
        }

        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self' ws: wss: http: https:; font-src 'self' data:; frame-ancestors 'self'; base-uri 'self'" always;

        location / {
            try_files $uri $uri/ /index.html;
        }
    }
}

```


---

## Исходный код: `ТЗ-сервер.md`

> 28 строк, 1,290 байт

```md
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
  - `/api/`, `/health`, `/openapi.json`, `/uploads/` → backend **8010**;
  - длинный `proxy_read_timeout` для WebSocket.

## Связь с MainStream Shop
Тот же бренд в домене (**mainstreamfs**), но **другой код** и **другой systemd** на сервере.

## Данные
- Загрузки и БД приложения — внутри `/opt/streaming/backend` по конфигурации.

```


---

# ЧАСТЬ XIV. ПРИЛОЖЕНИЯ (ДОКУМЕНТАЦИЯ)

## Документ: `/opt/streaming/README.md`

# Платформа эфиров MainStream

> Полная техническая документация: [.cursor/skills/streaming/reference.md](.cursor/skills/streaming/reference.md)  
> AI skill: [.cursor/skills/streaming/SKILL.md](.cursor/skills/streaming/SKILL.md)

---

## Содержание

- [О проекте](#о-проекте)
- [Архитектура](#архитектура)
- [Функциональность](#функциональность)
- [API](#api)
- [Установка и запуск](#установка-и-запуск)
- [Деплой на сервер](#деплой-на-сервер)
- [Переменные окружения](#переменные-окружения)
- [Структура каталогов](#структура-каталогов)
- [Бэкапы и безопасность](#бэкапы-и-безопасность)
- [Документация](#документация)

---

## О проекте

**Платформа эфиров MainStream** — Управление видеоэфирами и таймкодами.

| Параметр | Значение |
|----------|----------|
| Бренд / заказчик | MainStream |
| Production URL | https://streaming.mainstreamfs.ru |
| Backend порт (localhost) | 8010 |
| База данных | PostgreSQL: streaming |
| ОС сервера | Ubuntu 22.04 (VPS Beget) |
| Процесс-менеджер | systemd |
| Reverse proxy | nginx + Let's Encrypt |
| Пользователь сервиса | root |
| Файлов в репозитории (анализ) | 154 |
| Строк кода (оценка) | 13,256 |

### Назначение системы

Система развёрнута на сервере `xkvlorcrjx` (45.12.237.105) и обслуживается в составе экосистемы MainStream.
Все HTTP-сервисы слушают только `127.0.0.1`; внешний доступ — через nginx (443/SSL).

---

---

## Архитектура

### Стек технологий

alembic, antd, fastapi, pydantic, react, sqlalchemy, typescript, uvicorn, vite

### Структура верхнего уровня

```
.env.example
Mainstream_logo_Black and 1
```

---

---

## Функциональность

# Платформа эфиров и спонсорских упоминаний

Сервис для видеооператоров MainStream: управление стрим-событиями, блокировки операторов, таймкоды упоминаний (Europe/Moscow), аудит, отчёты в Word.

## Стек

- **Backend:** FastAPI, SQLAlchemy 2 async, PostgreSQL, Alembic, JWT (access + refresh cookie), WebSocket
- **Frontend:** React 18, Vite, TypeScript, Ant Design, TanStack Query
- **Инфра:** Docker Compose, Nginx

## Возможности платформы (обзор)

| Область | Что сделано |
|--------|-------------|
| Наблюдаемость | Заголовок `X-Request-ID`, опционально **Sentry** (backend + `VITE_SENTRY_DSN` на фронте) |
| Health | `GET /health` (liveness), `GET /health/ready` (БД + ревизия Alembic) |
| Безопасность | CSP в Nginx, проброс `X-Request-ID`; cookie refresh настраиваются через `REFRESH_COOKIE_*` |
| WebSocket | Лимит подписчиков на комнату, сообщения **presence** (число зрителей пульта) |
| Уведомления | Таблица `notifications`, API `/notifications`, колокольчик в шапке; при старте эфира — уведомления менеджерам/админам |
| Интеграции | `EXTERNAL_WEBHOOK_URL` — POST при start/stop эфира |
| Аудит | Выгрузка **CSV** (`GET /api/v1/audit-logs/export.csv`), очистка `POST /audit-logs/purge` |
| Продуктовая аналитика | `POST /analytics/events`, сводка `/analytics/summary` (суперадмин, вкладка «Продукт») |
| Приглашения | `POST /users/invites`, регистрация `POST /auth/accept-invite` |
| Чек-лист эфира | `GET/PUT /stream-events/{id}/days/{day}/checklist` (6 пунктов, отдельно на каждый день) |
| PWA | `vite-plugin-pwa` — офлайн-кэш статики |
| E2E | Playwright: `npm run test:e2e` в `frontend` (нужен стенд, см. ниже) |
| Storybook | `npm run storybook` — компонент `BrandLogo` |
| Кодоген API | `npm run codegen:api` (нужен запущенный backend с `/openapi.json`) |
| Масштаб | Рекомендации по воркерам: [docs/WORKERS_AND_SCALE.md](docs/WORKERS_AND_SCALE.md) |

## Быстрый старт (Docker)

```bash
cp .env.example .env
# При необходимости отредактируйте .env

docker compose up --build
```

Если при сборке **backend** `pip` ругается на **SSL** (`UNEXPECTED_EOF_WHILE_READING`) или **таймаут** до `pypi.org` — это сеть/фильтрация, не код. В корневом `.env` задайте зеркало и пересоберите:

```env
PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
```

Затем `docker compose build --no-cache backend` или снова `docker compose up --build`. Альтернатива: VPN или другая сеть; временно отключить «сканирование HTTPS» в антивирусе.

Откройте http://localhost — SPA, API: http://localhost/api/v1/...

Первичные пользователи и демо-событие:

```bash
docker compose exec backend python -m scripts.seed
```

## Локальная разработка

### База данных

Поднимите PostgreSQL 16 и создайте БД `streaming` (или используйте `docker compose up db`).

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
set DATABASE_URL=postgresql+asyncpg://streaming:streaming@localhost:5432/streaming
set DATABASE_URL_SYNC=postgresql://streaming:streaming@localhost:5432/streaming
alembic upgrade head
python -m scripts.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

По умолчанию Vite проксирует `/api`, `/health`, `/openapi.json` и `/ws` на `http://127.0.0.1:8000` (см. `frontend/vite.config.ts`).

### E2E (Playwright)

```bash
cd frontend
npx playwright install   # один раз, ставит браузеры
# Поднимите приложение (docker compose или dev), затем:
set E2E_BASE_URL=http://localhost
npm run test:e2e
```

### Тесты backend

```bash
cd backend
pytest -q
```

## Учётные записи после seed

По умолчанию создаются три пользователя с паролем `ChangeMe123!`. Почты и пароль сида можно задать в `backend/.env`: `SEED_ADMIN_EMAIL`, `SEED_MANAGER_EMAIL`, `SEED_OPERATOR_EMAIL`, `SEED_PASSWORD` (см. `.env.example`).

| Email (по умолчанию) | Роль |
|----------------------|------|
| admin@example.com | SUPERADMIN |
| manager@example.com | STREAM_MANAGER |
| operator@example.com | OPERATOR |

Смените пароли в продакшене. Полное пересоздание БД: [docs/DB_RESET.md](docs/DB_RESET.md).

**Суперадмин** в разделе «Администрирование» → «Пользователи» может создавать учётки (пароль можно не задавать — уйдёт на почту при настроенном SMTP). Смена email админа в БД: [docs/CHANGE_ADMIN_EMAIL.md](docs/CHANGE_ADMIN_EMAIL.md).

Новые пользователи проходят короткое интерактивное знакомство с панелью (имя, пароль, аватар, роли); демо-учётки из `scripts.seed` помечены как уже прошедшие ознакомление. Дополнительно после входа с временным паролем можно показать напоминание сменить пароль в «Профиль».

## Git

Рекомендуемые ветки: `main` (стабильная), `develop` (интеграция), feature-ветки от `develop`.

## Продакшен

Пошаговый выклад на VPS (PostgreSQL, сборка фронта, **systemd** + **nginx** + **Let’s Encrypt**): [docs/DEPLOY_PRODUCTION.md](docs/DEPLOY_PRODUCTION.md).  
Команды «с нуля» одним файлом: [docs/SERVER_COPYPASTE.md](docs/SERVER_COPYPASTE.md).  
Инвентаризация прод-сервера (порты, домены, пути проектов): [docs/SERVER_INVENTORY_XKVLORCRJX.md](docs/SERVER_INVENTORY_XKVLORCRJX.md).

---

## API

Всего обнаружено маршрутов: **51**

```
GET /health — `backend/app/api/health.py`
GET /health/ready — `backend/app/api/health.py`
GET /export.csv — `backend/app/api/v1/audit.py`
POST /purge — `backend/app/api/v1/audit.py`
POST /accept-invite — `backend/app/api/v1/auth.py`
POST /forgot-password — `backend/app/api/v1/auth.py`
GET /password-reset/validate — `backend/app/api/v1/auth.py`
POST /reset-password — `backend/app/api/v1/auth.py`
POST /login — `backend/app/api/v1/auth.py`
POST /refresh — `backend/app/api/v1/auth.py`
POST /logout — `backend/app/api/v1/auth.py`
GET /me — `backend/app/api/v1/auth.py`
POST /change-password — `backend/app/api/v1/auth.py`
GET /sessions — `backend/app/api/v1/auth.py`
DELETE /sessions/{session_id} — `backend/app/api/v1/auth.py`
DELETE /{template_id} — `backend/app/api/v1/event_templates.py`
POST /from-event/{stream_id} — `backend/app/api/v1/event_templates.py`
POST /{template_id}/instantiate — `backend/app/api/v1/event_templates.py`
POST /upload — `backend/app/api/v1/logos.py`
POST /upload-batch — `backend/app/api/v1/logos.py`
POST /broadcast-sessions/{session_id}/mentions — `backend/app/api/v1/mentions.py`
PATCH /sponsor-mentions/{mention_id} — `backend/app/api/v1/mentions.py`
DELETE /sponsor-mentions/{mention_id} — `backend/app/api/v1/mentions.py`
POST /{notification_id}/read — `backend/app/api/v1/notifications.py`
POST /read-all — `backend/app/api/v1/notifications.py`
POST /events — `backend/app/api/v1/product_analytics.py`
GET /summary — `backend/app/api/v1/product_analytics.py`
POST /avatar — `backend/app/api/v1/profile.py`
GET /activity — `backend/app/api/v1/profile.py`
GET /mentions — `backend/app/api/v1/reports.py`
GET /export.docx — `backend/app/api/v1/reports.py`
GET /export.csv — `backend/app/api/v1/reports.py`
GET /export.xlsx — `backend/app/api/v1/reports.py`
GET /operators — `backend/app/api/v1/stats.py`
GET /{stream_id} — `backend/app/api/v1/stream_events.py`
PATCH /{stream_id} — `backend/app/api/v1/stream_events.py`
DELETE /{stream_id} — `backend/app/api/v1/stream_events.py`
POST /{stream_id}/lock — `backend/app/api/v1/stream_events.py`
POST /{stream_id}/unlock — `backend/app/api/v1/stream_events.py`
POST /{stream_id}/days/{day_index}/broadcast/start — `backend/app/api/v1/stream_events.py`
POST /{stream_id}/days/{day_index}/broadcast/stop — `backend/app/api/v1/stream_events.py`
GET /{stream_id}/days/{day_index}/checklist — `backend/app/api/v1/stream_events.py`
PUT /{stream_id}/days/{day_index}/checklist — `backend/app/api/v1/stream_events.py`
GET /{stream_id}/days/{day_index}/mentions — `backend/app/api/v1/stream_events.py`
POST /{stream_id}/logos — `backend/app/api/v1/stream_logos.py`
DELETE /{stream_id}/logos/{logo_id} — `backend/app/api/v1/stream_logos.py`
GET /{stream_id}/logos/archive.zip — `backend/app/api/v1/stream_logos.py`
GET /{stream_id}/logos/{logo_id}/file — `backend/app/api/v1/stream_logos.py`
POST /invites — `backend/app/api/v1/users.py`
PATCH /{user_id} — `backend/app/api/v1/users.py`
DELETE /{user_id} — `backend/app/api/v1/users.py`
```

---

---

## Установка и запуск

### Локальная разработка

```bash
cd /opt/streaming
# Python-проекты
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt  # или backend/requirements.txt

# Node-проекты
npm ci && npm run dev
```

Скопируйте `env.example` → `.env` и заполните переменные.

---

## Деплой на сервер

### Перезапуск
```bash
systemctl restart streaming-backend
```

### Логи
```bash
journalctl -u streaming-backend -f --since "2 hours ago"
```

### Типовой деплой
1. `cd /opt/streaming`
2. `git pull`
3. Обновить зависимости (pip/npm)
4. Миграции БД (если есть)
5. Сборка frontend (если есть)
6. `systemctl restart ...`

---

### ТЗ размещения на сервере

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
  - `/api/`, `/health`, `/openapi.json`, `/uploads/` → backend **8010**;
  - длинный `proxy_read_timeout` для WebSocket.

## Связь с MainStream Shop
Тот же бренд в домене (**mainstreamfs**), но **другой код** и **другой systemd** на сервере.

## Данные
- Загрузки и БД приложения — внутри `/opt/streaming/backend` по конфигурации.


---

## Переменные окружения

**Переменные из env.example:**

| Переменная |
|------------|
| `DATABASE_URL` |
| `DATABASE_URL_SYNC` |
| `JWT_SECRET` |
| `JWT_ACCESS_EXPIRE_MINUTES` |
| `JWT_REFRESH_EXPIRE_DAYS` |
| `CORS_ORIGINS` |
| `REFRESH_COOKIE_NAME` |
| `REFRESH_COOKIE_SECURE` |
| `REFRESH_COOKIE_SAMESITE` |
| `TZ` |
| `APP_VERSION` |

```env
# Куда класть: для systemd/uvicorn — backend/.env (рабочий каталог backend).
# Docker Compose: те же переменные в .env в корне репозитория / в environment сервиса backend.

# PostgreSQL (async URL для приложения)
DATABASE_URL=postgresql+asyncpg://streaming:streaming@localhost:5432/streaming

# Для Alembic (синхронный драйвер)
DATABASE_URL_SYNC=postgresql://streaming:streaming@localhost:5432/streaming

JWT_SECRET=change-me-to-a-long-random-string-in-production
JWT_ACCESS_EXPIRE_MINUTES=30
JWT_REFRESH_EXPIRE_DAYS=7

# CORS: через запятую, для dev: http://localhost:5173
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Cookie refresh (в prod задать свой домен)
REFRESH_COOKIE_NAME=refresh_token
REFRESH_COOKIE_SECURE=false
REFRESH_COOKIE_SAMESITE=lax

TZ=Europe/Moscow

# Версия API (отдаётся в /health, для Sentry release)
APP_VERSION=1.0.0

# Каталог загрузок (аватары и т.д.). В проде лучше абсолютный путь, например /var/lib/streaming/uploads
# UPLOAD_DIR=uploads

# Публичный URL панели (обязательно для ссылок в письмах: вход, сброс пароля, логотип)
# Пример: https://ops.example.ru — в письме сброса будет {APP_PUBLIC_BASE_URL}/reset-password?token=...
# APP_PUBLIC_BASE_URL=

# Срок жизни ссылки сброса пароля (минуты), по умолчанию 10
# PASSWORD_RESET_EXPIRE_MINUTES=10

# Sentry (опционально): backend DSN — ошибки API; на фронте задайте VITE_SENTRY_DSN в frontend/.env
# SENTRY_DSN=
# SENTRY_ENVIRONMENT=production
# SENTRY_TRACES_SAMPLE_RATE=0.1

# Внешний webhook: JSON POST при старте/остановке эфира (опционально)
# EXTERNAL_WEBHOOK_URL=https://hooks.example.com/stream

# SMTP: приветственные письма при создании пользователя + еженедельные/ежемесячные отчёты (Word)
# Пустой SMTP_HOST — почта не отправляется (пользователь всё равно создаётся)
# SMTP_HOST=smtp.example.com
# SMTP_PORT=587
# SMTP_USER=
# SMTP_PASSWORD=
# SMTP_FROM=noreply@example.com
# SMTP_USE_TLS=true
# Для порта 465 (SSL сразу, часто Beget): SMTP_USE_SSL=true и SMTP_USE_TLS=false
# SMTP_USE_SSL=false

# --- Сид пользователей (только для python -m scripts.seed; в проде задайте свои почты)
# SEED_ADMIN_EMAIL=admin@example.com
# SEED_MANAGER_EMAIL=manager@example.com
# SEED_OPERATOR_EMAIL=operator@example.com
# SEED_PASSWORD=ChangeMe123!
# Только суперадмин, без демо-мероприятия: SEED_ONLY_SUPERADMIN=1

# --- Frontend (создайте frontend/.env при локальной разработке)
# VITE_SENTRY_DSN=

# --- Только для docker compose build (backend): если pip внутри образа не достучится до pypi.org ---
# (таймауты, SSL UNEXPECTED_EOF — часто DPI/антивирус/провайдер). Скопируйте в .env и раскомментируйте одну строку:
# PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
# PIP_I

> **Важно:** никогда не коммитьте `.env` в git. На production права `chmod 600 .env`.

---

## Структура каталогов

См. полный каталог файлов в [reference.md §4](.cursor/skills/streaming/reference.md#4-каталог-файлов).

---

## Бэкапы и безопасность

- Ежедневный бэкап БД: cron `04:00` → `/usr/local/sbin/ffkm-project-backups.sh`
- Приложение слушает только `127.0.0.1`, наружу — nginx + Let's Encrypt
- Логи: `journalctl -u <service> -f`
- Аудит сервера: `/root/server_audit_report_2026-06-10.docx`

---

## Документация

| Документ | Путь |
|----------|------|
| Полная техдокументация | `.cursor/skills/streaming/reference.md` |
| AI skill (навигация) | `.cursor/skills/streaming/SKILL.md` |
| ТЗ сервера | `ТЗ-сервер.md` |
| Серверный skill | `/root/.cursor/skills/ffkm-server/` |

---

*Обновлено автоматически. Для детального анализа каждого файла проекта — reference.md.*


---

## Документ: `/opt/streaming/frontend/src/api/generated/README.md`

Сгенерированные типы OpenAPI: выполните из каталога `frontend` при запущенном backend:

```bash
npm run codegen:api
```

Файл `schema.ts` создаётся автоматически (при необходимости добавьте в `.gitignore`).


---

## Документ: `/opt/streaming/ТЗ-сервер.md`

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
  - `/api/`, `/health`, `/openapi.json`, `/uploads/` → backend **8010**;
  - длинный `proxy_read_timeout` для WebSocket.

## Связь с MainStream Shop
Тот же бренд в домене (**mainstreamfs**), но **другой код** и **другой systemd** на сервере.

## Данные
- Загрузки и БД приложения — внутри `/opt/streaming/backend` по конфигурации.


---

## Документ: `/opt/streaming/frontend/node_modules/@emotion/unitless/CHANGELOG.md`

# @emotion/unitless

## 0.7.5

### Patch Changes

- [`4c62ae9`](https://github.com/emotion-js/emotion/commit/4c62ae9447959d438928e1a26f76f1487983c968) [#1698](https://github.com/emotion-js/emotion/pull/1698) Thanks [@Andarist](https://github.com/Andarist)! - Add LICENSE file

## 0.7.4

### Patch Changes

- [c0eb604d](https://github.com/emotion-js/emotion/commit/c0eb604d) [#1419](https://github.com/emotion-js/emotion/pull/1419) Thanks [@mitchellhamilton](https://github.com/mitchellhamilton)! - Update build tool


---

## Документ: `/opt/streaming/frontend/node_modules/@emotion/hash/CHANGELOG.md`

# @emotion/hash

## 0.8.0

### Minor Changes

- [`446e756`](https://github.com/emotion-js/emotion/commit/446e75661c4aa01e51d1466472a212940c19cd82) [#1775](https://github.com/emotion-js/emotion/pull/1775) Thanks [@kripod](https://github.com/kripod)! - Optimized hashing for performance while also reducing the size of the function.

## 0.7.4

### Patch Changes

- [`4c62ae9`](https://github.com/emotion-js/emotion/commit/4c62ae9447959d438928e1a26f76f1487983c968) [#1698](https://github.com/emotion-js/emotion/pull/1698) Thanks [@Andarist](https://github.com/Andarist)! - Add LICENSE file

## 0.7.3

### Patch Changes

- [c81c0033](https://github.com/emotion-js/emotion/commit/c81c0033c490210077da0e9c3f9fa1a22fcd9c96) [#1503](https://github.com/emotion-js/emotion/pull/1503) Thanks [@Andarist](https://github.com/Andarist)! - Add TS types to util packages - hash, memoize & weak-memoize

## 0.7.2

### Patch Changes

- [c0eb604d](https://github.com/emotion-js/emotion/commit/c0eb604d) [#1419](https://github.com/emotion-js/emotion/pull/1419) Thanks [@mitchellhamilton](https://github.com/mitchellhamilton)! - Update build tool


---

