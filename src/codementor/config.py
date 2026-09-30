"""Uygulama yapılandırması.

Öncelik sırası (mimari §17): CLI bayrağı > ortam değişkeni > codementor.toml > varsayılan.
CLI bayrakları `get_settings(**overrides)` ile init argümanı olarak verilir.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

CONFIG_FILE_ENV = "CODEMENTOR_CONFIG_FILE"
DEFAULT_CONFIG_FILE = "codementor.toml"


class LimitsSettings(BaseModel):
    max_lines: int = Field(default=600, ge=1)
    max_bytes: int = Field(default=40960, ge=1)


class ValidationSettings(BaseModel):
    """Tier 1 yerel derleyici ayarları (mimari §5.2.2-5.2.3, ADR-0009)."""

    tier1_enabled: bool = True
    compile_timeout_s: int = Field(default=10, ge=1)
    compile_memory_mb: int = Field(default=1024, ge=64)
    stub_header: Path = Path("data/stubs/ue_stubs.h")
    roslyn_check_dll: Path = Path("tools/roslyn-check/out/RoslynCheck.dll")


class PipelineSettings(BaseModel):
    mode: Literal["two_pass", "single_pass"] = "two_pass"
    max_repair_attempts: int = Field(default=1, ge=0)
    use_cache: bool = True


class DataSettings(BaseModel):
    """Veri dizinleri; göreli yollar çalışma dizinine göredir."""

    questions_dir: Path = Path("data/questions")
    checklists_dir: Path = Path("data/checklists")
    call_costs_file: Path = Path("data/call_costs.yaml")
    mentor_templates_file: Path = Path("data/mentor_templates.yaml")


class PromptSettings(BaseModel):
    """Prompt şablonları ve token bütçesi (mimari §5.4.4-5.4.5)."""

    dir: Path = Path("prompts/v1")
    default_context_tokens: int = Field(default=32768, ge=1024)
    reserve_output_tokens: int = Field(default=4096, ge=256)
    max_fewshots: int = Field(default=2, ge=0, le=4)
    max_checklist_items: int = Field(default=12, ge=0)


class StorageSettings(BaseModel):
    """SQLite depolama (mimari §11); yol yoksa CODEMENTOR_DB_PATH, o da yoksa ~/.codementor."""

    db_path: Path | None = None


class VerifySettings(BaseModel):
    """K5 doğrulayıcı eşikleri (mimari §5.6); Faz 12 eval'inde ayarlanır."""

    evidence_window: int = Field(default=2, ge=0, le=10)
    leak_ngram_n: int = Field(default=5, ge=2, le=10)
    leak_ngram_threshold: float = Field(default=0.2, gt=0, le=1)
    leak_min_identifier_length: int = Field(default=3, ge=1)
    common_identifiers_file: Path = Path("data/leak_common_identifiers.yaml")


class RulesSettings(BaseModel):
    """Statik kural motoru (mimari §5.3.3); kurallar kimlikle tek tek kapatılabilir."""

    disabled: list[str] = Field(default_factory=list)


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


class OpenAIConfig(ProviderConfig):
    base_url: str | None = "https://api.openai.com/v1"
    api_key_env: str | None = "OPENAI_API_KEY"


class DeepSeekConfig(ProviderConfig):
    base_url: str | None = "https://api.deepseek.com"
    api_key_env: str | None = "DEEPSEEK_API_KEY"


class AnthropicConfig(ProviderConfig):
    base_url: str | None = "https://api.anthropic.com"
    api_key_env: str | None = "ANTHROPIC_API_KEY"
    max_tokens: int | None = Field(default=16000, ge=1)  # düşünme de bu bütçeden harcar
    context_tokens: int | None = Field(default=200000, ge=1024)


class CliConfig(ProviderConfig):
    """CLI ajanı (ADR-0012): çalıştırılabilir dosya adı ya da mutlak yolu."""

    command: str | None = None
    timeout_s: int = Field(default=300, ge=1)


class ClaudeCliConfig(CliConfig):
    """Claude Code CLI (`claude -p`); kimlik CLI oturumundan gelir, API anahtarı gerekmez."""

    command: str | None = "claude"
    context_tokens: int | None = Field(default=200000, ge=1024)


class AgyConfig(CliConfig):
    """Antigravity CLI (`agy -p`); araçları kapatılamadığı için açık onay gerekir."""

    command: str | None = "agy"
    allow_tool_agent: bool = False


class ProvidersSettings(BaseModel):
    default: str = "ollama"
    fallback: list[str] = Field(default_factory=list)
    max_retries: int = Field(default=2, ge=0, le=5)  # yalnızca ağ/429/5xx (mimari §5.5.3)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    deepseek: DeepSeekConfig = Field(default_factory=DeepSeekConfig)
    anthropic: AnthropicConfig = Field(default_factory=AnthropicConfig)
    claude_cli: ClaudeCliConfig = Field(default_factory=ClaudeCliConfig)
    agy: AgyConfig = Field(default_factory=AgyConfig)


class Settings(BaseSettings):
    """Kök yapılandırma nesnesi."""

    model_config = SettingsConfigDict(
        env_prefix="CODEMENTOR_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    limits: LimitsSettings = Field(default_factory=LimitsSettings)
    validation: ValidationSettings = Field(default_factory=ValidationSettings)
    pipeline: PipelineSettings = Field(default_factory=PipelineSettings)
    data: DataSettings = Field(default_factory=DataSettings)
    rules: RulesSettings = Field(default_factory=RulesSettings)
    prompts: PromptSettings = Field(default_factory=PromptSettings)
    verify: VerifySettings = Field(default_factory=VerifySettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    providers: ProvidersSettings = Field(default_factory=ProvidersSettings)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        toml_file = Path(os.environ.get(CONFIG_FILE_ENV, DEFAULT_CONFIG_FILE))
        toml_settings = TomlConfigSettingsSource(settings_cls, toml_file=toml_file)
        return (init_settings, env_settings, toml_settings)


def load_settings(**overrides: Any) -> Settings:
    """Önbelleksiz yükleme; `overrides` CLI bayraklarını temsil eder (en yüksek öncelik)."""
    return Settings(**overrides)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Süreç boyunca paylaşılan ayarlar."""
    return load_settings()
