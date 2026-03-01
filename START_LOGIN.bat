@echo off
echo =====================================
echo   AI EMPLOYEE SYSTEM - LOGIN TEST
echo =====================================
echo.
echo Starting server...
echo.

REM Kill any existing Python processes on port 5000
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Start the server
start "AI Employee Server" cmd /k "cd /d %~dp0 && python api_routes.py"

echo Waiting for server to start...
timeout /t 5 /nobreak >nul

echo.
echo Server started! Opening login page in browser...
echo.
echo IMPORTANT: Use these credentials:
echo   Email: admin@employee.ai
echo   Password: Admin@2026!
echo.
echo =====================================
echo.

REM Open the login page directly
start http://localhost:5000/login-page

echo Browser opened!
echo.
echo If you see "Token missing" error, press Ctrl+F5 to hard refresh!
echo.
pause
