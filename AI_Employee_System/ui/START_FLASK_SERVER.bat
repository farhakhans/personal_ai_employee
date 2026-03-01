@echo off
REM Start Flask UI Server
cd /d "D:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System\ui"
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         STARTING FLASK UI SERVER                              ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Server URL: http://localhost:5001
echo.
echo Available Routes:
echo   /              - Main page
echo   /tiers         - All Tiers Dashboard
echo   /run/gmail     - Run Gmail Watcher
echo   /run/whatsapp  - Run WhatsApp Watcher
echo   /run/linkedin  - Run LinkedIn Poster
echo   /run/hitl      - Run HITL Framework
echo.
echo Press Ctrl+C to stop the server
echo.
python flask_app.py
pause
