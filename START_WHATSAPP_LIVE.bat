@echo off
color 0A
cls
echo ================================================================
echo     WhatsApp Live Auto-Reply - START
echo ================================================================
echo.
echo Yeh script:
echo   1. WhatsApp Web kholegi
echo   2. Real-time messages receive karegi
echo   3. Auto-reply bhejegi keywords par
echo   4. Messages save karegi vault mein
echo.
echo ================================================================
echo.
echo [Checking] Playwright...
python -c "import playwright" 2>nul
if errorlevel 1 (
    echo [Installing] Playwright...
    pip install playwright
    playwright install chromium
)
echo [OK] Playwright ready!
echo.
echo ================================================================
echo Starting WhatsApp Live Receiver...
echo ================================================================
echo.
echo INSTRUCTIONS:
echo.
echo 1. Browser khulega automatically
echo 2. QR code scan karein (phone se)
echo 3. Is window ko khula chor dein
echo 4. Messages aayenge toh auto-reply jayega!
echo.
echo ================================================================
echo.
echo Press Ctrl+C to stop
echo ================================================================
echo.

cd /d "%~dp0"
python whatsapp_live_server.py

pause
