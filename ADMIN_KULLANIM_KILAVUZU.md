# 🎯 QUARXV1 ColorBot - Admin Panel Kullanım Kılavuzu

## 📋 Genel Bakış
Admin Panel, ColorBot lisans anahtarlarını yönetmek için kullanılan profesyonel araçtır.

## 🚀 Başlatma
```bash
cd admin_panel
python admin_panel.py
```

## 📊 Sekmeler

### 1. Key Generator
- **Amaç**: Yeni lisans anahtarları üretmek
- **Özellikler**:
  - 1 Day, 1 Week, 1 Month, Unlimited seçenekleri
  - Otomatik key formatı: QUA-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX
  - HWID binding (her key sadece bir PC'de çalışır)
  - Copy butonları ile kolay kopyalama

### 2. License Management
- **Amaç**: Aktif lisansları görüntülemek ve yönetmek
- **Özellikler**:
  - Tüm aktif lisansları listeler
  - Kullanıcı bilgileri
  - Kalan süre bilgisi
  - Delete Selected butonu

### 3. Expired Keys
- **Amaç**: Süresi dolmuş lisansları yönetmek
- **Özellikler**:
  - Süresi dolmuş lisansları listeler
  - Toplu silme işlemi
  - Temizlik için kullanılır

### 4. User Management
- **Amaç**: Kullanıcı bilgilerini yönetmek
- **Özellikler**:
  - Kullanıcı listesi
  - HWID bilgileri
  - Kullanım istatistikleri

## 🔑 Key Üretme Süreci

### Adım 1: Key Generator Sekmesine Git
- Admin panel'i aç
- "Key Generator" sekmesini seç

### Adım 2: Süre Seç
- 1 Day: 1 günlük lisans
- 1 Week: 1 haftalık lisans
- 1 Month: 1 aylık lisans
- Unlimited: Sınırsız lisans

### Adım 3: Key Üret
- "Generate Keys" butonuna bas
- Key otomatik olarak üretilir ve listeye eklenir

### Adım 4: Key'i Kopyala
- Key'in yanındaki "Copy" butonuna bas
- Key panoya kopyalanır

### Adım 5: Kullanıcıya Ver
- Kopyalanan key'i kullanıcıya gönder
- Kullanıcı ColorBot.exe'de key'i girer

## 🔄 Senkronizasyon

### Online Sistem
- Key'ler anında API'ye kaydedilir
- ColorBot.exe online kontrol yapar
- Senkronizasyon sorunu yoktur

### Offline Yedekleme
- Veritabanı local olarak saklanır
- İnternet olmasa bile çalışır
- API erişilemezse offline kontrol yapar

## 🛡️ Güvenlik

### HWID Binding
- Her key sadece bir PC'de çalışır
- Kullanıcı key'i paylaşamaz
- Admin panel'den kullanım takip edilir

### Süre Kontrolü
- Key'ler otomatik olarak süresi dolunca durur
- Admin panel'den manuel iptal edilebilir
- Süre bilgisi gerçek zamanlı görüntülenir

## 📈 İstatistikler

### Kullanım Takibi
- Hangi key'lerin kullanıldığı
- Kalan süre bilgileri
- Kullanıcı aktivite logları

### Performans
- Toplam üretilen key sayısı
- Aktif kullanıcı sayısı
- Süresi dolmuş key sayısı

## ⚠️ Önemli Notlar

### Key Formatı
- Format: QUA-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX
- 25 karakter uzunluğunda
- Otomatik üretilir

### Veritabanı
- SQLite kullanılır
- Otomatik yedekleme
- Güvenli saklama

### API Bağlantısı
- Vercel'de host edilir
- 7/24 erişilebilir
- Yüksek performans

## 🆘 Sorun Giderme

### Key Çalışmıyor
1. Key'in doğru kopyalandığını kontrol et
2. Kullanıcının internet bağlantısını kontrol et
3. Key'in süresinin dolmadığını kontrol et

### Admin Panel Açılmıyor
1. Python'un yüklü olduğunu kontrol et
2. Gerekli modüllerin yüklü olduğunu kontrol et
3. Dosya yolunu kontrol et

### API Bağlantı Sorunu
1. İnternet bağlantısını kontrol et
2. Vercel servisinin çalıştığını kontrol et
3. Firewall ayarlarını kontrol et

## 📞 Destek

Herhangi bir sorun yaşarsanız:
- Hata mesajlarını kaydedin
- Ekran görüntüsü alın
- Detaylı açıklama yapın

---

🎯 **QUARXV1 ColorBot - Professional License Management System**
