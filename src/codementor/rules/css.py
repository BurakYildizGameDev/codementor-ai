"""CSS kuralları (ADR-0015): bakım, erişilebilirlik ve taşma. Olgu yok; yalnızca ağaç."""

from __future__ import annotations

import re

from tree_sitter import Node

from codementor.analysis._symbols import line, text
from codementor.models.enums import AuditCategory, FindingKind, Language, Severity
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

_CSS = frozenset({Language.CSS})
IMPORTANT_THRESHOLD = 3
_VENDOR = ("-webkit-", "-moz-", "-ms-", "-o-")
# Yalnızca görsel/işaretleme öğeleri: metin taşması sorusu anlamsız (CSS-LAYOUT-001)
_MEDIA_ELEMENTS = frozenset(
    {
        "img",
        "svg",
        "canvas",
        "video",
        "iframe",
        "object",
        "embed",
        "input",
        "textarea",
        "select",
        "hr",
        "br",
    }
)
# Aynı blokta odak göstergesi yerine geçen özellikler (CSS-ACC-001)
_FOCUS_ALTERNATIVES = (
    "border",
    "box-shadow",
    "background",
    "text-decoration",
    "fill",
    "stroke",
    "font-weight",
)
_HEAD_TAG = re.compile(r"^[A-Za-z][\w-]*")
_PX = re.compile(r"^\d+(?:\.\d+)?px$")
_NEGATIVE_PX = re.compile(r"^-\d+(?:\.\d+)?px$")


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


def _selectors(rule_set: Node) -> str:
    """Kural bloğunun seçici metni (`button:focus`, `a, b`); yoksa boş."""
    node = next((c for c in rule_set.named_children if c.type == "selectors"), None)
    return text(node) if node is not None else ""


def _block(rule_set: Node) -> Node | None:
    """Kural bloğunun gövdesi (`{ … }`)."""
    return next((c for c in rule_set.named_children if c.type == "block"), None)


def _focus_parts(selectors: str) -> list[str]:
    """`:focus` içeren seçici parçaları; `:focus-visible` ayrı ele alınır (CSS-ACC-001)."""
    return [
        part.strip()
        for part in selectors.split(",")
        if ":focus" in part and ":focus-visible" not in part
    ]


def _focus_visible_bases(ctx: RuleContext) -> set[str]:
    """`:focus-visible` kuralı yazılmış kök seçiciler; ayrı kural odak göstergesi sayılır."""
    bases: set[str] = set()
    for rule_set in ctx.nodes_in(ctx.root, "rule_set"):
        for part in _selectors(rule_set).split(","):
            if ":focus-visible" in part:
                bases.add(part.split(":focus-visible")[0].strip())
    return bases


def _removes_outline(value: str) -> bool:
    """`outline: none` / `outline: 0` (başka her değer görünür bir gösterge bırakır)."""
    return value.strip().lower() in {"none", "0"}


@register_rule
class OutlineRemoved(Rule):
    """CSS-ACC-001: `outline: none/0` ve yerine başka odak göstergesi yok."""

    id = "CSS-ACC-001"
    title = "Odak göstergesi kaldırılmış"
    description = (
        "`outline: none` klavyeyle gezen kullanıcının kaldığı yeri gösteren tek işareti "
        "siliyor. Bu kutu odaklandığında ekranda ne değişiyor?"
    )
    languages = _CSS
    category = AuditCategory.ACCESSIBILITY
    default_severity = Severity.MEDIUM
    catalog_note = (
        "Yalnızca `:focus` (ama `:focus-visible` değil) içeren bloklar taranır: `outline: none` "
        "yanında aynı blokta `border`/`box-shadow`/`background`/`text-decoration` varsa ya da aynı "
        "seçici için ayrı bir `:focus-visible` kuralı yazılmışsa susar."
    )

    def check(self, ctx: RuleContext) -> list[Finding]:
        covered = _focus_visible_bases(ctx)
        found: list[Finding] = []
        for rule_set in ctx.nodes_in(ctx.root, "rule_set"):
            block = _block(rule_set)
            if block is None:
                continue
            parts = _focus_parts(_selectors(rule_set))
            if not parts:
                continue
            if any(part.split(":focus")[0].strip() in covered or "" in covered for part in parts):
                continue
            declarations = _declarations(block)
            outlines = [
                (value, node)
                for name, value, node in declarations
                if name == "outline" and _removes_outline(value)
            ]
            if not outlines:
                continue
            if any(name.startswith(_FOCUS_ALTERNATIVES) for name, _, _ in declarations):
                continue
            found += [self.finding(ctx, line(node)) for _, node in outlines]
        return found


