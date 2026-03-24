@echo off
title Gmail Watcher Quick Test
color 0A

echo.
echo ======================================================================
echo              GMAIL WATCHER - QUICK SETUP TEST
echo ======================================================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo.
    echo Please create .env file with your Gmail credentials:
    echo   GMAIL_ADDRESS=your.email@gmail.com
    echo   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
    echo   NOTIFICATION_EMAIL=your.email@gmail.com
    echo.
    pause
    exit /b 1
)

echo [OK] .env file found
echo.

REM Check if credentials are set
findstr /C:"GMAIL_ADDRESS=your.email" ".env" >nul
if %errorlevel% equ 0 (
    echo [WARN] Gmail address not configured in .env
    echo.
    echo Please edit .env and set your actual Gmail address
    echo.
    pause
    exit /b 1
)

findstr /C:"GMAIL_APP_PASSWORD=xxxx" ".env" >nul
if %errorlevel% equ 0 (
    echo [WARN] Gmail app password not configured in .env
    echo.
    echo Please edit .env and set your Gmail app password
    echo.
    pause
    exit /b 1
)

echo [OK] Gmail credentials configured
echo.
echo ======================================================================
echo                      SETUP INSTRUCTIONS
echo ======================================================================
echo.
echo If you haven't set up Gmail yet, follow these steps:
echo.
echo 1. Enable 2-Factor Authentication:
echo    https://myaccount.google.com/security
echo.
echo 2. Generate App Password:
echo    Security -^> 2-Step Verification -^> App passwords
echo    Select: Mail and Other (Custom name)
echo    Copy the 16-character password
echo.
echo 3. Update .env file:
echo    GMAIL_ADDRESS=your.email@gmail.com
echo    GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
echo    NOTIFICATION_EMAIL=your.email@gmail.com
echo.
echo ======================================================================
echo.

:menu
echo Choose an option:
echo.
echo [1] Start Gmail Watcher (Receive + Send Notifications)
echo [2] Test Connection Only
echo [3] Open Gmail Setup Guide
echo [4] Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto start_watcher
if "%choice%"=="2" goto test_connection
if "%choice%"=="3" goto open_guide
if "%choice%"=="4" goto exit

echo Invalid choice!
goto menu

:start_watcher
echo.
echo Starting Gmail Watcher...
echo Emails will be saved to: Vault\Inbox\
echo Notifications will be sent to your Gmail
echo.
echo Press Ctrl+C to stop the watcher
echo.
timeout /t 3 /nobreak >nul
python AI_Employee_System\Watchers\start_gmail_watcher.py
goto menu

:test_connection
echo.
echo Testing Gmail connection...
python -c "import os; from dotenv import load_dotenv; load_dotenv(); from AI_Employee_System.Watchers.gmail_watcher import GmailWatcher; w = GmailWatcher(os.getenv('GMAIL_ADDRESS'), os.getenv('GMAIL_APP_PASSWORD'), os.getenv('VAULT_PATH')); imap = w.connect_gmail(); print('Connection:', 'SUCCESS' if imap else 'FAILED'); exit(0 if imap else 1)"
if %errorlevel% equ 0 (
    echo.
    echo [OK] Gmail connection successful!
    echo You can now start the watcher
) else (
    echo.
    echo [ERROR] Gmail connection failed!
    echo Please check your credentials in .env file
)
echo.
pause
goto menu

:open_guide
echo.
echo Opening setup guide...
if exist "GMAIL_WATCHER_SETUP.md" (
    start GMAIL_WATCHER_SETUP.md
    echo Guide opened in default browser
) else (
    echo [ERROR] Guide not found!
)
echo.
pause
goto menu

:exit
echo.
echo Exiting...
echo.
exit /b 0
