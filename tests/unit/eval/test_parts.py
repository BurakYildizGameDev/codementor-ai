"""Dev bölümünü dengeli parçalara bölme (`eval run --part k/n`): canlı koşu bütçesi."""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import pytest
from typer.testing import CliRunner

from codementor.cli.main import app
from codementor.eval.breakdown import group_of
from codementor.eval.compare import compare_table
from codementor.eval.dataset import load_split
from codementor.eval.parts import (
    check_parts_coverage,
    parse_part,
    part_signature,
    sample_kind,
    select_part,
)
from codementor.models.eval import Metrics, RunConfig, RunResult

DATASET = Path(__file__).resolve().parents[3] / "eval" / "dataset"
SAMPLES = load_split(DATASET, "dev")
PARTS = 4


def _part(index: int) -> list[str]:
    return [s.label.id for s in select_part(SAMPLES, index, PARTS)]


def test_parts_are_disjoint_and_cover_split() -> None:
    parts = [_part(i) for i in range(1, PARTS + 1)]
    flat = [sample_id for part in parts for sample_id in part]
    assert sorted(flat) == sorted(s.label.id for s in SAMPLES)
    assert len(set(flat)) == len(flat)
    sizes = [len(p) for p in parts]
    assert max(sizes) - min(sizes) <= 1


@pytest.mark.parametrize("parts", [2, 3, 4, 5, 6])
@pytest.mark.parametrize("key", [lambda s: group_of(s.label), lambda s: sample_kind(s.label)])
def test_parts_are_balanced_per_group_and_kind(key: object, parts: int) -> None:
    """Her dil/motor grubu ve her örnek türü parçalara en fazla 1 farkla dağılır."""
    totals = Counter(key(s) for s in SAMPLES)  # type: ignore[operator]
    for index in range(1, parts + 1):
        counts = Counter(key(s) for s in select_part(SAMPLES, index, parts))  # type: ignore[operator]
        for value, total in totals.items():
            # pay ⌊total/n⌋ ya da ⌈total/n⌉ olmalı: parçalar arası fark en fazla 1
            assert abs(counts[value] - total / parts) < 1, (parts, index, value)


def test_parts_are_deterministic() -> None:
    assert [s.label.id for s in select_part(list(reversed(SAMPLES)), 1, PARTS)] == _part(1)


@pytest.mark.parametrize("spec", ["0/4", "5/4", "1/0", "a/4", "1-4", "2"])
def test_invalid_part_rejected(spec: str) -> None:
    with pytest.raises(ValueError, match="parça"):
        parse_part(spec)


def test_parse_part() -> None:
    assert parse_part("2/4") == (2, 4)


def test_cli_part_runs_subset_and_records_it(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "eval",
            "run",
            "--split",
            "dev",
            "--static-only",
            "--part",
            "1/4",
            "--out-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 0, result.output
    (path,) = tmp_path.glob("*.json")
    assert "_part1-4_" in path.name
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["config"]["part"] == "1/4"
    assert data["config"]["sample_ids"] == _part(1)


def test_cli_part_and_limit_conflict(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "eval",
            "run",
            "--split",
            "dev",
            "--static-only",
            "--part",
            "1/4",
            "--limit",
            "3",
            "--out-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code != 0
    assert "--part" in result.output


def test_part_signature_is_deterministic() -> None:
    sig1 = part_signature(SAMPLES, 4)
    sig2 = part_signature(list(reversed(SAMPLES)), 4)
    assert sig1 == sig2
    assert sig1.startswith("p4+")

    sig_other_parts = part_signature(SAMPLES, 3)
    assert sig_other_parts.startswith("p3+")
    assert sig_other_parts != sig1


def test_check_parts_coverage_detects_overlaps_and_missing() -> None:
    now = datetime.now(UTC)
    dummy_metrics = Metrics(samples=2)

    r1 = RunResult(
        config=RunConfig(
            split="dev",
            provider=None,
            model=None,
            mode="static",
            static_only=True,
            prompt_version="v1",
            rules_version="r3",
            schema_version="1.0.0",
            started_at=now,
            sample_ids=["py-001", "py-002"],
            part="1/2",
        ),
        metrics=dummy_metrics,
        samples=[],
    )
    r2 = RunResult(
        config=RunConfig(
            split="dev",
            provider=None,
            model=None,
            mode="static",
            static_only=True,
            prompt_version="v1",
            rules_version="r3",
            schema_version="1.0.0",
            started_at=now,
            sample_ids=["py-002", "cpp-001"],
            part="2/2",
        ),
        metrics=dummy_metrics,
        samples=[],
    )

    all_ids = ["py-001", "py-002", "cpp-001", "rs-001"]
    overlapping, missing = check_parts_coverage([r1, r2], all_sample_ids=all_ids)

    assert overlapping == ["py-002"]
    assert missing == ["rs-001"]

    table_output = compare_table([r1, r2])
    assert "Parçalı koşularda çakışan örnekler var: py-002" in table_output
