# Платформа эфиров и спонсорских упоминаний

Внутренняя система для федерации: управление стрим-событиями, блокировки операторов, таймкоды упоминаний (Europe/Moscow), аудит, отчёты в Word.

## Стек

- **Backend:** FastAPI, SQLAlchemy 2 async, PostgreSQL, Alembic, JWT (access + refresh cookie), WebSocket
- **Frontend:** React 18, Vite, TypeScript, Ant Design, TanStack Query
- **Инфра:** Docker Compose, Nginx

## Быстрый старт (Docker)

```bash
cp .env.example .env
# При необходимости отредактируйте .env

docker compose up --build
```

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

По умолчанию Vite проксирует `/api` и `/ws` на `http://127.0.0.1:8000` (см. `vite.config.ts`).

### Тесты backend

```bash
cd backend
pytest -q
```

## Учётные записи после seed

| Email | Роль | Пароль |
|-------|------|--------|
| admin@example.com | SUPERADMIN | ChangeMe123! |
| manager@example.com | STREAM_MANAGER | ChangeMe123! |
| operator@example.com | OPERATOR | ChangeMe123! |

Смените пароли в продакшене.

## Git

Рекомендуемые ветки: `main` (стабильная), `develop` (интеграция), feature-ветки от `develop`.
