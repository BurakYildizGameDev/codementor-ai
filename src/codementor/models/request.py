"""Analiz isteği ve K0 (giriş/normalizasyon) modelleri (mimari §5.1, §9)."""

from __future__ import annotations

from typing import Annotated, Self

from pydantic import Field, model_validator

from codementor.models._base import StrictModel
from codementor.models.enums import Engine, Language, PipelineMode, check_engine_language

# İstemciden gelen kimlik: kısa, yol/boşluk karakteri yok (Faz 47, ADR-0023)
Identifier = Annotated[str, Field(max_length=128, pattern=r"^[A-Za-z0-9_.-]+$")]


class AnalysisOptions(StrictModel):
    """İstek başına seçenekler; `None` → yapılandırmadaki değer kullanılır."""

    mode: PipelineMode | None = None
    tier1: bool | None = None
    use_cache: bool | None = None
    advance_hint: bool | None = Field(
        default=None,
        description="False: bu gönderim ipucu merdivenini ilerletmez (aynı kodu yeniden "
        "denetlemek, model değiştirmek); None/True: ilerletir",
    )


class AnalysisRequest(StrictModel):
    """Analiz isteği. Kullanıcı kodu güvenilmeyen veridir (mimari §12)."""

    code: str = Field(min_length=1)
    language: Language | None = Field(default=None, description="Boşsa sezgisel tespit")
    engine: Engine | None = Field(default=None, description="Boşsa sezgisel tespit")
    question_id: Identifier | None = None
    session_id: Identifier | None = None
    provider: Identifier | None = Field(
        default=None, description="Boşsa varsayılan; API'de yalnız `api.allowed_providers`"
    )
    options: AnalysisOptions = Field(default_factory=AnalysisOptions)


class LanguageHint(StrictModel):
    """Kullanıcının belirttiği dil/motor; boş alanlar sezgisel tespitle doldurulur."""

    language: Language | None = None
    engine: Engine | None = None

    @model_validator(mode="after")
    def _consistent(self) -> Self:
        if self.language is not None:
            check_engine_language(self.language, self.engine)
        return self


class Detection(StrictModel):
    """Dil/motor tespit sonucu."""

    language: Language
    engine: Engine
    confidence: float = Field(ge=0, le=1)
    reasons: list[str] = Field(description="Kararı destekleyen sinyaller")


class NormalizedCode(StrictModel):
    """K0 çıktısı: LF satır sonlu, UTF-8, numaralı görünümlü kod (mimari §5.1)."""

    text: str
    lines: list[str]
    numbered_view: str = Field(description="LLM'e giden `  14 | foo();` biçimi")
    language: Language
    engine: Engine
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
