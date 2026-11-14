# Purpose
MainStream streaming platform (streaming.mainstreamfs.ru): FastAPI backend with TypeScript frontend.

Каноническая ветка кода и продакшена — `master`. Ветка `remediation/streaming-wave7-media` должна совпадать с ней по дереву файлов.

# Architecture
- Backend: `backend/app/`; migrations: `backend/alembic/`; tests: `backend/tests/`.
- Frontend: `frontend/src/`; nginx/deploy: `nginx/`, `deploy/`; local infra: `docker-compose.yml`.
- Runtime state: PostgreSQL `streaming`, `backend/uploads/`.

# Commands
- Backend test: `(cd backend; python -m pytest)`
- Frontend build: `(cd frontend; npm run build)`

# Conventions
- Keep skill docs (`.cursor/skills/streaming/`) in sync with API/schema changes, in the same commit.
- Never commit `.env`, uploads, dumps, local databases, or secrets.

# Integration
- Separate service from `msshop` despite the shared domain; databases are independent.
- `../streaming-release-20260919` is a release checkout of this repo; edit only here.

# Verification
Run targeted backend pytest tests first; frontend build for UI changes. Alembic changes require a verified backup and restore path before any release.

# Ship
Прод (с 2026-11-14 — 31.128.41.221, сервер Mainstream): `/opt/streaming`, systemd `streaming-backend` (user streaming), порт 8010, `.env` в `backend/`. Origin на сервере — `/opt/bundles/streaming.bundle`. Выкат: локально `git bundle create` → scp в `/opt/bundles/streaming.bundle` → на сервере `git pull --ff-only`, `alembic upgrade head` (после бэкапа `mainstream-backup.service`), рестарт юнита; `frontend/dist` собирается локально и заливается в `/opt/streaming/frontend/dist` (Node на сервере нет). Синхронизация с ffkm-admin выключена (`FFKM_ADMIN_SYNC_ENABLED=false`). Схему не менять без бэкапа. Бэкап и восстановление: `deploy/BACKUP.md`.

SSH (ключ на ПК владельца):

```powershell
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" -p 2222 root@31.128.41.221
```

`.cursor/skills/ffkm-server/SKILL.md` и `scripts/ssh-ffkm.sh` ведут на другой VPS (ФФКМ, `46.173.17.188`), не на этот сервис.

Инструкция для операторов и менеджеров: шапка «Как работать», маршрут `/help`.
