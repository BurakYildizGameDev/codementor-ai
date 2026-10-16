"""C++ performans kuralları: döngü içi kopya, boşaltma ve büyüme (CPP-PERF-002..004).

`cpp.py` 400 satır sınırını aşmasın diye ayrı modül (`c.py` / `c_memory.py` kalıbı, AGENTS.md);
CPP-PERF-001 `cpp.py`'de kalır. İçerik kural kimliğine göre değil, konuya göre buradadır.
"""

from __future__ import annotations

from tree_sitter import Node

from codementor.analysis._symbols import line, operator_of, strip_templates, text
from codementor.models.enums import (
    AuditCategory,
    FindingKind,
    Language,
    LoopBound,
    Severity,
)
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

_CPP = frozenset({Language.CPP})
_MAX_TEXT = 200  # daha uzun metin alınmaz (mimari §12)
_STRING_TYPES = frozenset({"string", "wstring", "basic_string", "FString"})
_TEXT_LITERALS = frozenset({"string_literal", "raw_string_literal", "concatenated_string"})
_CONTAINERS = frozenset({"vector", "deque", "list", "TArray", "TSet", "basic_string"})
_GROW = frozenset({"push_back", "emplace_back"})
_PRESIZE = frozenset({"reserve", "resize"})
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


def _base_type(raw: str | None) -> str:
    """`std::vector<int>` → `vector` (şablon ve ad alanı atılır); tip yoksa boş."""
    return strip_templates(raw).removeprefix("std::").strip() if raw else ""


def _plus_leaves(node: Node) -> list[Node]:
    """`a + b + c` zincirinin yaprakları (yinelemeli; uzun zincirde doğrusal)."""
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


def _is_text(typed: str | None, leaves: list[Node]) -> bool:
    """Hedefin metin olduğu bildirilen tipten ya da sağdaki metin sabitinden anlaşılır."""
    if typed is not None:
        return _base_type(typed) in _STRING_TYPES
    return any(leaf.type in _TEXT_LITERALS for leaf in leaves)


def _member_call(node: Node) -> tuple[str, str] | None:
    """`v.push_back(x)` → (`v`, `push_back`); alıcı yalın ad değilse None."""
    fn = node.child_by_field_name("function")
    if fn is None or fn.type != "field_expression":
        return None
    receiver, field = fn.child_by_field_name("argument"), fn.child_by_field_name("field")
    if receiver is None or field is None or receiver.type != "identifier":
        return None
    if field.end_byte - field.start_byte > _MAX_TEXT:
        return None
    return text(receiver), text(field)


@register_rule
class StringCopyInLoop(Rule):
    """CPP-PERF-002: döngüde `s = s + …` (her turda tam kopya, karesel)."""

    id = "CPP-PERF-002"
    title = "Döngüde tam metin kopyası"
    description = (
        "`s = s + x` her turda s'in tamamını yeni bir tampona kopyalar. n tur dönen bir "
        "döngüde toplam kaç karakter kopyalanır ve `s += x` bunu nasıl değiştirir?"
    )
    languages = _CPP
    category = AuditCategory.PERFORMANCE
    default_severity = Severity.MEDIUM
    catalog_note = (
        "Yalnızca döngü gövdesindeki `s = s + …` biçimi (aynı yalın ad sağda yaprak olarak) "
        "aranır; `s += …`, `s.append(…)`, döngü dışı atamalar ve `this->alan = this->alan + …` "
        "kapsam dışıdır."
    )

    def check(self, ctx: RuleContext) -> list[Finding]:
        found: list[Finding] = []
        for node in ctx.nodes_in(ctx.root, "assignment_expression"):
            left = node.child_by_field_name("left")
            right = node.child_by_field_name("right")
            if (
                operator_of(node) != "="
                or left is None
                or right is None
                or left.type != "identifier"
                or right.type != "binary_expression"
                or operator_of(right) != "+"
                or not ctx.in_loop(node)
            ):
                continue
            name = text(left)
            leaves = _plus_leaves(right)
            copies_self = any(
                leaf.end_byte - leaf.start_byte <= _MAX_TEXT and text(leaf) == name
                for leaf in leaves
            )
            if copies_self and _is_text(ctx.types.get(name), leaves):
                found.append(self.finding(ctx, line(node)))
        return found


