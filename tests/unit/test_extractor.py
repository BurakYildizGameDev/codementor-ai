"""Olgu çıkarıcı testleri (mimari §5.3.1): fonksiyonlar, sıcak yol, derinlik, çağrılar,
tahsisler, özyineleme, motor sembolleri, uyarılar ve CLI."""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from codementor.analysis import extractor
from codementor.analysis.extractor import (
    FAILURE_WARNING,
    NO_FUNCTION_WARNING,
    SYNTAX_WARNING,
    extract_facts,
)
from codementor.ingest.normalize import normalize
from codementor.models.enums import AllocationKind, DeallocationKind, Engine, Language
from codementor.models.facts import CodeFacts
from codementor.models.request import LanguageHint

C, CPP, CS = Language.C, Language.CPP, Language.CSHARP


def _facts(text: str, language: Language, engine: Engine = Engine.NONE) -> CodeFacts:
    return extract_facts(normalize(text, LanguageHint(language=language, engine=engine)))


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
        (AllocationKind.CLOSURE, 12, 1, True),
        (AllocationKind.LINQ, 12, 1, True),
        (AllocationKind.CSHARP_NEW, 13, 1, True),
    ]
    assert all(a.function == "Update" for a in facts.allocations)


def test_long_string_chain_is_linear() -> None:
    body = " + ".join(['"a"'] * 3000)
    text = f"class A {{ void F() {{ var s = {body}; }} }}\n"
    start = time.perf_counter()
    facts = _facts(text, CS)
    assert time.perf_counter() - start < 2.0
    assert [a.kind for a in facts.allocations] == [AllocationKind.STRING_CONCAT]


# ------------------------------------------------------------------ özyineleme


def test_recursion_branching() -> None:
    text = "int fib(int n) {\n    if (n < 2) return n;\n    return fib(n - 1) + fib(n - 2);\n}\n"
    (rec,) = _facts(text, C).recursion
    assert (rec.function, rec.self_call_count, rec.branching_factor, rec.lines) == (
        "fib",
        2,
        2,
        [3],
    )
    assert not rec.halving


def test_recursion_exclusive_branches() -> None:
    text = (
        "int bs(int *a, int lo, int hi, int x) {\n"
        "    if (lo > hi) return -1;\n"
        "    int mid = lo + (hi - lo) / 2;\n"
        "    if (a[mid] < x) return bs(a, mid + 1, hi, x);\n"
        "    else return bs(a, lo, mid - 1, x);\n"
        "}\n"
    )
    (rec,) = _facts(text, C).recursion
    assert rec.self_call_count == 2
    assert rec.branching_factor == 1
    assert rec.halving


def test_recursion_ternary_and_csharp_member() -> None:
    text = "class A {\n  int F(int n) => n < 2 ? n : this.F(n - 1) + F(n - 2);\n}\n"
    (rec,) = _facts(text, CS).recursion
    assert rec.branching_factor == 2


def test_other_object_same_method_is_not_recursion() -> None:
    text = "class A { void Tick(B other) { other.Tick(null); } }\n"
    assert _facts(text, CS).recursion == []


@pytest.mark.parametrize(
    ("text", "language", "engine"),
    [
        ("void AFoo::BeginPlay() { Super::BeginPlay(); }\n", CPP, Engine.UNREAL),
        ("void Derived::Run() { Base::Run(); }\n", CPP, Engine.NONE),
        ("class A : B { override void Run() { base.Run(); } }\n", CS, Engine.NONE),
    ],
)
def test_parent_call_is_not_recursion(text: str, language: Language, engine: Engine) -> None:
    assert _facts(text, language, engine).recursion == []


def test_using_declaration_swap_is_not_recursion() -> None:
    """`using std::swap; swap(a.x, b.x);` ADL deyimi: çağrı std::swap'e gider."""
    text = (
        "struct B {\n"
        "  int x;\n"
        "  friend void swap(B& a, B& b) {\n"
        "    using std::swap;\n"
        "    swap(a.x, b.x);\n"
        "  }\n"
        "};\n"
    )
    assert _facts(text, CPP).recursion == []


def test_qualified_self_call_is_recursion() -> None:
    text = "int Math::Fact(int n) { return n < 2 ? 1 : n * Math::Fact(n - 1); }\n"
    (rec,) = _facts(text, CPP).recursion
    assert rec.function == "Math::Fact"


# ------------------------------------------------------------------ motor sembolleri


