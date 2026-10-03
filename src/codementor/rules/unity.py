"""Unity kuralları (mimari §8.2); yalnızca Unity motorlu C# kodunda çalışır."""

from __future__ import annotations

from tree_sitter import Node

from codementor.analysis._symbols import clip, line, operator_of, simple_name, text
from codementor.models.enums import AllocationKind, AuditCategory, Engine, Language, Severity
from codementor.models.findings import Finding
from codementor.rules.base import Rule, RuleContext
from codementor.rules.registry import register_rule

UNITY = frozenset({Engine.UNITY})
CSHARP = frozenset({Language.CSHARP})

# LINQ burada değil: daha özgül CS-ALLOC-002 raporlar (aynı satırda çift bulgu olmasın)
_HEAP = frozenset(
    {
        AllocationKind.CSHARP_NEW,
        AllocationKind.STRING_CONCAT,
        AllocationKind.CLOSURE,
    }
)
_ANY_RECEIVER = frozenset(
    {
        "GetComponent",
        "TryGetComponent",
        "GetComponents",
        "GetComponentInChildren",
        "GetComponentsInChildren",
        "GetComponentInParent",
        "GetComponentsInParent",
        "FindObjectOfType",
        "FindObjectsOfType",
        "FindFirstObjectByType",
        "FindAnyObjectByType",
        "FindObjectsByType",
        "FindGameObjectWithTag",
        "FindGameObjectsWithTag",
    }
)
# `Find` adı çok yaygın (`list.Find`, `transform.Find`, kullanıcının kendi `Find` metodu);
# yalnızca `GameObject` üzerinden yapılan sahne araması
_SCENE_FIND = frozenset({"GameObject.Find", "GameObject.FindWithTag"})
_CAMERA = frozenset({"Camera", "UnityEngine.Camera"})
_HANDLERS = frozenset({"lambda_expression", "anonymous_method_expression"})
_UNSUBSCRIBE_IN = ("OnDisable", "OnDestroy", "Dispose")
_MAX_NAME_BYTES = 200  # daha uzun hedef/işleyici metni alınmaz (iç içe ifadede karesel süre)


@register_rule
class HotPathAllocation(Rule):
    """UNITY-GC-001: `Update/FixedUpdate/LateUpdate` içinde heap tahsisi."""

    id = "UNITY-GC-001"
    title = "Sıcak yolda heap tahsisi"
    description = (
        "Bu satır her karede yeni bir nesne ayırıyor; çöp toplayıcı bunları bir noktada "
        "toplarken oyun takılabilir. Bu nesne bir kez oluşturulup yeniden kullanılabilir mi?"
    )
    languages = CSHARP
    engines = UNITY
    category = AuditCategory.GARBAGE_COLLECTION
    default_severity = Severity.HIGH

    def check(self, ctx: RuleContext) -> list[Finding]:
        hot = [a for a in ctx.facts.allocations if a.in_hot_path]
        # LINQ'e verilen lambda'nın closure'ı LINQ bulgusunun parçası (CS-ALLOC-002)
        linq_lines = {a.line for a in hot if a.kind is AllocationKind.LINQ}
        return [
            self.finding(ctx, a.line)
            for a in hot
            if a.kind in _HEAP and not (a.kind is AllocationKind.CLOSURE and a.line in linq_lines)
        ]


def _is_camera_main(node: Node) -> bool:
    """`Camera.main`; metin yalnızca kısa düğümlerde alınır (`a.b.c...` zincirinde doğrusal)."""
    name, target = node.child_by_field_name("name"), node.child_by_field_name("expression")
    return (
        name is not None
        and target is not None
        and target.end_byte - target.start_byte <= len("UnityEngine.Camera")
        and text(name) == "main"
        and text(target) in _CAMERA
    )


def _expensive_lookup(name: str) -> bool:
    return simple_name(name) in _ANY_RECEIVER or name in _SCENE_FIND


@register_rule
class HotPathLookup(Rule):
    """UNITY-PERF-001: sıcak yolda `GetComponent`, `Find`, `FindObjectOfType`, `Camera.main`."""

    id = "UNITY-PERF-001"
    title = "Sıcak yolda bileşen/sahne araması"
    description = (
        "Bu arama her karede yeniden yapılıyor ama sonucu kareden kareye değişiyor mu? "
        "Sonucu bir kez bulup saklamak mümkün mü?"
    )
    languages = CSHARP
    engines = UNITY
    category = AuditCategory.PERFORMANCE
    default_severity = Severity.HIGH

    def check(self, ctx: RuleContext) -> list[Finding]:
        found = [
            self.finding(ctx, c.line)
            for c in ctx.facts.calls
            if ctx.in_hot_function(c.function_line) and _expensive_lookup(c.name)
        ]
        covered = -1  # iç içe yerel fonksiyonlar dıştakiyle bir kez gezilir (Faz 17 denetimi)
        for fn in sorted(ctx.function_nodes, key=lambda f: f.node.start_byte):
            if fn.fact.is_hot_path and fn.node.start_byte >= covered:
                covered = fn.node.end_byte
                found += [
                    self.finding(ctx, line(n))
                    for n in ctx.nodes_in(fn.node, "member_access_expression")
                    if _is_camera_main(n)
                ]
        return found


