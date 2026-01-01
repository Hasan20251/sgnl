<div align="center">

# <span style="font-family: 'Courier New', Courier, monospace; font-weight: 900; font-size: 2.5em; letter-spacing: 8px; text-transform: uppercase; line-height: 1.1;">SGNL</span>
// Sinyal Çıkarma Motoru

**ÇÖP OKUMAYI DURDURUN.**

*Bilgi filtreleme aracı.*

</div>

---

<div align="center">

**🌐 Dil Seçimi / Language Selection**

[🇬🇧 English](README.md) | [🇹🇷 Türkçe](README_TR.md)

</div>

---

## 📖 Bu Nedir? (Kısa Özet)

**SGNL, internetteki yüksek kaliteli içeriği düşük kaliteli gürültüden ayıran akıllı bir filtreleme sistemidir.**

Bir araştırma asistanı gibi düşünün; makaleleri, akademik çalışmaları ve web içeriğini analiz eder ve size şunları söyler:
- Okunmaya değer olan içerikler (sinyal)
- Sadece reklam ve SEO spamı olan içerikler (gürültü)

**3 basit adımda nasıl çalışır:**
1. Bir konu başlığı girin
2. SGNL ilgili içerikleri bulur ve kalite/yoğunluk puanı verir
3. Sadece değerli içerikleri yapay zeka analiziyle birlikte alırsınız

**Kimler için ideal?** Araştırmacılar, geliştiriciler, öğrenciler veya internet'teki bilgi kirliliğinden rahatsız olan herkes.

---

## 🎯 Çalışma Prensibi: Gürültü Filtreleme

İnternette çok fazla içerik var. Bir kısmı değerli, büyük kısmı zaman kaybı.

**SGNL işte tam bu noktada yardımcı oluyor.**

```python
core_principles = {
    "SIGNAL": "Kod benchmark'ları, hakemli araştırmalar, birincil kaynaklar.",
    "NOISE": "Listicle'ler, tık tuzağı başlıkları, yüzeysel içerik.",
    "METHOD": "Filtreleme ve analiz yapıyoruz. Mükemmel değil, ama faydalı olmayı hedefliyoruz."
}
```

---

## 📊 Sinyal Skoru Nasıl Hesaplanır?

SGNL, içerik kalitesini belirlemek için **çok katmanlı puanlama sistemi** kullanır. Bu sistem sezgisel analizi, yoğunluk ölçümü ve yapay zeka değerlendirmesini birleştirir.

### Puanlama Mimarisi

```
┌─────────────────────────────────────────┐
│  Sezgisel Analiz (Hızlı, <100ms)│
│  ───────────────────────────────────  │
│  Kod Yoğunluğu (±0 ila +20)     │
│  Veri Yoğunluğu (±0 ila +15)     │
│  Slop Tespiti (-30 ila +10)       │
│  Affiliate Tespiti (-30)           │
│  Hype Tespiti (-20)                │
│                                      │
│  Son Sezgisel Puan: 0-100          │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  İçerik Yoğunluk Analizi (Hızlı)   │
│  ───────────────────────────────────  │
│  CPIDR Skoru (0.0-1.0)             │
│  DEPID Skoru (0.0-1.0)             │
│  Okunabilirlik Skoru                │
│  Birleşik Yoğunluk (0.0-1.0)          │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  Alan Adı İtibarı                  │
│  ───────────────────────────────────  │
│  Yüksek itibar alanları (+%8 ila +15%)│
│  Nötr alanlar (%0)                │
│  Spam alanları (-)                    │
└─────────────────────────────────────────┘
                  ↓
         SON SİNYAL SKORU (0-100)
```

### 1️⃣ Sezgisel Analiz (Taban Katman)

**Başlangıç Puanı:** 50 (nötr)

| Faktör | Etki | Nasıl Ölçülür |
|--------|--------|-----------------|
| **Kod Yoğunluğu** | +0 ila +20 | `<pre>` ve `<code>` bloklarını sayar. Kod sorgularıyla eşleşen teknik içeriği yükseltir. |
| **Veri Yoğunluğu** | +0 ila +15 | Tablolar (`<table>`) ve yapılandırılmış veriyi tespit eder. Dolaylı içeriği gösterir. |
| **Slop Tespiti** | -30 ila +10 | HTML şişirme oranını analiz eder (metin vs etiketler). Aşırı markup = daha düşük puan. |
| **Affiliate Tespiti** | -30 sabit | Affiliate linkleri, ref ID'leri, sponsorlu içeriği tarar. Anında ceza uygular. |
| **Hype Tespiti** | -20 sabit | Tık tuzağı kelimelerini tespit eder (şok, mucize, sırr, inanılmaz, vb.). |

