"""Bağlantı mantığı (ADR-0014): anahtar kasası, ayar birleştirme, CLI/Ollama yoklaması.

Bölüm 2/2.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from codementor.config import Settings
from codementor.desktop import connections, runtime
from codementor.desktop.bridge import Cancellation
from codementor.desktop.connections import (
    KeyStore,
    probe,
    try_connection,
)
from codementor.desktop.connections_controller import ConnectionsController
from codementor.desktop.services import OllamaPullError, ollama_pull_argv, run_ollama_pull
from codementor.models.provider import GenerationOptions
from codementor.providers.base import RetryPolicy
from codementor.providers.fake import FakeProvider, FakeReply
from codementor.validation.runner import ProcessResult
from tests.desktop.connections_support import (
    CODEX_MODELS,
    OLLAMA_MODEL,
    FakeRunner,
    SequenceRunner,
    _fake_ollama,
    _logged_in,
    cli_settings,
)


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


@pytest.mark.anyio
async def test_try_connection_sends_no_temperature_and_room_for_reasoning(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz 28: akıl yürüten modeller (Gemini düşünme modu vb.) `temperature=0`'ı
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
    await try_connection("gemini", settings)
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
    message = await try_connection("anthropic", settings)
    assert message.startswith("Başarısız")
    assert "length" in message


@pytest.mark.anyio
async def test_try_connection_unrelated_json_is_failure(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Denetim L1: yanıtta ilgisiz bir JSON nesnesi varsa bağlantı "çalışıyor" sayılmaz."""
    other = FakeProvider(script=[FakeReply(data={"baska": 1})], retry=RetryPolicy(max_retries=0))
    monkeypatch.setattr(connections, "build_provider", lambda *_a, **_k: other)
    assert (await try_connection("agy", settings)).startswith("Başarısız")


def test_ollama_pull_argv_is_absolute_and_shell_free(tmp_path: Path) -> None:
    """F10: argv = [mutlak ollama yolu, "pull", model]; model tek bir argv öğesidir (kabuk yok)."""
    exe = _fake_ollama(tmp_path / "bin")
    argv = ollama_pull_argv(OLLAMA_MODEL, str(tmp_path / "bin"))
    assert argv == [str(exe.resolve()), "pull", OLLAMA_MODEL]


def test_ollama_pull_runner_gets_validated_argv(tmp_path: Path) -> None:
    """F10: doğrulanan argv sahte runner'a gider; gerçek süreç çalıştırılmaz."""
    exe = _fake_ollama(tmp_path / "bin")
    argv = ollama_pull_argv(OLLAMA_MODEL, str(tmp_path / "bin"))
    runner = FakeRunner("pulling manifest\n")
    outcome = run_ollama_pull(OLLAMA_MODEL, argv, runner=runner)
    assert runner.calls == [[str(exe.resolve()), "pull", OLLAMA_MODEL]]
    assert outcome.ok
    assert OLLAMA_MODEL in outcome.message


@pytest.mark.parametrize(
    "model",
    [
        "",
        "   ",
        "qwen; rm -rf /",
        "a b",
        "$(whoami)",
        "model|cat",
        "a\nb",
        "kötü:model",
        "qwen&del",
        "/x",
        "../x",
        "-flag",
        ".hidden",
        ":model",
    ],
)
def test_ollama_pull_rejects_unsafe_model_names(model: str, tmp_path: Path) -> None:
    """F10/İş 9: model adı geçerli kalıp dışındaysa reddedilir (süreç başlamaz)."""
    _fake_ollama(tmp_path / "bin")
    with pytest.raises(OllamaPullError):
        ollama_pull_argv(model, str(tmp_path / "bin"))


def test_ollama_pull_missing_binary_is_turkish_error(tmp_path: Path) -> None:
    """F10: ollama PATH'te yoksa çalıştırma denenmez; kullanıcıya Türkçe mesaj döner."""
    empty = tmp_path / "bos"
    empty.mkdir()
    with pytest.raises(OllamaPullError, match="Ollama bulunamadı"):
        ollama_pull_argv(OLLAMA_MODEL, str(empty))


