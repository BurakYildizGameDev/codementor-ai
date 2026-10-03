"""Few-shot örnekleri: `prompts/v1/fewshots/{language}_{engine}_*.yaml` (mimari §5.4.4).

Örnekler küçük modellere kanıt biçimini (satırdan birebir alıntı, önek yok) ve statik
bulguları tekrar etmemeyi gösterir; bu yüzden yüklenirken kanıtlar koda karşı doğrulanır.
Faz 36: "temiz" örnekler (hata yok; en fazla öneri) modelin her kodda sorun aramamasını öğretir.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from codementor.ingest.normalize import numbered_view, split_lines
from codementor.models.enums import Engine, Language, has_complexity
from codementor.models.llm_output import LLMAnalysisOutput
from codementor.models.prompts import FewShotExample, FewShotView
from codementor.questions._loader import DataFileError, list_yaml_files, load_model


class FewShotError(DataFileError):
    """Few-shot dosyası okunamadı ya da geçersiz."""


def _window(lines: list[str], start: int, end: int | None) -> str:
    return "\n".join(lines[start - 1 : end or start])


def _validate(example: FewShotExample, source: Path) -> None:
    if has_complexity(example.language) != isinstance(example.analysis, LLMAnalysisOutput):
        need = "gerekli" if has_complexity(example.language) else "olmamalı"
        raise FewShotError(f"{source.name}: {example.language} örneğinde karmaşıklık {need}")
    lines = split_lines(example.code)
    checks = [(f.line, None, f.evidence) for f in example.static_findings] + [
        (f.line_start, f.line_end, f.evidence) for f in example.analysis.additional_findings
    ]
    for start, end, evidence in checks:
        if start > len(lines) or (end is not None and not start <= end <= len(lines)):
            raise FewShotError(f"{source.name}: {start}. satır kodda yok")
        if not evidence.strip() or evidence not in _window(lines, start, end):
            raise FewShotError(
                f"{source.name}: {start}. satırdaki kanıt koddan birebir alıntı değil: {evidence!r}"
            )
    # Örnek "tekrar etme"yi öğretir: statik bulgunun satırına yeni bulgu konmaz (farklı alt
    # dizeyle aynı sorunu yeniden yazmak da tekrardır).
    static_lines = {f.line for f in example.static_findings}
    for finding in example.analysis.additional_findings:
        end = finding.line_end or finding.line_start
        if static_lines & set(range(finding.line_start, end + 1)):
            raise FewShotError(
                f"{source.name}: {finding.line_start}. satır statik bulguyu tekrar ediyor"
            )


def load_fewshots(directory: Path) -> list[FewShotExample]:
    """Dizindeki tüm örnekleri yükler ve doğrular; kimlikler benzersiz olmalı."""
    examples: list[FewShotExample] = []
    seen: dict[str, str] = {}
    for path in list_yaml_files(directory, FewShotError):
        example = load_model(path, FewShotExample, FewShotError)
        if example.id in seen:
            raise FewShotError(
                f"{path.name}: '{example.id}' kimliği {seen[example.id]} ile çakışıyor"
            )
        seen[example.id] = path.name
        _validate(example, path)
        examples.append(example)
    return examples


def is_clean(example: FewShotExample) -> bool:
    """Temiz kod örneği: statik bulgu yok, modelin bulguları (varsa) yalnızca öneri."""
    return not example.static_findings and all(
        f.kind == "suggestion" for f in example.analysis.additional_findings
    )


def select_fewshots(
    examples: Iterable[FewShotExample], language: Language, engine: Engine, limit: int
) -> list[FewShotExample]:
    """Önce aynı dil + motor, sonra aynı dilin diğer örnekleri; kimliğe göre belirleyici.

    Faz 36: ilk sırada en uygun hatalı örnek, ikinci sırada en uygun temiz örnek (limit 1'de
    yalnız hatalı örnek kalır: few-shot ablasyonu eskisi gibi).
    """
    if limit <= 0:
        return []
    ordered = sorted(examples, key=lambda e: e.id)
    exact = [e for e in ordered if e.language == language and e.engine == engine]
    related = [e for e in ordered if e.language == language and e.engine != engine]
    ranked = exact + related
    flawed = [e for e in ranked if not is_clean(e)]
    clean = [e for e in ranked if is_clean(e)]
    head = flawed[:1] + clean[:1]
    return (head + [e for e in ranked if e not in head])[:limit]


def fewshot_view(example: FewShotExample, *, numbered: bool = True) -> FewShotView:
    """Şablon için kod (numaralı; `numbered_code` ablasyonunda düz) ve kısa JSON metinleri."""
    return FewShotView(
        title=example.title,
        numbered_code=numbered_view(split_lines(example.code)) if numbered else example.code,
        static_hint=example.static_hint,
        static_findings=example.static_findings,
        analysis_json=json.dumps(example.analysis.model_dump(mode="json"), ensure_ascii=False),
        socratic_json=json.dumps(example.socratic.model_dump(mode="json"), ensure_ascii=False),
    )
