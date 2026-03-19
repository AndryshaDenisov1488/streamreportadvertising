import logging
import uuid
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("app.request")


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Пробрасывает X-Request-ID: из заголовка или генерирует UUID, кладёт в request.state и ответ."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        rid = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = rid
        response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        return response
