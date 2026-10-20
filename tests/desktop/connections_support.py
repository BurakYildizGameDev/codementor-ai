"""`test_connections.py` için ortak düzenek: sabitler, yardımcılar, fixture'lar."""

from __future__ import annotations

import stat
import sys
from pathlib import Path
from typing import Any

import pytest

from codementor.config import Settings
from codementor.validation.runner import ProcessResult

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


# --- Faz F (F10): `ollama pull` ----------------------------------------------------------------

OLLAMA_MODEL = "qwen2.5-coder:7b"


EXE_SUFFIX = ".exe" if sys.platform == "win32" else ""


def _fake_ollama(directory: Path) -> Path:
    """PATH'te duran sahte `ollama` (çalıştırılmaz; yalnız bulunur)."""
    directory.mkdir(parents=True, exist_ok=True)
    exe = directory / f"ollama{EXE_SUFFIX}"
    exe.write_bytes(b"")
    exe.chmod(exe.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return exe
