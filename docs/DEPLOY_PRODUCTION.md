# Деплой платформы эфиров на VPS (nginx + HTTPS + systemd)

**Готовый сценарий команд для пустого сервера (копипаст по шагам):** [SERVER_COPYPASTE.md](SERVER_COPYPASTE.md).

Цель: **отдельный поддомен** (например `ops.mainstreamfs.ru` или `streaming.mainstreamfs.ru`), **бэкенд на `127.0.0.1`**, **PostgreSQL**, **SPA из `frontend/dist`**, **TLS через Let’s Encrypt**. Сайт **`mainstreamfs.ru` на порту 5002** — другой проект; этот стек **не** подставляем туда без явной замены vhost.

Рекомендуемый порт бэкенда на этом сервере: **`8010`** (диапазон 801x часто свободен — всё равно проверьте `ss -tlnp`).

---

## Часть A — у себя на машине: Git

1. Убедитесь, что **нет секретов** в коммите (файл `.env` в репозиторий не попадает — см. `.gitignore`).
2. Зафиксируйте изменения и отправьте на удалённый репозиторий:

```bash
git status
git add -A
git commit -m "feat: подготовка к прод-деплою и документация"
git push origin master
```

Если основная ветка называется `main`, замените имя ветки. При необходимости: `git remote -v` и настройка `origin`.

---

## Часть B — на сервере: обзор шагов

1. Установить зависимости: **nginx**, **certbot**, **PostgreSQL** (или отдельный контейнер только для БД), **Python 3.12+**, **Node.js 20** (для сборки фронта).
2. Создать пользователя БД и базу `streaming` (или свои имя/пароль — тогда поправьте URL в `.env`).
3. Клонировать репозиторий в каталог, например `/opt/streaming` или `/root/streaming`.
4. Backend: venv, `pip install -r requirements.txt`, файл **`backend/.env`** (см. ниже), `alembic upgrade head`, при необходимости `python -m scripts.seed`.
5. Frontend: `npm ci && npm run build` → артефакт в `frontend/dist`.
6. **systemd** — юнит для `uvicorn` (пример: `deploy/streaming-backend.service.example`).
7. **nginx** — раздача статики из `frontend/dist`, прокси `/api/`, `/health`, `/uploads`, WebSocket (пример: `deploy/nginx-streaming-site.conf.example`).
8. **HTTPS:** `certbot --nginx -d ВАШ_ПОДДОМЕН`.
9. `sudo systemctl enable --now streaming-backend` (имя сервиса как в вашем unit-файле), `sudo nginx -t && sudo systemctl reload nginx`.

---

## 1. Установка пакетов (Ubuntu 22.04)

```bash
sudo apt update
sudo apt install -y nginx certbot python3.12-venv python3-pip postgresql postgresql-contrib curl git
```

**Node.js 20** (официальный репозиторий NodeSource или `nvm` — на выбор). Пример через NodeSource:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node -v
```

---

## 2. PostgreSQL

Вариант **A — отдельная БД на уже установленном Postgres** (часто на VPS уже есть инстанс):

```bash
sudo -u postgres psql -c "CREATE USER streaming WITH PASSWORD 'СГЕНЕРИРУЙТЕ_СИЛЬНЫЙ_ПАРОЛЬ';"
sudo -u postgres psql -c "CREATE DATABASE streaming OWNER streaming;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE streaming TO streaming;"
```

Вариант **B — только Docker с Postgres** (если не хотите трогать системный кластер): поднимите контейнер с пробросом **`127.0.0.1:5433:5432`**, тогда в `DATABASE_URL` укажите порт `5433`.

---

## 3. Клонирование и каталоги

```bash
sudo mkdir -p /opt/streaming
sudo chown "$USER":"$USER" /opt/streaming
cd /opt/streaming
git clone https://ВАШ_ГИТ/streaming.git .
# или отдельная папка и git pull внутри неё
```

Каталог для загрузок (аватары и т.д.), чтобы не терять при деплое:

```bash
sudo mkdir -p /var/lib/streaming/uploads
sudo chown "$USER":"$USER" /var/lib/streaming/uploads
```

---

## 4. Backend

```bash
cd /opt/streaming/backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Создайте **`/opt/streaming/backend/.env`** (права `chmod 600`). Шаблон — из **`.env.example`**, для прода обязательно:

