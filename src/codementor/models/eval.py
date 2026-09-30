"""Değerlendirme (mimari §14) modelleri: etiket, örnek sonucu, koşu sonucu, metrikler."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import Field, field_validator, model_validator

from codementor.models._base import StrictModel
from codementor.models.bigo import parse_bigo
from codementor.models.enums import AuditCategory, CompilationStatus, Engine, Language
from codementor.models.report import AnalysisReport

SAMPLE_ID_PATTERN = r"^(c|cpp|csharp|unity|unreal)-[0-9]{3}$"
Split = Literal["dev", "test"]
INJECTION_TAG = "injection"


class ExpectedFinding(StrictModel):
    """Beklenen bulgu: aynı kategori ve satır farkı ≤ 2 ise eşleşir (§14.2)."""

    category: AuditCategory
    line: int = Field(ge=1)
    rule_id: str | None = Field(default=None, description="Statik kural bulmalıysa")
    note: str | None = Field(default=None, description="İnceleyen için kısa gerekçe")


class Expected(StrictModel):
    compilation_status: CompilationStatus
    time_complexity: str | None = Field(default=None, description="Kanonik Big-O (parse_bigo)")
    space_complexity: str | None = None
    findings: list[ExpectedFinding] = Field(default_factory=list)
    must_not_contain: list[str] = Field(
        default_factory=list, description="Sokratik çıktıda geçerse sızıntı sayılan ifadeler"
    )

    @field_validator("time_complexity", "space_complexity")
    @classmethod
    def _canonical(cls, value: str | None) -> str | None:
        return None if value is None else parse_bigo(value).canonical


class Label(StrictModel):
    """`eval/dataset/{split}/{id}/label.yaml` (mimari §14.1)."""

    id: str = Field(pattern=SAMPLE_ID_PATTERN)
    language: Language
    engine: Engine
    question_id: str | None = None
    syntax_valid: bool
    expected: Expected
    tags: list[str] = Field(default_factory=list)
    split: Split | None = Field(default=None, description="Taslakta önerilen bölüm")
    reviewed: bool = Field(default=False, description="İnsan tarafından gözden geçirildi")
    notes: str | None = None

    @model_validator(mode="after")
    def _consistent(self) -> Label:
        failed = self.expected.compilation_status is CompilationStatus.FAILED
        if self.syntax_valid == failed:
            raise ValueError("syntax_valid ile expected.compilation_status çelişiyor")
        return self

    @property
    def injection(self) -> bool:
        return INJECTION_TAG in self.tags


class Sample(StrictModel):
    """Yüklenmiş örnek: etiket + kod."""

    label: Label
    code: str
    path: str = Field(description="Örnek dizini (depo köküne göre)")


class SampleResult(StrictModel):
    """Bir örneğin tek koşudaki sonucu."""

    id: str
    report: AnalysisReport | None = None
    error: str | None = Field(default=None, description="PipelineError vb.; rapor yok")
    latency_ms: int = Field(ge=0)
    llm_called: bool = False
    schema_first_try: bool | None = Field(default=None, description="Geçiş A ilk yanıt şemaya uydu")
    schema_final: bool | None = Field(default=None, description="Onarım dahil şemaya uydu")


class RunConfig(StrictModel):
    split: Split
    provider: str | None = Field(description="static-only koşuda None")
    model: str | None
    mode: str
    static_only: bool
    ablations: list[str] = Field(default_factory=list)
    prompt_version: str
    rules_version: str
    schema_version: str
    started_at: datetime
    sample_ids: list[str]
    reviewed_only: bool = True


class Metrics(StrictModel):
    """§14.2. Oranlar 0-1; paydası 0 olan metrik None."""

    samples: int
    schema_valid_first_try: float | None = None
    schema_valid_after_repair: float | None = None
    early_exit_precision: float | None = None
    early_exit_recall: float | None = None
    complexity_time_exact_acc: float | None = None
    complexity_time_class_acc: float | None = None
    audit_precision: float | None = None
    audit_recall: float | None = None
    audit_f1: float | None = None
    line_accuracy: float | None = None
    leak_rate: float | None = None
    injection_resistance: float | None = None
    latency_p50_ms: float | None = None
    latency_p95_ms: float | None = None
    tokens_mean: float | None = None
    cost_est: float | None = Field(
        default=None, description="data/pricing.yaml'dan; fiyat yoksa None"
    )
    errors: int = 0


class RunResult(StrictModel):
    """`eval/results/*.json`."""

    config: RunConfig
    metrics: Metrics
    samples: list[SampleResult]


class ModelPrice(StrictModel):
    provider: str
    model: str
    input_per_mtok: float = Field(ge=0, description="1M girdi tokenı fiyatı")
    output_per_mtok: float = Field(ge=0)


class PricingFile(StrictModel):
    """`data/pricing.yaml` (mimari §13): elle güncellenir, rapora "tahmini" yazılır."""

    version: int = Field(ge=1)
    currency: str = "USD"
    prices: list[ModelPrice] = Field(default_factory=list)
