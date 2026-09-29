"""Soru bankası ve kontrol listesi modelleri (mimari §7.1, §8.3)."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Annotated, Self

from pydantic import AfterValidator, Field, StringConstraints, field_validator, model_validator

from codementor.models._base import StrictModel
from codementor.models.bigo import parse_bigo
from codementor.models.enums import Difficulty, Engine, Language

QUESTION_ID_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)+$"
CHECKLIST_ITEM_ID_PATTERN = r"^[A-Z]+-[A-Z]+-\d{3}$"
TAG_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
REFERENCE_ROOT = "private"
HINT_LEVELS = (1, 2, 3)

# Mentorluk motoruna ait, öğrenciye/API'ye verilmeyen alanlar (Question'da, QuestionPublic'te yok)
MENTOR_FIELDS = frozenset({"concept_tags", "checklist_extra", "hint_ladder"})

# Motorun gerektirdiği dil (mimari §7.2): Unity → C#, Unreal → C++
_ENGINE_LANGUAGE = {Engine.UNITY: Language.CSHARP, Engine.UNREAL: Language.CPP}


def _check_bigo(value: str) -> str:
    """Big-O metnini doğrular; sondaki `*` amortize işaretidir (`1*`)."""
    parse_bigo(value.removesuffix("*"))
    return value


def _check_unique(values: list[str]) -> list[str]:
    duplicates = sorted({v for v in values if values.count(v) > 1})
    if duplicates:
        raise ValueError(f"yinelenen öğe: {', '.join(duplicates)}")
    return values


def _check_engine_language(language: Language, engine: Engine | None) -> None:
    required = _ENGINE_LANGUAGE.get(engine) if engine is not None else None
    if required is not None and language != required:
        raise ValueError(f"{engine} motoru yalnızca {required} diliyle kullanılabilir")


BigOText = Annotated[str, AfterValidator(_check_bigo)]
NonEmptyText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Tag = Annotated[str, StringConstraints(pattern=TAG_PATTERN)]
TagList = Annotated[list[Tag], Field(min_length=1), AfterValidator(_check_unique)]


class ExpectedComplexity(StrictModel):
    """Sorunun beklenen karmaşıklığı; işlem adı → Big-O."""

    time: dict[NonEmptyText, BigOText] = Field(min_length=1)
    space: BigOText


class QuestionPublic(StrictModel):
    """Öğrenciye (API, CLI) verilen soru: yalnızca problem tanımı.

    Referans çözüm (mimari §12) ve mentorluk verisi (`MENTOR_FIELDS`: kavram
    etiketleri, soruya özgü kontrol maddeleri, ipucu merdiveni) içermez; ipuçları
    analiz sırasında kademeli açılır.
    """

    id: str = Field(pattern=QUESTION_ID_PATTERN)
    version: int = Field(ge=1)
    language: Language
    engine: Engine
    difficulty: Difficulty
    title: NonEmptyText = Field(max_length=120)
    prompt: NonEmptyText
    constraints: list[NonEmptyText] = Field(min_length=1)
    expected: ExpectedComplexity

    @model_validator(mode="after")
    def _engine_matches_language(self) -> Self:
        _check_engine_language(self.language, self.engine)
        return self


class Question(QuestionPublic):
    """Tam soru kaydı (iç kullanım): mentorluk verisi + referans çözüm yolu."""

    concept_tags: TagList
    checklist_extra: list[NonEmptyText] = Field(default_factory=list)
    hint_ladder: dict[int, str]
    reference_solution_path: str | None = Field(
        default=None, description="Yalnızca K5 sızıntı korumasında okunur; asla dışarı verilmez"
    )

    @field_validator("hint_ladder")
    @classmethod
    def _three_levels(cls, ladder: dict[int, str]) -> dict[int, str]:
        if tuple(sorted(ladder)) != HINT_LEVELS:
            raise ValueError("tam olarak 1, 2 ve 3. seviye ipuçları olmalı")
        if any(not hint.strip() for hint in ladder.values()):
            raise ValueError("ipucu metni boş olamaz")
        return {level: ladder[level].strip() for level in HINT_LEVELS}

    @field_validator("reference_solution_path")
    @classmethod
    def _inside_private(cls, path: str | None) -> str | None:
        """`private/` altında göreli bir dosya yolu; normalleştirilmiş hali saklanır.

        Metinsel denetimdir; dosyayı okuyan bileşen (K5) ayrıca `resolve()` +
        `is_relative_to()` ile sembolik bağlantılara karşı denetlemelidir.
        """
        if path is None:
            return None
        pure = PurePosixPath(path)
        invalid = (
            any(ord(c) < 32 or c in ":\\" for c in path)
            or pure.is_absolute()
            or len(pure.parts) < 2
            or pure.parts[0] != REFERENCE_ROOT
            or ".." in pure.parts
        )
        if invalid:
            raise ValueError(
                f"referans çözüm yolu '{REFERENCE_ROOT}/' altında göreli bir dosya olmalı"
            )
        return str(pure)

    def to_public(self) -> QuestionPublic:
        """Mentorluk verisi ve referans çözüm bilgisi atılmış kopya."""
        exclude = {*MENTOR_FIELDS, "reference_solution_path"}
        return QuestionPublic.model_validate(self.model_dump(exclude=exclude))


class AppliesTo(StrictModel):
    """Kontrol listesinin geçerli olduğu dil ve (isteğe bağlı) motor; motor yoksa tümü."""

    language: Language
    engine: Engine | None = None

    @model_validator(mode="after")
    def _engine_matches_language(self) -> Self:
        _check_engine_language(self.language, self.engine)
        return self


class ChecklistItem(StrictModel):
    id: str = Field(pattern=CHECKLIST_ITEM_ID_PATTERN)
    text: NonEmptyText
    tags: TagList


class ChecklistFile(StrictModel):
    version: int = Field(ge=1)
    applies_to: AppliesTo
    items: list[ChecklistItem] = Field(min_length=1)
