"""§5.6 Bulgu birleştirme ve önem sağlaması."""

from __future__ import annotations

from codementor.models.enums import AuditCategory, FindingSource, Severity
from codementor.models.findings import Finding
from codementor.verify.merge import merge_findings


def _finding(
    line: int,
    source: FindingSource,
    category: AuditCategory = AuditCategory.GARBAGE_COLLECTION,
    severity: Severity = Severity.LOW,
    rule_id: str | None = None,
) -> Finding:
    return Finding(
        id="F-000",
        rule_id=rule_id,
        category=category,
        severity=severity,
        line_start=line,
        line_end=None,
        evidence=f"satir{line}",
        description=f"{source} açıklaması",
        source=source,
        confidence=0.9 if source == FindingSource.STATIC else 0.7,
    )


def static(line: int, category: AuditCategory = AuditCategory.GARBAGE_COLLECTION) -> Finding:
    return _finding(
        line, FindingSource.STATIC, category, severity=Severity.HIGH, rule_id="UNITY-GC-001"
    )


def llm(line: int, category: AuditCategory = AuditCategory.GARBAGE_COLLECTION) -> Finding:
    return _finding(line, FindingSource.LLM, category)


def test_same_issue_becomes_single_confirmed() -> None:
    (merged,) = merge_findings([static(10)], [llm(12)])
    assert merged.source == FindingSource.CONFIRMED
    assert merged.severity == Severity.HIGH  # statik önem öncelikli (LLM low demişti)
    assert merged.rule_id == "UNITY-GC-001"
    assert merged.description == "static açıklaması"
    assert merged.confidence >= 0.95


def test_three_lines_apart_stay_separate() -> None:
    merged = merge_findings([static(10)], [llm(13)])
    assert [f.source for f in merged] == [FindingSource.STATIC, FindingSource.LLM]


def test_different_category_stays_separate() -> None:
    merged = merge_findings([static(10)], [llm(10, category=AuditCategory.EDGE_CASE)])
    assert len(merged) == 2
    assert FindingSource.CONFIRMED not in {f.source for f in merged}


def test_static_absorbs_at_most_one_llm_finding() -> None:
    merged = merge_findings([static(10)], [llm(10), llm(11)])
    # 11 aynı sorunun tekrarı (LLM içi yinelenme) → atılır, tek confirmed bulgu kalır
    assert [f.source for f in merged] == [FindingSource.CONFIRMED]


def test_llm_duplicates_deduped() -> None:
    merged = merge_findings([], [llm(20), llm(21), llm(30)])
    assert [f.line_start for f in merged] == [20, 30]


def test_nearest_static_chosen() -> None:
    merged = merge_findings([static(10), static(14)], [llm(13)])
    by_line = {f.line_start: f.source for f in merged}
    assert by_line == {10: FindingSource.STATIC, 14: FindingSource.CONFIRMED}


def test_numbering_by_line() -> None:
    merged = merge_findings([static(30)], [llm(5), llm(50)])
    assert [(f.id, f.line_start) for f in merged] == [("F-001", 5), ("F-002", 30), ("F-003", 50)]


def test_static_only_and_llm_only_unchanged() -> None:
    assert [f.source for f in merge_findings([static(1)], [])] == [FindingSource.STATIC]
    assert [f.source for f in merge_findings([], [llm(1)])] == [FindingSource.LLM]


def test_merge_with_static_keeps_issue_kind() -> None:
    """Faz 36: statik bir hatayla birleşen LLM önerisi hata olarak kalır."""
    suggestion = llm(11).model_copy(update={"kind": "suggestion"})
    (merged,) = merge_findings([static(10)], [suggestion])
    assert merged.source == FindingSource.CONFIRMED
    assert merged.kind == "issue"


def test_static_suggestion_upgraded_by_llm_issue() -> None:
    """Faz 52: statik öneri, LLM aynı satırda hata diyorsa birleşik bulgu hatadır."""
    suggestion = static(11).model_copy(update={"kind": "suggestion"})
    (merged,) = merge_findings([suggestion], [llm(11)])
    assert merged.source == FindingSource.CONFIRMED
    assert merged.kind == "issue"


def test_static_suggestion_with_llm_suggestion_stays_suggestion() -> None:
    """İkisi de öneriyse birleşik bulgu öneridir (Faz 52)."""
    suggestion = static(11).model_copy(update={"kind": "suggestion"})
    other = llm(11).model_copy(update={"kind": "suggestion"})
    (merged,) = merge_findings([suggestion], [other])
    assert merged.kind == "suggestion"


def test_dedupe_prefers_issue_over_suggestion() -> None:
    """LLM aynı sorunu hem öneri hem hata olarak yazarsa hata kalır."""
    suggestion = llm(10).model_copy(update={"kind": "suggestion", "description": "öneri"})
    issue = llm(11).model_copy(update={"description": "hata"})
    (merged,) = merge_findings([], [suggestion, issue])
    assert merged.kind == "issue"
    assert merged.description == "hata"
