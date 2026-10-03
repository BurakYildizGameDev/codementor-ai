"""`codementor providers check` (mimari §10).

Ollama gerçekten sorgulanır (`GET /api/tags`): sunucu erişilebilir mi, yapılandırılan model
çekilmiş mi. Bulut sağlayıcılar için ağa çıkılmaz: model tanımlı mı ve anahtar ortam değişkeni
dolu mu denetlenir; anahtarın değeri asla yazdırılmaz.

Çıkış kodları: 0 birincil sağlayıcı hazır · 1 hazır değil · 2 geçersiz komut/sağlayıcı ·
3 yapılandırma okunamadı.
"""

from __future__ import annotations

import asyncio
import tomllib
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from codementor.config import load_settings
from codementor.providers.factory import (
    PROVIDER_NAMES,
    chain_names,
    unknown_provider_reason,
)
from codementor.providers.health import check_providers

EXIT_NOT_READY = 1
EXIT_USAGE = 2
EXIT_SYSTEM_ERROR = 3

providers_app = typer.Typer(name="providers", no_args_is_help=True, help="LLM sağlayıcıları.")


@providers_app.command("check")
def providers_check(
    provider: Annotated[
        str | None, typer.Option("--provider", help="Yalnızca bu sağlayıcı (varsayılan: zincir).")
    ] = None,
) -> None:
    """Birincil sağlayıcıyı ve fallback zincirini denetler."""
    try:
        providers = load_settings().providers
    except (ValidationError, tomllib.TOMLDecodeError, OSError) as exc:
        typer.echo(f"Hata: yapılandırma okunamadı ({type(exc).__name__})", err=True)
        raise typer.Exit(EXIT_SYSTEM_ERROR) from exc
    names = [provider] if provider else chain_names(providers)
    unknown = [n for n in names if n not in PROVIDER_NAMES]
    if unknown:
        for name in unknown:
            typer.echo(f"Hata: {name}: {unknown_provider_reason(name)}", err=True)
        raise typer.Exit(EXIT_USAGE)
    statuses = asyncio.run(check_providers(names, providers))
    table = Table(title="Sağlayıcılar")
    for column in ("Sağlayıcı", "Model", "Durum", "Ayrıntı"):
        table.add_column(column, overflow="fold")
    for i, status in enumerate(statuses):
        label = f"{status.name} (birincil)" if i == 0 else status.name
        state = "[green]hazır[/green]" if status.ready else "[red]hazır değil[/red]"
        table.add_row(escape(label), escape(status.model), state, escape(status.detail))
    Console().print(table)
    if not statuses[0].ready:
        raise typer.Exit(EXIT_NOT_READY)
