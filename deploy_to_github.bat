@echo off
echo ================================================================
echo   GitHub Deployment Script
echo   For: Personal AI Employee - Farha Khan
echo ================================================================
echo.

cd /d "%~dp0"

echo Step 1: Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)
echo [OK] Git is installed
echo.

echo Step 2: Initializing Git repository...
if not exist ".git" (
    git init
    echo [OK] Git repository initialized
) else (
    echo [OK] Git repository already exists
)
echo.

echo Step 3: Adding all files to Git...
git add .
echo [OK] All files added
echo.

echo Step 4: Creating commit...
git commit -m "Complete AI Employee System - Farha Khan
Features:
- Dashboard with animations
- Order Management System
- WhatsApp Automation
- Banking & Reconciliation
- Email Integration
- Auto-reconciliation
- Payment processing
- Auto-notifications"
echo [OK] Commit created
echo.

echo Step 5: Setting remote repository...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/farhakhans/Personal-AI-Employee.git
echo [OK] Remote repository set
echo.

echo Step 6: Pushing to GitHub...
echo [INFO] This may ask for your GitHub credentials
git branch -M main
git push -u origin main --force
echo.

if %errorlevel% equ 0 (
    echo ================================================================
    echo   SUCCESS! Files uploaded to GitHub
    echo ================================================================
    echo.
    echo Repository: https://github.com/farhakhans/Personal-AI-Employee
    echo.
    echo Next steps:
    echo 1. Visit your GitHub repository
    echo 2. Check all files are uploaded
    echo 3. Enable GitHub Pages for live demo
    echo.
) else (
    echo ================================================================
    echo   ERROR: Push failed!
    echo ================================================================
    echo.
    echo Possible solutions:
    echo 1. Make sure you're logged into GitHub
    echo 2. Check repository permissions
    echo 3. Try using GitHub Desktop instead
    echo.
)

echo ================================================================
pause
