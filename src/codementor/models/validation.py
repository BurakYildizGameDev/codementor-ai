"""K1 kademeli ön doğrulama sonuç modelleri (mimari §5.2)."""

from __future__ import annotations

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import CompilationStatus
from codementor.models.findings import CompilationBlock, Diagnostic


class Tier0Result(StrictModel):
    """tree-sitter sözdizimi denetimi sonucu."""

    diagnostics: list[Diagnostic]
    truncated: bool = Field(default=False, description="Tanı sayısı üst sınıra takıldı")

    @property
    def has_errors(self) -> bool:
        return any(d.severity == "error" for d in self.diagnostics)


class PolicyDecision(StrictModel):
    """Erken çıkış politikasının kararı (mimari §5.2.4)."""

    status: CompilationStatus
    early_exit: bool
    diagnostics: list[Diagnostic]

    def to_block(self) -> CompilationBlock:
        """Rapordaki `compilation` bloğu."""
        return CompilationBlock(status=self.status, diagnostics=self.diagnostics)
