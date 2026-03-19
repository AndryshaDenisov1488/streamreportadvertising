# Пересоздать PostgreSQL и сид с новыми почтами

## 1. Пропишите почты в `backend/.env` на сервере

Добавьте (или отредактируйте) строки:

```env
SEED_ADMIN_EMAIL=ваш-суперадмин@домен.ru
SEED_MANAGER_EMAIL=менеджер@домен.ru
SEED_OPERATOR_EMAIL=оператор@домен.ru
SEED_PASSWORD=НадёжныйВременныйПароль123
```

Пароль стартовый один для трёх учёток — после первого входа смените у каждого пользователя в интерфейсе.

## 2. Остановите API и снимите подключения к БД

```bash
systemctl stop streaming-backend
sudo -u postgres psql -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'streaming' AND pid <> pg_backend_pid();"
sudo -u postgres psql -d postgres -c "DROP DATABASE IF EXISTS streaming;"
sudo -u postgres psql -d postgres -c "CREATE DATABASE streaming OWNER streaming;"
sudo -u postgres psql -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE streaming TO streaming;"
```

Если пользователь PostgreSQL называется иначе — подставьте своего владельца в `CREATE DATABASE`.

## 3. Миграции и сид

```bash
cd /opt/streaming/backend
source .venv/bin/activate
set -a && source .env && set +a
alembic upgrade head
python -m scripts.seed
deactivate
systemctl start streaming-backend
```

## 4. Проверка

```bash
curl -s http://127.0.0.1:8010/health
```

Войдите на сайт под новыми email из `.env`.
