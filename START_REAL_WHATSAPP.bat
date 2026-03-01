@echo off
color 0A
cls
echo ================================================================
echo          WhatsApp Real-Time Message Receiver
echo ================================================================
echo.
echo This will:
echo   1. Open WhatsApp Web in a browser window
echo   2. Monitor for incoming messages in REAL-TIME
echo   3. Send AUTO-REPLIES based on keywords
echo   4. Save all messages to vault/Inbox/
echo.
echo ================================================================
echo.

:: Check if playwright is installed
python -c "import playwright" 2>nul
if errorlevel 1 (
    echo [INSTALLING] Installing Playwright...
    pip install playwright
    echo.
    echo [INSTALLING] Installing Chromium browser...
    playwright install chromium
    echo.
)

echo ================================================================
echo Starting WhatsApp Receiver...
echo ================================================================
echo.
echo INSTRUCTIONS:
echo 1. Wait for browser to open
echo 2. Scan QR code with your phone
echo 3. Keep this window open
echo 4. Messages will appear here in real-time!
echo.
echo Press Ctrl+C to stop
echo ================================================================
echo.

python run_whatsapp_receiver.py

pause
