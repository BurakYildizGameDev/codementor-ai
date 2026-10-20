"""Prompt anlık görüntüleri: sabit girdiden üretilen prompt metni (Faz 8).

Vaka: `tests/golden/prompts/{id}/code.*`; `{id}` soru bankasında varsa soru bağlamıyla,
`free-<dil>` ise serbest modda kurulur. Güncellemek için:
`uv run pytest tests/golden/prompts --update-golden` (farkı gözle incele!).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from codementor.config import CONFIG_FILE_ENV, Settings, load_settings
from codementor.models.enums import Engine, Language
from codementor.models.llm_output import LLMComplexity
from codementor.models.prompts import AnalysisPromptInput, BuiltPrompt, SocraticPromptInput
from codementor.prompts._demo import GOLDEN_DIR, demo_input, sample_input
from codementor.prompts.builder import (
    build_analysis_messages,
    build_single_pass_messages,
    build_socratic_messages,
)
from codementor.questions.bank import QuestionBank

REPO = Path(__file__).resolve().parents[3]
ROOT = Path(__file__).parent
CASES = sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith("__"))
FREE_LANGUAGES = {"c": Language.C, "cpp": Language.CPP, "csharp": Language.CSHARP}
MODES = ("analysis", "single_pass", "socratic")


def _verified_complexity(inp: AnalysisPromptInput) -> LLMComplexity:
    """Geçiş B'nin girdisi normalde K5'ten gelir; anlık görüntü için statik ipucundan kurulur."""
    value = f"O({inp.hint.value})" if inp.hint else "O(n)"
    return LLMComplexity(
        reasoning_steps=[f"Statik ipucuyla uyumlu: {value}."],
        time_complexity=value,
        space_complexity="O(n)",
        optimal_time_target=None,
        agreement="agrees",
    )


@pytest.fixture
def settings(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Settings:
    """Depodaki `codementor.toml`'dan bağımsız, sabit ayarlar."""
    monkeypatch.setenv(CONFIG_FILE_ENV, str(tmp_path / "yok.toml"))
    return load_settings(
        data={
            "questions_dir": REPO / "data" / "questions",
            "checklists_dir": REPO / "data" / "checklists",
            "call_costs_file": REPO / "data" / "call_costs.yaml",
        },
        prompts={"dir": REPO / "prompts" / "v1"},
        rules={"disabled": []},
        providers={"default": "claude_cli"},
    )


def _input(case: Path, settings: Settings) -> AnalysisPromptInput:
    (source,) = case.glob("code.*")
    if case.name.startswith("free-"):
        language = FREE_LANGUAGES[case.name.removeprefix("free-")]
        return sample_input(source.read_bytes(), language, Engine.NONE, None, settings)
    question = QuestionBank.load(settings.data.questions_dir).get(case.name)
    return sample_input(source.read_bytes(), question.language, question.engine, question, settings)


def _build(mode: str, inp: AnalysisPromptInput, settings: Settings) -> BuiltPrompt:
    if mode == "analysis":
        return build_analysis_messages(inp, settings=settings)
    if mode == "single_pass":
        return build_single_pass_messages(inp, settings=settings)
    socratic = SocraticPromptInput(
        code=inp.code,
        question=inp.question,
        findings=inp.static_findings,
        complexity=_verified_complexity(inp),
    )
    return build_socratic_messages(socratic, settings=settings)


def _snapshot(built: BuiltPrompt) -> str:
    return "\n\n".join(f"===== {m.role} =====\n{m.content}" for m in built.messages) + "\n"


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("case", CASES, ids=[c.name for c in CASES])
def test_prompt_snapshot(case: Path, mode: str, settings: Settings, update_golden: bool) -> None:
    built = _build(mode, _input(case, settings), settings)
    assert built.trimmed == []  # varsayılan bütçede hiçbir bölüm kırpılmamalı
    actual = _snapshot(built)
    expected_path = case / f"expected_{mode}.txt"
    if update_golden:
        expected_path.write_text(actual, encoding="utf-8", newline="\n")
    assert expected_path.exists(), f"{expected_path} yok; --update-golden ile üretin"
    assert actual == expected_path.read_text(encoding="utf-8")


def test_cases_exist() -> None:
    names = {c.name for c in CASES}
    assert {"unity-hard-inventory", "c-medium-linked-list", "free-cpp"} <= names


def test_demo_golden_dir_independent_of_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Sonraya #33: demo örnek kodu çalışma dizininden bağımsız depo kökünden bulur."""
    assert GOLDEN_DIR == ROOT
    monkeypatch.chdir(tmp_path)
    inp = demo_input(CASES[0].name)
    assert inp.code.text
