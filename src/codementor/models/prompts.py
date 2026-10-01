"""Prompt orkestrasyonu (K3, mimari §5.4) veri modelleri."""

from __future__ import annotations

from pydantic import Field

from codementor.models._base import StrictModel
from codementor.models.enums import Difficulty, Engine, Language
from codementor.models.facts import (
    AllocationFact,
    CallFact,
    CodeFacts,
    ComplexityHint,
    FunctionFact,
    LoopFact,
    RecursionFact,
    SymbolRef,
)
from codementor.models.findings import Finding
from codementor.models.llm_output import LLMAnalysisOutput, LLMComplexity, LLMSocraticOutput
from codementor.models.provider import ChatMessage
from codementor.models.questions import ChecklistItem, ExpectedComplexity, Question
from codementor.models.request import NormalizedCode


class QuestionContext(StrictModel):
    """Prompt'a giren soru bilgisi. Referans çözüm yolu bilinçli olarak yok (mimari §12)."""

    id: str
    title: str
    prompt: str
    constraints: list[str]
    difficulty: Difficulty
    expected: ExpectedComplexity | None
    concept_tags: list[str] = Field(default_factory=list)
    checklist_extra: list[str] = Field(default_factory=list)
    hint_ladder: dict[int, str] = Field(default_factory=dict)

    @classmethod
    def from_question(cls, question: Question) -> QuestionContext:
        """Sorudan yalnızca prompt'a girebilecek alanları kopyalar."""
        return cls(
            id=question.id,
            title=question.title,
            prompt=question.prompt,
            constraints=list(question.constraints),
            difficulty=question.difficulty,
            expected=question.expected,
            concept_tags=list(question.concept_tags),
            checklist_extra=list(question.checklist_extra),
            hint_ladder=dict(question.hint_ladder),
        )


class MentoringProfile(StrictModel):
    """Zorluk + deneme sayısından mentorluk ayarı (mimari §5.4.3)."""

    hint_level: int = Field(ge=1, le=3)
    min_questions: int = Field(ge=1, le=4)
    max_questions: int = Field(ge=1, le=4)
    name_concept: bool


class FewShotStaticFinding(StrictModel):
    """Few-shot örneğinde statik analizin zaten bulduğu bulgu."""

    rule_id: str
    line: int = Field(ge=1)
    evidence: str
    description: str


class FewShotExample(StrictModel):
    """`prompts/v1/fewshots/*.yaml`: kısa kod + statik bulgular + örnek doğru çıktı."""

    id: str
    language: Language
    engine: Engine
    title: str
    code: str = Field(min_length=1)
    static_hint: str | None = Field(default=None, description='Statik ipucu, ör. "O(n)"')
    static_findings: list[FewShotStaticFinding] = Field(default_factory=list)
    analysis: LLMAnalysisOutput
    socratic: LLMSocraticOutput


class FewShotView(StrictModel):
    """Şablona verilen few-shot: numaralı kod ve JSON metinleri hazır."""

    title: str
    numbered_code: str
    static_hint: str | None
    static_findings: list[FewShotStaticFinding]
    analysis_json: str
    socratic_json: str


class FactsDigest(StrictModel):
    """`CodeFacts`'in bütçeye göre süzülmüş özeti; şablon bunu okunabilir satırlara çevirir.

    Metin Python'da değil `prompts/v1/_macros.j2` içinde üretilir.
    """

    functions: list[FunctionFact] = Field(default_factory=list)
    loops: list[LoopFact] = Field(default_factory=list)
    recursion: list[RecursionFact] = Field(default_factory=list)
    costly_calls: list[CallFact] = Field(default_factory=list)
    allocations: list[AllocationFact] = Field(default_factory=list)
    unmanaged_uobjects: list[SymbolRef] = Field(
        default_factory=list, description="UPROPERTY olmayan UObject* alanları (Unreal)"
    )
    event_subscriptions: list[SymbolRef] = Field(default_factory=list)
    has_on_disable: bool = False
    omitted: int = Field(default=0, ge=0, description="Yer kalmadığı için atlanan olgu sayısı")

    def is_empty(self) -> bool:
        """Gösterilecek olgu yoksa True."""
        return not (
            self.functions
            or self.loops
            or self.recursion
            or self.costly_calls
            or self.allocations
            or self.unmanaged_uobjects
            or self.event_subscriptions
        )


class AnalysisPromptInput(StrictModel):
    """Geçiş A (ve tek geçiş) girdisi (mimari §5.4.1)."""

    code: NormalizedCode
    question: QuestionContext | None = None
    facts: CodeFacts = Field(default_factory=CodeFacts)
    hint: ComplexityHint | None = None
    function_hints: list[ComplexityHint] = Field(default_factory=list)
    static_findings: list[Finding] = Field(default_factory=list)
    checklist: list[ChecklistItem] = Field(default_factory=list)
    attempt: int = Field(default=1, ge=1, description="Aynı oturumda kaçıncı gönderim")


class SocraticPromptInput(StrictModel):
    """Geçiş B girdisi: yalnızca doğrulanmış analiz soruya dönüşür (mimari §5.4.2)."""

    code: NormalizedCode
    question: QuestionContext | None = None
    findings: list[Finding] = Field(default_factory=list)
    complexity: LLMComplexity | None = None
    attempt: int = Field(default=1, ge=1)


class BuiltPrompt(StrictModel):
    """Oluşturulan mesajlar ve bütçe bilgisi."""

    messages: list[ChatMessage]
    prompt_version: str
    estimated_tokens: int = Field(ge=0)
    budget_tokens: int = Field(ge=0)
    trimmed: list[str] = Field(
        default_factory=list, description="Bütçe için kısaltılan/çıkarılan bölümler, sırayla"
    )
