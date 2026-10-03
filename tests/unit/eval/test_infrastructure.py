"""Eval altyapısı: veri seti yükleme/taşıma, koşucu (önbellek kapalı, static-only, ablasyon),
karşılaştırma tablosu, taslak kontrolü, CLI."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

from codementor.cli.main import app
from codementor.config import Settings
from codementor.eval.compare import compare_table, load_results
from codementor.eval.dataset import DatasetError, check_disjoint, load_split, promote
from codementor.eval.review import check_draft
from codementor.eval.runner import apply_ablations, result_filename, run_eval, save_result
from codementor.models.enums import PipelineMode
from codementor.models.eval import RunResult
from codementor.providers.base import RetryPolicy
from codementor.providers.fake import FakeProvider, FakeReply
from tests.integration.conftest import (
    BROKEN_C,
    LINKED_LIST,
    analysis_reply,
    socratic_reply,
)

LABEL_OK = """\
# inceleme notu: korunmalı
id: {id}
language: c
engine: none
question_id: c-medium-linked-list
syntax_valid: true
expected:
  compilation_status: passed
  time_complexity: "O(n)"
  findings:
    - {{ category: memory_safety, line: 31, note: "free sonrası erişim" }}
  must_not_contain: ["Node *next ="]
tags: [injection-none]
split: dev
"""
# Bozuk kod için yanlış etiket: sözdizimi geçerli diyor, sızıntı işareti kodda zaten var
LABEL_WRONG = """\
id: {id}
language: c
engine: none
syntax_valid: true
expected:
  compilation_status: passed
  must_not_contain: ["int x = 1"]
"""
LABEL_BROKEN = """\
id: {id}
language: c
engine: none
syntax_valid: false
expected:
  compilation_status: failed
