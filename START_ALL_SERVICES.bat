@echo off
echo ================================================================
echo   ALL WATCHERS + MCP SERVER - Personal AI Employee
echo ================================================================
echo.
cd /d "%~dp0"

echo Starting all services...
echo.

echo [1/5] Starting Gmail Watcher...
start "Gmail Watcher" python AI_Employee_System\Watchers\start_gmail_watcher.py
timeout /t 2 /nobreak >nul

echo [2/5] Starting File Watcher...
start "File Watcher" python AI_Employee_System\Watchers\start_file_watcher.py
timeout /t 2 /nobreak >nul

echo [3/5] Starting WhatsApp Watcher...
start "WhatsApp Watcher" python AI_Employee_System\Watchers\start_whatsapp_watcher.py
timeout /t 2 /nobreak >nul

echo [4/5] Starting MCP Server...
start "MCP Server" python run_mcp_server.py
timeout /t 2 /nobreak >nul

echo [5/5] Starting Flask API Server...
start "Flask API" python api_routes.py
timeout /t 3 /nobreak >nul

echo.
echo ================================================================
echo ✅ All services started successfully!
echo ================================================================
echo.
echo Services Running:
echo   ✓ Gmail Watcher
echo   ✓ File Watcher
echo   ✓ WhatsApp Watcher
echo   ✓ MCP Server
echo   ✓ Flask API Server
echo.
echo Access URLs:
echo   Dashboard:    http://localhost:5000/
echo   Agent Skills: http://localhost:5000/agent-skills
echo   MCP API:      http://localhost:5000/api/mcp/servers
echo.
echo Press Ctrl+C in each window to stop individual services
echo ================================================================
echo.
pause
