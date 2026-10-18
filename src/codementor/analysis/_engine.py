"""Motor yaşam döngüsü ve motor sembolleri (mimari §5.3.1 `functions`, `engine_symbols`).

- Sıcak yol: Unity `Update/FixedUpdate/LateUpdate/OnGUI`, Unreal `Tick/TickComponent`.
- Unreal: `UPROPERTY(...)` ile işaretli alanlar (makro, ayrıştırmadan önce nötrleştirildiği
  için özgün metinden satır olarak bulunur ve sonraki alan bildirimine bağlanır),
  `UObject`/`AActor` türevi ham işaretçi ve `TObjectPtr` alanları, `AddDynamic` benzeri
  delege abonelikleri.
- C#: `+=` olay abonelikleri (sağda lambda veya dosyadaki bir metot; ya da solda `event`
  / `Action` olarak bildirilmiş ad), Unity `AddListener` çağrıları, `OnEnable` /
  `OnDisable` varlığı.
"""

from __future__ import annotations

import re

from tree_sitter import Node

from codementor.analysis._symbols import (
    CallName,
    NodeKey,
    clip,
    declarator_name,
    key,
    line,
    operator_of,
    simple_name,
    strip_templates,
    text,
)
from codementor.analysis.lexical import mask_non_code
from codementor.analysis.parsers import iter_nodes
from codementor.models.enums import Engine, Language
from codementor.models.facts import EngineSymbols, FunctionFact, SymbolRef

UNITY_LIFECYCLE = frozenset(
    {
        "Awake",
        "Start",
        "Update",
        "FixedUpdate",
        "LateUpdate",
        "OnGUI",
        "OnEnable",
        "OnDisable",
        "OnDestroy",
        "OnValidate",
    }
)
UNITY_HOT = frozenset({"Update", "FixedUpdate", "LateUpdate", "OnGUI"})
UNREAL_LIFECYCLE = frozenset(
    {"BeginPlay", "EndPlay", "Tick", "TickComponent", "PostInitializeComponents", "OnConstruction"}
)
UNREAL_HOT = frozenset({"Tick", "TickComponent"})

_UPROPERTY = re.compile(r"\bUPROPERTY\s*\(")
# Unreal adlandırması: U/A öneki + PascalCase (`UObject`, `AActor`); `ANSICHAR` gibi
# tamamı büyük harfli tipler hariç
_UOBJECT_TYPE = re.compile(r"^(?:class\s+)?[UA][A-Z][a-z]\w*$")
_UNITY_LISTENERS = frozenset({"AddListener"})
_OBJECT_PTR = frozenset({"TObjectPtr"})
# GC'nin UPROPERTY ile izlediği kapsayıcılar; öğe ya da değer UObject ise alan aynı risktedir
_CONTAINERS = frozenset({"TArray", "TSet", "TMap"})
_MAX_CONTAINER_DEPTH = 2  # `TMap<FName, TArray<UObject*>>`; daha derin iç içe yapı incelenmez
_UOBJECT_ARG = re.compile(r"^(?:class\s+)?[UA][A-Z][a-z]\w*\s*\*$|^TObjectPtr\s*<")
_REFLECTION = re.compile(r"\b(?:UCLASS|USTRUCT)\s*\(")
_MAX_TEMPLATE_BYTES = 300  # daha uzun şablon argümanı incelenmez (doğrusal süre)
_DELEGATE_BIND = frozenset(
    {"AddDynamic", "AddUniqueDynamic", "AddUObject", "AddLambda", "AddRaw", "AddSP", "AddUFunction"}
)
_EVENT_TYPES = frozenset({"Action", "UnityEvent", "EventHandler", "Func"})
_HANDLER_NODES = frozenset({"lambda_expression", "anonymous_method_expression"})


_CS_TYPES = frozenset({"class_declaration", "struct_declaration", "record_declaration"})
_CPP_TYPES = frozenset({"class_specifier", "struct_specifier"})
_MEMBERS = frozenset({"method_declaration", "function_definition"})


