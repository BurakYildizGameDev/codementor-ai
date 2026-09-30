/* OTOMATİK ÜRETİLDİ — elle düzenlemeyin.
 * Kaynak: schemas/stage_event.schema.json (Python modelleri). Yeniden üretmek için:
 * `make schema` ardından `npm run gen:types`. */

export type AnalysisId = string;
export type Detail = string | null;
export type DurationMs = number;
export type Stage =
  | "cache"
  | "ingest"
  | "tier0"
  | "tier1"
  | "facts"
  | "rules"
  | "prompt_a"
  | "llm_a"
  | "verify_a"
  | "prompt_b"
  | "llm_b"
  | "verify_b"
  | "report";
export type Status = "started" | "completed" | "skipped" | "failed";
export type Tokens = number;

/**
 * Bir aşamanın durumu (CLI ilerleme göstergesi, Web UI SSE).
 */
export interface StageEvent {
  analysis_id: AnalysisId;
  detail?: Detail;
  duration_ms?: DurationMs;
  stage: Stage;
  status: Status;
  tokens?: Tokens;
}
