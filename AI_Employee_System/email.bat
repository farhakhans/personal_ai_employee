@echo off
REM REAL EMAIL SERVICE - CLI Launcher
REM Usage: email.bat [command] [options]

cd /d "%~dp0"

echo.
echo ================================================================
echo   REAL EMAIL SERVICE - CLI
echo   Send and Receive Real Emails
echo ================================================================
echo.

python real_email_service.py %*
