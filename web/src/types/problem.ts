/* OTOMATİK ÜRETİLDİ — elle düzenlemeyin.
 * Kaynak: schemas/problem.schema.json (Python modelleri). Yeniden üretmek için:
 * `make schema` ardından `npm run gen:types`. */

export type Detail = string | null;
/**
 * Doğrulama hataları (422)
 */
export type Errors = string[] | null;
/**
 * İsteğin yolu
 */
export type Instance = string | null;
export type Status = number;
export type Title = string;
/**
 * Sorun türü URI'si
 */
export type Type = string;

/**
 * RFC 7807 `application/problem+json` gövdesi.
 */
export interface Problem {
  detail?: Detail;
  errors?: Errors;
  instance?: Instance;
  status: Status;
  title: Title;
  type?: Type;
}
