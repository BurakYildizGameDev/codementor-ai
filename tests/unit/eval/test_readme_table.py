"""README'deki eval tabloları `eval/results/` dosyalarıyla birebir (Faz 13 kabul kriteri).

Tablo elle yazılmaz: `codementor eval compare <dosyalar>` çıktısı işaretler arasına konur.
Sonuç dosyası değişirse ya da tablo elle düzenlenirse bu test düşer.
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
    r"<!-- eval-table:(?P<split>\w+):start -->\n(?P<body>.*?)\n<!-- eval-table:(?P=split):end -->",
    re.DOTALL,
)


def _blocks() -> dict[str, str]:
    text = README.read_text(encoding="utf-8").replace("\r\n", "\n")
    return {m["split"]: m["body"].strip() for m in BLOCK.finditer(text)}


def test_readme_has_test_and_dev_tables() -> None:
    assert set(_blocks()) == {"test", "dev"}


@pytest.mark.parametrize("split", ["test", "dev"])
def test_readme_eval_table_matches_results(split: str) -> None:
    files = sorted(RESULTS.glob(f"*_{split}.json"))
    assert files, f"eval/results/*_{split}.json yok"
    expected = compare_table(load_results(files)).strip()
    assert _blocks()[split] == expected, (
        f"README {split} tablosu güncel değil: "
        f"`uv run codementor eval compare eval/results/*_{split}.json` çıktısını yapıştırın"
    )
