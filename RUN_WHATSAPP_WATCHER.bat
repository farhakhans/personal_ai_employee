@echo off
title WhatsApp Watcher - Personal AI Employee
color 02
cls
echo ================================================================
echo         WHATSAPP WATCHER - Starting...
echo ================================================================
echo.
cd /d "%~dp0"
python AI_Employee_System\Watchers\start_whatsapp_watcher.py
echo.
echo ================================================================
echo WhatsApp Watcher has stopped.
echo Press any key to exit...
pause >nul
