// ../schemas/*.schema.json → src/types/*.ts. Tipler elle yazılmaz (Faz 13 kabul kriteri);
// şemalar Python modellerinden `make schema` ile üretilir.
import { readdir, readFile, writeFile } from "node:fs/promises";
import { basename, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { compile } from "json-schema-to-typescript";

const here = dirname(fileURLToPath(import.meta.url));
const schemaDir = join(here, "..", "..", "schemas");
const outDir = join(here, "..", "src", "types");
const UI_SCHEMAS = [
  "report",
  "request",
  "stage_event",
  "question_public",
  "problem",
  "provider_status",
];
const BANNER =
  "/* OTOMATİK ÜRETİLDİ — elle düzenlemeyin.\n" +
  " * Kaynak: schemas/{name}.schema.json (Python modelleri). Yeniden üretmek için:\n" +
  " * `make schema` ardından `npm run gen:types`. */";

const available = new Set((await readdir(schemaDir)).map((f) => basename(f, ".schema.json")));
for (const name of UI_SCHEMAS) {
  if (!available.has(name)) throw new Error(`şema yok: ${name}.schema.json`);
  const schema = JSON.parse(await readFile(join(schemaDir, `${name}.schema.json`), "utf-8"));
  const ts = await compile(schema, schema.title, {
    bannerComment: BANNER.replace("{name}", name),
    additionalProperties: false,
    style: { singleQuote: false },
  });
  await writeFile(join(outDir, `${name}.ts`), ts.replace(/\r\n/g, "\n"), "utf-8");
}
console.log(`${UI_SCHEMAS.length} tip dosyası üretildi → src/types/`);
