"""Uygulama yapılandırması.

Öncelik sırası (mimari §17): CLI bayrağı > ortam değişkeni > codementor.toml > varsayılan.
CLI bayrakları `get_settings(**overrides)` ile init argümanı olarak verilir.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal, get_args

from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from codementor.paths import resolve_relative, resource_path

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
    stub_header: Path = Field(default_factory=lambda: resource_path("data/stubs/ue_stubs.h"))
    roslyn_check_dll: Path = Field(
        default_factory=lambda: resource_path("tools/roslyn-check/out/RoslynCheck.dll")
    )


class PipelineSettings(BaseModel):
    mode: Literal["two_pass", "single_pass"] = "two_pass"
    max_repair_attempts: int = Field(default=1, ge=0)
    use_cache: bool = True


class DataSettings(BaseModel):
    """Veri dizinleri; göreli yolların çözümü `codementor.paths` (ADR-0016)."""

    questions_dir: Path = Field(default_factory=lambda: resource_path("data/questions"))
    checklists_dir: Path = Field(default_factory=lambda: resource_path("data/checklists"))
    call_costs_file: Path = Field(default_factory=lambda: resource_path("data/call_costs.yaml"))
    mentor_templates_file: Path = Field(
        default_factory=lambda: resource_path("data/mentor_templates.yaml")
    )
    pricing_file: Path = Field(default_factory=lambda: resource_path("data/pricing.yaml"))


class PromptSettings(BaseModel):
    """Prompt şablonları ve token bütçesi (mimari §5.4.4-5.4.5)."""

    dir: Path = Field(default_factory=lambda: resource_path("prompts/v1"))
    default_context_tokens: int = Field(default=32768, ge=1024)
    reserve_output_tokens: int = Field(default=4096, ge=256)
    max_fewshots: int = Field(default=2, ge=0, le=4)
    max_checklist_items: int = Field(default=12, ge=0)
    # Ablasyon (mimari §14.4, eval): normalde ikisi de açık
    include_facts: bool = Field(default=True, description="Statik olgular + ipucu prompt'ta")
    numbered_code: bool = Field(default=True, description="Kod numaralı görünümle")


class ApiSettings(BaseModel):
    """REST API (mimari §9); varsayılan yalnızca yerel bağlama (§12)."""

    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://127.0.0.1:5173", "http://localhost:5173"]
    )
    api_key_env: str | None = Field(
        default=None,
        description="Doluysa bu ortam değişkenindeki anahtar `/v1/*` için X-API-Key ister (Faz 26)",
    )


class StorageSettings(BaseModel):
    """SQLite depolama (mimari §11); yol yoksa CODEMENTOR_DB_PATH, o da yoksa ~/.codementor."""

    db_path: Path | None = None


class VerifySettings(BaseModel):
    """K5 doğrulayıcı eşikleri (mimari §5.6); Faz 12 eval'inde ayarlanır."""

    evidence_window: int = Field(default=2, ge=0, le=10)
    leak_ngram_n: int = Field(default=5, ge=2, le=10)
    leak_ngram_threshold: float = Field(default=0.2, gt=0, le=1)
    leak_min_identifier_length: int = Field(default=3, ge=1)
    common_identifiers_file: Path = Field(
        default_factory=lambda: resource_path("data/leak_common_identifiers.yaml")
    )


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
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    deepseek: DeepSeekConfig = Field(default_factory=DeepSeekConfig)
    anthropic: AnthropicConfig = Field(default_factory=AnthropicConfig)
    claude_cli: ClaudeCliConfig = Field(default_factory=ClaudeCliConfig)
    agy: AgyConfig = Field(default_factory=AgyConfig)
    codex: CodexConfig = Field(default_factory=CodexConfig)


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
    api: ApiSettings = Field(default_factory=ApiSettings)
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
        toml_settings = _RelativeTomlSource(settings_cls, toml_file)
        return (init_settings, env_settings, toml_settings)


def _path_fields(settings_cls: type[BaseSettings]) -> dict[str, list[str]]:
    """Bölüm adı → `Path` tipli alan adları (iç içe modellerde bir düzey)."""
    found: dict[str, list[str]] = {}
    for section, info in settings_cls.model_fields.items():
        model = info.annotation
        if not (isinstance(model, type) and issubclass(model, BaseModel)):
            continue
        names = [
            name
            for name, field in model.model_fields.items()
            if field.annotation is Path or Path in get_args(field.annotation)
        ]
        if names:
            found[section] = names
    return found


class _RelativeTomlSource(TomlConfigSettingsSource):
    """`codementor.toml`'daki göreli yolları dosyanın dizinine göre çözer (ADR-0016)."""

    def __init__(self, settings_cls: type[BaseSettings], toml_file: Path) -> None:
        super().__init__(settings_cls, toml_file=toml_file)
        self._base = toml_file.absolute().parent

    def __call__(self) -> dict[str, Any]:
        data = dict(super().__call__())
        for section, names in _path_fields(self.settings_cls).items():
            values = data.get(section)
            if not isinstance(values, dict):
                continue
            data[section] = {
                key: resolve_relative(Path(value), self._base)
                if key in names and isinstance(value, str)
                else value
                for key, value in values.items()
            }
        return data


def load_settings(**overrides: Any) -> Settings:
    """Önbelleksiz yükleme; `overrides` CLI bayraklarını temsil eder (en yüksek öncelik)."""
    return Settings(**overrides)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Süreç boyunca paylaşılan ayarlar."""
    return load_settings()