| Переменная | Комментарий |
|------------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://streaming:ПАРОЛЬ@127.0.0.1:5432/streaming` |
| `DATABASE_URL_SYNC` | Синхронный URL для Alembic |
| `JWT_SECRET` | Длинная случайная строка |
| `CORS_ORIGINS` | `https://ВАШ_ПОДДОМЕН` (без слэша в конце) |
| `REFRESH_COOKIE_SECURE` | `true` |
| `REFRESH_COOKIE_SAMESITE` | `lax` |
| `UPLOAD_DIR` | `/var/lib/streaming/uploads` |

```bash
export $(grep -v '^#' .env | xargs)   # опционально для одной сессии
alembic upgrade head
python -m scripts.seed    # первичные роли и демо; в проде смените пароли
```

Проверка:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8010
# с другого ssh: curl -s http://127.0.0.1:8010/health
```

Остановите тестовый процесс (Ctrl+C), дальше — systemd.

---

## 5. Frontend

```bash
cd /opt/streaming/frontend
npm ci
npm run build
```

По умолчанию API и WebSocket идут на **тот же хост** (`/api/v1`, относительные пути) — для продакшена за nginx **отдельный `VITE_API_BASE` обычно не нужен**.

---

## 6. systemd

Скопируйте пример и подставьте пути/пользователя:

```bash
sudo cp /opt/streaming/deploy/streaming-backend.service.example /etc/systemd/system/streaming-backend.service
sudo nano /etc/systemd/system/streaming-backend.service   # User, WorkingDirectory, порт
sudo systemctl daemon-reload
sudo systemctl enable --now streaming-backend
sudo systemctl status streaming-backend
```

---

## 7. nginx + HTTPS

1. Скопируйте конфиг с подстановкой домена и путей к `dist`:

```bash
sudo cp /opt/streaming/deploy/nginx-streaming-site.conf.example /etc/nginx/sites-available/streaming.conf
sudo nano /etc/nginx/sites-available/streaming.conf
sudo ln -sf /etc/nginx/sites-available/streaming.conf /etc/nginx/sites-enabled/streaming.conf
sudo nginx -t
```

2. Первый запуск можно сделать **только HTTP** (certbot сам допишет SSL), либо сразу:

```bash
sudo certbot --nginx -d ВАШ_ПОДДОМЕН
```

3. Перезагрузка:

```bash
sudo systemctl reload nginx
```

Откройте в браузере `https://ВАШ_ПОДДОМЕН`, войдите под учёткой из seed и **смените пароли**.

---

## 8. Обновление после `git pull`

```bash
cd /opt/streaming
git pull
cd backend && source .venv/bin/activate && pip install -r requirements.txt && alembic upgrade head && deactivate
cd ../frontend && npm ci && npm run build
sudo systemctl restart streaming-backend
sudo nginx -t && sudo systemctl reload nginx
```

---

## 9. Альтернатива: Docker Compose на сервере

Если на VPS установите **Docker Engine + compose plugin**, можно поднять **`db` + `backend`** из `docker-compose.yml`, а **фронт и TLS** оставить на **системном nginx** (контейнерный nginx из compose на проде часто не нужен — на одном хосте уже слушает `:80/:443`). Этот путь требует отдельной правки compose (не биндить 80, пробросить бэкенд на `127.0.0.1:8010`). Текущий репозиторий ориентирован на **docker для разработки**; прод-стек выше — **systemd + nginx** — проще стыкуется с уже занятыми vhost’ами на `xkvlorcrjx`.

---

## Чеклист безопасности

- [ ] `JWT_SECRET` уникальный и длинный  
- [ ] Пароли seed-пользователей изменены  
- [ ] `REFRESH_COOKIE_SECURE=true`  
- [ ] `CORS_ORIGINS` только ваш HTTPS-оригин  
- [ ] PostgreSQL не торчит в интернет (`ss` / UFW)  
- [ ] Резервные копии БД по расписанию (`pg_dump`)
