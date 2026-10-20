"""LLM sağlayıcı ayar modelleri (mimari §5.5, §17); `config.py` 400 satır sınırı için ayrıldı.

`codementor.config` bu adları yeniden dışa aktarır: `from codementor.config import CodexConfig`
gibi mevcut içe aktarmalar değişmez.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ProviderConfig(BaseModel):
    """Bir LLM sağlayıcısının ayarları (mimari §5.5, §17); anahtarın kendisi değil, adı tutulur."""

    base_url: str | None = None
    model: str = ""
    api_key_env: str | None = None
    num_ctx: int | None = Field(default=None, ge=512)
    context_tokens: int | None = Field(
        default=None, ge=1024, description="Bağlam penceresi; yoksa prompts.default_context_tokens"
    )
    temperature: float | None = Field(default=None, ge=0, le=2)
    seed: int | None = None
    max_tokens: int | None = Field(default=None, ge=1)
    timeout_s: int = Field(default=60, ge=1)  # bulut: 60 sn (mimari §5.5.3)


# Alt sınıflar, TOML'da bölüm kısmen verildiğinde de sağlayıcıya özgü varsayılanları korur.
class OllamaConfig(ProviderConfig):
    base_url: str | None = "http://127.0.0.1:11434"
    num_ctx: int | None = Field(default=16384, ge=512)
    timeout_s: int = Field(default=120, ge=1)  # yerel: 120 sn
    think: bool | None = Field(
        default=None, description="Akıl yürütme modelleri (deepseek-r1) için `think`"
    )
    profile: Literal["small", "standard"] | None = Field(
        default=None, description="Faz I (ADR-0031): model boyutu profili"
    )


class GeminiConfig(ProviderConfig):
    """Google Gemini, OpenAI uyumlu uç noktası üzerinden (ADR-0020)."""

    base_url: str | None = "https://generativelanguage.googleapis.com/v1beta/openai"
    api_key_env: str | None = "GEMINI_API_KEY"


# Anthropic Messages API'de `max_tokens` zorunlu; adaptör de yapılandırma da tek bu değeri
# kullanır (D9: ikinci bir sabit yok). Düşünme de bu bütçeden harcar.
ANTHROPIC_DEFAULT_MAX_TOKENS = 16000


class AnthropicConfig(ProviderConfig):
    base_url: str | None = "https://api.anthropic.com"
    api_key_env: str | None = "ANTHROPIC_API_KEY"
    max_tokens: int | None = Field(default=ANTHROPIC_DEFAULT_MAX_TOKENS, ge=1)
    context_tokens: int | None = Field(default=200000, ge=1024)


class CliConfig(ProviderConfig):
    """CLI ajanı (ADR-0012): çalıştırılabilir dosya adı ya da mutlak yolu."""

    command: str | None = None
    timeout_s: int = Field(default=300, ge=1)
    # G1: CLI'lar her parça/olay için ayrı satır yazıyor; derleyici sınırı (64 KB) ajan yanıtını
    # kesiyordu. stdout ve stderr ayrı ayrı bu sınıra tabidir.
    output_limit_bytes: int = Field(default=1_048_576, ge=65_536, le=16_777_216)


class ClaudeCliConfig(CliConfig):
    """Claude Code CLI (`claude -p`); kimlik CLI oturumundan gelir, API anahtarı gerekmez."""

    command: str | None = "claude"
    context_tokens: int | None = Field(default=200000, ge=1024)
    # Faz 34: CLI bazı modellerde (Haiku 4.5) uzun düşünme açar; verilirse alt sürece
    # MAX_THINKING_TOKENS olarak geçer (0 = kapalı). Verilmezse CLI'ın varsayılanı.
    thinking_tokens: int | None = Field(default=None, ge=0)


class AgyConfig(CliConfig):
    """Antigravity CLI (`agy -p`); araçları kapatılamadığı için açık onay gerekir."""

    command: str | None = "agy"
    allow_tool_agent: bool = False


class CodexConfig(CliConfig):
    """OpenAI Codex CLI (`codex exec`); ChatGPT oturumuyla. Salt okunur sandbox'ta bile dosya
    okuyabilen bir ajan olduğu için açık onay gerekir (ADR-0017)."""

    command: str | None = "codex"
    allow_tool_agent: bool = False


class ProvidersSettings(BaseModel):
    default: str = "ollama"
    fallback: list[str] = Field(default_factory=list)
    max_retries: int = Field(default=2, ge=0, le=5)  # yalnızca ağ/429/5xx (mimari §5.5.3)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    gemini: GeminiConfig = Field(default_factory=GeminiConfig)
    anthropic: AnthropicConfig = Field(default_factory=AnthropicConfig)
    claude_cli: ClaudeCliConfig = Field(default_factory=ClaudeCliConfig)
    agy: AgyConfig = Field(default_factory=AgyConfig)
    codex: CodexConfig = Field(default_factory=CodexConfig)
