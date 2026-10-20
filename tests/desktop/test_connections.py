"""Bağlantı mantığı (ADR-0014): anahtar kasası, ayar birleştirme, CLI/Ollama yoklaması.

Bölüm 1/2.
"""

from __future__ import annotations

import os
from pathlib import Path

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
    model_suggestions,
    parse_agy_models,
    parse_claude_status,
    parse_codex_models,
    probe,
    try_connection,
)
from codementor.models.desktop import DesktopPrefs, ProviderOverride
from codementor.providers.base import RetryPolicy
from codementor.providers.fake import FakeProvider, FakeReply
from tests.desktop.conftest import FakeVault
from tests.desktop.connections_support import (
    AGY_ONE_MODEL,
    CODEX_MODELS,
    EXE,
    FakeRunner,
    cli_settings,
)

# --- Kasa -------------------------------------------------------------------------------------


def test_key_store_round_trip_and_idempotent_delete(store: KeyStore) -> None:
    assert store.get("gemini") is None
    store.set("gemini", "sk-abc")
    assert store.get("gemini") == "sk-abc"
    store.delete("gemini")
    store.delete("gemini")  # yoksa sessiz
    assert store.get("gemini") is None


def test_key_store_errors_are_turkish(vault: FakeVault, store: KeyStore) -> None:
    vault.broken = True
    with pytest.raises(KeyStoreError, match="okunamadı"):
        store.get("gemini")
    with pytest.raises(KeyStoreError, match="kaydedilemedi"):
        store.set("gemini", "x")


def test_vault_keys_fill_env_but_never_override_existing(
    settings: Settings, store: KeyStore, monkeypatch: pytest.MonkeyPatch
) -> None:
    store.set("gemini", "sk-vault-gemini-123")
    store.set("anthropic", "sk-vault-anthropic-123")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "dis-ortam-anahtari")
    loaded = load_vault_keys(settings.providers, store)
    assert loaded == {"gemini"}
    assert os.environ["GEMINI_API_KEY"] == "sk-vault-gemini-123"
    assert os.environ["ANTHROPIC_API_KEY"] == "dis-ortam-anahtari"
    assert key_source(settings.providers, "gemini", loaded) == "vault"
    assert key_source(settings.providers, "anthropic", loaded) == "environment"
    monkeypatch.delenv("ANTHROPIC_API_KEY")
    assert key_source(settings.providers, "anthropic", set()) == "missing"


def test_locked_vault_does_not_crash_startup(settings: Settings, vault: FakeVault) -> None:
    vault.broken = True
    assert load_vault_keys(settings.providers, KeyStore(vault)) == set()


def test_purge_legacy_removes_only_removed_providers(store: KeyStore, vault: FakeVault) -> None:
    """ADR-0021/F8: eski openai/deepseek anahtarları silinir; güncel kayıt korunur."""
    store.set("openai", "sk-eski-openai")
    store.set("deepseek", "sk-eski-deepseek")
    store.set("gemini", "sk-guncel")
    assert store.purge_legacy() == 2
    assert store.purge_legacy() == 0  # ikinci çağrı: silinecek bir şey kalmadı
    assert vault.items == {(connections.KEYRING_SERVICE, "gemini"): "sk-guncel"}


def test_purge_legacy_locked_vault_is_turkish_error(vault: FakeVault, store: KeyStore) -> None:
    vault.broken = True
    with pytest.raises(KeyStoreError, match="okunamadı"):
        store.purge_legacy()


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
        update={"gemini": settings.providers.gemini.model_copy(update={"model": "gemini-x"})}
    )
    cfg = settings.model_copy(update={"providers": providers})
    assert not (await probe("gemini", cfg)).ready
    monkeypatch.setenv("GEMINI_API_KEY", "sk-test")
    assert (await probe("gemini", cfg)).ready


@pytest.mark.anyio
async def test_try_connection_reports_success_and_failure(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    ok = FakeProvider(script=[FakeReply(data={"ok": True})], retry=RetryPolicy(max_retries=0))
    monkeypatch.setattr(connections, "build_provider", lambda *_a, **_k: ok)
    assert (await try_connection("gemini", settings)).startswith("Bağlantı çalışıyor")

    broken = FakeProvider(script=[FakeReply(error="401")], retry=RetryPolicy(max_retries=0))
    monkeypatch.setattr(connections, "build_provider", lambda *_a, **_k: broken)
    assert (await try_connection("gemini", settings)).startswith("Başarısız")


@pytest.mark.anyio
async def test_try_connection_agy_two_objects_succeeds(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz 63: agy 1.3.1'in gerçek çıktısı (yanıt + kendiliğinden eklenen araç izi) geçer."""
    from codementor.config import AgyConfig
    from codementor.providers.cli_agent import CliAgentProvider

    fixture = Path(__file__).parents[1] / "providers" / "fixtures" / "agy_stream_result.ndjson"
    agy = CliAgentProvider(
        "agy",
        AgyConfig(command=EXE, model="gemini-3.8-flash-low", allow_tool_agent=True),
        retry=RetryPolicy(max_retries=0),
        runner=FakeRunner(fixture.read_text(encoding="utf-8")),
    )
    monkeypatch.setattr(connections, "build_provider", lambda *_a, **_k: agy)
    assert (await try_connection("agy", settings)).startswith("Bağlantı çalışıyor")


@pytest.mark.anyio
async def test_agy_without_model_still_discovers_models(settings: Settings) -> None:
    cfg = cli_settings(settings, model="", allow_tool_agent=True)
    result = await probe("agy", cfg, runner=FakeRunner(AGY_ONE_MODEL))
    assert result.models == ["gemini-a"]
    assert not result.ready
    assert result.status.detail.startswith("Önce bir model seç")


def test_parse_codex_models_skips_hidden_and_bad_json() -> None:
    assert parse_codex_models(CODEX_MODELS) == ["gpt-5.5", "gpt-5.6-terra"]
    assert parse_codex_models("değil json") == []
    assert parse_codex_models('{"models": "x"}') == []
