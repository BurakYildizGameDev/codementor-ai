"""Ortak pytest yapılandırması.

`--update-golden`: golden testlerin beklenen çıktılarını (ör. `expected_facts.json`)
mevcut davranıştan yeniden yazar. Değişikliği `git diff` ile gözden geçirip commit'leyin.
"""

from __future__ import annotations

import io
import json
import logging
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest

import codementor.config
from codementor.log import configure_logging
from codementor.validation.toolchain import clear_toolchain_cache


@pytest.fixture(autouse=True)
def _isolated_toolchain_dir(
    tmp_path_factory: pytest.TempPathFactory, monkeypatch: pytest.MonkeyPatch
) -> Iterator[None]:
    """Testler geliştiricinin indirdiği derleyiciyi (~/.codementor/toolchain) görmez (Faz 29)."""
    empty: Path = tmp_path_factory.getbasetemp() / "no-toolchain"
    monkeypatch.setattr(codementor.config, "_default_toolchain_dir", lambda: empty)
    clear_toolchain_cache()
    yield
    clear_toolchain_cache()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--update-golden",
        action="store_true",
        default=False,
        help="Golden beklenen çıktılarını yeniden yaz (uv run pytest --update-golden)",
    )


@pytest.fixture
def update_golden(request: pytest.FixtureRequest) -> bool:
    """`--update-golden` verildi mi."""
    return bool(request.config.getoption("--update-golden"))


@pytest.fixture
def captured_logs() -> Iterator[Callable[[], list[dict[str, Any]]]]:
    """Projenin kendi logger'ının (`codementor.log.get_logger`) JSON çıktısını yakalar.

    `structlog.testing.capture_logs` bu logger'ı görmez (kendi işlemci zinciriyle kurulur);
    bu fikstür gerçek çıktıyı (maskeleme dahil) satır satır sözlük olarak verir.
    """
    stream = io.StringIO()
    configure_logging(stream, json=True, level=logging.DEBUG)

    def read() -> list[dict[str, Any]]:
        return [json.loads(line) for line in stream.getvalue().splitlines() if line.strip()]

    yield read
    configure_logging()  # varsayılan ayarlara dön (stderr, WARNING)
