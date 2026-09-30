"""`python -m codementor.prompts.builder --demo <soru>`: üretilen prompt'u yazdırır.

Kod `--code` ile verilmezse `tests/golden/prompts/<soru>/code.*` kullanılır. LLM çağrılmaz.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from codementor.analysis.call_costs import load_call_costs
from codementor.analysis.complexity_hint import compute_hint, function_hints
from codementor.analysis.extractor import extract_facts
from codementor.config import Settings, get_settings
from codementor.ingest.normalize import normalize
from codementor.models.enums import Engine, Language
from codementor.models.prompts import AnalysisPromptInput, BuiltPrompt, QuestionContext
from codementor.models.questions import Question
from codementor.models.request import LanguageHint
from codementor.prompts.builder import build_analysis_messages, build_single_pass_messages
from codementor.questions.bank import QuestionBank
from codementor.questions.checklists import Checklists
from codementor.rules.engine import run_rules

GOLDEN_DIR = Path("tests/golden/prompts")


def sample_input(
    raw: bytes,
    language: Language,
    engine: Engine,
    question: Question | None,
    settings: Settings,
) -> AnalysisPromptInput:
    """K0-K2 (normalizasyon, olgular, ipucu, kurallar, kontrol listesi) → prompt girdisi."""
    code = normalize(raw, LanguageHint(language=language, engine=engine), limits=settings.limits)
    facts = extract_facts(code, costs=load_call_costs(settings.data.call_costs_file))
    tags = question.concept_tags if question else []
    return AnalysisPromptInput(
        code=code,
        question=QuestionContext.from_question(question) if question else None,
        facts=facts,
        hint=compute_hint(facts),
        function_hints=list(function_hints(facts).values()),
        static_findings=run_rules(code, facts, disabled=settings.rules.disabled).findings,
        checklist=Checklists.load(settings.data.checklists_dir).select_items(
            code.language, code.engine, tags
        ),
    )


def demo_input(
    question_id: str, code_path: Path | None = None, settings: Settings | None = None
) -> AnalysisPromptInput:
    """Soru bankasındaki sorunun örnek koduyla prompt girdisi kurar."""
    settings = settings or get_settings()
    question = QuestionBank.load(settings.data.questions_dir).get(question_id)
    if code_path is None:
        matches = sorted((GOLDEN_DIR / question_id).glob("code.*"))
        if not matches:
            raise FileNotFoundError(f"Örnek kod bulunamadı: {GOLDEN_DIR / question_id}/code.*")
        code_path = matches[0]
    return sample_input(
        code_path.read_bytes(), question.language, question.engine, question, settings
    )


def format_prompt(built: BuiltPrompt) -> str:
    """Mesajları başlıklarla tek metne çevirir."""
    parts = [
        f"# prompt_version={built.prompt_version} tokens≈{built.estimated_tokens}"
        f"/{built.budget_tokens} trimmed={built.trimmed}"
    ]
    parts += [f"\n===== {m.role} =====\n{m.content}" for m in built.messages]
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    """Komut satırı girişi."""
    parser = argparse.ArgumentParser(prog="python -m codementor.prompts.builder")
    parser.add_argument("--demo", required=True, metavar="SORU_ID")
    parser.add_argument("--code", type=Path, default=None)
    parser.add_argument("--mode", choices=["analysis", "single_pass"], default="analysis")
    args = parser.parse_args(argv)
    inp = demo_input(args.demo, args.code)
    builder = build_analysis_messages if args.mode == "analysis" else build_single_pass_messages
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(format_prompt(builder(inp)))
    return 0
