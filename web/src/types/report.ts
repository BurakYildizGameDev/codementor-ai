/* OTOMATİK ÜRETİLDİ — elle düzenlemeyin.
 * Kaynak: schemas/report.schema.json (Python modelleri). Yeniden üretmek için:
 * `make schema` ardından `npm run gen:types`. */

/**
 * ULID (Crockford base32, 26 karakter)
 */
export type AnalysisId = string;
export type Column = number | null;
export type Line = number;
export type Message = string;
export type Severity = "error" | "warning" | "note";
export type Tool = "tree-sitter" | "gcc" | "clang" | "roslyn" | "python";
export type Diagnostics = Diagnostic[];
export type CompilationStatus = "passed" | "warning" | "failed" | "skipped";
export type Agreement = "agrees" | "conflicts" | "no_hint";
export type Confidence = number;
/**
 * Gösterim, ör. "O(n²)"
 */
export type DisplayTime = string;
/**
 * Soru bağlamı yoksa null
 */
export type IsOptimal = boolean | null;
export type OptimalTimeTarget = string | null;
export type ReasoningSteps = string[];
export type SpaceComplexity = string;
export type StaticHint = string | null;
/**
 * Kanonik Big-O, ör. "n^2"
 */
export type TimeComplexity = string;
export type CreatedAt = string;
export type Difficulty = "very_easy" | "easy" | "medium" | "hard";
export type Engine = "none" | "unity" | "unreal";
export type AuditCategory =
  | "memory_safety"
  | "resource_leak"
  | "undefined_behavior"
  | "garbage_collection"
  | "performance"
  | "engine_best_practice"
  | "edge_case"
  | "input_handling"
  | "design"
  | "accessibility"
  | "maintainability";
export type Confidence1 = number;
export type Description = string;
export type Evidence = string;
/**
 * Rapor içi kimlik, ör. "F-001"
 */
export type Id = string;
/**
 * issue: gerçek hata; suggestion: hataya yol açmayan öneri (yalnız low)
 */
export type FindingKind = "issue" | "suggestion";
export type LineEnd = number | null;
export type LineStart = number;
/**
 * Statik kural kimliği, ör. "UNITY-GC-001"
 */
export type RuleId = string | null;
export type Severity1 = "high" | "medium" | "low";
export type FindingSource = "static" | "llm" | "confirmed";
export type Findings = Finding[];
export type Language = "c" | "cpp" | "csharp" | "python" | "html" | "css";
export type CacheHit = boolean;
/**
 * Tahmini maliyet (USD, data/pricing.yaml); fiyat yoksa null
 */
export type CostEst = number | null;
export type Degraded = boolean;
export type EarlyExit = boolean;
export type Model = string | null;
export type PromptVersion = string;
export type Provider = string | null;
export type RepairAttempts = number;
export type RulesVersion = string;
export type SchemaVersion = string;
export type Input = number;
export type Output = number;
export type TokensIn = number;
export type TokensOut = number;
/**
 * Sağlayıcı token bildirmedi; sayılar yaklaşık
 */
export type UsageEstimated = boolean;
export type Warnings = string[];
export type QuestionId = string | null;
export type SchemaVersion1 = "1.0" | "1.1";
export type GuidingQuestions = string[];
export type HintLevel = number;
export type KeyFlawConcept = string;
export type LeakCheck = "passed" | "regenerated" | "dropped_questions" | "skipped";
export type NextStepHint = string | null;

/**
 * Bir analizin tam sonucu.
 */
export interface AnalysisReport {
  analysis_id: AnalysisId;
  compilation: CompilationBlock;
  complexity: ComplexityResult | null;
  created_at: CreatedAt;
  difficulty: Difficulty | null;
  engine: Engine;
  findings: Findings;
  language: Language;
  meta: ReportMeta;
  question_id: QuestionId;
  schema_version?: SchemaVersion1;
  socratic: SocraticResult | null;
}
/**
 * Ön doğrulama sonucu: durum + tanılar.
 */
export interface CompilationBlock {
  diagnostics: Diagnostics;
  status: CompilationStatus;
}
/**
 * Ayrıştırıcı/derleyici tanısı (K1).
 */
export interface Diagnostic {
  column: Column;
  line: Line;
  message: Message;
  severity: Severity;
  tool: Tool;
}
export interface ComplexityResult {
  agreement: Agreement;
  confidence: Confidence;
  display_time: DisplayTime;
  is_optimal: IsOptimal;
  optimal_time_target: OptimalTimeTarget;
  reasoning_steps: ReasoningSteps;
  space_complexity: SpaceComplexity;
  static_hint: StaticHint;
  time_complexity: TimeComplexity;
}
/**
 * Rapordaki tek bulgu; statik kural, LLM ya da ikisinin birleşimi.
 */
export interface Finding {
  category: AuditCategory;
  confidence: Confidence1;
  description: Description;
  evidence: Evidence;
  id: Id;
  kind?: FindingKind;
  line_end: LineEnd;
  line_start: LineStart;
  rule_id: RuleId;
  severity: Severity1;
  source: FindingSource;
}
export interface ReportMeta {
  cache_hit: CacheHit;
  cost_est?: CostEst;
  degraded: Degraded;
  early_exit: EarlyExit;
  model: Model;
  prompt_version: PromptVersion;
  provider: Provider;
  repair_attempts: RepairAttempts;
  rules_version: RulesVersion;
  schema_version: SchemaVersion;
  stage_latency_ms: StageLatencyMs;
  stage_tokens?: StageTokens;
  tokens_in: TokensIn;
  tokens_out: TokensOut;
  usage_estimated?: UsageEstimated;
  warnings: Warnings;
}
export interface StageLatencyMs {
  [k: string]: number;
}
/**
 * LLM aşaması → giriş/çıkış token
 */
export interface StageTokens {
  [k: string]: TokenSplit;
}
/**
 * Bir LLM aşamasının token kullanımı (Faz K).
 */
export interface TokenSplit {
  input: Input;
  output: Output;
}
export interface SocraticResult {
  guiding_questions: GuidingQuestions;
  hint_level: HintLevel;
  key_flaw_concept: KeyFlawConcept;
  leak_check: LeakCheck;
  next_step_hint: NextStepHint;
}
