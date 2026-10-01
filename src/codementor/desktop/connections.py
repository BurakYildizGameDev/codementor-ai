"""Sağlayıcı bağlantıları (ADR-0014): anahtar kasası, model keşfi, oturum yoklaması, canlı deneme.

GUI'siz ve test edilebilir. Kurallar:
- API anahtarı yalnızca işletim sisteminin kimlik kasasında (`keyring`; Windows'ta Kimlik
  Bilgisi Yöneticisi) durur; dosyaya yazılmaz, log'a düşmez. Uygulama açılışta anahtarı yalnız
  **kendi sürecinin** ortamına koyar; sağlayıcılar anahtarı her zamanki gibi ortamdan okur.
- CLI ajanları (claude, agy) yalnız mutlak yol ve sabit argv ile, boş çalışma dizininde
  çalıştırılır (`validation.runner.run_process`).
"""

from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Protocol

import yaml

from codementor.config import ProvidersSettings, Settings
from codementor.log import register_secret
from codementor.models.desktop import ConnectionPing, DesktopPrefs
from codementor.models.provider import ChatMessage, GenerationOptions, ProviderStatus
from codementor.paths import resource_path
from codementor.providers._http import HttpTransport
from codementor.providers.base import ProviderError, RetryPolicy
from codementor.providers.cli_agent import profile_env, resolve_executable
from codementor.providers.factory import build_provider
from codementor.providers.health import HEALTH_TIMEOUT_S, check_providers
from codementor.providers.ollama import OllamaProvider
from codementor.validation.runner import ProcessLimits, ProcessResult, run_process

KEYRING_SERVICE = "CodeMentor AI"
MODELS_FILE = resource_path("data/desktop_models.yaml")
PROBE_TIMEOUT_S = 20
NO_MODEL_DETAIL = "Önce bir model seç (listeden ya da yazarak)"
_PROBE_LIMITS = ProcessLimits(
    timeout_s=PROBE_TIMEOUT_S, memory_mb=2048, limit_address_space=False, max_processes=64
)

Kind = Literal["cli", "local", "api"]


@dataclass(frozen=True)
class ProviderInfo:
    name: str
    label: str
    kind: Kind
    blurb: str


PROVIDERS: tuple[ProviderInfo, ...] = (
    ProviderInfo("claude_cli", "Claude Code", "cli", "Claude aboneliğinle, `claude` CLI üzerinden"),
    ProviderInfo("agy", "Antigravity", "cli", "Gemini/Claude modelleri, `agy` CLI (deneysel)"),
    ProviderInfo("ollama", "Ollama", "local", "Yerel model; kod bilgisayardan çıkmaz"),
    ProviderInfo("anthropic", "Anthropic API", "api", "Claude, API anahtarıyla"),
    ProviderInfo("openai", "OpenAI API", "api", "GPT modelleri, API anahtarıyla"),
    ProviderInfo("deepseek", "DeepSeek API", "api", "DeepSeek modelleri, API anahtarıyla"),
)
INFO: dict[str, ProviderInfo] = {p.name: p for p in PROVIDERS}
API_PROVIDERS = tuple(p.name for p in PROVIDERS if p.kind == "api")

Runner = Callable[..., ProcessResult]


class KeyBackend(Protocol):
    """`keyring` modülünün kullandığımız kısmı (testlerde sahtesi verilir)."""

    def get_password(self, service_name: str, username: str) -> str | None: ...
    def set_password(self, service_name: str, username: str, password: str) -> None: ...
    def delete_password(self, service_name: str, username: str) -> None: ...


class KeyStoreError(Exception):
    """Kimlik kasasına erişilemedi; mesaj kullanıcıya dönük."""


def _default_backend() -> KeyBackend:
    import keyring

    return keyring


