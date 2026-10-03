"""`codementor toolchain status|install` (Faz 29): kurulum ve keşif sahteleriyle, ağsız."""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from codementor.cli import toolchain as cli_toolchain
from codementor.cli.main import app
from codementor.config import ValidationSettings
from codementor.models.validation import CompilerTool, DownloadProgress, Toolchain
from codementor.validation.toolchain_install import ToolchainInstallError

runner = CliRunner()


def test_status_lists_tools(monkeypatch: pytest.MonkeyPatch) -> None:
    chain = Toolchain(
        c=CompilerTool(name="gcc", kind="gcc", command=["/usr/bin/gcc"]),
        cpp=CompilerTool(name="zig", kind="clang", command=["/z/zig"], origin="downloaded"),
    )
    monkeypatch.setattr(cli_toolchain, "get_toolchain", lambda _s: chain)
    result = runner.invoke(app, ["toolchain", "status"])
    assert result.exit_code == 0, result.output
    assert "gcc" in result.output
    assert "PATH" in result.output
    assert "zig" in result.output
    assert "indirilen" in result.output
    assert "bulunamadı" in result.output


def test_install_success_reports_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    def fake_install(settings: ValidationSettings, **kwargs: object) -> Path:
        progress = kwargs["progress"]
        assert callable(progress)
        progress(DownloadProgress(stage="download", done=10, total=100))
        progress(DownloadProgress(stage="check", done=1, total=1))
        return tmp_path / "zig"

    monkeypatch.setattr(cli_toolchain, "install_zig", fake_install)
    result = runner.invoke(app, ["toolchain", "install", "zig"])
    assert result.exit_code == 0, result.output
    assert "Zig kuruldu" in result.output


def test_install_reports_turkish_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def failing(settings: ValidationSettings, **kwargs: object) -> Path:
        raise ToolchainInstallError("İndirilen dosya doğrulanamadı (sha256 uyuşmuyor).")

    monkeypatch.setattr(cli_toolchain, "install_zig", failing)
    result = runner.invoke(app, ["toolchain", "install"])
    assert result.exit_code == 1
    assert "sha256 uyuşmuyor" in result.output


def test_install_unknown_tool() -> None:
    result = runner.invoke(app, ["toolchain", "install", "gcc"])
    assert result.exit_code == 2
    assert "Yalnızca 'zig'" in result.output
