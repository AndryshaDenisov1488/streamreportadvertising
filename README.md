# Платформа эфиров и спонсорских упоминаний

Внутренняя система для федерации: управление стрим-событиями, блокировки операторов, таймкоды упоминаний (Europe/Moscow), аудит, отчёты в Word.

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
| Чек-лист эфира | `GET/PUT /stream-events/{id}/checklist` (микрофон, сцена, слоты, ключи) |
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
