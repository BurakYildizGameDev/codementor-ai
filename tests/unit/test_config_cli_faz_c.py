"""Faz C: BOM'lu toml, toml yazıcısı biçim koruması, yapılandırma konumu, CLI çıkış kodları."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

from codementor.cli.main import app
from codementor.config import CONFIG_FILE_ENV, DEFAULT_CONFIG_FILE, config_file, load_settings
from codementor.desktop import runtime
from codementor.desktop.config_writer import write_provider_prefs
from codementor.models.desktop import DesktopPrefs
from tests.integration.conftest import BROKEN_C
from tests.unit.test_cli_analyze import run  # noqa: F401  (fikstür)

BOM = chr(0xFEFF)
PREFS = DesktopPrefs.model_validate(
    {"provider": "claude_cli", "providers": {"ollama": {"model": "qwen"}}}
)


def _load(path: Path, monkeypatch: pytest.MonkeyPatch) -> Any:
    monkeypatch.setenv(CONFIG_FILE_ENV, str(path))
    return load_settings()


# --- O7: BOM ------------------------------------------------------------------------------------


def test_bom_toml_is_read(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "codementor.toml"
    path.write_text(f'{BOM}[providers]\ndefault = "gemini"\n', encoding="utf-8")
    assert _load(path, monkeypatch).providers.default == "gemini"


def test_writer_reads_bom_and_writes_without(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "codementor.toml"
    path.write_text(f'{BOM}[providers]  # yorum\nfallback = ["gemini"]\n', encoding="utf-8")
    write_provider_prefs(path, PREFS)
    text = path.read_text(encoding="utf-8")
    assert not text.startswith(BOM)
    assert "# yorum" in text
    settings = _load(path, monkeypatch)
    assert settings.providers.default == "claude_cli"
    assert settings.providers.fallback == ["gemini"]


# --- Y7: biçim koruması ve atomik yazım ----------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        'providers = { default = "ollama", fallback = ["anthropic"] }\n',
        '# üst yorum\nproviders.fallback = ["anthropic"]\nproviders.default = "ollama"\n',
        '[providers]\ndefault = "ollama"\nfallback = ["anthropic"]  # yedek\n',
    ],
    ids=["satir-ici-tablo", "nokta-anahtari", "baslikli-tablo"],
)
def test_writer_keeps_user_keys(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, text: str) -> None:
    path = tmp_path / "codementor.toml"
    path.write_text(text, encoding="utf-8")
    write_provider_prefs(path, PREFS)
    settings = _load(path, monkeypatch)
    assert settings.providers.default == "claude_cli"
    assert settings.providers.fallback == ["anthropic"]  # eskiden kayboluyordu
    assert settings.providers.ollama.model == "qwen"
    written = path.read_text(encoding="utf-8")
    for comment in ("# üst yorum", "# yedek"):
        if comment in text:
            assert comment in written


def test_writer_failure_keeps_old_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "codementor.toml"
    original = '[providers]\ndefault = "ollama"\n'
    path.write_text(original, encoding="utf-8")

    def broken(*_a: Any, **_k: Any) -> None:
        raise OSError("disk dolu")

    monkeypatch.setattr("codementor.desktop.config_writer.os.replace", broken)
    with pytest.raises(OSError, match="disk dolu"):
        write_provider_prefs(path, PREFS)
    assert path.read_text(encoding="utf-8") == original
    assert [p.name for p in tmp_path.iterdir()] == ["codementor.toml"]  # geçici dosya kalmadı


# --- O9 / Y8: yapılandırma konumu -------------------------------------------------------------


def test_config_file_falls_back_to_bundled_default(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(CONFIG_FILE_ENV, raising=False)
    monkeypatch.chdir(tmp_path)  # çalışma dizininde toml yok
    resources = tmp_path / "_resources"
    resources.mkdir()
    (resources / DEFAULT_CONFIG_FILE).write_text(
        '[providers]\ndefault = "claude_cli"\n', encoding="utf-8"
    )
    monkeypatch.setattr("codementor.config.resource_path", lambda rel: resources / rel)
    assert config_file() == resources / DEFAULT_CONFIG_FILE
    assert load_settings().providers.default == "claude_cli"
    (tmp_path / DEFAULT_CONFIG_FILE).write_text('[providers]\ndefault = "gemini"\n', "utf-8")
    assert load_settings().providers.default == "gemini"  # çalışma dizinindeki önce


def test_writable_config_prefers_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "benim.toml"
    monkeypatch.setenv(CONFIG_FILE_ENV, str(target))
    assert runtime.writable_config_file() == target.absolute()


def _bundle(root: Path) -> Path:
    root.mkdir(parents=True)
    (root / DEFAULT_CONFIG_FILE).write_text('[providers]\ndefault = "claude_cli"\n', "utf-8")
    return root


def test_writable_config_frozen_copies_next_to_exe_and_activates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(CONFIG_FILE_ENV, raising=False)
    bundle = _bundle(tmp_path / "meipass")
    exe_dir = tmp_path / "uygulama"
    exe_dir.mkdir()
    monkeypatch.setattr(runtime, "is_frozen", lambda: True)
    monkeypatch.setattr(runtime, "resource_root", lambda: bundle)
    monkeypatch.setattr(sys, "executable", str(exe_dir / "CodeMentor.exe"))
    target = runtime.writable_config_file()
    assert target == exe_dir / DEFAULT_CONFIG_FILE
    assert target.read_text(encoding="utf-8") == (bundle / DEFAULT_CONFIG_FILE).read_text("utf-8")
    assert os.environ[CONFIG_FILE_ENV] == str(target)  # yeniden yükleme bu dosyayı okur
    assert config_file() == target  # Bağlantılar ekranındaki konum da bu
    write_provider_prefs(target, DesktopPrefs.model_validate({"provider": "gemini"}))
    assert load_settings().providers.default == "gemini"


def test_writable_config_installed_wheel_uses_home(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(CONFIG_FILE_ENV, raising=False)
    bundle = _bundle(tmp_path / "site-packages" / "codementor" / "_resources")
    home = tmp_path / "ev" / ".codementor"
    monkeypatch.setattr(runtime, "is_frozen", lambda: False)
    monkeypatch.setattr(runtime, "resource_root", lambda: bundle)
    monkeypatch.setattr(runtime, "user_dir", lambda: home)
    assert runtime.is_installed_package()
    assert runtime.user_config_file() is None
    target = runtime.writable_config_file()
    assert target == home / DEFAULT_CONFIG_FILE  # paket dizinine yazılmaz
    assert target.is_file()
    assert runtime.user_config_file() == target


def test_writable_config_repo_uses_active_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(CONFIG_FILE_ENV, raising=False)
    monkeypatch.setattr(runtime, "is_frozen", lambda: False)
    monkeypatch.setattr(runtime, "resource_root", lambda: tmp_path / "depo")
    monkeypatch.chdir(tmp_path)
    (tmp_path / DEFAULT_CONFIG_FILE).write_text("", encoding="utf-8")
    assert runtime.writable_config_file() == (tmp_path / DEFAULT_CONFIG_FILE).absolute()


# --- Y9 / O12 / O11 / D20: CLI ------------------------------------------------------------------


def test_analyze_db_error_exits_3_without_traceback(
    run: Any,  # noqa: F811
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blocker = tmp_path / "dosya"
    blocker.write_text("x", encoding="utf-8")
    monkeypatch.setenv("CODEMENTOR_STORAGE__DB_PATH", str(blocker / "alt" / "cm.db"))
    result = run(BROKEN_C)
    assert result.exit_code == 3, result.output
    assert "Hata:" in result.output
    assert "Traceback" not in result.output


def test_analyze_unwritable_out_exits_3(run: Any, tmp_path: Path) -> None:  # noqa: F811
    blocker = tmp_path / "dosya"
    blocker.write_text("x", encoding="utf-8")
    for fmt in ("pretty", "json"):
        result = run(BROKEN_C, "--format", fmt, "--out", str(blocker / "rapor.txt"))
        assert result.exit_code == 3, (fmt, result.output)
        assert "çıktı yazılamadı" in result.output


def test_toolchain_status_broken_toml_exits_3(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    broken = tmp_path / "codementor.toml"
    broken.write_text("[validation\n", encoding="utf-8")
    monkeypatch.setenv(CONFIG_FILE_ENV, str(broken))
    result = CliRunner().invoke(app, ["toolchain", "status"])
    assert result.exit_code == 3, result.output
    assert "codementor.toml okunamadı" in result.output


def test_eval_compare_missing_file_exits_3(tmp_path: Path) -> None:
    result = CliRunner().invoke(app, ["eval", "compare", str(tmp_path / "yok.json")])
    assert result.exit_code == 3, result.output
    assert "Hata:" in result.output


def test_rules_list_marks_disabled(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config = tmp_path / "codementor.toml"
    config.write_text('[rules]\ndisabled = ["C-MEM-001"]\n', encoding="utf-8")
    monkeypatch.setenv(CONFIG_FILE_ENV, str(config))
    result = CliRunner().invoke(app, ["rules", "list", "--language", "c"], env={"COLUMNS": "220"})
    assert result.exit_code == 0, result.output
    line = next(row for row in result.output.splitlines() if "C-MEM-001" in row)
    assert "kapalı" in line
    other = next(row for row in result.output.splitlines() if "C-MEM-002" in row)
    assert "açık" in other


def test_root_help_is_utf8() -> None:
    """Kök `--help` gerçek konsol girişinden (cp125x olabilir) UTF-8 baytları basar (O11)."""
    env = {**os.environ, "PYTHONIOENCODING": "cp1254", "COLUMNS": "120"}
    out = subprocess.run(
        [sys.executable, "-c", "from codementor.cli.main import run; run()", "--help"],
        capture_output=True,
        env=env,
        check=False,
        timeout=60,
    )
    assert out.returncode == 0, out.stderr
    assert "kodu düzeltmeyen".encode() in out.stdout
