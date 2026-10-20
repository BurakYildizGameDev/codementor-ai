"""Kullanıcı soruları deposu (ADR-0028, Faz K).

Sorular `data.user_questions_dir` altında (varsayılan `~/.codementor/questions`) yerleşik bankayla
aynı YAML biçiminde, `kullanici-<başlık>.yaml` adıyla durur. Yazım atomiktir (geçici dosya +
`os.replace`). Bozuk bir kullanıcı dosyası uygulamayı düşürmez: atlanır ve uyarı döner.
"""

from __future__ import annotations

import os
import re
import tempfile
import unicodedata
from pathlib import Path

import yaml

from codementor.log import get_logger
from codementor.models.questions import (
    QUESTION_ID_PATTERN,
    USER_QUESTION_PREFIX,
    Question,
    UserQuestionDraft,
)
from codementor.paths import replace_file
from codementor.questions._loader import DataFileError, list_yaml_files, load_model

log = get_logger("codementor.questions")

_SLUG_MAX = 48
_TURKISH = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


class UserQuestionError(DataFileError):
    """Kullanıcı sorusu kaydedilemedi, silinemedi ya da bulunamadı (mesaj Türkçe)."""


def slugify(title: str) -> str:
    """`Bağlı liste — tersine çevir` → `bagli-liste-tersine-cevir` (en çok 48 karakter)."""
    text = unicodedata.normalize("NFKD", title.translate(_TURKISH))
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", text).strip("-")[:_SLUG_MAX].strip("-")
    return slug or "soru"


def _path(directory: Path, question_id: str) -> Path:
    return directory / f"{question_id}.yaml"


def _is_user_id(question_id: str) -> bool:
    """Kimlik deseni (yol ayırıcısı, `..` olamaz) + kullanıcı öneki."""
    return question_id.startswith(USER_QUESTION_PREFIX) and bool(
        re.fullmatch(QUESTION_ID_PATTERN, question_id)
    )


def new_question_id(
    title: str, directory: Path, taken: set[str] | frozenset[str] = frozenset()
) -> str:
    """Başlıktan benzersiz kimlik; dosya ya da `taken` ile çakışırsa `-2`, `-3` …"""
    base = f"{USER_QUESTION_PREFIX}{slugify(title)}"
    candidate, n = base, 2
    while candidate in taken or _path(directory, candidate).exists():
        candidate, n = f"{base}-{n}", n + 1
    return candidate


def _write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.stem}-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        replace_file(Path(tmp), path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def _dump(question: Question) -> str:
    data = question.model_dump(mode="json", exclude={"reference_solution_path"})
    if data.get("expected") is None:
        data.pop("expected", None)
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100)


def save_question(
    draft: UserQuestionDraft,
    directory: Path,
    *,
    question_id: str | None = None,
    taken: set[str] | frozenset[str] = frozenset(),
) -> Question:
    """Yeni soru kaydeder ya da `question_id` verilirse onu günceller (sürüm bir artar).

    `taken`: yerleşik bankadaki kimlikler (yeni kimlik bunlarla da çakışmaz).
    """
    version = 1
    if question_id is None:
        question_id = new_question_id(draft.title, directory, taken)
    else:
        existing = get_question(question_id, directory)
        version = existing.version + 1
    question = draft.to_question(question_id, version=version)
    try:
        _write_atomic(_path(directory, question_id), _dump(question))
    except OSError as exc:
        raise UserQuestionError(f"Soru kaydedilemedi: {exc}") from exc
    return question


def get_question(question_id: str, directory: Path) -> Question:
    """Kayıtlı kullanıcı sorusu; yoksa ya da yerleşik bir kimlikse `UserQuestionError`."""
    path = _path(directory, question_id)
    if not _is_user_id(question_id) or not path.is_file():
        raise UserQuestionError(f"Kullanıcı sorusu bulunamadı: {question_id}")
    return _load(path)


def delete_question(question_id: str, directory: Path) -> None:
    """Kullanıcı sorusunu siler; yerleşik sorular silinemez."""
    path = _path(directory, question_id)
    if not _is_user_id(question_id) or not path.is_file():
        raise UserQuestionError(
            f"Yalnız kendi eklediğin sorular silinebilir; bulunamadı: {question_id}"
        )
    try:
        path.unlink()
    except OSError as exc:
        raise UserQuestionError(f"Soru silinemedi: {exc}") from exc


def _load(path: Path) -> Question:
    question = load_model(path, Question, UserQuestionError)
    if question.id != path.stem:
        raise UserQuestionError(f"{path.name}: id ({question.id!r}) dosya adıyla eşleşmiyor")
    if question.origin != "user" or not _is_user_id(question.id):
        raise UserQuestionError(f"{path.name}: kullanıcı sorusu değil (origin: user olmalı)")
    return question


def load_user_questions(directory: Path) -> tuple[list[Question], list[str]]:
    """Dizindeki kullanıcı soruları ve okunamayan dosyalar için Türkçe uyarılar.

    Dizin yoksa boş liste (ilk soru eklenince oluşur).
    """
    if not directory.is_dir():
        return [], []
    questions: list[Question] = []
    warnings: list[str] = []
    try:
        paths = list_yaml_files(directory, UserQuestionError)
    except DataFileError as exc:
        return [], [f"Kendi soruların okunamadı: {exc}"]
    for path in paths:
        # denetim Y-2: depo yalnız `.yaml` yazar/okur; `.yml` kopyası aynı kimliği iki kez
        # getirip yerleşik bankayı da düşürüyordu
        if path.suffix != ".yaml":
            warnings.append(f"Kendi sorun atlandı (yalnız .yaml okunur): {path.name}")
            continue
        try:
            questions.append(_load(path))
        except DataFileError as exc:
            log.warning("user_question_skipped", file=path.name, error=str(exc)[:300])
            warnings.append(f"Kendi sorun okunamadı, atlandı: {exc}")
    return questions, warnings
