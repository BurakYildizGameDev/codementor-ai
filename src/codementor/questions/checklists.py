"""Dil/motor kontrol listeleri ve LLM'e enjekte edilecek madde seçimi (mimari §8.3)."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from pathlib import Path

from codementor.models.enums import Engine, Language
from codementor.models.questions import ChecklistFile, ChecklistItem
from codementor.questions._loader import DataFileError, list_yaml_files, load_model

CORE_TAG = "core"
DEFAULT_LIMIT = 12


class ChecklistError(DataFileError):
    """Kontrol listeleri yüklenemedi."""


class Checklists:
    """Yüklenmiş kontrol listesi dosyaları (dosya adı → içerik, ada göre sıralı)."""

    def __init__(self, files: dict[str, ChecklistFile]) -> None:
        self._files = dict(sorted(files.items()))
        seen: dict[str, str] = {}
        for name, checklist in self._files.items():
            for item in checklist.items:
                if item.id in seen:
                    where = (
                        f"{name} içinde birden fazla kez"
                        if seen[item.id] == name
                        else f"{seen[item.id]} ve {name}"
                    )
                    raise ChecklistError(f"Yinelenen kontrol maddesi {item.id!r}: {where}")
                seen[item.id] = name

    @classmethod
    def load(cls, directory: Path) -> Checklists:
        """`directory` altındaki tüm kontrol listesi dosyalarını yükler."""
        return cls(
            {
                path.name: load_model(path, ChecklistFile, ChecklistError)
                for path in list_yaml_files(directory, ChecklistError)
            }
        )

    def __len__(self) -> int:
        return len(self._files)

    def all_items(self) -> Iterator[ChecklistItem]:
        for checklist in self._files.values():
            yield from checklist.items

    def _applicable(self, language: Language, engine: Engine) -> list[ChecklistItem]:
        """Uygun maddeler: önce motora özgü dosyalar, sonra dilin genel dosyaları."""
        specific: list[ChecklistItem] = []
        generic: list[ChecklistItem] = []
        for checklist in self._files.values():
            target = checklist.applies_to
            if target.language != language:
                continue
            if target.engine is None:
                generic.extend(checklist.items)
            elif target.engine == engine:
                specific.extend(checklist.items)
        return specific + generic

    def select_items(
        self,
        language: Language,
        engine: Engine,
        concept_tags: Iterable[str],
        limit: int = DEFAULT_LIMIT,
    ) -> list[ChecklistItem]:
        """LLM'e verilecek maddeler: `core` maddeler + soru etiketleriyle kesişenler.

        Sıra: core (motora özgü önce) → kesişen etiket sayısı azalan (eşitlikte
        motora özgü önce, sonra dosya sırası). En fazla `limit` madde.
        """
        if isinstance(concept_tags, str):
            raise TypeError("concept_tags tek bir metin değil, etiket listesi olmalı")
        if limit < 0:
            raise ValueError(f"limit negatif olamaz: {limit}")
        tags = set(concept_tags) - {CORE_TAG}
        candidates = self._applicable(language, engine)
        core = [item for item in candidates if CORE_TAG in item.tags]
        tagged = sorted(
            (item for item in candidates if CORE_TAG not in item.tags and tags & set(item.tags)),
            key=lambda item: -len(tags & set(item.tags)),
        )
        return (core + tagged)[:limit]
