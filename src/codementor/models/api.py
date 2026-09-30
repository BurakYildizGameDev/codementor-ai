"""REST API (mimari §9) yanıt modelleri: RFC 7807 hata gövdesi ve sağlık durumu."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.provider import ProviderStatus

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


class Readiness(StrictModel):
    """`/health/ready`: birincil sağlayıcı hazır mı + kullanılabilir derleyiciler."""

    ready: bool
    providers: list[ProviderStatus]
    compilers: list[CompilerStatus]
