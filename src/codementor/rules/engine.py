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
FINDING_CAP_WARNING = (
    "Statik analiz {} bulgu üretti; en önemli {} tanesi gösteriliyor (rules.max_findings)."
)
_SEVERITY_RANK = {"high": 0, "medium": 1, "low": 2}


def run_rules(
    code: NormalizedCode,
    facts: CodeFacts,
    parsed: ParsedSource | None = None,
    *,
    disabled: Iterable[str] | None = None,
    max_findings: int | None = None,
) -> RuleRunResult:
    """Koda uygun statik kuralları çalıştırır; istisna fırlatmaz (çöken kural → uyarı).

    `disabled` / `max_findings` verilmezse yapılandırmadaki `rules` ayarları kullanılır.
    Bulgu sayısı sınırı aşarsa önem sırasıyla kesilir ve uyarı yazılır (Faz 31, §12).
    """
    if disabled is None:
        disabled = get_settings().rules.disabled
    if max_findings is None:
        max_findings = get_settings().rules.max_findings
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
            # İstisna mesajı kullanıcı kodu parçası içerebilir (§12): WARNING'de yalnız tür,
            # tam iz yalnız DEBUG'da (Faz 31)
            log.warning("rule_failed", rule=rule.id, error=type(exc).__name__)
            log.debug("rule_failed_trace", rule=rule.id, exc_info=True)
            warnings.append(RULE_FAILURE_WARNING.format(rule.id, type(exc).__name__))
    unique = _dedupe(findings)
    if len(unique) > max_findings:
        warnings.append(FINDING_CAP_WARNING.format(len(unique), max_findings))
        unique = _most_severe(unique, max_findings)
    return RuleRunResult(findings=_number(unique), warnings=warnings)


def _most_severe(findings: list[Finding], limit: int) -> list[Finding]:
    """Önem (yüksek → düşük), eşitlikte satır sırasıyla ilk `limit` bulgu."""
    ranked = sorted(findings, key=lambda f: (_SEVERITY_RANK.get(f.severity, 3), f.line_start))
    return ranked[:limit]


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
