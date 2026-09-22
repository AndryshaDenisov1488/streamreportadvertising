# Purpose
MainStream streaming platform (streaming.mainstreamfs.ru): FastAPI backend with TypeScript frontend.

# Architecture
- Backend: `backend/app/`; migrations: `backend/alembic/`; tests: `backend/tests/`.
- Frontend: `frontend/src/`; nginx/deploy: `nginx/`, `deploy/`; local infra: `docker-compose.yml`.
- Runtime state: PostgreSQL `streaming`, `backend/uploads/`.

# Commands
- Backend test: `(cd backend; python -m pytest)`
- Frontend build: `(cd frontend; npm run build)`
- Dev/lint: `unknown`

# Conventions
- Keep skill docs (`.cursor/skills/streaming/`) in sync with API/schema changes, in the same commit.
- Never commit `.env`, uploads, dumps, local databases, or secrets.

# Integration
- Separate service from `msshop` despite the shared domain; databases are independent.
- `../streaming-release-20260919` is a release checkout of this repo; edit only here.

# Verification
Run targeted backend pytest tests first; frontend build for UI changes. Alembic changes require a verified backup and restore path before any release.

# Ship
Workspace policy (`../.cursor/context/decisions.md`) currently allows local task-scoped commit after QA only; no automatic push or deploy. Deploy facts (/opt/streaming, systemd `streaming-backend`): `.cursor/skills/streaming/SKILL.md` — use only when the user explicitly authorizes a release.
