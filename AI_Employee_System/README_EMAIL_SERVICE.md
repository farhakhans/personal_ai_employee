# 📧 REAL EMAIL FLOW - Complete Guide

## Overview

Two modes available:
1. **Demo Mode** - Test without credentials (recommended for testing)
2. **Real Mode** - Send/receive real emails via SMTP/IMAP

---

## 🚀 QUICK START (Demo Mode - No Setup Required)

### Step 1: Send Your First Email

```bash
cd "D:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System"

# Send a test email
demo_email.bat send --to john@example.com --subject "Hello" --body "This is a test email"
```

### Step 2: Check Inbox

```bash
demo_email.bat inbox
```

### Step 3: Receive Emails

```bash
demo_email.bat receive
```

### Step 4: Interactive Compose

```bash
demo_email.bat compose
```

---

## 📋 ALL CLI COMMANDS

### Demo Mode (No Credentials)

| Command | Description |
|---------|-------------|
| `demo_email.bat send --to EMAIL --subject SUBJ --body BODY` | Send email |
| `demo_email.bat receive` | Receive emails |
| `demo_email.bat inbox` | Show inbox summary |
| `demo_email.bat compose` | Interactive compose |

### Real Mode (Requires Gmail Setup)

| Command | Description |
|---------|-------------|
| `email.bat test` | Test SMTP/IMAP connection |
| `email.bat send --to EMAIL --subject SUBJ --body BODY` | Send real email |
| `email.bat receive` | Receive real emails |
| `email.bat inbox` | Show inbox |
| `email.bat compose` | Interactive compose |

---

## 🔧 REAL MODE SETUP (Gmail)

### Step 1: Enable 2-Step Verification

1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification**

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Select **Mail** and your device
3. Copy the **16-character password**

### Step 3: Add to .env File

Create/edit `.env` file:

```env
# Email Configuration
GMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
EMAIL_PROVIDER=gmail
```

### Step 4: Test Connection

```bash
email.bat test
```

### Step 5: Send Real Email

```bash
email.bat send --to recipient@example.com --subject "Hello" --body "Real email test"
```

---

## 📌 ADVANCED USAGE

### Send with CC

```bash
email.bat send --to user@example.com --cc boss@example.com --subject "Report" --body "Please review"
```

### Send with Attachments

```bash
email.bat send --to client@example.com --subject "Documents" --body "Attached files" --attachments file1.pdf file2.docx
```

### Send HTML Email

```bash
email.bat send --to user@example.com --subject "Newsletter" --body "<h1>Hello</h1><p>HTML content</p>" --html
```

### Receive All Emails (Including Read)

```bash
email.bat receive --all --limit 20
```

---

## 📁 EMAIL STORAGE

Emails are saved to:

```
Vault/
├── Inbox/
│   └── EMAIL/
│       ├── EMAIL_sender_example_com_Subject_2026-03-15_14-30-22.md
│       └── ...
├── Sent/
│   └── EMAIL/
│       ├── SENT_recipient_example_com_Subject_2026-03-15_14-30-22.md
│       └── ...
└── Demo/
    └── EMAIL/
        └── (demo emails)
```

### Email File Format

```markdown
# Email - RECEIVED

## Header
- **Subject:** Hello
- **From:** john@example.com
- **To:** you@gmail.com
- **Date:** 2026-03-15 14:30:22
- **Timestamp:** 2026-03-15T14:30:22

## Content

This is the email body content...

## Metadata
- **Has Attachments:** false
- **Format:** Plain Text

## Status
- [ ] Read
- [ ] Processed
- [ ] Archived
```

---

## 🌐 SUPPORTED EMAIL PROVIDERS

### Gmail (Default)
```
SMTP: smtp.gmail.com:587
IMAP: imap.gmail.com:993
```

### Outlook
```
SMTP: smtp-mail.outlook.com:587
IMAP: outlook.office365.com:993
```

### Yahoo
```
SMTP: smtp.mail.yahoo.com:465
IMAP: imap.mail.yahoo.com:993
```

