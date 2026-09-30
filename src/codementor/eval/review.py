"""Taslak etiket incelemesi: örnekleri statik analizden geçirip etiketle uyuşmayanları listeler.

Etiketi otomatik düzeltmez; yalnızca insan incelemesine yol gösterir (Faz 12 tuzağı: etiketleri
ajana yazdırıp kontrol etmemek). Uyuşmazlık her zaman etiket hatası değildir: statik analiz
LLM'in bulacağı sorunları bulamaz, bu beklenen bir durumdur.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from codementor.config import Settings
from codementor.eval.metrics import match_findings, same_growth_class
from codementor.eval.runner import StaticOnlyProvider, run_sample
from codementor.models.enums import FindingSource, PipelineMode
from codementor.models.eval import Sample
from codementor.providers.base import LLMProvider


@dataclass
class DraftCheck:
    """Bir taslağın statik analizle karşılaştırması."""

    id: str
    problems: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems


async def check_draft(sample: Sample, settings: Settings) -> DraftCheck:
    """Kesin tutarsızlıklar `problems` (etiket büyük olasılıkla yanlış), bilgi `notes`."""
    baseline = StaticOnlyProvider()

    def factory(_name: str) -> LLMProvider:
        return baseline

    result = await run_sample(sample, settings, factory, baseline.name, PipelineMode.TWO_PASS)
    label, check = sample.label, DraftCheck(sample.label.id)
    report = result.report
    if report is None:
        check.problems.append(f"analiz yapılamadı: {result.error}")
        return check

    early = report.meta.early_exit
    if early and label.syntax_valid:
        first = report.compilation.diagnostics[0] if report.compilation.diagnostics else None
        where = f" ({first.line}. satır: {first.message})" if first else ""
        check.problems.append(f"etiket sözdizimi geçerli diyor ama kod derlenmiyor{where}")
    if not early and not label.syntax_valid:
        check.problems.append("etiket sözdizimi hatalı diyor ama Tier 0 hata bulmadı")

    expected_time = label.expected.time_complexity
    hint = report.complexity.static_hint if report.complexity else None
    if expected_time and hint and not same_growth_class(expected_time, hint):
        check.notes.append(f"statik ipucu O({hint}), etiket O({expected_time}) — hangisi doğru?")

    static = [f for f in report.findings if f.source is FindingSource.STATIC]
    matched = match_findings(label.expected.findings, static)
    matched_rules = {p.rule_id for _, p in matched}
    for expected in label.expected.findings:
        if expected.rule_id and expected.rule_id not in matched_rules:
            check.problems.append(
                f"{expected.line}. satırda {expected.rule_id} bekleniyor ama kural bulmadı"
            )
    labeled = {(p.rule_id, p.line_start) for _, p in matched}
    for finding in static:
        if (finding.rule_id, finding.line_start) not in labeled:
            check.notes.append(
                f"kural {finding.rule_id} {finding.line_start}. satırda buldu, etikette yok "
                f"({finding.category.value}) — eklenmeli mi?"
            )

    code = sample.code.lower()
    for marker in label.expected.must_not_contain:
        if marker.lower() in code:
            check.problems.append(
                f"must_not_contain {marker!r} öğrenci kodunda zaten geçiyor "
                "(alıntı yanlışlıkla sızıntı sayılır)"
            )
    return check
