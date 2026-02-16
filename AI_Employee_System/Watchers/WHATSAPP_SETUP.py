"""
WhatsApp Watcher Setup Guide
Quick setup for Playwright-based WhatsApp automation
"""

SETUP_STEPS = """
╔════════════════════════════════════════════════════════════════════════════╗
║                   WhatsApp Watcher - SETUP GUIDE                          ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 WHAT IT DOES:
   • Watches WhatsApp messages in real-time
   • Saves messages to Vault/Inbox/ automatically
   • Keeps track of processed messages
   • Can send replies automatically


⚠️  IMPORTANT - READ THIS:
   ✓ Uses WhatsApp Web automation (requires browser)
   ✓ Respects WhatsApp's terms (reads messages only)
   ⚠️  May trigger rate-limiting if left too aggressive
   ✓ Your phone stays connected
   ✓ No account takeover or password sharing


═══════════════════════════════════════════════════════════════════════════════

STEP 1: INSTALL REQUIREMENTS
─────────────────────────────────────────────────────────────────────────────

Run in Terminal:

    pip install playwright asyncio


STEP 2: INSTALL CHROMIUM BROWSER
─────────────────────────────────────────────────────────────────────────────

Run in Terminal:

    playwright install chromium


This downloads Chromium (~400 MB). One-time only.


STEP 3: RUN THE WATCHER
─────────────────────────────────────────────────────────────────────────────

Run in Terminal:

    cd "d:\\DocuBook-Chatbot folder\\Personal AI Employee\\AI_Employee_System"
    python Watchers/whatsapp_watcher.py


STEP 4: SCAN QR CODE
─────────────────────────────────────────────────────────────────────────────

   1. Browser window opens automatically
   2. You see a QR code
   3. Open WhatsApp on your phone
   4. Settings → Linked Devices → Link a Device
   5. Point phone camera at QR code on screen
   6. Confirm on phone


STEP 5: WATCH MESSAGES ARRIVE
─────────────────────────────────────────────────────────────────────────────

   ✅ Monitoring started!
   
   Every 5 seconds, the watcher checks for new messages.
   
   New messages appear here:
   → Vault/Inbox/WHATSAPP_[name]_[timestamp].md
   
   Example:
   → Vault/Inbox/WHATSAPP_John_Smith_2026-02-15-143022.md


═══════════════════════════════════════════════════════════════════════════════

INTEGRATE WITH YOUR SYSTEM
─────────────────────────────────────────────────────────────────────────────

Option A: RUN STANDALONE (Easiest)
   - Run whatsapp_watcher.py directly
   - Messages save automatically
   - Control with Ctrl+C

Option B: ADD TO ORCHESTRATOR (Recommended)
   - The orchestrator will start WhatsApp watcher automatically
   - See: orchestrator.py integration below


═══════════════════════════════════════════════════════════════════════════════

PYTHON CODE TO USE IN YOUR APP:
─────────────────────────────────────────────────────────────────────────────

from Watchers.whatsapp_watcher import WhatsAppWatcher
import asyncio

async def watch_whatsapp():
    watcher = WhatsAppWatcher(vault_path="./vault")
    
    # Launch browser and login
    success = await watcher.launch_browser()
    if not success:
        print("Failed to connect")
        return
    
    # Start watching
    await watcher.monitor_messages(poll_interval=5)

# Run it
asyncio.run(watch_whatsapp())


═══════════════════════════════════════════════════════════════════════════════

AVAILABLE FUNCTIONS:
─────────────────────────────────────────────────────────────────────────────

1. Launch Browser
   await watcher.launch_browser()
   → Opens WhatsApp Web, waits for QR scan


2. Get Recent Chats
   chats = await watcher.get_recent_chats(limit=5)
   → Returns list of recent conversations


3. Monitor Messages
   await watcher.monitor_messages(poll_interval=5)
   → Continuously watches for new messages


4. Send Message
   await watcher.send_message("John Smith", "Hello!")
   → Sends automated message to specific chat


5. Close Browser
   await watcher.close_browser()
   → Cleanup


═══════════════════════════════════════════════════════════════════════════════

TROUBLESHOOTING:
─────────────────────────────────────────────────────────────────────────────

❌ "Playwright not found"
   → Run: pip install playwright

❌ "Chromium not found"
   → Run: playwright install chromium

❌ QR code doesn't appear
   → Check internet connection
   → Try in Chrome/Chromium beforehand: https://web.whatsapp.com
   → Make sure WhatsApp is installed on phone

❌ "HeadlessError: Browser closed"
   → Browser crashed. Try again.
   → Check for Chrome updates

❌ Messages not saving
   → Check Vault/Inbox/ folder exists
   → Check file permissions
   → See console for error messages


═══════════════════════════════════════════════════════════════════════════════

BEST PRACTICES:
─────────────────────────────────────────────────────────────────────────────

✅ Leave phone connected to internet
✅ Don't disconnect device from WhatsApp while watcher runs
✅ Check messages every few seconds (poll_interval=5)
✅ Archive old messages regularly
✅ Monitor vault/Needs_Action/ for replies needed

❌ Don't press buttons on QR code screen
❌ Don't minimize browser while scanning QR
❌ Don't change poll interval too low (may throttle)
❌ Don't keep too many messages unprocessed


═══════════════════════════════════════════════════════════════════════════════

NEXT STEPS:
─────────────────────────────────────────────────────────────────────────────

If it works:

1. Try sending a message to yourself to test reply feature:
   await watcher.send_message("Your Name", "Test message")

2. Add to orchestrator for automatic startup

3. Create automation rules:
   - Save specific senders to Plans/
   - Auto-reply to common questions
   - Escalate urgent messages to Needs_Action/

═══════════════════════════════════════════════════════════════════════════════
""".strip()

if __name__ == "__main__":
    print(SETUP_STEPS)
    
    print("\n\n" + "="*80)
    print("QUICK START (Copy & Paste):")
    print("="*80)
    print("""
pip install playwright
playwright install chromium
cd "d:\\DocuBook-Chatbot folder\\Personal AI Employee\\AI_Employee_System"
python Watchers/whatsapp_watcher.py
    """)