def test_ollama_pull_failure_outcome_is_turkish() -> None:
    """F10: başarısız çıkışta neden Türkçe gösterilir (süreç sahte runner ile)."""
    runner = SequenceRunner(ProcessResult(1, "", "Error: pull model manifest: file does not exist"))
    outcome = run_ollama_pull(OLLAMA_MODEL, ["/opt/ollama", "pull", OLLAMA_MODEL], runner=runner)
    assert runner.calls == [["/opt/ollama", "pull", OLLAMA_MODEL]]
    assert not outcome.ok
    assert "başarısız" in outcome.message.lower()
    assert "manifest" in outcome.message


def test_ollama_pull_error_outcome_is_turkish() -> None:
    """F10/İş 9: süreç başlatılamazsa hata Türkçe gösterilir."""
    runner = SequenceRunner(ProcessResult(None, "", "", error="erişim engellendi"))
    outcome = run_ollama_pull(OLLAMA_MODEL, ["/opt/ollama", "pull", OLLAMA_MODEL], runner=runner)
    assert not outcome.ok
    assert "başlatılamadı" in outcome.message
    assert "erişim engellendi" in outcome.message


def test_ollama_pull_timeout_outcome_is_turkish() -> None:
    """F10/İş 9: indirme zaman aşımına uğrarsa Türkçe zaman aşımı metni döner."""
    runner = SequenceRunner(ProcessResult(None, "", "", timed_out=True))
    outcome = run_ollama_pull(OLLAMA_MODEL, ["/opt/ollama", "pull", OLLAMA_MODEL], runner=runner)
    assert not outcome.ok
    assert "zaman aşımı" in outcome.message


def test_ollama_pull_cancelled_outcome_is_turkish() -> None:
    """F10/İş 9: indirme iptal edildiğinde Türkçe iptal metni döner."""
    runner = SequenceRunner(ProcessResult(None, "", "", cancelled=True))
    outcome = run_ollama_pull(OLLAMA_MODEL, ["/opt/ollama", "pull", OLLAMA_MODEL], runner=runner)
    assert not outcome.ok
    assert "iptal edildi" in outcome.message


def test_controller_cancel_pull(settings: Settings, store: KeyStore) -> None:
    """F10/İş 9: cancel_pull süren görevin iptalini tetikler ve bayrağı temizler."""
    from codementor.desktop.bridge import Bridge

    fake_app = SimpleNamespace(settings=settings, bridge=Bridge())
    ctrl = ConnectionsController(fake_app, store)  # type: ignore[arg-type]
    cancellation = Cancellation()
    ctrl._pull_cancellations["ollama"] = cancellation
    assert ctrl.is_pulling
    ctrl.cancel_pull("ollama")
    assert cancellation.cancelled
    assert not ctrl.is_pulling


def test_runtime_confirm_close_checks_pulling(settings: Settings, store: KeyStore) -> None:
    """F10/İş 9: model indirmesi sürerken kapatma onay ister."""
    from codementor.desktop.bridge import Bridge

    fake_app = SimpleNamespace(
        files=SimpleNamespace(is_dirty=False),
        analyze_view=SimpleNamespace(busy=False),
        connections=None,
        confirm=lambda *_a, **_k: False,
        settings=settings,
        bridge=Bridge(),
    )
    ctrl = ConnectionsController(fake_app, store)  # type: ignore[arg-type]
    fake_app.connections = ctrl
    ctrl._pull_cancellations["ollama"] = Cancellation()
    assert runtime.confirm_close(fake_app) is False  # type: ignore[arg-type]
    ctrl._pull_cancellations.clear()
    assert runtime.confirm_close(fake_app) is True  # type: ignore[arg-type]
