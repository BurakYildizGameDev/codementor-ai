"""Olgu çıkarıcı testleri (mimari §5.3.1): fonksiyonlar, sıcak yol, derinlik, çağrılar,
tahsisler, özyineleme, motor sembolleri, uyarılar ve CLI.

Bölüm 2/2.
"""

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
)
from codementor.models.enums import AllocationKind, Engine, Language
from tests.unit.extractor_support import (
    CPP,
    CS,
    C,
    _facts,
)


def test_sibling_lambda_on_linq_line_is_still_a_closure() -> None:
    """Bastırma satır bazlı değil: aynı satırdaki LINQ dışı lambda tahsis sayılır (iş 5 dilim 3)."""
    text = (
        "using System;\n"
        "using System.Collections.Generic;\n"
        "using System.Linq;\n"
        "using UnityEngine;\n"
        "public class Radar : MonoBehaviour {\n"
        "    List<int> xs;\n"
        "    void Update() {\n"
        "        var q = xs.Where(v => v > 0); Action log = () => Debug.Log(1);\n"
        "        log();\n"
        "    }\n"
        "}\n"
    )
    facts = _facts(text, CS, Engine.UNITY)
    assert [(a.kind, a.line) for a in facts.allocations] == [
        (AllocationKind.CLOSURE, 8),
        (AllocationKind.LINQ, 8),
    ]


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
