@echo off
title QUARXV1 GitHub Push
color 0E

echo.
echo ========================================
echo    QUARXV1 GITHUB'A YUKLEME
echo ========================================
echo.

echo [1/4] Git durumu kontrol ediliyor...
git status

echo.
echo [2/4] Değişiklikler ekleniyor...
git add .

echo.
echo [3/4] Commit oluşturuluyor...
git commit -m "QUARXV1 v$(date /t) - GitHub Actions build system added"

echo.
echo [4/4] GitHub'a push ediliyor...
git push origin main

echo.
echo ========================================
echo    GITHUB ACTIONS TETIKLENDI!
echo ========================================
echo.
echo GitHub'da Actions sekmesine gidin:
echo https://github.com/baranbayrektt-source/colorbot-api/actions
echo.
echo Build tamamlandığında:
echo 1. Actions > Latest workflow run
echo 2. Artifacts > QUARXV1-Setup
echo 3. Download ZIP
echo.
pause
