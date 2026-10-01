"""Tahmini maliyet (mimari §13): `data/pricing.yaml` birim fiyatlarından.

Fiyatlar değişir ve dosya elle güncellenir; sonuç rapora yalnızca "tahmini" olarak yazılır.
Listede olmayan sağlayıcı/model (ör. abonelikle çalışan claude_cli, yerel ollama) için `None`.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from codementor.models.eval import PricingFile
from codementor.questions._loader import DataFileError, load_model

PER_TOKENS = 1_000_000


class PricingError(DataFileError):
    """`data/pricing.yaml` okunamadı ya da geçersiz."""


@lru_cache(maxsize=4)
def _load(path: str, mtime_ns: int) -> PricingFile:
    return load_model(Path(path), PricingFile, PricingError)


def load_pricing(path: Path) -> PricingFile | None:
    """Fiyat dosyası (yoksa None); değişince yeniden okunur."""
    try:
        mtime = path.stat().st_mtime_ns
    except OSError:
        return None
    return _load(str(path), mtime)


def estimate_cost(
    pricing: PricingFile | None,
    provider: str | None,
    model: str | None,
    tokens_in: int,
    tokens_out: int,
) -> float | None:
    """Bir analizin tahmini maliyeti; fiyat yoksa ya da token harcanmadıysa None."""
    if pricing is None or not (tokens_in or tokens_out):
        return None
    price = next((p for p in pricing.prices if p.provider == provider and p.model == model), None)
    if price is None:
        return None
    return (tokens_in * price.input_per_mtok + tokens_out * price.output_per_mtok) / PER_TOKENS
