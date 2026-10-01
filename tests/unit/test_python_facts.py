"""Python olguları ve Big-O ipucu (ADR-0015)."""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.analysis.call_costs import load_call_costs
from codementor.analysis.complexity_hint import compute_hint
from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language, LoopBound
from codementor.models.facts import CodeFacts
from codementor.models.request import LanguageHint

COSTS = load_call_costs(Path(__file__).resolve().parents[2] / "data" / "call_costs.yaml")


def facts(source: str) -> CodeFacts:
    code = normalize(source, LanguageHint(language=Language.PYTHON, engine=Engine.NONE))
    return extract_facts(code, costs=COSTS)


def hint(source: str) -> str | None:
    found = facts(source)
    assert found.warnings == [], found.warnings
    return compute_hint(found).value if found.functions or found.loops else None


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("def f(xs):\n    for x in xs:\n        print(x)\n", "n"),
        (
            "def f(xs):\n    for i in range(len(xs)):\n"
            "        for j in range(len(xs)):\n            pass\n",
            "n^2",
        ),
        ("def f():\n    for i in range(10):\n        print(i)\n", "1"),
        (
            "def f(xs, t):\n    lo, hi = 0, len(xs) - 1\n    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n        if xs[mid] < t:\n            lo = mid + 1\n"
            "        else:\n            hi = mid - 1\n",
            "log n",
        ),
        ("def f(n):\n    c = 0\n    while n > 0:\n        n //= 2\n        c += 1\n", "log n"),
        ("def f(a, b):\n    return [x for x in a if x in [y for y in b]]\n", "n^2"),
        ("def f(xs):\n    for x in xs:\n        ys = sorted(xs)\n", "n^2 log n"),
        (
            "def f(n):\n    out: list[int] = []\n    for i in range(n):\n"
            "        out.insert(0, i)\n    return out\n",
            "n^2",
        ),
        (
            "def f(items):\n    seen = []\n    for item in items:\n"
            "        if item in seen:\n            return True\n        seen.append(item)\n",
            "n^2",
        ),
        (
            "def f(items):\n    seen = set()\n    for item in items:\n"
            "        if item in seen:\n            return True\n        seen.add(item)\n",
            "n",
        ),
        (
            "def fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n",
            "2^n",
        ),
    ],
    ids=[
        "foreach",
        "nested-range",
        "constant-range",
        "binary-search",
        "floor-halving",
        "nested-comprehension",
        "sort-in-loop",
        "insert-front",
        "list-membership",
        "set-membership",
        "fibonacci",
    ],
)
def test_python_complexity_hint(source: str, expected: str) -> None:
    assert hint(source) == expected


def test_python_function_and_parameters() -> None:
    found = facts("def f(a, b: int, c=1, *args, d: str = 'x', **kw):\n    return a\n")
    (function,) = found.functions
    assert function.name == "f"
    assert function.parameters == ["a", "b", "c", "args", "d", "kw"]


def test_python_loop_kinds_and_bounds() -> None:
    found = facts("def f(xs):\n    for x in xs:\n        while x > 0:\n            x -= 1\n")
    assert [(loop.kind, loop.bound) for loop in found.loops] == [
        ("foreach", LoopBound.LINEAR),
        ("while", LoopBound.LINEAR),
    ]


def test_untyped_membership_is_not_guessed() -> None:
    found = facts("def f(xs, ys):\n    for x in xs:\n        if x in ys:\n            pass\n")
    assert all(c.known_cost is None for c in found.calls)