@dataclass
class KeyStore:
    """Sağlayıcı başına tek API anahtarı (kullanıcı adı = sağlayıcı adı)."""

    backend: KeyBackend = field(default_factory=_default_backend)

    def get(self, provider: str) -> str | None:
        try:
            return self.backend.get_password(KEYRING_SERVICE, provider) or None
        except Exception as exc:
            raise KeyStoreError(f"Kimlik kasası okunamadı ({type(exc).__name__}).") from exc

    def set(self, provider: str, key: str) -> None:
        try:
            self.backend.set_password(KEYRING_SERVICE, provider, key)
        except Exception as exc:
            raise KeyStoreError(f"Anahtar kaydedilemedi ({type(exc).__name__}).") from exc

    def delete(self, provider: str) -> None:
        try:
            self.backend.delete_password(KEYRING_SERVICE, provider)
        except Exception as exc:
            if type(exc).__name__ != "PasswordDeleteError":  # zaten yok
                raise KeyStoreError(f"Anahtar silinemedi ({type(exc).__name__}).") from exc


KeySource = Literal["vault", "environment", "missing"]


def key_env(providers: ProvidersSettings, name: str) -> str | None:
    env: str | None = getattr(providers, name).api_key_env
    return env


def key_source(providers: ProvidersSettings, name: str, vaulted: set[str]) -> KeySource:
    """Anahtar nereden geliyor: kasadan (bu uygulama koydu), dış ortamdan ya da yok."""
    if name in vaulted:
        return "vault"
    env = key_env(providers, name)
    return "environment" if env and os.environ.get(env, "").strip() else "missing"


def apply_key(providers: ProvidersSettings, name: str, key: str | None) -> None:
    """Anahtarı bu sürecin ortamına koyar ya da (None) kaldırır; log'da maskelenir."""
    env = key_env(providers, name)
    if not env:
        return
    if key:
        register_secret(key)
        os.environ[env] = key
    else:
        os.environ.pop(env, None)


def load_vault_keys(providers: ProvidersSettings, store: KeyStore) -> set[str]:
    """Açılışta kasadaki anahtarları ortama yükler; dış ortamda zaten tanımlıysa ona dokunmaz."""
    loaded: set[str] = set()
    for name in API_PROVIDERS:
        env = key_env(providers, name)
        if not env or os.environ.get(env, "").strip():
            continue
        try:
            key = store.get(name)
        except KeyStoreError:
            return loaded
        if key:
            apply_key(providers, name, key)
            loaded.add(name)
    return loaded


def apply_overrides(base: Settings, prefs: DesktopPrefs) -> Settings:
    """Arayüzde seçilen model/adres ayarlarını temel ayarların (toml + ortam) üstüne yazar."""
    data = base.providers.model_dump()
    for name, override in prefs.providers.items():
        if name in data and isinstance(data[name], dict):
            data[name].update(override.as_settings())
    return base.model_copy(update={"providers": ProvidersSettings.model_validate(data)})


def model_suggestions(path: Path = MODELS_FILE) -> dict[str, list[str]]:
    """`data/desktop_models.yaml`; okunamazsa boş (öneri yoksa alan yine serbest metindir)."""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}
    return {str(k): [str(m) for m in v] for k, v in data.items() if isinstance(v, list)}


# --- Yoklama ---------------------------------------------------------------------------------


@dataclass
class Probe:
    """Bir sağlayıcının ayrıntılı durumu (Bağlantılar kartı)."""

    status: ProviderStatus
    models: list[str] = field(default_factory=list)
    account: str | None = None  # claude_cli: oturum açan hesap

    @property
    def ready(self) -> bool:
        return self.status.ready


async def ollama_models(providers: ProvidersSettings) -> list[str]:
    transport = HttpTransport("ollama", HEALTH_TIMEOUT_S, RetryPolicy(max_retries=0))
    return await OllamaProvider(providers.ollama, transport=transport).list_models()


def parse_claude_status(stdout: str) -> tuple[bool, str | None]:
    """`claude auth status --json` → (oturum açık mı, hesap)."""
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return False, None
    if not isinstance(data, dict):
        return False, None
    account = data.get("email") or data.get("orgName")
    return bool(data.get("loggedIn")), str(account) if account else None


def parse_agy_models(stdout: str) -> list[str]:
    """`agy models` → model kimlikleri (`kimlik<TAB>açıklama` satırları)."""
    return [
        line.split("\t", 1)[0].strip()
        for line in stdout.splitlines()
        if "\t" in line and line.split("\t", 1)[0].strip()
    ]


