"""Sistem genelindeki sabit değer kümeleri (mimari §6.2, §5.3.1)."""

from __future__ import annotations

from enum import StrEnum


class Language(StrEnum):
    C = "c"
    CPP = "cpp"
    CSHARP = "csharp"
    PYTHON = "python"
    HTML = "html"
    CSS = "css"


class Engine(StrEnum):
    NONE = "none"
    UNITY = "unity"
    UNREAL = "unreal"


class Difficulty(StrEnum):
    VERY_EASY = "very_easy"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Severity(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CompilationStatus(StrEnum):
    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"
    SKIPPED = "skipped"


class FindingSource(StrEnum):
    STATIC = "static"
    LLM = "llm"
    CONFIRMED = "confirmed"


# Faz 36 (ADR-0022): gerçek hata mı, hataya yol açmayan öneri mi. Docstring yok: LLM şemasına
# açıklama olarak girer ve dar bağlamlı bütçeyi tüketir.
class FindingKind(StrEnum):
    ISSUE = "issue"
    SUGGESTION = "suggestion"


class AuditCategory(StrEnum):
    MEMORY_SAFETY = "memory_safety"
    RESOURCE_LEAK = "resource_leak"
    UNDEFINED_BEHAVIOR = "undefined_behavior"
    GARBAGE_COLLECTION = "garbage_collection"
    PERFORMANCE = "performance"
    ENGINE_BEST_PRACTICE = "engine_best_practice"
    EDGE_CASE = "edge_case"
    INPUT_HANDLING = "input_handling"
    DESIGN = "design"
    ACCESSIBILITY = "accessibility"  # HTML/CSS (ADR-0015)
    MAINTAINABILITY = "maintainability"  # HTML/CSS (ADR-0015)


class PipelineMode(StrEnum):
    """Pipeline çağrı modu (mimari §5.4, §17 `pipeline.mode`)."""

    TWO_PASS = "two_pass"
    SINGLE_PASS = "single_pass"


class LoopBound(StrEnum):
    """Döngü sınır sınıfı sezgiseli (mimari §5.3.1)."""

    LINEAR = "linear"
    LOG = "log"
    CONSTANT = "constant"
    UNKNOWN = "unknown"


class AllocationKind(StrEnum):
    """Tahsis türleri (mimari §5.3.1 `allocations`)."""

    MALLOC = "malloc"
    CALLOC = "calloc"
    REALLOC = "realloc"
    NEW = "new"
    NEW_ARRAY = "new_array"
    MAKE_UNIQUE = "make_unique"
    MAKE_SHARED = "make_shared"
    CSHARP_NEW = "csharp_new"
    STRING_CONCAT = "string_concat"
    LINQ = "linq"
    CLOSURE = "closure"


class DeallocationKind(StrEnum):
    """Serbest bırakma türleri (mimari §5.3.1 `deallocations`)."""

    FREE = "free"
    DELETE = "delete"
    DELETE_ARRAY = "delete_array"


# İşaretleme/stil dilleri (ADR-0015): Big-O ve olgu çıkarımı yok, karmaşıklık kartı yok.
MARKUP_LANGUAGES: frozenset[Language] = frozenset({Language.HTML, Language.CSS})


def has_complexity(language: Language) -> bool:
    """Dilde zaman/bellek karmaşıklığı (olgular, Big-O ipucu, Geçiş A karmaşıklığı) anlamlı mı."""
    return language not in MARKUP_LANGUAGES


_ENGINE_LANGUAGE = {Engine.UNITY: Language.CSHARP, Engine.UNREAL: Language.CPP}


def required_language(engine: Engine | None) -> Language | None:
    """Motorun gerektirdiği dil (Unity → C#, Unreal → C++); motor yoksa None."""
    return _ENGINE_LANGUAGE.get(engine) if engine is not None else None


def check_engine_language(language: Language, engine: Engine | None) -> None:
    """Dil/motor uyumsuzsa Türkçe mesajlı `ValueError` fırlatır."""
    required = required_language(engine)
    if required is not None and language != required:
        raise ValueError(f"{engine} motoru yalnızca {required} diliyle kullanılabilir")
