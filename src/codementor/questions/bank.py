"""YAML tabanlı soru bankası (mimari §7)."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from pathlib import Path

from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.questions import Question, QuestionPublic
from codementor.questions._loader import DataFileError, list_yaml_files, load_model

_LANGUAGE_ORDER = {lang: i for i, lang in enumerate(Language)}
_ENGINE_ORDER = {engine: i for i, engine in enumerate(Engine)}
_DIFFICULTY_ORDER = {diff: i for i, diff in enumerate(Difficulty)}


class QuestionBankError(DataFileError):
    """Soru bankası yüklenemedi."""


class QuestionNotFoundError(LookupError):
    """İstenen kimlikte soru yok."""

    def __init__(self, question_id: str) -> None:
        super().__init__(f"Soru bulunamadı: {question_id!r}")
        self.question_id = question_id


def _sort_key(q: Question) -> tuple[int, int, int, str]:
    return (
        _LANGUAGE_ORDER[q.language],
        _ENGINE_ORDER[q.engine],
        _DIFFICULTY_ORDER[q.difficulty],
        q.id,
    )


class QuestionBank:
    """Doğrulanmış soruların salt okunur koleksiyonu.

    Dışarıya dönük erişim (`public`, `filter`) `QuestionPublic` döndürür; referans
    çözüm yolu yalnızca `get` ile, iç bileşenlere (K5 sızıntı koruması) açıktır.
    """

    def __init__(self, questions: Iterable[Question]) -> None:
        self._questions: dict[str, Question] = {}
        for q in questions:
            if q.id in self._questions:
                raise QuestionBankError(f"Yinelenen soru kimliği {q.id!r}")
            self._questions[q.id] = q

    @classmethod
    def load(cls, directory: Path) -> QuestionBank:
        """`directory` altındaki tüm `*.yaml` / `*.yml` soru dosyalarını yükler."""
        questions: list[Question] = []
        sources: dict[str, Path] = {}
        for path in list_yaml_files(directory, QuestionBankError):
            q = load_model(path, Question, QuestionBankError)
            if q.id != path.stem:
                raise QuestionBankError(
                    f"{path.name}: id ({q.id!r}) dosya adıyla eşleşmiyor ({path.stem!r})"
                )
            if q.id in sources:
                raise QuestionBankError(
                    f"Yinelenen soru kimliği {q.id!r}: {sources[q.id].name} ve {path.name}"
                )
            sources[q.id] = path
            questions.append(q)
        return cls(questions)

    def __len__(self) -> int:
        return len(self._questions)

    def __contains__(self, question_id: object) -> bool:
        return question_id in self._questions

    def __iter__(self) -> Iterator[Question]:
        return iter(sorted(self._questions.values(), key=_sort_key))

    def get(self, question_id: str) -> Question:
        """Tam soru kaydı (iç kullanım)."""
        try:
            return self._questions[question_id]
        except KeyError:
            raise QuestionNotFoundError(question_id) from None

    def public(self, question_id: str) -> QuestionPublic:
        """Dışarıya verilebilir soru."""
        return self.get(question_id).to_public()

    def filter(
        self,
        language: Language | None = None,
        engine: Engine | None = None,
        difficulty: Difficulty | None = None,
    ) -> list[QuestionPublic]:
        """Verilen ölçütlerin hepsine uyan sorular (dil, motor, zorluk, id sırasıyla)."""
        return [
            q.to_public()
            for q in self
            if (language is None or q.language == language)
            and (engine is None or q.engine == engine)
            and (difficulty is None or q.difficulty == difficulty)
        ]
