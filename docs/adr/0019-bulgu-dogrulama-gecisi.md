# ADR-0019: LLM bulguları için doğrulama geçişi

**Tarih:** 2026-10-03 · **Durum:** Kabul edildi (varsayılan kapalı; açma kararı canlı ölçüme bağlı) ·
**Etkilenen bölümler:** mimari §4, §5.4.2, §5.6, §6.3, §11, §17; ADR-0003

## Bağlam

Faz 22B'de prompt kuralları C ailesinde F1'i 48'den 75'e çıkardı. Ama precision'ın kalan açığı
tek prompt'la kapanmıyor: model "olabilir" türünden bulgular yazıyor ve K5 bunları yalnızca
kanıt satırı kodda var mı diye denetliyor. Rapordaki bulgu `confidence` değeri de modelden
gelmiyordu. Sistem kanıt eşleşmesine göre sabit 0,7 / 0,6 veriyordu, yani doğru ve yanlış
bulguları ayırt etmiyordu (Faz 22B ölçümü).

## Karar

1. Geçiş A ile Sokratik geçiş arasına isteğe bağlı bir **doğrulama geçişi** eklenir
   (`prompt_v` → `llm_v` → `verify_v`, şema `LLMVerifyOutput`, şablon `prompts/v1/verify.*.j2`).
   Yalnızca kaynağı `llm` olan bulgular girer. Statik ve `confirmed` bulgular deterministiktir,
   doğrulanmaz. Doğrulanacak LLM bulgusu yoksa çağrı yapılmaz.
2. Model her bulgu için `proven` / `unproven` kararı verir. `proven` için ya somut bir girdi
   (`input`, `expected`, `actual`) ya da sorudan ihlal edilen gereksinim (`requirement`)
   göstermek **zorundadır**. Bunu sistem denetler: alanları boş bir `proven` de düşer.
   Kararlar ve gerekçeler `AnalysisVerification.finding_checks`'te tutulur. Öğrenciye
   gösterilmezler ve gerekçeler yine de sızıntı korumasından geçer (§12).
3. **Güvenli geri dönüş:** Sağlayıcı ya da bütçe hatası olursa, ya da şema onarımdan sonra da
   bozuksa bulgular olduğu gibi kalır ve uyarı yazılır. Model bir bulgu için karar vermediyse
   bulgu korunur (bilgi kaybı yok).
4. `single_pass` modunda doğrulama bir bulguyu düşürürse tek çağrının Sokratik çıktısı atılır,
   ayrı bir Geçiş B üretilir (sorular düşen bulguya dayanıyor olabilir). Hiçbir bulgu düşmezse
   ilk çıktı aynen kullanılır.
5. Modelin kendi güveni `LLMFinding.certainty` (`high` / `medium` / `low`, isteğe bağlı) olarak
   şemaya eklenir. Alan adı `confidence` değildir, çünkü o rapor şemasında sistem alanıdır
   (ADR-0004). Rapordaki bulgu güveni: high 0,85, medium 0,7, low 0,5. Satır düzeltildiyse bu
   değerden 0,1 düşülür. Beyan yoksa eski 0,7 / 0,6 kalır.
6. `pipeline.verify_findings` ile açılır; varsayılan Faz 35B ölçümüyle `true` (aşağıda). Önbellek anahtarına pipeline
   imzası (mod + doğrulama) eklenir. Mod daha önce anahtarda yoktu ve bu bir açıktı.
7. Ölçüm araçları: `eval run --ablate verify` doğrulamalı koşu yapar. `eval analyze`,
   LLM bulgularını güven eşiğine (0,5 / 0,6 / 0,7 / 0,85) göre süzerek precision/recall tablosu
   üretir.

## Sonuçlar

- (+) Precision'ı prompt'tan bağımsız, açıklanabilir bir adımla artırma imkânı. Kararın
  gerekçesi kayıtlıdır.
- (+) `certainty` ile güven eşiği uygulanabilir. Eşik kararı ölçümle verilir.
- (−) LLM bulgusu olan her analizde bir çağrı daha yapılır: gecikme ve token artar. Bu yüzden
  varsayılan kapalıdır.
