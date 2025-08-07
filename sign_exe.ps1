# QUARXV1.exe Code Signing Script
Write-Host "Signing QUARXV1.exe with digital signature..." -ForegroundColor Green

# Certificate bilgileri
$pfxPath = "QUARXV1_Secure.pfx"
$pfxPassword = "QUARXV1Secure2025!"
$exePath = "dist\QUARXV1.exe"

# Dosyaları kontrol et
if (-not (Test-Path $pfxPath)) {
    Write-Host "Certificate file not found: $pfxPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $exePath)) {
    Write-Host "EXE file not found: $exePath" -ForegroundColor Red
    exit 1
}

Write-Host "Certificate: $pfxPath" -ForegroundColor Yellow
Write-Host "EXE: $exePath" -ForegroundColor Yellow
Write-Host "Password: $pfxPassword" -ForegroundColor Cyan

# Certificate'i yükle (alternatif yöntem)
try {
    # Certificate store'dan al
    $certs = Get-ChildItem -Path Cert:\CurrentUser\My | Where-Object {$_.Subject -like "*QUARXV1*"}
    
    if ($certs) {
        $cert = $certs[0]  # İlk certificate'i al
        Write-Host "Certificate loaded from store successfully" -ForegroundColor Green
        Write-Host "Certificate: $($cert.Subject)" -ForegroundColor White
    } else {
        Write-Host "Certificate not found in store, trying to import..." -ForegroundColor Yellow
        
        # PFX'i import et
        $securePassword = ConvertTo-SecureString -String $pfxPassword -Force -AsPlainText
        Import-PfxCertificate -FilePath $pfxPath -CertStoreLocation Cert:\CurrentUser\My -Password $securePassword
        
        $certs = Get-ChildItem -Path Cert:\CurrentUser\My | Where-Object {$_.Subject -like "*QUARXV1*"}
        $cert = $certs[0]  # İlk certificate'i al
        Write-Host "Certificate imported and loaded successfully" -ForegroundColor Green
    }
} catch {
    Write-Host "Failed to load certificate: $_" -ForegroundColor Red
    exit 1
}

# EXE'yi imzala
try {
    Write-Host "Signing QUARXV1.exe..." -ForegroundColor Yellow
    
    # Basit imzalama (timestamp olmadan)
    $result = Set-AuthenticodeSignature -FilePath $exePath -Certificate $cert -HashAlgorithm SHA256
    
    if ($result.Status -eq "Valid") {
        Write-Host "QUARXV1.exe signed successfully!" -ForegroundColor Green
        Write-Host "Signature Details:" -ForegroundColor Yellow
        Write-Host "  Status: $($result.Status)" -ForegroundColor White
        Write-Host "  SignerCertificate: $($result.SignerCertificate.Subject)" -ForegroundColor White
    } else {
        Write-Host "Signing failed: $($result.Status)" -ForegroundColor Red
    }
} catch {
    Write-Host "Signing error: $_" -ForegroundColor Red
}

Write-Host "QUARXV1.exe is now digitally signed!" -ForegroundColor Green
