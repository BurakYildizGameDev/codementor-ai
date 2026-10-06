"""Tier 0 — tree-sitter ile sözdizimi ön doğrulaması (mimari §5.2.1).

Ağaçtaki `ERROR` ve `MISSING` düğümleri 1 tabanlı satır/kolonlu `Diagnostic`e
çevrilir. Kolonlar **karakter** cinsindendir (tree-sitter bayt verir; Türkçe
karakterli satırlarda kayma olmasın). Dosya sonunda kapanmamış bir blok,
tree-sitter'ın blok başına yerleştirdiği dev ERROR düğümü yerine son satırda
anlaşılır bir mesajla raporlanır; özet, blok hatasıyla aynı ERROR düğümüne
sarılan bağımsız bir `;` eksikliğini gizlemez (Faz 55 D2).
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass

from tree_sitter import Node

from codementor.analysis.parsers import ParsedSource, iter_nodes, parse
from codementor.ingest.normalize import split_lines
from codementor.models.enums import Language
from codementor.models.findings import Diagnostic
from codementor.models.request import NormalizedCode
from codementor.models.validation import Tier0Result

MAX_DIAGNOSTICS = 20
_SNIPPET_CHARS = 40
_STATEMENT_ENDS = frozenset({";", "{", "}", ":", ","})
_SEMICOLON_HINT = "Burada noktalı virgül (;) eksik olabilir."
# `;` ipucu yalnızca bu dillerde anlamlı (Faz 55 D2; Python/CSS'te deyim sonu `;` değil)
_SEMICOLON_LANGUAGES = frozenset({Language.C, Language.CPP, Language.CSHARP})
_ANON_STATEMENT_END = frozenset({")", "]"})  # çağrı/indeks sonu: ardından `;` makul
# `)` bu sözcüklerin başlığını kapatıyorsa ardından gövde gelir, `;` değil
_CONTROL_KEYWORDS = frozenset(
    {"if", "while", "for", "switch", "foreach", "catch", "using", "lock", "fixed"}
)

_MISSING_NAMES = {
    ";": "noktalı virgül (;)",
    "}": "kapanış süslü parantezi (})",
    ")": "kapanış parantezi ())",
    "]": "kapanış köşeli parantezi (])",
    ">": "kapanış açılı parantezi (>)",
    ":": "iki nokta (:)",
    ",": "virgül (,)",
    "identifier": "bir ad (tanımlayıcı)",
}


@dataclass(frozen=True, slots=True)
class _Position:
    line: int  # 1 tabanlı
    column: int  # 1 tabanlı, karakter


def _position(lines: list[str], row: int, byte_column: int) -> _Position:
    if not lines:
        return _Position(1, 1)
    if row >= len(lines):  # dosya sonundaki satır sonundan sonrası
        return _Position(len(lines), len(lines[-1]) + 1)
    prefix = lines[row].encode("utf-8")[:byte_column].decode("utf-8", errors="ignore")
    return _Position(row + 1, len(prefix) + 1)


def _is_error(node: Node) -> bool:
    return node.is_error or node.is_missing


def _error_nodes(root: Node) -> list[Node]:
    """En dıştaki ERROR/MISSING düğümleri, belge sırasıyla; temiz alt ağaçlara inilmez."""
    return [
        node
        for node in iter_nodes(root, descend=lambda n: n.has_error and not _is_error(n))
        if _is_error(node)
    ]


def _unclosed_brace_rows(root: Node) -> list[int]:
    """Eşi olmayan `{` simgelerinin satırları (0 tabanlı). Metin/yorum içindekiler sayılmaz."""
    open_rows: list[int] = []
    for node in iter_nodes(root):
        if node.child_count or node.is_missing:
            continue
        if node.type == "{":
            open_rows.append(node.start_point.row)
        elif node.type == "}" and open_rows:
            open_rows.pop()
    return open_rows


def _snippet(node: Node) -> str:
    text = (node.text or b"").decode("utf-8", errors="replace").strip()
    first = " ".join(text.split("\n", 1)[0].split())
    return first if len(first) <= _SNIPPET_CHARS else first[: _SNIPPET_CHARS - 1] + "…"


def _message(node: Node) -> str:
    if node.is_missing:
        name = _MISSING_NAMES.get(node.type, f"'{node.type}'")
        return f"Burada {name} eksik görünüyor."
    snippet = _snippet(node)
    return f"Beklenmeyen sözdizimi: '{snippet}'" if snippet else "Beklenmeyen sözdizimi."


def _diagnostic(pos: _Position, message: str) -> Diagnostic:
    return Diagnostic(
        tool="tree-sitter", severity="error", line=pos.line, column=pos.column, message=message
    )


class _CodeTokens:
    """Yorum ve MISSING olmayan yaprak simgeler (belge sırası; bitiş baytları artan)."""

    def __init__(self, root: Node) -> None:
        self.leaves = [
            n for n in iter_nodes(root) if not n.child_count and not n.is_extra and not n.is_missing
        ]
        self.ends = [n.end_byte for n in self.leaves]
        self.starts = [n.start_byte for n in self.leaves]

    @property
    def last_end(self) -> int:
        return self.ends[-1] if self.ends else 0

    def anchor(self, missing: Node) -> tuple[int, int]:
        """Eksik simgenin raporlanacağı (satır, bayt kolonu): önceki kod simgesinin hemen sonu.

        tree-sitter MISSING düğümünü araya giren yorumların arkasına yerleştirir;
        derleyiciler gibi hatayı eksik simgenin ait olduğu satırda göstermek için.
        """
        k = bisect_right(self.ends, missing.start_byte) - 1
        point = self.leaves[k].end_point if k >= 0 else missing.start_point
        return point.row, point.column

    def semicolon_gap(self, error: Node) -> tuple[int, int] | None:
        """ERROR içinde `}` öncesi deyim sonlandırılmamışsa `;` beklenen konum.

        Ör. C#'ta `{ total += v }` bir başlatıcı ifadesi sanılıp ERROR'a sarılır;
        asıl sorun `v`'den sonra eksik olan `;`'dür.
        """
        first = bisect_left(self.starts, error.start_byte)
        last = bisect_left(self.starts, error.end_byte)
        for k in range(max(first, 1), last):
            if self.leaves[k].type == "}" and self.leaves[k - 1].type not in _STATEMENT_ENDS:
                point = self.leaves[k - 1].end_point
                return point.row, point.column
        return None

    def trailing_semicolon_gap(self, dropped: list[Node]) -> tuple[int, int] | None:
        """Kapanmamış blok özeti için atılan ERROR düğümleri son deyimi yuttuysa `;` konumu.

        Faz 55 D2: `int main() { int x = 1` gibi girdide tree-sitter eksik `;`'yi
        blok hatasıyla tek ERROR düğümünde birleştirir; özet bu düğümü düşürür.
        Son kod yaprağı bir ifadenin doğal sonuysa (tanımlayıcı, sabit, tırnak;
        ya da çağrı/indeks sonu `)`/`]`) eksik `;` de ayrı tanı olarak döner.
        """
        if not self.leaves or not dropped:
            return None
        last = self.leaves[-1]
        if not any(
            n.start_byte <= last.start_byte and last.end_byte <= n.end_byte for n in dropped
        ):
            return None
        if last.type in _ANON_STATEMENT_END:
            if last.type == ")" and self._control_header(len(self.leaves) - 1):
                return None  # `if (x)` / `while (x)` sonrası `;` boş deyim olur, öneri yanıltır
        else:
            text = (last.text or b"").decode("utf-8", errors="replace")
            if not text or not (text[-1].isalnum() or text[-1] in "_\"'"):
                return None
            if not last.is_named and text.isidentifier():
                return None  # anahtar sözcük (`else`, `return`, `public` ...) deyim sonu değil
        return last.end_point.row, last.end_point.column

    def _control_header(self, close: int) -> bool:
        """`close` indeksindeki `)` bir denetim başlığını (`if (...)`, `for (...)`) kapatıyor mu."""
        depth = 0
        for k in range(close, -1, -1):
            kind = self.leaves[k].type
            if kind == ")":
                depth += 1
            elif kind == "(":
                depth -= 1
                if depth == 0:
                    return k > 0 and self.leaves[k - 1].type in _CONTROL_KEYWORDS
        return False


def _unclosed_diagnostic(lines: list[str], open_rows: list[int]) -> Diagnostic:
    last = max((i for i, line in enumerate(lines) if line.strip()), default=0)
    extra = f" ({len(open_rows)} blok)" if len(open_rows) > 1 else ""
    return _diagnostic(
        _Position(last + 1, len(lines[last]) + 1 if lines else 1),
        f"Satır {open_rows[0] + 1} ile başlayan blok kapanmamış görünüyor{extra}; "
        "dosyanın sonunda '}' eksik olabilir.",
    )


def run_tier0(code: NormalizedCode) -> Tier0Result:
    """Kodu ayrıştırır ve sözdizimi hatalarını tanıya çevirir."""
    parsed: ParsedSource = parse(code)
    root = parsed.tree.root_node
    if not root.has_error:
        return Tier0Result(diagnostics=[])

    lines = split_lines(parsed.text)
    errors = _error_nodes(root)
    tokens = _CodeTokens(root)
    semicolon_language = code.language in _SEMICOLON_LANGUAGES

    summary: Diagnostic | None = None
    trailing: tuple[int, int] | None = None
    open_rows = _unclosed_brace_rows(root)
    if open_rows and any(n.end_byte >= tokens.last_end for n in errors):
        # Kapanmamış blok: dosya sonuna uzayan hata düğümleri yerine tek, yerinde bir mesaj
        dropped = [n for n in errors if n.end_byte >= tokens.last_end]
        errors = [n for n in errors if n.end_byte < tokens.last_end]
        summary = _unclosed_diagnostic(lines, open_rows)
        if semicolon_language:  # Faz 55 D2: yutulan ERROR bağımsız `;` eksikliği taşır
            trailing = tokens.trailing_semicolon_gap(dropped)

    found: list[Diagnostic] = []
    if trailing is not None:
        found.append(_diagnostic(_position(lines, *trailing), _SEMICOLON_HINT))
    for node in errors:
        gap = None if node.is_missing or not semicolon_language else tokens.semicolon_gap(node)
        if gap is not None:
            found.append(_diagnostic(_position(lines, *gap), _SEMICOLON_HINT))
            continue
        row, byte_col = tokens.anchor(node) if node.is_missing else node.start_point
        found.append(_diagnostic(_position(lines, row, byte_col), _message(node)))

    unique = {(d.line, d.column, d.message): d for d in found}
    ordered = sorted(unique.values(), key=lambda d: (d.line, d.column or 0))
    room = MAX_DIAGNOSTICS - (summary is not None)  # özet mesaj üst sınırda asla düşmez
    kept = ordered[:room] + ([summary] if summary else [])
    return Tier0Result(diagnostics=kept, truncated=len(ordered) > room)
