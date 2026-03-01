@echo off
title Gmail Watcher - Personal AI Employee
color 0A
cls
echo ================================================================
echo         GMAIL WATCHER - Starting...
echo ================================================================
echo.
cd /d "%~dp0"
python AI_Employee_System\Watchers\start_gmail_watcher.py
echo.
echo ================================================================
echo Gmail Watcher has stopped.
echo Press any key to exit...
pause >nul
