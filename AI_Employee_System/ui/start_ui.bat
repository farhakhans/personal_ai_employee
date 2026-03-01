@echo off
REM Start Flask UI and open tiers dashboard
cd /d "D:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System\ui"
echo Starting Flask UI Server...
start /B python app.py
timeout /t 3 /nobreak >nul
echo Opening Tiers Dashboard...
start http://localhost:5001/tiers
echo Done! Check your browser.
pause
