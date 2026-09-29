"""YAML veri dosyalarını Pydantic modellerine yükleyen ortak yardımcılar."""

from __future__ import annotations

from collections.abc import Hashable
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError
from pydantic_core import ErrorDetails

from codementor.models.questions import (
    CHECKLIST_ITEM_ID_PATTERN,
    QUESTION_ID_PATTERN,
    TAG_PATTERN,
)

YAML_SUFFIXES = (".yaml", ".yml")

# Pydantic hata türü → Türkçe mesaj (ctx alanlarıyla biçimlenir)
_MESSAGES: dict[str, str] = {
    "missing": "alan zorunlu",
    "extra_forbidden": "tanımsız alan",
    "string_too_short": "boş olamaz",
    "string_too_long": "en fazla {max_length} karakter olabilir",
    "too_short": "en az {min_length} öğe olmalı",
    "too_long": "en fazla {max_length} öğe olabilir",
    "enum": "geçersiz değer (izin verilenler: {expected})",
    "literal_error": "geçersiz değer (izin verilenler: {expected})",
    "int_parsing": "tam sayı olmalı",
    "int_type": "tam sayı olmalı",
    "int_from_float": "tam sayı olmalı",
    "string_type": "metin olmalı (YAML'da on/off/yes/no gibi değerleri tırnak içine alın)",
    "bool_type": "true veya false olmalı",
    "list_type": "liste olmalı",
    "dict_type": "eşleme (anahtar: değer) olmalı",
    "model_type": "eşleme (anahtar: değer) olmalı",
    "greater_than_equal": "en az {ge} olmalı",
}

# Düzenli ifade yerine içerik yazarının anlayacağı örnekler
_PATTERN_HINTS: dict[str, str] = {
    QUESTION_ID_PATTERN: "küçük harf, rakam ve tire; ör. c-hard-stack",
    CHECKLIST_ITEM_ID_PATTERN: "ALAN-KATEGORİ-NNN; ör. UNITY-SO-001",
    TAG_PATTERN: "küçük harf, rakam ve tire; ör. memory-safety",
}


class DataFileError(ValueError):
    """Veri dosyası okunamadı veya doğrulanamadı. Mesaj kullanıcıya gösterilir."""


class _DuplicateKeyError(yaml.YAMLError):
    def __init__(self, key: object, line: int) -> None:
        super().__init__(f"yinelenen anahtar {key!r} (satır {line})")


class _UniqueKeyLoader(yaml.SafeLoader):
    """`SafeLoader` + yinelenen eşleme anahtarlarını reddeder (sessizce ezilmesin)."""

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Hashable, Any]:
        seen: set[Hashable] = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if isinstance(key, Hashable):
                if key in seen:
                    raise _DuplicateKeyError(key, key_node.start_mark.line + 1)
                seen.add(key)
        return super().construct_mapping(node, deep=deep)


def _message(error: ErrorDetails) -> str:
    ctx: dict[str, Any] = dict(error.get("ctx") or {})
    kind = error["type"]
    if kind == "value_error":
        return str(ctx.get("error", error["msg"]))
    if kind == "string_pattern_mismatch":
        hint = _PATTERN_HINTS.get(str(ctx.get("pattern")), f"desen: {ctx.get('pattern')}")
        return f"biçim geçersiz ({hint})"
    template = _MESSAGES.get(kind)
    if template is None:
        return f"geçersiz değer ({kind})"
    try:
        return template.format(**ctx)
    except KeyError:
        return f"geçersiz değer ({kind})"


def format_validation_error(path: Path, exc: ValidationError) -> str:
    """Doğrulama hatalarını `dosya: alan.yolu: mesaj` satırlarına çevirir.

    Girdi değerleri mesaja konmaz (ör. referans çözüm yolu dışarı sızmasın).
    """
    lines = [f"{path.name}: geçersiz içerik"]
    for error in exc.errors():
        loc = ".".join(str(part) for part in error["loc"]) or "(kök)"
        lines.append(f"  - {loc}: {_message(error)}")
    return "\n".join(lines)


def list_yaml_files(directory: Path, error_cls: type[DataFileError]) -> list[Path]:
    """Dizindeki YAML dosyaları (uzantı büyük/küçük harf duyarsız), ada göre sıralı."""
    if not directory.is_dir():
        raise error_cls(f"Veri dizini bulunamadı: {directory}")
    return sorted(
        p for p in directory.iterdir() if p.suffix.lower() in YAML_SUFFIXES and p.is_file()
    )


def load_model[M: BaseModel](path: Path, model: type[M], error_cls: type[DataFileError]) -> M:
    """YAML dosyasını güvenli okur (`SafeLoader` tabanlı) ve `model` ile doğrular."""
    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    except _DuplicateKeyError as exc:
        raise error_cls(f"{path.name}: {exc}") from exc
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        where = f" (satır {mark.line + 1})" if mark is not None else ""
        raise error_cls(f"{path.name}: YAML sözdizimi hatası{where}") from exc
    except (OSError, UnicodeDecodeError) as exc:
        raise error_cls(f"{path.name}: dosya okunamadı ({exc})") from exc
    if not isinstance(data, dict):
        raise error_cls(f"{path.name}: kök öğe bir eşleme (anahtar: değer) olmalı")
    try:
        return model.model_validate(data)
    except ValidationError as exc:
        raise error_cls(format_validation_error(path, exc)) from exc
