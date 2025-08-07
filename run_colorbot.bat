@echo off
echo ============================================
echo    ColorBot - Konsol Modu
echo    Renk Tabanli Nishan Yardimcisi
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadi!
    echo Lutfen Python 3.8 veya uzeri yukleyin.
    pause
    exit /b 1
)

REM Change to script directory
cd /d "%~dp0"

REM Check if requirements are installed
echo Gerekli kutuphaneler kontrol ediliyor...
python -c "import cv2, numpy, pynput, pyautogui" >nul 2>&1
if errorlevel 1 (
    echo Gerekli kutuphaneler eksik. Yukleniyor...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo HATA: Kutuphaneler yuklenemedi!
        pause
        exit /b 1
    )
)

REM Run the application
echo.
echo ColorBot Konsol Modu baslatiliyor...
echo.
python main.py

pause