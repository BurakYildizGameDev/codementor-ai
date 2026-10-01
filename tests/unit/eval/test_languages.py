"""Eval altyapısında Python/HTML/CSS örnekleri ve dil filtresi (Faz 18)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from codementor.cli.main import app
from codementor.config import Settings
from codementor.eval.compare import load_results
from codementor.eval.dataset import DatasetError, load_split
from codementor.eval.runner import result_filename, run_eval
from codementor.models.enums import PipelineMode

pytestmark = pytest.mark.anyio

PY_CODE = """\
def has_duplicate(items):
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False
"""
HTML_CODE = """\
<!DOCTYPE html>
<html lang="tr">
<head><title>Profil</title></head>
<body>
  <img src="foto.png">
  <h1>Ada</h1>
</body>
</html>
"""
CSS_CODE = """\
.card {
  width: 320px;
  color: #333;
}
"""
LABELS = {
    "python-001": ("python", "py", 'time_complexity: "n^2"\n  findings: []'),
    "html-001": (
        "html",
        "html",
        "findings:\n    - { category: accessibility, line: 5, rule_id: HTML-ACC-001 }",
    ),
    "css-001": ("css", "css", "findings: []"),
}
CODES = {"python-001": PY_CODE, "html-001": HTML_CODE, "css-001": CSS_CODE}


def _write(root: Path, split: str, sample_id: str, suffix: str | None = None) -> None:
    language, ext, expected = LABELS[sample_id]
    directory = root / split / sample_id
    directory.mkdir(parents=True)
    (directory / f"code.{suffix or ext}").write_text(CODES[sample_id], encoding="utf-8")
    (directory / "label.yaml").write_text(
        f"id: {sample_id}\nlanguage: {language}\nengine: none\nsyntax_valid: true\n"
        f"expected:\n  compilation_status: passed\n  {expected}\nsplit: {split}\n"
        "reviewed: true\n",
        encoding="utf-8",
    )


@pytest.fixture
def dataset(tmp_path: Path) -> Path:
    root = tmp_path / "dataset"
    for sample_id in LABELS:
        _write(root, "dev", sample_id)
    return root


def test_load_python_html_css_samples(dataset: Path) -> None:
    samples = load_split(dataset, "dev")
    assert [(s.label.id, s.label.language.value) for s in samples] == [
        ("css-001", "css"),
        ("html-001", "html"),
        ("python-001", "python"),
    ]
    assert samples[2].label.expected.time_complexity == "n^2"


def test_wrong_suffix_for_markup_rejected(tmp_path: Path) -> None:
    root = tmp_path / "dataset"
    _write(root, "dev", "html-001", suffix="htm")
    with pytest.raises(DatasetError, match=r"\.html olmalı"):
        load_split(root, "dev")


async def test_run_eval_language_filter(dataset: Path, settings: Settings) -> None:
    result = await run_eval(
        load_split(dataset, "dev"),
        settings,
        split="dev",
        provider=None,
        mode=PipelineMode.TWO_PASS,
        static_only=True,
        languages=["html", "css"],
    )
    assert result.config.languages == ["css", "html"]
    assert result.config.sample_ids == ["css-001", "html-001"]
    assert [s.id for s in result.samples] == ["css-001", "html-001"]
    assert result_filename(result.config).endswith("_static_css-html_dev.json")


async def test_run_eval_unknown_language_rejected(dataset: Path, settings: Settings) -> None:
    with pytest.raises(ValueError, match="Bilinmeyen dil"):
        await run_eval(
            load_split(dataset, "dev"),
            settings,
            split="dev",
            provider=None,
            mode=PipelineMode.TWO_PASS,
            static_only=True,
            languages=["cobol"],
        )


async def test_markup_sample_metrics_skip_complexity(dataset: Path, settings: Settings) -> None:
    result = await run_eval(
        load_split(dataset, "dev"),
        settings,
        split="dev",
        provider=None,
        mode=PipelineMode.TWO_PASS,
        static_only=True,
        languages=["html"],
    )
    (sample,) = result.samples
    assert sample.error is None
    assert sample.report is not None
    assert sample.report.complexity is None
    assert result.metrics.complexity_time_exact_acc is None  # Big-O paydası 0
    assert result.metrics.audit_recall == 1.0  # HTML-ACC-001, 5. satır


def test_eval_run_language_option(
    dataset: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = tmp_path / "cfg.toml"
    config.write_text(
        '[validation]\ntier1_enabled = false\n[providers]\ndefault = "fake"\nfallback = []\n',
        encoding="utf-8",
    )
    monkeypatch.setenv("CODEMENTOR_CONFIG_FILE", str(config))
    out = tmp_path / "results"
    args = ["eval", "run", "--split", "dev", "--static-only", "--dataset", str(dataset)]
    run = CliRunner().invoke(app, [*args, "--language", "python", "--out-dir", str(out)])
    assert run.exit_code == 0, run.output
    (path,) = out.glob("*_python_dev.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["config"]["languages"] == ["python"]
    assert data["config"]["sample_ids"] == ["python-001"]
    bad = CliRunner().invoke(app, [*args, "--language", "cobol", "--out-dir", str(out)])
    assert bad.exit_code == 2


def test_eval_run_language_filter_applied_before_limit(
    dataset: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Denetim: `--limit 1` dil filtresinden sonra uygulanmalı (ilk örnek css-001 değil)."""
    config = tmp_path / "cfg.toml"
    config.write_text(
        '[validation]\ntier1_enabled = false\n[providers]\ndefault = "fake"\nfallback = []\n',
        encoding="utf-8",
    )
    monkeypatch.setenv("CODEMENTOR_CONFIG_FILE", str(config))
    out = tmp_path / "results"
    args = ["eval", "run", "--split", "dev", "--static-only", "--dataset", str(dataset)]
    run = CliRunner().invoke(
        app, [*args, "--language", "python", "--limit", "1", "--out-dir", str(out)]
    )
    assert run.exit_code == 0, run.output
    (path,) = out.glob("*.json")
    assert json.loads(path.read_text(encoding="utf-8"))["config"]["sample_ids"] == ["python-001"]
    empty = CliRunner().invoke(app, [*args, "--language", "c", "--out-dir", str(out)])
    assert empty.exit_code == 2  # filtre sonrası örnek yok: boş sonuç dosyası yazılmaz
    assert len(list(out.glob("*.json"))) == 1


def test_old_result_without_languages_loads() -> None:
    """Faz 18 öncesi sonuç dosyalarında `languages` alanı yok; varsayılan boş liste."""
    results = Path(__file__).resolve().parents[3] / "eval" / "results"
    old = results / "20260930T181653_claude_cli_claude-opus-5-5_two_pass_test.json"
    data = json.loads(old.read_text(encoding="utf-8"))
    assert "languages" not in data["config"]
    (result,) = load_results([old])
    assert result.config.languages == []
