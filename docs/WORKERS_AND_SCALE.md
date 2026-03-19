# Фоновые воркеры и масштабирование

Тяжёлые отчёты (`/reports/export.docx`, большие выборки аудита) сейчас выполняются в HTTP-запросе. При росте данных рекомендуется:

1. **Очередь задач** — вынести генерацию DOCX/массовый экспорт в **Celery + Redis/RabbitMQ** или **RQ**, отдавать клиенту `job_id` и poll/WebSocket по готовности.
2. **Кэш агрегатов** — кэшировать `/stats/operators` и сводки `/analytics/summary` в **Redis** с TTL 30–60 с.
3. **Read replicas** — при высокой нагрузке на чтение журнала аудита — реплика PostgreSQL только для отчётов.

Интеграция с Docker: отдельный сервис `worker` в `docker-compose` с тем же образом backend и командой `celery -A app.worker worker`.
