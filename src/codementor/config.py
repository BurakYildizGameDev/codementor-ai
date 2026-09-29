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


class ProviderConfig(BaseModel):
    base_url: str | None = None
    model: str = ""
    api_key_env: str | None = None
    num_ctx: int | None = None
    temperature: float | None = None
    seed: int | None = None
    timeout_s: int = 120


class ProvidersSettings(BaseModel):
    default: str = "ollama"
    fallback: list[str] = Field(default_factory=list)
    ollama: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(base_url="http://127.0.0.1:11434")
    )
    openai: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(api_key_env="OPENAI_API_KEY")
    )
    deepseek: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(api_key_env="DEEPSEEK_API_KEY")
    )
    anthropic: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(api_key_env="ANTHROPIC_API_KEY")
    )


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
