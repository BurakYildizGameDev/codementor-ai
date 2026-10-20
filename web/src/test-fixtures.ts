// Testlerde kullanılan örnek veriler; tipler şemadan üretilmiş dosyalardan gelir.
import type { QuestionPublic } from "./types/question_public";
import type { AnalysisReport, Finding } from "./types/report";
import type { StageEvent } from "./types/stage_event";

export function finding(overrides: Partial<Finding> = {}): Finding {
  return {
    id: "F-001",
    rule_id: "C-MEM-001",
    category: "resource_leak",
    severity: "high",
    line_start: 4,
    line_end: null,
    evidence: "int *tmp = malloc(n * sizeof(int));",
    description: "Ayrılan bellek kimde kalıyor?",
    source: "static",
    confidence: 0.9,
    ...overrides,
  };
}

export function report(overrides: Partial<AnalysisReport> = {}): AnalysisReport {
  return {
    schema_version: "1.0",
    analysis_id: "01TEST",
    created_at: "2026-09-30T20:00:00Z",
    language: "c",
    engine: "none",
    question_id: null,
    difficulty: null,
    compilation: { status: "skipped", diagnostics: [] },
    complexity: {
      time_complexity: "n",
      space_complexity: "n",
      display_time: "O(n)",
      reasoning_steps: ["6. satırdaki döngü n kez döner."],
      is_optimal: null,
      optimal_time_target: null,
      static_hint: "n",
      agreement: "agrees",
      confidence: 0.9,
    },
    findings: [finding()],
    socratic: {
      key_flaw_concept: "bellek sahipliği",
      hint_level: 1,
      guiding_questions: ["Fonksiyon bittiğinde tmp nereye gidiyor?"],
      next_step_hint: null,
      leak_check: "passed",
    },
    meta: {
      provider: "claude_cli",
      model: "claude-opus-5-5",
      prompt_version: "v1",
      rules_version: "r1",
      schema_version: "1.0",
      tokens_in: 100,
      tokens_out: 50,
      stage_latency_ms: {},
      early_exit: false,
      cache_hit: false,
      degraded: false,
      repair_attempts: 0,
      warnings: [],
    },
    ...overrides,
  };
}

export function stage(
  name: StageEvent["stage"],
  status: StageEvent["status"],
  duration_ms = 0,
): StageEvent {
  return { analysis_id: "01TEST", stage: name, status, duration_ms, tokens: 0 };
}

export const QUESTIONS: QuestionPublic[] = [
  {
    id: "c-easy-sum",
    version: 1,
    language: "c",
    engine: "none",
    difficulty: "easy",
    title: "Dizi toplamı",
    prompt: "Bir dizinin toplamını hesapla.",
    constraints: ["n ≤ 10^5"],
    expected: { time: { sum: "n" }, space: "1" },
    sample_io: [{ input: "3\n1 2 3", output: "6", explanation: "1 + 2 + 3" }],
  },
];

/** SSE gövdesi: verilen olayları parçalara bölerek akıtan bir Response. */
export function sseResponse(events: [string, unknown][], chunkSize = 7): Response {
  const text = events.map(([e, d]) => `event: ${e}\ndata: ${JSON.stringify(d)}\n\n`).join("");
  const bytes = new TextEncoder().encode(text);
  const stream = new ReadableStream<Uint8Array>({
    start(controller) {
      for (let i = 0; i < bytes.length; i += chunkSize) {
        controller.enqueue(bytes.slice(i, i + chunkSize));
      }
      controller.close();
    },
  });
  return new Response(stream, { status: 200, headers: { "Content-Type": "text/event-stream" } });
}
