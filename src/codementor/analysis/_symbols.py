"""Düğüm adlandırma ve basit tip tablosu (olgu çıkarımı yardımcıları).

- Fonksiyon adı/parametreleri (C/C++ bildirici zinciri, C# `name` alanı).
- Çağrı adı: `strlen`, `std::sort`, `v.push_back`, `list.Contains`, `GetComponent`.
- Tip tablosu: dosyadaki bildirimlerden değişken adı → temel tip (`vector`, `List`, `TArray`).
  Kapsam yok sayılır; aynı ada birden çok tip bağlanmışsa belirsizdir ve çözülmez.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from tree_sitter import Node

from codementor.analysis.parsers import iter_nodes
from codementor.models.enums import Language

NodeKey = tuple[int, int, str]

_MAX_NAME = 80
_TEMPLATE_ARGS = re.compile(r"<[^<>]*>")
_WS = re.compile(r"\s+")
_DECLARATOR_WRAPPERS = frozenset(
    {
        "pointer_declarator",
        "reference_declarator",
        "array_declarator",
        "init_declarator",
        "parenthesized_declarator",
        "attributed_declarator",
        "function_declarator",
    }
)
_NAME_TYPES = frozenset(
    {
        "identifier",
        "field_identifier",
        "qualified_identifier",
        "destructor_name",
        "operator_name",
        "type_identifier",
    }
)
_CSHARP_STRING_INIT = frozenset(
    {
        "string_literal",
        "verbatim_string_literal",
        "raw_string_literal",
        "interpolated_string_expression",
    }
)
_TYPE_QUALIFIERS = re.compile(
    r"\b(const|volatile|static|mutable|constexpr|struct|class|unsigned)\b"
)


def key(node: Node) -> NodeKey:
    """Düğümü sözlükte anahtar olarak kullanmak için kimlik."""
    return (node.start_byte, node.end_byte, node.type)


def text(node: Node | None) -> str:
    """Düğüm metni (UTF-8); boşluklar tekilleştirilir."""
    if node is None or node.text is None:
        return ""
    return _WS.sub(" ", node.text.decode("utf-8", errors="replace")).strip()


def line(node: Node) -> int:
    """1 tabanlı satır."""
    return node.start_point[0] + 1


def operator_of(node: Node) -> str:
    """İkili/atama ifadesinin işleci (`+`, `+=`, `<` ...); yoksa boş dizge."""
    op = node.child_by_field_name("operator")
    if op is not None:
        return op.type
    return next((c.type for c in node.children if not c.is_named), "")


def clip(name: str) -> str:
    """Olgu adlarını makul uzunlukta tutar (kullanıcı kodu sınırsız uzunlukta olabilir)."""
    return name if len(name) <= _MAX_NAME else name[: _MAX_NAME - 1] + "…"


def strip_templates(name: str) -> str:
    """`std::map<int, std::vector<int>>::find` → `std::map::find` (iç içe de)."""
    previous = None
    while previous != name:
        previous, name = name, _TEMPLATE_ARGS.sub("", name)
    return name.replace(" ", "")


def declarator_name(node: Node | None) -> Node | None:
    """C/C++ bildirici zincirinin sonundaki ad düğümü."""
    while node is not None and node.type not in _NAME_TYPES:
        inner = node.child_by_field_name("declarator")
        if inner is None:
            inner = next((c for c in node.named_children if c.type in _NAME_TYPES), None)
            if inner is None and node.type in _DECLARATOR_WRAPPERS:
                inner = next(iter(node.named_children), None)
        node = inner
    return node


def function_name(node: Node, language: Language) -> str:
    """Fonksiyon adı; C++'ta nitelikli ad korunur (`AFoo::Tick`)."""
    if language in (Language.CSHARP, Language.PYTHON):
        return text(node.child_by_field_name("name")) or "<anonim>"
    return strip_templates(text(declarator_name(node.child_by_field_name("declarator")))) or (
        "<anonim>"
    )


def simple_name(name: str) -> str:
    """`AFoo::Tick` → `Tick`, `this.Foo` → `Foo`."""
    return re.split(r"::|\.|->", name)[-1]


def parameters(node: Node, language: Language) -> list[str]:
    """Parametre adları (sırasıyla)."""
    if language is Language.PYTHON:
        return _python_parameters(node)
    if language is Language.CSHARP:
        plist = node.child_by_field_name("parameters")
        if plist is None:
            return []
        return [
            text(p.child_by_field_name("name"))
            for p in plist.named_children
            if p.type == "parameter"
        ]
    declarator = node.child_by_field_name("declarator")
    while declarator is not None and declarator.type != "function_declarator":
        declarator = declarator.child_by_field_name("declarator")
    plist = declarator.child_by_field_name("parameters") if declarator is not None else None
    if plist is None:
        return []
    names = []
    for param in plist.named_children:
        name = declarator_name(param.child_by_field_name("declarator"))
        if name is not None:
            names.append(text(name))
    return names