def _run_cli(
    name: str, providers: ProvidersSettings, args: list[str], runner: Runner
) -> ProcessResult:
    executable = resolve_executable(name, getattr(providers, name).command)
    return runner([executable, *args], "", _PROBE_LIMITS, extra_env=profile_env())


async def probe(name: str, settings: Settings, runner: Runner = run_process) -> Probe:
    """Sağlayıcının hazır olup olmadığı + keşfedilen modeller + oturum bilgisi."""
    providers = settings.providers
    (status,) = await check_providers([name], providers)
    no_model = not getattr(providers, name).model.strip()
    if no_model:
        status = status.model_copy(update={"detail": NO_MODEL_DETAIL})
    result = Probe(status)
    if name == "ollama":
        with contextlib.suppress(ProviderError):  # sunucu yoksa durum zaten söylüyor
            result.models = await ollama_models(providers)
    elif name in ("claude_cli", "agy") and (status.ready or no_model):
        # model seçilmemiş olsa da oturum ve model listesi yoklanır (seçilecek liste gelsin)
        result = _probe_cli(name, providers, status, runner)
        if no_model:
            result.status = result.status.model_copy(
                update={"ready": False, "detail": f"{NO_MODEL_DETAIL} · {result.status.detail}"}
            )
    return result


def _probe_cli(
    name: str, providers: ProvidersSettings, status: ProviderStatus, runner: Runner
) -> Probe:
    args = ["auth", "status", "--json"] if name == "claude_cli" else ["models"]
    try:
        out = _run_cli(name, providers, args, runner)
    except ProviderError as exc:
        return Probe(status.model_copy(update={"ready": False, "detail": str(exc)}))
    if out.error or out.timed_out:
        detail = "yanıt vermedi (zaman aşımı)" if out.timed_out else "çalıştırılamadı"
        return Probe(status.model_copy(update={"ready": False, "detail": detail}))
    if name == "claude_cli":
        logged_in, account = parse_claude_status(out.stdout)
        detail = f"oturum açık: {account}" if logged_in and account else "oturum açık"
        if not logged_in:
            detail = "oturum açılmamış — Oturum aç'a bas"
        return Probe(status.model_copy(update={"ready": logged_in, "detail": detail}), [], account)
    models = parse_agy_models(out.stdout)
    if out.returncode != 0 or not models:
        return Probe(status.model_copy(update={"ready": False, "detail": "oturum açılmamış"}))
    allowed = providers.agy.allow_tool_agent
    detail = f"oturum açık, {len(models)} model" + ("" if allowed else " · araç onayı gerekli")
    return Probe(status.model_copy(update={"ready": allowed, "detail": detail}), models)


async def try_connection(name: str, settings: Settings) -> str:
    """Küçük gerçek bir istek gönderir; başarı ya da Türkçe hata metni döner (birkaç token)."""
    provider = build_provider(name, settings.providers, retry=RetryPolicy(max_retries=0))
    messages = [
        ChatMessage(role="system", content="Yalnızca istenen JSON nesnesini döndür."),
        ChatMessage(role="user", content='{"ok": true} döndür.'),
    ]
    try:
        result = await provider.generate_structured(
            messages, ConnectionPing, GenerationOptions(max_tokens=64, temperature=0)
        )
    except ProviderError as exc:
        return f"Başarısız: {str(exc).removeprefix(f'{name}: ')}"
    return f"Bağlantı çalışıyor ({result.model}, {result.latency_ms} ms)"


def login_command(name: str, providers: ProvidersSettings) -> list[str]:
    """Oturum açma için sabit argv (mutlak yol)."""
    executable = resolve_executable(name, getattr(providers, name).command)
    return [executable, "auth", "login"] if name == "claude_cli" else [executable]


def open_login_console(name: str, providers: ProvidersSettings) -> None:
    """Oturum açma komutunu yeni bir konsol penceresinde başlatır (etkileşimli; yalnız Windows)."""
    if sys.platform != "win32":
        raise ProviderError(name, "konsoldan oturum açma yalnızca Windows'ta destekleniyor")
    argv = login_command(name, providers)
    flags: Any = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    subprocess.Popen(argv, cwd=Path.home(), creationflags=flags, close_fds=True)