tags: [syntax]
"""


def _sample(root: Path, split: str, sample_id: str, code: str, label: str) -> Path:
    directory = root / split / sample_id
    directory.mkdir(parents=True)
    (directory / "code.c").write_text(code, encoding="utf-8")
    (directory / "label.yaml").write_text(label.format(id=sample_id), encoding="utf-8")
    return directory


@pytest.fixture
def dataset(tmp_path: Path) -> Path:
    root = tmp_path / "dataset"
    _sample(root, "_draft", "c-001", LINKED_LIST, LABEL_OK)
    _sample(root, "_draft", "c-002", BROKEN_C, LABEL_BROKEN)
    return root


# --- veri seti --------------------------------------------------------------------------------


def test_load_and_validate(dataset: Path) -> None:
    samples = load_split(dataset, "_draft")
    assert [s.label.id for s in samples] == ["c-001", "c-002"]
    assert samples[0].label.expected.time_complexity == "n"  # kanonik
    assert not samples[0].label.reviewed


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda t: t.replace("line: 31", "line: 999"), "999. satır kodda yok"),
        (lambda t: t.replace("syntax_valid: true", "syntax_valid: false"), "çelişiyor"),
        (lambda t: t.replace("id: c-001", "id: c-009"), "dizin adıyla"),
        (lambda t: t.replace("memory_safety", "bellek"), "geçersiz değer"),
    ],
)
def test_invalid_labels_rejected(dataset: Path, change: Any, message: str) -> None:
    path = dataset / "_draft" / "c-001" / "label.yaml"
    path.write_text(change(path.read_text(encoding="utf-8")), encoding="utf-8")
    with pytest.raises(DatasetError, match=message):
        load_split(dataset, "_draft")


def test_wrong_code_extension_rejected(dataset: Path) -> None:
    (dataset / "_draft" / "c-001" / "code.c").rename(dataset / "_draft" / "c-001" / "code.cpp")
    with pytest.raises(DatasetError, match=r"\.c olmalı"):
        load_split(dataset, "_draft")


def test_promote_marks_reviewed_and_keeps_comments(dataset: Path) -> None:
    target = promote(dataset, "c-001", "dev")
    text = (target / "label.yaml").read_text(encoding="utf-8")
    assert "# inceleme notu: korunmalı" in text
    assert "reviewed: true" in text
    (sample,) = load_split(dataset, "dev")
    assert sample.label.reviewed
    assert sample.label.split == "dev"
    with pytest.raises(DatasetError, match="Taslak bulunamadı"):
        promote(dataset, "c-001", "test")


def test_disjoint_detects_duplicate_code(dataset: Path) -> None:
    _sample(dataset, "test", "c-003", LINKED_LIST.replace("\n", "\n\n"), LABEL_OK)
    problems = check_disjoint(dataset)
    assert any("c-003" in p and "kod" in p for p in problems)


# --- koşucu -----------------------------------------------------------------------------------

pytestmark = pytest.mark.anyio


async def test_static_only_run(dataset: Path, settings: Settings) -> None:
    samples = load_split(dataset, "_draft")
    result = await run_eval(
        samples, settings, split="dev", provider=None, mode=PipelineMode.TWO_PASS, static_only=True
    )
    assert result.config.static_only
    assert result.config.provider is None
    assert not result.config.reviewed_only
    assert [s.llm_called for s in result.samples] == [False, False]
    assert result.metrics.early_exit_precision == 1.0
    assert result.metrics.early_exit_recall == 1.0
    assert result.metrics.schema_valid_first_try is None  # LLM yok


async def test_llm_run_uses_no_cache_and_records_schema(dataset: Path, settings: Settings) -> None:
    provider = FakeProvider(
        script=[
            FakeReply(data={"bozuk": 1}),  # ilk yanıt şemaya uymaz → onarım
            FakeReply(data=analysis_reply()),
            FakeReply(data=socratic_reply()),
        ],
        retry=RetryPolicy(max_retries=0),
    )
    samples = load_split(dataset, "_draft")[:1]
    result = await run_eval(
        samples * 1,
        settings,
        split="dev",
        provider="fake",
        mode=PipelineMode.TWO_PASS,
        provider_factory=lambda _n: provider,
    )
    (sample,) = result.samples
    assert sample.llm_called
    assert sample.schema_first_try is False
    assert sample.schema_final is True
    assert result.metrics.schema_valid_first_try == 0.0
    assert result.metrics.schema_valid_after_repair == 1.0
    assert sample.report is not None
    assert sample.report.meta.cache_hit is False


def test_ablations(settings: Settings) -> None:
    ablated = apply_ablations(settings, ["facts", "line_numbers", "fewshot0"])
    assert not ablated.prompts.include_facts
    assert not ablated.prompts.numbered_code
    assert ablated.prompts.max_fewshots == 0
    assert apply_ablations(settings, ["fewshot1"]).prompts.max_fewshots == 1
    with pytest.raises(ValueError, match="Bilinmeyen ablasyon"):
        apply_ablations(settings, ["hepsi"])


async def test_ablated_prompt_has_no_facts_or_numbers(dataset: Path, settings: Settings) -> None:
    provider = FakeProvider(
        script=[
            FakeReply(data=analysis_reply(agreement="no_hint")),
            FakeReply(data=socratic_reply()),
        ],
        retry=RetryPolicy(max_retries=0),
    )
    result = await run_eval(
        load_split(dataset, "_draft")[:1],
        settings,
        split="dev",
        provider="fake",
        mode=PipelineMode.TWO_PASS,
        ablations=["facts", "line_numbers"],
        provider_factory=lambda _n: provider,
    )
    prompt = provider.calls[0].messages[-1].content
    assert "## Statik olgular" not in prompt
    assert "Statik ipucu yok" in prompt
    assert " 1 | #include" not in prompt  # öğrenci kodu da few-shot kodu da numarasız
    assert "#include <stdio.h>" in prompt
    assert result.config.ablations == ["facts", "line_numbers"]
    assert result.samples[0].report is not None
    assert not result.samples[0].report.meta.degraded  # ipucu yokken çatışma onarımı istenmez


async def test_save_compare_roundtrip(dataset: Path, settings: Settings, tmp_path: Path) -> None:
    result = await run_eval(
        load_split(dataset, "_draft"),
        settings,
        split="dev",
        provider=None,
        mode=PipelineMode.TWO_PASS,
        static_only=True,
    )
    path = save_result(result, tmp_path / "results")
    assert path.name == result_filename(result.config)
    assert path.name.endswith("_static_none_static_dev.json")
    loaded = load_results([path])
    assert isinstance(loaded[0], RunResult)
    table = compare_table(loaded)
    assert "Yalnızca statik (LLM yok)" in table
    assert "⚠ incelenmemiş" in table
    assert "Sürümler: prompt v1+" in table


async def test_check_draft_flags_problems(dataset: Path, settings: Settings) -> None:
    good, broken = load_split(dataset, "_draft")
    assert (await check_draft(broken, settings)).ok
    path = dataset / "_draft" / "c-002" / "label.yaml"
    path.write_text(LABEL_WRONG.format(id="c-002"), encoding="utf-8")
    (reloaded,) = [s for s in load_split(dataset, "_draft") if s.label.id == "c-002"]
    check = await check_draft(reloaded, settings)
    assert any("derlenmiyor" in p for p in check.problems)
    assert any("öğrenci kodunda zaten geçiyor" in p for p in check.problems)
    assert good.label.id == "c-001"


# --- CLI --------------------------------------------------------------------------------------


def test_cli_run_test_split_requires_final(dataset: Path) -> None:
    result = CliRunner().invoke(app, ["eval", "run", "--split", "test", "--dataset", str(dataset)])
    assert result.exit_code == 2
    assert "--final" in result.output


def test_cli_static_only_and_compare(
    dataset: Path, tmp_path: Path, settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = tmp_path / "cfg.toml"
    config.write_text(
        '[validation]\ntier1_enabled = false\n[providers]\ndefault = "fake"\nfallback = []\n',
        encoding="utf-8",
    )
    monkeypatch.setenv("CODEMENTOR_CONFIG_FILE", str(config))
    promote(dataset, "c-002", "dev")
    out = tmp_path / "results"
    runner = CliRunner()
    run = runner.invoke(
        app,
        [
            "eval",
            "run",
            "--split",
            "dev",
            "--static-only",
            "--dataset",
            str(dataset),
            "--out-dir",
            str(out),
        ],
    )
    assert run.exit_code == 0, run.output
    (path,) = out.glob("*.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["config"]["static_only"] is True
    assert data["config"]["reviewed_only"] is True
    compared = runner.invoke(app, ["eval", "compare", str(path)])
    assert "Yalnızca statik" in compared.output


def test_cli_check_drafts_and_promote(dataset: Path) -> None:
    runner = CliRunner()
    checked = runner.invoke(app, ["eval", "check-drafts", "--dataset", str(dataset)])
    assert "c-001" in checked.output
    moved = runner.invoke(
        app, ["eval", "promote", "c-002", "--split", "test", "--dataset", str(dataset)]
    )
    assert moved.exit_code == 0
    assert (dataset / "test" / "c-002").is_dir()


def test_verify_ablation_enables_flag(settings: Settings) -> None:
    """Faz 35: `--ablation verify` doğrulama geçişini açar; diğer ayarlara dokunmaz."""
    assert not settings.pipeline.verify_findings
    enabled = apply_ablations(settings, ["verify"])
    assert enabled.pipeline.verify_findings
    assert enabled.prompts == settings.prompts
    assert not apply_ablations(settings, ["fewshot0"]).pipeline.verify_findings


def test_compare_static_row_has_no_injection_score() -> None:
    """Faz 31: LLM'siz koşuda injection direnci anlamsız; tabloda '—'."""
    from codementor.eval.compare import HEADERS, row
    from codementor.models.eval import Metrics, RunConfig, RunResult

    result = RunResult(
        config=RunConfig(
            split="dev",
            provider=None,
            model=None,
            mode="static",
            static_only=True,
            prompt_version="v1",
            rules_version="r1",
            schema_version="1.0",
            started_at=datetime(2026, 10, 3, tzinfo=UTC),
            sample_ids=[],
        ),
        metrics=Metrics(samples=1, injection_resistance=1.0),
        samples=[],
    )
    cells = dict(zip(HEADERS, row(result), strict=True))
    injection = next(k for k in cells if "njection" in k)
    assert cells[injection] == "—"
