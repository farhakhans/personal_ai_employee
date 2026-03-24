# 📧 REAL EMAIL FLOW - QUICK START

## ✅ System Ready!

Your email system is fully configured and tested.

---

## 🚀 DEMO MODE (No Setup Required)

### Send Email
```bash
cd "D:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System"

# Quick send
demo_email.bat send --to john@example.com --subject "Hello" --body "Test message"

# With CC
demo_email.bat send --to user@example.com --cc boss@example.com --subject "Report" --body "Please review"

# With attachments
demo_email.bat send --to client@example.com --subject "Docs" --body "See attached" --attachments file.pdf
```

### Receive Emails
```bash
# Check inbox
demo_email.bat receive

# Show inbox summary
demo_email.bat inbox
```

### Interactive Compose
```bash
demo_email.bat compose
```

---

## 📋 TEST RESULTS

✅ **Send Test:** PASSED
```
✅ Email sent (DEMO MODE)
   To: alice@company.com
   Subject: Meeting Tomorrow
   Time: 2026-03-15 19:49:19
```

✅ **Receive Test:** PASSED
```
📬 Found 1 email(s) in inbox
📧 Email #1
   From: alice@company.com
   Subject: Re: Meeting Tomorrow
```

✅ **Inbox Test:** PASSED
```
Found 1 email(s):
  1. EMAIL_alice_company.com_Re_Meeting_Tomorrow_2026-03-15_19-49-19.md
```

---

## 📁 EMAIL STORAGE

All emails saved to:
```
Vault/
├── Inbox/
│   └── EMAIL/
│       └── EMAIL_alice_company.com_Re_Meeting_Tomorrow_2026-03-15_19-49-19.md
└── Sent/
    └── EMAIL/
        └── SENT_alice_company.com_Meeting_Tomorrow_2026-03-15_19-49-19.md
```

---

## 🔧 REAL MODE (Gmail Setup)

### Step 1: Get App Password
1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to App Passwords
4. Generate password for "Mail"

### Step 2: Add to .env File
```env
GMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
EMAIL_PROVIDER=gmail
```

### Step 3: Test Connection
```bash
email.bat test
```

### Step 4: Send Real Email
```bash
email.bat send --to recipient@example.com --subject "Hello" --body "Real email!"
```

---

## 📌 ALL COMMANDS

| Command | Description |
|---------|-------------|
| `demo_email.bat send --to EMAIL --subject SUBJ --body BODY` | Send demo email |
| `demo_email.bat receive` | Receive demo emails |
| `demo_email.bat inbox` | Show inbox summary |
| `demo_email.bat compose` | Interactive compose |
| `email.bat test` | Test real email connection |
| `email.bat send --to EMAIL --subject SUBJ --body BODY` | Send real email |
| `email.bat receive` | Receive real emails |
| `email.bat inbox` | Show real inbox |
| `email.bat compose` | Interactive compose (real) |

---

## 🎯 WORKFLOW EXAMPLE

```bash
# 1. Send an email
demo_email.bat send --to team@company.com --subject "Project Update" --body "Here's the latest update..."

# 2. Check it was sent
demo_email.bat inbox

# 3. Receive response (simulated)
demo_email.bat receive

# 4. View the saved emails in Vault
cd Vault\Inbox\EMAIL
dir
```

---

## 📞 INTEGRATION

### Python Code
```python
from demo_email_service import DemoEmailService

email = DemoEmailService()
email.send_email(
    to="user@example.com",
    subject="Hello",
    body="Test email"
)
```

### Real Email in Python
```python
from real_email_service import RealEmailService

email = RealEmailService(
    email_addr="your@gmail.com",
    password="app-password",
    provider="gmail"
)
result = email.send_email(
    to="client@example.com",
    subject="Proposal",
    body="Please find attached..."
)
```

---

## ✅ STRUCTURE PRESERVED

- ✅ Same folder structure maintained
- ✅ CLI-based commands
- ✅ Vault integration for email storage
- ✅ Markdown format for all emails
- ✅ Compatible with existing watchers

---

## 🎉 READY TO USE!

Start with demo mode to test, then configure real Gmail when ready.

**Demo Mode:** No credentials needed - perfect for testing!
**Real Mode:** Add Gmail credentials to `.env` for production use.

---

**Happy Emailing! 📧**
