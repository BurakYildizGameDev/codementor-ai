"""Big-O normalizasyonu, statik ipucuyla uzlaştırma ve `is_optimal` (mimari §5.6)."""

from __future__ import annotations

import re

from codementor.models.bigo import BigO, BigOError, parse_bigo, parse_cost
from codementor.models.facts import ComplexityHint
from codementor.models.llm_output import LLMComplexity
from codementor.models.questions import ExpectedComplexity
from codementor.models.verification import AgreementState, ComplexityCheck

# `O(`, `Θ(`, `Ω(` (büyük/küçük): içerik dengeli parantezle alınır, sonraki ekler atılır
_WRAPPER = re.compile(r"[OoΘθΩω]\s*\(")
# Sarmalayıcı yoksa ifadeden sonra gelen açıklama: "n^2 per frame", "n (kare başına)"
# Baştaki `\s*` kaldırıldı: sınırsız sınıf her konumda yeniden denenip boşluk dizisinde
# karesel süre üretiyordu (§12); ayırıcı boşluk `_before_trailer` içinde `rstrip` ile atılır.
_TRAILER = re.compile(
    r"(?:\(|,|;|\bper\b|\bkare\b|\bher\b|\bamorti|\bworst\b|\baverage\b|\bbest\b"
    r"|\ben kötü\b|\bortalama\b|\bin the\b)",
    re.IGNORECASE,
)
_WORDS = {
    "constant": "1",
    "sabit": "1",
    "linear": "n",
    "doğrusal": "n",
    "quadratic": "n^2",
    "karesel": "n^2",
    "logarithmic": "log n",
    "logaritmik": "log n",
}


def _wrapped(text: str) -> str | None:
    match = _WRAPPER.search(text)
    if match is None:
        return None
    depth = 1
    for i in range(match.end(), len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return text[match.end() : i]
    return None


def _before_trailer(text: str) -> str:
    """İlk açıklama işaretinden önceki karmaşıklık ifadesi (yoksa metnin kendisi).

    `_TRAILER.split(text, maxsplit=1)[0]` ile aynı sonucu verir: işaretten önceki
    ayırıcı boşluk `rstrip` ile atılır, desende sınırsız `\\s*` taşınmaz (§12).
    """
    match = _TRAILER.search(text)
    return text if match is None else text[: match.start()].rstrip()


def normalize_complexity(text: str) -> BigO | None:
    """`O(n^2) per frame`, `Θ(n log n)`, `O(n) amortized`, `O(N²)` → BigO; olmazsa None."""
    text = text.strip()
    if _WRAPPER.search(text):
        # `O(...)` yazılmışsa yalnızca içi geçerlidir; yarım `O(n` → None (`O` değişken değil)
        inner = _wrapped(text)
        candidates = [inner] if inner else []
    else:
        candidates = [c for c in (text, _before_trailer(text)) if c]
    word = _WORDS.get(text.lower())
    if word is not None:
        candidates.append(word)
    for candidate in candidates:
        try:
            return parse_bigo(candidate)
        except BigOError:
            continue
    return None


def resolve_conflict(llm_time: BigO, hint: ComplexityHint | None, agreement: str) -> AgreementState:
    """§5.6: çatışma + `agreement != "conflicts"` → onarım; `conflicts` → gerekçeli, kabul."""
    if hint is None:
        return "no_hint"
    if llm_time.same_class(parse_bigo(hint.value)):
        return "agrees"
    return "justified_conflict" if agreement == "conflicts" else "unjustified_conflict"


def is_optimal(time: BigO, expected: ExpectedComplexity | None) -> bool | None:
    """Sorunun beklenen en baskın zamanına eşit ya da daha iyi mi; soru yoksa ya da
    karşılaştırılamıyorsa (çok değişkenli) None. Amortize `1*` O(1) sayılır."""
    if expected is None:
        return None
    targets = [parse_cost(cost)[0] for cost in expected.time.values()]
    try:
        target = max(targets)
        return time <= target
    except BigOError:
        return True if any(time.same_class(t) for t in targets) else None


def check_complexity(
    complexity: LLMComplexity,
    hint: ComplexityHint | None,
    expected: ExpectedComplexity | None,
) -> ComplexityCheck:
    """Normalizasyon + uzlaştırma; onarım gerekçeleri modele dönecek Türkçe satırlardır."""
    errors: list[str] = []
    time = normalize_complexity(complexity.time_complexity)
    space = normalize_complexity(complexity.space_complexity)
    target = (
        normalize_complexity(complexity.optimal_time_target)
        if complexity.optimal_time_target
        else None
    )
    for field, value, parsed in (
        ("time_complexity", complexity.time_complexity, time),
        ("space_complexity", complexity.space_complexity, space),
    ):
        if parsed is None:
            errors.append(
                f"complexity.{field}: {value[:60]!r} Big-O olarak ayrıştırılamadı; "
                'yalnızca "O(n^2)" gibi bir ifade yaz, açıklamayı reasoning_steps içine koy'
            )
    state: AgreementState = "no_hint" if hint is None else "agrees"
    optimal: bool | None = None
    if time is not None:
        state = resolve_conflict(time, hint, complexity.agreement)
        optimal = is_optimal(time, expected)
        if state == "unjustified_conflict" and hint is not None:
            errors.append(
                f"complexity: statik ipucu O({hint.value}), yanıtın {time.display}. Katılmıyorsan "
                'agreement alanına "conflicts" yaz ve nedenini reasoning_steps içinde açıkla; '
                "katılıyorsan karmaşıklığı düzelt"
            )
    return ComplexityCheck(
        time=time.canonical if time else None,
        space=space.canonical if space else None,
        optimal_target=target.canonical if target else None,
        state=state,
        is_optimal=optimal,
        errors=errors,
    )
