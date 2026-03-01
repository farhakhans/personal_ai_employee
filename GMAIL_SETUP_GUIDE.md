# 📧 Gmail Watcher Setup Guide

## Quick Setup (5 minutes)

### Step 1: Enable 2FA on Google Account
1. Go to: https://myaccount.google.com/
2. Click **Security** (left sidebar)
3. Under "Signing in to Google", click **2-Step Verification**
4. Click **Get Started** and follow the steps
5. Enable 2-Step Verification

### Step 2: Generate App Password
1. After enabling 2FA, go back to **Security** page
2. Under "Signing in to Google", click **App passwords**
3. In the "App" dropdown, select **Mail**
4. In the "Device" dropdown, select **Windows Computer** (or your device)
5. Click **Generate**
6. Google will show a password like: `xxxx xxxx xxxx xxxx`
7. **Copy this password** (you won't see it again!)

### Step 3: Update .env File
1. Open: `D:\DocuBook-Chatbot folder\Personal AI Employee\.env`
2. Replace these lines:
   ```
   GMAIL_ADDRESS=your.email@gmail.com
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
   ```
3. With your actual credentials:
   ```
   GMAIL_ADDRESS=farha.khan@gmail.com
   GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
   ```
4. Save the file

### Step 4: Run Gmail Watcher
**Option 1: Batch File**
```batch
run_gmail_watcher.bat
```

**Option 2: Python**
```batch
python AI_Employee_System\Watchers\start_gmail_watcher.py
```

### Step 5: Check Emails
Emails will be saved to:
```
D:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System\Vault\Inbox\EMAIL_*.md
```

---

## Troubleshooting

### Error: "Authentication failed"
- Make sure you're using **App Password**, not regular password
- App password format: `xxxx xxxx xxxx xxxx` (16 characters with spaces)
- Regular password won't work!

### Error: "IMAP not enabled"
1. Go to Gmail Settings
2. See all settings → **Forwarding and POP/IMAP**
3. Enable **IMAP**
4. Save changes

### Error: ".env file not found"
1. Copy `.env.example` to `.env`
2. Edit `.env` with your credentials
3. Save and run again

---

## What Gmail Watcher Does

✅ **Monitors** your Gmail inbox every 5 minutes
✅ **Saves** new emails to Vault/Inbox/
✅ **Extracts** sender, subject, date, and body
✅ **Marks** emails as processed
✅ **Creates** markdown files for each email

### Example Output:
```markdown
---
From: client@example.com
Subject: Project Update
Date: 2026-02-26 10:30 AM
Status: New
---

Email body content here...
```

---

## Security Notes

🔒 **Never share your .env file**
🔒 **Keep app password secret**
🔒 **Use 2FA on your Google account**
🔒 **Rotate app passwords monthly**

---

## Next Steps

After Gmail Watcher is running:

1. **Send yourself a test email**
2. **Wait 5 minutes**
3. **Check Vault/Inbox/** - email will be there!
4. **Move important emails** to Vault/Needs_Action/
5. **Process emails** using AI Employee

---

**Need help?** Check the logs in the console window.
