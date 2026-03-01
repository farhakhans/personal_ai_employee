@echo off
color 0A
cls
echo ================================================================
echo     Starting WhatsApp Manager Server
echo ================================================================
echo.
echo Server URL: http://localhost:5000
echo WhatsApp Manager: http://localhost:5000/whatsapp-manager
echo.
echo ================================================================
echo.
echo Starting server... Press Ctrl+C to stop
echo.

cd /d "%~dp0"
python api_routes.py
