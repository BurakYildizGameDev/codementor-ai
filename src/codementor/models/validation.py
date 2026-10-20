"""K1 kademeli ön doğrulama sonuç modelleri (mimari §5.2)."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import CompilationStatus, Engine, Language
from codementor.models.findings import CompilationBlock, Diagnostic

DiagnosticTool = Literal["gcc", "clang", "roslyn"]
# system: PATH'te bulundu · downloaded: kullanıcı dizinine indirildi · bundled: pakete gömülü
ToolOrigin = Literal["system", "downloaded", "bundled"]


class Tier0Result(StrictModel):
    """tree-sitter sözdizimi denetimi sonucu."""

    diagnostics: list[Diagnostic]
    truncated: bool = Field(default=False, description="Tanı sayısı üst sınıra takıldı")
    # D18: durdurma artık yapısal; tanı metni değişse de çağıran sessizce bozulmaz
    stopped: bool = Field(
        default=False,
        description="Yalıtım durdurma tanısı (süre/bellek/altyapı); analiz erken biter",
    )

    @property
    def has_errors(self) -> bool:
        return any(d.severity == "error" for d in self.diagnostics)


class SkipReason(StrEnum):
    """Tier 1'in çalıştırılmama / sonuç vermeme nedeni (mimari §5.2.3)."""

    DISABLED = "disabled"
    TOOL_MISSING = "tool_missing"
    STUB_MISSING = "stub_missing"
    INCLUDE_GUARD = "include_guard"
    TIMEOUT = "timeout"
    TOOL_ERROR = "tool_error"
    NOT_APPLICABLE = "not_applicable"  # HTML/CSS: derleyici kavramı yok (ADR-0015)


class CompilerTool(StrictModel):
    """Keşfedilmiş bir derleyici/araç: çağrı öneki ve tanı biçimi."""

    name: str = Field(description="gcc, g++, clang, clang++, zig veya roslyn-check")
    kind: DiagnosticTool
    command: list[str] = Field(description="Mutlak yollu çağrı öneki")
    origin: ToolOrigin = "system"


class Toolchain(StrictModel):
    """Dil/motor başına kullanılacak araçlar; `None` = yok (Tier 1 `SKIPPED`)."""

    c: CompilerTool | None = None
    cpp: CompilerTool | None = None
    unreal: CompilerTool | None = None
    csharp: CompilerTool | None = None

    def for_code(self, language: Language, engine: Engine) -> CompilerTool | None:
        """Koda uygun araç."""
        if engine is Engine.UNREAL:
            return self.unreal
        return {Language.C: self.c, Language.CPP: self.cpp, Language.CSHARP: self.csharp}.get(
            language
        )

    def summary(self) -> dict[str, str | None]:
        """`/health/ready` için özet: hedef → araç adı."""
        return {
            "c": self.c.name if self.c else None,
            "cpp": self.cpp.name if self.cpp else None,
            "unreal": self.unreal.name if self.unreal else None,
            "csharp": self.csharp.name if self.csharp else None,
        }


class Tier1Result(StrictModel):
    """Yerel derleyici denetimi sonucu (mimari §5.2.2-5.2.3)."""

    status: CompilationStatus
    tool: str | None = None
    diagnostics: list[Diagnostic] = Field(default_factory=list)
    skip_reason: SkipReason | None = None
    warnings: list[str] = Field(default_factory=list, description="Kullanıcıya dönük notlar")
    truncated: bool = False


class PolicyDecision(StrictModel):
    """Erken çıkış politikasının kararı (mimari §5.2.4)."""

    status: CompilationStatus
    early_exit: bool
    diagnostics: list[Diagnostic]
    warnings: list[str] = Field(default_factory=list, description="Rapor `meta.warnings`'e")

    def to_block(self) -> CompilationBlock:
        """Rapordaki `compilation` bloğu."""
        return CompilationBlock(status=self.status, diagnostics=self.diagnostics)


class DownloadProgress(StrictModel):
    """Derleyici kurulumunun ilerlemesi (Faz 29): masaüstü ve CLI gösterir."""

    stage: Literal["download", "extract", "check"]
    done: int = Field(ge=0, description="İndirilen bayt / açılan dosya sayısı")
    total: int | None = Field(default=None, ge=0, description="Bilinmiyorsa None")


class PruneReport(StrictModel):
    """Zig libc başlık budaması raporu (Faz J, `validation/toolchain_prune.py`)."""

    removed_dirs: list[str]
    removed_files_count: int
    reclaimed_bytes: int
    dry_run: bool
    failed_dirs: list[str] = Field(
        default_factory=list,
        description="Silinemeyen (kilitli/izinsiz) dizinler; kaldırılmış sayılmaz",
    )
