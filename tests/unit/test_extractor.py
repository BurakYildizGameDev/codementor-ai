"""Olgu çıkarıcı testleri (mimari §5.3.1): fonksiyonlar, sıcak yol, derinlik, çağrılar,
tahsisler, özyineleme, motor sembolleri, uyarılar ve CLI.

Bölüm 1/2.
"""

from __future__ import annotations

import pytest

from codementor.models.enums import AllocationKind, DeallocationKind, Engine
from tests.unit.extractor_support import (
    CPP,
    CS,
    C,
    _call_names,
    _facts,
)


def test_first_argument_text_is_captured() -> None:
    """İndeks desenlerini ayırt etmek için ilk argümanın metni taşınır."""
    names = _call_names("void F() { xs.RemoveAt(xs.Count - 1); xs.Insert(0, y); }", CS)
    assert [(n.method, n.first_arg) for n in names] == [
        ("RemoveAt", "xs.Count - 1"),
        ("Insert", "0"),
    ]


def test_argumentless_call_has_no_first_argument() -> None:
    (name,) = _call_names("void F() { xs.Clear(); }", CS)
    assert name.first_arg is None
    assert name.arg_count == 0


def test_long_first_argument_is_not_read() -> None:
    """Kullanıcı koduna bağlı ölçek: çok uzun argüman metni okunmaz (mimari §12)."""
    names = _call_names("void F() { g(" + "a + " * 100 + "b); }", C)
    assert names[0].method == "g"
    assert names[0].first_arg == "…"


# ------------------------------------------------------------------ fonksiyonlar ve sıcak yol


@pytest.mark.parametrize("name", ["Update", "FixedUpdate", "LateUpdate", "OnGUI"])
def test_hot_path_unity(name: str) -> None:
    text = (
        "using UnityEngine;\n"
        "public class P : MonoBehaviour {\n"
        f"    void {name}() {{ }}\n"
        "    void Start() { }\n"
        "    void Helper() { }\n"
        "}\n"
    )
    facts = _facts(text, CS, Engine.UNITY)
    by_name = {f.name: f for f in facts.functions}
    assert by_name[name].is_hot_path
    assert by_name[name].lifecycle == name
    assert by_name["Start"].lifecycle == "Start"
    assert not by_name["Start"].is_hot_path
    assert by_name["Helper"].lifecycle is None


@pytest.mark.parametrize(
    ("signature", "name"),
    [
        ("void AFoo::Tick(float DeltaTime)", "AFoo::Tick"),
        (
            "void UHealth::TickComponent(float Dt, ELevelTick T, FActorComponentTickFunction* F)",
            "UHealth::TickComponent",
        ),
    ],
)
def test_hot_path_unreal(signature: str, name: str) -> None:
    text = f'#include "Foo.h"\n{signature}\n{{\n    Super::Tick(1.0f);\n}}\n'
    facts = _facts(text, CPP, Engine.UNREAL)
    (fn,) = facts.functions
    assert fn.name == name
    assert fn.is_hot_path
    assert fn.lifecycle == name.split("::")[-1]


def test_plain_csharp_update_is_not_hot() -> None:
    facts = _facts("class A { void Update() { } }\n", CS)
    assert not facts.functions[0].is_hot_path


def test_function_lines_and_parameters() -> None:
    text = "int add(int a, int *b)\n{\n    return a + *b;\n}\n"
    (fn,) = _facts(text, C).functions
    assert (fn.name, fn.line_start, fn.line_end, fn.parameters) == ("add", 1, 4, ["a", "b"])


def test_csharp_parameters() -> None:
    (fn,) = _facts("class A { int F(int n, List<int> xs) { return n; } }\n", CS).functions
    assert fn.parameters == ["n", "xs"]


# ------------------------------------------------------------------ derinlik


def test_nested_depth_and_parent() -> None:
    text = (
        "void f(int n) {\n"
        "    for (int i = 0; i < n; i++) {\n"
        "        for (int j = 0; j < n; j++) {\n"
        "            while (n > 0) { n /= 2; }\n"
        "        }\n"
        "    }\n"
        "    for (int k = 0; k < 10; k++) {}\n"
        "}\n"
    )
    loops = _facts(text, C).loops
    assert [(lp.line, lp.depth, lp.parent_line) for lp in loops] == [
        (2, 1, None),
        (3, 2, 2),
        (4, 3, 3),
        (7, 1, None),
    ]
    assert all(lp.function == "f" for lp in loops)


