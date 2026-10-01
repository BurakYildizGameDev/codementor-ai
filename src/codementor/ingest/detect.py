"""Sezgisel dil/motor tespiti (mimari §5.1).

Her sinyal bir desen + ağırlıktır; bir desen kaç kez geçerse geçsin bir kez sayılır.
Sinyaller yorum ve metin sabiti içerikleri maskelenmiş kodda aranır. Önce motor
(Unity/Unreal), sonra dil puanlanır. C++ kodu C sinyallerini de içerebildiği için C
yalnızca belirgin bir C++/C# sinyali yokken seçilir ve tree-sitter dilbilgisiyle
doğrulanır. Karar verilemezse `LanguageDetectionError` (API'de 422) — kullanıcıya sorulur.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from codementor.analysis.lexical import mask_non_code
from codementor.analysis.parsers import parse_source
from codementor.ingest.errors import LanguageDetectionError
from codementor.models.enums import Engine, Language, required_language
from codementor.models.request import Detection, LanguageHint

ENGINE_THRESHOLD = 5  # motor kararı için gereken en düşük puan
LANGUAGE_THRESHOLD = 3  # dil kararı için gereken en düşük puan
_FULL_CONFIDENCE_SCORE = 8

_M = re.MULTILINE
SUPPORTED = "C, C++, C#, Python, HTML ve CSS"


@dataclass(frozen=True, slots=True)
class _Signal:
    pattern: re.Pattern[str]
    weight: int
    reason: str


def _s(pattern: str, weight: int, reason: str, flags: int = 0) -> _Signal:
    return _Signal(re.compile(pattern, flags), weight, reason)


_ENGINE_SIGNALS: dict[Engine, list[_Signal]] = {
    Engine.UNITY: [
        _s(r"\busing\s+UnityEngine\b", 5, "using UnityEngine"),
        _s(r":\s*MonoBehaviour\b", 5, "MonoBehaviour türevi"),
        _s(r"\bScriptableObject\b", 3, "ScriptableObject"),
        _s(r"\[\s*SerializeField\b", 3, "[SerializeField]"),
        _s(r"\bGetComponent\s*<", 2, "GetComponent<T>"),
        _s(r"\bTime\.deltaTime\b", 2, "Time.deltaTime"),
    ],
    Engine.UNREAL: [
        _s(r"\bUCLASS\s*\(", 5, "UCLASS()"),
        _s(r"\bGENERATED_(?:U\w+_)?BODY\s*\(", 5, "GENERATED_BODY()"),
        _s(r"#\s*include\s*\"CoreMinimal\.h\"", 5, "CoreMinimal.h"),
        _s(r"\bU(?:PROPERTY|FUNCTION|STRUCT|ENUM)\s*\(", 4, "UPROPERTY/UFUNCTION"),
        _s(r"\b[A-Z][A-Z0-9_]*_API\b", 2, "*_API dışa aktarma makrosu"),
        _s(r"\bT(?:Array|Map|Set|ObjectPtr|WeakObjectPtr)\s*<", 2, "Unreal kapsayıcıları"),
        _s(r"\bF(?:String|Name|Vector)\b", 1, "FString/FName/FVector"),
        _s(r"\bu?int(?:8|16|32|64)\b", 1, "int32 türleri"),
    ],
}

_LANGUAGE_SIGNALS: dict[Language, list[_Signal]] = {
    Language.C: [
        _s(r"#\s*include\s*<[\w/]+\.h>", 3, "C standart başlığı (<*.h>)"),
        _s(
            r"\b(?:printf|scanf|malloc|calloc|realloc|free|puts|fgets)\s*\(",
            2,
            "C kütüphane çağrısı",
        ),
        _s(r"\btypedef\s+(?:struct|enum|union)\b", 2, "typedef struct/enum"),
    ],
    Language.CPP: [
        _s(r"#\s*include\s*<(?![\w/]+\.h>)[\w/]+>", 4, "C++ standart başlığı (uzantısız)"),
        _s(r"\bstd::", 4, "std:: kullanımı"),
        _s(r"\btemplate\s*<", 3, "template"),
        _s(r"\bnullptr\b", 3, "nullptr"),
        _s(r"^\s*(?:public|private|protected)\s*:", 3, "erişim belirteci etiketi", _M),
        _s(r"\b(?:unique_ptr|shared_ptr|make_unique|make_shared)\b", 3, "akıllı pointer"),
        _s(r"\b(?:cout|cin|cerr)\b", 3, "iostream akışları"),
        _s(r"\w::\w", 1, ":: kapsam çözümü"),
    ],
    Language.CSHARP: [
        _s(r"^\s*using\s+System(?:\.[\w.]+)?\s*;", 5, "using System", _M),
        _s(r"^\s*using\s+[A-Z][\w.]*\s*;", 2, "using yönergesi", _M),
        _s(r"\bnamespace\s+[\w.]+\s*[;{]", 2, "namespace"),
        _s(
            r"\b(?:public|internal|private|protected)\s+(?:(?:static|sealed|abstract|partial)\s+)*"
            r"(?:class|struct|record|interface)\b",
            3,
            "erişim belirteçli tür bildirimi",
        ),
        _s(r"\{\s*get\s*;", 3, "otomatik özellik (get;)"),
        _s(r"\bConsole\.Write", 4, "Console.Write"),
        _s(r"\bforeach\s*\(\s*var\b", 3, "foreach (var"),
        _s(r"\bvar\s+\w+\s*=", 2, "var bildirimi"),
        _s(r"=>", 1, "=> ifadesi"),
    ],
}

_I = re.IGNORECASE

# Python, HTML ve CSS (ADR-0015): C maskeleyicisi `#` yorumlarını ve etiketleri tanımadığı için
# bu sinyaller ham kodda aranır; yalnızca C ailesinden belirgin biçimde güçlüyse seçilir.
_OTHER_SIGNALS: dict[Language, list[_Signal]] = {
    Language.PYTHON: [
        _s(r"^\s*def\s+\w+\s*\([^)]*\)\s*(?:->[^:]+)?:\s*(?:#.*)?$", 5, "def fonksiyon(...):", _M),
        _s(r"^\s*(?:from\s+[\w.]+\s+import|import\s+[\w.]+)(?!.*;\s*$)", 3, "import", _M),
        _s(
            r"^\s*(?:if|elif|for|while|with|try|except|else|class)[^;{}]*:\s*(?:#.*)?$",
            3,
            "iki noktayla biten blok başlığı",
            _M,
        ),
        _s(r"if\s+__name__\s*==", 5, "if __name__ =="),
        _s(r"self\.\w+", 2, "self."),
        _s(r"^\s*elif", 3, "elif", _M),
        _s(r"(?:None|True|False)", 1, "None/True/False"),
        _s(r"print\s*\(", 1, "print("),
    ],
    Language.HTML: [
        _s(r"^\s*<!DOCTYPE\s+html", 6, "<!DOCTYPE html>", _M | _I),
        _s(r"<html", 5, "<html>", _I),
        _s(
            r"</(?:div|p|body|head|section|ul|ol|li|a|span|main|nav|form|table|h[1-6]|article)>",
            4,
            "kapanış etiketi",
            _I,
        ),
        _s(r"<(?:meta|link|img|input|br|hr)[^>]*>", 2, "boş HTML öğesi", _I),
        _s(r"(?:class|id|href|src)=\"", 1, "HTML özniteliği"),
    ],
    Language.CSS: [
        _s(r"^\s*[\w.#:*\-\[\]=\"' >+~,()]+\{\s*$", 2, "seçici {", _M),
        _s(r"^\s*-{0,2}[a-z][a-z-]*\s*:\s*[^;{}()=]*[^;{}]*;\s*$", 3, "özellik: değer;", _M),
        _s(r"@(?:media|import|font-face|keyframes|supports)", 4, "@kural"),
        _s(r":root|var\(--", 3, "CSS değişkeni"),
        _s(r"\d(?:px|rem|em|vh|vw|%)", 1, "CSS birimi"),
    ],
}

# Desteklenmeyen ama C#'a çok benzeyen dil: sessizce C# sayılmasın
_JAVA = re.compile(
    r"\bSystem\.out\.print|^\s*import\s+java\.|\bpublic\s+static\s+void\s+main\s*\(\s*String", _M
)


def _score(code: str, signals: list[_Signal]) -> tuple[int, list[str]]:
    matched = [s for s in signals if s.pattern.search(code)]
    return sum(s.weight for s in matched), [s.reason for s in matched]


def _confidence(best: int, second: int) -> float:
    if best <= 0:
        return 0.0
    strength = min(1.0, best / _FULL_CONFIDENCE_SCORE)
    return round(strength * best / (best + second), 2)


def _detect_engine(code: str) -> tuple[Engine, int, list[str]]:
    scored = {engine: _score(code, signals) for engine, signals in _ENGINE_SIGNALS.items()}
    engine, (score, reasons) = max(scored.items(), key=lambda item: item[1][0])
    if score < ENGINE_THRESHOLD:
        return Engine.NONE, 0, []
    return engine, score, reasons


def _parses_cleanly(code: str, language: Language) -> bool:
    return not parse_source(code, language, Engine.NONE).tree.root_node.has_error


def _detect_other(code: str, family_best: int) -> Detection | None:
    """Python/HTML/CSS: eşiği geçen ve C ailesinden güçlü olan en yüksek puanlı dil."""
    scored = {lang: _score(code, signals) for lang, signals in _OTHER_SIGNALS.items()}
    ranked = sorted(scored.items(), key=lambda item: item[1][0], reverse=True)
    (language, (best, reasons)), (_, (runner_up, _)) = ranked[0], ranked[1]
    if best < LANGUAGE_THRESHOLD or best <= family_best:
        return None
    if language is not Language.HTML and not _parses_cleanly(code, language):
        # HTML dilbilgisi neredeyse her metni kabul eder; diğerlerinde ayrışma kanıttır
        reasons = [*reasons, "dilbilgisiyle tam ayrışmıyor (sözdizimi hatası olabilir)"]
    return Detection(
        language=language,
        engine=Engine.NONE,
        confidence=_confidence(best, max(family_best, runner_up)),
        reasons=reasons,
    )


def _detect_language(code: str, masked: str) -> Detection:
    """`masked`: yorum/metin içeriği maskelenmiş kod (sinyaller bunun üzerinde aranır)."""
    if _JAVA.search(masked):
        raise LanguageDetectionError(f"Java kodu gibi görünüyor; desteklenen diller {SUPPORTED}")
    scores = {lang: _score(masked, signals) for lang, signals in _LANGUAGE_SIGNALS.items()}
    c, cpp, cs = (scores[lang][0] for lang in (Language.C, Language.CPP, Language.CSHARP))
    other = _detect_other(code, max(c, cpp, cs))
    if other is not None:
        return other

    if c >= LANGUAGE_THRESHOLD and max(cpp, cs) < LANGUAGE_THRESHOLD:
        # Yalnızca C başlıkları kullanan "C tarzı C++" (class, new, T&) sık görülür:
        # C dilbilgisiyle ayrışmıyor ama C++ ile ayrışıyorsa C++'tır.
        if not _parses_cleanly(code, Language.C) and _parses_cleanly(code, Language.CPP):
            return Detection(
                language=Language.CPP,
                engine=Engine.NONE,
                confidence=_confidence(c, 0),
                reasons=[*scores[Language.C][1], "C++ dilbilgisiyle hatasız ayrışıyor"],
            )
        return Detection(
            language=Language.C,
            engine=Engine.NONE,
            confidence=_confidence(c, max(cpp, cs)),
            reasons=scores[Language.C][1],
        )
    if max(cpp, cs) < LANGUAGE_THRESHOLD:
        raise LanguageDetectionError("belirgin bir dil işareti yok")
    if cpp == cs:
        raise LanguageDetectionError("C++ ve C# işaretleri eşit ağırlıkta")
    winner, best, second = (Language.CPP, cpp, cs) if cpp > cs else (Language.CSHARP, cs, cpp)
    return Detection(
        language=winner,
        engine=Engine.NONE,
        confidence=_confidence(best, second),
        reasons=scores[winner][1],
    )


def detect(code: str, hint: LanguageHint | None = None) -> Detection:
    """Kodun dilini ve motorunu belirler; `hint`teki dolu alanlar her zaman kazanır."""
    hint = hint or LanguageHint()
    if hint.language is not None and hint.engine is not None:
        return Detection(
            language=hint.language,
            engine=hint.engine,
            confidence=1.0,
            reasons=["kullanıcı belirtti"],
        )

    masked = mask_non_code(code)
    implied = required_language(hint.engine)
    if implied is not None:  # yalnızca motor verildi → dil motordan gelir
        return Detection(
            language=implied,
            engine=hint.engine or Engine.NONE,
            confidence=1.0,
            reasons=["kullanıcı motoru belirtti"],
        )

    engine, engine_score, engine_reasons = _detect_engine(masked)
    if hint.engine is Engine.NONE:
        engine, engine_score, engine_reasons = Engine.NONE, 0, []

    if hint.language is not None:  # yalnızca dil verildi → uyumluysa motoru tespit et
        compatible = required_language(engine) == hint.language
        return Detection(
            language=hint.language,
            engine=engine if compatible else Engine.NONE,
            confidence=1.0,
            reasons=["kullanıcı dili belirtti", *(engine_reasons if compatible else [])],
        )

    language = required_language(engine)
    if language is not None:  # motor tespit edildi → dil motordan gelir
        return Detection(
            language=language,
            engine=engine,
            confidence=_confidence(engine_score, 0),
            reasons=engine_reasons,
        )
    return _detect_language(code, masked)
