# Инвентаризация сервера `xkvlorcrjx`

Документ для быстрой ориентации: **где какой проект, порты, пути**. Перед критичными действиями на живой машине перепроверьте: `sudo ss -tulpn`, `ls /etc/nginx/sites-enabled/`, `systemctl list-units --type=service`.

**Последнее обновление описания:** март 2026 (данные из снимков `ss`, `df`, `du`, гайда `SERVER_GUIDE_XKVLORCRJX`).

---

## 1. Железо и ОС

| Параметр | Значение |
|----------|----------|
| Hostname | `xkvlorcrjx` |
| ОС | Ubuntu **22.04** LTS (Jammy), ядро **5.15** |
| Архитектура | x86_64 |
| CPU | **2** vCPU |
| RAM | ~**4.8 GiB** |
| Диск `/` | ~**49 GiB** (ориентир: ~50–60% занятости после обслуживания) |
| Docker | **не используется** (приложения на хосте: venv + systemd + nginx) |

---

## 2. Точки входа и инфраструктура

| Компонент | Назначение |
|-----------|------------|
| **nginx** | Публичный HTTP/HTTPS **:80**, **:443**; reverse proxy на приложения на localhost |
| **PostgreSQL** | Обычно **`127.0.0.1:5432`** — снаружи не должен быть нужен |
| **Redis** | **`127.0.0.1:6379`** |
| **OpenSSH** | **:22** и **:2222** (два порта; в UFW настроены правила) |
| **vsftpd** | **:21** FTP (оцените необходимость; альтернатива — SFTP) |

---

## 3. Таблица портов → процесс (снимок `ss`)

Колонка **Bind** показывает, с какого интерфейса принимаются соединения: **`0.0.0.0`** = все интерфейсы (снаружи доступно, если UFW не режет); **`127.0.0.1`** = только локально (нормально за nginx).

| Порт | Bind | Процесс (тип) | Назначение (по снимкам/гайду) |
|------|------|----------------|--------------------------------|
| 21 | `*` | vsftpd | FTP |
| 22 | 0.0.0.0 | sshd | SSH |
| 2222 | 0.0.0.0 | sshd | SSH (доп. порт) |
| 80, 443 | 0.0.0.0 | nginx | Веб-вход |
| 3000 | 0.0.0.0 | next-server | Next.js (судьи / judges) |
| 5000 | 0.0.0.0 | python3 | figurebase.ru |
| 5002 | 0.0.0.0 | gunicorn | **MainStream Shop** (Flask), `mainstreamfs.ru` |
| 5003 | 127.0.0.1 | gunicorn | calc.edelweissconsent.ru |
| 6060 | 127.0.0.1 | uvicorn/python | docs.dirffk.ru |
| 6379 | 127.0.0.1 | redis-server | Кэш/очереди |
| 7000 | 127.0.0.1 | gunicorn | calc.figurebase.ru |
| 8000 | 127.0.0.1 | uvicorn | consent.danfs.ru |
| 8001 | 127.0.0.1 | uvicorn | dirffk.ru (ffkm-admin backend) |
| 8002 | 127.0.0.1 | uvicorn | secrffkm.ru |
| 8003 | 127.0.0.1 | uvicorn | consentffkm.ru |
| **8010** | **127.0.0.1** | **uvicorn** | **Панель MainStream Ops** (`streaming` репозиторий), systemd **`streaming-backend`** |
| 8100 | 127.0.0.1 | uvicorn | API cartoteka / judgesffkm |
| 8101 | 0.0.0.0 | uvicorn | judges_bot_v2 API (лучше привязать к 127.0.0.1 + nginx) |
| 9000 | 0.0.0.0 | uvicorn | edelweissconsent.ru |
| 5432 | 127.0.0.1 | postgres | БД |

**Примечание:** порт **8501** (Streamlit mychamp) был снят; конфиг nginx **mychamp** отключён, файл в `sites-available` удалить/переименовать при желании.

---

## 4. Домены nginx → upstream (по гайду)

Файлы конфигов: ` /etc/nginx/sites-available/`, активные симлинки в **`sites-enabled/`**.

| Домен / конфиг | Upstream |
|----------------|----------|
| figurebase.ru | `http://127.0.0.1:5000` |
| edelweissconsent.ru | `http://127.0.0.1:9000` |
| calc.edelweissconsent.ru | `http://127.0.0.1:5003` |
| judgesffkm | `http://127.0.0.1:8100/api/` |
| judges (несколько location) | `http://127.0.0.1:3000`, `http://127.0.0.1:8101` |
| dirffk.ru | `http://127.0.0.1:8001` |
| docs.dirffk.ru | `http://127.0.0.1:6060` |
| **mainstreamfs.ru** | `http://127.0.0.1:5002` (+ статика/загрузки в конфиге) |
| consent.danfs.ru | `http://127.0.0.1:8000` |
| secrffkm.ru | `http://127.0.0.1:8002` |
| consentffkm.ru | `http://127.0.0.1:8003` |
| calc.figurebase.ru | `http://127.0.0.1:7000` |

