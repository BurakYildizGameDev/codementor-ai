"""`data/call_costs.yaml` ve çağrı maliyeti çözümleyicisi testleri (mimari §5.3.2)."""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.analysis._symbols import CallName
from codementor.analysis.call_costs import CallCostError, CostResolver, load_call_costs
from codementor.models.bigo import parse_cost
from codementor.models.enums import Language
from codementor.models.facts import CallCostTable

DATA = Path(__file__).resolve().parents[2] / "data" / "call_costs.yaml"


@pytest.fixture(scope="module")
def table() -> CallCostTable:
    return load_call_costs(DATA)


def test_mimari_examples_present(table: CallCostTable) -> None:
    """Mimari §5.3.2'deki örnek tablonun tamamı."""
    assert table.cpp["std::sort"] == "n log n"
    assert table.cpp["std::find"] == "n"
    assert table.cpp["std::vector::push_back"] == "1*"
    assert table.cpp["std::map::find"] == "log n"
    assert table.cpp["std::unordered_map::find"] == "1*"
    assert table.csharp["List.Contains"] == "n"
    assert table.csharp["List.IndexOf"] == "n"
    assert table.csharp["List.Insert"] == "n"
    assert table.csharp["Dictionary.ContainsKey"] == "1*"
    assert table.csharp["Array.Sort"] == "n log n"
    assert table.csharp["Enumerable.OrderBy"] == "n log n"
    assert table.c["strlen"] == "n"
    assert table.c["qsort"] == "n log n"


def test_every_cost_parses(table: CallCostTable) -> None:
    for entries in (table.c, table.cpp, table.csharp):
        for cost in entries.values():
            value, _ = parse_cost(cost)
            assert value.canonical in {"1", "log n", "n", "n log n"}


def test_invalid_cost_rejected(tmp_path: Path) -> None:
    bad = tmp_path / "costs.yaml"
    bad.write_text('cpp:\n  "std::sort": "hızlı"\n', encoding="utf-8")
    with pytest.raises(CallCostError, match=r"costs\.yaml"):
        load_call_costs(bad)


def test_unknown_language_key_rejected(tmp_path: Path) -> None:
    bad = tmp_path / "costs.yaml"
    bad.write_text('java:\n  "List.add": "1"\n', encoding="utf-8")
    with pytest.raises(CallCostError):
        load_call_costs(bad)


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(CallCostError, match="bulunamadı"):
        load_call_costs(tmp_path / "yok.yaml")


def _call(method: str, receiver: str | None = None, qualified: str | None = None) -> CallName:
    display = qualified or (f"{receiver}.{method}" if receiver else method)
    return CallName(display, method, receiver, qualified)


@pytest.mark.parametrize(
    ("language", "call", "types", "flags", "expected"),
    [
        (Language.C, _call("strlen"), {}, {}, ("strlen", "n")),
        (Language.C, _call("printf"), {}, {}, None),
        (Language.CPP, _call("sort", qualified="std::sort"), {}, {}, ("std::sort", "n log n")),
        (Language.CPP, _call("sort"), {}, {"using_std": True}, ("std::sort", "n log n")),
        (Language.CPP, _call("sort"), {}, {}, None),
        (Language.CPP, _call("find", "m"), {"m": "std::map"}, {}, ("std::map::find", "log n")),
        (Language.CPP, _call("find", "m"), {"m": "map"}, {}, ("std::map::find", "log n")),
        (Language.CPP, _call("Add", "this->Items"), {"Items": "TArray"}, {}, ("TArray::Add", "1*")),
        (Language.CPP, _call("find", "m"), {}, {}, None),
        (Language.CSHARP, _call("Contains", "xs"), {"xs": "List"}, {}, ("List.Contains", "n")),
        (Language.CSHARP, _call("Sort", "Array"), {}, {}, ("Array.Sort", "n log n")),
        (Language.CSHARP, _call("Contains", "s"), {"s": "String"}, {}, ("string.Contains", "n")),
        (
            Language.CSHARP,
            _call("Where", "xs"),
            {"xs": "IEnumerable"},
            {"using_linq": True},
            ("Enumerable.Where", "n"),
        ),
        (Language.CSHARP, _call("Where", "xs"), {"xs": "IEnumerable"}, {}, None),
        (Language.CSHARP, _call("FindObjectOfType"), {}, {}, ("FindObjectOfType", "n")),
    ],
)
def test_resolve(
    table: CallCostTable,
    language: Language,
    call: CallName,
    types: dict[str, str],
    flags: dict[str, bool],
    expected: tuple[str, str] | None,
) -> None:
    resolver = CostResolver(table=table, language=language, types=types, **flags)
    assert resolver.resolve(call) == expected
