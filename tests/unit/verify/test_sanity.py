"""Bulgu sağduyu denetimi testleri (Faz I / İş 11, ADR-0031)."""

from __future__ import annotations

import pytest

from codementor.models.enums import AuditCategory, FindingKind, FindingSource, Severity
from codementor.models.findings import Finding
from codementor.verify.sanity import apply_sanity_checks, is_guard_hallucination


def _make_finding(
    fid: str,
    evidence: str,
    description: str,
    source: FindingSource = FindingSource.LLM,
    severity: Severity = Severity.MEDIUM,
    line_start: int = 10,
    rule_id: str | None = None,
) -> Finding:
    return Finding(
        id=fid,
        rule_id=rule_id,
        category=AuditCategory.EDGE_CASE,
        severity=severity,
        line_start=line_start,
        line_end=None,
        evidence=evidence,
        description=description,
        source=source,
        confidence=0.9,
        kind=FindingKind.ISSUE,
    )


def test_is_guard_hallucination_detects_contradiction() -> None:
    # Kanıt satırı açık bir if/null denetimi yaparken açıklama "kontrol edilmiyor" diyor
    assert is_guard_hallucination(
        description="Fonksiyona gelen işaretçi null için kontrol edilmiyor.",
        evidence="if (ptr == NULL) return;",
    )
    assert is_guard_hallucination(
        description="n parametresinin sıfır veya negatif olması denetlenmemiş.",
        evidence="if (n <= 0) { return 0; }",
    )
    assert is_guard_hallucination(
        description="The buffer is unhandled and not checked for null.",
        evidence="if (!buf) return NULL;",
    )


def test_is_guard_hallucination_false_for_valid_issues() -> None:
    # Normal bir mantık hatası veya döngü sınırı ihlali
    assert not is_guard_hallucination(
        description="Döngü son indeksi aşarak bellek dışına yazıyor.",
        evidence="for (int i = 0; i <= n; i++)",
    )
    # Kontrolsüz erişim (kanıt satırında if yok)
    assert not is_guard_hallucination(
        description="Dizi boyutu kontrol edilmiyor, doğrudan elemana erişiliyor.",
        evidence="return array[index];",
    )


_MISSING = "Dizi sınırı kontrol edilmiyor."


@pytest.mark.parametrize(
    "evidence",
    [
        # Boşluksuz yazılmış karşılaştırmalar denetim değildir (eski kalıp bunları düşürüyordu)
        "for(int i=0;i<=n;i++) a[i]=0;",
        "cout<<a[n];",
        "while(i<n) sum += a[i+1];",
        "std::vector<int> v(n);",
        "return p->next == nullptr;",
        # `if` içeren tanımlayıcı, dize sabiti ve yorum denetim sayılmaz
        "ifstream f(path);",
        'printf("if empty\\n"); x = a[n];',
        "x = a[n]; // if n is 0",
        "x = a[n]  # if n is 0",
        "x = a[n]; /* assert later */",
    ],
)
def test_is_guard_hallucination_keeps_unguarded_evidence(evidence: str) -> None:
    assert not is_guard_hallucination(description=_MISSING, evidence=evidence)


@pytest.mark.parametrize(
    "evidence",
    [
        "if(ptr==NULL)return;",
        "} else if (n < 0) {",
        "if x is None:",
        "elif n <= 0:",
        "assert(n > 0);",
        "assert idx < len(arr)",
        "Debug.Assert(index < items.Length);",
        "int n = 1'000; if (i < n) a[i] = 0;",  # C++14 basamak ayırıcısı karakter sabiti değil
    ],
)
def test_is_guard_hallucination_detects_real_guards(evidence: str) -> None:
    assert is_guard_hallucination(description=_MISSING, evidence=evidence)


def test_apply_sanity_checks_keeps_compact_overflow_in_standard_profile() -> None:
    overflow = _make_finding(
        "F-LLM-1",
        evidence="for(int i=0;i<=n;i++) a[i]=0;",
        description="Döngü sınırı kontrol edilmiyor; son adımda a[n] yazılıyor.",
    )

    findings, warnings = apply_sanity_checks([overflow], model_profile="standard")

    assert [f.id for f in findings] == ["F-LLM-1"]
    assert not any("çeliştiği için düşürüldü" in w for w in warnings)


def test_apply_sanity_checks_drops_hallucinations_and_keeps_static() -> None:
    static_f = _make_finding(
        "F-STATIC",
        evidence="if (p == NULL) return;",
        description="Statik kural bulgusu.",
        source=FindingSource.STATIC,
    )
    hallucination_f = _make_finding(
        "F-LLM-1",
        evidence="if (p == NULL) return;",
        description="İşaretçi null için kontrol edilmiyor.",
        source=FindingSource.LLM,
    )
    valid_llm_f = _make_finding(
        "F-LLM-2",
        evidence="buf[i] = val;",
        description="Döngü sınır kontrolü yapılmıyor.",
        source=FindingSource.LLM,
    )

    findings, warnings = apply_sanity_checks([static_f, hallucination_f, valid_llm_f])

    assert len(findings) == 2
    assert [f.id for f in findings] == ["F-STATIC", "F-LLM-2"]
    assert any("çeliştiği için düşürüldü" in w for w in warnings)


def test_apply_sanity_checks_small_profile_caps_findings() -> None:
    f1 = _make_finding("F-1", "x = 1;", "Hata 1", severity=Severity.LOW, line_start=1)
    f2 = _make_finding("F-2", "y = 2;", "Hata 2", severity=Severity.HIGH, line_start=2)
    f3 = _make_finding("F-3", "z = 3;", "Hata 3", severity=Severity.MEDIUM, line_start=3)
    f4 = _make_finding("F-4", "w = 4;", "Hata 4", severity=Severity.HIGH, line_start=4)
    f5 = _make_finding("F-5", "t = 5;", "Hata 5", severity=Severity.LOW, line_start=5)

    findings, warnings = apply_sanity_checks([f1, f2, f3, f4, f5], model_profile="small")

    # En fazla 3 LLM bulgusu seçilmeli: F-2 (HIGH), F-4 (HIGH), F-3 (MEDIUM)
    assert len(findings) == 3
    ids = {f.id for f in findings}
    assert ids == {"F-2", "F-4", "F-3"}
    assert any("Küçük model profilinde" in w for w in warnings)
