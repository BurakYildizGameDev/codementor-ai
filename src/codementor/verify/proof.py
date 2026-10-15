"""Bulgu doğrulama geçişinin kararlarını uygular (Faz 35, ADR-0019).

Saf fonksiyonlar; LLM çağırmaz. Model her LLM bulgusu için ya somut bir girdi (girdi,
beklenen, gerçekleşen) ya da ihlal edilen bir gereksinim göstermek zorundadır; gösteremediği
bulgu düşer. Statik ve `confirmed` bulgular deterministik olduğu için doğrulamaya girmez.

Faz 39 (ADR-0019 eki): performans/GC sorununda çıktı doğrudur, yanlış olan büyüme hızıdır. Bu
yüzden `expected`/`actual` Big-O ile başlıyorsa (`O(n)` → `O(n^2)`) ölçek kanıtı sayılır;
yalnız bu iki kategoride ve gerçekleşen büyüme beklenenden hızlıysa geçerlidir.
"""

from __future__ import annotations

import re
from collections.abc import Collection
from dataclasses import dataclass, field

from codementor.models.bigo import BigOError, collapse_variables, parse_bigo
from codementor.models.enums import AuditCategory, FindingKind, FindingSource
from codementor.models.findings import Finding
from codementor.models.llm_output import LLMFindingVerdict, LLMVerifyOutput
from codementor.models.verification import FindingCheck, ProofBasis
from codementor.verify.merge import number_findings, renumbered_ids

SCALING_CATEGORIES = frozenset({AuditCategory.PERFORMANCE, AuditCategory.GARBAGE_COLLECTION})


@dataclass(frozen=True)
class ProofResult:
    """Kararlar uygulandıktan sonraki bulgular; `dropped` atılan LLM bulgusu sayısı."""

    findings: list[Finding]
    checks: list[FindingCheck]
    dropped: int
    warnings: list[str] = field(default_factory=list)


def verify_targets(findings: list[Finding]) -> list[Finding]:
    """Doğrulamaya girecek bulgular: yalnız LLM kaynaklı hatalar, rapordaki sırayla (1'den).

    Öneriler (Faz 36) somut hatalı bir girdiyle kanıtlanamaz; doğrulamaya girmez, korunur.
    """
    return [f for f in findings if f.source is FindingSource.LLM and f.kind == FindingKind.ISSUE]


def _filled(*values: str | None) -> bool:
    return all(v is not None and v.strip() for v in values)


_BIGO_HEAD = re.compile(r"^\s*[oOΘθ]\s*\(")


def _leading_bigo(text: str | None) -> str | None:
    """Metnin başındaki `O(...)` grubu (`Θ`, küçük harf, `O (` da); sonrasındaki açıklama
    yok sayılır: `O(n^2) (iç içe döngü)` → `O(n^2)`. Big-O ile başlamıyorsa None."""
    if text is None or (head := _BIGO_HEAD.match(text)) is None:
        return None
    depth, start = 0, head.end() - 1
    for i in range(start, len(text)):
        depth += {"(": 1, ")": -1}.get(text[i], 0)
        if depth == 0:
            return "O" + text[start : i + 1]
    return text  # kapanmayan ayraç: ayrışmaz, kanıt sayılmaz


def _grows(expected: str | None, actual: str | None) -> bool:
    """Gerçekleşen büyüme beklenenden hızlı mı? İki taraf da Big-O olmalı; ayrışmayan ifade
    kanıt değildir."""
    if expected is None or actual is None:
        return False
    try:
        return collapse_variables(parse_bigo(actual)) > collapse_variables(parse_bigo(expected))
    except BigOError:
        return False


def _basis(verdict: LLMFindingVerdict | None, finding: Finding) -> ProofBasis:
    if verdict is None:
        return "no_verdict"
    if verdict.verdict == "unproven":
        return "unproven"
    if _filled(verdict.input, verdict.expected, verdict.actual):
        expected, actual = _leading_bigo(verdict.expected), _leading_bigo(verdict.actual)
        if expected is None and actual is None:
            return "input"
        if finding.category in SCALING_CATEGORIES and _grows(expected, actual):
            return "scaling"
        return "no_demonstration"
    if _filled(verdict.requirement):
        return "requirement"
    return "no_demonstration"


def apply_verdicts(findings: list[Finding], output: LLMVerifyOutput) -> ProofResult:
    """Kararları uygular. Karar verilmeyen bulgu korunur (bilgi kaybı yok) ve uyarı yazılır;
    bilinmeyen numaralar yok sayılır, aynı bulguya ikinci karar dikkate alınmaz."""
    targets = verify_targets(findings)
    verdicts: dict[int, LLMFindingVerdict] = {}
    for item in output.verdicts:
        verdicts.setdefault(item.finding, item)
    checks: list[FindingCheck] = []
    warnings: list[str] = []
    dropped_ids: set[str] = set()
    for index, finding in enumerate(targets, start=1):
        verdict = verdicts.get(index)
        basis = _basis(verdict, finding)
        kept = basis in ("input", "requirement", "scaling", "no_verdict")
        checks.append(
            FindingCheck(
                finding_id=finding.id,
                line_start=finding.line_start,
                category=finding.category,
                kept=kept,
                basis=basis,
                reason=verdict.reason if verdict is not None else "",
            )
        )
        if basis == "no_verdict":
            warnings.append(
                f"Model {finding.line_start}. satırdaki bulgu için doğrulama kararı vermedi; "
                "bulgu korundu."
            )
        elif not kept:
            dropped_ids.add(finding.id)
            warnings.append(
                f"Model {finding.line_start}. satırdaki bulguyu somut bir örnekle "
                "kanıtlayamadı; bulgu atıldı."
            )
    remaining = [f for f in findings if f.id not in dropped_ids]
    if dropped_ids:
        # D5: bulgular yeniden numaralandığı için KORUNAN bulguların karar kaydı da yeni kimliği
        # göstermeli; atılan bulgunun kaydı eski kimliğiyle kalır (artık raporda olmayan bulgu).
        new_ids = renumbered_ids(remaining)
        checks = [
            c.model_copy(update={"finding_id": new_ids.get(c.finding_id, c.finding_id)})
            if c.kept
            else c
            for c in checks
        ]
    return ProofResult(
        findings=number_findings(remaining) if dropped_ids else findings,
        checks=checks,
        dropped=len(dropped_ids),
        warnings=warnings,
    )


def redact_reasons(checks: list[FindingCheck], leaky: Collection[int]) -> list[FindingCheck]:
    """Sızıntı korumasına takılan gerekçeleri boşaltır (§12); kararlar değişmez."""
    return [c.model_copy(update={"reason": ""}) if i in leaky else c for i, c in enumerate(checks)]
