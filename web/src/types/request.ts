/* OTOMATİK ÜRETİLDİ — elle düzenlemeyin.
 * Kaynak: schemas/request.schema.json (Python modelleri). Yeniden üretmek için:
 * `make schema` ardından `npm run gen:types`. */

export type Code = string;
export type Engine = "none" | "unity" | "unreal";
export type Language = "c" | "cpp" | "csharp" | "python" | "html" | "css";
/**
 * Pipeline çağrı modu (mimari §5.4, §17 `pipeline.mode`).
 */
export type PipelineMode = "two_pass" | "single_pass";
export type Tier1 = boolean | null;
export type UseCache = boolean | null;
export type Provider = string | null;
export type QuestionId = string | null;
export type SessionId = string | null;

/**
 * Analiz isteği. Kullanıcı kodu güvenilmeyen veridir (mimari §12).
 */
export interface AnalysisRequest {
  code: Code;
  /**
   * Boşsa sezgisel tespit
   */
  engine?: Engine | null;
  /**
   * Boşsa sezgisel tespit
   */
  language?: Language | null;
  options?: AnalysisOptions;
  provider?: Provider;
  question_id?: QuestionId;
  session_id?: SessionId;
}
/**
 * İstek başına seçenekler; `None` → yapılandırmadaki değer kullanılır.
 */
export interface AnalysisOptions {
  mode?: PipelineMode | null;
  tier1?: Tier1;
  use_cache?: UseCache;
}
