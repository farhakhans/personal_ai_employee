@echo off
echo ================================================================
echo   WHATSAPP WATCHER - Personal AI Employee
echo ================================================================
echo.
cd /d "%~dp0"
echo Starting WhatsApp Watcher...
echo.
python AI_Employee_System\Watchers\start_whatsapp_watcher.py
echo.
echo ================================================================
echo WhatsApp Watcher has stopped.
echo Press any key to exit...
pause >nul
