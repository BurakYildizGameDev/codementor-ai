"""Rapor ve önbellek anahtarındaki sürümler (mimari §6.4 `meta`, §11)."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from functools import lru_cache
from pathlib import Path

import codementor.analysis as analysis_package
import codementor.rules as rules_package
import codementor.validation as validation_package
import codementor.verify as verify_package
from codementor.log import get_logger
from codementor.models.report import AnalysisReport
from codementor.paths import resource_path
from codementor.rules.registry import all_rules

SCHEMA_VERSION: str = AnalysisReport.model_fields["schema_version"].default
DEFAULT_CALL_COSTS = resource_path("data/call_costs.yaml")
DEFAULT_MENTOR_TEMPLATES = resource_path("data/mentor_templates.yaml")

log = get_logger("codementor.pipeline")


def _package_root(package: object) -> Path:
    return Path(str(getattr(package, "__file__", ""))).parent


SOURCE_ROOT = _package_root(rules_package).parent  # `codementor/`


def hashed_sources() -> list[Path]:
    """Raporu belirleyen kaynaklar: kurallar, olgu/ipucu çıkarımı ve tree-sitter sorguları,
    Tier 0/1 doğrulama, LLM bulgu doğrulama (Faz 49: `.scm`, `validation/`, `verify/` eklendi)."""
    rules, analysis = _package_root(rules_package), _package_root(analysis_package)
    paths = [
        *rules.glob("*.py"),
        *analysis.rglob("*.py"),
        *analysis.rglob("*.scm"),
        *_package_root(validation_package).glob("*.py"),
        *_package_root(verify_package).glob("*.py"),
    ]
    return sorted(p for p in paths if "__pycache__" not in p.parts)


def _normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def digest_files(paths: Sequence[Path], base: Path) -> str:
    """Yolları (köke göreli, `/` ile) ve satır sonu normalleştirilmiş içerikleri özetler."""
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.relative_to(base).as_posix().encode() + b"\0")
        digest.update(_normalized(path.read_bytes()) + b"\0")
    return digest.hexdigest()


@lru_cache(maxsize=1)
def _code_digest() -> str:
    digest = hashlib.sha256()
    for rule_id in sorted(rule.id for rule in all_rules()):
        digest.update(rule_id.encode() + b"\0")
    sources = hashed_sources()
    if not sources:
        # Paketlenmiş exe'de .py/.scm kaynakları yoksa imza yalnız kural kimlikleri ve veri
        # dosyalarına dayanır; kural gövdesi değişince önbellek bayatlayabilir (Faz 50)
        log.warning("rules_version_without_sources", root=str(SOURCE_ROOT))
    digest.update(digest_files(sources, SOURCE_ROOT).encode())
    return digest.hexdigest()


def _file_bytes(path: Path, missing: bytes) -> bytes:
    """Veri dosyasının özete girecek içeriği; yoksa yer tutucu (eksiklik de sürümdür)."""
    try:
        return _normalized(path.read_bytes()) + b"\0"
    except OSError:
        return missing


def rules_version(call_costs: Path | None = None, mentor_templates: Path | None = None) -> str:
    """`"r2+" + sha256(kural kimlikleri + kaynaklar + maliyet tablosu + mentor şablonları)[:8]`:
    kural, olgu çıkarımı, sorgu, doğrulama ya da veri dosyası değişince önbellek geçersizleşir
    (Faz 31, Faz 49). Kod kısmı süreç başına bir kez, veri dosyaları her çağrıda okunur
    (küçük dosyalar). Satır sonu farkı sürümü değiştirmez."""
    digest = hashlib.sha256(_code_digest().encode())
    digest.update(_file_bytes(call_costs or DEFAULT_CALL_COSTS, b"<call_costs yok>"))
    templates = mentor_templates or DEFAULT_MENTOR_TEMPLATES
    digest.update(_file_bytes(templates, b"<mentor_templates yok>"))
    return f"r2+{digest.hexdigest()[:8]}"
