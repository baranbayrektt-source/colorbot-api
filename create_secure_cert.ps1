# QUARXV1 Güvenli Code Signing Certificate Creator
Write-Host "Creating QUARXV1 Secure Code Signing Certificate..." -ForegroundColor Green

# Güvenli şifre oluştur
$password = ConvertTo-SecureString -String "QUARXV1Secure2025!" -Force -AsPlainText

# Self-signed certificate oluştur (5 yıl geçerli)
$cert = New-SelfSignedCertificate -Subject "CN=QUARXV1 ColorBot Code Signing" -Type CodeSigningCert -CertStoreLocation Cert:\CurrentUser\My -KeyAlgorithm RSA -KeyLength 2048 -HashAlgorithm SHA256 -NotAfter (Get-Date).AddYears(5) -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3")

# PFX formatında export et
Export-PfxCertificate -Cert $cert -FilePath "QUARXV1_Secure.pfx" -Password $password

# Public certificate export et
Export-Certificate -Cert $cert -FilePath "QUARXV1_Secure.cer"

# Certificate'i trusted root'a ekle
Write-Host "Installing certificate to trusted root..." -ForegroundColor Yellow
Import-Certificate -FilePath "QUARXV1_Secure.cer" -CertStoreLocation Cert:\CurrentUser\Root

Write-Host "✅ Secure certificate created successfully!" -ForegroundColor Green
Write-Host "📁 Files created:" -ForegroundColor Yellow
Write-Host "  - QUARXV1_Secure.pfx (Code Signing Certificate)" -ForegroundColor White
Write-Host "  - QUARXV1_Secure.cer (Public Certificate)" -ForegroundColor White
Write-Host "🔐 Password: QUARXV1Secure2025!" -ForegroundColor Cyan
Write-Host "⏰ Valid until: $((Get-Date).AddYears(5).ToString('dd/MM/yyyy'))" -ForegroundColor Green

# Certificate bilgilerini göster
Write-Host "`n📋 Certificate Details:" -ForegroundColor Yellow
Write-Host "  Subject: $($cert.Subject)" -ForegroundColor White
Write-Host "  Issuer: $($cert.Issuer)" -ForegroundColor White
Write-Host "  Thumbprint: $($cert.Thumbprint)" -ForegroundColor White
Write-Host "  Valid From: $($cert.NotBefore.ToString('dd/MM/yyyy'))" -ForegroundColor White
Write-Host "  Valid Until: $($cert.NotAfter.ToString('dd/MM/yyyy'))" -ForegroundColor White

Write-Host "`n🎯 Certificate is ready for signing QUARXV1.exe!" -ForegroundColor Green
