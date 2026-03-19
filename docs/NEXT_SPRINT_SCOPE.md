# Следующий спринт: приоритеты и ТЗ

Документ закрывает этап планирования по списку из 15 идей улучшений. Выбраны **5 направлений** на ближайший спринт: упор на **эксплуатацию** и **доверие к релизам**, без распыления на крупные продуктовые фичи (presence, PWA, чек-листы — в бэклог).

| # в исходном списке | Направление                         | Зачем сейчас |
|--------------------|-------------------------------------|--------------|
| 1                  | Наблюдаемость: Sentry + request ID  | Быстрый разбор инцидентов на эфире |
| 7                  | Health / readiness (БД, миграции)   | Честные деплои и оркестраторы |
| 2                  | E2E Playwright (критические сценарии) | Регрессия пульта и ролей |
| 3                  | Клиент API из OpenAPI               | Меньше рассинхрона `types.ts` ↔ backend |
| 9                  | Безопасность: прод-настройки        | CSP, cookie flags, политика сессий |

Остальные пункты (4–6, 8, 10–15) остаются в бэклоге; при необходимости следующий спринт можно сместить в сторону **комплаенса** (8, 10) или **операторского UX** (4, 5, 6, 11).

---

## 1. Наблюдаемость: Sentry + correlation / request ID

**Цель:** связать логи HTTP, ошибки и (по возможности) WebSocket в одну цепочку по `X-Request-ID`.

### Критерии готовности

- [ ] Backend: middleware принимает `X-Request-ID` от клиента или генерирует UUID; id попадает в логи uvicorn/structlog (или стандартный logging filter).
- [ ] Backend: ответы API содержат заголовок `X-Request-ID` (тот же id).
- [ ] Sentry SDK подключён к FastAPI (и опционально к frontend build) за флагом `SENTRY_DSN`; при пустом DSN — поведение как сейчас, без ошибок.
- [ ] В README или `.env.example` описаны переменные `SENTRY_DSN`, `SENTRY_ENVIRONMENT`.

### Затрагиваемые файлы / сервисы

- [backend/app/main.py](backend/app/main.py) — middleware, опционально Sentry ASGI integration
- [backend/app/core/config.py](backend/app/core/config.py) — настройки Sentry
- [backend/requirements.txt](backend/requirements.txt) — `sentry-sdk`
- [frontend/src/api/client.ts](frontend/src/api/client.ts) — генерация/проброс `X-Request-ID` на запросы
- [nginx](docker-compose.yml) / конфиг прокси — при необходимости проброс заголовка (если уже не пробрасывается)

---

## 2. Health / readiness для продакшена

**Цель:** отличать «процесс жив» от «готов принимать трафик».

### Критерии готовности

- [ ] `GET /health` — лёгкий liveness: `{"status":"ok"}` без обращения к БД (или отдельный `/health/live`).
- [ ] `GET /health/ready` (или query `?deep=1`) — проверка **async-сессии PostgreSQL** (простой `SELECT 1`).
- [ ] В ответе readiness: версия приложения (из env `APP_VERSION` или git SHA при сборке) и **текущая ревизия Alembic** (`alembic current` логика через `alembic_version` таблицу одним SELECT).
- [ ] При недоступности БД — HTTP 503 на readiness, не на liveness.

### Затрагиваемые файлы / сервисы

- [backend/app/main.py](backend/app/main.py) или новый роутер `health.py`
- [backend/app/db/session.py](backend/app/db/session.py) — получение session для проверки
- [docker-compose.yml](docker-compose.yml) / Helm (если появится) — `healthcheck` на `/health/ready`

---

## 3. E2E-тесты (Playwright)

**Цель:** автоматический прогон «логин → список → событие → lock» по ролям.

### Критерии готовности

- [ ] В корне или `e2e/`: `playwright.config.ts`, зависимости в `package.json` или отдельном workspace.
- [ ] Скрипт `npm run test:e2e` запускает тесты против `BASE_URL` (по умолчанию `http://localhost`).
- [ ] Минимум **2 сценария**: (а) оператор: логин `operator@example.com` → открыт список событий; (б) менеджер/суперадмин: логин → таблица/админка доступна.
- [ ] В README — раздел «E2E»: предусловие `docker compose up` + seed, переменные `E2E_*`.

### Затрагиваемые файлы / сервисы

- Новая папка `e2e/` или `frontend/e2e/`
- [README.md](README.md)
- [package.json](frontend/package.json) (или корневой, если монорепо без корневого package — тогда только frontend)

---

## 4. Генерация API-клиента из OpenAPI

**Цель:** единый источник правды для типов и вызовов API.

### Критерии готовности

- [ ] Скрипт `npm run codegen:api` скачивает `http://localhost:8000/openapi.json` (или из файла) и генерирует TypeScript-типы и/или fetch-обёртки.
- [ ] Выбранный инструмент зафиксирован в README (orval / openapi-typescript + openapi-fetch).
- [ ] Хотя бы **один** модуль (например `users` или `auth`) переведён на сгенерированные типы; остальное — постепенная миграция.
- [ ] Сгенерированные файлы в `.gitignore` или коммитятся — решение зафиксировано в README.

### Затрагиваемые файлы / сервисы

- [frontend/package.json](frontend/package.json)
- [frontend/src/api/types.ts](frontend/src/api/types.ts) — сокращение ручных дубликатов
- Новый каталог `frontend/src/api/generated/` (пример)

---

## 5. Безопасность: прод-настройки (срез без 2FA)

**Цель:** базовая гигиена для внутреннего контура: заголовки, cookies, таймауты.

### Критерии готовности

- [ ] **CSP** для отдачи SPA через Nginx: минимум `default-src 'self'`; `script-src` с учётом Vite/React (inline-хэши или `'unsafe-inline'` только если неизбежно — задокументировать компромисс).
- [ ] Refresh-token cookie: `Secure`, `HttpOnly`, `SameSite` — проверка и правка в [backend/app/api/v1/auth.py](backend/app/api/v1/auth.py) / security utils; в dev оставить возможность HTTP.
- [ ] Конфиг **idle timeout** access-токена или рекомендация в README (короткий access TTL + refresh) — согласовать с текущим [backend/app/core/security.py](backend/app/core/security.py).
- [ ] Краткий чеклист в README: «перед продом проверить CORS, cookie flags, HTTPS за Nginx».

### Затрагиваемые файлы / сервисы

- [nginx конфиг в репозитории](docker-compose.yml) / `nginx/` если есть
- [backend/app/core/config.py](backend/app/core/config.py)
- [backend/app/core/security.py](backend/app/core/security.py)
- [README.md](README.md)

---

## Резюме для трекера

| Задача              | Оценка (условно) | Зависимости |
|---------------------|------------------|-------------|
| Request ID + Sentry | S–M              | DSN, секреты |
| Health readiness    | S                | DB URL |
| Playwright E2E      | M                | Стабильный seed |
| OpenAPI codegen       | M                | Стабильный OpenAPI |
| Security slice        | S–M              | Nginx, HTTPS |

После выполнения работ по этому документу можно отметить в бэклоге **следующий крупный блок**: presence (п. 4 исходного списка) + центр уведомлений (п. 5) или экспорт аудита (п. 8).
