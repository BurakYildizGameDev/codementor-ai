"""Tier 0 fixture keşfi: `tests/fixtures/tier0/{dil}/{valid,invalid}/`.

- Dil dizinden, motor dosya adı önekinden (`unity_`, `unreal_`) gelir.
- Geçersiz dosyalarda beklenen hata satırı `expect-error` yorumuyla işaretlidir.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from codementor.models.enums import Engine, Language

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "tier0"
ERROR_MARKER = "expect-error"

_LANGUAGES = {"c": Language.C, "cpp": Language.CPP, "csharp": Language.CSHARP}


@dataclass(frozen=True)
class Tier0Fixture:
    path: Path
    language: Language
    engine: Engine
    valid: bool
    expected_line: int | None

    @property
    def text(self) -> str:
        return self.path.read_text(encoding="utf-8")

    @property
    def id(self) -> str:
        return "/".join(self.path.parts[-3:])


def _engine(name: str) -> Engine:
    if name.startswith("unity_"):
        return Engine.UNITY
    if name.startswith("unreal_"):
        return Engine.UNREAL
    return Engine.NONE


def load_fixtures(*, valid: bool | None = None) -> list[Tier0Fixture]:
    result: list[Tier0Fixture] = []
    for path in sorted(FIXTURES.glob("*/*/*")):
        language = _LANGUAGES[path.parts[-3]]
        is_valid = path.parts[-2] == "valid"
        if valid is not None and is_valid != valid:
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        marked = [i for i, line in enumerate(lines, start=1) if ERROR_MARKER in line]
        result.append(
            Tier0Fixture(
                path, language, _engine(path.name), is_valid, marked[0] if marked else None
            )
        )
    return result