### Custom Provider

Add to `.env`:

```env
EMAIL_PROVIDER=custom
CUSTOM_SMTP_SERVER=smtp.company.com
CUSTOM_SMTP_PORT=587
CUSTOM_IMAP_SERVER=imap.company.com
CUSTOM_IMAP_PORT=993
```

---

## 🧪 TESTING WORKFLOW

### 1. Test with Demo Mode First

```bash
# Send test email
demo_email.bat send --to test@example.com --subject "Demo Test" --body "Testing demo mode"

# Check it was saved
demo_email.bat inbox

# Receive (simulated response)
demo_email.bat receive
```

### 2. Then Test Real Mode

```bash
# Test connection
email.bat test

# Send to yourself
email.bat send --to your.email@gmail.com --subject "Self Test" --body "Testing real email"

# Check inbox
email.bat receive
```

---

## ❌ TROUBLESHOOTING

### SMTP Authentication Failed

```
❌ SMTP Authentication failed. Check email and password.
```

**Solution:**
- Use **App Password**, not regular password
- Enable 2-Step Verification first
- Check for typos in email address

### IMAP Connection Failed

```
❌ IMAP connection failed: [AUTHENTICATIONFAILED]
```

**Solution:**
- Regenerate app password
- Wait 5 minutes after creating new password
- Check IMAP is enabled in Gmail settings

### Module Not Found

```
ModuleNotFoundError: No module named 'dotenv'
```

**Solution:**
```bash
pip install python-dotenv
```

---

## 📞 INTEGRATION WITH EXISTING SYSTEM

### Use in Python Code

```python
from real_email_service import RealEmailService

# Initialize
email_service = RealEmailService(
    email_addr="your.email@gmail.com",
    password="app-password",
    provider="gmail"
)

# Send email
result = email_service.send_email(
    to="client@example.com",
    subject="Project Update",
    body="Hi, here's the update...",
    html=False
)

# Receive emails
emails = email_service.receive_emails(limit=10)

for email in emails:
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
```

### Use Demo in Code

```python
from demo_email_service import DemoEmailService

demo = DemoEmailService()
demo.send_email(
    to="test@example.com",
    subject="Test",
    body="Demo email"
)
```

---

## 🎯 BEST PRACTICES

1. **Always test with Demo Mode first**
2. **Keep App Password secure** - never commit to Git
3. **Use descriptive subjects** for easy tracking
4. **Check Vault folders** regularly for saved emails
5. **Mark emails as processed** using the checkboxes

---

## 📊 COMPARISON

| Feature | Demo Mode | Real Mode |
|---------|-----------|-----------|
| Credentials Required | ❌ No | ✅ Yes |
| Sends Real Emails | ❌ No | ✅ Yes |
| Receives Real Emails | ❌ Simulated | ✅ Yes |
| Saves to Vault | ✅ Yes | ✅ Yes |
| Good For | Testing, Development | Production Use |

---

## 🎉 SUCCESS INDICATORS

### Demo Mode Success
```
✅ Email sent (DEMO MODE)
   To: john@example.com
   Subject: Hello
   Time: 2026-03-15 14:30:22
   Location: D:\...\Vault\Sent\EMAIL
```

### Real Mode Success
```
✅ Email sent successfully to john@example.com!
   Subject: Hello
   Time: 2026-03-15T14:30:22
```

### Connection Test Success
```
===============================================================
RESULTS:
  SMTP (Send): ✅ Connected
  IMAP (Receive): ✅ Connected
===============================================================

✅ All connections successful!
```

---

## 📚 RELATED FILES

- `real_email_service.py` - Real email sending/receiving
- `demo_email_service.py` - Demo/testing mode
- `email.bat` - CLI launcher for real mode
- `demo_email.bat` - CLI launcher for demo mode
- `EMAIL_SETUP.md` - Setup instructions
- `.env` - Your credentials (create from .env.example)

---

**Happy Emailing! 📧**
