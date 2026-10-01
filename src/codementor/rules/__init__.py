"""Statik kural motoru ve kurallar (mimari §5.3.3, §8.2).

Kural modülleri içe aktarılınca `@register_rule` ile kayıt defterine eklenir.
"""

from __future__ import annotations

from codementor.rules import c, cpp, csharp, css, html, python, unity, unreal
from codementor.rules.engine import run_rules
from codementor.rules.registry import all_rules, applicable_rules

__all__ = [
    "all_rules",
    "applicable_rules",
    "c",
    "cpp",
    "csharp",
    "css",
    "html",
    "python",
    "run_rules",
    "unity",
    "unreal",
]
