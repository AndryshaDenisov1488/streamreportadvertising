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
Прод: `/opt/streaming`, systemd `streaming-backend`, порт 8010. Выкат — `git pull` на `master`, сборка `frontend`, рестарт юнита. Схему не менять без бэкапа.

SSH (ключ на ПК владельца):

```powershell
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" -p 2222 root@159.194.203.175
```

`.cursor/skills/ffkm-server/SKILL.md` и `scripts/ssh-ffkm.sh` ведут на другой VPS (ФФКМ, `46.173.17.188`), не на этот сервис.

Инструкция для операторов и менеджеров: шапка «Как работать», маршрут `/help`.