@register_rule
class EndlInLoop(Rule):
    """CPP-PERF-003: döngüde `std::endl` (her turda tampon boşaltma)."""

    id = "CPP-PERF-003"
    title = "Döngüde std::endl"
    description = (
        "`std::endl` satır sonu eklemekle kalmaz, tamponu da her turda boşaltır. Döngü 10 000 "
        "kez dönüyorsa alt katmana kaç yazma çağrısı iner?"
    )
    languages = _CPP
    category = AuditCategory.PERFORMANCE
    default_severity = Severity.LOW
    default_kind = FindingKind.SUGGESTION
    catalog_note = (
        "Yalnızca `std::endl` yazımı ve döngü gövdesi aranır; `using namespace std;` ile yazılan "
        "yalın `endl`, `std::flush` ve döngü dışı kullanımlar kapsam dışıdır (muhafazakâr)."
    )

    def check(self, ctx: RuleContext) -> list[Finding]:
        return [
            self.finding(ctx, line(node))
            for node in ctx.nodes_in(ctx.root, "qualified_identifier")
            if text(node).replace(" ", "") == "std::endl" and ctx.in_loop(node)
        ]


@register_rule
class PushBackWithoutReserve(Rule):
    """CPP-PERF-004: eleman sayısı bilinen döngüde `reserve` olmadan `push_back`."""

    id = "CPP-PERF-004"
    title = "Reserve olmadan push_back"
    description = (
        "Döngünün kaç kez döneceği belli ve her turda kapsayıcıya bir eleman ekleniyor. "
        "Kapasite dolduğunda `push_back` ne yapmak zorunda kalır ve bu döngüde kaç kez olur?"
    )
    languages = _CPP
    category = AuditCategory.PERFORMANCE
    default_severity = Severity.LOW
    default_kind = FindingKind.SUGGESTION
    catalog_note = (
        "Yalnızca sınırı bilinen `for`/aralık döngüleri, yalın adlı kapsayıcılar "
        "(`std::vector`/`std::deque`/`std::list`/`TArray`/`TSet`) ve koşulsuz `push_back`/"
        "`emplace_back` sayılır; erken `return`/`break`/koşul varsa susar. Aynı alıcı için "
        "fonksiyonda bir `reserve`/`resize` çağrısı varsa bulgu verilmez: sıralama denetlenmez. "
        "Unreal'daki `TArray::Add` için UE-MEM-001 geçerlidir."
    )

    def check(self, ctx: RuleContext) -> list[Finding]:
        counted: dict[int, bool] = {}  # döngü satırı → sınırı bilinen mi (aynı satırda hepsi)
        for lp in ctx.facts.loops:
            if lp.kind in ("for", "foreach"):
                counted[lp.line] = counted.get(lp.line, True) and lp.bound is not LoopBound.UNKNOWN
        found: list[Finding] = []
        outer = -1  # işlenen en dıştaki fonksiyonun sonu (yerel sınıf metotları yeniden gezilmez)
        for fn in sorted(ctx.function_nodes, key=lambda f: f.node.start_byte):
            if fn.node.start_byte < outer:
                continue
            outer = fn.node.end_byte
            calls = [c for n in ctx.nodes_in(fn.node, "call_expression") if (c := _member_call(n))]
            if not any(name in _GROW for _, name in calls):
                continue
            presized = {receiver for receiver, name in calls if name in _PRESIZE}
            covered = -1  # işlenen en dıştaki döngünün sonu (iç döngüler yeniden gezilmez)
            for loop in ctx.nodes_in(fn.node, *_COUNTED_LOOPS):
                if loop.start_byte < covered or not counted.get(line(loop), False):
                    continue
                covered = loop.end_byte
                found += self._grows(ctx, loop, counted, presized)
        return found

    def _grows(
        self,
        ctx: RuleContext,
        loop: Node,
        counted: dict[int, bool],
        presized: set[str],
    ) -> list[Finding]:
        """Döngüde koşulsuz büyüyen kapsayıcılar; erken çıkış ya da koşul varsa hiçbiri."""
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
                and (call := _member_call(node)) is not None
            ):
                receiver, name = call
                if (
                    name in _GROW
                    and receiver not in presized
                    and _base_type(ctx.types.get(receiver)) in _CONTAINERS
                ):
                    grows.setdefault(receiver, line(node))
            stack.extend((c, conditional) for c in reversed(node.named_children))
        return [self.finding(ctx, n) for n in grows.values()]
