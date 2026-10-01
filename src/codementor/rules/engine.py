"""Kural motoru: uygun kuralları çalıştırır, bulguları tekilleştirir ve numaralar."""

from __future__ import annotations

from collections.abc import Iterable

from codementor.analysis.parsers import ParsedSource, parse
from codementor.config import get_settings
from codementor.log import get_logger
from codementor.models.facts import CodeFacts
from codementor.models.findings import Finding
from codementor.models.request import NormalizedCode
from codementor.models.rules import RuleRunResult
from codementor.rules.base import RuleContext
from codementor.rules.registry import all_rules, applicable_rules

log = get_logger("codementor.rules")
RULE_FAILURE_WARNING = "{} kuralı çalıştırılamadı ({}); diğer kurallar etkilenmedi."
UNKNOWN_DISABLED_WARNING = "Yapılandırmada kapatılan kural bulunamadı (yazım hatası?): {}"


def run_rules(
    code: NormalizedCode,
    facts: CodeFacts,
    parsed: ParsedSource | None = None,
    *,
    disabled: Iterable[str] | None = None,
) -> RuleRunResult:
    """Koda uygun statik kuralları çalıştırır; istisna fırlatmaz (çöken kural → uyarı).

    `disabled` verilmezse yapılandırmadaki `rules.disabled` kullanılır.
    """
    if disabled is None:
        disabled = get_settings().rules.disabled
    disabled = list(disabled)
    known = {r.id for r in all_rules()}
    ctx = RuleContext(
        language=code.language,
        engine=code.engine,
        lines=code.lines,
        facts=facts,
        parsed=parsed if parsed is not None else parse(code),
    )
    findings: list[Finding] = []
    warnings = [UNKNOWN_DISABLED_WARNING.format(i) for i in sorted(set(disabled) - known)]
    for rule in applicable_rules(code.language, code.engine, disabled):
        try:
            findings += rule().check(ctx)
        except Exception as exc:  # sözleşme: bir kural analizi düşüremez
            # kullanıcıya kısa Türkçe uyarı; istisna izi geliştirici log'una (Faz 21)
            log.exception("rule_failed", rule=rule.id)
            warnings.append(RULE_FAILURE_WARNING.format(rule.id, type(exc).__name__))
    return RuleRunResult(findings=_number(_dedupe(findings)), warnings=warnings)


def _dedupe(findings: list[Finding]) -> list[Finding]:
    """Aynı kural aynı satırda tek bulgu verir (ilki kalır)."""
    seen: set[tuple[str | None, int]] = set()
    unique: list[Finding] = []
    for f in findings:
        if (f.rule_id, f.line_start) not in seen:
            seen.add((f.rule_id, f.line_start))
            unique.append(f)
    return unique


def _number(findings: list[Finding]) -> list[Finding]:
    ordered = sorted(findings, key=lambda f: (f.line_start, f.rule_id or ""))
    return [f.model_copy(update={"id": f"F-{i:03d}"}) for i, f in enumerate(ordered, start=1)]
