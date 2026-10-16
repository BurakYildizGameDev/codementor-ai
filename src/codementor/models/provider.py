"""LLM sağlayıcı arayüzünün veri modelleri (mimari §5.5.1)."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from codementor.models._base import StrictModel

Role = Literal["system", "user", "assistant"]


class ChatMessage(StrictModel):
    role: Role
    content: str


class GenerationOptions(StrictModel):
    """Tek çağrının üretim ayarları; None olan alan sağlayıcı yapılandırmasından gelir."""

    temperature: float | None = Field(default=None, ge=0, le=2)
    seed: int | None = None
    max_tokens: int | None = Field(default=None, ge=1)


class TokenUsage(StrictModel):
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    estimated: bool = Field(default=False, description="Sağlayıcı bildirmediyse yaklaşık sayım")


class ProviderCapabilities(StrictModel):
    """Sağlayıcının yapılandırılmış çıktı yetenekleri (mimari §5.5.2)."""

    native_schema: bool = Field(description="Şema API'de zorlanıyor mu (değilse prompt'ta)")
    strict_schema: bool = Field(description="Katı mod: tüm alanlar zorunlu, ek alan yok")
    seed: bool = False
    local: bool = False


class ProviderResult(StrictModel):
    """Sağlayıcı yanıtı. `parsed` yalnızca JSON nesnesi olarak çözülebildiyse dolu; şema
    doğrulaması K5'in (Faz 9) işidir, ham metin onarım için korunur."""

    raw_text: str
    parsed: dict[str, Any] | None
    usage: TokenUsage
    latency_ms: int = Field(ge=0)
    model: str
    finish_reason: str | None
    provider: str
    schema_enforced: bool = Field(
        default=False,
        description=(
            "JSON şemasını sağlayıcı mı zorladı (Faz G7): anthropic, openai_compat ve ollama True; "
            "CLI alt süreçleri (claude_cli, agy, codex) False. Rapora yazılmaz, tanı içindir."
        ),
    )
    warnings: list[str] = Field(
        default_factory=list, description="Rapora `meta.warnings` olarak yazılır (ör. fallback)"
    )


class ProviderStatus(StrictModel):
    """`codementor providers check` satırı."""

    name: str
    model: str
    ready: bool
    detail: str
