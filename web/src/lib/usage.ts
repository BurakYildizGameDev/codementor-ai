/** Token ve tahmini maliyet etiketi (Faz 33); CLI/masaüstündeki `usage_label` ile aynı metin. */
import type { AnalysisReport } from "../types/report";

type Meta = AnalysisReport["meta"];

export function usageLabel(meta: Meta): string | null {
  if (!meta.tokens_in && !meta.tokens_out) return null;
  let label = `token ${meta.tokens_in}/${meta.tokens_out}`;
  if (meta.usage_estimated) label += " (tahmini)";
  if (meta.cost_est !== null && meta.cost_est !== undefined) {
    label += ` · ~$${meta.cost_est.toFixed(4)}`;
  }
  return label;
}
