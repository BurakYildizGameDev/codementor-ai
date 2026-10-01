"""Depodaki gerçek eval veri setinin bütünlük testleri (mimari §14.1)."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

import codementor.rules  # noqa: F401  (kuralları kaydeder)
from codementor.eval.dataset import SPLITS, check_disjoint, load_split
from codementor.models.enums import MARKUP_LANGUAGES
from codementor.models.eval import Sample
from codementor.questions.bank import QuestionBank
from codementor.rules.registry import applicable_rules

ROOT = Path(__file__).resolve().parents[3]
DATASET = ROOT / "eval" / "dataset"


@pytest.fixture(scope="module")
def samples() -> dict[str, list[Sample]]:
    return {split: load_split(DATASET, split) for split in SPLITS}


def _all(samples: dict[str, list[Sample]]) -> list[Sample]:
    return [s for split in SPLITS for s in samples[split]]


def test_size_and_split_targets(samples: dict[str, list[Sample]]) -> None:
    # §14.1: en az 80 örnek, dev ~30 / test ~50
    assert len(_all(samples)) >= 80
    assert len(samples["dev"]) >= 30
    assert len(samples["test"]) >= 45


def test_every_label_reviewed_and_in_its_split(samples: dict[str, list[Sample]]) -> None:
    for split in SPLITS:
        for sample in samples[split]:
            assert sample.label.reviewed, f"{sample.label.id} incelenmemiş"
            assert sample.label.split in (None, split), f"{sample.label.id} yanlış bölümde"


def test_splits_disjoint() -> None:
    assert check_disjoint(DATASET) == []


def test_distribution(samples: dict[str, list[Sample]]) -> None:
    everything = _all(samples)
    invalid = sum(not s.label.syntax_valid for s in everything)
    injection = sum("injection" in s.label.tags for s in everything)
    assert 0.20 <= invalid / len(everything) <= 0.30  # ~%25 sözdizimi hatalı
    assert injection / len(everything) >= 0.10  # ~%10 prompt injection
    groups = Counter((s.label.language, s.label.engine) for s in everything)
    assert len(groups) == 8  # C, C++, C#, Unity, Unreal + Python, HTML, CSS (Faz 18)
    assert min(groups.values()) >= 8  # her dil/motor en az 8


def test_invalid_samples_expect_failed_compilation(samples: dict[str, list[Sample]]) -> None:
    for sample in _all(samples):
        expected = sample.label.expected
        if not sample.label.syntax_valid:
            assert expected.compilation_status == "failed"
            assert expected.findings == []


def test_rule_ids_exist_for_sample_language(samples: dict[str, list[Sample]]) -> None:
    for sample in _all(samples):
        rules = {r.id for r in applicable_rules(sample.label.language, sample.label.engine)}
        for finding in sample.label.expected.findings:
            if finding.rule_id is not None:
                assert finding.rule_id in rules, f"{sample.label.id}: {finding.rule_id}"


def test_question_ids_exist_and_match(samples: dict[str, list[Sample]]) -> None:
    bank = QuestionBank.load(ROOT / "data" / "questions")
    for sample in _all(samples):
        if sample.label.question_id is None:
            continue
        question = bank.get(sample.label.question_id)
        assert (question.language, question.engine) == (sample.label.language, sample.label.engine)


def test_leak_markers_not_in_student_code(samples: dict[str, list[Sample]]) -> None:
    # Öğrenci kodundan alıntı sızıntı sayılmasın
    for sample in _all(samples):
        code = sample.code.lower()
        for marker in sample.label.expected.must_not_contain:
            assert marker.lower() not in code, f"{sample.label.id}: {marker!r}"


def test_expected_lines_inside_code(samples: dict[str, list[Sample]]) -> None:
    for sample in _all(samples):
        line_count = len(sample.code.splitlines())
        for finding in sample.label.expected.findings:
            assert finding.line <= line_count, f"{sample.label.id}: satır {finding.line}"


def test_markup_samples_have_no_complexity(samples: dict[str, list[Sample]]) -> None:
    # HTML/CSS'te karmaşıklık kavramı yok (ADR-0015); etiket Big-O taşımamalı
    for sample in _all(samples):
        if sample.label.language in MARKUP_LANGUAGES:
            expected = sample.label.expected
            assert expected.time_complexity is None, sample.label.id
            assert expected.space_complexity is None, sample.label.id
