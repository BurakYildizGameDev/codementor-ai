"""Bağlantı mantığı (ADR-0014): anahtar kasası, ayar birleştirme, CLI/Ollama yoklaması."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import httpx
import pytest
import respx

from codementor.config import Settings
from codementor.desktop import connections
from codementor.desktop.connections import (
    KeyStore,
    KeyStoreError,
    apply_overrides,
    key_source,
    load_vault_keys,
    login_command,
    model_suggestions,
    parse_agy_models,
    parse_claude_status,
    parse_codex_models,
    probe,
    try_connection,
)
from codementor.models.desktop import DesktopPrefs, ProviderOverride
from codementor.models.provider import GenerationOptions
from codementor.providers.base import RetryPolicy
from codementor.providers.fake import FakeProvider, FakeReply
from codementor.validation.runner import ProcessResult
from tests.desktop.conftest import FakeVault

EXE = sys.executable  # var olan mutlak bir çalıştırılabilir (CLI yerine; çalıştırılmaz)
AGY_ONE_MODEL = "gemini-a\tA\n"


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def cli_settings(settings: Settings, **agy: Any) -> Settings:
    providers = settings.providers.model_copy(
        update={
            "claude_cli": settings.providers.claude_cli.model_copy(
                update={"command": EXE, "model": "claude-opus-5-5"}
            ),
            "agy": settings.providers.agy.model_copy(
                update={"command": EXE, "model": "gemini", **agy}
            ),
            "codex": settings.providers.codex.model_copy(
                update={"command": EXE, "model": "gpt-5.5", **agy}
            ),
        }
    )
    return settings.model_copy(update={"providers": providers})


class FakeRunner:
    def __init__(self, stdout: str, returncode: int | None = 0, **kw: Any) -> None:
        self.result = ProcessResult(returncode, stdout, "", **kw)
        self.calls: list[list[str]] = []

    def __call__(self, argv: list[str], stdin: str, limits: object, **_: object) -> ProcessResult:
        self.calls.append(list(argv))
        return self.result


# --- Kasa -------------------------------------------------------------------------------------


def test_key_store_round_trip_and_idempotent_delete(store: KeyStore) -> None:
    assert store.get("openai") is None
    store.set("openai", "sk-abc")
    assert store.get("openai") == "sk-abc"
    store.delete("openai")
    store.delete("openai")  # yoksa sessiz
    assert store.get("openai") is None


def test_key_store_errors_are_turkish(vault: FakeVault, store: KeyStore) -> None:
    vault.broken = True
    with pytest.raises(KeyStoreError, match="okunamadı"):
        store.get("openai")
    with pytest.raises(KeyStoreError, match="kaydedilemedi"):
        store.set("openai", "x")


def test_vault_keys_fill_env_but_never_override_existing(
    settings: Settings, store: KeyStore, monkeypatch: pytest.MonkeyPatch
) -> None:
    store.set("openai", "sk-vault-openai-123")
    store.set("anthropic", "sk-vault-anthropic-123")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "dis-ortam-anahtari")
    loaded = load_vault_keys(settings.providers, store)
    assert loaded == {"openai"}
    assert os.environ["OPENAI_API_KEY"] == "sk-vault-openai-123"
    assert os.environ["ANTHROPIC_API_KEY"] == "dis-ortam-anahtari"
    assert key_source(settings.providers, "openai", loaded) == "vault"
    assert key_source(settings.providers, "anthropic", loaded) == "environment"
    assert key_source(settings.providers, "deepseek", loaded) == "missing"


def test_locked_vault_does_not_crash_startup(settings: Settings, vault: FakeVault) -> None:
    vault.broken = True
    assert load_vault_keys(settings.providers, KeyStore(vault)) == set()


# --- Ayarlar ---------------------------------------------------------------------------------


def test_overrides_merge_over_base_settings(settings: Settings) -> None:
    prefs = DesktopPrefs(
        providers={
            "ollama": ProviderOverride(model="qwen2.5-coder:14b", base_url="http://pc:11434"),
            "agy": ProviderOverride(allow_tool_agent=True),
            "bilinmeyen": ProviderOverride(model="x"),
        }
    )
    merged = apply_overrides(settings, prefs)
    assert merged.providers.ollama.model == "qwen2.5-coder:14b"
    assert merged.providers.ollama.base_url == "http://pc:11434"
    assert merged.providers.ollama.num_ctx == settings.providers.ollama.num_ctx
    assert merged.providers.agy.allow_tool_agent is True
    assert settings.providers.ollama.model != "qwen2.5-coder:14b"  # temel değişmez
    assert merged.data == settings.data


def test_model_suggestions_file(tmp_path: Path) -> None:
    assert "claude_cli" in model_suggestions()
    assert model_suggestions(tmp_path / "yok.yaml") == {}


# --- Ayrıştırma ------------------------------------------------------------------------------


def test_parse_claude_status() -> None:
    assert parse_claude_status('{"loggedIn": true, "email": "a@b.c"}') == (True, "a@b.c")
    assert parse_claude_status('{"loggedIn": false}') == (False, None)
    assert parse_claude_status("Not logged in") == (False, None)


def test_parse_agy_models() -> None:
    out = "Fetching available models...\ngemini-3.8-flash-high\tGemini\nclaude-x\tClaude\n"
    assert parse_agy_models(out) == ["gemini-3.8-flash-high", "claude-x"]


# --- Yoklama ---------------------------------------------------------------------------------


@pytest.mark.anyio
async def test_claude_probe_reports_login(settings: Settings) -> None:
    cfg = cli_settings(settings)
    run = FakeRunner('{"loggedIn": true, "email": "ogrenci@okul.edu"}')
    result = await probe("claude_cli", cfg, runner=run)
    assert result.ready
    assert result.account == "ogrenci@okul.edu"
    assert run.calls[0][1:] == ["auth", "status", "--json"]
    assert Path(run.calls[0][0]).is_absolute()

    logged_out = await probe("claude_cli", cfg, runner=FakeRunner('{"loggedIn": false}'))
    assert not logged_out.ready
    assert "Oturum aç" in logged_out.status.detail

    timeout = await probe("claude_cli", cfg, runner=FakeRunner("", None, timed_out=True))
    assert not timeout.ready


@pytest.mark.anyio
async def test_agy_probe_lists_models_and_needs_tool_consent(settings: Settings) -> None:
    out = "gemini-a\tA\ngemini-b\tB\n"
    blocked = await probe("agy", cli_settings(settings), runner=FakeRunner(out))
    assert blocked.models == ["gemini-a", "gemini-b"]
    assert not blocked.ready
    assert "araç onayı" in blocked.status.detail
    allowed = await probe(
        "agy", cli_settings(settings, allow_tool_agent=True), runner=FakeRunner(out)
    )
    assert allowed.ready
    failed = await probe("agy", cli_settings(settings), runner=FakeRunner("", 1))
    assert not failed.ready


@pytest.mark.anyio
async def test_ollama_probe_discovers_models(settings: Settings) -> None:
    providers = settings.providers.model_copy(
        update={
            "ollama": settings.providers.ollama.model_copy(
                update={"base_url": "http://ollama.test", "model": "qwen2.5-coder:14b"}
            )
        }
    )
    cfg = settings.model_copy(update={"providers": providers})
    tags = {"models": [{"name": "qwen2.5-coder:1.5b"}, {"name": "qwen2.5-coder:14b"}]}
    with respx.mock:
        respx.get("http://ollama.test/api/tags").mock(return_value=httpx.Response(200, json=tags))
        result = await probe("ollama", cfg)
    assert result.ready
    assert result.models == ["qwen2.5-coder:1.5b", "qwen2.5-coder:14b"]

    with respx.mock:
        respx.get("http://ollama.test/api/tags").mock(side_effect=httpx.ConnectError("yok"))
        down = await probe("ollama", cfg)
    assert not down.ready
    assert down.models == []


@pytest.mark.anyio
async def test_api_probe_needs_key(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    providers = settings.providers.model_copy(
        update={"openai": settings.providers.openai.model_copy(update={"model": "gpt-x"})}
    )
    cfg = settings.model_copy(update={"providers": providers})
    assert not (await probe("openai", cfg)).ready
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    assert (await probe("openai", cfg)).ready


@pytest.mark.anyio
async def test_try_connection_reports_success_and_failure(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    ok = FakeProvider(script=[FakeReply(data={"ok": True})], retry=RetryPolicy(max_retries=0))
    monkeypatch.setattr(connections, "build_provider", lambda *_a, **_k: ok)
    assert (await try_connection("openai", settings)).startswith("Bağlantı çalışıyor")

    broken = FakeProvider(script=[FakeReply(error="401")], retry=RetryPolicy(max_retries=0))
    monkeypatch.setattr(connections, "build_provider", lambda *_a, **_k: broken)
    assert (await try_connection("openai", settings)).startswith("Başarısız")


@pytest.mark.anyio
async def test_agy_without_model_still_discovers_models(settings: Settings) -> None:
    cfg = cli_settings(settings, model="", allow_tool_agent=True)
    result = await probe("agy", cfg, runner=FakeRunner(AGY_ONE_MODEL))
    assert result.models == ["gemini-a"]
    assert not result.ready
    assert result.status.detail.startswith("Önce bir model seç")


def test_login_command_uses_absolute_path(settings: Settings) -> None:
    cfg = cli_settings(settings).providers
    assert login_command("claude_cli", cfg)[1:] == ["auth", "login"]
    assert len(login_command("agy", cfg)) == 1
    assert Path(login_command("agy", cfg)[0]).is_absolute()


# --- Codex (Faz 28, ADR-0017) -----------------------------------------------------------------

CODEX_MODELS = (
    '{"models": [{"slug": "gpt-5.5", "visibility": "list"},'
    ' {"slug": "gizli-model", "visibility": "hide"}, {"slug": "gpt-5.6-terra"}]}'
)


class SequenceRunner:
    """Her çağrıda sıradaki sonucu döndürür (`login status`, ardından `debug models`)."""

    def __init__(self, *results: ProcessResult) -> None:
        self.results = list(results)
        self.calls: list[list[str]] = []

    def __call__(self, argv: list[str], stdin: str, limits: object, **_: object) -> ProcessResult:
        self.calls.append(list(argv))
        return self.results.pop(0)


def _logged_in(stderr: str = "Logged in using ChatGPT") -> ProcessResult:
    return ProcessResult(0, "", stderr)


def test_parse_codex_models_skips_hidden_and_bad_json() -> None:
    assert parse_codex_models(CODEX_MODELS) == ["gpt-5.5", "gpt-5.6-terra"]
    assert parse_codex_models("değil json") == []
    assert parse_codex_models('{"models": "x"}') == []


@pytest.mark.anyio
async def test_codex_probe_login_models_and_tool_consent(settings: Settings) -> None:
    run = SequenceRunner(_logged_in(), ProcessResult(0, CODEX_MODELS, ""))
    blocked = await probe("codex", cli_settings(settings), runner=run)
    assert [c[1:] for c in run.calls] == [["login", "status"], ["debug", "models"]]
    assert Path(run.calls[0][0]).is_absolute()
    assert blocked.models == ["gpt-5.5", "gpt-5.6-terra"]
    assert not blocked.ready
    assert "araç onayı" in blocked.status.detail

    allowed = await probe(
        "codex",
        cli_settings(settings, allow_tool_agent=True),
        runner=SequenceRunner(_logged_in(), ProcessResult(0, CODEX_MODELS, "")),
    )
    assert allowed.ready
    assert "2 model" in allowed.status.detail


@pytest.mark.anyio
async def test_codex_probe_logged_out_does_not_list_models(settings: Settings) -> None:
    run = SequenceRunner(ProcessResult(1, "", "Not logged in"))
    result = await probe("codex", cli_settings(settings, allow_tool_agent=True), runner=run)
    assert not result.ready
    assert "Oturum aç" in result.status.detail
    assert len(run.calls) == 1


@pytest.mark.anyio
async def test_codex_probe_model_list_timeout_keeps_login(settings: Settings) -> None:
    run = SequenceRunner(_logged_in(), ProcessResult(None, "", "", timed_out=True))
    result = await probe("codex", cli_settings(settings, allow_tool_agent=True), runner=run)
    assert result.ready
    assert result.models == []


def test_codex_login_command(settings: Settings) -> None:
    command = login_command("codex", cli_settings(settings).providers)
    assert command[1:] == ["login"]
    assert Path(command[0]).is_absolute()


@pytest.mark.anyio
async def test_try_connection_sends_no_temperature_and_room_for_reasoning(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz 28: akıl yürüten modeller (OpenAI gpt-5+/o, DeepSeek düşünme modu) `temperature=0`'ı
    reddeder ve küçük çıktı bütçesini düşünmeye harcar; deneme isteği ikisini de yapmamalı."""
    seen: list[GenerationOptions] = []

    class Spy(FakeProvider):
        async def generate_structured(
            self, messages: Any, output_model: Any, options: GenerationOptions
        ) -> Any:
            seen.append(options)
            return await super().generate_structured(messages, output_model, options)

    spy = Spy(script=[FakeReply(data={"ok": True})], retry=RetryPolicy(max_retries=0))
    monkeypatch.setattr(connections, "build_provider", lambda *_a, **_k: spy)
    await try_connection("openai", settings)
    (options,) = seen
    assert options.temperature is None
    assert options.max_tokens is not None
    assert options.max_tokens >= 1024


@pytest.mark.anyio
async def test_try_connection_unparsed_reply_is_failure(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Yanıt geldi ama JSON değil (ör. çıktı sınırı düşünmede bitti): 'çalışıyor' denmez."""
    empty = FakeProvider(
        script=[FakeReply(raw="", finish_reason="length")], retry=RetryPolicy(max_retries=0)
    )
    monkeypatch.setattr(connections, "build_provider", lambda *_a, **_k: empty)
    message = await try_connection("deepseek", settings)
    assert message.startswith("Başarısız")
    assert "length" in message
