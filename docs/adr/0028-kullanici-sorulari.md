# ADR-0028: Kullanıcı kendi sorularını ekleyebilir

**Tarih:** 2026-10-13 · **Durum:** Kabul edildi · **Etkilenen bölümler:** mimari §7, §6.4

## Bağlam

Soru bankası (mimari §7) paketle gelen, salt okunur `data/questions/*.yaml` dosyalarından oluşur.
Her soru kavram etiketleri, üç kademeli ipucu ve (C/C++/C#/Python için) hedef karmaşıklık ister;
referans çözüm `private/` altındadır. Kullanıcı kendi ödevini ya da sınav sorusunu bir görev olarak
çalışmak istiyor. Serbest mod (§7.3) bunu kısmen karşılar ama görev metni, kısıtlar ve hedef
karmaşıklık analize girmez, ipucu merdiveni görevden bağımsızdır.

## Karar

1. **Ayrı depo.** Kullanıcı soruları `data.user_questions_dir` altında (varsayılan
   `~/.codementor/questions`, yapılandırılabilir, `config.WRITABLE_PATHS`'te) yerleşik bankayla
   aynı YAML biçiminde durur. Paket verisine yazılmaz (exe'de salt okunur, güncellemede silinir).
   `QuestionBank.load_all` iki kaynağı birleştirir; API, masaüstü, CLI ve orkestratör bunu kullanır.
2. **`origin` alanı.** `QuestionPublic.origin: "builtin" | "user"` (varsayılan `builtin`; eski
   dosyalar değişmez). Kullanıcı sorusunun kimliği `kullanici-` önekiyle başlar; yerleşik
   kimliklerle çakışamaz.
3. **Basit taslak.** Form/CLI girdisi `UserQuestionDraft`: başlık, açıklama, dil, zorluk zorunlu;
   kısıtlar, hedef karmaşıklık (zaman + bellek birlikte), kavram etiketleri ve ipuçları isteğe
   bağlı. Boş bırakılanlar genel değerlerle dolar (`DEFAULT_USER_*`): genel kısıt, `genel` etiketi
   (kontrol listesinden yalnız `core` maddeler), genel ipuçları.
4. **Hedef karmaşıklık kullanıcı sorusunda isteğe bağlı.** Yerleşik sorularda zorunluluk sürer.
   Hedef yoksa `is_optimal` boş kalır (pipeline bu durumu zaten işliyordu: serbest mod).
5. **Referans çözüm yok.** Sızıntı koruması (K5) yalnız soru metnine ve kod içeriğine dayanır;
   `reference_solution_path` her zaman boş.
6. **Hata yalıtımı.** Bozuk ya da `origin: user` taşımayan kullanıcı dosyası atlanır, uyarı
   loglanır/gösterilir; yerleşik banka bundan etkilenmez. Yazım atomiktir (geçici dosya +
   `os.replace`).
7. **Yazma yüzeyi.** Masaüstü formu (ekle/düzenle/sil) ve CLI (`questions add|remove`). Web/API
   salt okunur kalır: yazma uç noktası ayrı bir güvenlik incelemesi gerektirir (kimlik doğrulama,
   dosya sistemi, §12).
8. **`questions validate` yalnız yerleşik bankayı denetler** (dağılım ve referans çözüm kuralları
   kullanıcı sorularına uygulanmaz).

## Sonuçlar

- Önbellek imzası soru içeriğini içerdiği için (Faz B, O3) soru düzenlenince eski rapor dönmez.
- Genel ipuçları yerleşik sorulardaki kadar hedefli değildir; mentor kalitesi kullanıcının
  verdiği ipucu ve etiketlere bağlıdır. Form bunları isteğe bağlı olarak sunar.
- Eval veri seti ve ölçümler yalnız yerleşik bankayı kullanır; kullanıcı soruları ölçülmez.