**Поддомен под панель streaming** (например `ops.mainstreamfs.ru` или отдельный домен) — отдельный `server_name` в nginx с `proxy_pass http://127.0.0.1:8010` и заголовками `X-Forwarded-*` (см. `docs/DEPLOY_PRODUCTION.md`).

---

## 5. Проекты и пути на диске

| Путь | Что это |
|------|---------|
| **`/opt/streaming`** | Монорепозиторий **MainStream Ops** (FastAPI + React): `backend/`, `frontend/`, venv `backend/.venv`, прод-статика после `npm run build` в `frontend/dist` |
| **`/root/mainstreamfs.ru`** | Существующий **MainStream Shop** (Flask/Gunicorn **:5002**), не путать с `/opt/streaming` |
| `/var/www/ffkm-admin` | Админка FFKM (~гигабайты; подкаталог `backend/backups/` — ежедневные `ffkm_backup_*.tar.gz`) |
| `/var/www/figurebase.ru` | Сайт figurebase |
| `/var/www/calc.figurebase.ru` | Калькулятор; рядом может быть `calc.figurebase.ru.backup` |
| `/opt/cartoteka` | Проект cartoteka (frontend/backend) |
| `/opt/ffkm-consent`, `/opt/ffkm-consent-coaches-judges` | Сервисы согласий |
| `/opt/edelweiss-consent` | Edelweiss consent |
| `/opt/secretary-portal` | Секретариат |
| `/opt/docsffkm` | Документация (docs) |
| `/root/judges_bot_v2` | Бот/веб judges (порты 8101 / 3000 в связке с nginx) |
| `/root/msphoto`, `/root/bot_gpt`, `/root/ffkm_feedback`, и т.д. | Прочие утилиты/боты |

Загрузки для streaming (если настроено в `.env`): часто **`/var/lib/streaming/uploads`** — см. `UPLOAD_DIR` в `backend/.env`.

---

## 6. MainStream Ops (`/opt/streaming`) — кратко

| Что | Где |
|-----|-----|
| Backend | `cd /opt/streaming/backend`, venv: `source .venv/bin/activate` |
| Конфиг | `/opt/streaming/backend/.env` (в т.ч. `DATABASE_URL`, `JWT_SECRET`) |
| Миграции | `alembic upgrade head` |
| systemd | `streaming-backend.service` → `uvicorn` на **`127.0.0.1:8010`** |
| Перезапуск | `sudo systemctl restart streaming-backend` |
| Обновление кода | `git pull` → `pip install` → `alembic` → `npm ci && npm run build` → restart backend → `reload nginx` |

Подробнее: **`docs/DEPLOY_PRODUCTION.md`**, **`docs/SERVER_COPYPASTE.md`**.

---

## 7. systemd-сервисы (по именам)

Проверка на сервере:

```bash
systemctl list-units --type=service --state=running | grep -iE 'nginx|postgres|streaming|redis'
```

Ожидаемо в проде: **`nginx`**, **`postgresql`**, **`streaming-backend`** (если панель развёрнута), **`redis-server`**, при необходимости **`vsftpd`**.

---

## 8. Логи и обслуживание

| Задача | Команда |
|--------|---------|
| Логи backend панели | `sudo journalctl -u streaming-backend -n 200 --no-pager` |
| Логи nginx | `/var/log/nginx/access.log`, `error.log` |
| Журнал systemd (размер) | `journalctl --disk-usage` |
| Ограничить журнал | см. drop-in `journald.conf.d` с `SystemMaxUse=500M` |
| Проверка nginx | `sudo nginx -t && sudo systemctl reload nginx` |
| Порты | `sudo ss -tulpn` |

---

## 9. Безопасность — напоминание

- Сервисы на **`0.0.0.0`** (5000, 5002, 3000, 8101, 9000, …) при открытом UFW на эти порты доступны **напрямую по IP**; предпочтительно **127.0.0.1** + только **80/443** снаружи.
- **PostgreSQL** не должен быть в UFW как `ALLOW` для всего интернета, если слушает только localhost.
- Регулярные **обновления**: `apt update && apt upgrade` (в окне обслуживания).

---

## 10. Резерв под новые сервисы

Свободные порты **не зафиксированы навсегда** — перед запуском:

```bash
ss -tlnp | grep ':ВАШ_ПОРТ'
```

Диапазон **8010** уже занят панелью streaming; для нового сервиса выберите другой порт и пропишите в nginx.

---

*При смене сервера или крупных правках обновите таблицы портов и путей по свежему выводу команд.*
