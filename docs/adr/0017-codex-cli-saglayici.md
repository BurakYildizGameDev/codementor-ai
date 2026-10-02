# ADR-0017: OpenAI Codex CLI sağlayıcı olarak

**Tarih:** 2026-10-02 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §5.5.2, §12; ADR-0012, ADR-0014

## Bağlam

Kullanıcıda API anahtarı yok; ChatGPT aboneliği ve oturum açılmış `codex` CLI'ı (0.157) var.
ADR-0012 yalnızca Claude Code ve Antigravity'yi kapsıyordu. Canlı denemeler (2026-10-02):

- `codex --no-daemon exec --json --output-schema <dosya> -` stdin'den prompt alır; çıktı JSONL
  olay akışıdır: `item.completed` / `agent_message` (yanıt metni), `turn.completed` (`usage`),
  hata için `turn.failed` / `error`. Öğe düzeyinde `error` türü bilgilendirme uyarılarıdır
  (ör. tanınmayan ayar).
- Şema dosyadan verilir ve OpenAI katı biçimini ister (`additionalProperties: false`, tüm
  alanlar `required`).
- Kullanıcı `~/.codex/config.toml`'undaki MCP sunucuları her çalıştırmada yükleniyor;
  `--ignore-user-config` bunu kapatır, kimlik `CODEX_HOME`'dan okunmaya devam eder.
- Araçları kapatan bir bayrak yok. En kısıtlı mod `--sandbox read-only`: komut çalıştırabilir,
  dosya okuyabilir, yazamaz.
- `codex debug models` hesabın görebildiği model kataloğunu verir, ama katalogda listelenen her
  model hesaba açık değil (`gpt-5.5` 404 döndü; `gpt-6-luna`, `gpt-5.6-terra`, `gpt-5.6-luna`
  çalıştı). Uçtan uca bir analiz (`c-012`, `gpt-6-luna`) 14,6 sn sürdü; çağrı başına ~15 bin
  token Codex'in kendi sistem prompt'u.

## Karar

1. `providers/codex_cli.py` → `CodexCliProvider` (`[providers.codex]`: `command`, `model`,
   `timeout_s`, `allow_tool_agent`).
2. ADR-0012'nin güvenlik kuralları aynen: mesajlar yalnızca stdin'den, mutlak çalıştırılabilir
   yolu, Faz 4 çalıştırıcısı (izin listeli ortam, süreç ağacı öldürme, çıktı sınırı).
3. Sabit argv: `--no-daemon exec --sandbox read-only --ephemeral --skip-git-repo-check
   --ignore-user-config --ignore-rules --json --color never --output-schema <geçici>/schema.json
   --cd <geçici> --model <model> -`. Geçici dizin her çağrıda yeni ve yalnızca şema dosyasını
   içerir; çağrıdan sonra silinir.
4. Dosya okuyabilen bir ajan olduğu için agy gibi **açık onay** gerekir:
   `allow_tool_agent = true` (masaüstünde Bağlantılar kartındaki anahtar). Varsayılan kapalı.
5. Hata sınıflandırması: kullanım/hız sınırı → yeniden denenmeyen hız sınırı hatası (ChatGPT
   planı saatlerce sürer); oturum yok → `codex login` önerisi; diğerleri maskelenmiş kısa metin.
6. Model seçimi zorunlu (ADR-0008); Bağlantılar ekranı `codex debug models` listesini öneri
   olarak gösterir, erişilemeyen model seçilirse hata metni bunu söyler.

## Sonuçlar

- API anahtarı olmadan ikinci bir model ailesi (OpenAI) kullanılabilir ve eval'de ölçülebilir
  (Faz 34).
- Risk: öğrenci kodundaki bir prompt injection Codex'i dosya okumaya yönlendirebilir; okunan
  içerik rapora yalnızca şemaya uyan alanlarla girer ve rapor yine aynı yerel kullanıcıya
  gösterilir. Paylaşılan sunucuda (API) `allow_tool_agent` kapalı tutulmalı (ADR-0012 ile aynı).
- `--ignore-user-config` kullanıcının Codex model varsayılanını da yok sayar; model her zaman
  `[providers.codex] model`'den gelir.
