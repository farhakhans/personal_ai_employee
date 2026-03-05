@echo off
title Deploy to Vercel - Personal AI Employee
color 0A

echo ================================================================
echo         VERCEL DEPLOYMENT - Quick Setup
echo ================================================================
echo.
echo This script will:
echo   1. Initialize Git (if needed)
echo   2. Add all files
echo   3. Commit changes
echo   4. Help you push to GitHub
echo   5. Deploy to Vercel
echo.
echo ================================================================
echo.

cd /d "%~dp0"

echo Step 1: Checking Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed!
    echo Download from: https://git-scm.com
    pause
    exit /b 1
)
echo [OK] Git found
echo.

echo Step 2: Initializing Git repository...
if not exist ".git" (
    git init
    echo [OK] Git initialized
) else (
    echo [OK] Git already initialized
)
echo.

echo Step 3: Adding all files...
git add .
echo [OK] Files added
echo.

echo Step 4: Committing changes...
git commit -m "Deploy to Vercel - %date%"
echo [OK] Changes committed
echo.

echo Step 5: Checking Node.js (for Vercel CLI)...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN] Node.js not found!
    echo.
    echo Please install Node.js from: https://nodejs.org
    echo OR deploy manually at: https://vercel.com/new
    echo.
    goto MANUAL_DEPLOY
)
echo [OK] Node.js found
echo.

echo Step 6: Checking Vercel CLI...
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Vercel CLI not found. Installing...
    npm install -g vercel
)
echo [OK] Vercel CLI ready
echo.

echo Step 7: Logging in to Vercel...
vercel login
echo [OK] Logged in
echo.

echo Step 8: Deploying to Vercel...
echo.
echo ================================================================
echo    DEPLOYMENT STARTED
echo ================================================================
echo.
vercel --prod

echo.
echo ================================================================
echo    DEPLOYMENT COMPLETE!
echo ================================================================
echo.
echo Next Steps:
echo   1. Go to your Vercel dashboard
echo   2. Set environment variables:
echo      - ANTHROPIC_API_KEY
echo      - SECRET_KEY
echo      - GMAIL_ADDRESS (optional)
echo      - GMAIL_APP_PASSWORD (optional)
echo   3. Redeploy after setting variables
echo.
echo Dashboard: https://vercel.com/dashboard
echo.
pause
exit /b 0

:MANUAL_DEPLOY
echo ================================================================
echo    MANUAL DEPLOYMENT INSTRUCTIONS
echo ================================================================
echo.
echo 1. Go to: https://vercel.com/new
echo 2. Sign in with GitHub
echo 3. Import this repository
echo 4. Click Deploy
echo 5. Set environment variables
echo.
pause
exit /b 0
