"""Kural motoru: numaralama, tekilleştirme, yalıtım, kanıt, doğrusal süre.

Bölüm 1/2.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from codementor.analysis.extractor import extract_facts
from codementor.analysis.parsers import parse
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language
from codementor.models.request import LanguageHint
from codementor.models.rules import RuleRunResult
from codementor.rules.base import MAX_EVIDENCE, RuleContext
from codementor.rules.engine import RULE_FAILURE_WARNING, UNKNOWN_DISABLED_WARNING
from tests.rules.engine_support import (
    C_TEXT,
    run_text,
)


@pytest.mark.usefixtures("probes")
def test_crashing_rule_isolated_with_warning(
    captured_logs: Callable[[], list[dict[str, Any]]],
) -> None:
    result = run_text(C_TEXT, Language.C, disabled=[])
    assert result.warnings == [RULE_FAILURE_WARNING.format("TEST-CRASH-001", "RuntimeError")]
    assert any(f.rule_id == "C-BUF-001" for f in result.findings)
    # Faz 31: WARNING'de yalnız kural ve istisna türü (mesaj kullanıcı kodu içerebilir, §12);
    # istisna izi yalnız DEBUG düzeyinde
    logs = captured_logs()
    (failed,) = [e for e in logs if e["event"] == "rule_failed"]
    assert failed["rule"] == "TEST-CRASH-001"
    assert failed["level"] == "warning"
    assert failed["error"] == "RuntimeError"
    assert "bozuk kural" not in str(failed)
    (trace,) = [e for e in logs if e["event"] == "rule_failed_trace"]
    assert trace["level"] == "debug"
    assert "RuntimeError: bozuk kural" in trace["exception"]


@pytest.mark.usefixtures("probes")
def test_same_line_deduplicated() -> None:
    result = run_text(C_TEXT, Language.C, disabled=["TEST-CRASH-001"])
    twice = [f.line_start for f in result.findings if f.rule_id == "TEST-TWICE-001"]
    assert twice == [1, 3]


@pytest.mark.usefixtures("probes")
def test_finding_ids_sequential_sorted_by_line() -> None:
    result = run_text(C_TEXT, Language.C, disabled=["TEST-CRASH-001"])
    assert [f.id for f in result.findings] == [
        f"F-{i:03d}" for i in range(1, len(result.findings) + 1)
    ]
    assert [f.line_start for f in result.findings] == sorted(f.line_start for f in result.findings)
    gets = next(f for f in result.findings if f.rule_id == "C-BUF-001")
    assert gets.line_start == 4
    assert gets.evidence == "gets(a);"
    assert gets.source == "static"
    assert gets.line_end is None


def test_evidence_clipped() -> None:
    long_line = "    gets(a); /*" + "x" * 500 + "*/"
    text = C_TEXT.replace("    gets(a);", long_line)
    finding = next(f for f in run_text(text, Language.C).findings if f.rule_id == "C-BUF-001")
    assert len(finding.evidence) == MAX_EVIDENCE
    assert finding.evidence.endswith("…")


def test_line_text_out_of_range() -> None:
    code = normalize(C_TEXT, LanguageHint(language=Language.C))
    ctx = RuleContext(Language.C, Engine.NONE, code.lines, extract_facts(code), parse(code))
    assert ctx.line_text(0) == ""
    assert ctx.line_text(999) == ""


def test_unknown_disabled_rule_warns() -> None:
    result = run_text(C_TEXT, Language.C, disabled=["C-BUF-01", "C-BUF-001"])
    assert result.warnings == [UNKNOWN_DISABLED_WARNING.format("C-BUF-01")]
    assert not any(f.rule_id == "C-BUF-001" for f in result.findings)


def test_in_loop_uses_loop_bodies() -> None:
    text = (
        "public class P { public void F(int[] a) {\n"
        '  string s = "";\n'
        "  foreach (var x in a) { s += x; }\n"
        '  s += "son";\n'
        "} }\n"
    )
    found = [f.line_start for f in run_text(text, Language.CSHARP).findings]
    assert found == [3]


def test_no_rules_for_clean_code() -> None:
    text = "int add(int a, int b) { return a + b; }\n"
    assert run_text(text, Language.C) == RuleRunResult()
