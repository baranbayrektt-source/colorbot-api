🎯 QUARXV1 SETUP OLUŞTURUCU
═══════════════════════════════════════════════════════════════════════════════

📦 OTOMATIK SETUP OLUŞTURMA SİSTEMİ

Bu sistem ile QUARXV1.exe'yi otomatik olarak oluşturabilir, 
dijital imza ekleyebilir ve dağıtım paketini hazırlayabilirsiniz.

🚀 KULLANIM YÖNTEMLERİ:

1️⃣ HIZLI SETUP (ÖNERİLEN):
   - QUICK_BUILD.bat dosyasına çift tıklayın
   - 2-3 dakika bekleyin
   - dist\ klasöründe hazır setup

2️⃣ DETAYLI SETUP:
   - BUILD_SETUP.bat dosyasına çift tıklayın
   - Adım adım ilerleme görünür
   - Hata durumunda detaylı bilgi

3️⃣ MANUEL SETUP:
   - PowerShell'de: .\build_setup.ps1
   - Komut satırında: pyinstaller --onefile --icon quarxv1.ico main.py --name QUARXV1

📁 OLUŞTURULAN DOSYALAR:

✅ QUARXV1.exe (Dijital İmzalı)
   - Boyut: ~70MB
   - Icon: QUARXV1 crosshair
   - Certificate: QUARXV1 ColorBot Code Signing
   - Geçerlilik: 5 yıl

✅ README.txt
   - Kullanım kılavuzu
   - Özellikler listesi
   - Güvenlik bilgileri

✅ KURULUM_KILAVUZU.txt
   - Detaylı kurulum adımları
   - Sorun giderme
   - İletişim bilgileri

✅ GUVENLIK_REHBERI.txt
   - Antivirüs uyarıları
   - Windows Defender ayarları
   - Güvenlik çözümleri

🔧 TEKNIK ÖZELLİKLER:

• PyInstaller ile tek dosya EXE
• Self-signed dijital imza
• SHA256 hash algoritması
• 2048-bit RSA anahtar
• Windows uyumlu icon
• Otomatik certificate yönetimi

⚠️ ÖNEMLİ NOTLAR:

• İlk çalıştırmada certificate oluşturulur
• Windows güvenlik uyarısı normaldir
• Certificate 5 yıl geçerlidir
• Setup boyutu ~70MB'dır
• Tüm dosyalar dist\ klasöründe

🆘 SORUN GİDERME:

1. PyInstaller hatası:
   - pip install pyinstaller
   - Python PATH kontrolü

2. Certificate hatası:
   - PowerShell'i yönetici olarak çalıştırın
   - ExecutionPolicy kontrolü

3. İmzalama hatası:
   - Certificate store kontrolü
   - Dosya izinleri kontrolü

🎯 SONUÇ:

Setup oluşturulduktan sonra dist\ klasöründeki tüm dosyaları
kullanıcılara verin. Tek kurulum ile çalışır, internet bağlantısı
gerektirmez (ilk lisans aktivasyonu hariç).

═══════════════════════════════════════════════════════════════════════════════
🎯 QUARXV1 ColorBot - Professional Aim Assistant
═══════════════════════════════════════════════════════════════════════════════
