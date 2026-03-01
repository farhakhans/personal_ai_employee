@echo off
echo ================================================================
echo WhatsApp Real Auto-Reply System
echo ================================================================
echo.
echo Installing requirements...
pip install playwright
playwright install chromium
echo.
echo ================================================================
echo Starting WhatsApp Auto-Reply...
echo ================================================================
echo.
python run_whatsapp_autoreply.py
pause
