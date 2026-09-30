/* OTOMATİK ÜRETİLDİ — elle düzenlemeyin.
 * Kaynak: schemas/question_public.schema.json (Python modelleri). Yeniden üretmek için:
 * `make schema` ardından `npm run gen:types`. */

/**
 * @minItems 1
 */
export type Constraints = [string, ...string[]];
export type Difficulty = "very_easy" | "easy" | "medium" | "hard";
export type Engine = "none" | "unity" | "unreal";
export type Space = string;
export type Id = string;
export type Language = "c" | "cpp" | "csharp";
export type Prompt = string;
export type Title = string;
export type Version = number;

/**
 * Öğrenciye (API, CLI) verilen soru: yalnızca problem tanımı.
 *
 * Referans çözüm (mimari §12) ve mentorluk verisi (`MENTOR_FIELDS`: kavram
 * etiketleri, soruya özgü kontrol maddeleri, ipucu merdiveni) içermez; ipuçları
 * analiz sırasında kademeli açılır.
 */
export interface QuestionPublic {
  constraints: Constraints;
  difficulty: Difficulty;
  engine: Engine;
  expected: ExpectedComplexity;
  id: Id;
  language: Language;
  prompt: Prompt;
  title: Title;
  version: Version;
}
/**
 * Sorunun beklenen karmaşıklığı; işlem adı → Big-O.
 */
export interface ExpectedComplexity {
  space: Space;
  time: Time;
}
export interface Time {
  [k: string]: string;
}
