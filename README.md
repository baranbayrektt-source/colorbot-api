# 🎯 ColorBot Pro - Gelişmiş Renk Tabanlı Nişan Yardımcısı

Profesyonel seviyede geliştirilmiş, ekran görüntüsü analizi yapan renk tabanlı nişan yardımcısı. Basit konsol arayüzü ile güçlü özellikler.

## ⚠️ UYARI

Bu yazılım **yalnızca eğitim amaçlıdır**. Kullanımından doğan sorumluluk tamamen kullanıcıya aittir.

## ✨ Pro Özellikler

- 🎯 **FOV Sistemi** - Ayarlanabilir görüş alanı (50-500 piksel)
- 🔄 **Adaptive Smooth** - Mesafeye göre otomatik smooth ayarı
- 🎮 **Gelişmiş Tuş Sistemi** - Gerçek zamanlı tuş yakalama ve atama
- ⚙️ **Hold/Toggle Modları** - Basılı tutma veya aç/kapat seçenekleri
- 📊 **Akıllı Hedef Seçimi** - Mesafe + güvenilirlik skorlaması
- 🎨 **HSV Renk Sistemi** - Gelişmiş renk algılama
- 🖱️ **Smooth Nişan Alma** - Doğal hareket algoritması

## 🚀 Hızlı Başlangıç

### Kurulum
```bash
# Otomatik kurulum (Önerilen)
run_colorbot.bat

# Manuel kurulum
pip install -r requirements.txt
python main.py
```

### İlk Kullanım
1. **Programı başlat**: `run_colorbot.bat`
2. **Ayarları kontrol et**: Menüden `1` (settings)
3. **Tuşları ayarla**: Menüden `2` (keys)
4. **Test et**: Menüden `4` (toggle)

## ⚙️ Ana Ayarlar

### FOV (Görüş Alanı)
- **Düşük FOV (50-100)**: Sadece crosshair yakını, hassas nişan
- **Orta FOV (150-250)**: Dengeli kullanım
- **Yüksek FOV (300-500)**: Geniş alan taraması

### Smooth (Yumuşaklık)
- **Düşük (1.0-5.0)**: Hızlı snap, agresif
- **Orta (5.0-10.0)**: Dengeli, doğal
- **Yüksek (10.0-20.0)**: Çok yumuşak, güvenli

### Hassasiyet
- **0.1-1.0**: Yavaş, hassas kontrol
- **1.0-3.0**: Normal kullanım
- **3.0-5.0**: Hızlı hareket

## 🎮 Kontrol Modları

### Hold Modu (Önerilen)
- Tuşa basılı tuttuğun sürece aktif
- Daha güvenli ve kontrollü
- Ani durma imkanı

### Toggle Modu
- Bir kez bas: aç, tekrar bas: kapat
- Sürekli aktif kalma
- Dikkatli kullanım gerekli

## 🎮 Tuş Atama

### Güvenli Tuşlar
- **F tuşları**: F1, F2, F3, F4, F5, F6
- **Fare**: Sol, Sağ, Orta düğme
- **Harfler**: X, C, V, B, N, M

### Kaçınılacak Tuşlar
- **Sistem tuşları**: Ctrl, Alt, Windows
- **Oyun tuşları**: W, A, S, D, Space
- **Önemli tuşlar**: Enter, Esc, Tab

## 📋 Kullanım Menüsü

```
1. settings  - Ayarları görüntüle/değiştir
2. keys      - Tuş atamalarını değiştir  
3. stats     - İstatistikleri göster
4. toggle    - Nişanı manuel aç/kapat
5. exit      - Programdan çık
```

## 🔧 Performans İpuçları

### Optimum Ayarlar
```
FOV: 200 piksel
Smooth: 6.0
Hassasiyet: 1.5
Mod: Hold
```

### Düşük Performans İçin
```
FOV: 150 piksel  
Smooth: 4.0
Hassasiyet: 1.0
```

### Agresif Kullanım İçin
```
FOV: 300 piksel
Smooth: 8.0  
Hassasiyet: 2.0
```

## 🎨 Renk Sistemi

### Varsayılan Hedef Renkler
- **Kırmızı**: Ana düşman rengi
- **Sarı**: Vurgu ve highlight'lar
- **Turuncu**: Çerçeve ve outline'lar

### Renk Dosyası
Renkler `color_config.json` dosyasında saklanır ve özelleştirilebilir.

## 🔍 Sorun Giderme

### Program Başlamıyor
```bash
# Test çalıştır
python test_colorbot.py

# Kütüphaneleri kontrol et
pip install -r requirements.txt --upgrade
```

### Hedefler Bulunamıyor
1. **FOV'yi artır** (300-400 piksel)
2. **Test ortamında dene** (renkli objeler koy)
3. **Renk ayarlarını kontrol et**

### Hareket Çok Hızlı/Yavaş
1. **Smooth ayarını değiştir** (1.0-20.0)
2. **Hassasiyeti ayarla** (0.1-5.0)
3. **Hold modunu kullan** (daha kontrollü)

### Tuş Çalışmıyor
1. **Yönetici olarak çalıştır**
2. **Güvenli tuş kullan** (F1-F6)
3. **Tuş çakışmasını kontrol et**

## 📊 Sistem Gereksinimleri

- **OS**: Windows 10/11
- **Python**: 3.8+
- **RAM**: 2GB+
- **CPU**: Herhangi modern işlemci

## 📁 Dosya Yapısı

```
ColorBot/
├── main.py              # Ana program (Pro sürüm)
├── screen_capture.py    # Ekran yakalama
├── color_detection.py   # Renk tespit sistemi
├── mouse_control.py     # Fare kontrolü
├── key_binding.py       # Tuş bağlama
├── key_capture.py       # Tuş yakalama sistemi (YENİ)
├── test_colorbot.py     # Sistem testi
├── run_colorbot.bat     # Kolay başlatma
├── requirements.txt     # Kütüphaneler
└── *.json              # Ayar dosyaları
```

## ⚖️ Yasal Uyarı

- Bu yazılım **sadece eğitim amaçlıdır**
- Oyun ToS'larını ihlal etme amacı taşımaz
- **Kullanıcının sorumluluğundadır**
- Anti-cheat sistemler tarafından tespit edilebilir

---

**🎯 ColorBot Pro** - Profesyonel seviyede nişan yardımcısı deneyimi!

**⚠️ Sorumluluk Reddi**: Geliştiriciler hiçbir zarardan sorumlu değildir.