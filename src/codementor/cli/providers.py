"""`codementor providers check` (mimari §10).

Ollama gerçekten sorgulanır (`GET /api/tags`): sunucu erişilebilir mi, yapılandırılan model
çekilmiş mi. Bulut sağlayıcılar için ağa çıkılmaz: model tanımlı mı ve anahtar ortam değişkeni
dolu mu denetlenir; anahtarın değeri asla yazdırılmaz.

Çıkış kodları: 0 birincil sağlayıcı hazır · 1 hazır değil · 2 geçersiz komut/sağlayıcı ·
3 yapılandırma okunamadı.
"""

from __future__ import annotations

import asyncio
import os
import tomllib
from pathlib import Path
from typing import Annotated
from urllib.parse import urlsplit

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.markup import escape
from rich.table import Table

from codementor.config import ProvidersSettings, load_settings
from codementor.models.provider import ProviderStatus
from codementor.providers._http import HttpTransport
from codementor.providers.base import ProviderError, RetryPolicy
from codementor.providers.cli_agent import resolve_executable
from codementor.providers.factory import PROVIDER_NAMES, chain_names
from codementor.providers.ollama import DEFAULT_NUM_CTX, OllamaProvider

CLI_AGENTS = ("claude_cli", "agy")
HEALTH_TIMEOUT_S = 5  # erişilemeyen adres CLI'yı 2 dakika askıda tutmasın
EXIT_NOT_READY = 1
EXIT_USAGE = 2
EXIT_SYSTEM_ERROR = 3

providers_app = typer.Typer(name="providers", no_args_is_help=True, help="LLM sağlayıcıları.")


async def _check_ollama(providers: ProvidersSettings) -> ProviderStatus:
    cfg = providers.ollama
    model = cfg.model.strip()
    if not model:
        return ProviderStatus(name="ollama", model="—", ready=False, detail="model tanımlı değil")
    try:
        transport = HttpTransport("ollama", HEALTH_TIMEOUT_S, RetryPolicy(max_retries=0))
        available = await OllamaProvider(cfg, transport=transport).list_models()
    except ProviderError as exc:
        reason = str(exc).removeprefix("ollama: ")
        return ProviderStatus(
            name="ollama",
            model=model,
            ready=False,
            detail=f"{_origin(cfg.base_url)} erişilemiyor ({reason}); `ollama serve` çalışıyor mu?",
        )
    wanted = {model, f"{model}:latest"} if ":" not in model else {model}
    if not wanted & set(available):
        return ProviderStatus(
            name="ollama", model=model, ready=False, detail=f"model çekilmemiş: ollama pull {model}"
        )
    num_ctx = cfg.num_ctx or DEFAULT_NUM_CTX
    return ProviderStatus(
        name="ollama",
        model=model,
        ready=True,
        detail=f"erişilebilir, {len(available)} yerel model, num_ctx={num_ctx}",
    )


def _origin(url: str | None) -> str:
    """`http://kullanici:parola@host:11434/yol` → `http://host:11434` (kimlik bilgisi basılmaz)."""
    parts = urlsplit(url or "")
    if not parts.hostname:
        return "(adres yok)"
    port = f":{parts.port}" if parts.port else ""
    return f"{parts.scheme}://{parts.hostname}{port}"


def _check_cloud(name: str, providers: ProvidersSettings) -> ProviderStatus:
    cfg = getattr(providers, name)
    model = cfg.model.strip()
    if not model:
        return ProviderStatus(
            name=name, model="—", ready=False, detail=f"model tanımlı değil ([providers.{name}])"
        )
    env = cfg.api_key_env or "—"
    if not cfg.api_key_env or not os.environ.get(cfg.api_key_env, "").strip():
        return ProviderStatus(
            name=name, model=model, ready=False, detail=f"{env} ortam değişkeni tanımlı değil"
        )
    return ProviderStatus(
        name=name, model=model, ready=True, detail=f"{env} tanımlı (ağ denetimi yapılmadı)"
    )


def _check_cli_agent(name: str, providers: ProvidersSettings) -> ProviderStatus:
    """CLI ajanı: çalıştırılabilir çözülür (`.cmd` → `.exe`); oturum denetlenmez (ağsız)."""
    cfg = getattr(providers, name)
    model = cfg.model.strip() or "—"
    if model == "—":
        return ProviderStatus(
            name=name, model=model, ready=False, detail=f"model tanımlı değil ([providers.{name}])"
        )
    try:
        path = resolve_executable(name, cfg.command)
    except ProviderError as exc:
        return ProviderStatus(
            name=name, model=model, ready=False, detail=str(exc).removeprefix(f"{name}: ")
        )
    note = " (deneysel, ADR-0012)" if name == "agy" else ""
    return ProviderStatus(
        name=name,
        model=model,
        ready=True,
        detail=f"{Path(path).name} bulundu; oturum denetlenmedi{note}",
    )


async def check_providers(names: list[str], providers: ProvidersSettings) -> list[ProviderStatus]:
    """Sağlayıcıların hazır olup olmadığı (Ollama gerçekten sorgulanır)."""
    statuses: list[ProviderStatus] = []
    for name in names:
        if name == "ollama":
            statuses.append(await _check_ollama(providers))
        elif name in CLI_AGENTS:
            statuses.append(_check_cli_agent(name, providers))
        else:
            statuses.append(_check_cloud(name, providers))
    return statuses


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
        typer.echo(
            f"Hata: bilinmeyen sağlayıcı: {', '.join(unknown)} "
            f"(seçenekler: {', '.join(PROVIDER_NAMES)})",
            err=True,
        )
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