def _plain(node: Node) -> bool:
    """Motorun çağıramayacağı tip: tabanı olmayan sınıf, C# struct'ı ya da kaydı."""
    if node.type in ("struct_declaration", "record_declaration"):
        return True  # MonoBehaviour'dan türeyemez
    if any(c.type == "modifier" and text(c) == "partial" for c in node.children):
        return False  # taban başka bir parçada (başka dosyada da olabilir)
    bases = ("base_list", "base_class_clause")
    return not any(child.type in bases for child in node.children)


def engine_inert_members(root: Node, language: Language) -> frozenset[NodeKey]:
    """Tabanı olmayan tiplerin doğrudan metotları (Faz 21): `class Plain { void Update() }`
    Unity/Unreal tarafından çağrılmaz, sıcak yol değildir. Taban varsa (kullanıcının kendi
    tabanı da MonoBehaviour'dan türeyebilir) ya da tanım sınıf dışındaysa (`AFoo::Tick`)
    eskisi gibi ad belirler. Tek geçiş; iç içe tip kendi üyelerini ayrıca belirler."""
    types = _CS_TYPES if language is Language.CSHARP else _CPP_TYPES
    found: set[NodeKey] = set()
    for node in iter_nodes(root):
        if node.type not in types or not _plain(node):
            continue
        body = node.child_by_field_name("body")
        if body is not None:
            found.update(key(m) for m in body.named_children if m.type in _MEMBERS)
    return frozenset(found)


def lifecycle(name: str, engine: Engine) -> tuple[str | None, bool]:
    """(yaşam döngüsü adı, sıcak yol mu) — motora göre."""
    simple = simple_name(name)
    if engine is Engine.UNITY and simple in UNITY_LIFECYCLE:
        return simple, simple in UNITY_HOT
    if engine is Engine.UNREAL and simple in UNREAL_LIFECYCLE:
        return simple, simple in UNREAL_HOT
    return None, False


def _field_name(field: Node) -> str | None:
    for declarator in field.children_by_field_name("declarator"):
        name = declarator_name(declarator)
        if name is not None:
            return text(name)
    return None


def _is_method(field: Node) -> bool:
    """`AActor* GetTarget() const;` alan değil metot bildirimidir."""
    return any(
        n.type == "function_declarator"
        for declarator in field.children_by_field_name("declarator")
        for n in iter_nodes(declarator)
    )


def _holds_uobject(type_node: Node | None, depth: int = _MAX_CONTAINER_DEPTH) -> bool:
    """`TArray<AActor*>`, `TMap<FName, UTexture2D*>`, `TSet<TObjectPtr<AEnemy>>`.

    Kapsayıcı içinde kapsayıcı da sayılır (`TMap<FName, TArray<UObject*>>`); iç argümanlar
    `type_descriptor` sarmalayıcısında gelir, açılır. `depth` katman sınırı hem karesel
    süreyi hem yapay iç içe girdide özyineleme taşmasını önler (§12).
    """
    if type_node is not None and type_node.type == "type_descriptor":
        type_node = next(iter(type_node.named_children), None)
    if depth <= 0 or type_node is None or type_node.type != "template_type":
        return False
    if strip_templates(text(type_node)) not in _CONTAINERS:
        return False
    args = type_node.child_by_field_name("arguments")
    if args is None or args.end_byte - args.start_byte > _MAX_TEMPLATE_BYTES:
        return False
    return any(
        _UOBJECT_ARG.match(text(arg).strip()) or _holds_uobject(arg, depth - 1)
        for arg in args.named_children
    )


def _reflected(field: Node, masked_lines: list[str]) -> bool:
    """Alanın tipi UCLASS()/USTRUCT() ile işaretli mi (makro, tipten önceki dolu satırda).

    Tip bulunamazsa (ör. ayrıştırma hatası) işaretli sayılır: yanlış öneri vermeyelim.
    """
    owner = field.parent.parent if field.parent is not None else None
    if owner is None or owner.type not in _CPP_TYPES:
        return True
    row = owner.start_point[0]
    if _REFLECTION.search(masked_lines[row][: owner.start_point[1]]):
        return True
    for previous in range(row - 1, max(row - 4, -1), -1):
        if masked_lines[previous].strip():
            return _REFLECTION.search(masked_lines[previous]) is not None
    return False


