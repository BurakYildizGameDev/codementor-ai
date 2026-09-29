"""Ortak pytest yapılandırması.

`--update-golden`: golden testlerin beklenen çıktılarını (ör. `expected_facts.json`)
mevcut davranıştan yeniden yazar. Değişikliği `git diff` ile gözden geçirip commit'leyin.
"""

from __future__ import annotations

import pytest


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