- (−) Doğrulayıcı da bir LLM'dir. Gerçek bulguları da düşürebilir (recall kaybı). Bunun
  ölçülmesi gerekir.

## Ölçüm ve karar (Faz 35 Aşama B, 2026-10-03)

Dev (46 örnek), `claude_cli` / `claude-opus-5-5`, two_pass, önbellek kapalı:

| | P / R / F1 | p50 / p95 (sn) | Token ort. | Koruma müdahalesi |
|---|---|---|---|---|
| Doğrulamasız | 69 / 89 / 78 | 17,9 / 36,1 | 14,1 bin | 11 |
| Doğrulamalı | **79 / 89 / 84** | 22,1 / 38,3 | 15,9 bin | 6 |

Güven eşiği (doğrulamalı koşu): ≥ 0,5 / 0,6 F1 84, ≥ 0,7 F1 83, ≥ 0,85 P 90 / R 78 / F1 83.

**Karar:** `pipeline.verify_findings = true` varsayılan. Precision 10 puan arttı, recall
kaybı yok; ek gecikme (~%24) ve token (~%13) tek dosyalık mentorluk kullanımında kabul
edilebilir. Güven eşiği uygulanmaz (F1'i artırmıyor; `certainty` rapordaki `confidence`
değerini belirlemeye devam eder). Doğrulamasız ölçüm için `eval run --ablate noverify`.
Testlerde doğrulama kapalı başlar (betikli FakeProvider yanıtları; `tests/conftest.py`).
Ayrıntı: `docs/eval-findings.md` §9.

## Ek (Faz 39, 2026-10-04): ölçek kanıtı ve düşürülenlerin kaydı

**Sorun:** Performans sorununda çıktı doğrudur, yanlış olan büyüme hızıdır. Model "girdi /
beklenen / gerçekleşen" gösteremeyince doğru bulguyu düşürüyordu (Claude dev parça 2: `cpp-007`).
Codex `gpt-6-luna` 96 örnek ölçümünde 10 düşürmenin en az 5'i gerçek hataydı. Bunların çoğu
performans dışıydı: sığ kopya → çift silme, gezilirken dizi değişmesi, `Super::BeginPlay` eksik.

**Karar:**
- Ölçek kanıtı **mevcut alanlarla** verilir: `input = "n = 100000"`, `expected = "O(n)"`,
  `actual = "O(n^2)"`. LLM şeması, şema sürümü ve dar bağlam bütçesi değişmez. Plandaki yeni alan
  önerisinden bu yüzden vazgeçildi.
- Sistem denetimi (`verify/proof.py`): `expected` ya da `actual` `O(` ile başlıyorsa iddia ölçek
  kanıtıdır. Yalnız `performance` / `garbage_collection` kategorisinde geçerlidir. İki ifade de
  `parse_bigo` ile ayrışmalı ve gerçekleşen beklenenden hızlı büyümelidir (çok değişkenliler
  `collapse_variables` ile tek değişkene indirgenir). Aksi halde taban `no_demonstration`, bulgu
  düşer. Yeni taban `ProofBasis = "scaling"`.
- Prompt (`verify.system.j2` kural 3–4): ölçek kanıtı (c) maddesi; girdi bir işlem dizisi ya da
  motor olayı da olabilir; büyümesi gösterilen performans sorunu "kuramsal" değildir.
- Doğrulama kararları (`FindingCheck`, artık `category` taşır) `Orchestrator.analyze_traced` ile
  eval sonucuna (`SampleResult.finding_checks`) yazılır. `eval analyze` "Doğrulamanın attığı
  bulgular" bölümünde düşürmeleri gerçek hata / yanlış alarm diye ayırır.

**Bedeli / risk:** Daha az bulgu düşeceği için precision biraz düşebilir. Etki canlı dev
ölçümüyle (Claude, 96 örnek) görülecek; Faz 39 çevrimdışı yapıldı.

