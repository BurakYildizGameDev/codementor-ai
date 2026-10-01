/* OTOMATİK ÜRETİLDİ — elle düzenlemeyin.
 * Kaynak: schemas/provider_status.schema.json (Python modelleri). Yeniden üretmek için:
 * `make schema` ardından `npm run gen:types`. */

export type Detail = string;
export type Model = string;
export type Name = string;
export type Ready = boolean;

/**
 * `codementor providers check` satırı.
 */
export interface ProviderStatus {
  detail: Detail;
  model: Model;
  name: Name;
  ready: Ready;
}
