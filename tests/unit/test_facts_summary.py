"""`CodeFacts` → bütçeli olgu özeti (mimari §5.4.1 madde 3)."""

from __future__ import annotations

from codementor.prompts.summary import BRIEF_LIMIT, FULL_LIMIT, digest_facts

from codementor.models.enums import AllocationKind, LoopBound
from codementor.models.facts import (
    AllocationFact,
    CallFact,
    CodeFacts,
    EngineSymbols,
    FunctionFact,
    LoopFact,
    RecursionFact,
    SymbolRef,
)


def _facts() -> CodeFacts:
    return CodeFacts(
        functions=[
            FunctionFact(name="Update", line_start=3, line_end=20, is_hot_path=True),
            FunctionFact(name="Helper", line_start=22, line_end=30),
        ],
        loops=[
            LoopFact(kind="for", line=5, depth=1, bound=LoopBound.LINEAR, function="Update"),
            LoopFact(
                kind="for",
                line=6,
                depth=2,
                bound=LoopBound.LINEAR,
                function="Update",
                parent_line=5,
                parent_index=0,
            ),
            LoopFact(kind="while", line=24, depth=1, bound=LoopBound.CONSTANT, function="Helper"),
        ],
        recursion=[RecursionFact(function="Helper", self_call_count=2, branching_factor=2)],
        calls=[
            CallFact(name="list.Contains", line=7, loop_depth=2, known_cost="n", function="Update"),
            CallFact(name="Debug.Log", line=8, loop_depth=2, function="Update"),
            CallFact(name="Mathf.Max", line=25, loop_depth=1, known_cost="1", function="Helper"),
            CallFact(name="list.Sort", line=26, loop_depth=0, known_cost="n log n"),
        ],
        allocations=[
            AllocationFact(kind=AllocationKind.CSHARP_NEW, line=9, loop_depth=2, in_hot_path=True),
            AllocationFact(kind=AllocationKind.CSHARP_NEW, line=27, loop_depth=0),
        ],
        engine_symbols=EngineSymbols(
            uobject_fields=[SymbolRef(name="Target", line=2), SymbolRef(name="Owner", line=3)],
            uproperty_fields=[SymbolRef(name="Owner", line=3)],
            event_subscriptions=[SymbolRef(name="OnHit", line=4)],
            has_on_disable=False,
        ),
    )


def test_full_keeps_relevant_facts_and_drops_trivial_calls() -> None:
    digest = digest_facts(_facts(), "full")
    assert [f.name for f in digest.functions] == ["Update", "Helper"]
    assert len(digest.loops) == 3
    # O(1) ve maliyeti bilinmeyen çağrılar gürültü: yalnızca bilinen O(1) olmayanlar
    assert [c.name for c in digest.costly_calls] == ["list.Contains", "list.Sort"]
    assert len(digest.allocations) == 2
    assert [s.name for s in digest.unmanaged_uobjects] == ["Target"]
    assert [s.name for s in digest.event_subscriptions] == ["OnHit"]
    assert digest.omitted == 0


def test_brief_keeps_only_hot_or_nested() -> None:
    digest = digest_facts(_facts(), "brief")
    assert [f.name for f in digest.functions] == ["Update"]
    assert [loop.line for loop in digest.loops] == [5, 6]  # sıcak yoldaki döngüler
    assert [c.name for c in digest.costly_calls] == ["list.Contains"]  # döngüdeki
    assert [a.line for a in digest.allocations] == [9]
    assert digest.recursion  # özyineleme her zaman önemli
    assert digest.omitted > 0


def test_limits_applied() -> None:
    many = CodeFacts(
        loops=[LoopFact(kind="for", line=i, depth=1, bound=LoopBound.LINEAR) for i in range(1, 200)]
    )
    full = digest_facts(many, "full")
    assert len(full.loops) == FULL_LIMIT
    assert full.omitted == 199 - FULL_LIMIT
    brief_many = CodeFacts(
        loops=[LoopFact(kind="for", line=i, depth=2, bound=LoopBound.LINEAR) for i in range(1, 200)]
    )
    assert len(digest_facts(brief_many, "brief").loops) == BRIEF_LIMIT


def test_empty_facts() -> None:
    assert digest_facts(CodeFacts(), "full").is_empty()
    assert digest_facts(CodeFacts(), "brief").is_empty()
