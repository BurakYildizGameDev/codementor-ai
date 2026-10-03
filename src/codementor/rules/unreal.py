"""Unreal kuralları (mimari §8.2); yalnızca Unreal motorlu C++ kodunda çalışır."""

from __future__ import annotations

from tree_sitter import Node

from codementor.analysis._symbols import line, simple_name, text
from codementor.models.enums import (
    AllocationKind,
    AuditCategory,
    Engine,
    Language,
    LoopBound,
    Severity,
)
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
        plain = {(s.name, s.line) for s in symbols.unreflected_fields}
        return [
            self.finding(
                ctx, s.line, description=_UNREFLECTED if (s.name, s.line) in plain else None
            )
            for s in symbols.uobject_fields
            if (s.name, s.line) not in marked
        ]


# UCLASS/USTRUCT olmayan tipte UPROPERTY yansıtma sistemine görünmez (Faz 32)
_UNREFLECTED = (
    "Bu tip UCLASS ya da USTRUCT değil; yansıtma sistemi onu görmediği için UPROPERTY de "
    "burada işe yaramaz. Çöp toplayıcıya bu referansı başka hangi yolla bildirebilirsin "
    "(ör. TStrongObjectPtr ya da FGCObject)?"
)


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
        facts = ctx.facts
        hot = ctx.in_hot_function
        lines = [lp.line for lp in facts.loops if hot(lp.function_line) and lp.depth == 1]
        lines += [
            c.line
            for c in facts.calls
            if hot(c.function_line)
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


_GROW = frozenset({"Add", "Emplace", "Push"})
_PRESIZE = frozenset({"Reserve", "SetNum", "SetNumUninitialized", "SetNumZeroed", "Init"})
_PRESIZE_WITH_COUNT = frozenset({"Empty", "Reset"})  # `Empty(n)`/`Reset(n)` yer ayırır
_COUNTED_LOOPS = ("for_statement", "for_range_loop")
# Bu düğümlerin altındaki ekleme her turda çalışmayabilir; eleman sayısı belli değil
_CONDITIONAL = frozenset(
    {
        "if_statement",
        "switch_statement",
        "conditional_expression",
        "while_statement",
        "do_statement",
    }
)
# Döngüden erken çıkış ya da tur atlama: eklenen eleman sayısı belli değil
_JUMPS = frozenset({"break_statement", "continue_statement", "return_statement", "goto_statement"})


def _member_call(node: Node) -> tuple[str, str, int] | None:
    """`Arr.Add(x)` → (`Arr`, `Add`, argüman sayısı); alıcı yalın ad değilse None."""
    fn = node.child_by_field_name("function")
    if fn is None or fn.type != "field_expression":
        return None
    receiver, field = fn.child_by_field_name("argument"), fn.child_by_field_name("field")
    if receiver is None or field is None or receiver.type != "identifier":
        return None
    args = node.child_by_field_name("arguments")
    return text(receiver), text(field), args.named_child_count if args is not None else 0


@register_rule
class AddWithoutReserve(Rule):
    """UE-MEM-001: eleman sayısı bilinen döngüde `Reserve` olmadan `TArray::Add`."""

    id = "UE-MEM-001"
    title = "Reserve olmadan TArray::Add"
    description = (
        "Döngünün kaç kez döneceği belli ve her turda diziye bir eleman ekleniyor. Dizinin "
        "kapasitesi dolduğunda `Add` ne yapmak zorunda kalır ve bu döngüde kaç kez olabilir?"
    )
    languages = CPP
    engines = UNREAL
    category = AuditCategory.PERFORMANCE
    default_severity = Severity.LOW

    def check(self, ctx: RuleContext) -> list[Finding]:
        counted: dict[int, bool] = {}  # döngü satırı → sınırı bilinen mi (aynı satırda hepsi)
        for lp in ctx.facts.loops:
            if lp.kind in ("for", "foreach"):
                known = lp.bound is not LoopBound.UNKNOWN
                counted[lp.line] = counted.get(lp.line, True) and known
        found: list[Finding] = []
        outer = -1  # işlenen en dıştaki fonksiyonun sonu (yerel sınıf metotları yeniden gezilmez)
        for fn in sorted(ctx.function_nodes, key=lambda f: f.node.start_byte):
            if fn.node.start_byte < outer:
                continue
            outer = fn.node.end_byte
            calls = [m for n in ctx.nodes_in(fn.node, "call_expression") if (m := _member_call(n))]
            if not any(name in _GROW for _, name, _ in calls):
                continue
            presized = {
                receiver
                for receiver, name, argc in calls
                if name in _PRESIZE or (name in _PRESIZE_WITH_COUNT and argc >= 1)
            }
            covered = -1  # işlenen en dıştaki döngünün sonu (iç döngüler yeniden gezilmez)
            for loop in ctx.nodes_in(fn.node, *_COUNTED_LOOPS):
                if loop.start_byte < covered or not counted.get(line(loop), False):
                    continue
                covered = loop.end_byte
                found += self._grows(ctx, loop, counted, presized)
        return found

    def _grows(
        self, ctx: RuleContext, loop: Node, counted: dict[int, bool], presized: set[str]
    ) -> list[Finding]:
        """Döngüde koşulsuz büyüyen `TArray` alıcıları; erken çıkış/atlama varsa hiçbiri."""
        body = loop.child_by_field_name("body")
        grows: dict[str, int] = {}
        stack: list[tuple[Node, bool]] = [(body, False)] if body is not None else []
        while stack:
            node, conditional = stack.pop()
            if node.type == "lambda_expression":
                continue
            if node.type in _JUMPS:
                return []
            if node.type in _CONDITIONAL or (
                node.type in _COUNTED_LOOPS and not counted.get(line(node), False)
            ):
                conditional = True
            if (
                not conditional
                and node.type == "call_expression"
                and (m := _member_call(node)) is not None
            ):
                receiver, name, _ = m
                if (
                    name in _GROW
                    and receiver not in presized
                    and ctx.types.get(receiver) == "TArray"
                ):
                    grows.setdefault(receiver, line(node))
            stack.extend((c, conditional) for c in reversed(node.named_children))
        return [self.finding(ctx, n) for n in grows.values()]
