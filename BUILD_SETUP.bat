@echo off
title QUARXV1 Setup Builder
color 0A

echo.
echo ========================================
echo    QUARXV1 OTOMATIK SETUP OLUSTURUCU
echo ========================================
echo.

echo Setup olusturuluyor...
echo Bu islem 2-3 dakika surebilir...
echo.

powershell -ExecutionPolicy Bypass -File build_setup.ps1

echo.
echo ========================================
echo Setup olusturma tamamlandi!
echo Dist klasorunu kontrol edin.
echo ========================================
echo.

pause
