"""Masaüstü istemcisinin (ADR-0013) kalıcı kullanıcı tercihleri."""

from __future__ import annotations

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import Engine, Language

MAX_RECENT_FILES = 8


class DesktopPrefs(StrictModel):
    """`~/.codementor/desktop.json`: son seçimler ve ipucu merdiveni oturumu."""

    provider: str | None = Field(default=None, description="Boşsa codementor.toml varsayılanı")
    language: Language = Language.C
    engine: Engine = Engine.NONE
    session_id: str | None = Field(default=None, description="İpucu merdiveni oturumu")
    recent_files: list[str] = Field(default_factory=list, max_length=MAX_RECENT_FILES)
