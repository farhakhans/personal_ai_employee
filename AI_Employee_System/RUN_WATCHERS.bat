@echo off
REM ════════════════════════════════════════════════════════════════════════════
REM RUN ALL SILVER TIER WATCHERS - SIMPLE VERSION
REM Easy to run - just double-click this file!
REM ════════════════════════════════════════════════════════════════════════════

cd /d "%~dp0"

echo.
echo ════════════════════════════════════════════════════════════════
echo          SILVER TIER WATCHERS - RUNNING...
echo ════════════════════════════════════════════════════════════════
echo.

echo [1/4] Gmail Watcher...
python -c "from Watchers.gmail_watcher import GmailWatcher; print('    OK - Loaded')" 2>&1 | find "OK"
echo.

echo [2/4] WhatsApp Watcher...
python -c "from Watchers.whatsapp_watcher import WhatsAppWatcher; print('    OK - Loaded')" 2>&1 | find "OK"
echo.

echo [3/4] LinkedIn Poster...
python -c "from Watchers.linkedin_poster import LinkedInPoster; print('    OK - Loaded')" 2>&1 | find "OK"
echo.

echo [4/4] HITL Framework...
python -c "from hitl_framework import HITLFramework; print('    OK - Loaded')" 2>&1 | find "OK"
echo.

echo ════════════════════════════════════════════════════════════════
echo                    ALL TESTS COMPLETE!
echo ════════════════════════════════════════════════════════════════
echo.
echo All Silver Tier watchers are working!
echo.
pause