**Örnek:**
```python
# Kod blokları içeren teknik makale
Taban: 50
+ Kod yoğunluğu: +20 (sorguyla eşleşiyor, 5 kod bloğu var)
+ Veri yoğunluğu: +10 (araştırma tabloları var)
- Slop: -5 (baz HTML şişirmesi)
─────────────────────────────────────────
Son: 75 (İyi kalite)
```

### 2️⃣ İçerik Yoğunluk Analizi

Özel kütüphaneler kullanarak **bilgiyel yoğunluğu** ölçer:

| Metrik | Kaynak | Aralık | Ağırlık |
|---------|---------|--------|--------|
| **CPIDR** | `ideadensity` kütüphanesi | 0.0-1.0 | %50 |
| **DEPID** | `ideadensity` kütüphanesi | 0.0-1.0 | %30 |
| **Okunabilirlik** | `textstat` kütüphanesi | 0.0-1.0 | %20 |

**CPIDR Nasıl Çalışır?**
- Benzersiz fikir birimlerini sayar (isimler, fiiller, kavramlar)
- Leksal yoğunluğunu toplam kelime sayısına karşı ölçer
- Yüksek yoğunluk = bilgi-zengin içerik

**DEPID Nasıl Çalışır?**
- spaCy NLP modelini kullanarak cümle bileşenlerini etiketler
- Cümle başına fikir yoğunluğunu hesaplar
- Daha yüksek yoğunluk = cümle başına daha fazla bilgi

**Birleşik Formül:**
```
Yoğunluk Skoru = (CPIDR × 0.5) + (DEPID × 0.3) + (Okunabilirlik × 0.2)
```

**Eşik Değeri:** `Density < 0.45` olan içerik LLM analizinden atlanır (çok hafif).

### 3️⃣ Alan Adı İtibarı

| Alan Adı Türü | Artış | Örnekler |
|-----------------|-------|-----------|
| **Akademik** | +%15 | arxiv.org, nature.com, science.org |
| **Açık Kaynak** | +%12 | github.com, openai.com, anthropic.com |
| **Araştırma** | +%12 | deepmind.com, distill.pub, huggingface.co |
| **Nötr** | %0 | Bilinmeyen alan adları |
| **Spam** | - | Bilinen spam/affiliate çiftlikleri |

**Örnek:**
```python
# Farklı alan adlarında aynı içerik
Medium.com makale → 65 (nötr alan adı)
arxiv.org makale → 75 (+%15 akademik artış)
```

### 4️⃣ Son Puan Hesaplama

**Adım 1: Sezgisel Skor** (0-100)
```
Taban: 50
+ Kod yoğunluğu (+0 ila +20)
+ Veri yoğunluğu (+0 ila +15)
- Slop (-30 ila +10)
- Affiliate'ler (-30)
- Hype (-20)
─────────────────────────────────
Son: [0, 100] aralığına sıkıştırılır
```

**Adım 2: Alan Adı Artışı Uygula**
```
Son Skor = Sezgisel Skor × (1 + AlanAdıArtışı)
# Örnek: 75 × 1.15 = 86.25 (arxiv.org)
```

**Adım 3: LLM İstihbarat Raporu** (Derin Tarama için)
- GPT-OSS-120B tam içeriği okur
- Anlamsal analiz sağlar
- Temel bulguları çıkarır
- Teknik derinlik puanı atar (sezgisel değerleri geçersiz kılar)

### "Yüksek Sinyal" Nedir?

| Puan Aralığı | Derecelendirme | Özellikleri |
|-------------|---------|-----------------|
| **85-100** | ⭐⭐⭐ İstisnai | Hakemli araştırmalar, kod benchmark'ları, yüksek yoğunluklu akademik makaleler |
| **70-84** | ⭐⭐ Yüksek | Teknik dokümantasyon, iyi yapılandırılmış eğitimler, detaylı rehberler |
| **50-69** | ⭐ İyi | Sağlam içerik, bazı değer, hafif şişirme |
| **30-49** | ⚠️ Orta | Ortalama kalite, aşırı içe dönüş, listicle formatı |
| **0-29** | ❌ Düşük | Tık tuzağı, affiliate spam, düşük bilgi yoğunluğu |

### Neden Bu Yaklaşım?

| Endişe | Çözüm |
|----------|-----------|
| **Hız** | Sezgisel analizler <100ms içinde çalışır, LLM gecikmesi yok |
| **Doğruluk** | Yoğunluk analizi gerçek bilgiyel değeri yakalar |
| **Bağlam** | Alan adı itibarı güven sinyalleri ekler |
| **Derinlik** | LLM üst sonuçlar için anlamsal anlayış sağlar |
| **Şeffaflık** | Her puanın bir nedeni var, kara kutu değil |

---

## ⚡ Sistem Mimarisi
