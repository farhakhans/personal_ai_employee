@echo off
title Silver Tier - Personal AI Employee
color 03

echo ================================================================
echo         SILVER TIER - Starting...
echo ================================================================
echo.
echo Silver Tier Features:
echo   * WhatsApp Watcher (Message Monitoring)
echo   * LinkedIn Poster (Professional Network)
echo   * Twitter Poster (Social Media)
echo   * File Watcher (File System Monitoring)
echo   * Flask API Server (Dashboard)
echo.
echo NOTE: Gmail skipped - setup .env first
echo ================================================================
echo.

cd /d "%~dp0"

echo [1/6] Starting Flask API Server...
start "Flask API" python api_routes.py
timeout /t 3 /nobreak >nul

echo [2/6] Starting WhatsApp Watcher...
start "WhatsApp Watcher" python AI_Employee_System\Watchers\start_whatsapp_watcher.py
timeout /t 2 /nobreak >nul

echo [3/6] Starting LinkedIn Poster...
start "LinkedIn Poster" python AI_Employee_System\Watchers\linkedin_poster.py
timeout /t 2 /nobreak >nul

echo [4/6] Starting Twitter Poster...
start "Twitter Poster" python AI_Employee_System\Watchers\twitter_poster.py
timeout /t 2 /nobreak >nul

echo [5/6] Starting File Watcher...
start "File Watcher" python AI_Employee_System\Watchers\start_file_watcher.py
timeout /t 2 /nobreak >nul

echo [6/6] Opening Dashboard...
timeout /t 5 /nobreak >nul
start http://localhost:5000/silver

echo.
echo ================================================================
echo ✅ Silver Tier Started Successfully!
echo ================================================================
echo.
echo Running Services:
echo   ✓ Flask API Server (Port 5000)
echo   ✓ WhatsApp Watcher
echo   ✓ LinkedIn Poster
echo   ✓ Twitter Poster
echo   ✓ File Watcher
echo.
echo Dashboard: http://localhost:5000/silver
echo.
echo ================================================================
echo    THIS WINDOW WILL STAY OPEN - DO NOT CLOSE
echo    Services are running in separate windows
echo    Press Ctrl+C to stop all services
echo ================================================================
echo.

:loop
timeout /t 60 /nobreak >nul
goto loop
