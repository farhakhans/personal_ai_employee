@echo off
echo ================================================================
echo   GMAIL WATCHER - Personal AI Employee
echo ================================================================
echo.
cd /d "%~dp0"
echo Starting Gmail Watcher...
echo.
python AI_Employee_System\Watchers\start_gmail_watcher.py
echo.
echo ================================================================
echo Gmail Watcher has stopped.
echo Press any key to exit...
pause >nul
