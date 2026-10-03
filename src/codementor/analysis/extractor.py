"""K2 statik olgu çıkarımı (mimari §5.3.1).

`extract_facts(code)` tree-sitter ağacından `CodeFacts` üretir. Düğümler
`analysis/queries/{dil}/*.scm` sorgularıyla bulunur; bağlam (kapsayan fonksiyon, döngü
derinliği, en içteki döngü) tek bir cursor geçişinde hesaplanır — toplam süre girdi
boyutuyla doğrusaldır (§12).

Hiçbir durumda istisna fırlatmaz. Bölümler (döngüler, çağrılar, özyineleme, tahsisler,
motor sembolleri) birbirinden yalıtılmıştır: biri başarısız olursa yalnızca o bölüm boş
kalır ve uyarı eklenir; diğer olgular (ve Faz 6 kuralları) etkilenmez. Maliyet tablosu
okunamazsa maliyetler bilinmeden devam edilir.

Hata ayıklama: `uv run python -m codementor.analysis.extractor dosya.cs`
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import TypeVar

from tree_sitter import Node

from codementor.analysis import _engine, _loops, _memory, _recursion
from codementor.analysis._context import Ctx, contexts
from codementor.analysis._symbols import (
    CallName,
    NodeKey,
    call_name,
    function_name,
    key,
    line,
    operator_of,
    parameters,
    simple_name,
    text,
    type_table,
)
from codementor.analysis.call_costs import CostResolver, load_call_costs
from codementor.analysis.lexical import mask_non_code
from codementor.analysis.parsers import ParsedSource, iter_nodes, parse
from codementor.analysis.queries import captures
from codementor.config import get_settings
from codementor.models.enums import AllocationKind, Engine, Language
from codementor.models.facts import (
    AllocationFact,
    CallCostTable,
    CallFact,
    CodeFacts,
    DeallocationFact,
    EngineSymbols,
    FunctionFact,
    LoopFact,
    RecursionFact,
)
from codementor.models.request import NormalizedCode
from codementor.questions._loader import DataFileError

SYNTAX_WARNING = "Kodda sözdizimi hatası var; statik olgular eksik olabilir."
NO_FUNCTION_WARNING = "Fonksiyon bulunamadı; olgular dosya düzeyinde toplandı."
FAILURE_WARNING = "Statik olgular çıkarılamadı ({}); analiz olgusuz devam ediyor."
SECTION_WARNING = "{} olguları çıkarılamadı ({}); bu bölüm boş."
COSTS_WARNING = "Çağrı maliyeti tablosu okunamadı; çağrı maliyetleri bilinmiyor."

_USING_STD = re.compile(r"\busing\s+namespace\s+std\s*;")
_USING_LINQ = re.compile(r"\busing\s+System\.Linq\s*;")
_STRING_TYPES = frozenset({"string", "String", "std::string", "FString"})
_TYPE_DECLARATIONS = frozenset(
    {
        "class_specifier",
        "struct_specifier",
        "union_specifier",
        "enum_specifier",
        "class_declaration",
        "struct_declaration",
        "interface_declaration",
        "enum_declaration",
        "record_declaration",
        "class_definition",  # Python
    }
)

T = TypeVar("T")
_Call = tuple[Node, CallName, tuple[str, str] | None]


class _Extractor:
    def __init__(self, code: NormalizedCode, parsed: ParsedSource, costs: CallCostTable) -> None:
        self.code = code
        self.language = code.language
        self.root = parsed.tree.root_node
        self.masked = mask_non_code(code.text)
        self.types = type_table(self.root, self.language)
        self.found = {
            name: captures(self.language, name, self.root)
            for name in ("functions", "loops", "calls", "memory", "fields")
        }
        self.costs = costs
        self.loop_index: dict[NodeKey, int] = {}
        self.warnings: list[str] = []

    def _nodes(self, query: str, capture: str) -> list[Node]:
        return self.found[query].get(capture, [])

    def _section(self, label: str, build: Callable[[], T], empty: T) -> T:
        """Bölümü yalıtır: hata olursa uyarı + boş sonuç, diğer bölümler sürer."""
        try:
            return build()
        except Exception as exc:
            self.warnings.append(SECTION_WARNING.format(label, type(exc).__name__))
            return empty

    def run(self) -> CodeFacts:
        self.inert = (
            _engine.engine_inert_members(self.root, self.language)
            if self.code.engine is not Engine.NONE
            else frozenset[NodeKey]()
        )
        fn_nodes = self._nodes("functions", "function")
        functions = [self._function(n) for n in fn_nodes]
        self.by_key = {key(n): f for n, f in zip(fn_nodes, functions, strict=True)}
        self.fn_nodes = {key(n): n for n in fn_nodes}
        loops = self._nodes("loops", "loop")
        call_nodes = self._nodes("calls", "call")
        membership = self._nodes("calls", "membership")  # yalnız Python
        memory = [n for nodes in self.found["memory"].values() for n in nodes]
        wanted = {key(n) for n in [*loops, *call_nodes, *membership, *memory]}
        self.ctx = contexts(self.root, wanted, set(self.by_key))
        self.loop_index = {key(n): i for i, n in enumerate(loops)}
        resolver = CostResolver(
            table=self.costs,
            language=self.language,
            types=self.types,
            using_std=bool(_USING_STD.search(self.masked)),
            using_linq=bool(_USING_LINQ.search(self.masked)),
            user_functions=frozenset(simple_name(f.name) for f in functions),
        )
        calls: list[_Call] = self._section(
            "Çağrı",
            lambda: sorted(
                [
                    (n, name, resolver.resolve(name))
                    for n in call_nodes
                    for name in [call_name(n, self.language)]
                ]
                + self._memberships(membership, resolver),
                key=lambda c: c[0].start_byte,
            ),
            [],
        )
        facts = CodeFacts(functions=functions)
        facts.loops = self._section("Döngü", lambda: self._loops(loops), [])
        facts.calls = self._section(
            "Çağrı",
            lambda: sorted(
                [self._call(*c) for c in calls] + self._accumulations(),
                key=lambda c: c.line,
            ),
            [],
        )
        facts.recursion = self._section(
            "Özyineleme", lambda: self._recursion(fn_nodes, functions, calls), []
        )
        facts.allocations = self._section("Tahsis", lambda: self._allocations(calls), [])
        facts.deallocations = self._section("Serbest bırakma", self._deallocations, [])
        facts.engine_symbols = self._section(
            "Motor sembolü",
            lambda: _engine.engine_symbols(
                language=self.language,
                engine=self.code.engine,
                original=self.code.text,
                fields=self.found["fields"],
                functions=functions,
                calls=[(name, line(n)) for n, name, _ in calls],
            ),
            EngineSymbols(),
        )
        if self.root.has_error:
            facts.warnings.append(SYNTAX_WARNING)
        if not functions and not self._declares_types():
            facts.warnings.append(NO_FUNCTION_WARNING)
        facts.warnings += self.warnings
        return facts

    def _owner(self, node: Node) -> FunctionFact | None:
        here = self.ctx.get(key(node))
        return self.by_key.get(here.function) if here and here.function else None

    def _declares_types(self) -> bool:
        """Yalnızca bildirim içeren başlık/arayüz dosyası mı (uyarı gerektirmez)."""
        return any(n.type in _TYPE_DECLARATIONS for n in iter_nodes(self.root))

    def _function(self, node: Node) -> FunctionFact:
        name = function_name(node, self.language)
        lifecycle, hot = _engine.lifecycle(name, self.code.engine)
        if key(node) in self.inert:  # tabanı olmayan tipte: motor çağırmaz (Faz 21)
            lifecycle, hot = None, False
        return FunctionFact(
            name=name,
            line_start=line(node),
            line_end=node.end_point[0] + 1,
            parameters=parameters(node, self.language),
            lifecycle=lifecycle,
            is_hot_path=hot,
        )

    def _index(self, loop: Node | None) -> int | None:
        """Döngünün `facts.loops` içindeki indeksi (aynı satırdaki döngüler ayrışır)."""
        return self.loop_index.get(key(loop)) if loop is not None else None

    def _loops(self, loops: list[Node]) -> list[LoopFact]:
        indexes: dict[NodeKey | None, _loops.AssignmentIndex] = {}
        resets: dict[NodeKey, set[str]] = {}  # dış döngü başına bir kez (O1: doğrusal)
        result: list[LoopFact] = []
        for loop in loops:
            here = self.ctx[key(loop)]
            scope_key = here.function
            if scope_key not in indexes:
                scope = self.fn_nodes[scope_key] if scope_key is not None else self.root
                indexes[scope_key] = _loops.AssignmentIndex.build(scope)
            shape = _loops.classify(loop, indexes[scope_key])
            parent = here.loop
            outer = False
            if parent is not None:
                parent_key = key(parent)
                if parent_key not in resets:
                    resets[parent_key] = _loops.resets_in_body(parent)
                outer = _loops.counter_outer(loop, shape.counter, resets[parent_key])
            result.append(
                LoopFact(
                    kind=_loops.kind_of(loop),
                    line=line(loop),
                    depth=here.depth + 1,
                    bound=shape.bound,
                    function=_name(self._owner(loop)),
                    function_line=_start(self._owner(loop)),
                    parent_line=line(parent) if parent is not None else None,
                    parent_index=self._index(parent),
                    counter_outer=outer,
                )
            )
        return result

    def _memberships(self, nodes: list[Node], resolver: CostResolver) -> list[_Call]:
        """`x in xs` (Python): alıcının tipi biliniyorsa `tip.__contains__` maliyeti."""
        found: list[_Call] = []
        for node in nodes:
            operators = {c.type for c in node.children if not c.is_named}
            if not operators & {"in", "not in"} or node.named_child_count != 2:
                continue
            target = node.named_children[1]
            if target.type != "identifier":
                continue
            receiver = text(target)
            name = CallName(f"{receiver} içinde arama", "__contains__", receiver, None, 1)
            resolved = resolver.resolve(name)
            if resolved is not None:  # tipi bilinmeyen üyelik olgu üretmez (tahmin yok)
                found.append((node, name, resolved))
        return found

    def _call(self, node: Node, name: CallName, resolved: tuple[str, str] | None) -> CallFact:
        here = self.ctx.get(key(node), Ctx())
        return CallFact(
            name=resolved[0] if resolved else name.display,
            line=line(node),
            loop_depth=here.depth,
            known_cost=resolved[1] if resolved else None,
            function=_name(self._owner(node)),
            function_line=_start(self._owner(node)),
            loop_line=line(here.loop) if here.loop is not None else None,
            loop_index=self._index(here.loop),
        )

    def _recursion(
        self, fn_nodes: list[Node], functions: list[FunctionFact], calls: list[_Call]
    ) -> list[RecursionFact]:
        by_function: dict[NodeKey, list[tuple[Node, CallName]]] = {}  # O2: gruplama
        for node, name, _ in calls:
            owner = self.ctx[key(node)].function
            if owner is not None:
                by_function.setdefault(owner, []).append((node, name))
        result: list[RecursionFact] = []
        for node, fact in zip(fn_nodes, functions, strict=True):
            own = [
                call
                for call, name in by_function.get(key(node), [])
                if _recursion.is_self_call(name, fact.name)
            ]
            if not own or _recursion.imports_same_name(node, fact.name):
                continue
            in_loop = any(self.ctx[key(call)].depth > 0 for call in own)
            result.append(
                RecursionFact(
                    function=fact.name,
                    self_call_count=len(own),
                    branching_factor=_recursion.branching_factor(node, own, in_loop),
                    lines=sorted({line(call) for call in own}),
                    halving=_recursion.halves(own),
                )
            )
        return result

    def _accumulations(self) -> list[CallFact]:
        """Döngüde metin biriktirme (Faz 32): her tur birikmiş metni kopyalar, yani tur başına
        O(n). C#'ta `s += x` ve `s = s + x` (string değişmez); C++'ta yalnız `s = s + x`
        (`s += x` yerinde, amortize sabit büyür). Döngü dışındaki birleştirme olgu üretmez."""
        if self.language not in (Language.CSHARP, Language.CPP):
            return []
        strings = {name for name, t in self.types.items() if t in _STRING_TYPES}
        found: list[CallFact] = []
        for node in self.found["memory"].get("concat_assign", []):
            here = self.ctx.get(key(node))
            if here is None or here.depth == 0:
                continue
            target = text(node.child_by_field_name("left")).removeprefix("this.")
            if target not in strings:
                continue
            operator = operator_of(node)
            appends = operator == "+=" and self.language is Language.CSHARP
            rebuilds = (
                operator == "=" and _leftmost_operand(node.child_by_field_name("right")) == target
            )
            if not (appends or rebuilds):
                continue
            owner = self._owner(node)
            found.append(
                CallFact(
                    name=f"{target} metin birleştirme (her turda kopya)",
                    line=line(node),
                    loop_depth=here.depth,
                    known_cost="n",
                    function=_name(owner),
                    function_line=_start(owner),
                    loop_line=line(here.loop) if here.loop is not None else None,
                    loop_index=self._index(here.loop),
                )
            )
        return found

    def _allocations(self, calls: list[_Call]) -> list[AllocationFact]:
        string_vars = {name for name, t in self.types.items() if t in _STRING_TYPES}
        value_types = (
            _memory.file_value_types(self.root)
            if self.language is Language.CSHARP
            else frozenset[str]()
        )
        pairs = list(
            _memory.allocations(self.language, self.found["memory"], string_vars, value_types)
        )
        # LINQ: `Enumerable.*` olarak çözülen çağrılar (`Mathf.Max` LINQ değil); O(1)'e
        # indirgenen argümansız `First()`/`Any()` yineleyici tahsis etmez
        pairs += [
            (AllocationKind.LINQ, n)
            for n, _, resolved in calls
            if resolved is not None and resolved[0].startswith("Enumerable.") and resolved[1] != "1"
        ]
        result = []
        for kind, node in pairs:
            fn = self._owner(node)
            here = self.ctx.get(key(node), Ctx())
            result.append(
                AllocationFact(
                    kind=kind,
                    line=line(node),
                    loop_depth=here.depth,
                    in_hot_path=bool(fn and fn.is_hot_path),
                    function=_name(fn),
                )
            )
        return sorted(result, key=lambda a: (a.line, a.kind.value))

    def _deallocations(self) -> list[DeallocationFact]:
        found = [
            DeallocationFact(kind=kind, line=line(n), function=_name(self._owner(n)))
            for kind, n in _memory.deallocations(self.found["memory"])
        ]
        return sorted(found, key=lambda d: d.line)


def _name(fn: FunctionFact | None) -> str | None:
    return fn.name if fn is not None else None


def _start(fn: FunctionFact | None) -> int | None:
    return fn.line_start if fn is not None else None


_MAX_CHAIN = 64  # `a + b + ... ` zincirinde en soldaki işlenene kadar en fazla bu kadar adım


def _leftmost_operand(node: Node | None) -> str | None:
    """`s + a + b` → `s` (yalnız `+` zinciri); başka ifadede None."""
    for _ in range(_MAX_CHAIN):
        if node is None or node.type != "binary_expression" or operator_of(node) != "+":
            break
        node = node.child_by_field_name("left")
    else:
        return None
    if node is None or node.type not in (
        "identifier",
        "member_access_expression",
        "field_expression",
    ):
        return None
    return text(node).removeprefix("this.")


def extract_facts(
    code: NormalizedCode,
    parsed: ParsedSource | None = None,
    *,
    costs: CallCostTable | None = None,
) -> CodeFacts:
    """Kodun statik olguları; istisna fırlatmaz (sorun olursa eksik/boş olgu + uyarı)."""
    warnings: list[str] = []
    if costs is None:
        try:
            costs = load_call_costs(get_settings().data.call_costs_file)
        except DataFileError:
            costs = CallCostTable()
            warnings.append(COSTS_WARNING)
    try:
        facts = _Extractor(code, parsed if parsed is not None else parse(code), costs).run()
    except Exception as exc:  # sözleşme: analiz olgusuz da devam edebilmeli
        facts = CodeFacts(warnings=[FAILURE_WARNING.format(type(exc).__name__)])
    facts.warnings = warnings + facts.warnings
    return facts


def main(argv: list[str] | None = None) -> int:
    """Hata ayıklama CLI'ı (bkz. `analysis/_cli.py`)."""
    from codementor.analysis._cli import run

    return run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
