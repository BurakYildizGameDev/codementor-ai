"""README'deki eval tabloları `eval/results/` dosyalarıyla birebir (Faz 13 kabul kriteri).

Tablo elle yazılmaz: `codementor eval compare <dosyalar>` çıktısı işaretler arasına konur.
Sonuç dosyası değişirse ya da tablo elle düzenlenirse bu test düşer. Eski koşular
`eval/results/arsiv/` altındadır ve tablolara girmez; dil filtreli deneme koşuları da girmez.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from codementor.eval.compare import compare_table, load_results

ROOT = Path(__file__).resolve().parents[3]
README = ROOT / "README.md"
RESULTS = ROOT / "eval" / "results"
BLOCK = re.compile(
    r"<!-- eval-table:(?P<split>[\w-]+):start -->\n"
    r"(?P<body>.*?)\n<!-- eval-table:(?P=split):end -->",
    re.DOTALL,
)


def _blocks() -> dict[str, str]:
    text = README.read_text(encoding="utf-8").replace("\r\n", "\n")
    return {m["split"]: m["body"].strip() for m in BLOCK.finditer(text)}


BLOCKS = ["test", "dev"]


def test_readme_has_test_and_dev_tables() -> None:
    assert set(_blocks()) == set(BLOCKS)


@pytest.mark.parametrize("block", BLOCKS)
def test_readme_eval_table_matches_results(block: str) -> None:
    results = [
        r
        for r in load_results(sorted(RESULTS.glob(f"*_{block}.json")))
        if not r.config.languages  # dil filtreli deneme koşuları tabloya girmez
    ]
    assert results, f"{block}: sonuç dosyası yok"
    expected = compare_table(results).strip()
    assert _blocks()[block] == expected, (
        f"README {block} tablosu güncel değil: ilgili sonuç dosyalarıyla "
        "`uv run codementor eval compare ...` çıktısını yapıştırın"
    )
