"""K6: parçalardan `AnalysisReport` (mimari §6.4); `meta` tüm aşamaların süresini içerir."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from codementor.models.enums import Difficulty
from codementor.models.findings import Finding
from codementor.models.pipeline import ALL_STAGES
from codementor.models.report import AnalysisReport, ComplexityResult, ReportMeta, SocraticResult
from codementor.models.request import NormalizedCode
from codementor.models.validation import PolicyDecision
from codementor.pipeline.events import StageTimer
from codementor.pipeline.passes import LLMSession
from codementor.pipeline.versions import SCHEMA_VERSION, rules_version


@dataclass
class ReportParts:
    """Raporun analiz parçaları."""

    policy: PolicyDecision
    complexity: ComplexityResult | None = None
    findings: list[Finding] = field(default_factory=list)
    socratic: SocraticResult | None = None
    early_exit: bool = False
    degraded: bool = False


def stage_latencies(timer: StageTimer) -> dict[str, int]:
    """Tüm aşamalar (çalışmayanlar 0) — `meta.stage_latency_ms`."""
    return {stage: timer.latency_ms.get(stage, 0) for stage in ALL_STAGES}


def assemble_report(
    *,
    analysis_id: str,
    code: NormalizedCode,
    question_id: str | None,
    difficulty: Difficulty | None,
    parts: ReportParts,
    llm: LLMSession | None,
    prompt_version: str,
    warnings: list[str],
    timer: StageTimer,
    rules_version_value: str | None = None,
) -> AnalysisReport:
    """Raporu kurar; `report` aşaması da süreye dahildir."""
    with timer.stage("report"):
        for stage in ALL_STAGES:
            if stage != "report" and stage not in timer.latency_ms:
                timer.skip(stage)
        report = AnalysisReport(
            analysis_id=analysis_id,
            created_at=datetime.now(UTC),
            language=code.language,
            engine=code.engine,
            question_id=question_id,
            difficulty=difficulty,
            compilation=parts.policy.to_block(),
            complexity=parts.complexity,
            findings=parts.findings,
            socratic=parts.socratic,
            meta=ReportMeta(
                provider=llm.provider_name if llm else None,
                model=llm.model if llm else None,
                prompt_version=prompt_version,
                rules_version=rules_version_value or rules_version(),
                schema_version=SCHEMA_VERSION,
                tokens_in=llm.tokens_in if llm else 0,
                tokens_out=llm.tokens_out if llm else 0,
                stage_latency_ms={},
                early_exit=parts.early_exit,
                cache_hit=False,
                degraded=parts.degraded,
                repair_attempts=llm.repair_attempts if llm else 0,
                warnings=list(dict.fromkeys(warnings)),
                usage_estimated=llm.usage_estimated if llm else False,
            ),
        )
    report.meta.stage_latency_ms = stage_latencies(timer)
    return report


def from_cache(cached: AnalysisReport, analysis_id: str, timer: StageTimer) -> AnalysisReport:
    """Önbellekteki rapor: yeni kimlik, `cache_hit`, bu isteğin süreleri; token harcanmadı."""
    for stage in ALL_STAGES:
        if stage not in timer.latency_ms:
            timer.skip(stage, "önbellek")
    meta = cached.meta.model_copy(
        update={
            "cache_hit": True,
            "stage_latency_ms": stage_latencies(timer),
            "tokens_in": 0,
            "tokens_out": 0,
        }
    )
    return cached.model_copy(
        update={"analysis_id": analysis_id, "created_at": datetime.now(UTC), "meta": meta}
    )