def _short(node: Node | None) -> str | None:
    """Kısa düğümün metni; uzunsa None (iç içe `a -= a -= ...` zincirinde karesel süre olmasın)."""
    if node is None or node.end_byte - node.start_byte > _MAX_NAME_BYTES:
        return None
    return text(node)


def _norm(node: Node | None) -> str:
    """Karşılaştırma anahtarı: boşluksuz, `this.` öneksiz; `new Action(H)` → `H`."""
    if node is not None and node.type == "object_creation_expression":
        args = node.child_by_field_name("arguments")
        if args is not None and args.named_child_count == 1:
            node = _first_argument(node)
    raw = _short(node)
    return "" if raw is None else raw.replace(" ", "").removeprefix("this.")


def _first_argument(call: Node) -> Node | None:
    args = call.child_by_field_name("arguments")
    arg = args.named_child(0) if args is not None and args.named_child_count else None
    return arg.named_child(0) if arg is not None and arg.named_child_count else None


def _member_call(node: Node) -> tuple[str, str] | None:
    """`x.AddListener(...)` → (`x`, `AddListener`)."""
    fn = node.child_by_field_name("function")
    if fn is None or fn.type != "member_access_expression":
        return None
    return _norm(fn.child_by_field_name("expression")), text(fn.child_by_field_name("name"))


def _local_callees(fn: Node, ctx: RuleContext) -> set[str]:
    """Gövdede doğrudan çağrılan aynı sınıf metotları (`Unsub()`, `this.Unsub()`)."""
    names: set[str] = set()
    for n in ctx.nodes_in(fn, "invocation_expression"):
        callee = n.child_by_field_name("function")
        if callee is not None and callee.type == "identifier":
            names.add(text(callee))
        elif callee is not None and callee.type == "member_access_expression":
            target = callee.child_by_field_name("expression")
            if target is not None and target.type == "this_expression":
                names.add(text(callee.child_by_field_name("name")))
    return names


def _removed(ctx: RuleContext) -> set[tuple[str, str]]:
    """Kaldırılan (hedef, işleyici) çiftleri; `*` = hepsi.

    `OnDisable`/`OnDestroy`/`Dispose` ve bunların doğrudan çağırdığı aynı dosyadaki
    metotlar (tek seviye) taranır.
    """
    cleanup = ctx.functions_named(*_UNSUBSCRIBE_IN)
    callees = {name for fn in cleanup for name in _local_callees(fn.node, ctx)}
    removed: set[tuple[str, str]] = set()
    seen: set[int] = set()
    for fn in [*cleanup, *ctx.functions_named(*callees)]:
        if fn.node.start_byte in seen:
            continue
        seen.add(fn.node.start_byte)
        for n in ctx.nodes_in(fn.node, "assignment_expression", "invocation_expression"):
            if n.type == "assignment_expression":
                if operator_of(n) == "-=":
                    left, right = n.child_by_field_name("left"), n.child_by_field_name("right")
                    removed.add((_norm(left), _norm(right)))
            elif (member := _member_call(n)) is not None:
                if member[1] == "RemoveListener":
                    removed.add((member[0], _norm(_first_argument(n))))
                elif member[1] == "RemoveAllListeners":
                    removed.add((member[0], "*"))
    return removed


def _subscription(node: Node, facts: set[tuple[int, str]]) -> tuple[str, Node | None] | None:
    """`hedef += işleyici` ya da `hedef.AddListener(işleyici)` → (hedef, işleyici).

    `+=` yalnızca olgu çıkarıcının abonelik saydığı hedefse alınır (satır + ad); aynı
    satırdaki `count += 1` abonelik sayılmaz.
    """
    if node.type == "assignment_expression":
        left = node.child_by_field_name("left")
        raw = _short(left)
        if operator_of(node) != "+=" or raw is None or (line(node), clip(raw)) not in facts:
            return None
        return _norm(left), node.child_by_field_name("right")
    member = _member_call(node)
    if member is None or member[1] != "AddListener":
        return None
    return member[0], _first_argument(node)


