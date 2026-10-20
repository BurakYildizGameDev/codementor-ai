"""Veri seti ve etiket sürümü (Faz 51/İş 7) testleri:
`dataset_version` determinizmi, satır sonu toleransı, compare dipnotu ve
eski koşuların sessizce yeniden puanlanmasını önleyen uyuşmazlık uyarısı.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console

from codementor.cli.eval import _result_and_labels
from codementor.eval.compare import compare_table
from codementor.eval.dataset import DATASET_DIR, dataset_version, load_sample
from codementor.models.enums import AuditCategory, CompilationStatus, Engine, Language
from codementor.models.eval import (
    Expected,
    ExpectedFinding,
    Label,
    Metrics,
    RunConfig,
    RunResult,
    Sample,
)


def _sample(sample_id: str = "c-001", code: str = "int main() { return 0; }") -> Sample:
    label = Label(
        id=sample_id,
        language=Language.C,
        engine=Engine.NONE,
        syntax_valid=True,
        expected=Expected(
            compilation_status=CompilationStatus.PASSED,
            findings=[ExpectedFinding(category=AuditCategory.PERFORMANCE, line=1)],
        ),
        reviewed=True,
    )
    return Sample(label=label, code=code, path=f"eval/dataset/dev/{sample_id}")


def _run_result(dataset_ver: str | None = "d1+12345678", sample_id: str = "c-001") -> RunResult:
    config = RunConfig(
        split="dev",
        provider=None,
        model=None,
        mode="static",
        static_only=True,
        ablations=[],
        prompt_version="v1+12345678",
        rules_version="r3+12345678",
        schema_version="1.0.0",
        started_at=datetime.now(UTC),
        sample_ids=[sample_id],
        reviewed_only=True,
        dataset_version=dataset_ver,
    )
    metrics = Metrics(samples=1)
    return RunResult(config=config, metrics=metrics, samples=[])


def test_dataset_version_is_deterministic() -> None:
    v1 = dataset_version(DATASET_DIR)
    v2 = dataset_version(DATASET_DIR)
    assert v1 == v2
    assert v1.startswith("d1+")
    assert len(v1) == 11  # "d1+" + 8 hex chars


def test_dataset_version_normalizes_crlf() -> None:
    s1 = _sample(code="int main() {\n    return 0;\n}\n")
    s2 = _sample(code="int main() {\r\n    return 0;\r\n}\r\n")
    assert dataset_version([s1]) == dataset_version([s2])


def test_dataset_version_changes_on_label_change() -> None:
    s1 = _sample()
    s2 = _sample()
    s2.label.expected.findings[0].line = 2
    assert dataset_version([s1]) != dataset_version([s2])


def test_dataset_version_changes_on_code_change() -> None:
    s1 = _sample(code="int a = 1;")
    s2 = _sample(code="int a = 2;")
    assert dataset_version([s1]) != dataset_version([s2])


def test_compare_table_includes_dataset_version_footnote() -> None:
    r = _run_result(dataset_ver="d1+abcdef12")
    table = compare_table([r])
    assert "veri seti d1+abcdef12" in table
    assert "farklı veri seti sürümleri" not in table


def test_compare_table_warns_on_mismatched_dataset_versions() -> None:
    r1 = _run_result(dataset_ver="d1+11111111")
    r2 = _run_result(dataset_ver="d1+22222222")
    table = compare_table([r1, r2])
    assert "veri seti d1+11111111" in table
    assert "veri seti d1+22222222" in table
    assert "⚠ Tabloda farklı veri seti sürümleri var; satırlar doğrudan kıyaslanamaz." in table


def test_result_and_labels_warns_on_dataset_version_mismatch(tmp_path: Path) -> None:
    # Gerçek veri setinden bir örnek alıp geçici dizine koyalım
    real_sample = load_sample(DATASET_DIR / "dev" / "c-001")
    dev_dir = tmp_path / "dev" / "c-001"
    dev_dir.mkdir(parents=True)
    (dev_dir / "code.c").write_text(real_sample.code, encoding="utf-8")
    (dev_dir / "label.yaml").write_text(real_sample.label.model_dump_json(), encoding="utf-8")

    result_file = tmp_path / "result.json"
    result = _run_result(dataset_ver="d1+eski_surum", sample_id="c-001")
    result_file.write_text(result.model_dump_json(), encoding="utf-8")

    console = Console(record=True)
    _res, labels = _result_and_labels(result_file, tmp_path, console)

    assert "c-001" in labels
    output = console.export_text()
    assert "Kayıtlı veri seti (d1+eski_surum) ile diskteki etiketler" in output
    assert "uyuşmuyor" in output


def test_result_and_labels_no_warning_when_versions_match(tmp_path: Path) -> None:
    real_sample = load_sample(DATASET_DIR / "dev" / "c-001")
    dev_dir = tmp_path / "dev" / "c-001"
    dev_dir.mkdir(parents=True)
    (dev_dir / "code.c").write_text(real_sample.code, encoding="utf-8")
    (dev_dir / "label.yaml").write_text(real_sample.label.model_dump_json(), encoding="utf-8")

    actual_ver = dataset_version([real_sample])
    result_file = tmp_path / "result.json"
    result = _run_result(dataset_ver=actual_ver, sample_id="c-001")
    result_file.write_text(result.model_dump_json(), encoding="utf-8")

    console = Console(record=True)
    _res, labels = _result_and_labels(result_file, tmp_path, console)

    assert "c-001" in labels
    output = console.export_text()
    assert "uyuşmuyor" not in output
