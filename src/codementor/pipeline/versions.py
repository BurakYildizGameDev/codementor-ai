"""Rapor ve önbellek anahtarındaki sürümler (mimari §6.4 `meta`, §11)."""

from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path

import codementor.analysis as analysis_package
import codementor.rules as rules_package
from codementor.models.report import AnalysisReport
from codementor.paths import resource_path
from codementor.rules.registry import all_rules

SCHEMA_VERSION: str = AnalysisReport.model_fields["schema_version"].default
DEFAULT_CALL_COSTS = resource_path("data/call_costs.yaml")


def hashed_sources() -> list[Path]:
    """Statik analizin çıktısını belirleyen kaynaklar: kurallar ve olgu/ipucu çıkarımı."""
    packages = (rules_package, analysis_package)
    roots = [Path(str(pkg.__file__)).parent for pkg in packages]
    return sorted(p for root in roots for p in root.glob("*.py"))


def _normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


@lru_cache(maxsize=1)
def _code_digest() -> str:
    digest = hashlib.sha256()
    for rule_id in sorted(rule.id for rule in all_rules()):
        digest.update(rule_id.encode() + b"\0")
    for path in hashed_sources():
        digest.update(f"{path.parent.name}/{path.name}".encode() + b"\0")
        digest.update(_normalized(path.read_bytes()) + b"\0")
    return digest.hexdigest()


def rules_version(call_costs: Path | None = None) -> str:
    """`"r1+" + sha256(kural kimlikleri + rules/ ve analysis/ kaynakları + maliyet tablosu)[:8]`:
    bir kural, olgu çıkarımı ya da maliyet tablosu değişince önbellek geçersizleşir (Faz 31).
    Kod kısmı süreç başına bir kez, maliyet tablosu her çağrıda okunur (küçük dosya).
    Satır sonu farkı sürümü değiştirmez."""
    digest = hashlib.sha256(_code_digest().encode())
    try:
        digest.update(_normalized((call_costs or DEFAULT_CALL_COSTS).read_bytes()))
    except OSError:
        digest.update(b"<call_costs yok>")
    return f"r1+{digest.hexdigest()[:8]}"
