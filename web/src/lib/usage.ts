/** Token ve tahmini maliyet etiketleri (Faz 33, Faz K); CLI/masaüstündeki `report/usage.py` ile
 * aynı metin. */
import type { AnalysisReport } from "../types/report";

type Meta = AnalysisReport["meta"];

const STAGE_NAMES: [string, string][] = [
  ["llm_a", "Analiz"],
  ["llm_v", "Doğrulama"],
  ["llm_b", "Mentor soruları"],
];

/** Binlik ayırıcı nokta: `12.400`. */
export function formatCount(value: number): string {
  return String(value).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

export function usageLabel(meta: Meta): string {
  if (!meta.tokens_in && !meta.tokens_out) {
    let reason = "model çağrılmadı";
    if (meta.cache_hit) reason = "önbellekten";
    else if (meta.early_exit) reason = "derleme hatası; model çağrılmadı";
    else if (meta.degraded) reason = "model yanıt vermedi";
    return `token 0 (${reason})`;
  }
  const total = meta.tokens_in + meta.tokens_out;
  let label =
    `${formatCount(total)} token (giriş ${formatCount(meta.tokens_in)} · ` +
    `çıkış ${formatCount(meta.tokens_out)})`;
  if (meta.usage_estimated) label += " · tahmini";
  if (meta.cost_est !== null && meta.cost_est !== undefined) {
    label += ` · ~$${meta.cost_est.toFixed(4)}`;
  }
  return label;
}

/** Aşama başına `Giriş/çıkış: Analiz 1.200/340 · …`; LLM çağrılmadıysa null. */
export function usageBreakdown(meta: Meta): string | null {
  const stages = meta.stage_tokens ?? {};
  const parts: string[] = [];
  for (const [stage, name] of STAGE_NAMES) {
    const split = stages[stage];
    if (!split || (!split.input && !split.output)) continue;
    parts.push(
      `${name} ${formatCount(split.input)}/${formatCount(split.output)}`,
    );
  }
  // onarım sayısı tüm aşamaların toplamı: bir aşamaya değil sona yazılır
  if (parts.length && meta.repair_attempts)
    parts.push(`${meta.repair_attempts} onarım`);
  return parts.length ? `Giriş/çıkış: ${parts.join(" · ")}` : null;
}
