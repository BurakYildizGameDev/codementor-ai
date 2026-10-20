"""Faz 5 kod denetimi (kod-denetci) regresyon testleri.

Her test bir denetim bulgusunu sabitler (Y = yüksek, O = orta, D = düşük).
"""

from __future__ import annotations

import time
from collections.abc import Callable

import pytest

from codementor.analysis.complexity_hint import compute_hint, function_hints
from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize
from codementor.models.enums import AllocationKind, Engine, Language, LoopBound
from codementor.models.facts import CodeFacts
from codementor.models.request import LanguageHint
from tests.timing import deadline as _deadline

C, CPP, CS = Language.C, Language.CPP, Language.CSHARP


def _facts(text: str, language: Language, engine: Engine = Engine.NONE) -> CodeFacts:
    return extract_facts(normalize(text, LanguageHint(language=language, engine=engine)))


def _bound(body: str, language: Language = C) -> LoopBound:
    facts = _facts(f"void f(int n, int *a, int x) {{ int s = 0;\n{body}\n}}\n", language)
    return facts.loops[0].bound


# ------------------------------------------------------------------ Y1: rastgele /2 LOG değil


@pytest.mark.parametrize(
    "body",
    [
        "int i = 0; while (i < n) { s += a[i] / 2; i++; }",
        "for (int i = 0; i < n;) { s += a[i] >> 1; i++; }",
        "int lo = 0, hi = n; while (lo < hi) { s += a[lo] / 2; lo++; }",
    ],
)
def test_unrelated_halving_is_not_log(body: str) -> None:
    assert _bound(body) is LoopBound.LINEAR


# ------------------------------------------------------------------ Y2: yön güncellemeden


@pytest.mark.parametrize(
    "body",
    [
        "for (int i = n; i != 0; i--) {}",
        "while (n != 0) { n--; }",
        "for (int i = -n; i < 0; i++) {}",
        "int i = x; while (i < 10) { i++; }",
    ],
)
def test_non_constant_start_is_not_constant(body: str) -> None:
    assert _bound(body) is LoopBound.LINEAR


def test_mixed_directions_unknown() -> None:
    assert _bound("int i = 0; while (i < n) { i++; if (a[i]) i--; }") is LoopBound.UNKNOWN


# ------------------------------------------------------------------ O8: gövdede sayaç değişimi


@pytest.mark.parametrize(
    "body",
    [
        "for (int i = 1; i < n; i++) { i *= 2; }",
        "for (int i = 0; i < n; i++) { if (x) i = 0; }",
    ],
)
def test_body_counter_change_is_unknown(body: str) -> None:
    assert _bound(body) is LoopBound.UNKNOWN


def test_body_skip_increment_stays_linear() -> None:
    assert _bound("for (int i = 0; i < n; i++) { if (a[i]) i++; }") is LoopBound.LINEAR


# ------------------------------------------------------------ Y3: LINQ yalnızca koleksiyonlarda

UNITY_Y3 = (
    "using System.Collections.Generic;\n"
    "using System.Linq;\n"
    "using UnityEngine;\n"
    "public class P : MonoBehaviour {\n"
    "    private List<int> items = new List<int>();\n"
    "    private HashSet<int> Seen { get; } = new HashSet<int>();\n"
    "    private int[] arr;\n"
    "    void Update() {\n"
    "        int m = 0;\n"
    "        for (int i = 0; i < items.Count; i++) {\n"
    "            m = Mathf.Max(m, items[i]);\n"
    "            if (Seen.Contains(i)) m++;\n"
    "            m += items.First();\n"
    "        }\n"
    "        var big = items.Where(v => v > m).ToList();\n"
    "        bool has = arr.Contains(3);\n"
    "    }\n"
    "}\n"
)


def test_static_math_is_not_linq() -> None:
    facts = _facts(UNITY_Y3, CS, Engine.UNITY)
    calls = {c.line: (c.name, c.known_cost) for c in facts.calls if c.line in (11, 12, 13)}
    assert calls[11] == ("Mathf.Max", None)
    assert calls[12] == ("HashSet.Contains", "1*")  # property tipi tabloda
    assert calls[13] == ("Enumerable.First", "1")  # argümansız First O(1)
    linq_lines = {a.line for a in facts.allocations if a.kind is AllocationKind.LINQ}
    assert linq_lines == {15, 16}
    assert compute_hint(facts).value == "n"


def test_linq_chain_and_array_still_resolved() -> None:
    facts = _facts(UNITY_Y3, CS, Engine.UNITY)
    names = {(c.line, c.name, c.known_cost) for c in facts.calls}
    assert (15, "Enumerable.Where", "n") in names
    assert (15, "Enumerable.ToList", "n") in names
    assert (16, "Enumerable.Contains", "n") in names


# ------------------------------------------------------------------ Y4: karşılıklı özyineleme


def test_mutual_recursion_is_low_confidence() -> None:
    text = (
        "int is_even(int n) { return n == 0 ? 1 : is_odd(n - 1); }\n"
        "int is_odd(int n) { return n == 0 ? 0 : is_even(n - 1); }\n"
    )
    hint = compute_hint(_facts(text, C))
    assert hint.confidence == "low"
    assert any("karşılıklı" in b for b in hint.basis)


