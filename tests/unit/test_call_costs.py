"""`data/call_costs.yaml` ve çağrı maliyeti çözümleyicisi testleri (mimari §5.3.2)."""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.analysis._symbols import CallName
from codementor.analysis.call_costs import CallCostError, CostResolver, load_call_costs
from codementor.models.bigo import parse_cost
from codementor.models.enums import Engine, Language
from codementor.models.facts import CallCostTable
from tests.unit.extractor_support import _facts

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


def _call(
    method: str,
    receiver: str | None = None,
    qualified: str | None = None,
    first_arg: str | None = None,
    arg_count: int = 0,
) -> CallName:
    display = qualified or (f"{receiver}.{method}" if receiver else method)
    return CallName(display, method, receiver, qualified, arg_count, False, first_arg)


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


# --- Faz 21: tablo eksikleri ve arayüz tipleri ----------------------------------------------


def _costs(text: str, language: Language, engine: Engine = Engine.NONE) -> dict[str, str | None]:
    return {c.name: c.known_cost for c in _facts(text, language, engine).calls}


def test_cpp_memset_family_linear() -> None:
    costs = _costs(
        "#include <cstring>\nvoid f(char *a, char *b, int n) {\n"
        "    std::memset(a, 0, n); std::memcpy(a, b, n); memmove(a, b, n);\n}\n",
        Language.CPP,
    )
    assert costs["std::memset"] == "n"
    assert costs["std::memcpy"] == "n"
    assert costs["memmove"] == "n"


def test_unreal_get_all_actors_linear() -> None:
    costs = _costs(
        "void AA::F() {\n    UGameplayStatics::GetAllActorsOfClass(GetWorld(), X, Out);\n"
        "    UGameplayStatics::GetAllActorsWithTag(GetWorld(), T, Out);\n}\n",
        Language.CPP,
        Engine.UNREAL,
    )
    assert costs["UGameplayStatics::GetAllActorsOfClass"] == "n"
    assert costs["UGameplayStatics::GetAllActorsWithTag"] == "n"


def test_csharp_list_bulk_ops_linear() -> None:
    costs = _costs(
        "using System.Collections.Generic;\nclass A { void F(List<int> xs) {\n"
        "    xs.RemoveAll(x => x > 0); xs.RemoveRange(0, 2); xs.InsertRange(0, xs);\n} }\n",
        Language.CSHARP,
    )
    assert costs["List.RemoveAll"] == "n"
    assert costs["List.RemoveRange"] == "n"
    assert costs["List.InsertRange"] == "n"


def test_ilist_receiver_resolves_to_list() -> None:
    """`IList<T>` örnek metotları (`Contains`, `IndexOf`) List'inki gibi doğrusal."""
    costs = _costs(
        "using System.Collections.Generic;\nclass A { void F(IList<int> xs) {\n"
        "    xs.Contains(1); xs.IndexOf(2);\n} }\n",
        Language.CSHARP,
    )
    assert costs["List.Contains"] == "n"
    assert costs["List.IndexOf"] == "n"


def test_ireadonlylist_contains_stays_linq() -> None:
    """Denetim O1: `IReadOnlyList<T>`'te `Contains` örnek metodu yok; çağrı LINQ'tir
    (`Enumerable.Contains`) ve sıcak yolda CS-ALLOC-002 olarak raporlanmalı."""
    text = (
        "using System.Collections.Generic;\nusing System.Linq;\nusing UnityEngine;\n"
        "public class P : MonoBehaviour {\n    public IReadOnlyList<int> ys;\n"
        "    void Update() { if (ys.Contains(1)) { } }\n}\n"
    )
    facts = _facts(text, Language.CSHARP, Engine.UNITY)
    assert [c.name for c in facts.calls] == ["Enumerable.Contains"]
    assert [a.kind.value for a in facts.allocations] == ["linq"]


def test_icollection_stays_unknown() -> None:
    """`ICollection` bir HashSet de olabilir: maliyet tahmin edilmez."""
    costs = _costs(
        "using System.Collections.Generic;\nclass A { void F(ICollection<int> zs) {\n"
        "    zs.Contains(1);\n} }\n",
        Language.CSHARP,
    )
    assert costs == {"zs.Contains": None}


