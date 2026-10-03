/** SSE `stage` olaylarından aşama ilerleme listesi (Web UI ilerleme göstergesi). */
import type { StageEvent } from "../types/stage_event";

export interface StageState {
  stage: StageEvent["stage"];
  status: StageEvent["status"];
  duration_ms: number;
}

export const initialProgress: StageState[] = [];

/** Olayı listeye işler: yeni aşama sona eklenir, bilinen aşamanın durumu güncellenir. */
export function progressReducer(state: StageState[], event: StageEvent): StageState[] {
  const next: StageState = {
    stage: event.stage,
    status: event.status,
    duration_ms: event.duration_ms ?? 0,
  };
  const index = state.findIndex((s) => s.stage === event.stage);
  if (index === -1) return [...state, next];
  return state.map((s, i) => (i === index ? next : s));
}

export function totalDuration(state: StageState[]): number {
  return state.reduce((sum, s) => sum + s.duration_ms, 0);
}

/** Kullanıcıya gösterilen aşama adları. */
export const STAGE_LABELS: Record<StageEvent["stage"], string> = {
  cache: "Önbellek",
  ingest: "Giriş",
  tier0: "Sözdizimi",
  tier1: "Derleyici",
  facts: "Olgular",
  rules: "Kurallar",
  prompt_a: "Prompt A",
  llm_a: "LLM analiz",
  verify_a: "Doğrulama A",
  prompt_v: "Prompt V",
  llm_v: "LLM bulgu doğrulama",
  verify_v: "Doğrulama V",
  prompt_b: "Prompt B",
  llm_b: "LLM mentorluk",
  verify_b: "Doğrulama B",
  report: "Rapor",
};
