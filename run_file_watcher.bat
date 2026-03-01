@echo off
title File Watcher - Personal AI Employee
color 0B
cls
echo ================================================================
echo         FILE WATCHER - Starting...
echo ================================================================
echo.
cd /d "%~dp0"
python AI_Employee_System\Watchers\start_file_watcher.py
echo.
echo ================================================================
echo File Watcher has stopped.
echo Press any key to exit...
pause >nul