_PY_PARAM_TYPES = frozenset(
    {
        "identifier",
        "typed_parameter",
        "default_parameter",
        "typed_default_parameter",
        "list_splat_pattern",
        "dictionary_splat_pattern",
    }
)


def _python_parameters(node: Node) -> list[str]:
    """`def f(a, b: int, c=1, *args, **kw)` → ["a", "b", "c", "args", "kw"]."""
    plist = node.child_by_field_name("parameters")
    names: list[str] = []
    for param in plist.named_children if plist is not None else []:
        if param.type not in _PY_PARAM_TYPES:
            continue
        if param.type == "identifier":
            names.append(text(param))
            continue
        name = param.child_by_field_name("name") or next(
            (c for c in param.named_children if c.type == "identifier"), None
        )
        if name is not None:
            names.append(text(name))
    return names


_MAX_RECEIVER_BYTES = 120
_CALL_TYPES = frozenset({"call_expression", "invocation_expression", "call"})


@dataclass(frozen=True)
class CallName:
    """Çağrının parçaları: `recv.method(...)` / `ns::func(...)` / `func(...)`.

    `chained`: alıcı başka bir çağrının sonucu (`xs.Where(...).ToList()`).
    Uzun alıcı ifadeleri okunmaz (`…`): zincir boyunca metin kopyalamak karesel olurdu.
    `first_arg`: ilk argümanın kısa metni (`items.Count - 1`); argüman yoksa None.
    Maliyet çözümleyicisi indeks desenlerini bununla ayırt eder (Faz H3).
    """

    display: str
    method: str
    receiver: str | None
    qualified: str | None
    arg_count: int = 0
    chained: bool = False
    first_arg: str | None = None


def _arg_count(node: Node) -> int:
    args = node.child_by_field_name("arguments")
    return args.named_child_count if args is not None else 0


def _first_argument(node: Node) -> str | None:
    """İlk argümanın metni; argüman yoksa (ya da çok uzunsa `…`) None/`…`.

    Uzun argümanda metin okunmaz: ölçek kullanıcı koduna bağlı (mimari §12) ve argüman
    olgu adına değil yalnızca indeks desenlerine bakılır.
    """
    args = node.child_by_field_name("arguments")
    if args is None or not args.named_child_count:
        return None
    if (first := args.named_child(0)) is None:
        return None
    if first.end_byte - first.start_byte > _MAX_RECEIVER_BYTES:
        return "…"
    return clip(text(first))


def _receiver(node: Node | None) -> tuple[str, bool]:
    """(alıcı metni, zincir mi); uzun ifadede metin yerine `…`."""
    if node is None:
        return "<?>", False
    chained = node.type in _CALL_TYPES
    if node.end_byte - node.start_byte > _MAX_RECEIVER_BYTES:
        return "…", chained
    return strip_templates(text(node)), chained


def call_name(node: Node, language: Language) -> CallName:
    """Çağrı ifadesinin adı; genel tip argümanları atılır."""
    fn = node.child_by_field_name("function")
    count = _arg_count(node)
    first = _first_argument(node)
    if fn is None:
        return CallName("<?>", "<?>", None, None, count, False, first)
    if fn.type in ("field_expression", "member_access_expression", "attribute"):
        receiver_node = (
            fn.child_by_field_name("argument")
            or fn.child_by_field_name("expression")
            or fn.child_by_field_name("object")
        )
        method_node = (
            fn.child_by_field_name("field")
            or fn.child_by_field_name("name")
            or fn.child_by_field_name("attribute")
        )
        method = _bare(method_node)
        receiver, chained = _receiver(receiver_node)
        return CallName(clip(f"{receiver}.{method}"), method, receiver, None, count, chained, first)
    if fn.type == "qualified_identifier":
        qualified = strip_templates(text(fn))
        return CallName(
            clip(qualified), simple_name(qualified), None, qualified, count, False, first
        )
    method = _bare(fn)
    return CallName(clip(method), method, None, None, count, False, first)


def _bare(node: Node | None) -> str:
    """`GetComponent<Rigidbody>` / `make_unique<T>` → ad."""
    if node is None:
        return "<?>"
    if node.type in ("generic_name", "template_function", "template_method"):
        inner = node.child_by_field_name("name") or next(iter(node.named_children), None)
        return text(inner)
    return strip_templates(text(node))


