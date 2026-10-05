"""Python kuralları (ADR-0015)."""

from __future__ import annotations

from tree_sitter import Node

from codementor.analysis._symbols import line, text
from codementor.models.enums import AuditCategory, FindingKind, Language, Severity
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

_PY = frozenset({Language.PYTHON})
_MUTABLE_LITERALS = frozenset(
    {
        "list",
        "dictionary",
        "set",
        "list_comprehension",
        "dictionary_comprehension",
        "set_comprehension",
    }
)
_MUTABLE_CALLS = frozenset({"list", "dict", "set", "defaultdict", "deque"})


def _call_name(node: Node) -> str:
    return text(node.child_by_field_name("function"))


def _first_arg(node: Node) -> Node | None:
    args = node.child_by_field_name("arguments")
    return args.named_children[0] if args is not None and args.named_child_count else None


@register_rule
class MutableDefaultArgument(Rule):
    """PY-DESIGN-001: değiştirilebilir varsayılan argüman (`def f(x=[])`)."""

    id = "PY-DESIGN-001"
    title = "Değiştirilebilir varsayılan argüman"
    description = (
        "Varsayılan değer fonksiyon tanımlanırken bir kez oluşturulur. Fonksiyonu iki kez "
        "çağırdığında ikinci çağrı birincinin bıraktığı nesneyi mi görüyor?"
    )
    languages = _PY
    category = AuditCategory.DESIGN
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        found: list[Finding] = []
        for param in ctx.nodes_in(ctx.root, "default_parameter", "typed_default_parameter"):
            value = param.child_by_field_name("value")
            if value is None:
                continue
            mutable = value.type in _MUTABLE_LITERALS or (
                value.type == "call" and _call_name(value) in _MUTABLE_CALLS
            )
            if mutable:
                found.append(self.finding(ctx, line(param)))
        return found


@register_rule
class BareExcept(Rule):
    """PY-EDGE-001: türü belirtilmemiş `except:` her hatayı (Ctrl+C dahil) yutar."""

    id = "PY-EDGE-001"
    title = "Çıplak except"
    description = (
        "Bu blok hangi hataları yakalıyor? Beklemediğin bir hata (yazım hatası, Ctrl+C) da "
        "buraya düşerse fark eder misin?"
    )
    languages = _PY
    category = AuditCategory.EDGE_CASE
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        return [
            self.finding(ctx, line(clause))
            for clause in ctx.nodes_in(ctx.root, "except_clause")
            if all(child.type in ("block", "comment") for child in clause.named_children)
        ]


@register_rule
class OpenWithoutWith(Rule):
    """PY-RES-001: `with` dışında `open()`; hata yolunda dosya kapanmayabilir.

    Aynı kapsanda `close()` varsa (Faz 52) kapatma niyeti görünüyor → `suggestion`;
    hiç kapanmıyorsa `issue`.
    """

    id = "PY-RES-001"
    title = "with dışında open()"
    description = (
        "Bu dosya ne zaman kapanıyor? Okuma sırasında bir hata olursa kapanma satırına ulaşılır mı?"
    )
    languages = _PY
    category = AuditCategory.RESOURCE_LEAK
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        managed = [(item.start_byte, item.end_byte) for item in ctx.nodes_in(ctx.root, "with_item")]
        # Aynı kapsandaki herhangi bir `close()` çağrısı kapatma niyeti sayılır (Faz 52)
        closed = {
            ctx.scope_key(line(n))
            for n in ctx.nodes_in(ctx.root, "call")
            if (fn := n.child_by_field_name("function")) is not None
            and fn.type == "attribute"
            and text(fn.child_by_field_name("attribute")) == "close"
        }
        found: list[Finding] = []
        for call in ctx.nodes_in(ctx.root, "call"):
            if _call_name(call) not in ("open", "io.open"):
                continue
            if any(start <= call.start_byte < end for start, end in managed):
                continue
            kind = (
                FindingKind.SUGGESTION if ctx.scope_key(line(call)) in closed else FindingKind.ISSUE
            )
            found.append(self.finding(ctx, line(call), kind=kind))
        return found


@register_rule
class LinearListOpInLoop(Rule):
    """PY-PERF-001: döngüde `pop(0)`, `insert(0, …)` ya da listede `in` araması (gizli O(n))."""

    id = "PY-PERF-001"
    title = "Döngüde doğrusal liste işlemi"
    description = (
        "Bu işlem listenin ne kadarını kaydırıyor ya da tarıyor? Döngüyle birlikte toplam iş "
        "girdi büyüdükçe nasıl artıyor?"
    )
    languages = _PY
    category = AuditCategory.PERFORMANCE
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        lines: set[int] = set()
        for call in ctx.nodes_in(ctx.root, "call"):
            fn = call.child_by_field_name("function")
            if fn is None or fn.type != "attribute" or not ctx.in_loop(call):
                continue
            method = text(fn.child_by_field_name("attribute"))
            first = _first_arg(call)
            if method in ("pop", "insert") and first is not None and text(first) == "0":
                lines.add(line(call))
        for cmp in ctx.nodes_in(ctx.root, "comparison_operator"):
            operators = {c.type for c in cmp.children if not c.is_named}
            if not operators & {"in", "not in"} or cmp.named_child_count != 2:
                continue
            target = cmp.named_children[1]
            if (
                target.type == "identifier"
                and ctx.types.get(text(target)) == "list"
                and ctx.in_loop(cmp)
            ):
                lines.add(line(cmp))
        return [self.finding(ctx, n) for n in sorted(lines)]


@register_rule
class EqualityWithNone(Rule):
    """PY-DESIGN-002: `== None` yerine kimlik karşılaştırması (`is None`)."""

    id = "PY-DESIGN-002"
    title = "None ile eşitlik karşılaştırması"
    description = (
        "None bir değer mi, bir kimlik mi? Kendi `__eq__` yöntemi olan bir nesne bu "
        "karşılaştırmada ne döndürebilir?"
    )
    languages = _PY
    category = AuditCategory.DESIGN
    default_severity = Severity.LOW

    def check(self, ctx: RuleContext) -> list[Finding]:
        found: list[Finding] = []
        for cmp in ctx.nodes_in(ctx.root, "comparison_operator"):
            operators = {c.type for c in cmp.children if not c.is_named}
            if operators & {"==", "!="} and any(c.type == "none" for c in cmp.named_children):
                found.append(self.finding(ctx, line(cmp)))
        return found
