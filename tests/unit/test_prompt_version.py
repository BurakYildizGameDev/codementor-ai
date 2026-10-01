"""`prompt_version` (mimari §5.4.4)."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from codementor.prompts.builder import (
    build_analysis_messages,
)
from codementor.prompts.templates import prompt_version
from tests.unit.prompt_helpers import (
    REPO_PROMPTS,
    analysis_input,
    prompt_settings,
)

# --- prompt_version ----------------------------------------------------------------------


def test_prompt_version_format() -> None:
    version = prompt_version(REPO_PROMPTS)
    assert version.startswith("v1+")
    assert len(version) == len("v1+") + 8


def test_prompt_version_changes_when_template_changes(tmp_path: Path) -> None:
    copy = tmp_path / "v1"
    shutil.copytree(REPO_PROMPTS, copy)
    before = prompt_version(copy)
    template = copy / "analysis.system.j2"
    template.write_text(template.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    assert prompt_version(copy) != before


def test_prompt_version_changes_when_fewshot_changes(tmp_path: Path) -> None:
    copy = tmp_path / "v1"
    shutil.copytree(REPO_PROMPTS, copy)
    before = prompt_version(copy)
    fewshot = sorted((copy / "fewshots").glob("*.yaml"))[0]
    fewshot.write_text(fewshot.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    assert prompt_version(copy) != before


def test_prompt_version_ignores_line_endings(tmp_path: Path) -> None:
    copy = tmp_path / "v1"
    shutil.copytree(REPO_PROMPTS, copy)
    before = prompt_version(copy)
    for path in copy.rglob("*.j2"):
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    assert prompt_version(copy) == before


def test_built_prompt_carries_version(tmp_path: Path) -> None:
    built = build_analysis_messages(analysis_input(tmp_path), settings=prompt_settings())
    assert built.prompt_version == prompt_version(REPO_PROMPTS)


def test_missing_template_dir_error_is_turkish(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Prompt şablon dizini bulunamadı"):
        build_analysis_messages(
            analysis_input(tmp_path), settings=prompt_settings(tmp_path / "yok")
        )


def test_prompt_version_cached_until_files_change(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Faz 26: dosya listesi/mtime/boyut değişmedikçe şablonlar yeniden okunmaz."""
    directory = tmp_path / "v1"
    shutil.copytree(REPO_PROMPTS, directory)
    first = prompt_version(directory)
    reads: list[Path] = []
    original = Path.read_bytes

    def counting(self: Path) -> bytes:
        reads.append(self)
        return original(self)

    monkeypatch.setattr(Path, "read_bytes", counting)
    assert prompt_version(directory) == first
    assert reads == []

    template = directory / "analysis.user.j2"
    template.write_text(template.read_text(encoding="utf-8") + "\nek satır", encoding="utf-8")
    assert prompt_version(directory) != first
    assert reads


def test_prompt_version_detects_new_file(tmp_path: Path) -> None:
    directory = tmp_path / "v1"
    shutil.copytree(REPO_PROMPTS, directory)
    first = prompt_version(directory)
    (directory / "yeni.j2").write_text("{{ x }}", encoding="utf-8")
    assert prompt_version(directory) != first
