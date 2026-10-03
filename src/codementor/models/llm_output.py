"""LLM'in doldurduğu küçük, düz çıktı şemaları (mimari §6.1, §6.3).

Bu modül rapor modellerini içe aktarmaz: sistem alanları (`source`, `confidence`,
`meta` ...) LLM'e hiçbir zaman şema olarak gösterilmez.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import AuditCategory, Severity

# Soru başına üst sınır (Faz 27): sızıntı denetiminin regex süresi doğrusal kalsın
MAX_QUESTION_CHARS = 1000
# Doğrulama geçişinde gösterim alanı başına üst sınır (Faz 35)
MAX_PROOF_CHARS = 300

# Modelin bulguya kendi güveni (Faz 35). `confidence` sistem alanıdır; LLM şemasında yer almaz.
Certainty = Literal["high", "medium", "low"]


class LLMFinding(StrictModel):
    category: AuditCategory
    severity: Severity
    line_start: int = Field(ge=1)
    line_end: int | None = None
    evidence: str = Field(max_length=200, description="Satırdan birebir alıntı")
    description: str = Field(max_length=400)
    certainty: Certainty | None = None  # anlamı prompt kurallarında (Faz 35)


class LLMComplexity(StrictModel):
    reasoning_steps: list[str] = Field(min_length=1, max_length=8)
    time_complexity: str = Field(description="Ham metin; K5 normalize eder")
    space_complexity: str
    optimal_time_target: str | None
    agreement: Literal["agrees", "conflicts", "no_hint"]


class LLMAnalysisOutput(StrictModel):
    """Geçiş A çıktısı: karmaşıklık + statik analizin kaçırdığı bulgular."""

    complexity: LLMComplexity
    additional_findings: list[LLMFinding] = Field(max_length=10)


class LLMMarkupAnalysisOutput(StrictModel):
    """HTML/CSS Geçiş A çıktısı (ADR-0015): karmaşıklık yok, yalnızca ek bulgular."""

    additional_findings: list[LLMFinding] = Field(max_length=10)


class LLMSocraticOutput(StrictModel):
    """Geçiş B çıktısı: Sokratik yönlendirme soruları."""

    key_flaw_concept: str = Field(max_length=80)
    guiding_questions: list[Annotated[str, Field(max_length=MAX_QUESTION_CHARS)]] = Field(
        min_length=1, max_length=4
    )
    next_step_hint: str | None = Field(default=None, max_length=300)


class LLMSinglePassOutput(StrictModel):
    """`pipeline.mode = "single_pass"` çıktısı: Geçiş A ve B tek çağrıda (mimari §5.4.2)."""

    analysis: LLMAnalysisOutput
    socratic: LLMSocraticOutput


class LLMFindingVerdict(StrictModel):
    """Doğrulama geçişi (Faz 35): tek bir bulgunun kanıtı ya da reddi."""

    finding: int = Field(ge=1, description="Doğrulanan bulgunun listedeki numarası")
    verdict: Literal["proven", "unproven"]
    input: str | None = Field(
        default=None, max_length=MAX_PROOF_CHARS, description="Hatayı ortaya çıkaran somut girdi"
    )
    expected: str | None = Field(
        default=None, max_length=MAX_PROOF_CHARS, description="Bu girdide doğru davranış"
    )
    actual: str | None = Field(
        default=None, max_length=MAX_PROOF_CHARS, description="Kodun bu girdide yaptığı"
    )
    requirement: str | None = Field(
        default=None, max_length=MAX_PROOF_CHARS, description="İhlal edilen soru gereksinimi"
    )
    reason: str = Field(max_length=400)


class LLMVerifyOutput(StrictModel):
    """Doğrulama geçişi çıktısı: her LLM bulgusu için bir karar."""

    verdicts: list[LLMFindingVerdict] = Field(max_length=10)
