"""Zamanlama testleri için ortak yardımcılar."""

from __future__ import annotations


def deadline(seconds: float) -> float:
    """Zaman sınırı; kapsama ölçümü (CI'da `--cov`) yavaşlattığı için ölçümde 4× genişletilir.

    Faz 53 kalıbı: yerelde ~0,4 sn süren kural motoru girdisi CI'da kapsama altında ~2 sn sürdü.
    """
    try:
        from coverage import Coverage
    except ImportError:  # pragma: no cover
        return seconds
    return seconds * (4.0 if Coverage.current() is not None else 1.0)
