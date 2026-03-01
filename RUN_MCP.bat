@echo off
title MCP Server - Personal AI Employee
color 0D
cls
echo ================================================================
echo         MCP SERVER - Starting...
echo ================================================================
echo.
cd /d "%~dp0"
python run_mcp_server.py
echo.
echo ================================================================
echo MCP Server has stopped.
echo Press any key to exit...
pause >nul
