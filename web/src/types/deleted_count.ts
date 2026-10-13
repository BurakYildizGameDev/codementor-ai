/* OTOMATİK ÜRETİLDİ — elle düzenlemeyin.
 * Kaynak: schemas/deleted_count.schema.json (Python modelleri). Yeniden üretmek için:
 * `make schema` ardından `npm run gen:types`. */

export type Deleted = number;

/**
 * Silinen kayıt sayısı yanıtı (Faz E).
 */
export interface DeletedCount {
  deleted: Deleted;
}