def test_engine_symbols_unity() -> None:
    text = (
        "using System;\nusing UnityEngine;\n"
        "public class P : MonoBehaviour {\n"
        "    public event Action OnDie;\n"
        "    public Action<int> OnScore;\n"
        "    Health health;\n"
        "    int total;\n"
        "    void OnEnable() {\n"
        "        health.OnDeath += HandleDeath;\n"
        "        OnDie += () => { };\n"
        "        OnScore += s => total += s;\n"
        "        total += 5;\n"
        "    }\n"
        "    void OnDisable() { health.OnDeath -= HandleDeath; }\n"
        "    void HandleDeath() { }\n"
        "}\n"
    )
    symbols = _facts(text, CS, Engine.UNITY).engine_symbols
    assert [(s.name, s.line) for s in symbols.event_subscriptions] == [
        ("health.OnDeath", 9),
        ("OnDie", 10),
        ("OnScore", 11),
    ]
    assert symbols.has_on_enable
    assert symbols.has_on_disable


def test_engine_symbols_unreal() -> None:
    text = (
        '#include "Enemy.h"\n'
        "UCLASS()\n"
        "class AEnemy : public AActor {\n"
        "    GENERATED_BODY()\n"
        "    UPROPERTY(EditAnywhere)\n"
        "    UStaticMeshComponent* Mesh;\n"
        "    UPROPERTY() TObjectPtr<AActor> Target;\n"
        "    AActor* Unsafe;\n"
        "    int32 Health = 100;\n"
        "};\n"
        "void AEnemy::BeginPlay() {\n"
        "    OnDestroyed.AddDynamic(this, &AEnemy::HandleDestroyed);\n"
        "}\n"
    )
    symbols = _facts(text, CPP, Engine.UNREAL).engine_symbols
    assert [(s.name, s.line) for s in symbols.uproperty_fields] == [("Mesh", 6), ("Target", 7)]
    assert [(s.name, s.line) for s in symbols.uobject_fields] == [
        ("Mesh", 6),
        ("Target", 7),
        ("Unsafe", 8),
    ]
    assert [(s.name, s.line) for s in symbols.event_subscriptions] == [("OnDestroyed", 12)]


def test_uproperty_inside_comment_ignored() -> None:
    text = "class AFoo : public AActor {\n    // UPROPERTY()\n    AActor* Raw;\n};\n"
    symbols = _facts(text, CPP, Engine.UNREAL).engine_symbols
    assert symbols.uproperty_fields == []


# ------------------------------------------------------------------ dayanıklılık


def test_syntax_error_warns_but_extracts() -> None:
    facts = _facts(
        "int f(int n) {\n    for (int i = 0; i < n; i++) {\n        x = ;\n    }\n}\n", C
    )
    assert SYNTAX_WARNING in facts.warnings
    assert facts.functions


def test_no_functions_warns() -> None:
    facts = _facts("int x = 1;\nint y = 2;\n", C)
    assert NO_FUNCTION_WARNING in facts.warnings
    assert facts.functions == []


@pytest.mark.parametrize(
    ("text", "language"),
    [
        ("class AFoo : public AActor {\n    void Tick(float Dt);\n};\n", CPP),
        ("struct point { int x; int y; };\n", C),
        ("interface IShape { double Area(); }\n", CS),
    ],
)
def test_declarations_only_is_not_warned(text: str, language: Language) -> None:
    assert _facts(text, language).warnings == []