def _unreal_fields(
    original: str, fields: list[Node]
) -> tuple[list[SymbolRef], list[SymbolRef], list[SymbolRef]]:
    masked = mask_non_code(original)
    masked_lines = masked.split("\n")
    macro_lines = [masked.count("\n", 0, m.start()) + 1 for m in _UPROPERTY.finditer(masked)]
    data_fields = [f for f in fields if not _is_method(f)]
    uproperty: list[SymbolRef] = []
    position = 0  # makrolar ve alanlar kaynak sırasında: iki işaretçi, O(M + F)
    for macro_line in macro_lines:
        while position < len(data_fields) and line(data_fields[position]) < macro_line:
            position += 1
        if position == len(data_fields):
            break
        target = data_fields[position]
        position += 1
        name = _field_name(target)
        if name:
            uproperty.append(SymbolRef(name=clip(name), line=line(target)))
    uobject: list[SymbolRef] = []
    unreflected: list[SymbolRef] = []
    for field in data_fields:
        type_node = field.child_by_field_name("type")
        type_name = strip_templates(text(type_node))
        declarators = field.children_by_field_name("declarator")
        raw_pointer = _UOBJECT_TYPE.match(text(type_node)) and any(
            d.type == "pointer_declarator" for d in declarators
        )
        wrapped = (
            type_node is not None
            and type_node.type == "template_type"
            and (type_name in _OBJECT_PTR)
        )
        name = _field_name(field)
        if (raw_pointer or wrapped or _holds_uobject(type_node)) and name:
            ref = SymbolRef(name=clip(name), line=line(field))
            uobject.append(ref)
            if not _reflected(field, masked_lines):
                unreflected.append(ref)
    return uproperty, uobject, unreflected


def _csharp_event_names(fields: list[Node], events: list[Node]) -> set[str]:
    names: set[str] = set()
    for node in [*fields, *events]:
        declaration = next(
            (c for c in node.named_children if c.type == "variable_declaration"), None
        )
        if declaration is None:
            continue
        is_event = node.type == "event_field_declaration" or (
            strip_templates(text(declaration.child_by_field_name("type"))) in _EVENT_TYPES
        )
        if is_event:
            names |= {
                text(d.child_by_field_name("name"))
                for d in declaration.named_children
                if d.type == "variable_declarator"
            }
    return names


def _csharp_subscriptions(
    assignments: list[Node], event_names: set[str], methods: set[str]
) -> list[SymbolRef]:
    found: list[SymbolRef] = []
    for node in assignments:
        left, right = node.child_by_field_name("left"), node.child_by_field_name("right")
        if left is None or right is None or operator_of(node) != "+=":
            continue
        target = simple_name(text(left))
        handler = right.type in _HANDLER_NODES or (
            right.type in ("identifier", "member_access_expression")
            and simple_name(text(right)) in methods
        )
        if handler or target in event_names:
            found.append(SymbolRef(name=clip(text(left)), line=line(node)))
    return found


def engine_symbols(
    *,
    language: Language,
    engine: Engine,
    original: str,
    fields: dict[str, list[Node]],
    functions: list[FunctionFact],
    calls: list[tuple[CallName, int]],
) -> EngineSymbols:
    """Dosyanın motor sembolleri; ilgisiz dil/motor için boş."""
    symbols = EngineSymbols()
    names = {simple_name(f.name) for f in functions}
    if language is Language.CSHARP:
        events = _csharp_event_names(fields.get("field", []), fields.get("event", []))
        subscriptions = _csharp_subscriptions(fields.get("subscribe", []), events, names)
        subscriptions += [
            SymbolRef(name=clip(call.receiver or call.display), line=call_line)
            for call, call_line in calls
            if call.method in _UNITY_LISTENERS
        ]
        symbols.event_subscriptions = sorted(subscriptions, key=lambda s: s.line)
        symbols.has_on_enable = "OnEnable" in names
        symbols.has_on_disable = "OnDisable" in names
    elif engine is Engine.UNREAL:
        (
            symbols.uproperty_fields,
            symbols.uobject_fields,
            symbols.unreflected_fields,
        ) = _unreal_fields(original, fields.get("field", []))
        symbols.event_subscriptions = [
            SymbolRef(name=clip(call.receiver or call.display), line=call_line)
            for call, call_line in calls
            if call.method in _DELEGATE_BIND
        ]
    return symbols
