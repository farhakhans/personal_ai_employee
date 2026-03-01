@echo off
title Personal AI Employee - Service Manager
color 0A

:MENU
cls
echo ================================================================
echo         PERSONAL AI EMPLOYEE - SERVICE MANAGER
echo ================================================================
echo.
echo   WATCHERS:
echo   ---------
echo   [1] Start Gmail Watcher
echo   [2] Start File Watcher
echo   [3] Start WhatsApp Watcher
echo.
echo   MCP SERVERS:
echo   ------------
echo   [4] Start MCP Server
echo.
echo   MAIN SERVICES:
echo   --------------
echo   [5] Start Flask API Server
echo.
echo   ALL SERVICES:
echo   -------------
echo   [6] Start ALL Services Together
echo.
echo   EXIT:
echo   -----
echo   [0] Exit
echo.
echo ================================================================
echo.
set /p choice="Enter your choice (0-6): "

if "%choice%"=="1" goto START_GMAIL
if "%choice%"=="2" goto START_FILE
if "%choice%"=="3" goto START_WHATSAPP
if "%choice%"=="4" goto START_MCP
if "%choice%"=="5" goto START_FLASK
if "%choice%"=="6" goto START_ALL
if "%choice%"=="0" goto END
goto MENU

:START_GMAIL
cls
echo Starting Gmail Watcher...
start "Gmail Watcher" python AI_Employee_System\Watchers\start_gmail_watcher.py
echo Gmail Watcher started in new window!
pause
goto MENU

:START_FILE
cls
echo Starting File Watcher...
start "File Watcher" python AI_Employee_System\Watchers\start_file_watcher.py
echo File Watcher started in new window!
pause
goto MENU

:START_WHATSAPP
cls
echo Starting WhatsApp Watcher...
start "WhatsApp Watcher" python AI_Employee_System\Watchers\start_whatsapp_watcher.py
echo WhatsApp Watcher started in new window!
pause
goto MENU

:START_MCP
cls
echo Starting MCP Server...
start "MCP Server" python run_mcp_server.py
echo MCP Server started in new window!
pause
goto MENU

:START_FLASK
cls
echo Starting Flask API Server...
echo Access: http://localhost:5000
start "Flask API Server" python api_routes.py
echo Flask API Server started in new window!
pause
goto MENU

:START_ALL
cls
echo Starting ALL services...
echo.
call START_ALL_SERVICES.bat
goto MENU

:END
cls
echo.
echo Thank you for using Personal AI Employee Service Manager!
echo.
timeout /t 2 /nobreak >nul
exit
