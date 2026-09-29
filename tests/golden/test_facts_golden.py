"""Olgu çıkarımı golden testleri: `tests/golden/facts/{id}/code.* + expected_facts.json`.

`{id}` öneki dil/motoru belirler: `c-`, `cpp-`, `csharp-`, `unity-`, `unreal-`.
Beklenenleri güncellemek için: `uv run pytest tests/golden --update-golden`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language
from codementor.models.request import LanguageHint

ROOT = Path(__file__).parent / "facts"
EXPECTED = "expected_facts.json"
_PREFIXES = {
    "c": (Language.C, Engine.NONE),
    "cpp": (Language.CPP, Engine.NONE),
    "csharp": (Language.CSHARP, Engine.NONE),
    "unity": (Language.CSHARP, Engine.UNITY),
    "unreal": (Language.CPP, Engine.UNREAL),
}
CASES = sorted(p for p in ROOT.iterdir() if p.is_dir())


def _source(case: Path) -> Path:
    (source,) = case.glob("code.*")
    return source


def snapshot(case: Path) -> dict[str, Any]:
    """Bir golden vakanın güncel çıktısı (JSON uyumlu)."""
    language, engine = _PREFIXES[case.name.split("-")[0]]
    code = normalize(_source(case).read_bytes(), LanguageHint(language=language, engine=engine))
    return {
        "language": language.value,
        "engine": engine.value,
        "facts": extract_facts(code).model_dump(mode="json"),
    }


def write_snapshot(path: Path, data: dict[str, Any]) -> None:
    """Kararlı biçimde yazar (girinti 2, UTF-8, sonda satır sonu)."""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_every_language_and_engine_has_three_cases() -> None:
    counts = {prefix: 0 for prefix in _PREFIXES}
    for case in CASES:
        counts[case.name.split("-")[0]] += 1
    assert all(n >= 3 for n in counts.values()), counts


@pytest.mark.parametrize("case", CASES, ids=[c.name for c in CASES])
def test_facts_golden(case: Path, update_golden: bool) -> None:
    actual = snapshot(case)
    expected_path = case / EXPECTED
    if update_golden:
        write_snapshot(expected_path, actual)
        return
    assert expected_path.is_file(), (
        f"{expected_path} yok: uv run pytest tests/golden --update-golden"
    )
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    assert actual == expected
    assert actual["facts"]["warnings"] == [], "golden kodu geçerli olmalı"


def test_write_snapshot_round_trip(tmp_path: Path) -> None:
    data = {"facts": {"functions": [{"name": "Ölç"}]}}
    target = tmp_path / EXPECTED
    write_snapshot(target, data)
    assert json.loads(target.read_text(encoding="utf-8")) == data
    assert target.read_text(encoding="utf-8").endswith("}\n")


def test_update_golden_option_registered(request: pytest.FixtureRequest) -> None:
    assert request.config.getoption("--update-golden") in (True, False)
