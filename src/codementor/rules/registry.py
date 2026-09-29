"""Kural kayıt defteri (mimari §5.3.3, §8.1)."""

from __future__ import annotations

import re
from collections.abc import Iterable

from codementor.models.enums import Engine, Language
from codementor.models.rules import RULE_ID_PATTERN
from codementor.rules.base import Rule

RULE_ID = re.compile(RULE_ID_PATTERN)

_RULES: dict[str, type[Rule]] = {}


def register_rule[R: type[Rule]](cls: R) -> R:
    """Sınıf dekoratörü: kuralı kimliğiyle kaydeder; biçim hatası ve yinelenen kimlik reddedilir."""
    if not RULE_ID.fullmatch(cls.id):
        raise ValueError(f"Geçersiz kural kimliği: {cls.id!r} (biçim: ALAN-KATEGORİ-NNN)")
    if cls.id in _RULES and _RULES[cls.id] is not cls:
        raise ValueError(f"Kural kimliği iki kez kaydedildi: {cls.id}")
    if not cls.languages:
        raise ValueError(f"Kural dil kümesi boş: {cls.id}")
    _RULES[cls.id] = cls
    return cls


def unregister_rule(rule_id: str) -> None:
    """Kaydı siler (yalnızca testler için)."""
    _RULES.pop(rule_id, None)


def all_rules() -> list[type[Rule]]:
    """Kayıtlı kurallar, kimliğe göre sıralı."""
    return [_RULES[k] for k in sorted(_RULES)]


def applicable_rules(
    language: Language, engine: Engine, disabled: Iterable[str] = ()
) -> list[type[Rule]]:
    """Dil/motor filtresinden geçen ve yapılandırmada kapatılmamış kurallar."""
    off = set(disabled)
    return [r for r in all_rules() if r.id not in off and r.applies_to(language, engine)]
