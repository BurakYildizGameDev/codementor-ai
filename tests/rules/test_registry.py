"""Kayıt defteri ve dil/motor filtresi (mimari §5.3.3, §8.1)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from codementor.config import CONFIG_FILE_ENV, get_settings
from codementor.models.enums import AuditCategory, Engine, Language, Severity
from codementor.rules import applicable_rules
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule, unregister_rule
from tests.rules._fixtures import FIXTURES
from tests.rules.test_engine import run

UNITY_FIXTURE = FIXTURES / "UNITY-GC-001" / "positive" / "list_in_update.cs"


def _ids(language: Language, engine: Engine, disabled: tuple[str, ...] = ()) -> set[str]:
    return {r.id for r in applicable_rules(language, engine, disabled)}


def _rule(rule_id: str) -> type[Rule]:
    return type(
        "Probe",
        (Rule,),
        {
            "id": rule_id,
            "title": "t",
            "description": "d",
            "languages": frozenset({Language.C}),
            "category": AuditCategory.DESIGN,
            "default_severity": Severity.LOW,
            "check": lambda self, ctx: [],
        },
    )


@pytest.fixture
def probe_cleanup() -> Iterator[None]:
    yield
    unregister_rule("TEST-PROBE-001")


@pytest.mark.usefixtures("probe_cleanup")
def test_duplicate_id_rejected() -> None:
    register_rule(_rule("TEST-PROBE-001"))
    with pytest.raises(ValueError, match="iki kez"):
        register_rule(_rule("TEST-PROBE-001"))


@pytest.mark.parametrize("bad", ["c-buf-001", "C-BUF-1", "CBUF001", "C-BUF-001-X", ""])
def test_bad_id_format_rejected(bad: str) -> None:
    with pytest.raises(ValueError, match="Geçersiz"):
        register_rule(_rule(bad))


def test_unity_rule_not_applied_to_plain_csharp() -> None:
    plain = _ids(Language.CSHARP, Engine.NONE)
    assert not any(i.startswith("UNITY-") for i in plain)
    assert {"CS-ALLOC-001", "CS-PERF-001", "CS-ALLOC-002"} <= plain
    assert "UNITY-PERF-002" not in plain


def test_csharp_rule_applies_to_unity() -> None:
    unity = _ids(Language.CSHARP, Engine.UNITY)
    assert {"CS-ALLOC-001", "CS-ALLOC-002", "UNITY-GC-001", "UNITY-PERF-002"} <= unity


def test_unreal_rule_not_applied_to_plain_cpp() -> None:
    assert not any(i.startswith("UE-") for i in _ids(Language.CPP, Engine.NONE))
    assert {"UE-GC-001", "UE-MEM-001", "CPP-OWN-001", "CPP-SP-001"} <= _ids(
        Language.CPP, Engine.UNREAL
    )


def test_c_rules_only_for_c() -> None:
    assert not any(i.startswith("C-") for i in _ids(Language.CPP, Engine.NONE))
    assert _ids(Language.C, Engine.NONE) == {
        "C-BUF-001",
        "C-IO-001",
        "C-UB-001",
        "C-MEM-001",
        "C-MEM-002",
        "C-MEM-003",
        "C-PERF-001",
    }


def test_disabled_rule_skipped() -> None:
    assert "UNITY-GC-001" not in _ids(Language.CSHARP, Engine.UNITY, ("UNITY-GC-001",))
    findings = run(UNITY_FIXTURE, Engine.UNITY, disabled=["UNITY-GC-001"]).findings
    assert not any(f.rule_id == "UNITY-GC-001" for f in findings)


@pytest.fixture
def fresh_settings() -> Iterator[None]:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.mark.usefixtures("fresh_settings")
def test_disabled_from_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config = tmp_path / "codementor.toml"
    config.write_text('[rules]\ndisabled = ["UNITY-GC-001"]\n', encoding="utf-8")
    monkeypatch.setenv(CONFIG_FILE_ENV, str(config))
    findings = run(UNITY_FIXTURE, Engine.UNITY).findings
    assert not any(f.rule_id == "UNITY-GC-001" for f in findings)
    get_settings.cache_clear()
    monkeypatch.setenv(CONFIG_FILE_ENV, str(tmp_path / "yok.toml"))
    assert any(f.rule_id == "UNITY-GC-001" for f in run(UNITY_FIXTURE, Engine.UNITY).findings)


def test_rule_base_check_is_abstract() -> None:
    with pytest.raises(NotImplementedError):
        Rule.check(_rule("TEST-PROBE-002")(), RuleContext.__new__(RuleContext))
