"""K5 birleştirici: `verify_analysis` ve `verify_socratic` karar akışları."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pytest

from codementor.config import VerifySettings
from codementor.ingest.normalize import normalize
from codementor.models.enums import AuditCategory, Engine, FindingSource, Language, Severity
from codementor.models.facts import ComplexityHint
from codementor.models.findings import Finding
from codementor.models.llm_output import (
    LLMAnalysisOutput,
    LLMComplexity,
    LLMFinding,
    LLMSocraticOutput,
)
from codementor.models.questions import ExpectedComplexity
from codementor.models.request import LanguageHint
from codementor.verify.analysis import verify_analysis, verify_socratic

Agreement = Literal["agrees", "conflicts", "no_hint"]
REPO = Path(__file__).resolve().parents[3]
SETTINGS = VerifySettings(common_identifiers_file=REPO / "data" / "leak_common_identifiers.yaml")
CODE = normalize(
    "int sum(int *a, int n) {\n    int s = 0;\n    for (int i = 0; i <= n; i++) s += a[i];\n"
    "    return s;\n}\n",
    LanguageHint(language=Language.C, engine=Engine.NONE),
)
HINT = ComplexityHint(value="n", confidence="high", basis=["tek döngü"])


def _output(
    *findings: LLMFinding, time: str = "O(n)", agreement: Agreement = "agrees"
) -> LLMAnalysisOutput:
    return LLMAnalysisOutput.model_validate(
        {
            "complexity": LLMComplexity(
                reasoning_steps=["3. satırdaki döngü n + 1 kez döner."],
                time_complexity=time,
                space_complexity="O(1)",
                optimal_time_target="O(n)",
                agreement=agreement,
            ),
            "additional_findings": list(findings),
        }
    )


def _llm(line: int, evidence: str) -> LLMFinding:
    return LLMFinding(
        category=AuditCategory.MEMORY_SAFETY,
        severity=Severity.HIGH,
        line_start=line,
        line_end=None,
        evidence=evidence,
        description="Dizinin sonunu aşıyor.",
    )


def test_full_analysis_result() -> None:
    result = verify_analysis(
        _output(_llm(3, "i <= n")),
        code=CODE,
        static_findings=[],
        hint=HINT,
        expected=ExpectedComplexity(time={"sum": "n"}, space="1"),
        schema_first_try=True,
        settings=SETTINGS,
    )
    assert result.repair is None
    assert result.warnings == []
    assert result.confidence == 1.0
    assert result.complexity is not None
    assert result.complexity.display_time == "O(n)"
    assert result.complexity.is_optimal is True
    assert result.complexity.static_hint == "n"
    assert result.complexity.agreement == "agrees"
    (finding,) = result.findings
    assert (finding.id, finding.source, finding.line_start) == ("F-001", FindingSource.LLM, 3)


def test_dropped_findings_warn_in_turkish_and_lower_confidence() -> None:
    result = verify_analysis(
        _output(_llm(3, "i <= n"), _llm(3, "free(a)"), _llm(40, "i <= n")),
        code=CODE,
        static_findings=[],
        hint=HINT,
        expected=None,
        schema_first_try=False,
        settings=SETTINGS,
    )
    assert len(result.findings) == 1
    assert result.evidence_ratio == 1 / 3
    assert any("kanıt kodda bulunamadı" in w for w in result.warnings)
    assert any("40. satırda" in w and "5 satır" in w for w in result.warnings)
    assert result.confidence == pytest.approx(0.3 * 1 + 0.3 * (1 / 3), abs=1e-4)  # şema 2. deneme
    assert result.complexity is not None
    assert result.complexity.is_optimal is None  # soru yok


def test_unjustified_conflict_withholds_complexity() -> None:
    result = verify_analysis(
        _output(time="O(n^2)"),
        code=CODE,
        static_findings=[],
        hint=HINT,
        expected=None,
        schema_first_try=True,
        settings=SETTINGS,
    )
    assert result.repair is not None
    assert result.repair.reasons == ["unjustified_conflict"]
    assert result.complexity is None


def test_static_and_llm_merge_confirmed() -> None:
    static = Finding(
        id="F-001",
        rule_id="C-BUF-001",
        category=AuditCategory.MEMORY_SAFETY,
        severity=Severity.MEDIUM,
        line_start=3,
        line_end=None,
        evidence="i <= n",
        description="Döngü sınırı?",
        source=FindingSource.STATIC,
        confidence=0.9,
    )
    result = verify_analysis(
        _output(_llm(2, "i <= n")),
        code=CODE,
        static_findings=[static],
        hint=HINT,
        expected=None,
        schema_first_try=True,
        settings=SETTINGS,
    )
    (merged,) = result.findings
    assert merged.source == FindingSource.CONFIRMED
    assert merged.severity == Severity.MEDIUM


SOCRATIC = LLMSocraticOutput(
    key_flaw_concept="Sınır dışı erişim",
    guiding_questions=["n elemanlı dizide son indis kaçtır?", "`while (lo < hi) {` dener misin?"],
    next_step_hint=None,
)


def test_socratic_regenerate_then_drop() -> None:
    first = verify_socratic(
        SOCRATIC,
        code=CODE,
        hint_level=2,
        name_concept=False,
        question=None,
        reference=None,
        regenerated=False,
        settings=SETTINGS,
    )
    assert first.decision.action == "regenerate"
    assert first.result is None
    second = verify_socratic(
        SOCRATIC,
        code=CODE,
        hint_level=2,
        name_concept=False,
        question=None,
        reference=None,
        regenerated=True,
        settings=SETTINGS,
    )
    assert second.result is not None
    assert second.result.leak_check == "dropped_questions"
    assert second.result.guiding_questions == ["n elemanlı dizide son indis kaçtır?"]
    assert second.result.hint_level == 2
    assert second.warnings


def test_socratic_clean_after_regeneration_marked() -> None:
    clean = SOCRATIC.model_copy(update={"guiding_questions": ["Son indis kaçtır?"]})
    result = verify_socratic(
        clean,
        code=CODE,
        hint_level=1,
        name_concept=False,
        question=None,
        reference=None,
        regenerated=True,
        settings=SETTINGS,
    )
    assert result.result is not None
    assert result.result.leak_check == "regenerated"


def test_socratic_all_dropped_returns_no_result() -> None:
    leaky = SOCRATIC.model_copy(update={"guiding_questions": ["`int m = lo + hi;` yaz?"]})
    result = verify_socratic(
        leaky,
        code=CODE,
        hint_level=1,
        name_concept=False,
        question=None,
        reference=None,
        regenerated=True,
        settings=SETTINGS,
    )
    assert result.result is None
    assert result.decision.all_dropped
    assert any("tümü" in w for w in result.warnings)


def test_llm_certainty_sets_finding_confidence() -> None:
    """Faz 35: modelin `certainty` beyanı rapordaki bulgu güvenine yansır."""
    sure = _llm(3, "i <= n").model_copy(update={"certainty": "low"})
    result = verify_analysis(
        _output(sure),
        code=CODE,
        static_findings=[],
        hint=HINT,
        expected=None,
        schema_first_try=True,
        settings=SETTINGS,
    )
    assert [f.confidence for f in result.findings] == [pytest.approx(0.5)]


def _verified(finding: LLMFinding) -> list[Finding]:
    return verify_analysis(
        _output(finding),
        code=CODE,
        static_findings=[],
        hint=HINT,
        expected=None,
        schema_first_try=True,
        settings=SETTINGS,
    ).findings


def test_llm_kind_carried_to_finding() -> None:
    """Faz 36: düşük önemli öneri rapora öneri olarak geçer."""
    low = _llm(3, "i <= n").model_copy(update={"severity": Severity.LOW, "kind": "suggestion"})
    assert [f.kind for f in _verified(low)] == ["suggestion"]
    assert [f.kind for f in _verified(_llm(3, "i <= n"))] == ["issue"]


@pytest.mark.parametrize("severity", [Severity.MEDIUM, Severity.HIGH])
def test_suggestion_kept_only_for_low_severity(severity: Severity) -> None:
    """Orta/yüksek önemde bir gözlem öneri olamaz: hata olarak raporlanır."""
    finding = _llm(3, "i <= n").model_copy(update={"severity": severity, "kind": "suggestion"})
    assert [f.kind for f in _verified(finding)] == ["issue"]


# --- Faz C (Y6): kavram adı tek kuralla -----------------------------------------------------


def _clean_socratic(**kw: object) -> LLMSocraticOutput:
    return SOCRATIC.model_copy(update={"guiding_questions": ["Son indis kaçtır?"], **kw})


@pytest.mark.parametrize("name_concept", [False, True])
def test_concept_follows_name_concept(name_concept: bool) -> None:
    result = verify_socratic(
        _clean_socratic(),
        code=CODE,
        hint_level=3 if name_concept else 1,
        name_concept=name_concept,
        question=None,
        reference=None,
        regenerated=False,
        settings=SETTINGS,
    ).result
    assert result is not None
    assert result.concept_revealed is name_concept
    assert result.key_flaw_concept == ("Sınır dışı erişim" if name_concept else "")


def test_leaky_concept_regenerates_then_is_masked() -> None:
    """Kavram adı kodu ele veriyor: önce yeniden üretim, sonra kavram gizlenir, sorular kalır."""
    leaky = _clean_socratic(key_flaw_concept="`while (lo < hi) {` yaz")
    first = verify_socratic(
        leaky,
        code=CODE,
        hint_level=3,
        name_concept=True,
        question=None,
        reference=None,
        regenerated=False,
        settings=SETTINGS,
    )
    assert first.decision.action == "regenerate"
    assert any(v.field == "key_flaw_concept" for v in first.decision.violations)
    second = verify_socratic(
        leaky,
        code=CODE,
        hint_level=3,
        name_concept=True,
        question=None,
        reference=None,
        regenerated=True,
        settings=SETTINGS,
    )
    assert second.result is not None
    assert second.result.key_flaw_concept == ""
    assert second.result.concept_revealed is False
    assert second.result.guiding_questions == ["Son indis kaçtır?"]
    assert any("Kavram adı" in w for w in second.warnings)
    assert not any("Bazı mentor soruları" in w for w in second.warnings)


def test_hidden_concept_is_not_leak_checked() -> None:
    """Gösterilmeyecek kavram denetlenmez de: sızıntılı olsa bile yeniden üretim gerekmez."""
    leaky = _clean_socratic(key_flaw_concept="`while (lo < hi) {` yaz")
    checked = verify_socratic(
        leaky,
        code=CODE,
        hint_level=1,
        name_concept=False,
        question=None,
        reference=None,
        regenerated=False,
        settings=SETTINGS,
    )
    assert checked.decision.action == "passed"
    assert checked.result is not None
    assert checked.result.key_flaw_concept == ""
