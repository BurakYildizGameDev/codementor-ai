"""Zamanlama testleri için ortak yardımcılar."""

from __future__ import annotations

import time
from collections.abc import Callable


def deadline(seconds: float) -> float:
    """Zaman sınırı; kapsama ölçümü (CI'da `--cov`) yavaşlattığı için ölçümde 4× genişletilir.

    Faz 53 kalıbı: yerelde ~0,4 sn süren kural motoru girdisi CI'da kapsama altında ~2 sn sürdü.
    """
    try:
        from coverage import Coverage
    except ImportError:  # pragma: no cover
        return seconds
    return seconds * (4.0 if Coverage.current() is not None else 1.0)


def best_pair(
    small: Callable[[], object], large: Callable[[], object], runs: int = 3
) -> tuple[float, float]:
    """İki girdinin en iyi süreleri (saniye): ısınma + `runs` tur, ölçümler dönüşümlü.

    Büyüme oranı testleri için: küçük ve büyük girdi art arda değil iç içe ölçülür; koşucudaki
    geçici yük (CI) yalnız büyük girdinin ölçümüne denk gelip oranı şişirmesin.
    """
    small()
    large()
    best = [float("inf"), float("inf")]
    for _ in range(runs):
        for index, run in enumerate((small, large)):
            start = time.perf_counter()
            run()
            best[index] = min(best[index], time.perf_counter() - start)
    return best[0], best[1]
