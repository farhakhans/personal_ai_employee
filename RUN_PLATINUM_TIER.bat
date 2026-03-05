@echo off
title Platinum Tier - Personal AI Employee
color 0D

echo ================================================================
echo         PLATINUM TIER - Starting...
echo ================================================================
echo.
echo Platinum Tier Features:
echo   * All Gold Features
echo   * WhatsApp Real API (Live Messaging)
echo   * Flask API Server (Dashboard)
echo   * MCP Server (AI Integrations)
echo.
echo NOTE: Cloud VM setup required for 24/7 operation
echo Configure .env file first
echo ================================================================
echo.

cd /d "%~dp0"

echo [1/9] Starting Flask API Server...
start "Flask API" python api_routes.py
timeout /t 3 /nobreak >nul

echo [2/9] Starting WhatsApp Real API...
start "WhatsApp Real" python run_whatsapp_autoreply.py
timeout /t 2 /nobreak >nul

echo [3/9] Starting LinkedIn Poster...
start "LinkedIn Poster" python AI_Employee_System\Watchers\linkedin_poster.py
timeout /t 2 /nobreak >nul

echo [4/9] Starting Twitter Poster...
start "Twitter Poster" python AI_Employee_System\Watchers\twitter_poster.py
timeout /t 2 /nobreak >nul

echo [5/9] Starting Facebook Poster...
start "Facebook Poster" python AI_Employee_System\Watchers\facebook_poster.py
timeout /t 2 /nobreak >nul

echo [6/9] Starting Instagram Poster...
start "Instagram Poster" python AI_Employee_System\Watchers\instagram_poster.py
timeout /t 2 /nobreak >nul

echo [7/9] Starting File Watcher...
start "File Watcher" python AI_Employee_System\Watchers\start_file_watcher.py
timeout /t 2 /nobreak >nul

echo [8/9] Starting MCP Server...
start "MCP Server" python run_mcp_server.py
timeout /t 2 /nobreak >nul

echo [9/9] Opening Dashboard...
timeout /t 5 /nobreak >nul
start http://localhost:5000/platinum

echo.
echo ================================================================
echo ✅ Platinum Tier Started Successfully!
echo ================================================================
echo.
echo Running Services:
echo   ✓ Flask API Server (Port 5000)
echo   ✓ WhatsApp Real API
echo   ✓ LinkedIn Poster
echo   ✓ Twitter Poster
echo   ✓ Facebook Poster
echo   ✓ Instagram Poster
echo   ✓ File Watcher
echo   ✓ MCP Server
echo.
echo Dashboard: http://localhost:5000/platinum
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
