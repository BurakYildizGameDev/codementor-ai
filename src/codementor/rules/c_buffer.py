"""C tampon güvenliği kuralları (C-BUF-*).

C-BUF-001 `c.py`'de; bu modül dosya boyutunu 400 satır sınırında tutmak için ayrıldı
(AGENTS.md kod stili, `c.py` / `c_memory.py` kalıbı).
"""

from __future__ import annotations

from tree_sitter import Node

from codementor.analysis._symbols import line, text
from codementor.models.enums import AuditCategory, Language, Severity
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.c import callee_name
from codementor.rules.registry import register_rule

_WIDTH_SCANF = frozenset({"scanf", "fscanf"})
_MAX_FORMAT_BYTES = 200  # daha uzun biçim metni incelenmez (mimari §12)
_FLAGS = "-+ #0'"
_LENGTHS = "hlLjzt"


def unbounded_string_conversion(format_text: str) -> bool:
    """Biçim metninde genişlik sınırı olmayan `%s` var mı.

    `%99s`/`%8s` sınırlı, `%*s` atama yapmaz (hedef yok) sayılır. Tarama doğrusaldır:
    40 KB biçim metninde her `%` bir kez işlenir.
    """
    index = format_text.find("%")
    while index >= 0:
        cursor = index + 1
        if cursor < len(format_text) and format_text[cursor] == "%":  # `%%`
            index = format_text.find("%", cursor + 1)
            continue
        while cursor < len(format_text) and format_text[cursor] in _FLAGS:
            cursor += 1
        if cursor < len(format_text) and format_text[cursor] == "*":
            index = format_text.find("%", cursor + 1)
            continue
        width = ""
        while cursor < len(format_text) and format_text[cursor].isdigit():
            width += format_text[cursor]
            cursor += 1
        if cursor < len(format_text) and format_text[cursor] == ".":
            cursor += 1
            while cursor < len(format_text) and (
                format_text[cursor].isdigit() or format_text[cursor] == "*"
            ):
                cursor += 1
        while cursor < len(format_text) and format_text[cursor] in _LENGTHS:
            cursor += 1
        if not width and cursor < len(format_text) and format_text[cursor] == "s":
            return True
        index = format_text.find("%", cursor)
    return False


def _unbounded(call: Node) -> bool:
    """Çağrının biçim metni genişliksiz `%s` içeriyor mu.

    Biçim metin sabiti değilse (değişken) susar: hangi dönüşümlerin istendiği bilinmez.
    """
    args = call.child_by_field_name("arguments")
    index = 0 if callee_name(call) == "scanf" else 1  # `fscanf(akış, biçim, …)`
    fmt = args.named_child(index) if args is not None and args.named_child_count > index else None
    if (
        fmt is None
        or fmt.type != "string_literal"
        or fmt.end_byte - fmt.start_byte > _MAX_FORMAT_BYTES
    ):
        return False
    return unbounded_string_conversion(text(fmt)[1:-1])


@register_rule
class UnboundedScanf(Rule):
    """C-BUF-002: genişlik sınırı olmayan `scanf("%s", …)` (tampon taşması)."""

    id = "C-BUF-002"
    title = "Sınırı olmayan scanf %s"
    description = (
        "`%s` hedefe kaç karakter yazacağını bilmez; kullanıcı tampondan uzun bir girdi "
        "yazarsa ne olur ve genişliği kim belirlemeli?"
    )
    languages = frozenset({Language.C})
    category = AuditCategory.MEMORY_SAFETY
    default_severity = Severity.HIGH
    catalog_note = (
        "Yalnızca `scanf`/`fscanf` ve yalnızca biçim metin sabiti olduğunda çalışır. Genişlikli "
        "(`%99s`) ve atama yapmayan (`%*s`) dönüşümler, `sscanf` ile sınırı olmayan `%[` "
        "taraması kapsam dışıdır (muhafazakâr)."
    )

    def check(self, ctx: RuleContext) -> list[Finding]:
        if not any(c.name in _WIDTH_SCANF for c in ctx.facts.calls):
            return []
        return [
            self.finding(ctx, line(call))
            for call in ctx.nodes_in(ctx.root, "call_expression")
            if callee_name(call) in _WIDTH_SCANF and _unbounded(call)
        ]
