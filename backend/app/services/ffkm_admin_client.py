"""HTTP-клиент к ffkm-admin Integration API (календарь турниров)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from urllib.parse import urljoin

import httpx

from app.core.config import get_settings


class FfkmAdminClientError(RuntimeError):
    """Базовая ошибка клиента ffkm-admin."""


class FfkmAdminClientAuthError(FfkmAdminClientError):
    """Неверный/отозванный integration token."""


class FfkmAdminClient:
    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_token: str | None = None,
        timeout: float | None = None,
    ) -> None:
        settings = get_settings()
        self.base_url = (base_url if base_url is not None else settings.ffkm_admin_api_base_url or "").rstrip(
            "/"
        )
        self.api_token = (
            api_token if api_token is not None else settings.ffkm_admin_api_token or ""
        ).strip()
        self.timeout = (
            timeout if timeout is not None else float(settings.ffkm_admin_timeout_seconds)
        )

    def _headers(self) -> dict[str, str]:
        if not self.api_token:
            raise FfkmAdminClientAuthError("Не задан FFKM_ADMIN_API_TOKEN")
        return {
            "Accept": "application/json",
            "X-API-Token": self.api_token,
        }

    async def list_tournaments_page(
        self,
        *,
        page: int = 1,
        size: int = 200,
        updated_since: datetime | None = None,
    ) -> dict[str, Any]:
        if not self.base_url:
            raise FfkmAdminClientError("Не задан FFKM_ADMIN_API_BASE_URL")

        url = urljoin(f"{self.base_url}/", "api/v1/integration/tournaments")
        params: dict[str, Any] = {"page": page, "size": min(max(size, 1), 200)}
        if updated_since is not None:
            params["updated_since"] = updated_since.isoformat()

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=self._headers(),
                    params=params,
                    timeout=self.timeout,
                    follow_redirects=True,
                )
        except httpx.HTTPError as exc:
            raise FfkmAdminClientError(f"Ошибка запроса к ffkm-admin: {exc}") from exc

        if response.status_code in (401, 403):
            raise FfkmAdminClientAuthError(
                f"ffkm-admin отклонил токен (HTTP {response.status_code})"
            )
        if response.status_code >= 400:
            detail = response.text[:300]
            raise FfkmAdminClientError(f"ffkm-admin HTTP {response.status_code}: {detail}")

        data = response.json()
        if not isinstance(data, dict):
            raise FfkmAdminClientError("Некорректный ответ integration API")
        return data

    async def iter_all_tournaments(
        self,
        *,
        page_size: int = 200,
        updated_since: datetime | None = None,
    ) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        page = 1
        total: int | None = None

        while True:
            payload = await self.list_tournaments_page(
                page=page,
                size=page_size,
                updated_since=updated_since,
            )
            batch = payload.get("items") or []
            if not isinstance(batch, list):
                raise FfkmAdminClientError("Поле items должно быть списком")
            items.extend(batch)

            if total is None:
                try:
                    total = int(payload.get("total") or 0)
                except (TypeError, ValueError):
                    total = len(items)

            if not batch or len(items) >= (total or 0) or len(batch) < page_size:
                break
            page += 1
            if page > 500:
                raise FfkmAdminClientError("Слишком много страниц integration API")

        return items
