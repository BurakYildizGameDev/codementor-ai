"""Sağlayıcı testleri: anyio (yalnızca asyncio), respx ile ağsız HTTP, test API anahtarları."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
import respx

from tests.providers.contract import (
    API_KEYS,
    HARNESS_NAMES,
    FakeHarness,
    Harness,
    SleepRecorder,
    http_harness,
)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(autouse=True)
def api_keys(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    for name, value in API_KEYS.items():
        monkeypatch.setenv(name, value)
    return API_KEYS


@pytest.fixture
def router() -> Iterator[respx.MockRouter]:
    # assert_all_mocked: taklit edilmeyen her istek hata verir (testler ağa çıkamaz)
    with respx.mock(assert_all_called=False, assert_all_mocked=True) as mock:
        yield mock


@pytest.fixture
def sleep() -> SleepRecorder:
    return SleepRecorder()


@pytest.fixture(params=HARNESS_NAMES)
def harness(
    request: pytest.FixtureRequest, router: respx.MockRouter, sleep: SleepRecorder
) -> Harness:
    name: str = request.param
    if name == "fake":
        return FakeHarness(sleep)
    return http_harness(name, router, sleep)
