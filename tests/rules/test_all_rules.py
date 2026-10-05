"""Her kural için fixture tabanlı parametrik testler (mimari §15, Faz 6 kabul kriterleri)."""

from __future__ import annotations

import pytest

from codementor.models.enums import FindingKind, Severity
from codementor.rules import all_rules
from codementor.rules.base import Rule
from tests.rules._fixtures import FIXTURES, Fixture, all_fixtures

RULES: dict[str, type[Rule]] = {r.id: r for r in all_rules()}
_FIXTURES = all_fixtures()
POSITIVE = [f for f in _FIXTURES if f.kind == "positive"]
NEGATIVE = [f for f in _FIXTURES if f.kind == "negative"]


@pytest.mark.parametrize("fixture", POSITIVE, ids=lambda f: f.label)
def test_positive_fixture(fixture: Fixture) -> None:
    expected = fixture.expected_lines()
    assert expected, "pozitif fixture `// EXPECT: <satır>` içermeli"
    findings = fixture.findings(RULES[fixture.rule_id])
    assert {f.line_start for f in findings} == expected
    if (expected_kind := fixture.expected_kind()) is not None:
        assert {f.kind for f in findings} == {expected_kind}, fixture.label


@pytest.mark.parametrize("fixture", NEGATIVE, ids=lambda f: f.label)
def test_negative_fixture(fixture: Fixture) -> None:
    assert "EXPECT:" not in fixture.text
    assert fixture.findings(RULES[fixture.rule_id]) == []


@pytest.mark.parametrize("rule_id", sorted(RULES))
def test_every_registered_rule_has_fixtures(rule_id: str) -> None:
    for kind in ("positive", "negative"):
        count = sum(1 for f in _FIXTURES if f.rule_id == rule_id and f.kind == kind)
        assert count >= 2, f"{rule_id}: {kind} fixture sayısı {count} (en az 2)"


def test_every_fixture_dir_is_registered_rule() -> None:
    dirs = {p.name for p in FIXTURES.iterdir() if p.is_dir()}
    assert dirs <= set(RULES), dirs - set(RULES)
    kinds = {p.name for d in FIXTURES.iterdir() if d.is_dir() for p in d.iterdir()}
    assert kinds <= {"positive", "negative"}


def test_positive_findings_are_well_formed() -> None:
    for fixture in POSITIVE:
        rule = RULES[fixture.rule_id]
        for f in fixture.findings(rule):
            assert f.source == "static"
            assert f.category == rule.category
            # Faz 52 / ADR-0022: öneri her zaman düşük önemde; hata kural varsayılanını alır
            assert f.severity == (
                Severity.LOW if f.kind is FindingKind.SUGGESTION else rule.default_severity
            ), fixture.label
            assert f.evidence.strip(), fixture.label
