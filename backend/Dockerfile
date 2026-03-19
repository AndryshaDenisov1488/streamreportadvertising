FROM python:3.12-slim-bookworm
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Таймаут и зеркало: при SSLError/EOF к pypi.org задайте build-arg (см. .env.example и README)
ENV PIP_DEFAULT_TIMEOUT=300
ARG PIP_INDEX_URL=https://pypi.org/simple
RUN pip install --no-cache-dir --retries 15 --default-timeout=120 \
    -i "${PIP_INDEX_URL}" \
    -r requirements.txt

COPY alembic.ini alembic.ini
COPY alembic ./alembic
COPY app ./app
COPY scripts ./scripts

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
