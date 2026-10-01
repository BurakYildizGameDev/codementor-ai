# ADR-0015: Python, HTML ve CSS desteği; işaretleme dilleri için karmaşıklıksız hat

**Tarih:** 2026-10-01 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §1.4, §4, §5.1–§5.4, §6.2, §6.3, §7, §8; ADR-0005, ADR-0013

## Bağlam

v1.0 yalnızca C, C++ ve C#'ı (Unity, Unreal) kapsıyordu (mimari §1.4 "hedef dışı: diğer
diller"). Kullanıcı Python'u ve "basit olduğu için" HTML ile CSS'i istedi. Python, C ailesi gibi
algoritmik bir dildir: döngü, özyineleme ve Big-O anlamlıdır. HTML ve CSS ise işaretleme ve stil
dilleridir. Zaman/bellek karmaşıklığı yoktur. Öğrenci hataları erişilebilirlik, anlamsal yapı,
standartlar ve bakım kolaylığıyla ilgilidir. Mevcut hat, Geçiş A şemasında karmaşıklığı zorunlu
tutuyor ve rapor bunu doğrulayıp gösteriyordu.

## Karar

1. `Language` enum'una `python`, `html`, `css` eklendi. Motor (Unity/Unreal) yalnız C ailesinde.
   `models.enums.has_complexity(language)` ayrımı yapar: HTML ve CSS `MARKUP_LANGUAGES`'tadır.
2. **Python, tam hat:**
   - Tier 0: tree-sitter-python.
   - Tier 1: süreç içi `compile(..., PyCF_ONLY_AST)`. Kod **çalıştırılmaz** (ADR-0005
     korunur), dış araç gerekmez. Girinti hataları ve `SyntaxWarning` gibi tree-sitter'ın
     kaçırdıklarını yakalar.
   - Olgular: `queries/python/*.scm` sorguları ile `_symbols` ve `_loops` modüllerinin
     Python dalları.
     - `for x in xs` doğrusal; `range(sabit)` sabit; `//=` ile yarılama logaritmik.
     - Kavramalar (comprehension) örtük döngü sayılır.
     - Tip, ek açıklamadan ya da değerden çıkarılır (`xs: list`, `seen = []`).
     - Listede `x in xs` araması `list.__contains__` maliyetli çağrı olarak olguya girer.
   - Maliyet tablosu: `data/call_costs.yaml` → `python` bölümü.
3. **HTML ve CSS, karmaşıklıksız hat:**
   - Olgu çıkarımı ve Big-O ipucu yok (`facts` aşaması boş olgu üretir).
   - Tier 1 `SKIPPED/not_applicable` ve uyarı yok.
   - Geçiş A yeni şemayla (`LLMMarkupAnalysisOutput`: yalnızca `additional_findings`) ve
     ayrı şablonlarla (`markup_analysis.*.j2`, `_markup_rules.j2`) çalışır. Doğrulama
     `verify_markup_analysis` ile yapılır; satır kanıtı aynen geçerlidir.
   - Tek geçiş modu istense de işaretleme dillerinde iki geçiş kullanılır.
   - Raporda `complexity = null`; arayüzler karmaşıklık kartını gizler.
4. Yeni denetim kategorileri: `accessibility`, `maintainability` (mentor şablonları ve
   etiketleriyle).
5. Soru modelinde `expected` (hedef karmaşıklık) artık isteğe bağlıdır. Programlama dillerinde
   zorunlu, HTML/CSS'te yasaktır (model doğrulayıcısı).
6. 13 statik kural (fixture'lı):
   - `PY-DESIGN-001` değiştirilebilir varsayılan, `PY-DESIGN-002` `== None`,
     `PY-EDGE-001` çıplak except, `PY-PERF-001` döngüde `pop(0)` / `insert(0)` / listede
     `in`, `PY-RES-001` with dışında `open`.
   - `HTML-ACC-001` alt yok, `HTML-ACC-002` lang yok, `HTML-ACC-003` etiketsiz form alanı,
     `HTML-STD-001` yinelenen id, `HTML-STD-002` DOCTYPE yok.
   - `CSS-MAINT-001` çok sayıda `!important`, `CSS-MAINT-002` boş blok, `CSS-STD-001` aynı
     blokta yinelenen özellik.
   Kural kimliği biçimi rakamlı kategoriye (`A11Y`) izin vermediği için erişilebilirlik `ACC`.
7. Dil tespiti: Python/HTML/CSS sinyalleri ham kodda aranır (C maskeleyicisi `#` yorumlarını
   ve etiketleri tanımaz). Bu diller ancak C ailesi puanından belirgin biçimde yüksekse seçilir.
8. Veri: `data/checklists/{python,html,css}.yaml`, dört yeni soru (iki Python, bir HTML, bir CSS).
   Few-shot örneği yok; seçici yalnız aynı dili aldığı için yanlış dil örneği girmez.

## Sonuçlar

- Prompt sürümü değişti (sistem cümlesine "ve Python"). Golden prompt dosyaları güncellendi;
  önceki eval sonuçları eski sürüme aittir.
- Eval veri seti genişletilmedi: yeni dillerin precision/recall ve sızıntı oranı ölçülmedi.
  README "Sınırlamalar" bunu belirtir. **Güncelleme (Faz 18, 2026-10-01):** dil başına 12
  örnek eklendi ve ölçüldü; sonuçlar `docs/eval-findings.md` §4.
- Python Tier 1 süreç içinde çalışır. Çok derin iç içe girdide `RecursionError`
  yakalanır ve denetim atlanır.
- HTML'de kapanmamış/uyumsuz etiketler tree-sitter-html'de hata sayılmaz (tarayıcılar da
  hoşgörülüdür). Etiket dengesi denetimi ileride eklenebilir (PROGRESS "Sonraya").
  **Güncelleme (Faz 20, 2026-10-01):** statik kural `HTML-STD-003` eklendi (stdlib
  `html.parser` ile açık etiket yığını). Kullanıcı kararıyla sözdizimi hatası değil bulgudur:
  analiz durmaz, bulgu LLM'e "statik analizin bulduğu" olarak gider.
- Yeni sorular için referans çözümler `private/solutions/` altına eklenmelidir. Dosya
  yoksa sızıntı denetimi yalnız soru metni ve n-gram üzerinden yapılır.
