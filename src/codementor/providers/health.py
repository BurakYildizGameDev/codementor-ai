"""Sağlayıcı hazır mı? (CLI `providers check` ve API `/v1/providers`, `/health/ready`).

Ollama gerçekten sorgulanır (`GET /api/tags`): sunucu erişilebilir mi, yapılandırılan model
çekilmiş mi. Bulut sağlayıcılar için ağa çıkılmaz: model tanımlı mı ve anahtar ortam değişkeni
dolu mu denetlenir; anahtarın değeri asla yazdırılmaz. Sağlayıcının kapattığı model adları
(`data/retired_models.yaml`) anahtardan önce yakalanır (Faz 28).
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit

import yaml

from codementor.config import ProvidersSettings
from codementor.models.provider import ProviderStatus
from codementor.paths import resource_path
from codementor.providers._http import HttpTransport
from codementor.providers.base import ProviderError, RetryPolicy
from codementor.providers.cli_agent import resolve_executable
from codementor.providers.ollama import DEFAULT_NUM_CTX, OllamaProvider

CLI_AGENTS = ("claude_cli", "agy", "codex")
RETIRED_MODELS_FILE = resource_path("data/retired_models.yaml")
HEALTH_TIMEOUT_S = 5  # erişilemeyen adres 2 dakika askıda tutmasın


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
            detail=f"{origin(cfg.base_url)} erişilemiyor ({reason}); `ollama serve` çalışıyor mu?",
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


def origin(url: str | None) -> str:
    """`http://kullanici:parola@host:11434/yol` → `http://host:11434` (kimlik bilgisi basılmaz)."""
    parts = urlsplit(url or "")
    if not parts.hostname:
        return "(adres yok)"
    port = f":{parts.port}" if parts.port else ""
    return f"{parts.scheme}://{parts.hostname}{port}"


def load_retired_models(path: Path | None = None) -> dict[str, dict[str, str]]:
    """Kaldırılmış model adları (sağlayıcı → {ad: açıklama}); dosya yoksa ya da bozuksa boş."""
    return dict(_load_retired(path or RETIRED_MODELS_FILE))


@lru_cache(maxsize=4)
def _load_retired(path: Path) -> dict[str, dict[str, str]]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {
        str(provider): {str(k): str(v) for k, v in models.items()}
        for provider, models in data.items()
        if isinstance(models, dict)
    }


# Canlı doğrulanmamış sağlayıcılar (ADR-0021): durum metninde işaretlenir
EXPERIMENTAL_NOTES = {"agy": " (deneysel, ADR-0012)", "gemini": " (deneysel, ADR-0020)"}


def _check_cloud(name: str, providers: ProvidersSettings) -> ProviderStatus:
    cfg = getattr(providers, name)
    model = cfg.model.strip()
    if not model:
        return ProviderStatus(
            name=name, model="—", ready=False, detail=f"model tanımlı değil ([providers.{name}])"
        )
    retired = load_retired_models().get(name, {}).get(model)
    if retired is not None:
        return ProviderStatus(name=name, model=model, ready=False, detail=retired)
    env = cfg.api_key_env or "—"
    if not cfg.api_key_env or not os.environ.get(cfg.api_key_env, "").strip():
        return ProviderStatus(
            name=name, model=model, ready=False, detail=f"{env} ortam değişkeni tanımlı değil"
        )
    note = EXPERIMENTAL_NOTES.get(name, "")
    return ProviderStatus(
        name=name, model=model, ready=True, detail=f"{env} tanımlı (ağ denetimi yapılmadı){note}"
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
    note = {**EXPERIMENTAL_NOTES, "codex": " (araç ajanı, ADR-0017)"}.get(name, "")
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
