@echo off
echo ================================================================
echo   FILE WATCHER - Personal AI Employee
echo ================================================================
echo.
cd /d "%~dp0"
echo Starting File Watcher...
echo.
python AI_Employee_System\Watchers\start_file_watcher.py
echo.
echo ================================================================
echo File Watcher has stopped.
echo Press any key to exit...
pause >nul
