"""Kural fixture'larını okuma yardımcıları (mimari §15).

Düzen: `tests/rules/fixtures/{RULE_ID}/{positive,negative}/*.{c,cpp,cs}`.
- Dil dosya uzantısından gelir.
- Motor: dosyada `// ENGINE: unity|unreal|none` varsa o; yoksa kural tek bir motora
  özgüyse o motor, değilse `none`.
- Pozitif fixture'lar beklenen satırları `// EXPECT: 7` ya da `// EXPECT: 7, 12` ile verir.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language
from codementor.models.findings import Finding
from codementor.models.request import LanguageHint
from codementor.rules import run_rules
from codementor.rules.base import Rule

FIXTURES = Path(__file__).parent / "fixtures"
_EXTENSIONS = {".c": Language.C, ".cpp": Language.CPP, ".h": Language.CPP, ".cs": Language.CSHARP}
_EXPECT = re.compile(r"//\s*EXPECT:\s*([\d,\s]+)")
_ENGINE = re.compile(r"//\s*ENGINE:\s*(\w+)")


@dataclass(frozen=True)
class Fixture:
    rule_id: str
    kind: str  # positive | negative
    path: Path

    @property
    def label(self) -> str:
        return f"{self.rule_id}/{self.kind}/{self.path.name}"

    @property
    def text(self) -> str:
        return self.path.read_text(encoding="utf-8")

    def expected_lines(self) -> set[int]:
        return {int(n) for m in _EXPECT.finditer(self.text) for n in re.findall(r"\d+", m[1])}

    def engine(self, rule: type[Rule]) -> Engine:
        match = _ENGINE.search(self.text)
        if match:
            return Engine(match[1])
        return next(iter(rule.engines)) if len(rule.engines) == 1 else Engine.NONE

    def findings(self, rule: type[Rule]) -> list[Finding]:
        """Bu fixture'da yalnızca `rule`'un bulguları (tüm motor çalıştırılır)."""
        language = _EXTENSIONS[self.path.suffix]
        code = normalize(self.text, LanguageHint(language=language, engine=self.engine(rule)))
        result = run_rules(code, extract_facts(code))
        assert not result.warnings, result.warnings
        return [f for f in result.findings if f.rule_id == rule.id]


def all_fixtures() -> list[Fixture]:
    return [
        Fixture(rule_dir.name, kind_dir.name, path)
        for rule_dir in sorted(p for p in FIXTURES.iterdir() if p.is_dir())
        for kind_dir in sorted(p for p in rule_dir.iterdir() if p.is_dir())
        for path in sorted(kind_dir.iterdir())
        if path.suffix in _EXTENSIONS
    ]
