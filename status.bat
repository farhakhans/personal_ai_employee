@echo off
REM Quick Status Check - Windows Batch Script
REM Shows current system status without interactive mode

python quick_status.py %*

if errorlevel 1 (
    echo Error: Failed to display status.
    pause
)
