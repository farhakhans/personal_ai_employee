@echo off
REM ════════════════════════════════════════════════════════════════════════════
REM PERSONAL AI EMPLOYEE - START ALL DASHBOARDS
REM Starts Flask UI server and opens all dashboards in browser
REM ════════════════════════════════════════════════════════════════════════════

cd /d "D:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System\ui"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║    PERSONAL AI EMPLOYEE - STARTING ALL DASHBOARDS             ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Stop any existing Flask servers
taskkill /F /IM python.exe 2>nul
timeout /t 1 /nobreak >nul

echo [1/4] Starting Flask UI Server...
start /B python flask_app.py
timeout /t 3 /nobreak >nul

echo [2/4] Opening Main Dashboard...
start http://localhost:5001/

echo [3/4] Opening Tiers Dashboard...
start http://localhost:5001/tiers

echo [4/4] Opening Platinum Dashboard...
start http://localhost:5001/tier/platinum

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                 ALL DASHBOARDS STARTED ✅                     ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║  Flask UI Server: http://localhost:5001                        ║
echo ║                                                                ║
echo ║  Available Dashboards:                                         ║
echo ║  • Main (Social Poster):  http://localhost:5001/               ║
echo ║  • All Tiers:             http://localhost:5001/tiers          ║
echo ║  • Platinum:              http://localhost:5001/tier/platinum  ║
echo ║  • Complete:              http://localhost:5001/dashboard      ║
echo ║                                                                ║
echo ║  To stop server: taskkill /F /IM python.exe                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
pause
