"""Canlı testler: yalnızca `uv run pytest -m live` ile; ağ ve gerçek anahtar gerektirir."""

from __future__ import annotations

import pytest


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