def test_mutual_branching_recursion_is_exponential_suspect() -> None:
    text = (
        "int a(int n) { return n < 2 ? n : b(n - 1) + b(n - 2); }\nint b(int n) { return a(n); }\n"
    )
    hint = compute_hint(_facts(text, C))
    assert hint.exponential_suspect
    assert hint.confidence == "low"


# ------------------------------------------------------------------ Y5 / O5: üstel şüphe


def test_mid_argument_does_not_hide_exponential() -> None:
    text = "int f(int n, int mid) { return n < 2 ? n : f(n - 1, mid) + f(n - 2, mid); }\n"
    facts = _facts(text, C)
    assert not facts.recursion[0].halving
    assert compute_hint(facts).exponential_suspect


def test_self_call_in_loop_is_branching() -> None:
    text = (
        "void p(int *a, int k, int n) {\n"
        "    if (k == n) return;\n"
        "    for (int i = k; i < n; i++) { p(a, k + 1, n); }\n"
        "}\n"
    )
    facts = _facts(text, C)
    assert facts.recursion[0].branching_factor >= 2
    assert compute_hint(facts).exponential_suspect


def test_merge_sort_still_divide_and_conquer() -> None:
    text = (
        "void ms(int *a, int lo, int hi) {\n"
        "    if (lo >= hi) return;\n"
        "    int mid = (lo + hi) / 2;\n"
        "    ms(a, lo, mid);\n"
        "    ms(a, mid + 1, hi);\n"
        "}\n"
    )
    facts = _facts(text, C)
    assert facts.recursion[0].halving
    assert not compute_hint(facts).exponential_suspect


# ------------------------------------------------------------ Y6: kısmi hata tüm olguları silmez


def test_deep_condition_chain_does_not_drop_facts() -> None:
    chain = " && ".join(["i < n"] * 4000)
    facts = _facts(f"int f(int n) {{ for (int i = 0; {chain}; i++) {{}} return n; }}\n", C)
    assert facts.functions
    assert facts.loops
    assert facts.loops[0].bound is LoopBound.LINEAR  # yinelemeli ayrıştırma: sınır yok
    assert not any("çıkarılamadı" in w for w in facts.warnings)


def test_missing_cost_table_keeps_facts(tmp_path: object, monkeypatch: pytest.MonkeyPatch) -> None:
    from pathlib import Path

    from codementor.analysis import extractor
    from codementor.config import load_settings

    assert isinstance(tmp_path, Path)
    settings = load_settings(data={"call_costs_file": tmp_path / "yok.yaml"})
    monkeypatch.setattr(extractor, "get_settings", lambda: settings)
    facts = _facts("int f(int n) { for (int i = 0; i < n; i++) {} return strlen(0); }\n", C)
    assert facts.functions
    assert facts.loops
    assert facts.calls[0].known_cost is None
    assert any("maliyet" in w for w in facts.warnings)


def test_section_failure_is_isolated(monkeypatch: pytest.MonkeyPatch) -> None:
    from codementor.analysis import _engine

    def boom(**_kwargs: object) -> object:
        raise RuntimeError("motor")

    monkeypatch.setattr(_engine, "engine_symbols", boom)
    facts = _facts("int f(int n) { for (int i = 0; i < n; i++) {} return n; }\n", C)
    assert facts.functions
    assert facts.loops
    assert any("RuntimeError" in w for w in facts.warnings)


# ------------------------------------------------------------------ O1-O4: doğrusal süre
#
# Süre iddiaları iki katmanlıdır (KALAN_ISLER.md iş 4b):
#   1. **Göreli büyüme** — girdi iki katına çıkınca süre en çok `_GROWTH_LIMIT` kat artar; makine
#      yükünden bağımsız olduğu için asıl gerileme dedektörü (doğrusal ≈2×, karesel ≈4×).
#   2. **Mutlak bütçe** — 1,5 s (ADR-0024). Yük altında tepe gecikmesi `_best_of` ile elenir:
#      her ölçüm ısınma + `_RUNS` koşunun en hızlısıdır (tek koşu tam suite yükünde 0,76 → 1,10 s
#      görüp eşiği bir kez aşmıştı).

_RUNS = 3
_GROWTH_LIMIT = 3.0  # 2× girdi: doğrusal ≈2×, karesel ≈4×
_TIME_FLOOR = 0.02  # çok kısa ölçümlerde oran gürültüsünü engeller


def _best_of(run: Callable[[], None]) -> float:
    """Isınma + `_RUNS` koşunun en hızlısı (saniye)."""
    run()
    best = float("inf")
    for _ in range(_RUNS):
        start = time.perf_counter()
        run()
        best = min(best, time.perf_counter() - start)
    return best


def _timed(text: str, language: Language) -> float:
    code = normalize(text, LanguageHint(language=language))
    return _best_of(lambda: compute_hint(extract_facts(code)))


