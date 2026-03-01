@echo off
color 0B
cls
echo ================================================================
echo     WhatsApp Real Auto-Reply - Quick Start
echo ================================================================
echo.
echo Yeh script real WhatsApp messages receive karegi aur
echo unka automatic reply bhejegi!
echo.
echo ================================================================
echo.
echo [STEP 1] Playwright install ho raha hai...
echo ================================================================
pip install playwright
echo.

echo ================================================================
echo [STEP 2] Chromium browser install ho raha hai...
echo ================================================================
playwright install chromium
echo.

echo ================================================================
echo [STEP 3] WhatsApp Receiver start ho raha hai...
echo ================================================================
echo.
echo INSTRUCTIONS:
echo.
echo 1. Browser apne aap khulega
echo 2. QR code ko apne phone se scan karein
echo 3. Is window ko khula chor dein
echo 4. Jab bhi message ayega, console mein dikhega!
echo.
echo ================================================================
echo.
echo Shuru karne ke liye koi bhi button dabayein...
pause > nul
echo.

python run_whatsapp_receiver.py

pause
