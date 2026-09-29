"""Analiz isteği modelleri (mimari §9 istek örneği)."""

from __future__ import annotations

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import Engine, Language, PipelineMode


class AnalysisOptions(StrictModel):
    """İstek başına seçenekler; `None` → yapılandırmadaki değer kullanılır."""

    mode: PipelineMode | None = None
    tier1: bool | None = None
    use_cache: bool | None = None


class AnalysisRequest(StrictModel):
    """Analiz isteği. Kullanıcı kodu güvenilmeyen veridir (mimari §12)."""

    code: str = Field(min_length=1)
    language: Language | None = Field(default=None, description="Boşsa sezgisel tespit")
    engine: Engine | None = Field(default=None, description="Boşsa sezgisel tespit")
    question_id: str | None = None
    session_id: str | None = None
    provider: str | None = None
    options: AnalysisOptions = Field(default_factory=AnalysisOptions)
