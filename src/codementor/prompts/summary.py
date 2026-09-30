"""`CodeFacts` → bütçeli olgu özeti (tam JSON değil; mimari §5.4.1 madde 3)."""

from __future__ import annotations

from typing import Literal

from codementor.models.facts import CodeFacts, ComplexityHint
from codementor.models.prompts import FactsDigest

Detail = Literal["full", "brief"]

FULL_LIMIT = 40
BRIEF_LIMIT = 10
TRIVIAL_COSTS = frozenset({"1", "O(1)"})


def digest_facts(facts: CodeFacts, detail: Detail) -> FactsDigest:
    """Olguları süzer. `full`: tüm anlamlı olgular; `brief`: yalnızca sıcak yol ve iç içe
    yapılar (bütçe darsa). Maliyeti bilinmeyen ya da O(1) çağrılar her iki düzeyde de gürültüdür.
    """
    limit = FULL_LIMIT if detail == "full" else BRIEF_LIMIT
    costly_all = [c for c in facts.calls if c.known_cost and c.known_cost not in TRIVIAL_COSTS]
    managed = {s.name for s in facts.engine_symbols.uproperty_fields}
    unmanaged = [s for s in facts.engine_symbols.uobject_fields if s.name not in managed]
    functions, loops, costly, allocations = (
        facts.functions,
        facts.loops,
        costly_all,
        facts.allocations,
    )
    if detail == "brief":
        hot = {f.name for f in functions if f.is_hot_path or f.lifecycle}
        functions = [f for f in functions if f.name in hot]
        loops = [lp for lp in loops if lp.depth >= 2 or lp.function in hot]
        costly = [c for c in costly if c.loop_depth > 0]
        allocations = [a for a in allocations if a.loop_depth > 0 or a.in_hot_path]

    digest = FactsDigest(
        functions=functions[:limit],
        loops=loops[:limit],
        recursion=facts.recursion[:limit],
        costly_calls=costly[:limit],
        allocations=allocations[:limit],
        unmanaged_uobjects=unmanaged[:limit],
        event_subscriptions=facts.engine_symbols.event_subscriptions[:limit],
        has_on_disable=facts.engine_symbols.has_on_disable,
    )
    total = (
        len(facts.functions)
        + len(facts.loops)
        + len(facts.recursion)
        + len(costly_all)
        + len(facts.allocations)
        + len(unmanaged)
        + len(facts.engine_symbols.event_subscriptions)
    )
    kept = (
        len(digest.functions)
        + len(digest.loops)
        + len(digest.recursion)
        + len(digest.costly_calls)
        + len(digest.allocations)
        + len(digest.unmanaged_uobjects)
        + len(digest.event_subscriptions)
    )
    digest.omitted = total - kept
    return digest


def select_function_hints(
    hints: list[ComplexityHint], facts: CodeFacts, detail: Detail
) -> list[ComplexityHint]:
    """Fonksiyon ipuçları da olgudur ve olgularla aynı kademede kırpılır: `brief` yalnızca sıcak
    yoldaki ve üstel şüpheli fonksiyonları tutar (her fonksiyon için bir satır 40 KB kodda
    binlerce token olabilir)."""
    if detail == "full":
        return hints[:FULL_LIMIT]
    hot = {f.name for f in facts.functions if f.is_hot_path or f.lifecycle}
    return [h for h in hints if h.function in hot or h.exponential_suspect][:BRIEF_LIMIT]
