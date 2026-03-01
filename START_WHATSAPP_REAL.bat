@echo off
color 0A
cls
echo ================================================================
echo     WhatsApp Real Auto-Reply - START
echo ================================================================
echo.
echo Yeh script REAL WhatsApp messages receive karegi aur
echo unka automatic reply bhejegi!
echo.
echo ================================================================
echo.
echo [1/2] Checking Playwright...
python -c "import playwright" 2>nul
if errorlevel 1 (
    echo Installing Playwright...
    pip install playwright
)
echo Playwright OK!
echo.

echo [2/2] Starting WhatsApp Receiver...
echo.
echo ================================================================
echo INSTRUCTIONS:
echo ================================================================
echo.
echo 1. Browser apne aap khulega
echo 2. QR code ko apne phone se scan karein:
echo    - Phone mein WhatsApp kholein
echo    - Settings > Linked Devices > Link a Device
echo    - Camera ko QR code par le jayein
echo 3. Is window ko khula chor dein
echo 4. Jab message ayega, console mein dikhega!
echo.
echo ================================================================
echo.
echo Shuru karne ke liye koi button dabayein...
pause > nul
echo.
echo Starting...
echo.

cd /d "%~dp0"
python run_whatsapp_receiver.py

pause
