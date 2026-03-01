@echo off
title All Watchers - Personal AI Employee
color 0B

echo ================================================================
echo         ALL WATCHERS - Starting...
echo ================================================================
echo.

cd /d "%~dp0"

echo [1/4] Starting Gmail Watcher...
start "Gmail Watcher" python AI_Employee_System\Watchers\start_gmail_watcher.py
timeout /t 2 /nobreak >nul

echo [2/4] Starting File Watcher...
start "File Watcher" python AI_Employee_System\Watchers\start_file_watcher.py
timeout /t 2 /nobreak >nul

echo [3/4] Starting WhatsApp Watcher...
start "WhatsApp Watcher" python AI_Employee_System\Watchers\start_whatsapp_watcher.py
timeout /t 2 /nobreak >nul

echo [4/4] Starting MCP Server...
start "MCP Server" python run_mcp_server.py
timeout /t 2 /nobreak >nul

echo.
echo ================================================================
echo ✅ All Watchers Started Successfully!
echo ================================================================
echo.
echo Running Services:
echo   ✓ Gmail Watcher
echo   ✓ File Watcher
echo   ✓ WhatsApp Watcher
echo   ✓ MCP Server
echo.
echo API Endpoints:
echo   Dashboard:    http://localhost:5000
echo   MCP Servers:  http://localhost:5000/api/mcp/servers
echo   Agent Skills: http://localhost:5000/agent-skills
echo.
echo To stop: Close each window or press Ctrl+C
echo ================================================================
echo.
pause
