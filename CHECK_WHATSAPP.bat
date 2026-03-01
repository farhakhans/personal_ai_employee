@echo off
color 0A
echo ================================================================
echo           WhatsApp Manager - Status Check
echo ================================================================
echo.

:: Check if server is running
curl -s -o nul http://localhost:5000/whatsapp-manager
if %errorlevel% equ 0 (
    echo [OK] Server is running on port 5000
    echo.
    echo ================================================================
    echo           WhatsApp Manager is ACCESSIBLE!
    echo ================================================================
    echo.
    echo Open in your browser:
    echo   http://localhost:5000/whatsapp-manager
    echo.
    echo Or press any key to open it now...
    pause > nul
    start http://localhost:5000/whatsapp-manager
) else (
    echo [ERROR] Server is NOT running!
    echo.
    echo ================================================================
    echo           Starting WhatsApp Server...
    echo ================================================================
    echo.
    start python run_server.py
    echo Waiting for server to start...
    timeout /t 5 /nobreak > nul
    echo.
    echo Now opening WhatsApp Manager...
    start http://localhost:5000/whatsapp-manager
)

echo.
echo ================================================================
