"""`prompt_version` (mimari §5.4.4)."""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path
from typing import Any

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


def test_rules_version_covers_analysis_and_call_costs(tmp_path: Path) -> None:
    """Faz 31: maliyet tablosu ya da analiz modülü değişince önbellek bayatlamamalı."""
    from codementor.pipeline.versions import hashed_sources, rules_version

    names = {p.parent.name + "/" + p.name for p in hashed_sources()}
    assert any(n.startswith("rules/") for n in names)
    assert any(n.startswith("analysis/") for n in names)
    costs = tmp_path / "call_costs.yaml"
    costs.write_text("a: 1\n", encoding="utf-8")
    first = rules_version(costs)
    costs.write_text("a: 2\n", encoding="utf-8")
    assert rules_version(costs) != first
    crlf = tmp_path / "crlf.yaml"
    crlf.write_bytes(b"a: 2\r\n")
    assert rules_version(crlf) == rules_version(costs)  # satır sonu farkı sürümü değiştirmez


def test_hashed_sources_cover_queries_validation_verify() -> None:
    """Faz 49: tree-sitter sorguları, Tier 0/1 ve bulgu doğrulama da önbellek imzasında."""
    from codementor.pipeline.versions import SOURCE_ROOT, hashed_sources

    names = {p.relative_to(SOURCE_ROOT).as_posix() for p in hashed_sources()}
    assert any(n.startswith("analysis/queries/") and n.endswith(".scm") for n in names)
    assert "validation/tier0.py" in names
    assert "validation/tier1.py" in names
    assert "verify/proof.py" in names
    assert not any("__pycache__" in n for n in names)


def test_digest_changes_when_scm_changes(tmp_path: Path) -> None:
    """Kabul: bir `.scm` sorgusu değişince özet (dolayısıyla `rules_version`) değişir."""
    from codementor.pipeline.versions import digest_files

    query = tmp_path / "analysis" / "queries" / "c" / "loops.scm"
    query.parent.mkdir(parents=True)
    query.write_bytes(b"(for_statement) @loop\n")
    first = digest_files([query], tmp_path)
    query.write_bytes(b"(while_statement) @loop\n")
    changed = digest_files([query], tmp_path)
    assert changed != first
    query.write_bytes(b"(while_statement) @loop\r\n")
    assert digest_files([query], tmp_path) == changed  # satır sonu farkı sayılmaz


def test_rules_version_changes_with_mentor_templates(tmp_path: Path) -> None:
    """Faz 49: erken çıkış ve bozulmuş Sokratik şablonları değişince önbellek bayatlamaz."""
    from codementor.pipeline.versions import rules_version

    templates = tmp_path / "mentor_templates.yaml"
    templates.write_text("a: 1\n", encoding="utf-8")
    first = rules_version(None, templates)
    assert first.startswith("r2+")
    templates.write_text("a: 2\n", encoding="utf-8")
    assert rules_version(None, templates) != first


def test_empty_sources_logged(
    monkeypatch: pytest.MonkeyPatch, captured_logs: Callable[[], list[dict[str, Any]]]
) -> None:
    """Denetim K1: paketlenmiş exe'de kaynak yoksa sessiz kalmaz (imza zayıflar, Faz 50)."""
    from codementor.pipeline import versions

    monkeypatch.setattr(versions, "hashed_sources", list)
    versions._code_digest.cache_clear()
    try:
        assert versions.rules_version().startswith("r2+")
    finally:
        versions._code_digest.cache_clear()
    assert [e["event"] for e in captured_logs()] == ["rules_version_without_sources"]


def test_embedded_digest_used_when_sources_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    captured_logs: Callable[[], list[dict[str, Any]]],
) -> None:
    """Faz 50: exe'de kaynak yok ama derleme anında gömülen özet var → uyarı yok, sürüm özete
    bağlı (kural gövdesi değişen yeni exe eski önbelleği kullanmaz)."""
    from codementor.pipeline import versions

    embedded = tmp_path / versions.DIGEST_FILE
    monkeypatch.setattr(versions, "hashed_sources", list)
    monkeypatch.setattr(versions, "EMBEDDED_DIGEST", embedded)
    try:
        embedded.write_text("a" * 64, encoding="utf-8")
        versions._code_digest.cache_clear()
        first = versions.rules_version()
        embedded.write_text("b" * 64, encoding="utf-8")
        versions._code_digest.cache_clear()
        assert versions.rules_version() != first
    finally:
        versions._code_digest.cache_clear()
    assert captured_logs() == []
