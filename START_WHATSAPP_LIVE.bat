@echo off
echo ================================================================
echo   WHATSAPP LIVE RECEIVER - AI Auto-Reply
echo ================================================================
echo.
echo Starting WhatsApp message receiver...
echo.
echo This will:
echo 1. Monitor WhatsApp Web for new messages
echo 2. Send messages to AI for intelligent auto-reply
echo 3. Send replies back to WhatsApp
echo.
echo ================================================================
echo.
cd /d "%~dp0"
python whatsapp_live_receiver.py
echo.
echo ================================================================
echo Receiver stopped.
echo Press any key to exit...
pause >nul
