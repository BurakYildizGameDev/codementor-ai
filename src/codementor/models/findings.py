"""Sistemin birleştirdiği bulgu ve tanı modelleri (mimari §6.4)."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import (
    AuditCategory,
    CompilationStatus,
    FindingKind,
    FindingSource,
    Severity,
)


class Diagnostic(StrictModel):
    """Ayrıştırıcı/derleyici tanısı (K1)."""

    tool: Literal["tree-sitter", "gcc", "clang", "roslyn", "python"]
    severity: Literal["error", "warning", "note"]
    line: int
    column: int | None
    message: str


class CompilationBlock(StrictModel):
    """Ön doğrulama sonucu: durum + tanılar."""

    status: CompilationStatus
    diagnostics: list[Diagnostic]


class Finding(StrictModel):
    """Rapordaki tek bulgu; statik kural, LLM ya da ikisinin birleşimi."""

    id: str = Field(description='Rapor içi kimlik, ör. "F-001"')
    rule_id: str | None = Field(description='Statik kural kimliği, ör. "UNITY-GC-001"')
    category: AuditCategory
    severity: Severity
    line_start: int
    line_end: int | None
    evidence: str
    description: str
    source: FindingSource
    confidence: float = Field(ge=0, le=1)
    # Faz 36 (ADR-0022); varsayılanlı: eski raporlar okunur, bulguları hata sayılır
    kind: FindingKind = Field(
        default=FindingKind.ISSUE,
        description="issue: gerçek hata; suggestion: hataya yol açmayan öneri (yalnız low)",
    )


def issues_only(findings: list[Finding]) -> list[Finding]:
    """Gerçek hatalar (Faz 36): Sokratik sorular ve eval puanı önerilere dayanmaz."""
    return [f for f in findings if f.kind == FindingKind.ISSUE]
