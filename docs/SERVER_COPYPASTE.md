# Команды на пустом сервере (Ubuntu 22.04+, с нуля)

Подставьте **один раз** в начале сессии SSH:

```bash
# ОБЯЗАТЕЛЬНО замените на ваш поддомен (DNS A-запись уже должна смотреть на IP сервера)
export DOMAIN="ops.mainstreamfs.ru"
```

Репозиторий: `https://github.com/AndryshaDenisov1488/streamreportadvertising.git`  
Каталог приложения: `/opt/streaming`  
Бэкенд: `127.0.0.1:8010`

---

## 1. Пакеты

```bash
sudo apt update
sudo apt install -y nginx certbot python3-venv python3-pip postgresql postgresql-contrib curl git software-properties-common
```

Node.js 20:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node -v
```

---

## 2. PostgreSQL: пользователь, база, пароль

Пароль для пользователя БД генерируется один раз и показывается — **сохраните** (понадобится для `.env`).

```bash
export DB_PASS="$(openssl rand -base64 32)"
echo "Пароль БД (сохраните): $DB_PASS"

sudo -u postgres psql <<EOSQL
CREATE USER streaming WITH PASSWORD '${DB_PASS}';
CREATE DATABASE streaming OWNER streaming;
GRANT ALL PRIVILEGES ON DATABASE streaming TO streaming;
EOSQL
```

---

## 3. Клонирование кода и каталог загрузок

```bash
sudo mkdir -p /opt/streaming
sudo chown "$USER":"$USER" /opt/streaming

git clone https://github.com/AndryshaDenisov1488/streamreportadvertising.git /opt/streaming

sudo mkdir -p /var/lib/streaming/uploads
sudo chown "$USER":"$USER" /var/lib/streaming/uploads
```

---

## 4. Backend (venv, зависимости, миграции)

```bash
cd /opt/streaming/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Секрет JWT:

```bash
export JWT_SECRET="$(openssl rand -hex 48)"
echo "JWT_SECRET (уже подставится в .env ниже, при желании сохраните): $JWT_SECRET"
```

Создайте `/opt/streaming/backend/.env` (заменит переменные из текущей shell-сессии: `DOMAIN`, `DB_PASS`, `JWT_SECRET`):

```bash
cat > /opt/streaming/backend/.env <<EOF
DATABASE_URL=postgresql+asyncpg://streaming:${DB_PASS}@127.0.0.1:5432/streaming
DATABASE_URL_SYNC=postgresql://streaming:${DB_PASS}@127.0.0.1:5432/streaming
JWT_SECRET=${JWT_SECRET}
JWT_ACCESS_EXPIRE_MINUTES=30
JWT_REFRESH_EXPIRE_DAYS=7
CORS_ORIGINS=https://${DOMAIN}
REFRESH_COOKIE_NAME=refresh_token
REFRESH_COOKIE_SECURE=true
REFRESH_COOKIE_SAMESITE=lax
TZ=Europe/Moscow
APP_VERSION=1.0.0
UPLOAD_DIR=/var/lib/streaming/uploads
EOF

chmod 600 /opt/streaming/backend/.env
```

Миграции и начальные данные:

```bash
cd /opt/streaming/backend
source .venv/bin/activate
set -a && source .env && set +a
alembic upgrade head
python -m scripts.seed
deactivate
```

---

## 5. Сборка фронтенда

```bash
cd /opt/streaming/frontend
npm ci
npm run build
```

---

## 6. systemd

```bash
sudo tee /etc/systemd/system/streaming-backend.service > /dev/null <<'EOF'
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
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now streaming-backend
sudo systemctl status streaming-backend --no-pager
```

Проверка API:

```bash
curl -s http://127.0.0.1:8010/health
```

---

## 7. nginx (HTTP для certbot; подставляется `$DOMAIN`)

```bash
sudo tee /etc/nginx/sites-available/streaming.conf > /dev/null <<EOF
map \$http_upgrade \$connection_upgrade {
    default upgrade;
    ''      close;
}

map \$http_x_request_id \$proxy_request_id {
    default \$http_x_request_id;
    ''      \$request_id;
}

server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAIN};

    root /opt/streaming/frontend/dist;
    index index.html;

    location /api/ {
        proxy_pass http://127.0.0.1:8010;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Request-ID \$proxy_request_id;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection \$connection_upgrade;
        proxy_read_timeout 86400;
    }

    location /health {
        proxy_pass http://127.0.0.1:8010;
        proxy_set_header Host \$host;
        proxy_set_header X-Request-ID \$proxy_request_id;
    }

    location /openapi.json {
        proxy_pass http://127.0.0.1:8010;
        proxy_set_header Host \$host;
    }

    location /uploads/ {
        proxy_pass http://127.0.0.1:8010;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self' ws: wss: http: https:; font-src 'self' data:; frame-ancestors 'self'; base-uri 'self'" always;
}
EOF

sudo ln -sf /etc/nginx/sites-available/streaming.conf /etc/nginx/sites-enabled/streaming.conf
sudo nginx -t
sudo systemctl reload nginx
```

Если включён дефолтный сайт и мешает — отключите:

```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
```

---

## 8. HTTPS (Let’s Encrypt)

```bash
sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m YOUR_EMAIL@example.com --redirect
```

Замените `YOUR_EMAIL@example.com` на вашу почту (для уведомлений certbot).

---

## 9. Финальная проверка

```bash
curl -sS "https://${DOMAIN}/health"
```

В браузере откройте `https://$DOMAIN`, войдите под учёткой из seed и **смените пароли**.

Учётные данные по умолчанию (после `scripts.seed`) — см. `README.md` в репозитории.

---

## Обновление кода позже

```bash
cd /opt/streaming
git pull
cd backend && source .venv/bin/activate && pip install -r requirements.txt && set -a && source .env && set +a && alembic upgrade head && deactivate
cd ../frontend && npm ci && npm run build
sudo systemctl restart streaming-backend
sudo nginx -t && sudo systemctl reload nginx
```
