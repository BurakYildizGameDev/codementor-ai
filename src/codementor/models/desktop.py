"""Masaüstü istemcisinin (ADR-0013, ADR-0014) kalıcı kullanıcı tercihleri ve bağlantı modelleri."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import Engine, Language

MAX_RECENT_FILES = 8


class ProviderOverride(StrictModel):
    """Arayüzden seçilen sağlayıcı ayarları; `codementor.toml`'un üstüne yazılır (anahtar değil)."""

    model: str | None = Field(default=None, max_length=200)
    base_url: str | None = Field(default=None, max_length=500)
    allow_tool_agent: bool | None = Field(
        default=None, description="Yalnız agy ve codex (ADR-0012, ADR-0017)"
    )

    def as_settings(self) -> dict[str, Any]:
        """`load_settings(providers={ad: ...})` için yalnız dolu alanlar."""
        return self.model_dump(exclude_none=True)


class DesktopPrefs(StrictModel):
    """`~/.codementor/desktop.json`: son seçimler, sağlayıcı ayarları ve ipucu oturumu."""

    provider: str | None = Field(default=None, description="Boşsa codementor.toml varsayılanı")
    providers: dict[str, ProviderOverride] = Field(default_factory=dict)
    language: Language = Language.C
    engine: Engine = Engine.NONE
    session_id: str | None = Field(default=None, description="İpucu merdiveni oturumu")
    recent_files: list[str] = Field(default_factory=list, max_length=MAX_RECENT_FILES)


class ConnectionPing(StrictModel):
    """ "Bağlantıyı dene" düğmesinin istediği en küçük yapılandırılmış yanıt."""

    ok: bool
