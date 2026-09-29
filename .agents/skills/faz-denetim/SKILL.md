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
