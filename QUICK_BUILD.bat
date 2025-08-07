@echo off
title QUARXV1 Quick Builder
color 0B

echo.
echo ========================================
echo    QUARXV1 HIZLI SETUP OLUSTURUCU
echo ========================================
echo.

echo [1/6] EXE olusturuluyor...
pyinstaller --onefile --icon quarxv1.ico main.py --name QUARXV1 --noconfirm

echo [2/6] Certificate kontrol ediliyor...
if not exist "QUARXV1_Secure.pfx" (
    echo Certificate olusturuluyor...
    powershell -Command "New-SelfSignedCertificate -Subject 'CN=QUARXV1 ColorBot Code Signing' -Type CodeSigningCert -CertStoreLocation Cert:\CurrentUser\My -KeyAlgorithm RSA -KeyLength 2048 -HashAlgorithm SHA256 -NotAfter (Get-Date).AddYears(5) | Export-PfxCertificate -FilePath 'QUARXV1_Secure.pfx' -Password (ConvertTo-SecureString -String 'QUARXV1Secure2025!' -Force -AsPlainText)"
    powershell -Command "Get-ChildItem -Path Cert:\CurrentUser\My | Where-Object {$_.Subject -like '*QUARXV1*'} | Export-Certificate -FilePath 'QUARXV1_Secure.cer'"
    powershell -Command "Import-Certificate -FilePath 'QUARXV1_Secure.cer' -CertStoreLocation Cert:\CurrentUser\Root"
)

echo [3/6] Dijital imza ekleniyor...
powershell -Command "$cert = (Get-ChildItem -Path Cert:\CurrentUser\My | Where-Object {$_.Subject -like '*QUARXV1*'})[0]; Set-AuthenticodeSignature -FilePath 'dist\QUARXV1.exe' -Certificate $cert -HashAlgorithm SHA256"

echo [4/6] Dist klasoru temizleniyor...
del "dist\*.txt" 2>nul
del "dist\*.db" 2>nul

echo [5/6] Dosyalar kopyalaniyor...
copy "README.txt" "dist\" >nul
copy "KURULUM_KILAVUZU.txt" "dist\" >nul
copy "GUVENLIK_REHBERI.txt" "dist\" >nul

echo [6/6] Tamamlandi!
echo.
echo ========================================
echo    QUARXV1 SETUP HAZIR!
echo ========================================
echo.
echo Dosyalar: dist\ klasorunde
echo - QUARXV1.exe (Dijital Imzali)
echo - README.txt
echo - KURULUM_KILAVUZU.txt  
echo - GUVENLIK_REHBERI.txt
echo.
pause
