"""Pipeline (mimari §4) modelleri: aşama olayları ve LLM'siz mentor şablonları."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import AuditCategory

Stage = Literal[
    "cache",
    "ingest",
    "tier0",
    "tier1",
    "facts",
    "rules",
    "prompt_a",
    "llm_a",
    "verify_a",
    "prompt_v",
    "llm_v",
    "verify_v",
    "prompt_b",
    "llm_b",
    "verify_b",
    "report",
]
ALL_STAGES: tuple[Stage, ...] = (
    "cache",
    "ingest",
    "tier0",
    "tier1",
    "facts",
    "rules",
    "prompt_a",
    "llm_a",
    "verify_a",
    "prompt_v",
    "llm_v",
    "verify_v",
    "prompt_b",
    "llm_b",
    "verify_b",
    "report",
)
StageStatus = Literal["started", "completed", "skipped", "failed"]


class StageEvent(StrictModel):
    """Bir aşamanın durumu (CLI ilerleme göstergesi, Web UI SSE)."""

    analysis_id: str
    stage: Stage
    status: StageStatus
    duration_ms: int = Field(default=0, ge=0)
    tokens: int = Field(default=0, ge=0)
    detail: str | None = None


class EarlyExitTemplate(StrictModel):
    """Tanı mesajında `match` geçiyorsa bu soru (`{line}`, `{message}` yer tutucuları)."""

    match: str = Field(min_length=1)
    question: str = Field(min_length=1)


class CategoryTemplate(StrictModel):
    label: str = Field(min_length=1, max_length=80)
    conceptual: str = Field(min_length=1, description="Seviye 1: satır vermeden")
    pointed: str = Field(min_length=1, description="Seviye 2-3: `{line}` ile satıra işaret")


class MentorTemplates(StrictModel):
    """`data/mentor_templates.yaml`: erken çıkış ve bozulmada LLM kullanmayan sorular."""

    version: int = Field(ge=1)
    early_exit: list[EarlyExitTemplate] = Field(min_length=1)
    early_exit_default: str
    early_exit_concept: str = Field(max_length=80)
    early_exit_hint: str
    degraded_concept: str = Field(max_length=80)
    degraded_generic: str
    degraded_hint: str
    categories: dict[AuditCategory, CategoryTemplate]
    finding_fallback: str = Field(description="Sızıntı içeren LLM açıklamasının yerine (`{label}`)")
