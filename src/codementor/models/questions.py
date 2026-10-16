"""Soru bankası ve kontrol listesi modelleri (mimari §7.1, §8.3)."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Annotated, Literal, Self

from pydantic import (
    AfterValidator,
    BeforeValidator,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from codementor.models._base import StrictModel
from codementor.models.bigo import parse_cost
from codementor.models.enums import (
    Difficulty,
    Engine,
    Language,
    check_engine_language,
    has_complexity,
)

QUESTION_ID_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)+$"
# Faz K (ADR-0028): kullanıcı soruları bu önekle kimlik alır; yerleşik kimliklerle çakışmaz
USER_QUESTION_PREFIX = "kullanici-"
QuestionOrigin = Literal["builtin", "user"]
CHECKLIST_ITEM_ID_PATTERN = r"^[A-Z]+-[A-Z]+-\d{3}$"
TAG_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
REFERENCE_ROOT = "private"
HINT_LEVELS = (1, 2, 3)

# Mentorluk motoruna ait, öğrenciye/API'ye verilmeyen alanlar (Question'da, QuestionPublic'te yok)
MENTOR_FIELDS = frozenset({"concept_tags", "checklist_extra", "hint_ladder"})


def _check_bigo(value: str) -> str:
    """Big-O metnini doğrular; sondaki `*` amortize işaretidir (`1*`)."""
    parse_cost(value)
    return value


def _check_unique(values: list[str]) -> list[str]:
    duplicates = sorted({v for v in values if values.count(v) > 1})
    if duplicates:
        raise ValueError(f"yinelenen öğe: {', '.join(duplicates)}")
    return values


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
    expected: ExpectedComplexity | None = Field(
        default=None,
        description="Hedef karmaşıklık; HTML/CSS görevlerinde ve isteğe bağlı olarak kullanıcı "
        "sorularında yok (ADR-0015, ADR-0028)",
    )
    origin: QuestionOrigin = Field(
        default="builtin", description="builtin: soru bankası; user: kullanıcının eklediği"
    )

    @model_validator(mode="after")
    def _engine_matches_language(self) -> Self:
        check_engine_language(self.language, self.engine)
        if self.origin == "user" and not self.id.startswith(USER_QUESTION_PREFIX):
            raise ValueError(f"kullanıcı sorusu kimliği '{USER_QUESTION_PREFIX}' ile başlamalı")
        if has_complexity(self.language) and self.expected is None and self.origin == "builtin":
            raise ValueError(f"{self.language} görevi hedef karmaşıklık (expected) içermeli")
        if not has_complexity(self.language) and self.expected is not None:
            raise ValueError(f"{self.language} görevinde hedef karmaşıklık olmaz")
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
        check_engine_language(self.language, self.engine)
        return self


class ChecklistItem(StrictModel):
    id: str = Field(pattern=CHECKLIST_ITEM_ID_PATTERN)
    text: NonEmptyText
    tags: TagList


class ChecklistFile(StrictModel):
    version: int = Field(ge=1)
    applies_to: AppliesTo
    items: list[ChecklistItem] = Field(min_length=1)


class BankReport(StrictModel):
    """`codementor questions validate` sonucu (Faz 30): hatalar başarısızlık, uyarılar bilgi."""

    question_count: int = Field(ge=0)
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


# --- Faz K (ADR-0028): kullanıcı soruları -------------------------------------------------------

DEFAULT_USER_CONSTRAINT = "Görev tanımındaki gereksinimler eksiksiz karşılanmalı."
DEFAULT_USER_TAG = "genel"  # kontrol listesinde yalnız `core` maddeler seçilir
DEFAULT_USER_HINTS = (
    "Görevin kısıtlarını tek tek düşün: kodun hangisini henüz karşılamıyor olabilir?",
    "Şüphelendiğin satırı en küçük bir girdiyle elle izle; beklediğinle gördüğün nerede ayrılıyor?",
    "Bulduğun sorunun genel adı nedir ve bu tür hatalar genellikle nasıl önlenir?",
)
EXPECTED_OPERATION = "çözüm"  # tek hedef zaman karmaşıklığının işlem adı


def _strip_bigo(value: object) -> object:
    """Formdan gelen `O(n log n)` → `n log n`; boş metin → None."""
    if not isinstance(value, str):
        return value
    text = value.strip()
    if not text:
        return None
    if text[:2].upper() == "O(" and text.endswith(")"):
        text = text[2:-1].strip()
    return text


def _clean_lines(value: object) -> object:
    """Boş satırlar atılır (form metin kutusu satır başına bir öğe verir)."""
    if isinstance(value, list):
        return [v for v in value if not isinstance(v, str) or v.strip()]
    return value


OptionalBigO = Annotated[BigOText | None, BeforeValidator(_strip_bigo)]
MAX_USER_PROMPT_CHARS = 4000
MAX_USER_ITEM_CHARS = 400
MAX_USER_ITEMS = 12
ShortUserText = Annotated[NonEmptyText, StringConstraints(max_length=MAX_USER_ITEM_CHARS)]


class UserQuestionDraft(StrictModel):
    """Kullanıcının masaüstü formundan ya da CLI YAML'ından verdiği soru (ADR-0028).

    Zorunlu: başlık, açıklama, dil, zorluk. Kısıtlar, hedef karmaşıklık, kavram etiketleri ve
    ipuçları isteğe bağlı; boş olanlar `to_question` ile genel değerlerle doldurulur.
    """

    title: NonEmptyText = Field(max_length=120)
    # denetim: kullanıcı metni prompt'a girer; bütçe ve kötüye kullanım için üst sınır
    prompt: NonEmptyText = Field(max_length=MAX_USER_PROMPT_CHARS)
    language: Language
    engine: Engine = Engine.NONE
    difficulty: Difficulty
    constraints: Annotated[list[ShortUserText], BeforeValidator(_clean_lines)] = Field(
        default_factory=list, max_length=MAX_USER_ITEMS
    )
    expected_time: OptionalBigO = None
    expected_space: OptionalBigO = None
    concept_tags: Annotated[list[Tag], BeforeValidator(_clean_lines)] = Field(
        default_factory=list, max_length=MAX_USER_ITEMS
    )
    hints: Annotated[list[ShortUserText], BeforeValidator(_clean_lines)] = Field(
        default_factory=list, max_length=3
    )

    @model_validator(mode="after")
    def _consistent(self) -> Self:
        check_engine_language(self.language, self.engine)
        given = (self.expected_time is not None, self.expected_space is not None)
        if not has_complexity(self.language) and any(given):
            raise ValueError(f"{self.language} görevinde hedef karmaşıklık olmaz")
        if given[0] != given[1]:
            raise ValueError(
                "hedef karmaşıklık için hem zaman hem bellek verilmeli (ya da hiçbiri)"
            )
        return self

    def to_question(self, question_id: str, version: int = 1) -> Question:
        """Tam soru kaydı: boş alanlar genel değerlerle dolar, referans çözüm yok."""
        expected = (
            ExpectedComplexity(
                time={EXPECTED_OPERATION: self.expected_time}, space=self.expected_space
            )
            if self.expected_time is not None and self.expected_space is not None
            else None
        )
        hints = [*self.hints, *DEFAULT_USER_HINTS[len(self.hints) :]]
        return Question(
            id=question_id,
            version=version,
            language=self.language,
            engine=self.engine,
            difficulty=self.difficulty,
            title=self.title,
            prompt=self.prompt,
            constraints=self.constraints or [DEFAULT_USER_CONSTRAINT],
            expected=expected,
            origin="user",
            concept_tags=list(dict.fromkeys(self.concept_tags)) or [DEFAULT_USER_TAG],
            hint_ladder=dict(zip(HINT_LEVELS, hints, strict=True)),
            reference_solution_path=None,
        )

    @classmethod
    def from_question(cls, question: Question) -> UserQuestionDraft:
        """Düzenleme formu için mevcut sorudan taslak.

        Yalnızca genel varsayılanlardan oluşan alanlar formda boş görünür: kısıt listesi tam
        olarak `[DEFAULT_USER_CONSTRAINT]`, etiket listesi tam olarak `[DEFAULT_USER_TAG]` ise
        boşaltılır. Kullanıcı varsayılanı başka değerlerle birlikte açıkça yazdıysa liste
        olduğu gibi korunur (Faz G6: `['genel', 'dizi']` düzenlemede 'dizi'ye indirgeniyordu).
        """
        expected = question.expected
        hints = [question.hint_ladder[level] for level in HINT_LEVELS]
        while hints and hints[-1] == DEFAULT_USER_HINTS[len(hints) - 1]:
            hints.pop()
        return cls(
            title=question.title,
            prompt=question.prompt,
            language=question.language,
            engine=question.engine,
            difficulty=question.difficulty,
            constraints=(
                [] if question.constraints == [DEFAULT_USER_CONSTRAINT] else question.constraints
            ),
            expected_time=next(iter(expected.time.values())) if expected else None,
            expected_space=expected.space if expected else None,
            concept_tags=(
                [] if question.concept_tags == [DEFAULT_USER_TAG] else question.concept_tags
            ),
            hints=hints,
        )
