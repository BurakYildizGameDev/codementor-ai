"""K5 doğrulayıcı (mimari §5.6) sonuç modelleri.

Doğrulayıcılar saf fonksiyondur: onarımı yapmaz, onarım kararını bu modellerle döndürür
(onarımı Faz 10 pipeline'ı yapar).
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import AuditCategory
from codementor.models.findings import Finding
from codementor.models.report import ComplexityResult, SocraticResult

RepairReason = Literal["schema", "complexity_unparsable", "unjustified_conflict"]
AgreementState = Literal["agrees", "justified_conflict", "unjustified_conflict", "no_hint"]
LeakKind = Literal[
    "code_block", "code_line", "ngram_overlap", "forbidden_identifier", "too_long", "concept_named"
]
LeakAction = Literal["passed", "regenerate", "dropped_questions"]
LeakField = Literal["guiding_questions", "next_step_hint", "key_flaw_concept"]


class RepairRequest(StrictModel):
    """Modelden bir kez daha istenecek düzeltme; `errors` onarım prompt'una girer."""

    reasons: list[RepairReason] = Field(min_length=1)
    errors: list[str] = Field(min_length=1)


class SchemaCheck(StrictModel):
    """Şema kontrolü: `ok` değilse `errors` onarım için hazırdır (`input_value` içermez)."""

    ok: bool
    errors: list[str] = Field(default_factory=list)
    extracted: bool = Field(
        default=False,
        description="JSON düz yazı/``` çiti içinden çıkarıldı (sağlayıcı ayrıştıramadı)",
    )


class EvidenceMatch(StrictModel):
    """Kanıt araması: bulunduysa (düzeltilmiş) satır aralığı."""

    found: bool
    line_start: int | None = None
    line_end: int | None = None
    shifted: bool = Field(default=False, description="Satır numarası düzeltildi")


class ComplexityCheck(StrictModel):
    """Karmaşıklık normalizasyonu ve statik ipucuyla uzlaştırma."""

    time: str | None = Field(description="Kanonik Big-O; ayrıştırılamadıysa None")
    space: str | None
    optimal_target: str | None
    state: AgreementState
    is_optimal: bool | None
    errors: list[str] = Field(default_factory=list, description="Onarım gerekçeleri")

    @property
    def needs_repair(self) -> bool:
        """Ayrıştırılamayan ifade ya da gerekçesiz çatışma var mı."""
        return bool(self.errors)


class LeakViolation(StrictModel):
    field: LeakField
    index: int | None = Field(description="guiding_questions içindeki sıra; ipucunda None")
    kind: LeakKind
    detail: str


class LeakCheck(StrictModel):
    violations: list[LeakViolation] = Field(default_factory=list)
    reference_checked: bool = Field(
        description="Referans çözümle (5-gram, yasaklı tanımlayıcı) karşılaştırıldı mı"
    )

    @property
    def clean(self) -> bool:
        """Hiç ihlal yoksa True."""
        return not self.violations


class LeakDecision(StrictModel):
    """Sızıntıya göre ne yapılacağı (mimari §5.6: 1 kez yeniden üret, sonra sorunlu soruyu at)."""

    action: LeakAction
    guiding_questions: list[str] = Field(default_factory=list)
    next_step_hint: str | None = None
    violations: list[LeakViolation] = Field(default_factory=list)

    @property
    def all_dropped(self) -> bool:
        """Soru kalmadıysa True (Faz 10 şablon sorulara geçer)."""
        return self.action == "dropped_questions" and not self.guiding_questions


# `scaling`: performans/GC bulgusu için büyüme kanıtı, ör. O(n) yerine O(n^2) (Faz 39)
ProofBasis = Literal[
    "input", "requirement", "scaling", "unproven", "no_demonstration", "no_verdict"
]


class FindingCheck(StrictModel):
    """Doğrulama geçişinin bir LLM bulgusu için kararı (Faz 35); öğrenciye gösterilmez."""

    finding_id: str
    line_start: int = Field(ge=1)
    category: AuditCategory
    kept: bool
    basis: ProofBasis
    reason: str = Field(default="", description="Modelin gerekçesi; sızıntı varsa boş")


class AnalysisVerification(StrictModel):
    """Geçiş A çıktısının doğrulanmış hali."""

    findings: list[Finding]
    complexity: ComplexityResult | None
    confidence: float = Field(ge=0, le=1)
    evidence_ratio: float = Field(ge=0, le=1)
    warnings: list[str] = Field(default_factory=list, description="Kullanıcıya dönük notlar")
    repair: RepairRequest | None = None
    finding_checks: list[FindingCheck] = Field(
        default_factory=list, description="Doğrulama geçişi kararları (Faz 35)"
    )


class SocraticVerification(StrictModel):
    """Geçiş B çıktısının doğrulanmış hali; `action == "regenerate"` ise `result` yoktur."""

    decision: LeakDecision
    result: SocraticResult | None
    warnings: list[str] = Field(default_factory=list)


class CommonIdentifiers(StrictModel):
    """`data/leak_common_identifiers.yaml`: sızıntı sayılmayan genel adlar (dil başına)."""

    version: int = Field(ge=1)
    common: list[str] = Field(default_factory=list, description="Tüm diller için")
    c: list[str] = Field(default_factory=list)
    cpp: list[str] = Field(default_factory=list)
    csharp: list[str] = Field(default_factory=list)
    unity: list[str] = Field(default_factory=list)
    unreal: list[str] = Field(default_factory=list)
