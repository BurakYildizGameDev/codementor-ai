"""API hız sınırlayıcı (Faz E; tam tarama düşük madde, KALAN_ISLER iş 21)."""

from __future__ import annotations

import pytest

from codementor.api.errors import ApiProblemError
from codementor.api.guard import RateLimiter


class FakeClock:
    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now


def test_limit_and_window_use_injected_clock() -> None:
    clock = FakeClock()
    limiter = RateLimiter(2, clock=clock)
    limiter.check("10.0.0.1")
    limiter.check("10.0.0.1")
    with pytest.raises(ApiProblemError) as caught:
        limiter.check("10.0.0.1")
    assert caught.value.status == 429
    limiter.check("10.0.0.2")  # IP başına ayrı pencere
    clock.now += 60.1
    limiter.check("10.0.0.1")  # pencere geçti


def test_stale_clients_are_swept() -> None:
    """Geçip giden istemciler sözlüğü sınırsız büyütmez (eskiden her IP kalıcıydı)."""
    clock = FakeClock()
    limiter = RateLimiter(5, clock=clock)
    for i in range(500):
        limiter.check(f"10.0.{i // 256}.{i % 256}")
    assert limiter.tracked_clients() == 500
    clock.now += 61
    limiter.check("192.0.2.1")
    assert limiter.tracked_clients() == 1


def test_unlimited_tracks_nothing() -> None:
    limiter = RateLimiter(None)
    for _ in range(100):
        limiter.check("10.0.0.1")
    assert limiter.tracked_clients() == 0