@register_rule
class UnbalancedSubscription(Rule):
    """UNITY-EVT-001: `+=` aboneliği `OnDisable/OnDestroy`'da `-=` ile kaldırılmıyor."""

    id = "UNITY-EVT-001"
    title = "Kaldırılmayan olay aboneliği"
    description = (
        "Bu abonelik `OnDisable`/`OnDestroy` içinde kaldırılmıyor. Nesne yok edildikten "
        "sonra olay tetiklenirse ne olur?"
    )
    languages = CSHARP
    engines = UNITY
    category = AuditCategory.RESOURCE_LEAK
    default_severity = Severity.MEDIUM
    LAMBDA_DESCRIPTION = (
        "Abonelik bir lambda/anonim metotla yapılmış; `-=` ile aynı lambdayı yazmak yeni bir "
        "temsilci oluşturur, abonelik kaldırılamaz. Temsilciyi nerede saklayabilirsin?"
    )

    def check(self, ctx: RuleContext) -> list[Finding]:
        facts = {(s.line, s.name) for s in ctx.facts.engine_symbols.event_subscriptions}
        if not facts:
            return []
        lines = {n for n, _ in facts}
        removed = _removed(ctx)
        found: list[Finding] = []
        for n in ctx.nodes_in(ctx.root, "assignment_expression", "invocation_expression"):
            sub = _subscription(n, facts) if line(n) in lines else None
            if sub is None:
                continue
            target, handler = sub
            if (target, "*") in removed:
                continue
            if handler is not None and handler.type in _HANDLERS:
                found.append(self.finding(ctx, line(n), description=self.LAMBDA_DESCRIPTION))
            elif (target, _norm(handler)) not in removed:
                found.append(self.finding(ctx, line(n)))
        return found


# Her fizik adımında çağrılan geri çağrılar; `*Enter`/`*Exit` olay başına bir kez çalışır
_PHYSICS_STAY = ("OnTriggerStay", "OnTriggerStay2D", "OnCollisionStay", "OnCollisionStay2D")


# `tag` özelliği olan Unity tipleri; başka bir tiple bildirilmiş alıcının (`Item item`)
# `tag`'i kullanıcının kendi alanıdır
_TAGGED = frozenset(
    {
        "GameObject",
        "Component",
        "Transform",
        "Collider",
        "Collider2D",
        "Collision",
        "Collision2D",
        "Rigidbody",
        "Rigidbody2D",
        "MonoBehaviour",
        "Behaviour",
        "Renderer",
        "Camera",
    }
)


def _is_tag(node: Node | None, types: dict[str, str]) -> bool:
    """Unity `tag` özelliği: `tag`, `target.tag`, `other.gameObject.tag`.

    Kodda `tag` adlı değişken/alan bildirilmişse yalın `tag` o değişkendir; alıcı Unity
    dışı bir tiple bildirilmişse (`Item item; item.tag`) bulgu yok.
    """
    if node is None:
        return False
    if node.type == "identifier":
        return text(node) == "tag" and "tag" not in types
    if node.type != "member_access_expression":
        return False
    name, receiver = node.child_by_field_name("name"), node.child_by_field_name("expression")
    if name is None or text(name) != "tag":
        return False
    if receiver is None or receiver.end_byte - receiver.start_byte > _MAX_NAME_BYTES:
        return True
    declared = types.get(simple_name(text(receiver).removeprefix("this.")))
    return declared is None or declared in _TAGGED


@register_rule
class StringTagComparison(Rule):
    """UNITY-PERF-002: sıcak yolda `tag ==` (`CompareTag` yerine)."""

    id = "UNITY-PERF-002"
    title = "Sıcak yolda string etiket karşılaştırma"
    description = (
        "`tag` özelliği her okunduğunda yeni bir string ayırır ve bu karşılaştırma sık "
        "çalışıyor. Unity etiket karşılaştırması için ayırma yapmayan hangi metodu sunar?"
    )
    languages = CSHARP
    engines = UNITY
    category = AuditCategory.PERFORMANCE
    default_severity = Severity.LOW

    def check(self, ctx: RuleContext) -> list[Finding]:
        found: list[Finding] = []
        types = ctx.types
        covered = -1  # iç içe yerel fonksiyonlar dıştakiyle bir kez gezilir (mimari §12)
        for fn in sorted(ctx.function_nodes, key=lambda f: f.node.start_byte):
            if fn.node.start_byte < covered:
                continue
            if not (fn.fact.is_hot_path or simple_name(fn.fact.name) in _PHYSICS_STAY):
                continue
            covered = fn.node.end_byte
            for n in ctx.nodes_in(fn.node, "binary_expression", "invocation_expression"):
                if n.type == "binary_expression":
                    hit = operator_of(n) in ("==", "!=") and (
                        _is_tag(n.child_by_field_name("left"), types)
                        or _is_tag(n.child_by_field_name("right"), types)
                    )
                else:
                    callee = n.child_by_field_name("function")
                    hit = (
                        callee is not None
                        and callee.type == "member_access_expression"
                        and text(callee.child_by_field_name("name")) == "Equals"
                        and _is_tag(callee.child_by_field_name("expression"), types)
                    )
                if hit:
                    found.append(self.finding(ctx, line(n)))
        return found
