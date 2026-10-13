"""Güvenlik başlıkları ara katmanı (mimari §9, Faz E: E6)."""

from __future__ import annotations

from starlette.types import ASGIApp, Message, Receive, Scope, Send

_HEADER_CONTENT_TYPE_OPTIONS = (b"x-content-type-options", b"nosniff")
_HEADER_REFERRER_POLICY = (b"referrer-policy", b"no-referrer")


class SecurityHeadersMiddleware:
    """Tüm HTTP yanıtlarına X-Content-Type-Options: nosniff ve
    Referrer-Policy: no-referrer ekler.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.append(_HEADER_CONTENT_TYPE_OPTIONS)
                headers.append(_HEADER_REFERRER_POLICY)
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_wrapper)
