@echo off
title Gold Tier - Personal AI Employee
color 06

echo ================================================================
echo         GOLD TIER - Starting...
echo ================================================================
echo.
echo Gold Tier Features:
echo   * WhatsApp Watcher (Message Monitoring)
echo   * LinkedIn Poster (Professional Network)
echo   * Twitter Poster (Social Media)
echo   * Facebook Poster (Social Media)
echo   * Instagram Poster (Photo Sharing)
echo   * File Watcher (File System Monitoring)
echo   * Flask API Server (Dashboard)
echo.
echo NOTE: Gmail & Odoo skipped - setup .env first
echo ================================================================
echo.

cd /d "%~dp0"

echo [1/8] Starting Flask API Server...
start "Flask API" python api_routes.py
timeout /t 3 /nobreak >nul

echo [2/8] Starting WhatsApp Watcher...
start "WhatsApp Watcher" python AI_Employee_System\Watchers\start_whatsapp_watcher.py
timeout /t 2 /nobreak >nul

echo [3/8] Starting LinkedIn Poster...
start "LinkedIn Poster" python AI_Employee_System\Watchers\linkedin_poster.py
timeout /t 2 /nobreak >nul

echo [4/8] Starting Twitter Poster...
start "Twitter Poster" python AI_Employee_System\Watchers\twitter_poster.py
timeout /t 2 /nobreak >nul

echo [5/8] Starting Facebook Poster...
start "Facebook Poster" python AI_Employee_System\Watchers\facebook_poster.py
timeout /t 2 /nobreak >nul

echo [6/8] Starting Instagram Poster...
start "Instagram Poster" python AI_Employee_System\Watchers\instagram_poster.py
timeout /t 2 /nobreak >nul

echo [7/8] Starting File Watcher...
start "File Watcher" python AI_Employee_System\Watchers\start_file_watcher.py
timeout /t 2 /nobreak >nul

echo [8/8] Opening Dashboard...
timeout /t 5 /nobreak >nul
start http://localhost:5000/gold

echo.
echo ================================================================
echo ✅ Gold Tier Started Successfully!
echo ================================================================
echo.
echo Running Services:
echo   ✓ Flask API Server (Port 5000)
echo   ✓ WhatsApp Watcher
echo   ✓ LinkedIn Poster
echo   ✓ Twitter Poster
echo   ✓ Facebook Poster
echo   ✓ Instagram Poster
echo   ✓ File Watcher
echo.
echo Dashboard: http://localhost:5000/gold
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
