"""HTML kuralları (ADR-0015): erişilebilirlik ve standartlar. Olgu yok; yalnızca ağaç."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from tree_sitter import Node

from codementor.analysis._symbols import line, text
from codementor.models.enums import AuditCategory, Language, Severity
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

_HTML = frozenset({Language.HTML})
_TAGS = ("start_tag", "self_closing_tag")
_UNLABELED_INPUTS = frozenset({"hidden", "submit", "button", "reset", "image"})
_LABEL_ATTRIBUTES = frozenset({"aria-label", "aria-labelledby", "title"})


@dataclass(frozen=True)
class Tag:
    node: Node
    name: str
    attributes: dict[str, str]

    @property
    def line(self) -> int:
        return line(self.node)


def _attribute_value(attribute: Node) -> str:
    for child in attribute.named_children:
        if child.type == "attribute_value":
            return text(child)
        if child.type == "quoted_attribute_value":
            inner = next((c for c in child.named_children if c.type == "attribute_value"), None)
            return text(inner) if inner is not None else ""
    return ""


def tags(ctx: RuleContext, *names: str) -> Iterator[Tag]:
    """Açılış (ve kendi kendini kapatan) etiketler; ad ve öznitelikler küçük harfli."""
    wanted = {n.lower() for n in names}
    for node in ctx.nodes_in(ctx.root, *_TAGS):
        name_node = next((c for c in node.named_children if c.type == "tag_name"), None)
        name = text(name_node).lower()
        if wanted and name not in wanted:
            continue
        attributes = {
            text(
                attr.child_by_field_name("name") or attr.named_children[0]
            ).lower(): _attribute_value(attr)
            for attr in node.named_children
            if attr.type == "attribute" and attr.named_child_count
        }
        yield Tag(node, name, attributes)


@register_rule
class ImageWithoutAlt(Rule):
    """HTML-ACC-001: `alt` özniteliği olmayan görsel."""

    id = "HTML-ACC-001"
    title = "Alternatif metni olmayan görsel"
    description = (
        "Bu görseli göremeyen bir kullanıcı (ekran okuyucu, yüklenemeyen resim) burada ne "
        "duyar ya da görür?"
    )
    languages = _HTML
    category = AuditCategory.ACCESSIBILITY
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        return [self.finding(ctx, t.line) for t in tags(ctx, "img") if "alt" not in t.attributes]


@register_rule
class DocumentWithoutLang(Rule):
    """HTML-ACC-002: `<html>` öğesinde `lang` yok."""

    id = "HTML-ACC-002"
    title = "Belge dili belirtilmemiş"
    description = "Ekran okuyucu bu sayfayı hangi dilin telaffuzuyla okuyacağını nereden biliyor?"
    languages = _HTML
    category = AuditCategory.ACCESSIBILITY
    default_severity = Severity.LOW

    def check(self, ctx: RuleContext) -> list[Finding]:
        return [
            self.finding(ctx, t.line) for t in tags(ctx, "html") if not t.attributes.get("lang")
        ]


@register_rule
class UnlabeledFormControl(Rule):
    """HTML-ACC-003: etiketi (label / aria-label) olmayan form alanı."""

    id = "HTML-ACC-003"
    title = "Etiketsiz form alanı"
    description = (
        "Bu alana klavyeyle gelen bir ekran okuyucu kullanıcısı, alanın ne istediğini nereden "
        "öğreniyor?"
    )
    languages = _HTML
    category = AuditCategory.ACCESSIBILITY
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        labelled = {t.attributes["for"] for t in tags(ctx, "label") if t.attributes.get("for")}
        wrapping = [
            (element.start_byte, element.end_byte)
            for element in ctx.nodes_in(ctx.root, "element")
            if _element_name(element) == "label"
        ]
        found: list[Finding] = []
        for tag in tags(ctx, "input", "textarea", "select"):
            if tag.name == "input" and tag.attributes.get("type", "text") in _UNLABELED_INPUTS:
                continue
            if _LABEL_ATTRIBUTES & set(tag.attributes) or tag.attributes.get("id") in labelled:
                continue
            if any(start <= tag.node.start_byte < end for start, end in wrapping):
                continue
            found.append(self.finding(ctx, tag.line))
        return found


def _element_name(element: Node) -> str:
    start = next((c for c in element.named_children if c.type in _TAGS), None)
    name = next((c for c in start.named_children if c.type == "tag_name"), None) if start else None
    return text(name).lower()


@register_rule
class DuplicateId(Rule):
    """HTML-STD-001: aynı `id` birden çok öğede."""

    id = "HTML-STD-001"
    title = "Yinelenen id"
    description = "Bu id'ye bağlanan bir etiket, bağlantı ya da betik iki öğeden hangisini bulur?"
    languages = _HTML
    category = AuditCategory.DESIGN
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        seen: set[str] = set()
        found: list[Finding] = []
        for tag in tags(ctx):
            value = tag.attributes.get("id")
            if not value:
                continue
            if value in seen:
                found.append(self.finding(ctx, tag.line))
            seen.add(value)
        return found


@register_rule
class MissingDoctype(Rule):
    """HTML-STD-002: tam belgede `<!DOCTYPE html>` yok (tarayıcı uyumluluk moduna geçer)."""

    id = "HTML-STD-002"
    title = "DOCTYPE bildirimi yok"
    description = (
        "Tarayıcı bu belgeyi hangi kurallara göre çizeceğine nasıl karar veriyor? Bildirim "
        "olmadan düzen farklı tarayıcılarda aynı görünür mü?"
    )
    languages = _HTML
    category = AuditCategory.DESIGN
    default_severity = Severity.LOW

    def check(self, ctx: RuleContext) -> list[Finding]:
        if any(True for _ in ctx.nodes_in(ctx.root, "doctype")):
            return []
        root_tag = next(tags(ctx, "html"), None)
        return [self.finding(ctx, root_tag.line)] if root_tag is not None else []
