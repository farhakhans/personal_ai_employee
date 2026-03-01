@echo off
color 0A
cls
echo ================================================================
echo     WhatsApp Manager - Start Server
echo ================================================================
echo.
echo Yeh server WhatsApp Manager page ko run karega.
echo.
echo ================================================================
echo.
echo Server start ho raha hai...
echo.

cd /d "%~dp0"
python api_routes.py

pause