def _base_type(type_node: Node | None) -> str | None:
    """`const std::vector<int>&` → `std::vector`; `List<int>` → `List`; C# `int[]` → `Array`."""
    if type_node is None:
        return None
    if type_node.type == "array_type":
        return "Array"
    cleaned = strip_templates(_TYPE_QUALIFIERS.sub("", text(type_node))).strip("&*[] ?")
    if not cleaned or not re.fullmatch(r"[A-Za-z_][\w:.]*", cleaned):
        return None
    return cleaned


def _csharp_bindings(node: Node) -> list[tuple[str, str | None]]:
    """C# bildiriminden (ad, temel tip) çiftleri; `var x = new T()` için T."""
    if node.type in ("parameter", "property_declaration"):
        return [
            (text(node.child_by_field_name("name")), _base_type(node.child_by_field_name("type")))
        ]
    if node.type != "variable_declaration":
        return []
    type_node = node.child_by_field_name("type")
    pairs: list[tuple[str, str | None]] = []
    for declarator in node.named_children:
        if declarator.type != "variable_declarator":
            continue
        name = text(declarator.child_by_field_name("name"))
        if type_node is not None and type_node.type == "implicit_type":
            created = next(
                (c for c in declarator.named_children if c.type == "object_creation_expression"),
                None,
            )
            if created is not None:
                pairs.append((name, _base_type(created.child_by_field_name("type"))))
            elif any(c.type in _CSHARP_STRING_INIT for c in declarator.named_children):
                pairs.append((name, "string"))  # `var s = "";` / `var s = $"...";`
        else:
            pairs.append((name, _base_type(type_node)))
    return pairs


_PY_LITERAL_TYPES = {
    "list": "list",
    "list_comprehension": "list",
    "dictionary": "dict",
    "dictionary_comprehension": "dict",
    "set": "set",
    "set_comprehension": "set",
    "string": "str",
    "concatenated_string": "str",
    "tuple": "tuple",
}
_PY_CONSTRUCTORS = frozenset(
    {"list", "dict", "set", "str", "tuple", "deque", "Counter", "defaultdict", "OrderedDict"}
)


def _python_type(node: Node | None) -> str | None:
    """Python ek açıklaması (`list[int]` → `list`) ya da değer (`[]`, `deque()`) → temel tip."""
    if node is None:
        return None
    if node.type == "type":
        base = text(node).split("[", 1)[0].strip()
        base = base.removeprefix("typing.").removeprefix("collections.")
        return {"List": "list", "Dict": "dict", "Set": "set"}.get(base, base) or None
    if node.type in _PY_LITERAL_TYPES:
        return _PY_LITERAL_TYPES[node.type]
    if node.type == "call":
        name = text(node.child_by_field_name("function")).split(".")[-1]
        return name if name in _PY_CONSTRUCTORS else None
    return None


def _python_bindings(node: Node) -> list[tuple[str, str | None]]:
    """`xs: list[int] = []`, `seen = {}`, `def f(items: list[str])` → (ad, temel tip)."""
    if node.type == "assignment":
        left = node.child_by_field_name("left")
        if left is None or left.type != "identifier":
            return []
        declared = _python_type(node.child_by_field_name("type"))
        return [(text(left), declared or _python_type(node.child_by_field_name("right")))]
    if node.type in ("typed_parameter", "typed_default_parameter"):
        name = node.child_by_field_name("name") or next(
            (c for c in node.named_children if c.type == "identifier"), None
        )
        return [(text(name), _python_type(node.child_by_field_name("type")))] if name else []
    return []


def type_table(root: Node, language: Language) -> dict[str, str]:
    """Değişken/alan/özellik adı → temel tip; belirsiz (birden çok tip) adlar dışarıda kalır."""
    seen: dict[str, set[str]] = {}
    for node in iter_nodes(root):
        if language is Language.PYTHON:
            pairs = _python_bindings(node)
        elif language is Language.CSHARP:
            pairs = _csharp_bindings(node)
        elif node.type in ("declaration", "field_declaration", "parameter_declaration"):
            base = _base_type(node.child_by_field_name("type"))
            pairs = [
                (text(name_node), base)
                for declarator in node.children_by_field_name("declarator")
                if (name_node := declarator_name(declarator)) is not None
            ]
        else:
            continue
        for name, base in pairs:
            if name and base:
                seen.setdefault(name, set()).add(base)
    return {name: next(iter(types)) for name, types in seen.items() if len(types) == 1}
