"""C# kuralları (mimari §8.2); Unity kodu da C# olduğundan bunlar Unity'de de çalışır."""

from __future__ import annotations

from tree_sitter import Node

from codementor.analysis._symbols import line, operator_of, simple_name, text
from codementor.models.enums import AuditCategory, Language, Severity
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

_LINEAR_COLLECTIONS = frozenset({"List", "Array", "LinkedList", "Queue", "Stack"})
_LINEAR_SEARCH = frozenset({"Contains", "IndexOf", "LastIndexOf", "Remove", "Find", "Exists"})
_STRING_TYPES = frozenset({"string", "String"})
_STRING_NODES = frozenset(
    {
        "string_literal",
        "verbatim_string_literal",
        "raw_string_literal",
        "interpolated_string_expression",
    }
)
_MAX_TARGET_BYTES = 200


def _concat_leaves(node: Node) -> list[Node]:
    """`a + "x" + b` zincirinin yaprakları (yinelemeli; uzun zincirde doğrusal)."""
    leaves: list[Node] = []
    stack = [node]
    while stack:
        current = stack.pop()
        if current.type == "binary_expression" and operator_of(current) == "+":
            stack += [
                c
                for c in (current.child_by_field_name("right"), current.child_by_field_name("left"))
                if c is not None
            ]
        else:
            leaves.append(current)
    return leaves


def _target(node: Node | None) -> str | None:
    """Atama hedefinin adı (`this.log` → `log`); uzun ifadede None."""
    if node is None or node.end_byte - node.start_byte > _MAX_TARGET_BYTES:
        return None
    return text(node).removeprefix("this.")


def _accumulates(node: Node, types: dict[str, str]) -> bool:
    """Metni biriktiren atama: `s += ...`, `s = s + ...`, `s = x + s` (hedef string).

    Hedefin string olduğu bildirilen tipten ya da sağ taraftaki metin sabitinden anlaşılır;
    aynı satırdaki `total += i` (sayı) biriktirme sayılmaz.
    """
    op = operator_of(node)
    target = _target(node.child_by_field_name("left"))
    right = node.child_by_field_name("right")
    if target is None or right is None or op not in ("+=", "="):
        return False
    leaves = _concat_leaves(right)
    if op == "=" and not (
        right.type == "binary_expression"
        and any(
            leaf.end_byte - leaf.start_byte <= _MAX_TARGET_BYTES
            and text(leaf).removeprefix("this.") == target
            for leaf in leaves
        )
    ):
        return False
    typed = types.get(simple_name(target))
    if typed is not None:
        return typed in _STRING_TYPES
    return any(leaf.type in _STRING_NODES for leaf in leaves)


@register_rule
class StringConcatInLoop(Rule):
    """CS-ALLOC-001: döngüde metni `+=` ile biriktirme."""

    id = "CS-ALLOC-001"
    title = "Döngüde string birleştirme"
    description = (
        "`string` değiştirilemez: her `+=` yeni bir metin ayırıp eskisini kopyalar. "
        "Döngü n kez dönerse toplam kaç karakter kopyalanır?"
    )
    languages = frozenset({Language.CSHARP})
    category = AuditCategory.GARBAGE_COLLECTION
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        # Olgular yalnızca satır taşıdığından (aynı satırda `t += x; s = "a" + x;` karışır)
        # ve metin sabitsiz `s = x + s` birleştirmesini içermediğinden kural düğüm düzeyinde
        # çalışır: döngü gövdesindeki her atama doğrudan sınanır.
        return [
            self.finding(ctx, line(n))
            for n in ctx.nodes_in(ctx.root, "assignment_expression")
            if _accumulates(n, ctx.types) and ctx.in_loop(n)
        ]


@register_rule
class LinearSearchInLoop(Rule):
    """CS-PERF-001: döngü içinde `List.Contains/IndexOf` gibi doğrusal arama."""

    id = "CS-PERF-001"
    title = "Döngüde doğrusal arama"
    description = (
        "`List.Contains`/`IndexOf`/`Remove` elemanı bulmak için listeyi baştan sona tarar ve "
        "bu bir döngünün içinde. Toplam maliyet ne olur? Hangi veri yapısı bu aramayı daha "
        "hızlı yapar?"
    )
    languages = frozenset({Language.CSHARP})
    category = AuditCategory.PERFORMANCE
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        return [
            self.finding(ctx, c.line)
            for c in ctx.facts.calls
            if c.loop_depth >= 1
            and c.known_cost == "n"
            and c.name.split(".")[0] in _LINEAR_COLLECTIONS
            and simple_name(c.name) in _LINEAR_SEARCH
        ]
