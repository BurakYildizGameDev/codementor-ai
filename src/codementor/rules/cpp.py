"""C++ kuralları (mimari §8.2)."""

from __future__ import annotations

from codementor.analysis._symbols import line
from codementor.models.enums import (
    AllocationKind,
    AuditCategory,
    DeallocationKind,
    Language,
    Severity,
)
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

_RAW_NEW = frozenset({AllocationKind.NEW, AllocationKind.NEW_ARRAY})
_RAW_DELETE = frozenset({DeallocationKind.DELETE, DeallocationKind.DELETE_ARRAY})


@register_rule
class NakedNewDelete(Rule):
    """CPP-OWN-001: akıllı işaretçi yerine çıplak `new`/`delete`."""

    id = "CPP-OWN-001"
    title = "Çıplak new/delete"
    description = (
        "Nesnenin ömrü elle yönetiliyor. Arada bir istisna ya da erken `return` olursa "
        "`delete` çalışır mı? Sahipliği kim taşıyor?"
    )
    languages = frozenset({Language.CPP})
    category = AuditCategory.MEMORY_SAFETY
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        # placement new (`new (buf) T`) bellek ayırmaz; sahiplik sorusu yok
        placement = {
            line(n)
            for n in ctx.nodes_in(ctx.root, "new_expression")
            if n.child_by_field_name("placement") is not None
        }
        lines = [
            a.line for a in ctx.facts.allocations if a.kind in _RAW_NEW and a.line not in placement
        ]
        lines += [d.line for d in ctx.facts.deallocations if d.kind in _RAW_DELETE]
        return [self.finding(ctx, n) for n in lines]
