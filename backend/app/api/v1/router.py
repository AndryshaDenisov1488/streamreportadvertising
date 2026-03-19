from fastapi import APIRouter

from app.api.v1 import audit, auth, mentions, notifications, product_analytics, reports, stats, stream_events, users, ws

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(stream_events.router)
api_router.include_router(mentions.router)
api_router.include_router(reports.router)
api_router.include_router(stats.router)
api_router.include_router(audit.router)
api_router.include_router(notifications.router)
api_router.include_router(product_analytics.router)
api_router.include_router(ws.router)