def test_internal_error_returns_empty_facts(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("iç hata")

    monkeypatch.setattr(extractor, "captures", boom)
    facts = _facts("int f(void) { return 0; }\n", C)
    assert facts.functions == []
    assert facts.warnings == [FAILURE_WARNING.format("RuntimeError")]


def test_missing_call_costs_file_is_not_fatal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from codementor.config import load_settings

    settings = load_settings(data={"call_costs_file": tmp_path / "yok.yaml"})
    monkeypatch.setattr(extractor, "get_settings", lambda: settings)
    facts = _facts("int f(void) { return 0; }\n", C)
    assert [f.name for f in facts.functions] == ["f"]  # olgular silinmez
    assert facts.warnings == [extractor.COSTS_WARNING]


def test_deep_nesting_is_fast_and_safe() -> None:
    depth = 1300  # ~40 KB sınırına yakın
    body = "for (int i = 0; i < n; i++) {" * depth + "}" * depth
    text = f"void f(int n) {{ {body} }}\n"
    start = time.perf_counter()
    facts = _facts(text, C)
    assert time.perf_counter() - start < 3.0
    assert max(lp.depth for lp in facts.loops) == depth


def test_many_loops_is_linear() -> None:
    body = " ".join("while (i < n) { i++; }" for _ in range(1500))  # 600 satır sınırı
    text = f"void f(int n) {{ int i = 0;\n{body}\n}}\n"
    start = time.perf_counter()
    facts = _facts(text, C)
    assert time.perf_counter() - start < 3.0
    assert len(facts.loops) == 1500


# ------------------------------------------------------------------ CLI


def test_cli_main(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "code.c"
    source.write_text("int f(int n) { return n; }\n", encoding="utf-8")
    assert extractor.main([str(source)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["facts"]["functions"][0]["name"] == "f"
    assert out["hint"]["value"] == "1"
    assert set(out["function_hints"]) == {"f"}


def test_cli_main_bad_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert extractor.main([str(tmp_path / "yok.c")]) == 2
    assert "okunamadı" in capsys.readouterr().err


def test_cli_writes_utf8_on_legacy_console(tmp_path: Path) -> None:
    """Windows konsolu (cp1254) `→`/`ı` basamazdı; çıktı her zaman UTF-8 bayt."""
    import os
    import subprocess
    import sys

    source = tmp_path / "code.c"
    source.write_text("int f(int n) { for (int i = 0; i < n; i++) {} return n; }\n", "utf-8")
    env = {**os.environ, "PYTHONIOENCODING": "cp1254"}
    result = subprocess.run(
        [sys.executable, "-m", "codementor.analysis.extractor", str(source)],
        capture_output=True,
        env=env,
        check=False,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", "replace")
    out = json.loads(result.stdout.decode("utf-8"))
    assert "→" in out["hint"]["basis"][0]


# ------------------------------------------------------------------ Faz 21: sınıf tabanı, struct


def test_hot_path_requires_base_class_unity() -> None:
    """Tabanı olmayan sınıftaki `Update` Unity çağırmaz; kullanıcı tabanı varsa sıcak kalır."""
    text = (
        "using UnityEngine;\n"
        "public class Mover : MonoBehaviour { void Update() { } }\n"
        "public class Plain { void Update() { } }\n"
        "public struct Data { void Update() { } }\n"
        "public class Enemy : BaseEnemy { void Update() { } }\n"
        "public class Outer : MonoBehaviour { class Inner { void LateUpdate() { } } }\n"
    )
    facts = _facts(text, CS, Engine.UNITY)
    hot = [(f.line_start, f.is_hot_path) for f in facts.functions]
    assert hot == [(2, True), (3, False), (4, False), (5, True), (6, False)]


def test_unreal_tick_in_plain_class_not_hot() -> None:
    text = (
        "class FHelper { void Tick(float Dt) { } };\n"
        "class AMine : public AActor { void Tick(float Dt) override { } };\n"
    )
    facts = _facts(text, CPP, Engine.UNREAL)
    assert [f.is_hot_path for f in facts.functions] == [False, True]


def test_out_of_class_unreal_tick_still_hot() -> None:
    facts = _facts("void AFoo::Tick(float Dt)\n{\n}\n", CPP, Engine.UNREAL)
    assert facts.functions[0].is_hot_path


def test_user_struct_new_is_not_heap_allocation() -> None:
    text = (
        "using UnityEngine;\n"
        "public struct Hit { public Hit(int d) { } }\n"
        "public readonly record struct Point(int X);\n"
        "public class P : MonoBehaviour {\n"
        "    void Update() { var h = new Hit(3); var p = new Point(1); var l = new Ref(); }\n"
        "}\n"
        "public class Ref { }\n"
    )
    facts = _facts(text, CS, Engine.UNITY)
    assert [(a.kind, a.line) for a in facts.allocations] == [(AllocationKind.CSHARP_NEW, 5)]


def test_partial_class_part_without_base_stays_hot() -> None:
    """Denetim O2: `partial` sınıfın tabanı başka bir parçada (başka dosyada da olabilir)."""
    text = (
        "using UnityEngine;\n"
        "public partial class P : MonoBehaviour { }\n"
        "public partial class P { void Update() { } }\n"
    )
    facts = _facts(text, CS, Engine.UNITY)
    assert facts.functions[0].is_hot_path


def test_unreal_uclass_macro_class_tick_hot() -> None:
    text = (
        "UCLASS()\nclass MYGAME_API AMine : public AActor\n{\n    GENERATED_BODY()\n"
        "    void Tick(float Dt) override { }\n};\n"
    )
    facts = _facts(text, CPP, Engine.UNREAL)
    assert facts.functions[0].is_hot_path
