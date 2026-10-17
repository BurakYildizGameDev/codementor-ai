"""Faz B (O3): önbellek imzası — derleyici kimliği/sürümü ve soru içeriği."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from codementor.config import Settings
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language, PipelineMode
from codementor.models.questions import Question
from codementor.models.request import LanguageHint
from codementor.models.validation import CompilerTool, Toolchain
from codementor.pipeline.signature import pipeline_signature, tier1_tool
from codementor.questions.bank import QuestionBank

REPO = Path(__file__).resolve().parents[2]
C_CODE = normalize("int main(void) { return 0; }\n", LanguageHint(language=Language.C))


@pytest.fixture
def settings() -> Settings:
    return Settings()


@pytest.fixture
def question() -> Question:
    return QuestionBank.load(REPO / "data" / "questions").get("c-medium-linked-list")


def _tool(path: Path) -> CompilerTool:
    return CompilerTool(name="gcc", kind="gcc", command=[str(path)])


def _sig(
    settings: Settings, tool: CompilerTool | None = None, question: Question | None = None
) -> str:
    return pipeline_signature(
        settings,
        mode=PipelineMode.TWO_PASS,
        validation=settings.validation,
        tool=tool,
        question=question,
    )


def test_signature_is_stable_and_readable(settings: Settings) -> None:
    first = _sig(settings)
    assert first == _sig(settings)
    flag = "+verify" if settings.pipeline.verify_findings else ""
    assert first.startswith(f"two_pass{flag}:")


def test_mode_and_verify_flag_kept_in_prefix(settings: Settings) -> None:
    off = settings.model_copy(
        update={"pipeline": settings.pipeline.model_copy(update={"verify_findings": False})}
    )
    single = pipeline_signature(
        off, mode=PipelineMode.SINGLE_PASS, validation=off.validation, tool=None, question=None
    )
    assert single.startswith("single_pass:")


def test_compiler_identity_changes_signature(settings: Settings, tmp_path: Path) -> None:
    gcc = tmp_path / "gcc.exe"
    gcc.write_bytes(b"v1")
    clang = tmp_path / "clang.exe"
    clang.write_bytes(b"v1")
    base = _sig(settings, _tool(gcc))
    assert base != _sig(settings)  # araç yok ↔ var
    assert base != _sig(settings, _tool(clang))  # başka araç


def test_compiler_upgrade_changes_signature(settings: Settings, tmp_path: Path) -> None:
    gcc = tmp_path / "gcc.exe"
    gcc.write_bytes(b"v1")
    before = _sig(settings, _tool(gcc))
    gcc.write_bytes(b"surum-2")  # aynı yol, yeni sürüm (boyut + zaman)
    stat = gcc.stat()
    os.utime(gcc, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))
    assert _sig(settings, _tool(gcc)) != before


def test_question_content_changes_signature(settings: Settings, question: Question) -> None:
    base = _sig(settings, question=question)
    assert base != _sig(settings)
    edited = question.model_copy(update={"prompt": question.prompt + " (güncellendi)"})
    assert _sig(settings, question=edited) != base


def test_tier1_tool_follows_config(settings: Settings, tmp_path: Path) -> None:
    gcc = tmp_path / "gcc.exe"
    gcc.write_bytes(b"v1")
    chain = Toolchain(c=_tool(gcc))
    enabled = settings.validation.model_copy(update={"tier1_enabled": True})
    disabled = settings.validation.model_copy(update={"tier1_enabled": False})
    assert tier1_tool(C_CODE, enabled, chain) == chain.c
    assert tier1_tool(C_CODE, disabled, chain) is None
    assert C_CODE.engine is Engine.NONE


def test_signature_ignores_checklist_stamps(settings: Settings, tmp_path: Path) -> None:
    """Faz J4/O3: kontrol listesi *içeriği* `rules_version`'da; imzada dosya damgası yok.

    Aksi hâlde içerik aynı kalıp yalnız dosya zamanı değiştiğinde (ör. `git checkout` ardından)
    gereksiz önbellek ıskası oluşurdu.
    """
    lists = tmp_path / "checklists"
    lists.mkdir()
    (lists / "c-core.yaml").write_bytes(b"items: []\n")
    other = settings.model_copy(
        update={"data": settings.data.model_copy(update={"checklists_dir": lists})}
    )
    assert _sig(other) == _sig(settings)
