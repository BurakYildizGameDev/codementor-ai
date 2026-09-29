"""Unreal kuralları (mimari §8.2); yalnızca Unreal motorlu C++ kodunda çalışır."""

from __future__ import annotations

from codementor.analysis._symbols import simple_name
from codementor.models.enums import AllocationKind, AuditCategory, Engine, Language, Severity
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

UNREAL = frozenset({Engine.UNREAL})
CPP = frozenset({Language.CPP})

_CONSTANT_COSTS = frozenset({"1", "1*"})
_HEAVY_CALLS = frozenset(
    {
        "GetAllActorsOfClass",
        "GetAllActorsWithTag",
        "GetAllActorsWithInterface",
        "GetAllActorsOfClassWithTag",
        "FindComponentByClass",
        "GetComponents",
        "SpawnActor",
        "NewObject",
        "LoadObject",
        "StaticLoadObject",
        "FindObject",
    }
)
_HEAP = frozenset(
    {
        AllocationKind.NEW,
        AllocationKind.NEW_ARRAY,
        AllocationKind.MALLOC,
        AllocationKind.CALLOC,
        AllocationKind.MAKE_SHARED,
        AllocationKind.MAKE_UNIQUE,
    }
)


@register_rule
class UObjectWithoutUProperty(Rule):
    """UE-GC-001: `UPROPERTY` olmadan tutulan `UObject*`/`AActor*` üye alanı."""

    id = "UE-GC-001"
    title = "UPROPERTY'siz UObject alanı"
    description = (
        "Çöp toplayıcı yalnızca `UPROPERTY` ile işaretli alanları görür. Bu alanın "
        "gösterdiği nesne başka hiçbir yerden tutulmuyorsa GC onu toplar; alan ne gösterir?"
    )
    languages = CPP
    engines = UNREAL
    category = AuditCategory.GARBAGE_COLLECTION
    default_severity = Severity.HIGH

    def check(self, ctx: RuleContext) -> list[Finding]:
        symbols = ctx.facts.engine_symbols
        marked = {(s.name, s.line) for s in symbols.uproperty_fields}
        return [
            self.finding(ctx, s.line)
            for s in symbols.uobject_fields
            if (s.name, s.line) not in marked
        ]


@register_rule
class HeavyTick(Rule):
    """UE-PERF-001: `Tick` içinde döngü, pahalı arama veya tahsis."""

    id = "UE-PERF-001"
    title = "Tick içinde ağır iş"
    description = (
        "`Tick` her karede çalışır. Bu iş gerçekten her karede mi gerekli, yoksa bir olaya, "
        "zamanlayıcıya ya da önbelleğe taşınabilir mi?"
    )
    languages = CPP
    engines = UNREAL
    category = AuditCategory.PERFORMANCE
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        hot = ctx.hot_functions
        facts = ctx.facts
        lines = [lp.line for lp in facts.loops if lp.function in hot and lp.depth == 1]
        lines += [
            c.line
            for c in facts.calls
            if c.function in hot
            and c.loop_depth == 0
            and (
                simple_name(c.name) in _HEAVY_CALLS
                or (c.known_cost is not None and c.known_cost not in _CONSTANT_COSTS)
            )
        ]
        lines += [
            a.line
            for a in facts.allocations
            if a.in_hot_path and a.loop_depth == 0 and a.kind in _HEAP
        ]
        return [self.finding(ctx, n) for n in lines]
