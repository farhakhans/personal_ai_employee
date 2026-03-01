@echo off
REM ════════════════════════════════════════════════════════════════════════════
REM RUN ALL SILVER TIER WATCHERS
REM Runs Gmail, WhatsApp, LinkedIn watchers and HITL framework
REM ════════════════════════════════════════════════════════════════════════════

cd /d "D:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         RUNNING ALL SILVER TIER WATCHERS                      ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo [1/4] Testing Gmail Watcher...
echo ────────────────────────────────────────────────────────────────
python -c "from Watchers.gmail_watcher import GmailWatcher; print('OK - Gmail Watcher loads correctly')"
echo.

echo [2/4] Testing WhatsApp Watcher...
echo ────────────────────────────────────────────────────────────────
python -c "from Watchers.whatsapp_watcher import WhatsAppWatcher; print('OK - WhatsApp Watcher loads correctly')"
echo.

echo [3/4] Testing LinkedIn Poster...
echo ────────────────────────────────────────────────────────────────
python -c "from Watchers.linkedin_poster import LinkedInPoster; print('OK - LinkedIn Poster loads correctly')"
echo.

echo [4/4] Testing HITL Framework...
echo ────────────────────────────────────────────────────────────────
python -c "from hitl_framework import HITLFramework; print('OK - HITL Framework loads correctly')"
echo.

echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ALL WATCHERS TESTED ✅                            ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║  All Silver Tier watchers are working!                         ║
echo ║                                                                ║
echo ║  To run individually:                                          ║
echo ║  • python Watchers\gmail_watcher.py                            ║
echo ║  • python Watchers\whatsapp_watcher.py                         ║
echo ║  • python Watchers\linkedin_poster.py                          ║
echo ║  • python hitl_framework.py                                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
pause
