"""Eval veri seti (mimari §14.1): `eval/dataset/{dev,test,_draft}/{id}/code.* + label.yaml`.

Yükleyici etiketi şemaya göre doğrular, satırların kodda olduğunu ve `dev`/`test` arasında
aynı örneğin (kimlik ya da içerik) bulunmadığını denetler. Onaylanmamış örnekler `_draft/`'ta
kalır; `promote` onları gözden geçirildi işaretiyle bir bölüme taşır.
"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from codementor.ingest.normalize import split_lines
from codementor.languages import CANONICAL_SUFFIX
from codementor.models.enums import Language
from codementor.models.eval import Label, Sample, Split
from codementor.questions._loader import DataFileError, load_model

DATASET_DIR = Path("eval/dataset")
DRAFT = "_draft"
SPLITS: tuple[Split, ...] = ("dev", "test")


def code_suffix(language: str) -> str:
    """Örnek kod dosyasının uzantısı (tek tablo: `codementor.languages`, Faz 50)."""
    return CANONICAL_SUFFIX[Language(language)]


class DatasetError(DataFileError):
    """Veri seti dosyası eksik ya da tutarsız."""


def _code_file(directory: Path) -> Path:
    files = sorted(p for p in directory.glob("code.*") if p.is_file())
    if len(files) != 1:
        raise DatasetError(f"{directory.name}: tam olarak bir code.* dosyası olmalı")
    return files[0]


def load_sample(directory: Path) -> Sample:
    """Tek örnek: etiket şeması, kimlik = dizin adı, uzantı = dil, satırlar kodda."""
    label = load_model(directory / "label.yaml", Label, DatasetError)
    if label.id != directory.name:
        raise DatasetError(f"{directory.name}: label.id ({label.id}) dizin adıyla aynı olmalı")
    code_file = _code_file(directory)
    expected_suffix = code_suffix(label.language.value)
    if code_file.suffix != expected_suffix:
        raise DatasetError(
            f"{label.id}: {label.language.value} için dosya {expected_suffix} olmalı"
        )
    code = code_file.read_text(encoding="utf-8")
    lines = len(split_lines(code.replace("\r\n", "\n")))
    for finding in label.expected.findings:
        if finding.line > lines:
            raise DatasetError(f"{label.id}: {finding.line}. satır kodda yok ({lines} satır)")
    return Sample(label=label, code=code, path=directory.as_posix())


def load_split(root: Path, split: str) -> list[Sample]:
    """Bir bölümdeki tüm örnekler, kimliğe göre sıralı."""
    directory = root / split
    if not directory.is_dir():
        raise DatasetError(f"Veri seti bölümü bulunamadı: {directory}")
    return [load_sample(d) for d in sorted(directory.iterdir()) if d.is_dir()]


def _fingerprint(code: str) -> str:
    return hashlib.sha256("".join(code.split()).encode("utf-8")).hexdigest()


def check_disjoint(root: Path) -> list[str]:
    """`dev`/`test`/`_draft` arasında aynı kimlik ya da aynı kod (boşluk yok sayılarak)."""
    problems: list[str] = []
    seen_ids: dict[str, str] = {}
    seen_code: dict[str, str] = {}
    for split in (*SPLITS, DRAFT):
        if not (root / split).is_dir():
            continue
        for sample in load_split(root, split):
            where = f"{split}/{sample.label.id}"
            if sample.label.id in seen_ids:
                problems.append(f"{where}: kimlik {seen_ids[sample.label.id]} ile aynı")
            fingerprint = _fingerprint(sample.code)
            if fingerprint in seen_code:
                problems.append(f"{where}: kod {seen_code[fingerprint]} ile aynı")
            seen_ids.setdefault(sample.label.id, where)
            seen_code.setdefault(fingerprint, where)
    return problems


def _set_fields(text: str, **fields: str) -> str:
    """Üst düzey `anahtar: değer` satırlarını değiştirir/ekler; yorumlar ve düzen korunur."""
    lines = text.replace("\r\n", "\n").rstrip("\n").split("\n")
    for key, value in fields.items():
        prefix = f"{key}:"
        index = next((i for i, line in enumerate(lines) if line.startswith(prefix)), None)
        if index is None:
            lines.append(f"{prefix} {value}")
        else:
            lines[index] = f"{prefix} {value}"
    return "\n".join(lines) + "\n"


def promote(root: Path, sample_id: str, split: Split) -> Path:
    """`_draft/{id}` → `{split}/{id}`; etikete `reviewed: true` ve `split` yazılır."""
    source = root / DRAFT / sample_id
    if not source.is_dir():
        raise DatasetError(f"Taslak bulunamadı: {source}")
    target = root / split / sample_id
    if target.exists():
        raise DatasetError(f"Zaten var: {target}")
    load_sample(source)  # geçersiz taslak taşınmaz
    label_path = source / "label.yaml"
    label_path.write_text(
        _set_fields(label_path.read_text(encoding="utf-8"), reviewed="true", split=split),
        encoding="utf-8",
        newline="\n",
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))
    return target
