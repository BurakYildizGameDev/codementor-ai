"""REST API (mimari §9) yanıt modelleri: RFC 7807 hata gövdesi ve sağlık durumu."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import Engine, Language
from codementor.models.provider import ProviderStatus
from codementor.models.validation import ToolOrigin

PROBLEM_JSON = "application/problem+json"


class Problem(StrictModel):
    """RFC 7807 `application/problem+json` gövdesi."""

    type: str = Field(default="about:blank", description="Sorun türü URI'si")
    title: str
    status: int = Field(ge=400, le=599)
    detail: str | None = None
    instance: str | None = Field(default=None, description="İsteğin yolu")
    errors: list[str] | None = Field(default=None, description="Doğrulama hataları (422)")


class Health(StrictModel):
    status: Literal["ok"] = "ok"
    version: str


class CompilerStatus(StrictModel):
    target: str = Field(description="c, cpp, unreal veya csharp")
    tool: str | None = Field(description="Bulunan derleyici; yoksa None (Tier 1 SKIPPED)")
    origin: ToolOrigin | None = Field(
        default=None, description="system (PATH), downloaded (indirilen) ya da bundled (gömülü)"
    )


class Readiness(StrictModel):
    """`/health/ready`: birincil sağlayıcı hazır mı + kullanılabilir derleyiciler."""

    ready: bool
    providers: list[ProviderStatus]
    compilers: list[CompilerStatus]


class AnalysisSummary(StrictModel):
    """Geçmiş listesindeki bir satır; rapor gövdesi ve kod içermez."""

    analysis_id: str
    created_at: datetime
    language: Language
    engine: Engine
    question_id: str | None
    provider: str | None
    degraded: bool
    early_exit: bool
    tokens_in: int
    tokens_out: int


class AnalysisPage(StrictModel):
    items: list[AnalysisSummary]
    next_cursor: str | None = Field(
        default=None,
        description="Sonraki sayfa için `before` değeri; yoksa null",
    )


class DeletedCount(StrictModel):
    """Silinen kayıt sayısı yanıtı (Faz E)."""

    deleted: int