def test_loop_depth_resets_in_nested_function() -> None:
    text = (
        "class A {\n"
        "  void F(List<int> xs) {\n"
        "    foreach (var x in xs) {\n"
        "      int G(int y) { for (int i = 0; i < y; i++) {} return y; }\n"
        "    }\n"
        "  }\n"
        "}\n"
    )
    loops = _facts(text, CS).loops
    assert [(lp.function, lp.depth) for lp in loops] == [("F", 1), ("G", 1)]


def test_call_loop_depth() -> None:
    text = (
        "#include <string.h>\n"
        "void f(char **s, int n) {\n"
        "    puts(s[0]);\n"
        "    for (int i = 0; i < n; i++) {\n"
        "        for (int j = 0; j < strlen(s[i]); j++) {\n"
        "            putchar(s[i][j]);\n"
        "        }\n"
        "    }\n"
        "}\n"
    )
    calls = {(c.name, c.line): c for c in _facts(text, C).calls}
    assert calls[("puts", 3)].loop_depth == 0
    assert calls[("puts", 3)].loop_line is None
    assert calls[("strlen", 5)].loop_depth == 2
    assert calls[("strlen", 5)].known_cost == "n"
    assert calls[("putchar", 6)].loop_depth == 2
    assert calls[("putchar", 6)].loop_line == 5
    assert calls[("putchar", 6)].known_cost is None


def test_two_pointer_counter_outer() -> None:
    text = (
        "int f(int *a, int n, int k) {\n"
        "    int j = 0, best = 0;\n"
        "    for (int i = 0; i < n; i++) {\n"
        "        while (j < n && a[j] - a[i] <= k) { j++; }\n"
        "        for (int m = 0; m < n; m++) {}\n"
        "        int r = 0;\n"
        "        while (r < n) { r++; }\n"
        "    }\n"
        "    return best;\n"
        "}\n"
    )
    loops = _facts(text, C).loops
    assert [(lp.line, lp.counter_outer) for lp in loops] == [
        (3, False),
        (4, True),
        (5, False),
        (7, False),
    ]


# ------------------------------------------------------------------ çağrı adları ve maliyetler


def test_call_costs_resolved_by_declared_type() -> None:
    text = (
        "#include <map>\n#include <vector>\n#include <algorithm>\n"
        "using namespace std;\n"
        "void f(vector<int>& v, std::map<int, int> m) {\n"
        "    sort(v.begin(), v.end());\n"
        "    std::find(v.begin(), v.end(), 3);\n"
        "    v.push_back(1);\n"
        "    m.find(2);\n"
        "    unknown.find(2);\n"
        "}\n"
    )
    calls = {(c.line, c.name): c.known_cost for c in _facts(text, CPP).calls}
    assert calls[(6, "std::sort")] == "n log n"
    assert calls[(6, "v.begin")] is None
    assert calls[(7, "std::find")] == "n"
    assert calls[(8, "std::vector::push_back")] == "1*"
    assert calls[(9, "std::map::find")] == "log n"
    assert calls[(10, "unknown.find")] is None


def test_csharp_call_costs() -> None:
    text = (
        "using System.Linq;\n"
        "class A {\n"
        "  void F(List<int> list, int[] arr) {\n"
        "    var d = new Dictionary<int, int>();\n"
        "    list.Contains(3);\n"
        "    d.ContainsKey(1);\n"
        "    Array.Sort(arr);\n"
        "    list.Where(x => x > 0).ToList();\n"
        '    GameObject.Find("Player");\n'
        "  }\n"
        "}\n"
    )
    calls = {(c.name, c.known_cost) for c in _facts(text, CS).calls}
    assert ("List.Contains", "n") in calls
    assert ("Dictionary.ContainsKey", "1*") in calls
    assert ("Array.Sort", "n log n") in calls
    assert ("Enumerable.Where", "n") in calls
    assert ("Enumerable.ToList", "n") in calls
    assert ("GameObject.Find", "n") in calls


