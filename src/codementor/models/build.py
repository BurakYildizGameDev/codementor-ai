"""Derleme ve sürüm bilgisi modeli (Faz 60)."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from codementor.models._base import StrictModel


class BuildInfo(StrictModel):
    """Çalışan uygulamanın sürüm, commit ve derleme kaynağı bilgisi."""

    version: str  # codementor.__version__
    commit: str | None = None  # kısa git özeti; bilinmiyorsa None
    built_at: datetime | None = None  # exe derleme zamanı (UTC); kaynaktan çalışırken None
    source: Literal["exe", "kaynak"]
