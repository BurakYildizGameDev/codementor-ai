"""CLI ajan sağlayıcıları (ADR-0012): argv güvenliği, stdin, çalıştırılabilir çözümü, çıktı.

Gerçek alt süreç çalışmaz: `run_process` yerine kayıt tutan sahte bir çalıştırıcı verilir.

Bölüm 1/2.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from codementor.config import AgyConfig, ClaudeCliConfig
from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.provider import ChatMessage
from codementor.providers import (
    ProviderConfigError,
    ProviderRequestError,
    ProviderUnavailableError,
    RetryPolicy,
)
from codementor.providers.cli_agent import (
    FIXED_SYSTEM,
    CliAgentProvider,
    CliKind,
    CliTimeoutError,
    render_prompt,
)
from codementor.providers.schema_adapter import SchemaAdapter
from codementor.validation.runner import ProcessResult
from tests.providers.cli_agent_support import (
    ANSWER,
    EXE,
    MESSAGES,
    STUDENT_CODE,
    SYSTEM_MARKER,
    FakeRunner,
    _provider,
    _run,
    agy_json,
    claude_json,
    ok,
)

pytestmark = pytest.mark.anyio


# ------------------------------------------------------------------------ argv ve stdin


async def test_claude_argv_disables_tools_and_uses_schema() -> None:
    runner = FakeRunner([ok(claude_json(structured_output=ANSWER))])
    await _run(_provider("claude_cli", runner))
    argv = runner.calls[0]["argv"]
    assert argv[0] == str(Path(EXE).resolve())  # Linux'ta venv python'u sembolik bağ
    assert argv[argv.index("--tools") + 1] == ""  # hiç araç yok
    assert argv[argv.index("--permission-mode") + 1] == "dontAsk"
    assert argv[argv.index("--permission-prompts") + 1] == "none"
    for flag in (
        "--restricted",
        "--safe-mode",
        "--strict-mcp-config",
        "--disable-slash-commands",
        "--no-session-persistence",
    ):
        assert flag in argv
    schema = json.loads(argv[argv.index("--json-schema") + 1])
    assert schema == SchemaAdapter(LLMSocraticOutput).anthropic()
    assert argv[argv.index("--system-prompt") + 1] == FIXED_SYSTEM
    assert argv[argv.index("--model") + 1] == "m"


@pytest.mark.parametrize("kind", ["claude_cli", "agy"])
async def test_cli_schema_is_not_enforced(kind: CliKind) -> None:
    """G7: CLI alt süreci şema garantisi vermez (metinden JSON da gelebilir) → False."""
    output = claude_json(structured_output=ANSWER) if kind == "claude_cli" else agy_json()
    runner = FakeRunner([ok(output)])
    result = await _run(_provider(kind, runner))
    assert result.schema_enforced is False


@pytest.mark.parametrize("kind", ["claude_cli", "agy"])
async def test_messages_only_on_stdin(kind: CliKind) -> None:
    # denetim O1/O2: sistem mesajı da argv'ye girmez; agy'de kaybolmaz
    output = claude_json(structured_output=ANSWER) if kind == "claude_cli" else agy_json()
    runner = FakeRunner([ok(output)])
    await _run(_provider(kind, runner))
    call = runner.calls[0]
    stdin = call["stdin"]
    if kind == "agy":  # NDJSON olayı: içerik JSON dizesi olarak kaçışlı
        stdin = json.loads(stdin)["message"]["content"]
    assert STUDENT_CODE in stdin
    assert SYSTEM_MARKER in stdin
    joined = "\n".join(call["argv"])
    assert STUDENT_CODE not in joined
    assert "rm -rf" not in joined
    assert SYSTEM_MARKER not in joined


async def test_argv_values_follow_known_flags() -> None:
    # agy'nin bayrak ayrıştırıcısı ilk konumsal argümanda durur: her değer bir bayraktan sonra
    runner = FakeRunner([ok(agy_json())])
    await _run(_provider("agy", runner))
    argv = runner.calls[0]["argv"][1:]
    # `-p` de değer alır (agy 1.2.14): değersiz `-p` sonraki bayrağı prompt sanıyordu
    assert "-p" not in argv
    valued = {
        "--input-format",
        "--output-format",
        "--json-schema",
        "--mode",
        "--print-timeout",
        "--model",
    }
    for index, arg in enumerate(argv):
        if not arg.startswith("-"):
            assert argv[index - 1] in valued, arg


async def test_limits_and_profile_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("USERPROFILE", "C:/Users/test")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-baska-saglayici-anahtari-123")
    runner = FakeRunner([ok(claude_json(structured_output=ANSWER))])
    provider = _provider("claude_cli", runner)
    await _run(provider)
    call = runner.calls[0]
    assert call["limits"].timeout_s == 300
    assert call["limits"].max_processes > 8
    assert call["limits"].file_size_bytes > 1024 * 1024
    assert call["limits"].output_limit == provider.config.output_limit_bytes  # G1
    assert call["env"]["USERPROFILE"] == "C:/Users/test"
    assert call["env"]["DISABLE_AUTOUPDATER"] == "1"
    assert "OPENAI_API_KEY" not in call["env"]  # başka sağlayıcıların anahtarları geçmez


async def test_output_limit_bytes_comes_from_config() -> None:
    # G1 (O5): sınır config'ten gelir; varsayılanı (1 MB) 64 KB yanıtı kesiyordu
    runner = FakeRunner([ok(claude_json(structured_output=ANSWER))])
    config = ClaudeCliConfig(command=EXE, model="m", output_limit_bytes=131_072)
    provider = CliAgentProvider(
        "claude_cli", config, retry=RetryPolicy(max_retries=0), runner=runner
    )
    await _run(provider)
    assert runner.calls[0]["limits"].output_limit == 131_072


def test_render_prompt_delimits_roles() -> None:
    messages = [
        ChatMessage(role="system", content="s"),
        ChatMessage(role="user", content="u1"),
        ChatMessage(role="assistant", content="a1"),
    ]
    assert render_prompt(messages) == (
        "<system>\ns\n</system>\n\n<user>\nu1\n</user>\n\n<assistant>\na1\n</assistant>"
    )


# ---------------------------------------------------------------------------- agy onayı


async def test_agy_requires_explicit_opt_in() -> None:
    # denetim O3: araçları kapatılamayan ajan varsayılan olarak kullanılamaz
    runner = FakeRunner([])
    provider = CliAgentProvider("agy", AgyConfig(command=EXE, model="m"), runner=runner)
    with pytest.raises(ProviderConfigError, match="allow_tool_agent"):
        await _run(provider)
    assert runner.calls == []


async def test_agy_argv_and_response_parsed() -> None:
    runner = FakeRunner([ok("[agy] bilgi satırı\n" + agy_json(usage={"input_tokens": 7}))])
    result = await _run(_provider("agy", runner))
    assert result.parsed == ANSWER
    assert result.usage.input_tokens == 7
    argv = runner.calls[0]["argv"]
    assert "--sandbox" in argv
    assert argv[argv.index("--mode") + 1] == "plan"
    assert argv[argv.index("--input-format") + 1] == "stream-json"
    assert argv[argv.index("--output-format") + 1] == "stream-json"
    # agy kendi kısmi sonucunu bizim süreç zaman aşımımızdan (300 sn) önce döndürsün
    assert argv[argv.index("--print-timeout") + 1] == "290s"


async def test_agy_stdin_is_single_ndjson_user_event() -> None:
    runner = FakeRunner([ok(agy_json())])
    await _run(_provider("agy", runner))
    stdin = runner.calls[0]["stdin"]
    lines = stdin.strip("\n").split("\n")
    assert len(lines) == 1  # stream-json: satır başına bir mesaj, yani tek tur
    event = json.loads(lines[0])
    assert event == {
        "event": "user",
        "message": {"role": "user", "content": render_prompt(MESSAGES)},
    }


async def test_agy_error_status_reports_message() -> None:
    stdout = agy_json(status="ERROR", response="", error="stream input message has no content")
    with pytest.raises(ProviderRequestError, match="no content"):
        await _run(_provider("agy", FakeRunner([ok(stdout)])))


async def test_agy_print_timeout_is_cli_timeout() -> None:
    # agy --print-timeout dolunca stderr'e yazar ve SUCCESS + boş yanıt döner (bu oturumda gözlendi)
    stdout = agy_json(response="", num_turns=0)
    stderr = "[agy] print timeout after 4m50s with turn in progress; returning partial output"
    result = ProcessResult(returncode=0, stdout=stdout, stderr=stderr)
    with pytest.raises(CliTimeoutError, match="süre"):
        await _run(_provider("agy", FakeRunner([result])))


async def test_agy_empty_response_is_unavailable() -> None:
    # oturum açılmamış agy gerçekte böyle döner (Faz 25'te gözlendi)
    stdout = agy_json(response="", num_turns=0)
    with pytest.raises(ProviderUnavailableError, match="oturumu"):
        await _run(_provider("agy", FakeRunner([ok(stdout)])))


async def test_agy_print_timeout_message_mentions_mcp() -> None:
    # Faz 63: global bir MCP sunucusu (unity-mcp) bağlanamayınca agy turu hiç başlatmıyor
    stdout = agy_json(response="", num_turns=0)
    stderr = "[agy] print timeout after 4m50s with turn in progress; returning partial output"
    result = ProcessResult(returncode=0, stdout=stdout, stderr=stderr)
    with pytest.raises(CliTimeoutError, match="agy mcp list"):
        await _run(_provider("agy", FakeRunner([result])))


async def test_agy_zero_turns_message_mentions_mcp() -> None:
    stdout = agy_json(response="", num_turns=0)
    with pytest.raises(ProviderUnavailableError, match="agy mcp list"):
        await _run(_provider("agy", FakeRunner([ok(stdout)])))


async def test_agy_two_json_objects_takes_first() -> None:
    # agy 1.3.1 yanıttan sonra kendiliğinden ikinci tur açıp araç izi ekliyor (Faz 63)
    response = json.dumps(ANSWER) + '\n{"toolAction":"Completing task","toolSummary":"Finish"}\n'
    result = await _run(_provider("agy", FakeRunner([ok(agy_json(response=response))])))
    assert result.parsed == ANSWER


async def test_agy_structured_output_preferred() -> None:
    other = {**ANSWER, "key_flaw_concept": "metin"}
    stdout = agy_json(response=json.dumps(other), structured_output=ANSWER)
    result = await _run(_provider("agy", FakeRunner([ok(stdout)])))
    assert result.parsed == ANSWER
    assert json.loads(result.raw_text) == ANSWER


async def test_agy_non_dict_structured_output_ignored() -> None:
    stdout = agy_json(structured_output="bozuk")
    result = await _run(_provider("agy", FakeRunner([ok(stdout)])))
    assert result.parsed == ANSWER


async def test_agy_empty_response_recovered_from_text_deltas() -> None:
    text = json.dumps(ANSWER)
    deltas = [
        {"step_index": 1, "step_type": "agent_response", "text_delta": text[:10]},
        {"step_index": 1, "step_type": "agent_response", "text_delta": text[10:]},
        {"step_index": 3, "step_type": "agent_response", "text_delta": '{"toolAction":"x"}'},
    ]
    steps = "".join(json.dumps({"event": "step_update", "step_update": d}) + "\n" for d in deltas)
    result = await _run(_provider("agy", FakeRunner([ok(steps + agy_json(response=""))])))
    assert result.parsed == ANSWER


async def test_agy_print_timeout_with_partial_deltas_is_timeout() -> None:
    """Denetim O1: süre dolunca yarım akış parçaları yanıt sayılmaz (onarım değil zaman aşımı)."""
    partial = {"step_index": 1, "step_type": "agent_response", "text_delta": '{"a": [{"b": 1}'}
    steps = json.dumps({"event": "step_update", "step_update": partial}) + "\n"
    stderr = "[agy] print timeout after 4m50s with turn in progress; returning partial output"
    stdout = steps + agy_json(response="", num_turns=1)
    result = ProcessResult(returncode=0, stdout=stdout, stderr=stderr)
    with pytest.raises(CliTimeoutError):
        await _run(_provider("agy", FakeRunner([result])))


async def test_agy_slow_model_timeout_does_not_blame_mcp() -> None:
    """Denetim L2: tur başlamışsa (model yalnız yavaş) MCP yönlendirmesi gösterilmez."""
    stderr = "[agy] print timeout after 4m50s with turn in progress; returning partial output"
    result = ProcessResult(returncode=0, stdout=agy_json(response="", num_turns=1), stderr=stderr)
    with pytest.raises(CliTimeoutError) as info:
        await _run(_provider("agy", FakeRunner([result])))
    assert "agy mcp list" not in str(info.value)


async def test_agy_non_result_last_event_rejected() -> None:
    stdout = json.dumps({"event": "init", "conversation_id": "c", "status": "SUCCESS"})
    with pytest.raises(ProviderRequestError, match="JSON çıktı alınamadı"):
        await _run(_provider("agy", FakeRunner([ok(stdout)])))
