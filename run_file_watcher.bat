@echo off
echo ================================================================
echo   FILE WATCHER - Starting...
echo ================================================================
echo.
cd /d "D:\DocuBook-Chatbot folder\Personal AI Employee"
echo Current directory: %CD%
echo.
echo Python executable: C:\Users\Hp\AppData\Local\Programs\Python\Python313\python.exe
echo Script: D:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System\Watchers\start_file_watcher.py
echo.
echo ================================================================
echo.
"C:\Users\Hp\AppData\Local\Programs\Python\Python313\python.exe" "D:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System\Watchers\start_file_watcher.py"
echo.
echo ================================================================
echo File Watcher has stopped.
echo Press any key to exit...
pause >nul