def test_linq_requires_using() -> None:
    text = "class A { void F(List<int> xs) { xs.Where(x => x > 0); } }\n"
    (call,) = _facts(text, CS).calls
    assert call.known_cost is None


def test_ambiguous_type_is_not_resolved() -> None:
    text = (
        "#include <map>\n#include <unordered_map>\n"
        "void f() { std::map<int,int> m; m.find(1); }\n"
        "void g() { std::unordered_map<int,int> m; m.find(1); }\n"
    )
    assert all(c.known_cost is None for c in _facts(text, CPP).calls)


# ------------------------------------------------------------------ tahsisler


def test_allocations_c() -> None:
    text = (
        "#include <stdlib.h>\n"
        "void f(int n) {\n"
        "    int *a = malloc(n);\n"
        "    int *b = calloc(n, 4);\n"
        "    a = realloc(a, 2 * n);\n"
        "    free(a);\n"
        "    free(b);\n"
        "}\n"
    )
    facts = _facts(text, C)
    assert [(a.kind, a.line) for a in facts.allocations] == [
        (AllocationKind.MALLOC, 3),
        (AllocationKind.CALLOC, 4),
        (AllocationKind.REALLOC, 5),
    ]
    assert [(d.kind, d.line) for d in facts.deallocations] == [
        (DeallocationKind.FREE, 6),
        (DeallocationKind.FREE, 7),
    ]


def test_allocations_cpp() -> None:
    text = (
        "#include <memory>\n#include <string>\n"
        "void f(int n, std::string s) {\n"
        "    int *a = new int[n];\n"
        "    auto *p = new Point();\n"
        "    auto u = std::make_unique<Point>();\n"
        "    auto sh = std::make_shared<Point>();\n"
        "    auto l = [&](int x) { return x + n; };\n"
        '    std::string t = s + "!" + "?";\n'
        "    delete p;\n"
        "    delete[] a;\n"
        "}\n"
    )
    facts = _facts(text, CPP)
    assert [(a.kind, a.line) for a in facts.allocations] == [
        (AllocationKind.NEW_ARRAY, 4),
        (AllocationKind.NEW, 5),
        (AllocationKind.MAKE_UNIQUE, 6),
        (AllocationKind.MAKE_SHARED, 7),
        (AllocationKind.CLOSURE, 8),
        (AllocationKind.STRING_CONCAT, 9),
    ]
    assert [(d.kind, d.line) for d in facts.deallocations] == [
        (DeallocationKind.DELETE, 10),
        (DeallocationKind.DELETE_ARRAY, 11),
    ]


def test_allocations_csharp_hot_path_and_loop_depth() -> None:
    text = (
        "using System.Linq;\n"
        "using UnityEngine;\n"
        "public class P : MonoBehaviour {\n"
        "    List<int> xs; string label;\n"
        "    void Update() {\n"
        "        var v = new Vector3(1, 2, 3);\n"
        "        foreach (var x in xs) {\n"
        "            var l = new List<int>();\n"
        '            label = "Score: " + x;\n'
        '            label += "!";\n'
        '            Debug.Log($"x={x}");\n'
        "            var q = xs.Where(y => y > x);\n"
        "            var arr = new int[3];\n"
        "        }\n"
        "    }\n"
        "}\n"
    )
    facts = _facts(text, CS, Engine.UNITY)
    kinds = [(a.kind, a.line, a.loop_depth, a.in_hot_path) for a in facts.allocations]
    assert (AllocationKind.CSHARP_NEW, 6, 0, True) not in kinds  # Vector3 değer tipi
    assert kinds == [
        (AllocationKind.CSHARP_NEW, 8, 1, True),
        (AllocationKind.STRING_CONCAT, 9, 1, True),
        (AllocationKind.STRING_CONCAT, 10, 1, True),
        (AllocationKind.STRING_CONCAT, 11, 1, True),
        # LINQ lambda'sının closure'ı ayrı tahsis değil: LINQ çağrısının parçası (iş 5 dilim 3)
        (AllocationKind.LINQ, 12, 1, True),
        (AllocationKind.CSHARP_NEW, 13, 1, True),
    ]
    assert all(a.function == "Update" for a in facts.allocations)
