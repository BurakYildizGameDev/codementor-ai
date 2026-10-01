"""Ortak pytest yapılandırması.

`--update-golden`: golden testlerin beklenen çıktılarını (ör. `expected_facts.json`)
mevcut davranıştan yeniden yazar. Değişikliği `git diff` ile gözden geçirip commit'leyin.
"""

from __future__ import annotations

import io
import json
import logging
from collections.abc import Callable, Iterator
from typing import Any

import pytest

from codementor.log import configure_logging


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
