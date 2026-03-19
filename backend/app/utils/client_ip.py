"""Клиентский IP за reverse-proxy (nginx): X-Forwarded-For, затем X-Real-IP, затем peer."""

from fastapi import Request


def client_ip_from_request(request: Request) -> str | None:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        first = xff.split(",")[0].strip()
        if first:
            return first[:45]
    xri = request.headers.get("x-real-ip")
    if xri:
        return xri.strip()[:45]
    if request.client:
        return request.client.host[:45] if request.client.host else None
    return None
