@echo off
REM Run Personal AI Employee System
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║           PERSONAL AI EMPLOYEE SYSTEM                         ║
echo ║                  Starting...                                  ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

cd /d "D:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System\ui"

echo Starting Flask Server on http://localhost:5001
echo.
echo Routes Available:
echo   /              - Main page
echo   /tiers         - All Tiers Dashboard  
echo   /run/gmail     - Run Gmail Watcher
echo   /run/whatsapp  - Run WhatsApp Watcher
echo   /run/linkedin  - Run LinkedIn Poster
echo   /run/hitl      - Run HITL Framework
echo.
echo Press Ctrl+C to stop
echo.

python flask_app.py

pause
