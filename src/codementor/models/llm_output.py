"""LLM'in doldurduğu küçük, düz çıktı şemaları (mimari §6.1, §6.3).

Bu modül rapor modellerini içe aktarmaz: sistem alanları (`source`, `confidence`,
`meta` ...) LLM'e hiçbir zaman şema olarak gösterilmez.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import AuditCategory, Severity


class LLMFinding(StrictModel):
    category: AuditCategory
    severity: Severity
    line_start: int = Field(ge=1)
    line_end: int | None = None
    evidence: str = Field(max_length=200, description="Satırdan birebir alıntı")
    description: str = Field(max_length=400)


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


class LLMSocraticOutput(StrictModel):
    """Geçiş B çıktısı: Sokratik yönlendirme soruları."""

    key_flaw_concept: str = Field(max_length=80)
    guiding_questions: list[str] = Field(min_length=1, max_length=4)
    next_step_hint: str | None = Field(default=None, max_length=300)


class LLMSinglePassOutput(StrictModel):
    """`pipeline.mode = "single_pass"` çıktısı: Geçiş A ve B tek çağrıda (mimari §5.4.2)."""

    analysis: LLMAnalysisOutput
    socratic: LLMSocraticOutput
