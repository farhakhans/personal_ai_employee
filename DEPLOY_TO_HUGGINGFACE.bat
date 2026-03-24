@echo off
REM ================================================
REM Hugging Face Spaces Deployment Script
REM Personal AI Employee
REM ================================================

echo.
echo ================================================================
echo   PERSONAL AI EMPLOYEE - Hugging Face Deployment
echo ================================================================
echo.

REM Check if huggingface-cli is installed
where huggingface-cli >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Hugging Face CLI not found!
    echo.
    echo Installing huggingface_hub...
    pip install huggingface_hub
    echo.
)

REM Login to Hugging Face
echo [+] Logging into Hugging Face...
huggingface-cli login

echo.
echo [+] Enter your Space name (e.g., personal-ai-employee):
set /p SPACE_NAME=

echo.
echo [+] Enter your Hugging Face username:
set /p HF_USERNAME=

echo.
echo [+] Creating Space repository...
git init
git remote add huggingface https://huggingface.co/spaces/%HF_USERNAME%/%SPACE_NAME%

echo.
echo [+] Pushing to Hugging Face Spaces...
git add -A
git commit -m "Deploy to Hugging Face Spaces"
git push -u huggingface main

echo.
echo ================================================================
echo   Deployment Complete!
echo ================================================================
echo.
echo   Your app is deploying at:
echo   https://huggingface.co/spaces/%HF_USERNAME%/%SPACE_NAME%
echo.
echo   Note: First deployment may take 5-10 minutes
echo ================================================================
echo.
pause
