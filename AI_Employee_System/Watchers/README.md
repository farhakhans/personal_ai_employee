"""
WATCHERS SYSTEM - All Available Message Monitors
═══════════════════════════════════════════════════════════════════════════

Your AI Employee can watch MULTIPLE communication channels automatically.

This folder contains all watchers with different features:
"""

WATCHERS_INFO = """

╔═══════════════════════════════════════════════════════════════════════════╗
║                          AVAILABLE WATCHERS                              ║
╚═══════════════════════════════════════════════════════════════════════════╝

1️⃣  EMAIL WATCHER (gmail_watcher.py)
   ├─ Method: IMAP (Gmail API)
   ├─ Watches: Your Gmail inbox
   ├─ Saves to: Vault/Inbox/EMAIL_*.md
   ├─ Setup: Google OAuth credentials needed
   ├─ Tier: Bronze ✓ Ready
   └─ Command: python start_bronze.py

2️⃣  WHATSAPP WATCHER - WEB (whatsapp_watcher.py) 🆕
   ├─ Method: Playwright automation (browser-based)
   ├─ Watches: Personal WhatsApp messages in real-time
   ├─ Saves to: Vault/Inbox/WHATSAPP_*.md
   ├─ Setup: QR code scan (no password needed)
   ├─ Tier: Silver
   └─ Command: python start_whatsapp_watcher.py

3️⃣  WHATSAPP WATCHER - API (multi_watchers.py)
   ├─ Method: Meta WhatsApp Business API
   ├─ Watches: Business account messages
   ├─ Saves to: Vault/Inbox/WHATSAPP_*.md
   ├─ Setup: Facebook App credentials
   ├─ Best for: Business messaging
   └─ Note: Requires Meta Business Account

4️⃣  LINKEDIN WATCHER (linkedin_poster.py)
   ├─ Method: LinkedIn API
   ├─ Watches: Mentions, comments, messages
   ├─ Saves to: Vault/Inbox/LINKEDIN_*.md
   ├─ Setup: LinkedIn Developer credentials
   ├─ Tier: Silver
   └─ Note: Phase 2 implementation

5️⃣  TWITTER WATCHER (multi_watchers.py)
   ├─ Method: Twitter/X API
   ├─ Watches: Mentions, replies, DMs
   ├─ Saves to: Vault/Inbox/TWITTER_*.md
   ├─ Setup: Twitter API v2 credentials
   ├─ Tier: Silver+
   └─ Note: Phase 2 implementation

6️⃣  FILE SYSTEM WATCHER (file_watcher.py) 🆕
   ├─ Method: Local directory monitoring
   ├─ Watches: Dropped files in a monitored folder
   ├─ Saves to: Vault/Inbox/FILE_DROP_*.md
   ├─ Setup: No credentials needed!
   ├─ Tier: Bronze/Silver
   ├─ Supported: Documents, images, code, spreadsheets, archives
   └─ Command: python Watchers/start_file_watcher.py


╔═══════════════════════════════════════════════════════════════════════════╗
║                      WHICH ONE SHOULD YOU USE?                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

If your clients mainly contact you via:

  📧 Gmail or Email      → Use: gmail_watcher.py
  📱 WhatsApp (Personal) → Use: whatsapp_watcher.py
  💼 WhatsApp (Business) → Use: Meta WhatsApp API
  🔗 LinkedIn Messages   → Use: linkedin_poster.py
  🐦 Twitter/X DMs      → Use: multi_watchers.py
  📁 File Drops/Shares  → Use: file_watcher.py (NEW!)


╔═══════════════════════════════════════════════════════════════════════════╗
║                      QUICK START COMMANDS                                ║
╚═══════════════════════════════════════════════════════════════════════════╝

1. RUN EMAIL WATCHER (Ready Now):
   ─────────────────────────────────────────────────
   cd "d:\\DocuBook-Chatbot folder\\Personal AI Employee\\AI_Employee_System"
   python start_bronze.py


2. RUN WHATSAPP WATCHER (Just Added):
   ─────────────────────────────────────────────────
   pip install playwright
   playwright install chromium
   python Watchers/start_whatsapp_watcher.py


3. SEE WHATSAPP SETUP GUIDE:
   ─────────────────────────────────────────────────
   python Watchers/WHATSAPP_SETUP.py


4. RUN FILE SYSTEM WATCHER (Just Added):
   ─────────────────────────────────────────────────
   python Watchers/start_file_watcher.py
   (No credentials needed! Just drop files into Vault/Inbox/Drops/)


5. RUN ALL WATCHERS (Silver Tier):
   ─────────────────────────────────────────────────
   python start_silver.py
   (Once you configure all APIs)


╔═══════════════════════════════════════════════════════════════════════════╗
║                      CONFIGURATION                                       ║
╚═══════════════════════════════════════════════════════════════════════════╝

Edit these files to configure credentials:

File: .env (in AI_Employee_System folder)
──────────────────────────────────────────

ANTHROPIC_API_KEY=sk-ant-...your-key...

# Gmail
GMAIL_EMAIL=your@gmail.com
GMAIL_PASSWORD=your-app-password

# WhatsApp Web (Playwright) - No config needed (uses QR code)

# WhatsApp Business API (optional)
WHATSAPP_PHONE_NUMBER_ID=123456789
WHATSAPP_BUSINESS_API_TOKEN=wbl_...

# LinkedIn
LINKEDIN_ACCESS_TOKEN=...

# Twitter/X
TWITTER_API_KEY=...
TWITTER_API_SECRET=...


╔═══════════════════════════════════════════════════════════════════════════╗
║                      HOW WATCHERS WORK                                   ║
╚═══════════════════════════════════════════════════════════════════════════╝

Every watcher follows this flow:

  1. MONITOR (Every 5-10 seconds)
     └─ Check for new messages on the platform

  2. FETCH (If new messages found)
     └─ Download message details (text, sender, timestamp)

  3. PROCESS (Extract important info)
     └─ Sender name, message content, attachment names

  4. SAVE (Create markdown file)
     └─ File: Vault/Inbox/[PLATFORM]_[sender]_[timestamp].md

  5. MARK PROCESSED (Remember for next check)
     └─ Avoid saving same message twice

  6. NOTIFY (Optional - to AI)
     └─ "New message from John Smith in WhatsApp"


╔═══════════════════════════════════════════════════════════════════════════╗
║                      FILE STRUCTURE                                      ║
╚═══════════════════════════════════════════════════════════════════════════╝

Watchers/
├── gmail_watcher.py              (Email monitoring - READY ✓)
├── whatsapp_watcher.py           (WhatsApp Web - READY ✓)
├── start_whatsapp_watcher.py     (WhatsApp launcher)
├── WHATSAPP_SETUP.py             (WhatsApp setup guide)
├── file_watcher.py               (File system monitoring - NEW 🆕)
├── start_file_watcher.py         (File watcher launcher)
├── FILE_WATCHER_SETUP.py         (File watcher setup guide)
├── multi_watchers.py             (Other platforms template)
├── linkedin_poster.py            (LinkedIn integration)
├── task_scheduler.py             (Run watchers on schedule)
└── README.md                      (This file)


╔═══════════════════════════════════════════════════════════════════════════╗
║                      FILE EXAMPLES                                       ║
╚═══════════════════════════════════════════════════════════════════════════╝

When a message arrives, it creates a file like:

📄 Vault/Inbox/EMAIL_john@company.com_2026-02-15-143022.md
───────────────────────────────────────────────────────────
# Email from john@company.com

**Subject:** Project Update
**From:** john@company.com
**Date:** 2026-02-15 14:30:22
**Source:** Gmail
**Message ID:** ...

## Content

Hi, can you review the latest design?
Check attachment.pdf

## Status
- [ ] Read
- [ ] Reply
- [ ] Archive

---

📄 Vault/Inbox/WHATSAPP_John_Smith_2026-02-15-143022.md
──────────────────────────────────────────────────────
# WhatsApp Message

**From:** John Smith
**Time:** 14:30:22
**Date Added:** 2026-02-15T14:30:22
**Source:** WhatsApp Web
**Message ID:** ...

## Content

Hi! Are you available for a call?

## Status
- [ ] Read
- [ ] Process
- [ ] Archive

## Notes


📄 Vault/Inbox/FILE_DROP_contract_2026-02-15-143022.md
──────────────────────────────────────────────────────
# File Drop: contract.pdf

**Received:** 2026-02-15T14:30:22
**File Size:** 245600 bytes
**File Type:** pdf
**Original Path:** Vault/Inbox/Drops/contract.pdf

## Metadata
```json
{
  "type": "pdf",
  "pages": 5,
  "size_bytes": 245600
}
```

## Status
- [ ] Review
- [ ] Action
- [ ] Archive

## Action Items
- What should AI Employee do with this file?
- Extract key terms and dates
- Route to legal for review

## Notes


╔═══════════════════════════════════════════════════════════════════════════╗
║                      WHAT HAPPENS NEXT                                   ║
╚═══════════════════════════════════════════════════════════════════════════╝

Your orchestrator (AI brain) will:

1. DETECT new files in Vault/Inbox/
2. READ the message
3. DECIDE what to do (reply, escalate, archive)
4. TAKE ACTION (save to Plans/, mark as Done/, etc.)
5. NOTIFY you if action needed

So:
  Incoming Message → Saved to Inbox/ → AI processes → Auto-response

Easy! 🎯


╔═══════════════════════════════════════════════════════════════════════════╗
║                      TROUBLESHOOTING                                     ║
╚═══════════════════════════════════════════════════════════════════════════╝

❌ Watcher running but no messages saved?
   → Check Vault/Inbox/ folder exists
   → Check permissions (read/write access)
   → Check .env credentials are correct
   → Try: restart watcher

❌ Sees messages but not saving to Vault?
   → Check VAULT_PATH in code
   → Ensure Vault/ folder exists
   → Check file permissions

❌ Creating duplicate message files?
   → Watcher is working! Mark as processed
   → Check for old .processed files

❌ One watcher crashes, others stop?
   → Run watchers in separate terminal windows
   → Or use task_scheduler.py

"""

if __name__ == "__main__":
    print(WATCHERS_INFO)