def _media_only(selectors: str) -> bool:
    """Seçicinin tamamı görsel/işaretleme öğesi mi (metin kutusu değil)."""
    parts = [p.strip() for p in selectors.split(",") if p.strip()]
    return bool(parts) and all(
        (tag := _HEAD_TAG.match(p)) is not None and tag[0].lower() in _MEDIA_ELEMENTS for p in parts
    )


@register_rule
class FixedHeightForText(Rule):
    """CSS-LAYOUT-001: metin kutusunda sabit piksel yüksekliği (taşma)."""

    id = "CSS-LAYOUT-001"
    title = "Sabit yükseklikte metin kutusu"
    description = (
        "Kutunun yüksekliği pikselle sabitlenmiş. Metin uzayınca, yazı tipi büyüyünce ya da "
        "ekran daralınca fazlası nereye gider ve bunu kim fark eder?"
    )
    languages = _CSS
    category = AuditCategory.EDGE_CASE
    default_severity = Severity.LOW
    default_kind = FindingKind.SUGGESTION
    catalog_note = (
        "Yalnızca `height: <sayı>px` aranır; `min-height`/`max-height`, yüzde ve `rem` ile "
        "tümü görsel öğelerden (`img`, `svg`, `canvas`, `video`, `iframe`, `input` …) oluşan "
        "seçiciler kapsam dışıdır. Kutunun gerçekten metin içerdiği doğrulanamaz."
    )

    def check(self, ctx: RuleContext) -> list[Finding]:
        found: list[Finding] = []
        for rule_set in ctx.nodes_in(ctx.root, "rule_set"):
            block = _block(rule_set)
            if block is None or _media_only(_selectors(rule_set)):
                continue
            found += [
                self.finding(ctx, line(node))
                for name, value, node in _declarations(block)
                if name == "height" and _PX.match(value)
            ]
        return found


@register_rule
class NegativeMarginCentering(Rule):
    """CSS-LAYOUT-002: `left: 50%` + negatif `margin-left` ile ortalama."""

    id = "CSS-LAYOUT-002"
    title = "Negatif margin ile ortalama"
    description = (
        "Kutu `left: 50%` ile sağa itilip yarı genişliği kadar geri çekiliyor. Genişlik "
        "değişince o sabit sayı ne olur? Aynı sonucu genişlikten bağımsız nasıl alırsın?"
    )
    languages = _CSS
    category = AuditCategory.MAINTAINABILITY
    default_severity = Severity.LOW
    default_kind = FindingKind.SUGGESTION
    catalog_note = (
        "`position: absolute|fixed`, `left: 50%` ve negatif `margin-left` üçlüsü aynı blokta "
        "aranır; `transform: translateX(-50%)` gibi genişlikten bağımsız yöntemler kapsam dışıdır."
    )

    def check(self, ctx: RuleContext) -> list[Finding]:
        found: list[Finding] = []
        for block in ctx.nodes_in(ctx.root, "block"):
            values = {name: (value, node) for name, value, node in _declarations(block)}
            position = values.get("position")
            left = values.get("left")
            margin = values.get("margin-left")
            if position is None or position[0].lower() not in ("absolute", "fixed"):
                continue
            if left is None or left[0].replace(" ", "") != "50%":
                continue
            if margin is None or not _NEGATIVE_PX.match(margin[0]):
                continue
            found.append(self.finding(ctx, line(margin[1])))
        return found
