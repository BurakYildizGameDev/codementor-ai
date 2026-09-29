# CodeMentor AI — Faz Faz Uygulama Planı
### Claude Code (Claude CLI) ve Antigravity CLI ile

| Alan | Değer |
|---|---|
| Referans mimari | `docs/mimari.md` (bu plandaki bölüm numaraları oraya atıftır) |
| Toplam faz | 14 (Faz 0 – Faz 13) + kurulum |
| Tahmini süre | 5–7 hafta (günde 2–3 saat) |
| Çalışma biçimi | Her faz ayrı git dalı, ayrı ajan oturumu, testlerle kapanır |

---

## İçindekiler

1. Bu doküman nasıl kullanılır
2. İki aracı birlikte kullanma stratejisi
3. Kurulum (Faz öncesi)
4. Ajan yapılandırma dosyaları (kopyala-yapıştır)
5. Standart faz döngüsü
6. Fazlar
7. PROGRESS.md şablonu
8. Sorun giderme
9. Zaman çizelgesi

---

## 1. Bu Doküman Nasıl Kullanılır

- `mimari.md` ve bu dosyayı reponun `docs/` klasörüne koy. Ajanlar ikisini de okuyacak.
- Her fazda **Görev metni** bloğunu ajana ver. Bölüm 4'teki `/faz` komutunu kurduysan sadece `/faz 3` yazman yeterli; komut ilgili bölümü bu dosyadan kendisi okur.
- **Kabul kriterleri** karşılanmadan faz kapatılmaz. Ajan "bitti" dese bile Doğrulama komutlarını kendin çalıştır.
- Bir fazı bir araçla yap. Aynı dalda iki ajanı aynı anda çalıştırma; dosya çakışması olur.

> **Not:** Araçların komutları ve dosya konumları sık güncelleniyor. Aşağıdaki kurulum ve yapılandırma bilgileri Eylül 2026 itibarıyla derlendi; bir şey çalışmazsa önce resmi dokümana bak:
> Claude Code → https://docs.claude.com/en/docs/claude-code/overview
> Antigravity CLI → https://github.com/google-antigravity/antigravity-cli

---

## 2. İki Aracı Birlikte Kullanma Stratejisi

Tek araçla da bütün planı yapabilirsin. İkisine de erişimin varsa önerilen düzen şu:

| Rol | Önerilen araç | Neden |
|---|---|---|
| Uygulayıcı (faz yazan) | Hangisinde daha rahatsan | Tutarlılık için bir fazı baştan sona aynı araç yapar |
| Denetçi (fazı gözden geçiren) | **Diğer** araç | Farklı model ailesi, farklı kör noktalar yakalar |

Pratik akış:

1. Faz N'i A aracıyla uygula, testler geçsin, commit at.
2. B aracında `/faz-denetim` (Antigravity) veya `kod-denetci` alt ajanı (Claude Code) ile aynı dalı gözden geçirt.
3. Denetim bulgularını A aracına geri ver ya da küçükse B'ye düzelttir.
4. Dalı `main`'e birleştir.

**Tek doğruluk kaynağı ilkesi:** Proje kuralları yalnızca `AGENTS.md`'de yaşar. Antigravity bu dosyayı doğrudan okur; Claude Code ise `CLAUDE.md` içinden `@AGENTS.md` ile içe aktarır. Kuralları iki yerde tutma, zamanla birbirinden kopar.

---

## 3. Kurulum (Faz Öncesi)

### 3.1 Sistem gereksinimleri

