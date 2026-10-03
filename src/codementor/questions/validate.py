"""Soru bankası bütünlük denetimi (Faz 30, `codementor questions validate`).

Şema doğrulaması yüklemede yapılır (`QuestionBank.load`); burada bankanın bütünü denetlenir:

- her dil/motor grubunda en az `min_per_group` soru ve her zorluktan en az bir soru;
- her sorunun kavram etiketleri kontrol listesinde en az bir (çekirdek dışı) maddeyle kesişir;
- `solutions_root` verilirse referans çözüm dosyası var mı (yoksa uyarı: `private/` depoda
  değildir, CI'da bulunmaz).
"""

from __future__ import annotations

from pathlib import Path

from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.questions import BankReport
from codementor.questions.bank import QuestionBank
from codementor.questions.checklists import CORE_TAG, Checklists

DEFAULT_MIN_PER_GROUP = 8


def validate_bank(
    bank: QuestionBank,
    checklists: Checklists,
    *,
    min_per_group: int = DEFAULT_MIN_PER_GROUP,
    solutions_root: Path | None = None,
) -> BankReport:
    """Bankanın dağılımını, kontrol listesi kapsamını ve (istenirse) çözüm dosyalarını denetler."""
    errors: list[str] = []
    warnings: list[str] = []
    groups: dict[tuple[Language, Engine], set[Difficulty]] = {}
    counts: dict[tuple[Language, Engine], int] = {}
    for q in bank:
        key = (q.language, q.engine)
        groups.setdefault(key, set()).add(q.difficulty)
        counts[key] = counts.get(key, 0) + 1
        items = checklists.select_items(q.language, q.engine, q.concept_tags)
        if not any(CORE_TAG not in item.tags for item in items):
            errors.append(f"{q.id}: kavram etiketleri hiçbir kontrol maddesiyle kesişmiyor")
        if (
            solutions_root is not None
            and q.reference_solution_path is not None
            and not (solutions_root / q.reference_solution_path).is_file()
        ):
            warnings.append(f"{q.id}: referans çözüm dosyası yok ({q.reference_solution_path})")
    if len(bank) == 0:
        errors.append("Soru bankası boş: dizinde hiç soru dosyası yok")
    for (language, engine), difficulties in sorted(groups.items()):
        name = language.value if engine is Engine.NONE else f"{language.value}/{engine.value}"
        if counts[(language, engine)] < min_per_group:
            errors.append(
                f"{name}: {counts[(language, engine)]} soru var, en az {min_per_group} olmalı"
            )
        missing = [d.value for d in Difficulty if d not in difficulties]
        if missing:
            errors.append(f"{name}: şu zorluklarda soru yok: {', '.join(missing)}")
    return BankReport(question_count=len(bank), errors=errors, warnings=warnings)
