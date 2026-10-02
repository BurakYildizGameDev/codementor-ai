"""Few-shot örnekleri: yükleme, doğrulama, seçim (mimari §5.4.1, §5.4.4)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from codementor.analysis.complexity_hint import compute_hint
from codementor.analysis.extractor import extract_facts
from codementor.ingest.normalize import normalize, split_lines
from codementor.models.bigo import parse_bigo
from codementor.models.enums import Engine, Language
from codementor.models.request import LanguageHint
from codementor.prompts.fewshot import (
    FewShotError,
    fewshot_view,
    load_fewshots,
    select_fewshots,
)
from codementor.rules.engine import run_rules

LINE_REFERENCE = re.compile(r"\d+\. satır")
REPO_FEWSHOTS = Path(__file__).resolve().parents[2] / "prompts" / "v1" / "fewshots"
COMBOS = [
    (Language.C, Engine.NONE),
    (Language.CPP, Engine.NONE),
    (Language.CSHARP, Engine.NONE),
    (Language.CSHARP, Engine.UNITY),
    (Language.CPP, Engine.UNREAL),
    (Language.PYTHON, Engine.NONE),
]

VALID = """\
id: c-ornek
language: c
engine: none
title: Örnek
code: |
  int f(int *a, int n) {
      int s = 0;
      for (int i = 0; i <= n; i++) s += a[i];
      return s;
  }
static_findings: []
analysis:
  complexity:
    reasoning_steps: ["Tek döngü n+1 kez döner."]
    time_complexity: "O(n)"
    space_complexity: "O(1)"
    optimal_time_target: "O(n)"
    agreement: no_hint
  additional_findings:
    - category: memory_safety
      severity: high
      line_start: 3
      line_end: null
      evidence: "i <= n"
      description: "Döngü dizinin sonundan bir fazla eleman okuyabilir."
socratic:
  key_flaw_concept: "Sınır dışı erişim"
  guiding_questions: ["n elemanlı bir dizide son geçerli indis kaçtır?"]
  next_step_hint: null
