"""HTTP transport entry point for cia hosting, guarded by X-API-Key.

Mirrors reed's ApiKeyMiddleware pattern (src/reed/mcp_server.py in the
reed repo): a pure-ASGI wrapper around FastMCP's own http_app(), since
the mounted MCP app is a Starlette sub-app rather than routes that can
take a Depends().
"""
from __future__ import annotations

import os
import secrets

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from .server import mcp

API_KEY = os.environ.get("RAINKEEPER_API_KEY", "")


class ApiKeyMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        if API_KEY:
            headers = dict(scope["headers"])
            key = headers.get(b"x-api-key", b"").decode()
            if not secrets.compare_digest(key, API_KEY):
                response = JSONResponse({"error": "Invalid API key"}, status_code=401)
                await response(scope, receive, send)
                return
        await self.app(scope, receive, send)


app = ApiKeyMiddleware(mcp.http_app(path="/mcp"))


def main() -> None:
    import uvicorn

    uvicorn.run(
        app,
        host=os.environ.get("RAINKEEPER_HOST", "0.0.0.0"),
        port=int(os.environ.get("RAINKEEPER_PORT", "8001")),
        log_level="info",
    )


if __name__ == "__main__":
    main()