def _inner_loops(count: int) -> str:
    inner = " ".join(["while (j < n) j++;"] * count)
    return f"void f(int n) {{ int j = 0; for (int i = 0; i < n; i++) {{ {inner} }} }}\n"


def _functions(count: int) -> str:
    return " ".join(f"void f{i}(void) {{ f{i + 1}(); }}" for i in range(count)) + "\n"


def _member_chain(count: int) -> str:
    return f"void f(void) {{ {'x' + '.g()' * count}; }}\n"


def _concat_chain(count: int) -> str:
    chain = " + ".join(['"a"'] * count)  # < 40 KB
    return f"class A {{ void F() {{ var s = {chain}; }} }}\n"


def test_o1_many_inner_loops_linear() -> None:
    assert _timed(_inner_loops(2000), C) < _deadline(1.5)


def test_o1_growth_is_linear() -> None:
    small, large = (_timed(_inner_loops(count), C) for count in (1000, 2000))
    assert large <= _GROWTH_LIMIT * max(small, _TIME_FLOOR), f"{small:.3f} s → {large:.3f} s"


def test_o2_many_functions_linear() -> None:
    assert _timed(_functions(1300), C) < _deadline(1.5)


def test_o2_growth_is_linear() -> None:
    small, large = (_timed(_functions(count), C) for count in (650, 1300))
    assert large <= _GROWTH_LIMIT * max(small, _TIME_FLOOR), f"{small:.3f} s → {large:.3f} s"


def test_o3_long_member_chain_linear() -> None:
    assert _timed(_member_chain(7000), CPP) < _deadline(1.5)


def test_o3_member_chain_growth_is_linear() -> None:
    small, large = (_timed(_member_chain(count), CPP) for count in (3500, 7000))
    assert large <= _GROWTH_LIMIT * max(small, _TIME_FLOOR), f"{small:.3f} s → {large:.3f} s"


def test_o3_long_concat_chain_linear() -> None:
    assert _timed(_concat_chain(6000), CS) < _deadline(1.5)


def test_o3_concat_chain_growth_is_linear() -> None:
    small, large = (_timed(_concat_chain(count), CS) for count in (3000, 6000))
    assert large <= _GROWTH_LIMIT * max(small, _TIME_FLOOR), f"{small:.3f} s → {large:.3f} s"


def test_o4_long_call_chain_keeps_hint() -> None:
    n = 600
    functions = [f"void f{i}(int n) {{ f{i + 1}(n); }}" for i in range(n)]
    functions.append(f"void f{n}(int n) {{ for (int i = 0; i < n; i++) {{}} }}")
    facts = _facts(" ".join(functions) + "\n", C)
    hints = function_hints(facts)
    assert hints["f0"].value == "n"
    assert compute_hint(facts).value == "n"


# ------------------------------------------------------------------ O6 / O7


def test_user_function_shadows_std_table() -> None:
    text = (
        "#include <algorithm>\nusing namespace std;\n"
        "int count(int x) { return x + 1; }\n"
        "int f(int n) { int s = 0; for (int i = 0; i < n; i++) s += count(i); return s; }\n"
    )
    facts = _facts(text, CPP)
    call = next(c for c in facts.calls if c.function == "f")
    assert call.known_cost is None
    assert compute_hint(facts).value == "n"


def test_uobject_fields_exclude_methods_and_char_pointers() -> None:
    text = (
        "class AFoo : public AActor {\n"
        "    AActor* GetTarget() const;\n"
        "    UObject* MakeThing();\n"
        "    ANSICHAR* RawName;\n"
        "    UObject* Owner;\n"
        "};\n"
    )
    symbols = _facts(text, CPP, Engine.UNREAL).engine_symbols
    assert [(s.name, s.line) for s in symbols.uobject_fields] == [("Owner", 5)]


# ------------------------------------------------------------------ düşük önemli bulgular


def test_unity_add_listener_is_subscription() -> None:
    text = (
        "using UnityEngine;\n"
        "public class P : MonoBehaviour {\n"
        "    public Button button;\n"
        "    void OnEnable() { button.onClick.AddListener(Clicked); }\n"
        "    void Clicked() { }\n"
        "}\n"
    )
    symbols = _facts(text, CS, Engine.UNITY).engine_symbols
    assert [(s.name, s.line) for s in symbols.event_subscriptions] == [("button.onClick", 4)]


def test_cpp_string_append_assign_is_concat() -> None:
    text = (
        "#include <string>\n"
        'void f(std::string& s, int n) { for (int i = 0; i < n; i++) s += "x"; }\n'
    )
    kinds = [a.kind for a in _facts(text, CPP).allocations]
    assert kinds == [AllocationKind.STRING_CONCAT]


def test_callee_choice_uses_big_o_order() -> None:
    text = (
        "void cheap(int n) { for (int i = 0; i < n; i *= 2) {} }\n"
        "void cheap(int n, int m) { for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) {} }\n"
        "void f(int n) { for (int i = 0; i < n; i++) cheap(n); }\n"
    )
    hints = function_hints(_facts(text, CPP))
    assert hints["f"].value == "n^3"
