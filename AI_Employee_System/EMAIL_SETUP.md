# ================================================================
# REAL EMAIL SERVICE - SETUP GUIDE
# ================================================================
# Send and receive real emails via SMTP/IMAP
# Works with Gmail, Outlook, Yahoo, and custom providers
# ================================================================

QUICK START (Gmail):
────────────────────────────────────────────────────────────────
1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification"
3. Go to "App passwords" (https://myaccount.google.com/apppasswords)
4. Select "Mail" and your device
5. Copy the 16-character password
6. Add to .env file below
────────────────────────────────────────────────────────────────

# ================================================================
# EMAIL CONFIGURATION
# ================================================================

# Your Gmail address
GMAIL_ADDRESS=your.email@gmail.com

# Gmail App Password (16 characters, no spaces)
# Get from: Google Account → Security → App passwords
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop

# Email provider (gmail, outlook, yahoo, custom)
EMAIL_PROVIDER=gmail

# ================================================================
# CUSTOM SMTP/IMAP (Optional - for non-Gmail providers)
# ================================================================

# Custom SMTP Server
CUSTOM_SMTP_SERVER=smtp.company.com
CUSTOM_SMTP_PORT=587

# Custom IMAP Server
CUSTOM_IMAP_SERVER=imap.company.com
CUSTOM_IMAP_PORT=993

# ================================================================
# CLI COMMANDS
# ================================================================

# Test connection:
cd "D:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System"
email.bat test

# Send email:
email.bat send --to recipient@example.com --subject "Hello" --body "Test message"

# Receive emails:
email.bat receive

# Compose email (interactive):
email.bat compose

# Show inbox:
email.bat inbox

# ================================================================
# SUPPORTED PROVIDERS
# ================================================================

# Gmail (default):
#   SMTP: smtp.gmail.com:587
#   IMAP: imap.gmail.com:993

# Outlook:
#   SMTP: smtp-mail.outlook.com:587
#   IMAP: outlook.office365.com:993

# Yahoo:
#   SMTP: smtp.mail.yahoo.com:465
#   IMAP: imap.mail.yahoo.com:993

# ================================================================
