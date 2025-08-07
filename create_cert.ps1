# QUARXV1 Code Signing Certificate Creator
Write-Host "Creating QUARXV1 Code Signing Certificate..." -ForegroundColor Green

# Password oluştur
$password = ConvertTo-SecureString -String "QUARXV1Secure2025!" -Force -AsPlainText

# Self-signed certificate oluştur
$cert = New-SelfSignedCertificate -Subject "CN=QUARXV1 ColorBot Code Signing" -Type CodeSigningCert -CertStoreLocation Cert:\CurrentUser\My -KeyAlgorithm RSA -KeyLength 2048 -HashAlgorithm SHA256 -NotAfter (Get-Date).AddYears(5)

# PFX export
Export-PfxCertificate -Cert $cert -FilePath "QUARXV1_Secure.pfx" -Password $password

# CER export
Export-Certificate -Cert $cert -FilePath "QUARXV1_Secure.cer"

# Trusted root'a ekle
Write-Host "Installing certificate to trusted root..." -ForegroundColor Yellow
Import-Certificate -FilePath "QUARXV1_Secure.cer" -CertStoreLocation Cert:\CurrentUser\Root

Write-Host "Certificate created successfully!" -ForegroundColor Green
Write-Host "Files created:" -ForegroundColor Yellow
Write-Host "  - QUARXV1_Secure.pfx" -ForegroundColor White
Write-Host "  - QUARXV1_Secure.cer" -ForegroundColor White
Write-Host "Password: QUARXV1Secure2025!" -ForegroundColor Cyan

Write-Host "Certificate is ready for signing!" -ForegroundColor Green
