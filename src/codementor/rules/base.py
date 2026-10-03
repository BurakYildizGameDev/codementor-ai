"""Kural arayüzü ve bağlamı (mimari §5.3.3).

Kurallar önce Faz 5 olgularını (`CodeFacts`) kullanır; ağaca yalnızca olgularda olmayan
bilgi için iner. Ağaç gezintileri `iter_nodes` ile yapılır ve `Node.parent` kullanılmaz
(tree-sitter'da O(derinlik); 40 KB girdide karesel süre, mimari §12).
"""

from __future__ import annotations

from bisect import bisect_right
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar

from tree_sitter import Node

from codementor.analysis._symbols import function_name, line, simple_name, type_table
from codementor.analysis.parsers import ParsedSource, iter_nodes
from codementor.analysis.queries import captures
from codementor.models.enums import AuditCategory, Engine, FindingSource, Language, Severity
from codementor.models.facts import CodeFacts, FunctionFact
from codementor.models.findings import Finding
from codementor.models.rules import RuleInfo

MAX_EVIDENCE = 200
_LOOP_TYPES = (
    "for_statement",
    "for_range_loop",
    "foreach_statement",
    "while_statement",
    "do_statement",
    # Python kavramaları (ADR-0015)
    "list_comprehension",
    "set_comprehension",
    "dictionary_comprehension",
    "generator_expression",
)
_MAX_BYTE = 1 << 62


@dataclass(frozen=True)
class FunctionNode:
    """Olgudaki fonksiyon ve ağaçtaki düğümü."""

    fact: FunctionFact
    node: Node


@dataclass
class RuleContext:
    """Bir kod parçası için kuralların ortak girdisi."""

    language: Language
    engine: Engine
    lines: list[str]
    facts: CodeFacts
    parsed: ParsedSource

    @property
    def root(self) -> Node:
        """Ayrıştırma ağacının kökü."""
        return self.parsed.tree.root_node

    def line_text(self, number: int) -> str:
        """1 tabanlı satırın kırpılmış metni (kanıt alanı için; en fazla 200 karakter)."""
        if not 1 <= number <= len(self.lines):
            return ""
        stripped = self.lines[number - 1].strip()
        return stripped if len(stripped) <= MAX_EVIDENCE else stripped[: MAX_EVIDENCE - 1] + "…"

    @cached_property
    def function_nodes(self) -> list[FunctionNode]:
        """Fonksiyon olguları ağaç düğümleriyle; eşleşme ad + başlangıç satırıyla."""
        by_key = {(f.name, f.line_start): f for f in self.facts.functions}
        result: list[FunctionNode] = []
        for node in captures(self.language, "functions", self.root).get("function", []):
            fact = by_key.get((function_name(node, self.language), line(node)))
            if fact is not None:
                result.append(FunctionNode(fact, node))
        return result

    @cached_property
    def types(self) -> dict[str, str]:
        """Değişken/alan adı → bildirilen temel tip (belirsiz adlar yok)."""
        return type_table(self.root, self.language)

    @cached_property
    def hot_functions(self) -> frozenset[str]:
        """Sıcak yoldaki (Update, Tick ...) fonksiyon adları (yalnız görüntüleme/ipucu için)."""
        return frozenset(f.name for f in self.facts.functions if f.is_hot_path)

    @cached_property
    def hot_function_lines(self) -> frozenset[int]:
        """Sıcak fonksiyonların kimliği (ilk satır). Eşleme ada göre yapılmaz: aynı dosyada
        tabansız bir sınıfın `Update`'i sıcak değildir (Faz 21 denetimi O3, Faz 32)."""
        return frozenset(f.line_start for f in self.facts.functions if f.is_hot_path)

    def in_hot_function(self, function_line: int | None) -> bool:
        """Olgunun (çağrı, döngü) sahibi fonksiyon sıcak yolda mı."""
        return function_line is not None and function_line in self.hot_function_lines

    @cached_property
    def _loop_bodies(self) -> list[tuple[int, int]]:
        """En dıştaki döngü gövdelerinin bayt aralıkları (sıralı, çakışmasız)."""
        spans: list[tuple[int, int]] = []
        for loop in self.nodes_in(self.root, *_LOOP_TYPES):
            body = loop.child_by_field_name("body") or loop
            if spans and body.start_byte < spans[-1][1]:
                continue  # dıştaki döngünün içinde; belge sırası dıştakini önce verir
            spans.append((body.start_byte, body.end_byte))
        return spans

    def in_loop(self, node: Node) -> bool:
        """Düğüm bir döngü gövdesinde mi (O(log n); `Node.parent` kullanılmaz)."""
        spans = self._loop_bodies
        index = bisect_right(spans, (node.start_byte, _MAX_BYTE)) - 1
        return index >= 0 and node.start_byte < spans[index][1]

    def functions_named(self, *names: str) -> list[FunctionNode]:
        """Basit adı verilenlerden biri olan fonksiyonlar (`AFoo::Tick` → `Tick`)."""
        wanted = set(names)
        return [f for f in self.function_nodes if simple_name(f.fact.name) in wanted]

    def nodes_in(self, root: Node, *types: str) -> Iterator[Node]:
        """`root` altındaki verilen türden düğümler (belge sırasıyla)."""
        wanted = set(types)
        return (n for n in iter_nodes(root) if n.type in wanted)


class Rule:
    """Statik kural tabanı; alt sınıflar sınıf özniteliklerini ve `check`'i tanımlar."""

    id: ClassVar[str]
    title: ClassVar[str]
    description: ClassVar[str]
    languages: ClassVar[frozenset[Language]]
    engines: ClassVar[frozenset[Engine]] = frozenset()  # boş: motordan bağımsız
    category: ClassVar[AuditCategory]
    default_severity: ClassVar[Severity]
    confidence: ClassVar[float] = 0.9

    def check(self, ctx: RuleContext) -> list[Finding]:
        """Bulgular (satır sırası önemsiz; motor sıralar ve numaralar)."""
        raise NotImplementedError

    @classmethod
    def applies_to(cls, language: Language, engine: Engine) -> bool:
        """Dil eşleşmeli; motora özgü kural yalnızca o motorda çalışır."""
        return language in cls.languages and (not cls.engines or engine in cls.engines)

    @classmethod
    def info(cls) -> RuleInfo:
        """Katalog satırı."""
        return RuleInfo(
            id=cls.id,
            title=cls.title,
            description=cls.description,
            languages=sorted(cls.languages),
            engines=sorted(cls.engines),
            category=cls.category,
            severity=cls.default_severity,
        )

    def finding(
        self,
        ctx: RuleContext,
        line_start: int,
        *,
        description: str | None = None,
        evidence: str | None = None,
        line_end: int | None = None,
    ) -> Finding:
        """Kural kimliğiyle doldurulmuş statik bulgu (`id` motor tarafından verilir)."""
        return Finding(
            id="F-000",
            rule_id=self.id,
            category=self.category,
            severity=self.default_severity,
            line_start=line_start,
            line_end=line_end,
            evidence=evidence if evidence is not None else ctx.line_text(line_start),
            description=description or self.description,
            source=FindingSource.STATIC,
            confidence=self.confidence,
        )
