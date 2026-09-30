"""Rapor ve önbellek anahtarındaki sürümler (mimari §6.4 `meta`, §11)."""

from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path

import codementor.rules as rules_package
from codementor.models.report import AnalysisReport
from codementor.rules.registry import all_rules

SCHEMA_VERSION: str = AnalysisReport.model_fields["schema_version"].default


@lru_cache(maxsize=1)
def rules_version() -> str:
    """`"r1+" + sha256(kural kimlikleri + kural kaynak dosyaları)[:8]`: bir kural değişince
    önbellek geçersizleşir. Satır sonu farkı sürümü değiştirmez."""
    digest = hashlib.sha256()
    for rule_id in sorted(rule.id for rule in all_rules()):
        digest.update(rule_id.encode() + b"\0")
    package = Path(rules_package.__file__).parent
    for path in sorted(package.glob("*.py")):
        digest.update(path.name.encode() + b"\0")
        digest.update(path.read_bytes().replace(b"\r\n", b"\n") + b"\0")
    return f"r1+{digest.hexdigest()[:8]}"
