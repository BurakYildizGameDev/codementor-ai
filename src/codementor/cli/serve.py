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
from codementor.api.auth import configured_key
from codementor.config import Settings, load_settings

EXIT_SYSTEM_ERROR = 3


def is_loopback(host: str) -> bool:
    """`127.0.0.1`, `::1`, `localhost` → True; `0.0.0.0` ve diğerleri False."""
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def exposure_warning(settings: Settings, host: str) -> str | None:
    """Dışa açık bağlamada gerçek korumaları anlatan uyarı; loopback'te None (Faz 47)."""
    if is_loopback(host):
        return None
    parts = [f"{host} yerel olmayan bağlantılara açık."]
    if configured_key(settings) is None:
        parts.append(
            "API anahtarı tanımlı değil (api.api_key_env): kodunuz ve sağlayıcı kotanız "
            "ağdaki herkese açılır."
        )
    if not settings.api.allowed_hosts:
        parts.append(
            "api.allowed_hosts boş: yalnız loopback Host başlıkları kabul edilir, uzak istekler "
            "400 alır."
        )
    parts.append("Bkz. mimari §12.")
    return " ".join(parts)


def serve(
    host: Annotated[
        str | None, typer.Option(help="Bağlanılacak adres (varsayılan: api.host).")
    ] = None,
    port: Annotated[int | None, typer.Option(help="Port (varsayılan: api.port).")] = None,
    insecure: Annotated[
        bool,
        typer.Option("--insecure", help="Dışa açık adrese anahtarsız bağlanmaya izin ver."),
    ] = False,
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
    if not is_loopback(bind_host) and configured_key(settings) is None:
        if not insecure:
            console.print(
                "[red]Hata:[/red] Dışa açık adrese anahtarsız bağlanılamaz. "
                "[api] api_key_env ayarlayın ya da --insecure verin."
            )
            raise typer.Exit(EXIT_SYSTEM_ERROR)
        console.print(
            "[yellow]Uyarı:[/yellow] Dışa açık adrese anahtarsız bağlanılıyor (--insecure etkin)."
        )
    warning = exposure_warning(settings, bind_host)
    if warning is not None:
        console.print(f"[yellow]Uyarı:[/yellow] {warning}")
    console.print(f"CodeMentor API: http://{bind_host}:{bind_port}/docs")
    uvicorn.run(create_app(settings), host=bind_host, port=bind_port, log_level="warning")
