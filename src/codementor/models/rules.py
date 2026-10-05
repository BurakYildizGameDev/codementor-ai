"""Statik kural motoru modelleri (mimari §5.3.3, §8)."""

from __future__ import annotations

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import AuditCategory, Engine, FindingKind, Language, Severity
from codementor.models.findings import Finding

RULE_ID_PATTERN = r"^[A-Z]+-[A-Z]+-\d{3}$"  # {ALAN}-{KATEGORİ}-{NNN} (mimari §8.1)


class RuleInfo(StrictModel):
    """Kural kataloğu satırı (`codementor rules list`, `docs/rules-catalog.md`, `/v1/rules`)."""

    id: str = Field(pattern=RULE_ID_PATTERN)
    title: str
    description: str
    languages: list[Language]
    engines: list[Engine] = Field(description="Boşsa motordan bağımsız")
    category: AuditCategory
    severity: Severity
    # Faz 52: kuralın varsayılan bulgu türü; kurallar bulgu bazında bunu aşabilir
    kind: FindingKind = Field(description="issue: hata; suggestion: hataya yol açmayan öneri")


class RuleRunResult(StrictModel):
    """Kural motoru çıktısı; bir kural çökerse diğerleri sürer, uyarı eklenir."""

    findings: list[Finding] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list, description="Kullanıcıya dönük notlar")
