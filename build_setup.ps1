# QUARXV1 Otomatik Setup Oluşturucu
Write-Host "QUARXV1 Otomatik Setup Oluşturucu" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

# Adım 1: PyInstaller ile EXE oluştur
Write-Host "Adım 1: QUARXV1.exe oluşturuluyor..." -ForegroundColor Yellow
try {
    pyinstaller --onefile --icon quarxv1.ico main.py --name QUARXV1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "QUARXV1.exe başarıyla oluşturuldu!" -ForegroundColor Green
    } else {
        Write-Host "EXE oluşturma hatası!" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "PyInstaller hatası: $_" -ForegroundColor Red
    exit 1
}

# Adım 2: Certificate kontrol et
Write-Host "Adım 2: Certificate kontrol ediliyor..." -ForegroundColor Yellow
$pfxPath = "QUARXV1_Secure.pfx"
if (-not (Test-Path $pfxPath)) {
    Write-Host "Certificate bulunamadı, oluşturuluyor..." -ForegroundColor Yellow
    
    # Certificate oluştur
    $password = ConvertTo-SecureString -String "QUARXV1Secure2025!" -Force -AsPlainText
    $cert = New-SelfSignedCertificate -Subject "CN=QUARXV1 ColorBot Code Signing" -Type CodeSigningCert -CertStoreLocation Cert:\CurrentUser\My -KeyAlgorithm RSA -KeyLength 2048 -HashAlgorithm SHA256 -NotAfter (Get-Date).AddYears(5)
    Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $password
    Export-Certificate -Cert $cert -FilePath "QUARXV1_Secure.cer"
    Import-Certificate -FilePath "QUARXV1_Secure.cer" -CertStoreLocation Cert:\CurrentUser\Root
    
    Write-Host "Certificate oluşturuldu!" -ForegroundColor Green
} else {
    Write-Host "Certificate mevcut!" -ForegroundColor Green
}

# Adım 3: EXE'yi dijital imza ile imzala
Write-Host "Adım 3: Dijital imza ekleniyor..." -ForegroundColor Yellow
try {
    $exePath = "dist\QUARXV1.exe"
    $certs = Get-ChildItem -Path Cert:\CurrentUser\My | Where-Object {$_.Subject -like "*QUARXV1*"}
    
    if ($certs) {
        $cert = $certs[0]
        $result = Set-AuthenticodeSignature -FilePath $exePath -Certificate $cert -HashAlgorithm SHA256
        
        if ($result.Status -eq "Valid") {
            Write-Host "Dijital imza başarıyla eklendi!" -ForegroundColor Green
        } else {
            Write-Host "İmza eklendi ama status: $($result.Status)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "Certificate bulunamadı!" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "İmzalama hatası: $_" -ForegroundColor Red
    exit 1
}

# Adım 4: Dosya boyutunu kontrol et
Write-Host "Adım 4: Dosya kontrol ediliyor..." -ForegroundColor Yellow
$exeInfo = Get-Item $exePath
$sizeMB = [math]::Round($exeInfo.Length / 1MB, 2)
Write-Host "Dosya boyutu: $sizeMB MB" -ForegroundColor Green

# Adım 5: Dist klasörünü temizle ve kopyala
Write-Host "Adım 5: Dist klasörü hazırlanıyor..." -ForegroundColor Yellow
try {
    # Eski dosyaları sil (EXE hariç)
    Get-ChildItem "dist" -Exclude "QUARXV1.exe" | Remove-Item -Force
    
    # Gerekli dosyaları kopyala
    Copy-Item "README.txt" "dist\" -Force
    Copy-Item "KURULUM_KILAVUZU.txt" "dist\" -Force
    Copy-Item "GUVENLIK_REHBERI.txt" "dist\" -Force
    
    Write-Host "Dist klasörü hazırlandı!" -ForegroundColor Green
} catch {
    Write-Host "Dosya kopyalama hatası: $_" -ForegroundColor Red
}

# Adım 6: Son kontrol
Write-Host "Adım 6: Son kontrol yapılıyor..." -ForegroundColor Yellow
$distFiles = Get-ChildItem "dist"
Write-Host "Dist klasörü içeriği:" -ForegroundColor Green
foreach ($file in $distFiles) {
    $fileSize = [math]::Round($file.Length / 1KB, 1)
    Write-Host "  - $($file.Name) ($fileSize KB)" -ForegroundColor White
}

# Başarı mesajı
Write-Host ""
Write-Host "QUARXV1 SETUP BAŞARIYLA OLUŞTURULDU!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Konum: dist\ klasörü" -ForegroundColor Yellow
Write-Host "Dosyalar:" -ForegroundColor Yellow
Write-Host "  - QUARXV1.exe (Dijital İmzalı)" -ForegroundColor White
Write-Host "  - README.txt" -ForegroundColor White
Write-Host "  - KURULUM_KILAVUZU.txt" -ForegroundColor White
Write-Host "  - GUVENLIK_REHBERI.txt" -ForegroundColor White
Write-Host ""
Write-Host "Kullanıcılara dist klasörünü verin!" -ForegroundColor Cyan
Write-Host ""
