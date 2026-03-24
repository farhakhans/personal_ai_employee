@echo off
REM DEMO EMAIL SERVICE - CLI Launcher (No credentials needed)
REM Usage: demo_email.bat [command] [options]

cd /d "%~dp0"

echo.
echo ================================================================
echo   DEMO EMAIL SERVICE - CLI (TEST MODE)
echo   Send and Receive Emails WITHOUT Real Credentials
echo ================================================================
echo.

python demo_email_service.py %*
