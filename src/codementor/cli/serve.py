"""`codementor serve` (mimari §9, §12): varsayılan yalnızca 127.0.0.1."""

from __future__ import annotations

import ipaddress
import tomllib
from typing import Annotated

import typer
import uvicorn
from pydantic import ValidationError
from rich.console import Console

from codementor.api.app import create_app
from codementor.config import load_settings

EXIT_SYSTEM_ERROR = 3


def is_loopback(host: str) -> bool:
    """`127.0.0.1`, `::1`, `localhost` → True; `0.0.0.0` ve diğerleri False."""
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def serve(
    host: Annotated[
        str | None, typer.Option(help="Bağlanılacak adres (varsayılan: api.host).")
    ] = None,
    port: Annotated[int | None, typer.Option(help="Port (varsayılan: api.port).")] = None,
) -> None:
    """REST API ve SSE sunucusunu başlatır (`/docs` OpenAPI)."""
    console = Console(stderr=True)
    try:
        settings = load_settings()
    except (ValidationError, tomllib.TOMLDecodeError, OSError) as exc:
        console.print(f"[red]Hata:[/red] Yapılandırma okunamadı: {exc}")
        raise typer.Exit(EXIT_SYSTEM_ERROR) from exc
    bind_host = host or settings.api.host
    bind_port = port or settings.api.port
    if not is_loopback(bind_host):
        console.print(
            f"[yellow]Uyarı:[/yellow] {bind_host} yerel olmayan bağlantılara açık. API kimlik "
            "doğrulaması yok; kodunuz ve sağlayıcı kotanız ağdaki herkese açılır (mimari §12)."
        )
    console.print(f"CodeMentor API: http://{bind_host}:{bind_port}/docs")
    uvicorn.run(create_app(settings), host=bind_host, port=bind_port, log_level="warning")
