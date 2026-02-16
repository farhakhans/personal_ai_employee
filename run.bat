@echo off
REM Personal AI Employee - Windows Batch Script
REM This script starts the Personal AI Employee system

echo.
echo ========================================
echo Personal AI Employee System
echo ========================================
echo.

python app.py %*

if errorlevel 1 (
    echo.
    echo Error: Python not found or script failed.
    echo Please ensure Python 3.8+ is installed.
    pause
)
