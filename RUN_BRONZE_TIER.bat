@echo off
title Bronze Tier - Personal AI Employee
color 0B

echo ================================================================
echo         BRONZE TIER - Starting...
echo ================================================================
echo.
echo Bronze Tier Features:
echo   * File Watcher (File System Monitoring)
echo   * MCP Server (AI Integrations)
echo   * Flask API Server (Dashboard)
echo.
echo NOTE: Gmail Watcher skipped - setup .env first
echo ================================================================
echo.

cd /d "%~dp0"

echo [1/4] Starting Flask API Server...
start "Flask API" python api_routes.py
timeout /t 3 /nobreak >nul

echo [2/4] Starting File Watcher...
start "File Watcher" python AI_Employee_System\Watchers\start_file_watcher.py
timeout /t 2 /nobreak >nul

echo [3/4] Starting MCP Server...
start "MCP Server" python run_mcp_server.py
timeout /t 2 /nobreak >nul

echo [4/4] Opening Dashboard...
timeout /t 5 /nobreak >nul
start http://localhost:5000/bronze

echo.
echo ================================================================
echo ✅ Bronze Tier Started Successfully!
echo ================================================================
echo.
echo Running Services:
echo   ✓ Flask API Server (Port 5000)
echo   ✓ File Watcher
echo   ✓ MCP Server
echo.
echo Dashboard: http://localhost:5000/bronze
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
