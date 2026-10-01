"""CLI ajanı uçtan uca (Faz 25): sahte `claude`/`agy` gerçek `run_process` ile başlatılır.

Sahte CLI, Windows'ta distlib başlatıcısıyla `.exe`'ye sarılır (sağlayıcı `.cmd` çalıştırmaz),
POSIX'te shebang'li betiktir. Ağ yok; yalnızca yerel Python süreci.
"""

from __future__ import annotations

import asyncio
import shutil
import stat
import sys
import time
from pathlib import Path

import pytest

from codementor.config import AgyConfig, ClaudeCliConfig
from codementor.models.llm_output import LLMSocraticOutput
from codementor.models.provider import ChatMessage, GenerationOptions
from codementor.providers import RetryPolicy
from codementor.providers.cli_agent import CliAgentProvider

pytestmark = pytest.mark.anyio

SCRIPT = Path(__file__).with_name("fake_cli_script.py")
SECRET_CODE = "int gizli_kullanici_kodu_91f3(void) { return 7; }"


def make_fake_cli(directory: Path, name: str) -> Path:
    """`name` adlı çalıştırılabilir sahte CLI; mutlak yolunu döndürür."""
    source = directory / "src" / f"{name}.py"
    source.parent.mkdir(parents=True)
    shutil.copyfile(SCRIPT, source)
    target = directory / "bin"
    target.mkdir()
    if sys.platform == "win32":
        from distlib.scripts import ScriptMaker

        # pip'in konsol betiği exe'leriyle aynı biçim: başlatıcı + shebang + __main__.py zip'i.
        # `make()` düz betiği sarmıyor; giriş noktası ise modülü PYTHONPATH'te arar (ortam
        # temizlendiği için bulunamaz). Bu yüzden betik doğrudan gömülür.
        maker = ScriptMaker(str(source.parent), str(target), add_launchers=True)
        maker.executable = sys.executable
        made: list[str] = []
        maker._write_script([name], maker._get_shebang("utf-8"), source.read_bytes(), made, "py")
        return Path(made[0]).resolve()
    interpreter = sys.executable if " " not in sys.executable else "/usr/bin/env python3"
    executable = target / name
    executable.write_text(f"#!{interpreter}\n" + SCRIPT.read_text("utf-8"), encoding="utf-8")
    executable.chmod(executable.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return executable


def _messages(extra: str = "") -> list[ChatMessage]:
    return [
        ChatMessage(role="system", content="SISTEM_TALIMATI_42"),
        ChatMessage(role="user", content=f"<code>{SECRET_CODE}</code>{extra}"),
    ]


def _provider(kind: str, command: Path, timeout_s: int = 30) -> CliAgentProvider:
    retry = RetryPolicy(max_retries=0)
    if kind == "agy":
        config = AgyConfig(
            command=str(command), model="m", allow_tool_agent=True, timeout_s=timeout_s
        )
        return CliAgentProvider("agy", config, retry=retry)
    claude = ClaudeCliConfig(command=str(command), model="m", timeout_s=timeout_s)
    return CliAgentProvider("claude_cli", claude, retry=retry)


async def test_claude_fake_receives_prompt_on_stdin_only(tmp_path: Path) -> None:
    fake = make_fake_cli(tmp_path, "claude")
    result = await _provider("claude_cli", fake).generate_structured(
        _messages(), LLMSocraticOutput, GenerationOptions()
    )
    probe = result.parsed
    assert probe is not None
    assert SECRET_CODE in probe["stdin"]
    assert "<system>\nSISTEM_TALIMATI_42\n</system>" in probe["stdin"]
    assert all(SECRET_CODE not in arg and "SISTEM_TALIMATI_42" not in arg for arg in probe["argv"])
    assert {"--tools", "--safe-mode", "--no-session-persistence"} <= set(probe["argv"])
    assert result.usage.input_tokens == 11
    assert result.usage.output_tokens == 7
    assert result.provider == "claude_cli"


async def test_fake_cli_runs_in_empty_cwd_without_foreign_keys(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-baska-saglayici")
    monkeypatch.setenv("CODEMENTOR_SECRET_PROBE", "gizli")
    fake = make_fake_cli(tmp_path, "claude")
    monkeypatch.chdir(tmp_path)  # sürecin çalışma dizini bu olmamalı
    result = await _provider("claude_cli", fake).generate_structured(
        _messages(), LLMSocraticOutput, GenerationOptions()
    )
    probe = result.parsed
    assert probe is not None
    assert probe["cwd_entries"] == []
    assert Path(probe["cwd"]).resolve() != tmp_path.resolve()
    env = set(probe["env_keys"])
    assert "OPENAI_API_KEY" not in env
    assert "CODEMENTOR_SECRET_PROBE" not in env
    assert "DISABLE_AUTOUPDATER" in env  # sessiz mod değişkenleri verilir


async def test_agy_fake_plan_mode_and_system_in_stdin(tmp_path: Path) -> None:
    fake = make_fake_cli(tmp_path, "agy")
    result = await _provider("agy", fake).generate_structured(
        _messages(), LLMSocraticOutput, GenerationOptions()
    )
    probe = result.parsed
    assert probe is not None
    argv = probe["argv"]
    assert argv[argv.index("--mode") + 1] == "plan"
    assert "--sandbox" in argv
    assert "SISTEM_TALIMATI_42" in probe["stdin"]
    assert all(SECRET_CODE not in arg for arg in argv)
    assert result.provider == "agy"
    assert result.usage.output_tokens == 7


async def test_cancel_kills_fake_cli(tmp_path: Path) -> None:
    fake = make_fake_cli(tmp_path, "claude")
    marker = tmp_path / "basladi.txt"
    task = asyncio.create_task(
        _provider("claude_cli", fake, timeout_s=120).generate_structured(
            _messages(f" UYU:{marker.as_posix()}"), LLMSocraticOutput, GenerationOptions()
        )
    )
    deadline = time.monotonic() + 30
    while not marker.exists():
        assert time.monotonic() < deadline, "sahte CLI başlamadı"
        await asyncio.sleep(0.05)
    start = time.perf_counter()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert time.perf_counter() - start < 5  # 60 sn uyku ve 120 sn zaman aşımı beklenmedi
