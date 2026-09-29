"""Karmaşıklık ipucu testleri (mimari §5.3.2).

Fixture'lar `tests/fixtures/complexity/`; ilk satır beklentiyi taşır:
`// expect-hint: <Big-O> | <low|medium|high> [| exponential]`.
Two-pointer fixture'ında ipucunun YANILMASI beklenir (n^2, düşük güven).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.analysis.complexity_hint import compute_hint, function_hints
from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize
from codementor.models.bigo import parse_bigo
from codementor.models.enums import Engine, Language, LoopBound
from codementor.models.facts import (
    CallFact,
    CodeFacts,
    ComplexityHint,
    FunctionFact,
    LoopFact,
    RecursionFact,
)
from codementor.models.request import LanguageHint

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "complexity"
_SUFFIX = {".c": Language.C, ".cpp": Language.CPP, ".cs": Language.CSHARP}
CASES = sorted(FIXTURES.iterdir())


def _expectation(path: Path) -> tuple[str, str, bool]:
    header = path.read_text(encoding="utf-8").splitlines()[0]
    parts = [p.strip() for p in header.split("expect-hint:", 1)[1].split("|")]
    return parse_bigo(parts[0]).canonical, parts[1], "exponential" in parts[2:]


def _hint(path: Path) -> ComplexityHint:
    hint = LanguageHint(language=_SUFFIX[path.suffix], engine=Engine.NONE)
    facts = extract_facts(normalize(path.read_bytes(), hint))
    assert not facts.warnings, facts.warnings
    return compute_hint(facts)


def test_required_cases_exist() -> None:
    names = {p.stem for p in CASES}
    required = {
        "o1_constant",
        "ologn_binary_search",
        "on_linear_sum",
        "onlogn_sort_then_loop",
        "on2_nested",
        "on2_list_contains",
        "exp_fibonacci",
        "two_pointer",
    }
    assert required <= names


@pytest.mark.parametrize("path", CASES, ids=[p.name for p in CASES])
def test_fixture_hint(path: Path) -> None:
    value, confidence, exponential = _expectation(path)
    hint = _hint(path)
    assert (hint.value, hint.confidence, hint.exponential_suspect) == (
        value,
        confidence,
        exponential,
    ), hint.basis
    assert hint.basis, "ipucu gerekçesiz olmamalı"


def test_two_pointer_is_known_miss_with_low_confidence() -> None:
    hint = _hint(FIXTURES / "two_pointer.cpp")
    assert hint.value == "n^2"  # gerçek: O(n) — ipucu yanılıyor ve bunu biliyor
    assert hint.confidence == "low"
    assert any("sıfırlanmıyor" in b for b in hint.basis)


# ------------------------------------------------------------------ olgulardan doğrudan


def _loop(line: int, bound: LoopBound, parent: int | None = None, fn: str = "f") -> LoopFact:
    depth = 1 if parent is None else 2
    return LoopFact(
        kind="for", line=line, depth=depth, bound=bound, function=fn, parent_line=parent
    )


def _fn(name: str = "f") -> FunctionFact:
    return FunctionFact(name=name, line_start=1, line_end=50)


def test_empty_facts_low_confidence() -> None:
    hint = compute_hint(CodeFacts())
    assert (hint.value, hint.confidence) == ("1", "low")
    assert hint.basis


def test_linear_times_log() -> None:
    facts = CodeFacts(
        functions=[_fn()],
        loops=[_loop(2, LoopBound.LINEAR), _loop(3, LoopBound.LOG, parent=2)],
    )
    hint = compute_hint(facts)
    assert (hint.value, hint.confidence) == ("n log n", "high")
    assert hint.function == "f"


def test_constant_loops_do_not_multiply() -> None:
    facts = CodeFacts(
        functions=[_fn()],
        loops=[_loop(2, LoopBound.CONSTANT), _loop(3, LoopBound.LINEAR, parent=2)],
    )
    assert compute_hint(facts).value == "n"


def test_unknown_loop_assumed_linear_with_low_confidence() -> None:
    facts = CodeFacts(functions=[_fn()], loops=[_loop(2, LoopBound.UNKNOWN)])
    hint = compute_hint(facts)
    assert (hint.value, hint.confidence) == ("n", "low")
    assert any("varsayıldı" in b for b in hint.basis)


def test_unknown_loop_off_dominant_path_keeps_confidence() -> None:
    facts = CodeFacts(
        functions=[_fn()],
        loops=[
            _loop(2, LoopBound.LINEAR),
            _loop(3, LoopBound.LINEAR, parent=2),
            _loop(9, LoopBound.UNKNOWN),
        ],
    )
    hint = compute_hint(facts)
    assert (hint.value, hint.confidence) == ("n^2", "high")


def test_amortized_call_in_loop_is_medium() -> None:
    facts = CodeFacts(
        functions=[_fn()],
        loops=[_loop(2, LoopBound.LINEAR)],
        calls=[
            CallFact(
                name="List.Add", line=3, loop_depth=1, known_cost="1*", function="f", loop_line=2
            )
        ],
    )
    assert (compute_hint(facts).value, compute_hint(facts).confidence) == ("n", "medium")


def test_known_cost_outside_loop() -> None:
    facts = CodeFacts(
        functions=[_fn()],
        calls=[
            CallFact(name="std::sort", line=3, loop_depth=0, known_cost="n log n", function="f")
        ],
    )
    assert compute_hint(facts).value == "n log n"


def test_linear_recursion() -> None:
    facts = CodeFacts(
        functions=[_fn("fact")],
        recursion=[RecursionFact(function="fact", self_call_count=1, branching_factor=1)],
    )
    hint = compute_hint(facts)
    assert (hint.value, hint.confidence, hint.exponential_suspect) == ("n", "low", False)


def test_halving_recursion_is_logarithmic() -> None:
    facts = CodeFacts(
        functions=[_fn("bs")],
        recursion=[
            RecursionFact(function="bs", self_call_count=2, branching_factor=1, halving=True)
        ],
    )
    assert compute_hint(facts).value == "log n"


def test_callee_cycle_does_not_loop_forever() -> None:
    facts = CodeFacts(
        functions=[_fn("a"), _fn("b")],
        loops=[_loop(2, LoopBound.LINEAR, fn="a"), _loop(20, LoopBound.LINEAR, fn="b")],
        calls=[
            CallFact(name="b", line=3, loop_depth=1, function="a", loop_line=2),
            CallFact(name="a", line=21, loop_depth=1, function="b", loop_line=20),
        ],
    )
    hints = function_hints(facts)
    assert set(hints) == {"a", "b"}
    assert compute_hint(facts).value in ("n^2", "n")


def test_file_hint_is_max_over_functions() -> None:
    facts = CodeFacts(
        functions=[_fn("small"), _fn("big")],
        loops=[
            _loop(2, LoopBound.LINEAR, fn="small"),
            _loop(10, LoopBound.LINEAR, fn="big"),
            _loop(11, LoopBound.LINEAR, parent=10, fn="big"),
        ],
    )
    hint = compute_hint(facts)
    assert (hint.value, hint.function) == ("n^2", "big")
    assert function_hints(facts)["small"].value == "n"


def test_basis_is_bounded() -> None:
    loops = [_loop(i, LoopBound.UNKNOWN) for i in range(2, 200)]
    hint = compute_hint(CodeFacts(functions=[_fn()], loops=loops))
    assert len(hint.basis) <= 8


def test_overflowing_depth_is_clipped_with_low_confidence() -> None:
    loops = [_loop(2, LoopBound.LINEAR)]
    loops += [
        LoopFact(
            kind="for", line=i, depth=i - 1, bound=LoopBound.LINEAR, function="f", parent_line=i - 1
        )
        for i in range(3, 150)
    ]
    hint = compute_hint(CodeFacts(functions=[_fn()], loops=loops))
    assert hint.value == "n^100"
    assert hint.confidence == "low"
    assert any("kırpıldı" in b for b in hint.basis)
    assert all(len(b) < 400 for b in hint.basis)


def test_adversarial_nesting_end_to_end_is_fast() -> None:
    import time

    depth = 1300  # ~40 KB girdi sınırı
    body = "for (int i = 0; i < n; i++) {" * depth + "}" * depth
    code = normalize(f"void f(int n) {{ {body} }}\n", LanguageHint(language=Language.C))
    start = time.perf_counter()
    hint = compute_hint(extract_facts(code))
    assert time.perf_counter() - start < 3.0
    assert hint.value == "n^100"


def test_nested_loops_on_one_line() -> None:
    """Aynı satırdaki iç içe döngüler satır numarasıyla karışmamalı (indeks bağlantısı)."""
    text = (
        "int f(int n) { int s = 0;"
        " for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) s++; return s; }\n"
    )
    facts = extract_facts(normalize(text, LanguageHint(language=Language.C)))
    assert [lp.parent_index for lp in facts.loops] == [None, 0]
    assert compute_hint(facts).value == "n^2"


def test_call_loop_index_on_one_line() -> None:
    text = (
        "int f(int *a, int n) { int c = 0;"
        " for (int i = 0; i < n; i++) c += strlen(s); return c; }\n"
    )
    facts = extract_facts(normalize(text, LanguageHint(language=Language.C)))
    (call,) = facts.calls
    assert call.loop_index == 0
    assert compute_hint(facts).value == "n^2"
