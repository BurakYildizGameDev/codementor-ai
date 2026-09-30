"""Prompt testlerinin ortak girdileri (Unity radar örneği, soru, bulgu, ayarlar)."""

from __future__ import annotations

from pathlib import Path

from codementor.config import Settings, load_settings
from codementor.ingest.normalize import normalize
from codementor.models.enums import (
    AuditCategory,
    Difficulty,
    Engine,
    FindingSource,
    Language,
    LoopBound,
    Severity,
)
from codementor.models.facts import CodeFacts, ComplexityHint, LoopFact
from codementor.models.findings import Finding
from codementor.models.llm_output import LLMComplexity
from codementor.models.prompts import AnalysisPromptInput, QuestionContext, SocraticPromptInput
from codementor.models.provider import ChatMessage
from codementor.models.questions import ChecklistItem, ExpectedComplexity, Question
from codementor.models.request import LanguageHint, NormalizedCode

REPO_PROMPTS = Path(__file__).resolve().parents[2] / "prompts" / "v1"

CODE = """\
using UnityEngine;
public class Radar : MonoBehaviour {
    List<Enemy> enemies = new List<Enemy>();
    void Update() {
        foreach (var e in enemies) {
            var hits = new List<Enemy>();
            if (enemies.Contains(e)) hits.Add(e);
        }
    }
}
"""

SOLUTION_PATH = "private/solutions/unity-hard-radar.cs"
SOLUTION_MARKER = "private readonly HashSet<Enemy> gizliCozumKumesi_7f3a;"


def prompt_settings(prompts_dir: Path = REPO_PROMPTS, **extra: object) -> Settings:
    return load_settings(prompts={"dir": prompts_dir, **extra})


def unity_code(text: str = CODE) -> NormalizedCode:
    return normalize(text, LanguageHint(language=Language.CSHARP, engine=Engine.UNITY))


def make_question(tmp_path: Path, difficulty: Difficulty = Difficulty.HARD) -> Question:
    solution = tmp_path / SOLUTION_PATH
    solution.parent.mkdir(parents=True, exist_ok=True)
    solution.write_text(f"class Cozum {{\n    {SOLUTION_MARKER}\n}}\n", encoding="utf-8")
    return Question(
        id="unity-hard-radar",
        version=1,
        language=Language.CSHARP,
        engine=Engine.UNITY,
        difficulty=difficulty,
        title="Radar",
        prompt="Yakındaki düşmanları bulan bir radar yazın.",
        constraints=["Kare başına tahsis olmamalı"],
        expected=ExpectedComplexity(time={"update": "n"}, space="n"),
        concept_tags=["gc", "hot-path"],
        checklist_extra=["Liste her karede yeniden mi oluşturuluyor?"],
        hint_ladder={1: "Update ne sıklıkla çalışır?", 2: "6. satır", 3: "GC baskısı"},
        reference_solution_path=SOLUTION_PATH,
    )


def static_finding(line: int = 6, evidence: str = "new List<Enemy>()") -> Finding:
    return Finding(
        id="F-001",
        rule_id="UNITY-GC-001",
        category=AuditCategory.GARBAGE_COLLECTION,
        severity=Severity.HIGH,
        line_start=line,
        line_end=None,
        evidence=evidence,
        description="Update içinde her karede yeni liste oluşturuluyor mu?",
        source=FindingSource.STATIC,
        confidence=0.9,
    )


def analysis_input(tmp_path: Path, **overrides: object) -> AnalysisPromptInput:
    data: dict[str, object] = {
        "code": unity_code(),
        "question": QuestionContext.from_question(make_question(tmp_path)),
        "facts": CodeFacts(
            loops=[LoopFact(kind="foreach", line=5, depth=1, bound=LoopBound.LINEAR)]
        ),
        "hint": ComplexityHint(value="n^2", confidence="medium", basis=["5. satır × Contains"]),
        "static_findings": [static_finding()],
        "checklist": [
            ChecklistItem(id="UNITY-GC-001", text="Update içinde tahsis var mı?", tags=["core"])
        ],
    }
    data.update(overrides)
    return AnalysisPromptInput.model_validate(data)


def system_text(messages: list[ChatMessage]) -> str:
    return next(m.content for m in messages if m.role == "system")


def user_text(messages: list[ChatMessage]) -> str:
    return next(m.content for m in reversed(messages) if m.role == "user")


def socratic_input(tmp_path: Path, attempt: int = 1, **q: object) -> SocraticPromptInput:
    return SocraticPromptInput(
        code=unity_code(),
        question=QuestionContext.from_question(make_question(tmp_path, **q)),  # type: ignore[arg-type]
        findings=[static_finding()],
        complexity=LLMComplexity(
            reasoning_steps=["foreach n kez", "Contains n"],
            time_complexity="O(n^2)",
            space_complexity="O(n)",
            optimal_time_target="O(n)",
            agreement="agrees",
        ),
        attempt=attempt,
    )
