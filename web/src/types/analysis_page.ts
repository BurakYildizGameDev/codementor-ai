/* OTOMATİK ÜRETİLDİ — elle düzenlemeyin.
 * Kaynak: schemas/analysis_page.schema.json (Python modelleri). Yeniden üretmek için:
 * `make schema` ardından `npm run gen:types`. */

export type AnalysisId = string;
export type CreatedAt = string;
export type Degraded = boolean;
export type EarlyExit = boolean;
export type Engine = "none" | "unity" | "unreal";
export type Language = "c" | "cpp" | "csharp" | "python" | "html" | "css";
export type Provider = string | null;
export type QuestionId = string | null;
export type TokensIn = number;
export type TokensOut = number;
export type Items = AnalysisSummary[];
/**
 * Sonraki sayfa için `before` değeri; yoksa null
 */
export type NextCursor = string | null;

export interface AnalysisPage {
  items: Items;
  next_cursor?: NextCursor;
}
/**
 * Geçmiş listesindeki bir satır; rapor gövdesi ve kod içermez.
 */
export interface AnalysisSummary {
  analysis_id: AnalysisId;
  created_at: CreatedAt;
  degraded: Degraded;
  early_exit: EarlyExit;
  engine: Engine;
  language: Language;
  provider: Provider;
  question_id: QuestionId;
  tokens_in: TokensIn;
  tokens_out: TokensOut;
}
