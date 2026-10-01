"""Kullanıcıya dönen rapor modeli (mimari §6.4). Tek doğruluk kaynağı."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.findings import CompilationBlock, Finding

# Faz 27: kimlik dosya adına ve URL yoluna girer; yalnızca ULID alfabesi (I, L, O, U yok)
ULID_PATTERN = r"^[0-9A-HJKMNP-TV-Z]{26}$"


class ComplexityResult(StrictModel):
    time_complexity: str = Field(description='Kanonik Big-O, ör. "n^2"')
    space_complexity: str
    display_time: str = Field(description='Gösterim, ör. "O(n²)"')
    reasoning_steps: list[str]
    is_optimal: bool | None = Field(description="Soru bağlamı yoksa null")
    optimal_time_target: str | None
    static_hint: str | None
    agreement: Literal["agrees", "conflicts", "no_hint"]
    confidence: float


class SocraticResult(StrictModel):
    key_flaw_concept: str
    hint_level: int = Field(ge=1, le=3)
    guiding_questions: list[str]
    next_step_hint: str | None
    leak_check: Literal["passed", "regenerated", "dropped_questions", "skipped"]


class ReportMeta(StrictModel):
    provider: str | None
    model: str | None
    prompt_version: str
    rules_version: str
    schema_version: str
    tokens_in: int
    tokens_out: int
    stage_latency_ms: dict[str, int]
    early_exit: bool
    cache_hit: bool
    degraded: bool
    repair_attempts: int
    warnings: list[str]
    # Faz 25 (mimari §13); varsayılanlı: önbellekteki eski raporlar okunmaya devam eder
    usage_estimated: bool = Field(
        default=False, description="Sağlayıcı token bildirmedi; sayılar yaklaşık"
    )
    cost_est: float | None = Field(
        default=None, ge=0, description="Tahmini maliyet (USD, data/pricing.yaml); fiyat yoksa null"
    )


class AnalysisReport(StrictModel):
    """Bir analizin tam sonucu."""

    schema_version: Literal["1.0"] = "1.0"
    analysis_id: str = Field(
        pattern=ULID_PATTERN, description="ULID (Crockford base32, 26 karakter)"
    )
    created_at: datetime
    language: Language
    engine: Engine
    question_id: str | None
    difficulty: Difficulty | None
    compilation: CompilationBlock
    complexity: ComplexityResult | None
    findings: list[Finding]
    socratic: SocraticResult | None
    meta: ReportMeta
