"""HTML etiket dengesi (Faz 20): kapanmayan, eşi olmayan ve iç içe karışan etiketler.

tree-sitter-html dengesiz etiketlerde tutarsızdır (tam belgede eşi olmayan `</div>` hata
değil, `<div><span>x</div>` hiç işaretlenmez); bu yüzden kural ağaç yerine stdlib
`html.parser` ile kendi açık etiket yığınını tutar. Tarayıcılar hoşgörülü olduğundan bu bir
sözdizimi hatası değil, bulgu olarak raporlanır (ADR-0015 notu). HTML5'in tam ağaç kurma
algoritması değil, sade bir örtük kapanış tablosu kullanılır: emin olunmayan durumda kaçırma.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Literal

from codementor.models.enums import AuditCategory, Language, Severity
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

VOID = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)
# Kapanışı yazılmayabilen öğeler: açık kalmaları ya da örtük kapanmaları bulgu değildir
OPTIONAL_END = frozenset(
    {
        "p",
        "li",
        "dt",
        "dd",
        "tr",
        "td",
        "th",
        "thead",
        "tbody",
        "tfoot",
        "option",
        "optgroup",
        "colgroup",
        "caption",
        "rb",
        "rt",
        "rp",
        "html",
        "head",
        "body",
    }
)
# Eşi olmayan kapanışı raporlanmayan belge iskeleti (örtük açılıp kapanırlar)
_SKELETON = frozenset({"html", "head", "body"})
_CLOSES_P = frozenset(
    {
        "address",
        "article",
        "aside",
        "blockquote",
        "details",
        "div",
        "dl",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hgroup",
        "hr",
        "main",
        "menu",
        "nav",
        "ol",
        "p",
        "pre",
        "section",
        "table",
        "ul",
    }
)
_TABLE_SECTIONS = frozenset({"thead", "tbody", "tfoot", "tr", "td", "th"})
# açılan etiket → yığının tepesinde bulununca örtük kapattığı öğeler
_IMPLICIT: dict[str, frozenset[str]] = {
    **dict.fromkeys(_CLOSES_P, frozenset({"p"})),
    "li": frozenset({"li"}),
    "dt": frozenset({"dt", "dd"}),
    "dd": frozenset({"dt", "dd"}),
    "tr": frozenset({"tr", "td", "th"}),
    "td": frozenset({"td", "th"}),
    "th": frozenset({"td", "th"}),
    "thead": _TABLE_SECTIONS,
    "tbody": _TABLE_SECTIONS,
    "tfoot": _TABLE_SECTIONS,
    "option": frozenset({"option"}),
    "optgroup": frozenset({"option", "optgroup"}),
    "body": frozenset({"head"}),
}


# Kapsam sınırları: tarayıcı, sınırın dışında açılmış bir öğenin kapanışını yok sayar
# (`<div><table><tr><td></div>` → `</div>` eşsiz; tablo ve div bozulmaz)
_HARD_BOUNDS = frozenset({"table", "template", "object", "marquee", "applet"})
_CELL_BOUNDS = frozenset({"td", "th", "caption"})
_TABLE_TAGS = frozenset(
    {"table", "thead", "tbody", "tfoot", "tr", "td", "th", "caption", "colgroup"}
)
# İçeriği metin olan öğeler; HTMLParser'ın bu listesi Python yama sürümüne göre değiştiği için
# kural kendisi ayarlar (`<title>a </div></title>` her sürümde etiket sayılmaz)
_RAW_TEXT = frozenset({"title", "textarea", "xmp", "iframe", "noembed", "noframes"})
_FOREIGN = ("svg", "math")  # içlerinde `<x/>` gerçekten kendini kapatır


@dataclass(frozen=True)
class Imbalance:
    line: int
    kind: Literal["unclosed", "stray"]
    tag: str


class _Balance(HTMLParser):
    """Açık etiket yığını. Ad → yığın konumları ve sınır konumları ayrıca tutulur; böylece
    üyelik ve kapsam denetimi O(1), yığından çıkarma amorti doğrusal (mimari §12)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.positions: dict[str, list[int]] = defaultdict(list)
        self.hard_bounds: list[int] = []
        self.cell_bounds: list[int] = []
        self.found: list[Imbalance] = []

    def _push(self, tag: str) -> None:
        index = len(self.stack)
        self.stack.append((tag, self.getpos()[0]))
        self.positions[tag].append(index)
        if tag in _HARD_BOUNDS:
            self.hard_bounds.append(index)
        if tag in _HARD_BOUNDS or tag in _CELL_BOUNDS:
            self.cell_bounds.append(index)

    def _pop(self) -> tuple[str, int]:
        tag, line = self.stack.pop()
        self.positions[tag].pop()
        index = len(self.stack)
        if self.hard_bounds and self.hard_bounds[-1] == index:
            self.hard_bounds.pop()
        if self.cell_bounds and self.cell_bounds[-1] == index:
            self.cell_bounds.pop()
        return tag, line

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        closes = _IMPLICIT.get(tag)  # boş `hr` de açık `p`'yi kapatır
        while closes and self.stack and self.stack[-1][0] in closes:
            self._pop()
        if tag in VOID:
            return
        self._push(tag)
        if tag in _RAW_TEXT:
            self.set_cdata_mode(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # `<br/>` ve SVG/MathML `<path/>` kendini kapatır; HTML'de `<div/>`, `<script/>` ise
        # açık kalır (tarayıcı `/`'ı yok sayar; JSX alışkanlığı)
        if tag in VOID or any(self.positions[f] for f in _FOREIGN):
            return
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID:
            return
        opened = self.positions[tag]
        bounds = self.hard_bounds if tag in _TABLE_TAGS else self.cell_bounds
        if not opened or (bounds and bounds[-1] > opened[-1]):
            if tag not in _SKELETON:
                self.found.append(Imbalance(self.getpos()[0], "stray", tag))
            return
        while self.stack:
            name, line = self._pop()
            if name == tag:
                return
            if name not in OPTIONAL_END:
                self.found.append(Imbalance(line, "unclosed", name))

    def finish(self) -> list[Imbalance]:
        self.close()
        self.found += [
            Imbalance(line, "unclosed", name)
            for name, line in self.stack
            if name not in OPTIONAL_END
        ]
        return self.found


def imbalances(source: str) -> list[Imbalance]:
    """Kaynaktaki dengesiz etiketler (satır sırası önemsiz)."""
    parser = _Balance()
    parser.feed(source)
    return parser.finish()


@register_rule
class UnbalancedTag(Rule):
    """HTML-STD-003: kapanmayan, eşi olmayan ya da iç içe karışan etiket."""

    id = "HTML-STD-003"
    title = "Dengesiz etiket"
    description = (
        "Bu etiket nerede kapanıyor? Kapanışı tarayıcı kendisi tahmin ederse sayfanın yapısı "
        "senin düşündüğünle aynı kalır mı?"
    )
    STRAY_DESCRIPTION = (
        "Bu kapanış etiketinin açılışı nerede? Tarayıcı eşi olmayan bir kapanışla "
        "karşılaşınca ne yapıyor olabilir?"
    )
    languages = frozenset({Language.HTML})
    category = AuditCategory.DESIGN
    default_severity = Severity.MEDIUM

    def check(self, ctx: RuleContext) -> list[Finding]:
        return [
            self.finding(
                ctx,
                item.line,
                description=self.STRAY_DESCRIPTION if item.kind == "stray" else None,
            )
            for item in imbalances(ctx.parsed.text)
        ]
