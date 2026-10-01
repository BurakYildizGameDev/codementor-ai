"""CSS kuralları (ADR-0015): bakım kolaylığı ve standartlar. Olgu yok; yalnızca ağaç."""

from __future__ import annotations

from tree_sitter import Node

from codementor.analysis._symbols import line, text
from codementor.models.enums import AuditCategory, Language, Severity
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

_CSS = frozenset({Language.CSS})
IMPORTANT_THRESHOLD = 3
_VENDOR = ("-webkit-", "-moz-", "-ms-", "-o-")


@register_rule
class ImportantOveruse(Rule):
    """CSS-MAINT-001: çok sayıda `!important` (özgüllük savaşına işaret)."""

    id = "CSS-MAINT-001"
    title = "Çok sayıda !important"
    description = (
        "Bu kural neden !important olmadan uygulanmıyordu? Bir sonraki değişiklikte bunu ezmek "
        "için ne yapman gerekecek?"
    )
    languages = _CSS
    category = AuditCategory.MAINTAINABILITY
    default_severity = Severity.LOW

    def check(self, ctx: RuleContext) -> list[Finding]:
        marks = list(ctx.nodes_in(ctx.root, "important"))
        if len(marks) < IMPORTANT_THRESHOLD:
            return []
        return [self.finding(ctx, n) for n in sorted({line(m) for m in marks})]


def _declarations(block: Node) -> list[tuple[str, str, Node]]:
    """Bloğun doğrudan bildirimleri: (özellik, değer metni, düğüm)."""
    result: list[tuple[str, str, Node]] = []
    for child in block.named_children:
        if child.type != "declaration":
            continue
        name = next((c for c in child.named_children if c.type == "property_name"), None)
        values = [
            text(c) for c in child.named_children if c.type not in ("property_name", "important")
        ]
        result.append((text(name).lower(), " ".join(values), child))
    return result


@register_rule
class DuplicateProperty(Rule):
    """CSS-STD-001: aynı blokta aynı özellik iki kez (önceki değer etkisiz)."""

    id = "CSS-STD-001"
    title = "Aynı blokta yinelenen özellik"
    description = (
        "Bu blokta aynı özelliğe iki değer verilmiş. Tarayıcı hangisini kullanıyor ve "
        "öteki satır ne işe yarıyor?"
    )
    languages = _CSS
    category = AuditCategory.MAINTAINABILITY
    default_severity = Severity.LOW

    def check(self, ctx: RuleContext) -> list[Finding]:
        found: list[Finding] = []
        for block in ctx.nodes_in(ctx.root, "block"):
            seen: dict[str, str] = {}
            for name, value, node in _declarations(block):
                previous = seen.get(name)
                seen[name] = value
                if previous is None or name.startswith(_VENDOR):
                    continue
                # bilinçli geri dönüş deseni (`display: -webkit-box; display: flex`,
                # `color: red; color: var(--x)`) yinelenme sayılmaz
                fallback = any(v.startswith(_VENDOR) or "(" in v for v in (previous, value))
                if not fallback:
                    found.append(self.finding(ctx, line(node)))
        return found


@register_rule
class EmptyRule(Rule):
    """CSS-MAINT-002: hiç bildirimi olmayan kural bloğu."""

    id = "CSS-MAINT-002"
    title = "Boş kural bloğu"
    description = (
        "Bu seçici için bir stil yazılmamış. Kalması gerekiyor mu, yoksa yarım kalmış bir "
        "düzenlemenin izi mi?"
    )
    languages = _CSS
    category = AuditCategory.MAINTAINABILITY
    default_severity = Severity.LOW

    def check(self, ctx: RuleContext) -> list[Finding]:
        found: list[Finding] = []
        for rule_set in ctx.nodes_in(ctx.root, "rule_set"):
            block = next((c for c in rule_set.named_children if c.type == "block"), None)
            if block is not None and not any(c.type != "comment" for c in block.named_children):
                found.append(self.finding(ctx, line(rule_set)))
        return found
