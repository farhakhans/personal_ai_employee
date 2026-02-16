@echo off
echo ================================================================
echo   WhatsApp Watcher - Setup and Run
echo ================================================================
echo.
echo Installing Playwright browsers (this may take a few minutes)...
echo.

cd /d "%~dp0"

REM Install Playwright browsers
echo [1/2] Installing Chromium browser...
call python -m playwright install chromium

if %errorlevel% neq 0 (
    echo.
    echo Installation encountered issues. Trying to continue...
    echo.
)

echo.
echo [2/2] Starting WhatsApp Watcher...
echo.
echo ================================================================
echo IMPORTANT: When browser opens:
echo 1. Wait for WhatsApp Web to load
echo 2. Scan the QR code with your phone
echo 3. WhatsApp will start monitoring
echo ================================================================
echo.

cd /d "%~dp0AI_Employee_System\Watchers"
python start_whatsapp_watcher.py

echo.
echo ================================================================
echo WhatsApp Watcher exited.
echo ================================================================
pause
