@echo off
echo ================================================================
echo   WhatsApp Watcher - Quick Start
echo ================================================================
echo.
echo This will run the WhatsApp Watcher to monitor your WhatsApp messages.
echo.
echo BEFORE RUNNING:
echo 1. Make sure Playwright is installed: pip install playwright
echo 2. Install Chromium: playwright install chromium
echo 3. Have your phone ready to scan QR code
echo.
echo ================================================================
echo.

cd /d "%~dp0AI_Employee_System\Watchers"

echo Starting WhatsApp Watcher...
echo.
python start_whatsapp_watcher.py

echo.
echo ================================================================
echo WhatsApp Watcher exited.
echo ================================================================
pause
