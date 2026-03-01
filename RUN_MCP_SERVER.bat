@echo off
echo ================================================================
echo   MCP SERVER - Personal AI Employee
echo ================================================================
echo.
cd /d "%~dp0"
echo Starting MCP Server...
echo.
python run_mcp_server.py
echo.
echo ================================================================
echo MCP Server has stopped.
echo Press any key to exit...
pause >nul