| Araç | Sürüm | Kontrol |
|---|---|---|
| Python | 3.12+ | `python3 --version` |
| uv | güncel | `uv --version` |
| Git | 2.40+ | `git --version` |
| gcc / clang | opsiyonel (Tier 1 C/C++ için) | `gcc --version` |
| .NET SDK | opsiyonel (Tier 1 C# için) | `dotnet --version` |

Docker **gerekmez** (ADR-0009). Derleyiciler kurulu değilse Tier 1 `SKIPPED` olur; sistem Tier 0 ile çalışır.
| Node.js | 20+ (Web UI ve Claude Code npm kurulumu için) | `node --version` |
| Ollama | güncel | `ollama --version` |

```bash
# uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ollama modeli (GPU'na göre boyut seç: 7b ~ 8 GB VRAM civarı rahat çalışır)
ollama pull qwen2.5-coder:7b
```

### 3.2 Claude Code

```bash
npm install -g @anthropic-ai/claude-code   # veya dokümandaki yerel kurulum betiği
claude --version
cd codementor-ai && claude                  # ilk açılışta oturum açma
```

Bilmen gereken temel kullanım:

| Özellik | Kullanım |
|---|---|
| Plan modu | `Shift+Tab` ile geçiş; ajan dosya değiştirmeden plan çıkarır |
| Bağlamı temizle | `/clear` (her fazdan sonra) |
| Bağlamı sıkıştır | `/compact` (uzun fazın ortasında) |
| Dosya referansı | `@docs/mimari.md` |
| Özel komut | `.claude/commands/faz.md` → `/faz 3` |
| Alt ajan | `.claude/agents/kod-denetci.md` → "kod-denetci alt ajanını kullanarak incele" |
| Hook | `.claude/settings.json` → her düzenlemeden sonra otomatik `ruff` |
| Başsız mod | `claude -p "..."` (CI veya betik içinde) |

### 3.3 Antigravity CLI

Kurulumu resmi repodaki betikle yap (repo: `google-antigravity/antigravity-cli`). Komut adı `agy`.

```bash
agy --version
cd codementor-ai && agy
```

Bilmen gereken temel kullanım:

| Özellik | Konum / Komut |
|---|---|
| Proje talimatları | `AGENTS.md` (kök) ve `.agents/rules/*.md` |
| Global kurallar | `~/.gemini/GEMINI.md` |
| İş akışları (slash komut) | `.agents/workflows/faz.md` → `/faz` |
| Beceriler (skills) | `.agents/skills/<ad>/SKILL.md` |
| Oturuma dön | `/resume` |
| MCP yönetimi | `/mcp` |

Yüklü kuralları kontrol etmek için ajana şunu sor: *"Hangi kurallar ve iş akışları yüklü?"*

### 3.4 Repo oluşturma

```bash
mkdir codementor-ai && cd codementor-ai
git init -b main
mkdir -p docs .claude/commands .claude/agents .agents/rules .agents/workflows .agents/skills/faz-denetim
cp ~/Downloads/mimari.md ~/Downloads/UYGULAMA_PLANI.md docs/
# Bölüm 4'teki dosyaları oluştur
git add . && git commit -m "docs: mimari ve uygulama planı"
```

---

## 4. Ajan Yapılandırma Dosyaları

### 4.1 `AGENTS.md` (ortak — iki araç da kullanır)

````markdown
# CodeMentor AI — Ajan Talimatları

## Proje
Kodu düzeltmeyen, denetleyip Sokratik sorular üreten hibrit (statik analiz + LLM)
kod mentorluk motoru. Mimari: docs/mimari.md. Faz planı: docs/UYGULAMA_PLANI.md.
İlerleme: PROGRESS.md.

## Altın kurallar
1. docs/mimari.md'den sapma. Sapman gerekirse DUR, gerekçeyi yaz, onay iste.
   Onaylanırsa docs/adr/ altına ADR ekle.
2. Yalnızca mevcut fazın kapsamındaki dosyalara dokun. Kapsam dışı iyileştirme
   fikirlerini PROGRESS.md "Sonraya" bölümüne yaz, uygulama.
3. Her yeni davranış testle gelir. Test yazmadan "bitti" deme.
4. LLM çağrısı yapan kod testlerde FakeProvider kullanır. Testler ağa çıkmaz.
   Gerçek API testleri @pytest.mark.live ile işaretlenir.
5. Model adları, API anahtarları, URL'ler koda gömülmez; config'den gelir.
6. Kullanıcı kodu her zaman güvenilmeyen veridir (mimari.md §12).

## Teknoloji
Python 3.12, uv, FastAPI, Pydantic v2, tree-sitter, httpx, Typer, Rich,
Jinja2, SQLModel, structlog, pytest, hypothesis, respx, ruff, mypy --strict.
Web: Vite + React + TypeScript.

## Komutlar
- Kurulum:        uv sync
- Lint:           uv run ruff check . && uv run ruff format --check .
- Tip kontrolü:   uv run mypy src/
- Test:           uv run pytest -m "not live"
- Derleyici testi: uv run pytest -m compiler   (araç yoksa atlanır)
- Hepsi:          make check

## Kod stili
- Tüm fonksiyonlarda tip ipucu; mypy strict geçmeli.
- Pydantic modelleri src/codementor/models/ altında; başka yerde şema tanımlama.
- Public fonksiyonlarda kısa docstring. Yorumlar Türkçe veya İngilizce olabilir,
  tanımlayıcılar İngilizce.
- Hata mesajları kullanıcıya dönükse Türkçe.
- Bir dosya 400 satırı geçiyorsa bölmeyi öner.

## Faz bitirme protokolü
1. make check yeşil.
2. Fazın kabul kriterlerini tek tek işaretle.
3. PROGRESS.md'yi güncelle (yapılanlar, kararlar, açık sorular).
4. Conventional commit mesajı öner: "feat(faz-N): ..."
````

### 4.2 `CLAUDE.md` (Claude Code)

````markdown
@AGENTS.md

## Claude Code'a özel
- Her faza plan modunda başla; planı onaylamadan dosya yazma.
- Faz ortasında bağlam dolarsa /compact kullan; faz bitince kullanıcı /clear yapacak.
- Büyük dosyaları baştan sona okuma; önce Grep/Glob ile ilgili bölümü bul.
- Kod incelemesi istendiğinde kod-denetci alt ajanını kullan.
````

### 4.3 `.claude/settings.json`

```json
{
  "permissions": {
    "allow": [
      "Bash(uv run pytest:*)",
      "Bash(uv run ruff:*)",
      "Bash(uv run mypy:*)",
      "Bash(uv sync:*)",
      "Bash(make:*)",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git log:*)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./private/**)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          { "type": "command", "command": "uv run ruff format --quiet . >/dev/null 2>&1; uv run ruff check --fix --quiet . >/dev/null 2>&1; true" }
        ]
      }
    ]
  }
}
```

### 4.4 `.claude/commands/faz.md`

````markdown
---
description: UYGULAMA_PLANI.md'deki bir fazı standart protokolle uygular
argument-hint: <faz-numarası>
---
Faz $ARGUMENTS üzerinde çalışacağız.

1. @docs/UYGULAMA_PLANI.md içinde "### Faz $ARGUMENTS " ile başlayan bölümü oku.
2. O bölümün atıf yaptığı @docs/mimari.md kısımlarını oku.
3. @PROGRESS.md'yi oku; önceki fazlardan kalan açık soruları not et.
4. Kod yazmadan önce şunları içeren bir plan sun:
   - oluşturulacak/değiştirilecek dosyalar
   - yazılacak testler (dosya ve test adlarıyla)
   - mimariyle çelişen veya belirsiz noktalar
   - kabul kriterlerinin nasıl doğrulanacağı
5. Onayımı bekle.
6. Onaydan sonra önce testleri, sonra uygulamayı yaz (mümkünse TDD).
7. make check çalıştır; yeşil olana kadar düzelt.
8. Kabul kriterlerini tek tek [x] ile raporla, PROGRESS.md'yi güncelle,
   commit mesajı öner. Commit'i ben atacağım.
````

### 4.5 `.claude/agents/kod-denetci.md`

````markdown
---
name: kod-denetci
description: Tamamlanan bir fazın kodunu mimari uyum, test kalitesi ve güvenlik açısından inceler. Faz bitince veya "denetle" denince kullan.
tools: Read, Grep, Glob, Bash
---
Sen kıdemli bir kod denetçisisin. Dosya DEĞİŞTİRMEZSİN, yalnızca rapor yazarsın.

Kontrol listesi:
1. docs/mimari.md ile uyum: model adları, katman sınırları, şema ayrımı (§6.1).
2. Kapsam: fazın dışında dosya değişmiş mi? (git diff main --stat)
3. Testler: her kural için pozitif + negatif fixture var mı? Testler gerçekten
   davranışı mı doğruluyor, yoksa sadece çalışıyor mu?
4. Güvenlik: kullanıcı kodu prompt'a sınırlayıcısız giriyor mu? Tier 1 yerel
   yürütme önlemleri (include koruması, stdin, zaman aşımı) eksik mi? Gizli anahtar
   loglanıyor mu?
5. Tip güvenliği: Any, type: ignore, cast kullanımı gerekçeli mi?
6. Hata yönetimi: sessizce yutulan istisna var mı?

Çıktı biçimi: Kritik / Önemli / Küçük başlıkları altında dosya:satır referanslı
maddeler. Sonunda "Birleştirilebilir mi: Evet/Hayır" kararı.
````

### 4.6 `.agents/rules/codementor.md` (Antigravity)

````markdown
---
trigger: always_on
---
# CodeMentor çalışma kuralı
- Proje talimatlarının tamamı kökteki AGENTS.md dosyasındadır; her görevde uygula.
- Her faza planlama ile başla: uygulama planı çıkar, kullanıcı onaylamadan dosya yazma.
- Görev listesini fazın kabul kriterlerinden türet.
- Faz bitince kabul kriterlerini tek tek doğrula ve make check çıktısını göster.
- .env ve private/ dizinini okuma.
````

### 4.7 `.agents/workflows/faz.md` (Antigravity)

````markdown
---
description: UYGULAMA_PLANI.md'deki bir fazı standart protokolle uygular
---
1. Kullanıcının belirttiği faz numarasını al. Belirtilmemişse PROGRESS.md'deki
   ilk tamamlanmamış fazı kullan ve bunu kullanıcıya söyle.
2. docs/UYGULAMA_PLANI.md içinde "### Faz <N> " bölümünü ve atıf yaptığı
   docs/mimari.md kısımlarını oku.
3. PROGRESS.md'yi oku.
4. Uygulama planı üret: dosyalar, testler, riskler, kabul kriterlerinin doğrulama yolu.
5. Kullanıcı onayını bekle.
6. Önce testleri, sonra uygulamayı yaz.
7. make check çalıştır; yeşil olana kadar düzelt.
8. Kabul kriterlerini raporla, PROGRESS.md'yi güncelle, commit mesajı öner.
````

### 4.8 `.agents/skills/faz-denetim/SKILL.md` (Antigravity)

````markdown
---
name: faz-denetim
description: Tamamlanan bir fazın kodunu mimari uyum, test kalitesi ve güvenlik açısından inceler. Kullanıcı "denetle", "review" veya "/faz-denetim" dediğinde kullan.
---
# Faz denetimi
Dosya DEĞİŞTİRME; yalnızca rapor üret.

1. `git diff main --stat` ile değişen dosyaları listele; faz kapsamı dışındakileri işaretle.
2. docs/mimari.md ile uyumu kontrol et (katman sınırları, §6.1 şema ayrımı, §12 güvenlik).
3. Testleri incele: her kural için pozitif/negatif fixture, sağlayıcı testlerinde ağ yok.
4. `make check` çalıştır ve sonucu ekle.
5. Rapor: Kritik / Önemli / Küçük (dosya:satır) + "Birleştirilebilir mi" kararı.
````

---

## 5. Standart Faz Döngüsü

Her faz için aynı 9 adım:

```
1. git checkout -b faz/N-kisa-ad
2. Ajanı başlat (claude / agy) — temiz oturum
3. /faz N   (veya Görev metnini yapıştır)
4. Planı OKU. Sorular:
     - Mimariyle çelişen bir şey var mı?
     - Kapsam dışı dosya var mı?
     - Test listesi kabul kriterlerini karşılıyor mu?
5. Onayla → ajan uygular
6. Doğrulama komutlarını KENDİN çalıştır
7. Diğer araçla denetim (opsiyonel ama önerilir)
8. git commit → git checkout main → git merge --no-ff faz/N-...
9. Oturumu kapat (Claude Code: /clear)
```

**Altın kural:** Ajanın ürettiği kodu anlamadan birleştirme. Mülakatta bu kodu savunacak olan sensin. Her fazın sonunda "Bu fazda ne öğrendim?" sorusunu PROGRESS.md'ye iki cümleyle yaz.

---

## 6. Fazlar

### Genel bakış

| Faz | Başlık | Süre | Bağımlılık | Mimari § |
|---|---|---|---|---|
| 0 | Repo iskeleti ve araç zinciri | 0.5 gün | — | 16, 17, 19 |
| 1 | Veri modelleri ve Big-O ayrıştırıcı | 1.5 gün | 0 | 6 |
| 2 | Soru bankası ve kontrol listeleri | 1 gün | 1 | 7, 8.3 |
| 3 | Normalizasyon ve Tier 0 | 1.5 gün | 1 | 5.1, 5.2.1 |
| 4 | Tier 1 yerel derleyici (Docker'sız) | 2 gün | 3 | 5.2.2–5.2.4, 12 |
| 5 | Olgu çıkarımı ve karmaşıklık ipucu | 3 gün | 3 | 5.3.1, 5.3.2 |
| 6 | Kural motoru ve 20 kural | 3 gün | 5 | 5.3.3, 8 |
| 7 | Sağlayıcı adaptörleri | 2.5 gün | 1 | 5.5 |
| 8 | Prompt orkestrasyonu | 2 gün | 2, 6, 7 | 5.4 |
| 9 | Doğrulayıcı ve sızıntı koruması | 2.5 gün | 8 | 5.6 |
| 10 | Pipeline, CLI, depolama | 2.5 gün | 9 | 4, 10, 11 |
| 11 | REST API ve SSE | 1.5 gün | 10 | 9 |
| 12 | Eval altyapısı ve veri seti | 4 gün | 10 | 14 |
| 13 | Web UI, kurulum, dokümantasyon | 3 gün | 11, 12 | 5.7, 18, 23 |

Faz 7, Faz 3–6 ile paralel yürütülebilir (farklı dallar, farklı dosyalar).

---

### Faz 0 — Repo İskeleti ve Araç Zinciri

**Süre:** 0.5 gün · **Dal:** `faz/0-iskelet` · **Mimari:** §16, §17, §19

**Amaç:** Boş ama tam çalışan bir Python projesi: lint, tip kontrolü, test ve CI yeşil.

**Çıktılar**
- `pyproject.toml` (uv, ruff, mypy strict, pytest yapılandırması, `codementor` konsol betiği)
- `src/codementor/__init__.py`, `src/codementor/config.py` (pydantic-settings, §17'deki alanların iskeleti)
- `src/codementor/cli/main.py` (Typer; yalnızca `codementor --version`)
- `tests/unit/test_smoke.py`, `tests/unit/test_config.py`
- `Makefile` (`setup lint typecheck test check`), `.gitignore` (`.env`, `private/`, `eval/results/`, `*.db`), `.env.example`, `codementor.toml` örneği
- `.github/workflows/ci.yml` (ruff, mypy, pytest)
- `PROGRESS.md` (Bölüm 7 şablonu)
- Bölüm 4'teki ajan dosyaları

**Kabul kriterleri**
- [ ] `uv sync && make check` temiz makinede yeşil
- [ ] `uv run codementor --version` sürüm basıyor
- [ ] Config: env değişkeni TOML değerini eziyor (testle kanıtlı)
- [ ] pytest işaretleri tanımlı: `live`, `compiler`, `slow` (`sandbox` → `compiler`, ADR-0009)
- [ ] CI GitHub'da yeşil

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 0'ı uygula. Mimari §16 dizin yapısını ve §17
konfigürasyon öncelik sırasını (CLI > env > codementor.toml > varsayılan) kullan.
Bu fazda iş mantığı YOK: yalnızca iskelet, config, CLI girişi, Makefile, CI.
mypy --strict ve ruff baştan açık olsun. pytest işaretleri: live, compiler, slow.
Config için env değişkeninin TOML'u ezdiğini doğrulayan test yaz.
```

**Claude Code'da:** Bölüm 4 dosyalarını elle oluştur, sonra `claude` → `Shift+Tab` (plan modu) → görev metni. Plan onayından sonra plan modundan çık.

**Antigravity CLI'da:** Bölüm 4 dosyalarını elle oluştur, `agy` → önce *"Hangi kurallar ve iş akışları yüklü?"* diye sorarak `.agents/rules/codementor.md` ve `/faz` iş akışının yüklendiğini doğrula → `/faz 0`.

**Doğrulama**
```bash
uv sync && make check
uv run codementor --version
CODEMENTOR_LIMITS__MAX_LINES=10 uv run python -c "from codementor.config import get_settings; print(get_settings().limits.max_lines)"
```

**Tuzaklar:** Ajan bu fazda "örnek" iş mantığı eklemeye meyillidir, reddet. Nested env değişkeni ayracı (`__`) pydantic-settings'te açıkça ayarlanmalı.

**Commit:** `chore(faz-0): proje iskeleti, araç zinciri ve CI`

---

### Faz 1 — Veri Modelleri ve Big-O Ayrıştırıcı

**Süre:** 1.5 gün · **Dal:** `faz/1-modeller` · **Mimari:** §6, §5.6 (Big-O dilbilgisi)

**Amaç:** Sistemin tüm veri sözleşmeleri ve Big-O normalizasyonu. Sonraki her faz bunlara dayanır.

**Çıktılar**
- `models/enums.py`, `request.py`, `facts.py` (§5.3.1 olguları), `findings.py`, `llm_output.py`, `report.py`
- `models/bigo.py`: `parse_bigo(str) -> BigO`, `BigO.canonical`, `BigO.display` (`O(n²)`), tek değişkenli sıralama (`<`), `same_class()`
- `codementor schema export` komutu → `schemas/*.schema.json`
- `tests/unit/test_bigo.py` (hypothesis ile özellik testleri dahil), `tests/unit/test_models.py`
- `tests/golden/report_example.json` (§6.5 örneği) doğrulama testi

**Kabul kriterleri**
- [ ] §6.3 ve §6.4'teki tüm alanlar mevcut; LLM modelleri ile rapor modeli ayrı modüllerde
- [ ] `parse_bigo` şunları aynı kanonik biçime çeviriyor: `O(N^2)`, `O(n²)`, `O(n*n)`, `o(n^2)`, `n^2`
- [ ] `n log n`, `nlogn`, `N*log(N)` → `n log n`
- [ ] Çok değişkenli: `O(V+E)`, `O(n*m)` ayrıştırılıyor, sıralama çağrısında anlaşılır istisna
- [ ] Sıralama: `1 < log n < n < n log n < n^2 < n^3 < 2^n < n!` (hypothesis ile geçişlilik testi)
- [ ] §6.5 örnek JSON `AnalysisReport.model_validate` ile geçiyor
- [ ] `codementor schema export` 3 şema dosyası üretiyor

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 1'i uygula. Modeller mimari §6'da birebir tanımlı;
alan adlarını değiştirme. §6.1'deki "LLM şeması ≠ rapor şeması" ayrımına uy.
bigo.py için §5.6'daki dilbilgisini uygula; regex yığını yerine küçük bir
tokenizer + ayrıştırıcı tercih et. Üslü sayılar için unicode üst simgeleri
(², ³) destekle. Tek değişkenli ifadeler için toplam sıralama, çok değişkenliler
için same_class karşılaştırması. hypothesis ile sıralamanın geçişliliğini test et.
schema export CLI komutunu ekle.
```

**Claude Code'da:** Plan modunda `@docs/mimari.md` §6'yı referans vererek başla. Big-O ayrıştırıcı için "önce test listesini göster" de; sınır durumlarını birlikte genişletin.

**Antigravity CLI'da:** `/faz 1`. Planlama çıktısındaki görev listesinde Big-O test vakalarının ayrı madde olarak geçtiğini kontrol et.

**Doğrulama**
```bash
make check
uv run codementor schema export --out schemas/ && ls schemas/
uv run python -c "from codementor.models.bigo import parse_bigo as p; print(p('O(N²)').display, p('nlogn') < p('n^2'))"
```

**Tuzaklar:** Ajan `log n` ile `log(n)` arasında farklı kanonik biçim üretebilir; testte ikisini de iste. `display` alanında `n^2` → `n²` dönüşümünü unutmasın.

**Commit:** `feat(faz-1): veri modelleri, JSON şema üretimi ve Big-O ayrıştırıcı`

---

### Faz 2 — Soru Bankası ve Kontrol Listeleri

**Süre:** 1 gün · **Dal:** `faz/2-soru-bankasi` · **Mimari:** §7, §8.3

**Amaç:** YAML tabanlı, doğrulanmış soru ve kontrol listesi yükleyicileri + başlangıç içeriği.

**Çıktılar**
- `questions/bank.py`: `QuestionBank.load(dir)`, `get(id)`, `filter(language, engine, difficulty)`
- `questions/checklists.py`: `select_items(language, engine, concept_tags, limit=12)`
- `data/questions/*.yaml`: §7.2'deki 14 soru
- `data/checklists/{c,cpp,csharp,unity,unreal}.yaml`
- CLI: `codementor questions list|show`
- Testler: YAML şema hataları anlaşılır mesaj veriyor; `reference_solution_path` dışa verilen modelde yok

**Kabul kriterleri**
- [ ] 14 soru yükleniyor, her biri Pydantic ile doğrulanıyor
- [ ] Yinelenen `id` yükleme hatası veriyor
- [ ] `QuestionPublic` modeli referans çözüm yolunu **içermiyor** (testle kanıtlı)
- [ ] Kontrol listesi seçimi: `core` etiketliler + etiket kesişimi, en fazla 12
- [ ] `codementor questions list --language c --difficulty hard` doğru filtreliyor

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 2'yi uygula. Soru formatı mimari §7.1, başlangıç
matrisi §7.2, kontrol listesi formatı §8.3. 14 sorunun içeriğini sen yaz;
prompt, constraints, concept_tags ve 3 seviyeli hint_ladder her soruda dolu olsun.
Referans çözümleri YAZMA (private/ dizini bu fazın konusu değil).
QuestionPublic ile Question modellerini ayır; API ve CLI yalnızca Public'i görür.
```

**Claude Code'da:** 14 sorunun içeriği uzun; ajana "önce 2 soruyu yaz, onaylayayım, sonra kalanları aynı kalitede yaz" de. Bu, stil tutarlılığını korur.

**Antigravity CLI'da:** Aynı yaklaşım: içerik üretimini iki aşamaya böl. Görev listesinde "soru içeriği" ve "yükleyici kodu" ayrı maddeler olsun.

**Doğrulama**
```bash
make check
uv run codementor questions list
uv run codementor questions show unity-hard-inventory
```

**Tuzaklar:** Ajan soru metinlerine çözüm ipucu sızdırabilir (ör. "HashSet kullanarak..."). Soru metinleri problemi tanımlar, yöntemi söylemez. Hepsini oku.

**Commit:** `feat(faz-2): soru bankası, kontrol listeleri ve 14 başlangıç sorusu`

---

### Faz 3 — Normalizasyon ve Tier 0 Ön Doğrulama

**Süre:** 1.5 gün · **Dal:** `faz/3-tier0` · **Mimari:** §5.1, §5.2.1, §5.2.4

**Amaç:** Kodu normalize etmek, dili/motoru tespit etmek, tree-sitter ile sözdizimi hatalarını bulmak.

**Çıktılar**
- `ingest/normalize.py` (boyut limitleri, UTF-8/BOM, CRLF, numaralı görünüm, SHA-256)
- `ingest/detect.py` (dil/motor sezgileri; güven skoru; belirsizse istisna)
- `analysis/parsers.py` (dil başına önbelleklenmiş tree-sitter `Parser`)
- `validation/tier0.py` (`ERROR`/`MISSING` düğümleri → `Diagnostic`)
- `validation/policy.py` (§5.2.4 tablosu; bu fazda yalnızca Tier 0 satırları)
- Fixture'lar: `tests/fixtures/tier0/{c,cpp,csharp}/{valid,invalid}/` (dil başına 5+5)

**Kabul kriterleri**
- [ ] Numaralı görünüm sağa hizalı ve satır sayısıyla birebir
- [ ] Limit aşımında anlamlı istisna (`CodeTooLargeError`)
- [ ] Dil tespiti: 15 fixture'da doğru (Unity ve Unreal dahil)
- [ ] Tier 0: tüm `invalid` fixture'larda en az bir hata, doğru satırda (±1)
- [ ] Tier 0: tüm `valid` fixture'larda sıfır hata (Unreal makroları dahil!)
- [ ] Tier 0 tek dosyada < 50 ms (basit zamanlama testi, `@pytest.mark.slow`)

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 3'ü uygula. Mimari §5.1 ve §5.2.1. tree-sitter için
tree-sitter, tree-sitter-c, tree-sitter-cpp, tree-sitter-c-sharp paketlerini
kullan. Parser'ları modül düzeyinde önbelleğe al. Hata raporu için ağaçta
ERROR ve MISSING düğümlerini gez; satır/kolon 1 tabanlı olsun. Önemli: Unreal
kodundaki UCLASS(), GENERATED_BODY() gibi makrolar tree-sitter-cpp'de ERROR
üretebilir. Geçerli Unreal fixture'larıyla test et; sorun çıkarsa makro
satırlarını ayrıştırmadan önce nötrleştiren bir ön işlem ekle ve satır
numaralarının kaymadığını test et.
```

**Claude Code'da:** Bu fazda tree-sitter API'sini ajanın doğru kullandığını görmek için önce küçük bir deney betiği yazdır (`scripts/ts_probe.py`) ve çıktısına birlikte bak, sonra asıl modüle geç.

**Antigravity CLI'da:** Planlama aşamasında "önce tree-sitter paket sürümlerini ve API'sini terminalde doğrula" maddesini görev listesine eklet. Sürüm uyumsuzluğu bu fazın en sık hatasıdır.

**Doğrulama**
```bash
make check
uv run pytest tests/unit/test_tier0.py -v
```

**Tuzaklar:** tree-sitter Python bağlamalarının API'si sürümler arasında değişti (`Language(...)` kurucusu). Ajan eski API ile kod üretebilir; kilitli sürümün dokümanına baktır. Unreal makroları konusunu atlama; Faz 5 buna dayanıyor.

**Commit:** `feat(faz-3): kod normalizasyonu, dil tespiti ve tree-sitter ön doğrulama`

---

### Faz 4 — Tier 1 Yerel Derleyici (Docker'sız)

**Süre:** 2 gün · **Dal:** `faz/4-tier1` · **Mimari:** §5.2.2–5.2.4, §12 · **ADR:** 0009

**Amaç:** Makinede kurulu derleyicilerle (Docker olmadan) opsiyonel sözdizimi/tip denetimi ve erken çıkış politikasının tamamı. Araç yoksa sistem Tier 0 ile sorunsuz devam eder.

**Çıktılar**
- `validation/toolchain.py`: araç keşfi — `PATH`'te `gcc`/`g++`/`clang`/`clang++`; `dotnet` + derlenmiş `tools/roslyn-check`; sonuç önbelleklenir, `/health/ready` için özet verir
- `validation/include_guard.py`: §5.2.3 include koruması (maskelenmiş kodda; `analysis/lexical.py` yeniden kullanılır)
- `validation/runner.py`: güvenli alt süreç — stdin, boş geçici `cwd`, temizlenmiş ortam, duvar saati zaman aşımı + süreç ağacını öldürme, çıktı sınırı, POSIX rlimit / Windows Job Object
- `validation/diagnostics.py`: gcc/clang `file:line:col: severity: message` ayrıştırıcı + Roslyn JSON
- `validation/tier1.py`, `validation/policy.py` (§5.2.4 tam tablo)
- `data/stubs/ue_stubs.h` (§5.2.2 listesi)
- `tools/roslyn-check/` (.NET konsol; `CSharpSyntaxTree.ParseText`; stdin → JSON tanı; dosya sistemine erişmez)
- `make test-compiler`

**Kabul kriterleri**
- [ ] Kodda ve dokümanlarda Docker'a bağımlılık yok (`docker` çağrısı yok; testle doğrulanıyor)
- [ ] Kod yalnızca stdin ile gidiyor; kullanıcı kodu diske yazılmıyor; ek `-I` yolu yok
- [ ] Include koruması: mutlak yol, `..`, sürücü harfi, `\`, `#include MACRO`, `#embed`, `__has_include` → `SKIPPED` + uyarı, derleyici hiç çağrılmıyor (testte çağrı sayısı 0)
- [ ] Araç yoksa `SKIPPED` + uyarı, istisna yok (araç keşfi sahte `PATH` ile test ediliyor)
- [ ] Zaman aşımı → süreç ağacı öldürülüyor, `SKIPPED`, erken çıkış yok (sahte yavaş süreçle test)
- [ ] C/C++ tip hatası (tree-sitter'ın görmediği) Tier 1'de yakalanıyor → `FAILED` (`@pytest.mark.compiler`, gcc/clang yoksa atlanır)
- [ ] Geçerli Unreal fixture'ı stub ile `PASSED` veya `WARNING`, asla `FAILED` değil; yerel bulunamayan başlık `WARNING`
- [ ] C# (Roslyn) Tier 1 bu makinede `dotnet` ile çalışıyor
- [ ] gcc ve clang tanı biçimleri kaydedilmiş örnek çıktılarla (derleyicisiz) test ediliyor

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 4'ü uygula (ADR-0009: Docker yok). Güvenlik bu fazın
ana konusu: mimari §5.2.3'teki yerel yürütme önlemlerinin hiçbirini atlama ve her
birini testle sabitle. Kod her zaman stdin ile verilir (-x c - / -x c++ -).
Include korumasını derleyiciden ÖNCE, yorum/metin maskelenmiş kodda uygula.
Derleyici çıktısını file:line:col: severity: message kalıbıyla ayrıştır. ue_stubs.h
§5.2.2'deki tüm makro ve tipleri içersin. Unreal stub kaynaklı hataları ve yerel
bulunamayan başlıkları WARNING'e düşür (§5.2.4). Araç yoksa veya zaman aşımında
sistem çökmemeli. Roslyn aracı için CSharpSyntaxTree.ParseText kullanan minimal
bir konsol uygulaması yaz.
```

**Claude Code'da:** Güvenlik testlerini `kod-denetci` alt ajanına ayrıca inceletmeyi unutma: "kod-denetci ile runner.py ve include_guard.py'yi yalnızca güvenlik açısından incele."

**Antigravity CLI'da:** Terminal sandbox'ı derleyici süreçlerini kısıtlayabilir; `gcc`/`dotnet` çağrılarına dar kapsamlı izin ver.

**Doğrulama**
```bash
make check
uv run pytest -m compiler -v          # kurulu araçlar için; yoksa atlanır
echo 'int main(){ int x = "a"; }' | gcc -x c -fsyntax-only -
```

**Tuzaklar:** Ajan kolaylık için kodu geçici dosyaya yazıp derleyiciye yol olarak verebilir — reddet (stdin). `shell=True` kullanılmamalı; komut her zaman liste. Windows'ta `subprocess` zaman aşımı alt süreçleri öldürmez; süreç ağacı için Job Object veya `taskkill /T` gerekir. Derleyici tanı metinleri sürüme göre değişir; testler mesaj metnine değil satır/önem düzeyine bakmalı.

**Commit:** `feat(faz-4): yerel derleyiciyle opsiyonel Tier 1 doğrulaması ve erken çıkış politikası`

---

### Faz 5 — Statik Olgu Çıkarımı ve Karmaşıklık İpucu

**Süre:** 3 gün · **Dal:** `faz/5-olgular` · **Mimari:** §5.3.1, §5.3.2

**Amaç:** Ayrıştırma ağacından `StaticFacts` üretmek ve deterministik karmaşıklık ipucu hesaplamak. Projenin teknik çekirdeği.

**Çıktılar**
- `analysis/queries/{c,cpp,csharp}/*.scm` (fonksiyon, döngü, çağrı, tahsis, alan sorguları)
- `analysis/extractor.py` → `extract_facts(tree, code) -> StaticFacts`
- `analysis/complexity_hint.py` → `ComplexityHint`
- `analysis/call_costs.py` + `data/call_costs.yaml`
- Golden testler: `tests/golden/facts/{id}/code.* + expected_facts.json` (dil/motor başına 3+)
- Karmaşıklık fixture'ları: `O(1)`, `O(log n)` (ikili arama), `O(n)`, `O(n log n)` (döngü içinde sort değil, sort + döngü), `O(n^2)` (iç içe), `O(n^2)` (döngüde `List.Contains`), üstel şüphe (naif fibonacci), two-pointer (ipucunun **yanıldığı** bilinen vaka, beklenen: düşük güven)

**Kabul kriterleri**
- [ ] Sıcak yol tespiti: Unity `Update/FixedUpdate/LateUpdate/OnGUI`, Unreal `Tick/TickComponent`
- [ ] Döngü sınır sınıfları §5.3.1 tablosuna göre doğru (fixture başına test)
- [ ] İç içe derinlik ve döngü içi çağrı derinliği doğru
- [ ] Karmaşıklık fixture'larının tamamında beklenen ipucu (two-pointer hariç, o `low` güven)
- [ ] Golden test güncelleme komutu var: `uv run pytest --update-golden`
- [ ] Bilinmeyen dilde/yapıda istisna değil, boş olgu + uyarı

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 5'i uygula. Mimari §5.3.1 olgu tablosu ve §5.3.2
ipucu algoritması. tree-sitter sorgularını .scm dosyalarında tut, Python'a gömme.
Döngü sınır sınıflandırması için §5.3.1'deki desen tablosunu uygula; emin
olamadığında UNKNOWN de, tahmin etme. İpucu hesaplamada iç içe yol boyunca
çarpım + döngü içi bilinen çağrı maliyeti kullan. İpucunun bir tahmin olduğunu
unutma: confidence alanını (low/medium/high) ve basis listesini doldur.
Two-pointer fixture'ında ipucunun yanılmasını BEKLİYORUZ; bu vaka düşük
güvenle dönmeli. Golden testler için --update-golden pytest seçeneği ekle.
```

**Claude Code'da:** Bu faz uzun. İki alt oturuma böl: (a) sorgular + extractor + golden testler, `/compact`; (b) complexity_hint + call_costs. Her alt oturum sonunda ara commit.

**Antigravity CLI'da:** Görev listesini iki kilometre taşına ayırt, ilk taş bitince durup onay istemesini söyle. Uzun görevlerde `/resume` ile aynı oturuma dönebilirsin.

**Doğrulama**
```bash
make check
uv run pytest tests/golden -v
uv run python -m codementor.analysis.extractor tests/golden/facts/unity-01/code.cs   # hata ayıklama çıktısı
```

**Tuzaklar:** Ajan karmaşıklığı "akıllıca" çözmeye çalışıp devasa bir analizör yazabilir. Bu bir ipucu motoru; basit ve açıklanabilir kalmalı. C#'ta `foreach` ile `for` farklı düğüm tipleri; C++'ta range-for ayrı düğüm.

**Commit:** `feat(faz-5): tree-sitter olgu çıkarımı ve statik karmaşıklık ipucu`

---

### Faz 6 — Kural Motoru ve 20 Statik Kural

**Süre:** 3 gün · **Dal:** `faz/6-kurallar` · **Mimari:** §5.3.3, §8

**Amaç:** Kayıt defterli kural motoru ve §8.2'deki tüm statik kurallar, her biri fixture'larla.

> **Daraltılmış kapsam (2026-09-29, kullanıcı onaylı):** Bu fazda motor + 10 yüksek değerli kural
> uygulandı (C-BUF-001, C-MEM-001, CPP-OWN-001, CS-ALLOC-001, CS-PERF-001, UNITY-GC-001,
> UNITY-PERF-001, UNITY-EVT-001, UE-GC-001, UE-PERF-001). Kalan 10 statik kural (C-IO-001,
> C-UB-001, C-MEM-002, C-MEM-003, C-PERF-001, CPP-SP-001, CPP-PERF-001, CS-ALLOC-002,
> UNITY-PERF-002, UE-MEM-001) uçtan uca akış (Faz 7–10) bittikten sonra eklenecek; motor ve
> fixture düzeni değişmeden kural eklemeye hazır. Kabul kriterlerindeki "20 kural" buna göre okunur.

**Çıktılar**
- `rules/base.py` (`Rule`, `RuleContext`, `finding()` yardımcısı), `rules/registry.py` (`@register_rule`)
- `rules/{c,cpp,csharp,unity,unreal}.py`
- `tests/rules/fixtures/{RULE_ID}/{positive,negative}/` — kural başına ≥2 + ≥2
- `tests/rules/test_all_rules.py` — fixture dizinlerini otomatik tarayan parametrik test
- CLI: `codementor rules list [--engine]`, `make rules-doc` → `docs/rules-catalog.md`

**Kabul kriterleri**
- [ ] §8.2'de "Statik" veya "Statik + LLM" olan 20 kuralın tamamı uygulanmış
- [ ] Her kural için ≥2 pozitif, ≥2 negatif fixture; hepsi geçiyor
- [ ] Pozitif fixture'larda bulgu satırı beklenen satırla birebir (fixture dosyasında `// EXPECT: line` yorumu)
- [ ] Kural dil/motor filtresi çalışıyor (Unity kuralı düz C#'ta çalışmıyor)
- [ ] Kurallar yapılandırmadan tek tek devre dışı bırakılabiliyor
- [ ] `docs/rules-catalog.md` otomatik üretiliyor

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 6'yı uygula. Mimari §5.3.3'teki Rule arayüzü ve
§8.2'deki kural tablosu. Kurallar Faz 5'in StaticFacts'ini kullanır; ağaca
yalnızca olgularda olmayan bilgi için in. Her kural için fixture klasörü aç;
pozitif fixture'larda beklenen satırı "// EXPECT: <satır>" yorumuyla işaretle
ve parametrik test bunu okusun. Negatif fixture'lar "neredeyse ihlal" olsun
(ör. UNITY-GC-001 için Start() içinde new: sıcak yol değil, bulgu yok).
Önce motoru ve 3 kuralı yaz, onayımı al, sonra kalan 17'yi yaz.
```

**Claude Code'da:** Kalan 17 kural için ajana dil başına bir mesaj ver ("şimdi C kurallarını yaz"). Her grup sonrası `make check`. Negatif fixture'ların gerçekten "yakın ıskalama" olduğunu kendin kontrol et; bu, yanlış pozitif oranını belirler.

**Antigravity CLI'da:** Bu faz, iki aracı birlikte kullanmak için ideal: kuralları Antigravity'de yazdırıp fixture kalitesini Claude Code'daki `kod-denetci` ile denetletebilirsin (veya tersi).

**Doğrulama**
```bash
make check
uv run pytest tests/rules -v
uv run codementor rules list --engine unity
make rules-doc && head -40 docs/rules-catalog.md
```

**Tuzaklar:** `C-MEM-001` (malloc/free eşleşmesi) fonksiyon içi sınırlıdır; ajan fonksiyonlar arası analiz yazmaya kalkmasın. `UNITY-EVT-001` için lambda aboneliklerin (`+= () => ...`) çıkarılamayacağını da ayrı bulgu olarak işaretlemek güzel bir detay.

**Commit:** `feat(faz-6): kural motoru ve 20 statik kural (fixture'larla)`

---

### Faz 7 — Sağlayıcı Adaptörleri

**Süre:** 2.5 gün · **Dal:** `faz/7-saglayicilar` · **Mimari:** §5.5 · *(Faz 3–6 ile paralel yapılabilir)*

**Amaç:** Tek arayüz arkasında Fake, Ollama, OpenAI, DeepSeek ve Anthropic; sağlayıcıya özel yapılandırılmış çıktı.

**Çıktılar**
- `providers/base.py` (`LLMProvider` Protocol, `ProviderCapabilities`, `ProviderResult`, `TokenUsage`, hata sınıfları)
- `providers/schema_adapter.py` (katı mod varyantı, `$ref` açma, desteklenmeyen anahtar temizleme)
- `providers/fake.py` (fixture'dan yanıt; hata/bozuk JSON/gecikme simülasyonu)
- `providers/ollama.py`, `providers/openai_compat.py` (OpenAI + DeepSeek), `providers/anthropic.py`
- `providers/factory.py` (config → sağlayıcı; fallback zinciri)
- `tests/providers/contract.py` — **tüm adaptörlerin geçtiği ortak sözleşme test paketi** (respx ile HTTP mock)
- `tests/live/test_providers_live.py` (`@pytest.mark.live`; sahte anahtar fikstürlerinden ayrı dizin)
- CLI: `codementor providers check`

**Kabul kriterleri**
- [ ] Tüm adaptörler aynı sözleşme testlerini geçiyor (mock HTTP)
- [ ] Ollama isteğinde `format` = JSON Schema ve `options.num_ctx` her zaman gönderiliyor
- [ ] OpenAI katı mod şeması: tüm alanlar `required`, `additionalProperties: false` (şema testi)
- [ ] Anthropic: `output_config.format.schema` = şema; araç/`tool_choice` yok (ADR-0011 — güncel modeller zorunlu `tool_choice`'u reddediyor)
- [ ] Yeniden deneme yalnızca ağ/429/5xx'te; 4xx'te hemen hata (testle)
- [ ] Fallback zinciri çalışıyor ve rapora uyarı yazılacak bilgi dönüyor
- [ ] API anahtarı hiçbir log satırında görünmüyor (log yakalama testi)
- [ ] `codementor providers check` yerel Ollama'yı gerçekten sorguluyor

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 7'yi uygula. Mimari §5.5. Resmi SDK yerine httpx
kullan (tek bağımlılık, kolay mock). Her sağlayıcının güncel yapılandırılmış
çıktı API'sini uygulamaya başlamadan önce resmi dokümandan doğrula ve
kararını PROGRESS.md'ye kaynak linkiyle yaz. Sözleşme test paketini bir kez
yaz, her adaptör için parametrik çalıştır. SchemaAdapter tek Pydantic
modelinden sağlayıcı varyantları üretsin. Model adları yalnızca config'den.
Log'larda Authorization başlığını ve api_key alanlarını redakte eden bir
structlog işlemcisi ekle ve test et.
```

**Claude Code'da:** Web erişimi varsa ajana sağlayıcı dokümanlarını okut ve kararlarını linkle kaydettir. Canlı testler için `.env`'yi sen doldur; ajanın `.env` okuması `settings.json`'da engelli.

**Antigravity CLI'da:** Aynı şekilde güncel API dokümantasyonunu doğrulat. Anthropic ve OpenAI adaptörlerini farklı bir model ailesinin yazması, sözleşme testlerini daha tarafsız yapar.

**Doğrulama**
```bash
make check
uv run pytest tests/providers -v
uv run codementor providers check
uv run pytest -m live -k ollama -v     # yerel Ollama açıkken
```

**Tuzaklar:** Ollama'nın varsayılan bağlam penceresi küçüktür; `num_ctx` gönderilmezse uzun prompt sessizce kırpılır ve saatlerce "model neden saçmalıyor" diye aranırsın. OpenAI katı modda opsiyonel alanlar `null` birliği ile zorunlu yapılmalı.

**Commit:** `feat(faz-7): sağlayıcı bağımsız LLM adaptörleri ve sözleşme testleri`

---

### Faz 8 — Prompt Orkestrasyonu

**Süre:** 2 gün · **Dal:** `faz/8-promptlar` · **Mimari:** §5.4

**Amaç:** Olgular, kurallar, soru ve kontrol listesinden sürümlü, bütçeli, iki geçişli prompt'lar üretmek.

**Çıktılar**
- `prompts/v1/analysis.system.j2`, `analysis.user.j2`, `socratic.system.j2`, `socratic.user.j2`, `repair.user.j2`
- `prompts/v1/fewshots/*.yaml` (dil/motor başına 1–2 örnek)
- `prompts/builder.py` (`build_analysis_messages`, `build_socratic_messages`, `build_repair_messages`)
- `prompts/budget.py` (§5.4.5 öncelik sırasıyla kırpma; kod asla kırpılmaz)
- `prompts/fewshot.py`
- `prompt_version` hesaplama
- Snapshot testleri: sabit girdiden üretilen prompt metni (`tests/golden/prompts/`)

**Kabul kriterleri**
- [ ] Kod her zaman `<user_code>` sınırlayıcıları içinde ve numaralı görünümde
- [ ] Sistem prompt'u §5.4.4'teki tüm çekirdek kuralları içeriyor (testte anahtar ifade kontrolü)
- [ ] Referans çözüm hiçbir prompt'ta yok (testle: çözüm dosyasındaki benzersiz bir satır prompt'ta aranıyor)
- [ ] Bütçe aşımında few-shot → kontrol listesi → olgular sırasıyla kırpılıyor; kod sığmıyorsa istisna
- [ ] Zorluk → ipucu seviyesi tablosu (§5.4.3) uygulanıyor
- [ ] Şablon değişince `prompt_version` değişiyor
- [ ] `single_pass` modu da destekleniyor

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 8'i uygula. Mimari §5.4. Şablonlar Jinja2, repo
kökündeki prompts/v1/ altında; Python koduna prompt metni gömme. Sistem
prompt'unda §5.4.4'teki çekirdek kuralların hepsi olsun. Statik bulgular
prompt'a "zaten bulundu, tekrarlama, açıkla ve eksikleri tamamla" çerçevesiyle
girsin. StaticFacts'i tam JSON olarak değil, token bütçesine göre sıkıştırılmış
okunabilir bir özet olarak ver. Token sayımı için sağlayıcıdan bağımsız
yaklaşık sayıcı kullan. Snapshot testleri ekle.
```

**Claude Code'da:** Prompt metinleri üzerinde birlikte çalış; ajanın ilk taslağını oku ve kendi sözcüklerinle düzelt. Mülakatta prompt tasarımını sen anlatacaksın.

**Antigravity CLI'da:** Farklı model ailesinden gelen bir ajanın prompt'u yazması faydalı olabilir: modeller kendi ailelerinin tercih ettiği kalıplara yatkındır. Eval'de (Faz 12) iki taslağı karşılaştırabilirsin.

**Doğrulama**
```bash
make check
uv run pytest tests/golden/prompts -v
uv run python -m codementor.prompts.builder --demo unity-hard-inventory   # üretilen prompt'u yazdır
```

**Tuzaklar:** Kontrol listesi ve few-shot'lar kolayca 3000+ token olur; küçük yerel modellerde kaliteyi düşürür. Bütçeyi sağlayıcı config'inden al, sabit yazma.

**Commit:** `feat(faz-8): sürümlü iki geçişli prompt orkestrasyonu ve token bütçesi`

---

### Faz 9 — Doğrulayıcı, Uzlaştırma ve Sızıntı Koruması

**Süre:** 2.5 gün · **Dal:** `faz/9-dogrulayici` · **Mimari:** §5.6

**Amaç:** LLM çıktısının her iddiasını doğrulamak, statik bulgularla birleştirmek, çözüm sızıntısını engellemek.

**Çıktılar**
- `verify/schema_check.py` (Pydantic + onarım için okunabilir hata özeti)
- `verify/lines.py` (aralık + ±2 penceresinde boşluk-duyarsız kanıt arama + satır düzeltme)
- `verify/complexity.py` (normalizasyon, ipucu çatışması, `is_optimal` hesabı)
- `verify/merge.py` (kategori + satır ≤2 → `confirmed`; statik önem önceliği)
- `verify/leak_guard.py` (kod benzeri satır tespiti, 5-gram örtüşme, yasaklı tanımlayıcılar)
- `verify/confidence.py` (§5.6 formülü)
- Halüsinasyon fixture'ları: yanlış satır, var olmayan kanıt, `O(n)` iddiası + `n^2` ipucu (gerekçesiz / gerekçeli), çözüm sızdıran Sokratik yanıt, kod bloğu içeren soru

**Kabul kriterleri**
- [ ] §5.6 tablosundaki her kontrol için pozitif ve negatif test
- [ ] Kanıtı 1 satır kaymış bulgu düzeltiliyor; kanıtı hiç olmayan atılıyor + uyarı
- [ ] Gerekçesiz çatışma → onarım talebi; gerekçeli çatışma → kabul + düşük güven
- [ ] Statik ve LLM aynı sorunu bulunca tek `confirmed` bulgu
- [ ] Sızıntı: kod bloğu, referansla yüksek 5-gram örtüşmesi ve yasaklı tanımlayıcı ayrı ayrı yakalanıyor
- [ ] Güven skoru 0–1 aralığında ve formüle uygun (hypothesis ile)

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 9'u uygula. Mimari §5.6 tablosu bu fazın spesifikasyonu;
her satırı ayrı fonksiyon ve ayrı testle uygula. Doğrulayıcılar saf fonksiyon
olsun (LLM çağrısı yok); onarım kararını döndürsünler, onarımı pipeline
(Faz 10) yapacak. Sızıntı korumasında yasaklı tanımlayıcı listesi: referans
çözümde geçen ama kullanıcı kodunda geçmeyen tanımlayıcılar; std/BCL genel
adlarını (int, List, std) hariç tut. Halüsinasyon fixture'larını
tests/fixtures/llm_responses/ altında gerçekçi JSON yanıtlar olarak yaz.
```

**Claude Code'da:** Halüsinasyon fixture'ları için Faz 7'de canlı Ollama'dan birkaç gerçek yanıt kaydettiysen onları kullan; uydurulmuş fixture'lardan daha değerlidir.

**Antigravity CLI'da:** Sızıntı korumasının eşik değerlerini (5-gram oranı) sabit kodlamasın, config'e alsın; Faz 12'de eval ile ayarlanacak.

**Doğrulama**
```bash
make check
uv run pytest tests/unit/verify -v
```

**Tuzaklar:** Boşluk-duyarsız eşleşme yaparken C#'ta `var x=new List<int>()` ile `var x = new List<int>();` eşleşmeli; noktalı virgül ve boşluk normalizasyonunu test et. Leak guard aşırı hassas olursa her soruyu atar; negatif fixture'lar bunu önler.

**Commit:** `feat(faz-9): LLM çıktı doğrulayıcısı, bulgu birleştirme ve sızıntı koruması`

---

### Faz 10 — Pipeline, CLI ve Depolama

**Süre:** 2.5 gün · **Dal:** `faz/10-pipeline` · **Mimari:** §4, §10, §11, §5.7 (CLI/MD/SARIF)

**Amaç:** Tüm katmanları uçtan uca bağlamak; kullanılabilir ilk ürün (CLI).

**Çıktılar**
- `pipeline/orchestrator.py` (§4 akışı, onarım döngüsü, zarif bozulma, erken çıkış şablon mesajları)
- `pipeline/events.py` (`StageEvent` + abonelik)
- `storage/db.py`, `cache.py`, `sessions.py` (§11 tabloları, önbellek anahtarı, ipucu merdiveni)
- `report/cli_render.py` (Rich), `markdown.py`, `sarif.py`
- CLI: `codementor analyze` tam seçeneklerle; çıkış kodları §10
- Uçtan uca testler (FakeProvider): mutlu yol, erken çıkış, onarım başarılı, onarım başarısız → bozulma, önbellek isabeti, ipucu seviyesi artışı

**Kabul kriterleri**
- [ ] Erken çıkışta sağlayıcı **hiç çağrılmıyor** (FakeProvider çağrı sayacı = 0)
- [ ] Onarım en fazla `max_repair_attempts` kez
- [ ] Bozulmada rapor dönüyor, `degraded=true`, Sokratik bölüm şablondan
- [ ] Aynı istek ikinci kez → `cache_hit=true`, sağlayıcı çağrılmıyor
- [ ] Aynı oturum + soru ile 3. gönderimde `hint_level=3`
- [ ] SARIF çıktısı resmi SARIF 2.1.0 şemasıyla doğrulanıyor
- [ ] `meta.stage_latency_ms` tüm aşamaları içeriyor
- [ ] Gerçek Ollama ile manuel demo çalışıyor

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 10'u uygula. Mimari §4 yaşam döngüsü tablosu
orkestratörün spesifikasyonu. Orkestratör katman modüllerini çağırır, iş
mantığı içermez. Her aşamayı StageEvent ile yayınla. Erken çıkış mesajları
§5.2.4'teki gibi LLM'siz şablonlardan üretilsin. Depolama SQLModel + SQLite,
önbellek anahtarı §11'deki alanların tamamını içersin. Rich çıktısında
bulguları kod satırı vurgusuyla göster. SARIF'i resmi şemaya karşı doğrulayan
bir test ekle (şema dosyasını tests/fixtures'a koy).
```

**Claude Code'da:** İlk gerçek demo bu fazda. Faz bitince kendin çalıştır ve ekran görüntüsü al; README ve portföy için lazım olacak.

**Antigravity CLI'da:** Uçtan uca testlerin FakeProvider ile ağsız çalıştığını görev listesinde ayrı madde olarak doğrulat.

**Doğrulama**
```bash
make check
uv run codementor analyze tests/golden/facts/unity-01/code.cs --engine unity --question unity-hard-inventory --provider ollama
uv run codementor analyze broken.c --language c; echo "çıkış: $?"   # 2 beklenir
uv run codementor analyze x.cpp --format sarif > out.sarif
```

**Tuzaklar:** Orkestratör şişmeye meyillidir; 250 satırı geçerse aşamaları `stages.py`'ye böl. Async/sync karışıklığı: sağlayıcılar async, CLI senkron; CLI'da `asyncio.run` tek noktada olsun.

**Commit:** `feat(faz-10): uçtan uca pipeline, CLI, önbellek ve SARIF çıktısı`

---

### Faz 11 — REST API ve SSE

**Süre:** 1.5 gün · **Dal:** `faz/11-api` · **Mimari:** §9

**Amaç:** Pipeline'ı FastAPI üzerinden sunmak; aşama ilerlemesini SSE ile akıtmak.

**Çıktılar**
- `api/app.py` (uygulama fabrikası, CORS yalnızca yerel web UI kökenine), `api/routes.py`, `api/sse.py`, `api/errors.py` (RFC 7807)
- §9'daki tüm uç noktalar
- `codementor serve`
- Testler: `httpx.AsyncClient` ile tüm uç noktalar + SSE olay sırası

**Kabul kriterleri**
- [ ] §9 tablosundaki her uç nokta çalışıyor ve testli
- [ ] `/v1/questions/{id}` referans çözüm yolu döndürmüyor
- [ ] Hata yanıtları `application/problem+json`
- [ ] SSE: `stage` olayları doğru sırada, son olay `report`
- [ ] Varsayılan bağlama `127.0.0.1`
- [ ] OpenAPI dokümanı `/docs`'ta, örnek istek/yanıtlar dolu

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 11'i uygula. Mimari §9. Rotalar ince olsun; tüm iş
Faz 10'daki orkestratörde. SSE için orkestratörün StageEvent aboneliğini
kullan. Hataları RFC 7807 problem+json biçiminde döndür. CORS yalnızca
config'deki web UI kökenine açık. OpenAPI şemasında istek/yanıt örnekleri
(§9'daki JSON'lar) görünsün.
```

**Claude Code'da / Antigravity CLI'da:** Kısa ve kalıplaşmış bir faz; iki araçta da `/faz 11` yeterli. Bittiğinde `curl` ile SSE akışını kendin izle.

**Doğrulama**
```bash
make check
uv run codementor serve &
curl -s localhost:8000/health
curl -N -X POST localhost:8000/v1/analyze/stream -H 'content-type: application/json' \
  -d '{"code":"int main(){return 0;}","language":"c","engine":"none","provider":"ollama"}'
```

**Tuzaklar:** SSE yanıtında proxy tamponlaması; `Cache-Control: no-cache` ve `X-Accel-Buffering: no` başlıklarını ekle.

**Commit:** `feat(faz-11): FastAPI REST API ve SSE ilerleme akışı`

---

### Faz 12 — Eval Altyapısı ve Veri Seti

**Süre:** 4 gün · **Dal:** `faz/12-eval` · **Mimari:** §14, §13 (tasarruf ölçümü), §23

**Amaç:** CV'deki her sayının kaynağı. Veri seti + metrikler + karşılaştırma + ablasyon.

**Çıktılar**
- `eval/dataset.py`, `eval/metrics.py` (§14.2 tümü), `eval/runner.py`, `eval/compare.py`
- `eval/dataset/dev/` (30) ve `eval/dataset/test/` (50) örnek: §14.1 dağılımı
- `private/solutions/` (sızıntı ölçümü için referans çözümler; repoya girmez)
- CLI: `codementor eval run`, `codementor eval compare`
- `--static-only` modu (LLM'siz taban çizgisi)
- `--ablate facts|line_numbers|fewshot` bayrakları
- `docs/eval-findings.md` (sonuçlar, ablasyonlar, kararlar; ADR-0003 güncellemesi)

**Kabul kriterleri**
- [ ] 80 örnek, etiketleri elle kontrol edilmiş (her etiketi kendin gözden geçir)
- [ ] Metrik fonksiyonlarının kendi birim testleri var (bilinen girdi → bilinen skor)
- [ ] Eval'de önbellek kapalı
- [ ] Sonuç dosyası: tüm metrikler + sürüm bilgileri (prompt/kural/şema/model)
- [ ] En az 3 satırlı karşılaştırma tablosu: statik-only, yerel model two_pass, yerel model single_pass
- [ ] En az 2 ablasyon sonucu raporlanmış
- [ ] Prompt ayarlaması yalnızca `dev` ile yapıldı; `test` sonuçları en sonda bir kez alındı
- [ ] ADR-0003 (iki geçiş) ölçümle güncellendi

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 12'yi uygula. Mimari §14. Önce altyapıyı yaz
(dataset yükleyici, metrikler + birim testleri, runner, compare, static-only
ve ablasyon bayrakları). Sonra veri seti için ÖNERİ üret: her örnek için kod
ve label.yaml taslağı. Etiketleri ben kontrol edeceğim; kontrol edilmemiş
örnekleri eval/dataset/_draft/ altında tut. Veri setinde §14.1 dağılımına
uy: ~%25 sözdizimi hatalı, ~%10 prompt injection içeren. Metrik eşleşme
kuralı: aynı kategori ve satır farkı ≤ 2.
```

**Claude Code'da:** Veri seti taslaklarını küçük gruplar halinde (dil başına) ürettir, her grubu kendin gözden geçir, `_draft/`'tan taşı. Uzun eval koşuları için `claude -p` yerine doğrudan `uv run codementor eval run` kullan; ajan bağlamını harcama.

**Antigravity CLI'da:** Antigravity'nin eşzamansız çoklu ajan özelliği varsa veri seti taslaklarını dil bazında paralel ürettirebilirsin. Yine de her etiketi sen onayla.

**Doğrulama**
```bash
make check
uv run codementor eval run --split dev --static-only
uv run codementor eval run --split dev --provider ollama --mode two_pass
uv run codementor eval run --split dev --provider ollama --mode single_pass
uv run codementor eval compare eval/results/*.json
# en sonda, bir kez:
uv run codementor eval run --split test --provider ollama --mode two_pass
```

**Tuzaklar:** **Etiketleri ajana yazdırıp kontrol etmemek bu projenin en büyük riski.** Yanlış etiket, sahte doğruluk üretir ve mülakatta çöker. Test setine bakarak prompt ayarlamak da aynı şekilde sonuçları geçersiz kılar.

**Commit:** `feat(faz-12): eval altyapısı, 80 örneklik veri seti ve ilk sonuçlar`

---

### Faz 13 — Web UI, Kurulum ve Dokümantasyon

**Süre:** 3 gün · **Dal:** `faz/13-sunum` · **Mimari:** §5.7, §18, §23

**Amaç:** Portföye hazır ürün: web arayüzü, tek komutla kurulum, güçlü README.

**Çıktılar**
- `web/` (Vite + React + TS): Monaco editör, dil/motor/soru seçimi, SSE ilerleme göstergesi, satır işaretleri, bulgu listesi, Sokratik panel, "sonraki ipucu" düğmesi, karmaşıklık kartı (gerekçe adımları ve güven)
- `web/src/types/` → `schemas/`'tan otomatik üretilen tipler
- Docker'sız hızlı başlangıç: `uv sync` + `codementor serve` + `npm run dev` (§18)
- Opsiyonel paketleme: `Dockerfile` (API), `web/Dockerfile`, `docker-compose.yml` (§18.1; hiçbir özellik ona bağlı değil)
- `README.md`: GIF demo, mimari diyagram, hızlı başlangıç, eval tablosu, sınırlamalar
- `docs/adr/0001…0008` tamamlanmış
- CV maddeleri (§23.1) gerçek sayılarla doldurulmuş

**Kabul kriterleri**
- [ ] Docker'sız hızlı başlangıç temiz makinede çalışıyor (Ollama modeli indirme adımı README'de); `docker compose up` yalnızca opsiyonel yol
- [ ] Web UI'da analiz uçtan uca çalışıyor; bulgu satırları editörde işaretli
- [ ] Tipler elle yazılmamış, şemadan üretilmiş
- [ ] Mobil genişlikte kullanılabilir
- [ ] README'deki eval tablosu `eval/results/`'taki gerçek dosyayla birebir
- [ ] README'de "Sınırlamalar" bölümü dürüst (ör. Unreal için yalnızca stub derleme)

**Görev metni**
```
docs/UYGULAMA_PLANI.md Faz 13'ü uygula. Önce Web UI: mimari §5.7. Tipleri
schemas/*.schema.json'dan json-schema-to-typescript ile üret. SSE ile aşama
ilerlemesini göster. Monaco'da bulgu satırlarını önem derecesine göre işaretle.
Sonra kurulum: §18 (Docker'sız varsayılan; §18.1 opsiyonel). En son README: kısa tanıtım, mimari diyagram (mermaid),
hızlı başlangıç, eval sonuç tablosu (eval/results'tan), sınırlamalar, yol
haritası. README'de ölçülmemiş hiçbir sayı olmasın.
```

**Claude Code'da:** UI görsel doğrulaması için Playwright MCP gibi bir tarayıcı aracı bağlıysa ajana ekran görüntüsü aldırıp kontrol ettirebilirsin; yoksa kendin tarayıcıda test et.

**Antigravity CLI'da:** Antigravity'nin masaüstü sürümündeki tarayıcı doğrulama özelliği UI fazı için güçlüdür; CLI'da yoksa aynı dalı masaüstü uygulamasında açıp doğrulatabilirsin.

**Doğrulama**
```bash
make check
cd web && npm run build && npm run typecheck
uv run codementor serve &   # ve: cd web && npm run dev
# tarayıcı: http://127.0.0.1:5173
# opsiyonel: docker compose up --build
```

**Tuzaklar:** UI'da kapsam kayması çok kolaydır (tema, animasyon, hesaplar). Kabul kriterlerine sadık kal; güzelleştirme v1.1.

**Commit:** `feat(faz-13): web arayüzü, kurulum ve portföy dokümantasyonu`

---

## 7. PROGRESS.md Şablonu

````markdown
# İlerleme Günlüğü

## Durum
| Faz | Durum | Dal | Tarih | Araç (uygulayan / denetleyen) |
|---|---|---|---|---|
| 0 | ✅ | faz/0-iskelet | 2026-10-01 | Claude Code / Antigravity |
| 1 | 🔄 | faz/1-modeller | | |
| 2 | ⏳ | | | |

## Faz N — Notlar
**Yapılanlar:**
**Alınan kararlar (ve neden):**
**Mimariden sapmalar (ADR linki):**
**Açık sorular:**
**Bu fazda öğrendiğim:** (2 cümle — mülakat hazırlığı)

## Sonraya (kapsam dışı fikirler)
-
````

---

## 8. Sorun Giderme

| Belirti | Olası neden | Çözüm |
|---|---|---|
| Ajan fazın dışındaki dosyaları değiştiriyor | Görev metni belirsiz / bağlam eski | `/clear`, görevi yeniden ver; plan aşamasında dosya listesini kontrol et |
| Ajan `AGENTS.md` kurallarını görmezden geliyor | Dosya yüklenmemiş | Claude Code: `CLAUDE.md` içinde `@AGENTS.md` satırını kontrol et. Antigravity: "Hangi kurallar yüklü?" diye sor |
| `/faz` komutu görünmüyor | Yanlış konum | Claude Code: `.claude/commands/faz.md`. Antigravity: `.agents/workflows/faz.md` (tekil `.agent/` değil) |
| Ollama yanıtları anlamsız / şemaya uymuyor | `num_ctx` gönderilmiyor, prompt kırpılıyor | Faz 7 kabul kriterini kontrol et; Ollama loglarında "truncating" uyarısı ara |
| tree-sitter `Language` hatası | Bağlama sürümü uyumsuzluğu | `uv.lock`'taki sürümün dokümanına göre API'yi güncelle |
| `compiler` testleri atlanıyor | Makinede gcc/clang/dotnet yok | Beklenen davranış (ADR-0009); gerekiyorsa derleyiciyi kur. CI runner'ında gcc/clang hazır gelir |
| Eval sonuçları "fazla iyi" | Test setine göre ayar, önbellek açık, yanlış etiket | Önbelleği kapat, etiketleri yeniden gözden geçir, dev/test ayrımını kontrol et |
| Bağlam penceresi doluyor | Faz çok büyük | Fazı alt kilometre taşlarına böl; Claude Code'da `/compact`, Antigravity'de yeni oturum + PROGRESS.md |

---

## 9. Zaman Çizelgesi

| Hafta | Fazlar | Kilometre taşı |
|---|---|---|
| 1 | 0, 1, 2, 3 | Modeller ve Tier 0 hazır |
| 2 | 4, 5 (+ paralel 7 başlangıcı) | Tier 1 yerel derleyici ve olgu çıkarımı |
| 3 | 6, 7 | Kurallar ve sağlayıcılar |
| 4 | 8, 9, 10 | **İlk uçtan uca CLI demosu** |
| 5 | 11, 12 | API + eval sonuçları (CV sayıları) |
| 6 | 13 | Web UI, kurulum, README, portföy |
| 7 | Tampon | Hata düzeltme, mülakat provası |

**Minimum uygulanabilir sürüm (zaman darsa):** Faz 0–3, 5, 6 (yalnızca C ve Unity kuralları), 7 (yalnızca Fake + Ollama), 8–10, 12 (40 örnek). Bu kesit bile CV'deki hibrit mimari iddiasını dürüstçe taşır.
