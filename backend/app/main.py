from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.health import router as health_router
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.services.report_scheduler import setup_report_scheduler
from app.core.limiter import limiter
from app.middleware.request_id import RequestIDMiddleware
from app.websocket.hub import StreamEventHub


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    app.state.ws_hub = StreamEventHub()
    app.state.report_scheduler = setup_report_scheduler()
    yield
    sched = getattr(app.state, "report_scheduler", None)
    if sched is not None:
        sched.shutdown(wait=False)


def create_app() -> FastAPI:
    settings = get_settings()
    if settings.sentry_dsn:
        try:
            import sentry_sdk

            sentry_sdk.init(
                dsn=settings.sentry_dsn,
                environment=settings.sentry_environment,
                release=settings.app_version,
                traces_sample_rate=settings.sentry_traces_sample_rate,
            )
        except ImportError:
            pass

    app = FastAPI(title="Stream Sponsor Platform API", lifespan=lifespan)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIDMiddleware)

    app.include_router(health_router)
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    # SEC-MEDIA-004: do not mount public StaticFiles for /uploads.
    # Logos/avatars are served via /api/v1/media/... (signed URL or Bearer auth).
    upload_root = Path(settings.upload_dir)
    upload_root.mkdir(parents=True, exist_ok=True)
    return app


app = create_app()