"""


def _write(tmp_path: Path, text: str, name: str = "c_none_ornek.yaml") -> Path:
    (tmp_path / name).write_text(text, encoding="utf-8")
    return tmp_path


def test_repo_fewshots_load_and_cover_every_combo() -> None:
    examples = load_fewshots(REPO_FEWSHOTS)
    for language, engine in COMBOS:
        matching = [e for e in examples if (e.language, e.engine) == (language, engine)]
        assert 1 <= len(matching) <= 2, (language, engine)


def test_repo_fewshot_evidence_is_verbatim_in_line_range() -> None:
    # Loader bunu zaten doğruluyor; burada açıkça tekrar: örnekler kanıt biçimini öğretir.
    for example in load_fewshots(REPO_FEWSHOTS):
        lines = split_lines(example.code)
        for finding in example.analysis.additional_findings:
            end = finding.line_end or finding.line_start
            window = "\n".join(lines[finding.line_start - 1 : end])
            assert finding.evidence in window, example.id
            assert not finding.evidence.lower().startswith("line"), example.id


def test_repo_fewshots_do_not_repeat_static_findings() -> None:
    for example in load_fewshots(REPO_FEWSHOTS):
        static = {(f.line, f.evidence) for f in example.static_findings}
        for finding in example.analysis.additional_findings:
            assert (finding.line_start, finding.evidence) not in static, example.id


def test_at_least_one_repo_fewshot_shows_static_findings() -> None:
    assert any(e.static_findings for e in load_fewshots(REPO_FEWSHOTS))


def test_valid_file_loads(tmp_path: Path) -> None:
    (example,) = load_fewshots(_write(tmp_path, VALID))
    assert example.id == "c-ornek"
    assert example.analysis.additional_findings[0].evidence == "i <= n"


def test_evidence_not_on_line_rejected(tmp_path: Path) -> None:
    bad = VALID.replace("line_start: 3", "line_start: 2")
    with pytest.raises(FewShotError, match="kanıt"):
        load_fewshots(_write(tmp_path, bad))


def test_prefixed_evidence_rejected(tmp_path: Path) -> None:
    bad = VALID.replace('evidence: "i <= n"', 'evidence: "Line 3: i <= n"')
    with pytest.raises(FewShotError, match="kanıt"):
        load_fewshots(_write(tmp_path, bad))


def test_static_finding_evidence_checked(tmp_path: Path) -> None:
    bad = VALID.replace(
        "static_findings: []",
        'static_findings:\n  - {rule_id: C-X-001, line: 1, evidence: "free(a)", description: "x"}',
    )
    with pytest.raises(FewShotError, match="kanıt"):
        load_fewshots(_write(tmp_path, bad))


def test_schema_error_is_turkish(tmp_path: Path) -> None:
    bad = VALID.replace("severity: high", "severity: kritik")
    with pytest.raises(FewShotError, match="geçersiz değer"):
        load_fewshots(_write(tmp_path, bad))


def test_duplicate_id_rejected(tmp_path: Path) -> None:
    _write(tmp_path, VALID, "a.yaml")
    _write(tmp_path, VALID, "b.yaml")
    with pytest.raises(FewShotError, match="c-ornek"):
        load_fewshots(tmp_path)


def test_select_prefers_exact_combo_then_same_language() -> None:
    examples = load_fewshots(REPO_FEWSHOTS)
    unity = select_fewshots(examples, Language.CSHARP, Engine.UNITY, limit=2)
    assert unity
    assert unity[0].engine == Engine.UNITY
    assert all(e.language == Language.CSHARP for e in unity)
    assert len(select_fewshots(examples, Language.C, Engine.NONE, limit=1)) == 1
    assert select_fewshots(examples, Language.C, Engine.NONE, limit=0) == []


def test_select_is_deterministic() -> None:
    examples = load_fewshots(REPO_FEWSHOTS)
    first = select_fewshots(examples, Language.CPP, Engine.UNREAL, limit=2)
    assert first == select_fewshots(list(reversed(examples)), Language.CPP, Engine.UNREAL, 2)


def test_view_numbers_code_and_serializes_json(tmp_path: Path) -> None:
    (example,) = load_fewshots(_write(tmp_path, VALID))
    view = fewshot_view(example)
    assert view.numbered_code.splitlines()[2].startswith("3 |")
    assert '"evidence": "i <= n"' in view.analysis_json
    assert "Sınır dışı erişim" in view.socratic_json  # ensure_ascii kapalı


def test_repo_fewshots_match_static_engine() -> None:
    """Örnekteki "statik analizin zaten bulduğu" listesi ve ipucu gerçek motorla aynı olmalı;
    yoksa örnek, statik bulguyu tekrar etmeyi (ya da uydurmayı) öğretir."""
    for example in load_fewshots(REPO_FEWSHOTS):
        code = normalize(
            example.code, LanguageHint(language=example.language, engine=example.engine)
        )
        facts = extract_facts(code)
        actual = {
            (f.rule_id, f.line_start, f.evidence)
            for f in run_rules(code, facts, disabled=[]).findings
        }
        shown = {(f.rule_id, f.line, f.evidence) for f in example.static_findings}
        assert shown == actual, example.id
        assert example.static_hint == f"O({compute_hint(facts).value})", example.id


def test_same_line_as_static_finding_rejected(tmp_path: Path) -> None:
    """Denetim D6: statik bulgunun satırına farklı alt dizeyle yeni bulgu da tekrardır."""
    bad = VALID.replace(
        "static_findings: []",
        'static_findings:\n  - {rule_id: C-X-001, line: 3, evidence: "s += a[i]", description: x}',
    )
    with pytest.raises(FewShotError, match="tekrar"):
        load_fewshots(_write(tmp_path, bad))


def test_repo_fewshot_complexities_parse() -> None:
    """Örnek karmaşıklıklar Faz 9 normalizasyonundan geçebilmeli (ek ya da uydurma biçim yok)."""
    for example in load_fewshots(REPO_FEWSHOTS):
        c = example.analysis.complexity
        for value in (c.time_complexity, c.space_complexity, c.optimal_time_target):
            if value is not None:
                parse_bigo(value)


def test_repo_fewshot_questions_are_level_one() -> None:
    """Denetim O6: örnek sorular satır numarası vermez (seviye 1 üslubu); aksi halde küçük
    modeller seviye 1 talimatı yerine örneği taklit eder."""
    for example in load_fewshots(REPO_FEWSHOTS):
        texts = [*example.socratic.guiding_questions, example.socratic.next_step_hint or ""]
        for text in texts:
            assert not LINE_REFERENCE.search(text), (example.id, text)
        assert all(q.rstrip().endswith("?") for q in example.socratic.guiding_questions)