def test_icollection_with_linq_still_unknown() -> None:
    """Faz H2: `using System.Linq` olsa da `ICollection<T>.Contains` örnek metottur.

    LINQ uzantısına bağlanmaz (alıcı bir `HashSet` olabilir) → maliyet yine bilinmez.
    """
    costs = _costs(
        "using System.Collections.Generic;\nusing System.Linq;\nclass A { "
        "void F(ICollection<int> zs) {\n    zs.Contains(1);\n} }\n",
        Language.CSHARP,
    )
    assert costs == {"zs.Contains": None}


def test_ireadonlylist_contains_costs_linear() -> None:
    """Faz H2: `IReadOnlyList<T>.Contains` LINQ'tir → `Enumerable.Contains` = n."""
    costs = _costs(
        "using System.Collections.Generic;\nusing System.Linq;\nclass A { "
        "void F(IReadOnlyList<int> ys) {\n    ys.Contains(1);\n} }\n",
        Language.CSHARP,
    )
    assert costs == {"Enumerable.Contains": "n"}


# --- Faz H3: argümana duyarlı indeks maliyetleri --------------------------------------------


@pytest.mark.parametrize(
    ("call", "expected"),
    [
        # aynı listenin son elemanı: kaydırma yok → O(1)
        (
            _call("RemoveAt", "items", first_arg="items.Count - 1", arg_count=1),
            ("List.RemoveAt", "1"),
        ),
        (
            _call("RemoveAt", "items", first_arg="items.Length-1", arg_count=1),
            ("List.RemoveAt", "1"),
        ),
        # baştan ya da bilinmeyen indeksten silme: kaydırma → n (tablo değeri)
        (_call("RemoveAt", "items", first_arg="0", arg_count=1), ("List.RemoveAt", "n")),
        (
            _call("RemoveAt", "items", first_arg="items.Count - 2", arg_count=1),
            ("List.RemoveAt", "n"),
        ),
        (_call("RemoveAt", "items", first_arg="i", arg_count=1), ("List.RemoveAt", "n")),
        (_call("RemoveAt", "items", arg_count=1), ("List.RemoveAt", "n")),
        # başka bir koleksiyonun son indeksi hedef olabilir: muhafazakâr n
        (
            _call("RemoveAt", "items", first_arg="other.Count - 1", arg_count=1),
            ("List.RemoveAt", "n"),
        ),
        # sona ekleme = `Add` → amortize 1
        (_call("Insert", "items", first_arg="items.Count", arg_count=2), ("List.Insert", "1*")),
        (_call("Insert", "items", first_arg="0", arg_count=2), ("List.Insert", "n")),
        (_call("Insert", "items", first_arg="items.Count - 1", arg_count=2), ("List.Insert", "n")),
        (_call("Insert", "items", first_arg="i + 1", arg_count=2), ("List.Insert", "n")),
    ],
)
def test_argument_aware_index_costs(
    table: CallCostTable, call: CallName, expected: tuple[str, str]
) -> None:
    resolver = CostResolver(table=table, language=Language.CSHARP, types={"items": "List"})
    assert resolver.resolve(call) == expected


def test_receiver_prefix_is_ignored_for_index_pattern() -> None:
    """`this.items.RemoveAt(this.items.Count - 1)`: `this.` öneki eşleşmeyi bozmaz."""
    call = _call("RemoveAt", "this.items", first_arg="this.items.Count - 1", arg_count=1)
    resolver = CostResolver(
        table=load_call_costs(DATA), language=Language.CSHARP, types={"items": "List"}
    )
    assert resolver.resolve(call) == ("List.RemoveAt", "1")


@pytest.mark.parametrize(
    ("statement", "name", "expected"),
    [
        ("xs.RemoveAt(xs.Count - 1)", "List.RemoveAt", "1"),
        ("xs.RemoveAt(0)", "List.RemoveAt", "n"),
        ("xs.Insert(xs.Count, 9)", "List.Insert", "1*"),
        ("xs.Insert(0, 9)", "List.Insert", "n"),
    ],
)
def test_index_costs_reach_facts(statement: str, name: str, expected: str) -> None:
    """Argüman metni olgulara kadar taşınır (`CallName.first_arg` → `known_cost`)."""
    costs = _costs(
        "using System.Collections.Generic;\nclass A { void F(List<int> xs) {\n"
        f"    {statement};\n}} }}\n",
        Language.CSHARP,
    )
    assert costs == {name: expected}
