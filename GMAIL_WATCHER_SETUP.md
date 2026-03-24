# 📧 Gmail Watcher Setup Guide

## Overview
The Gmail Watcher monitors your Gmail inbox and:
- ✅ Receives real emails from Gmail
- ✅ Saves emails to your Vault/Inbox
- ✅ Sends email notifications when new emails arrive
- ✅ Runs continuously every 5 minutes
- ✅ Works via CLI commands

---

## Setup Steps

### Step 1: Enable 2-Factor Authentication on Gmail

1. Go to [Google Account](https://myaccount.google.com/)
2. Click **Security** in the left sidebar
3. Under "Signing in to Google", click **2-Step Verification**
4. Follow the steps to enable 2FA

### Step 2: Generate App Password

1. After enabling 2FA, go back to **Security**
2. Under "Signing in to Google", click **App passwords**
3. In the "App" dropdown, select **Mail**
4. In the "Device" dropdown, select **Other**
5. Enter a name like "AI Employee"
6. Click **Generate**
7. Copy the 16-character password (looks like: `xxxx xxxx xxxx xxxx`)

### Step 3: Create .env File

1. Navigate to your project folder:
   ```
   D:\DocuBook-Chatbot folder\Personal AI Employee
   ```

2. Create a new file named `.env` (no extension)

3. Add your credentials:
   ```env
   # Gmail Configuration
   GMAIL_ADDRESS=your.email@gmail.com
   GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
   NOTIFICATION_EMAIL=your.email@gmail.com
   ```

   **Important:**
   - Use your actual Gmail address
   - Paste the app password with spaces (or without, both work)
   - `NOTIFICATION_EMAIL` is where you'll receive alerts (can be same as Gmail)

### Step 4: Run Gmail Watcher

#### Option A: Using Batch File (Recommended)
```cmd
RUN_GMAIL_WATCHER.bat
```

Or:
```cmd
START_GMAIL_WATCHER.bat
```

#### Option B: Using Python CLI
```cmd
python AI_Employee_System\Watchers\start_gmail_watcher.py
```

#### Option C: From Dashboard
1. Open browser: `http://localhost:5000/`
2. Login to your account
3. Go to Silver Dashboard
4. Click "Run Gmail Watcher"

---

## How It Works

### Email Receiving
```
1. Watcher connects to Gmail via IMAP
2. Checks last 50 emails every 5 minutes
3. Downloads new emails (not previously processed)
4. Saves to: Vault/Inbox/EMAIL_*.md
```

### Email Notifications
```
1. When new email arrives
2. Watcher creates HTML notification
3. Sends to NOTIFICATION_EMAIL via Gmail SMTP
4. Includes: Sender, Subject, Body Preview
```

### File Structure
```
Vault/
└── Inbox/
    ├── EMAIL_12345.md      (New email from Gmail)
    ├── EMAIL_12346.md      (Another email)
    └── ...
```

---

## Testing

### Test Email Receiving

1. Start the Gmail Watcher
2. Send a test email to your Gmail from another email
3. Wait up to 5 minutes
4. Check console output for:
   ```
   📨 Found 1 new email(s)
   ✅ Saved to Inbox: EMAIL_12345
   📤 Notification sent to: your.email@gmail.com
   ```

5. Check `Vault/Inbox/` for new `.md` file
6. Check your Gmail for notification email

### Test Email Notification

1. Ensure `NOTIFICATION_EMAIL` is set in `.env`
2. Send test email to your Gmail
3. Check notification email inbox
4. You should receive an HTML formatted alert

---

## CLI Commands

### Start Watcher
```cmd
python AI_Employee_System\Watchers\start_gmail_watcher.py
```

### Check Status
```cmd
python -c "from AI_Employee_System.Watchers.gmail_watcher import GmailWatcher; import os; from dotenv import load_dotenv; load_dotenv(); w = GmailWatcher(os.getenv('GMAIL_ADDRESS'), os.getenv('GMAIL_APP_PASSWORD'), os.getenv('VAULT_PATH')); print('Connection test:', w.connect_gmail() is not None)"
```

### Run Once (Single Poll)
```cmd
python -c "from AI_Employee_System.Watchers.start_gmail_watcher import main; main()"
```

---

## Troubleshooting

### "Gmail credentials not found"
**Solution:** Make sure `.env` file exists in project root with correct variables

### "Authentication failed"
**Solution:** 
- Verify app password is correct
- Make sure 2FA is enabled on Gmail
- Try regenerating app password

### "IMAP connection failed"
**Solution:**
- Check internet connection
- Verify Gmail address is correct
- Ensure IMAP is enabled in Gmail settings

### No notifications received
**Solution:**
- Check `NOTIFICATION_EMAIL` in `.env`
- Verify SMTP is not blocked by firewall
- Check spam folder for notifications

### Emails not appearing in Vault
**Solution:**
- Check `VAULT_PATH` in `.env`
- Ensure Vault/Inbox folder exists
- Check console for error messages

---

## Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GMAIL_ADDRESS` | Your Gmail address | - | ✅ Yes |
| `GMAIL_APP_PASSWORD` | Gmail app password | - | ✅ Yes |
| `NOTIFICATION_EMAIL` | Email for alerts | GMAIL_ADDRESS | ❌ Optional |
| `VAULT_PATH` | Where to save emails | Auto-detected | ❌ Optional |

---

## Advanced: Custom Poll Interval

Edit `start_gmail_watcher.py` and change:
```python
watcher = GmailWatcher(
    ...
    poll_interval=60,  # Check every 60 seconds
    ...
)
```

---

## Security Notes

⚠️ **Important:**
- Never commit `.env` to Git
- Keep app password secret
- Use 2FA on your Gmail account
- App password is less secure than 2FA alone
- Consider using a dedicated Gmail account for business

---

## What Happens When

### When Email Arrives:
```
1. Gmail receives email
2. Watcher detects it (within 5 min)
3. Email saved to Vault/Inbox/
4. Notification sent to your email
5. Console shows: "📨 Found 1 new email(s)"
```

### When Watcher Starts:
```
1. Loads credentials from .env
2. Connects to Gmail IMAP
3. Loads list of already processed emails
4. Starts polling loop
5. Checks every 5 minutes
```

### When Watcher Stops (Ctrl+C):
```
1. Stops polling
2. Logs shutdown message
3. Processed emails list saved
4. Next start will resume from where it left
```

---

## Integration with Other Systems

### WhatsApp Notifications
You can also get WhatsApp alerts by integrating with the WhatsApp watcher.

### Email Auto-Reply
See `whatsapp_real_autoreply.py` for auto-reply patterns.

### Odoo Integration
Emails can trigger Odoo workflows (Gold tier+).

---

## Support

For issues:
1. Check console logs for errors
2. Verify `.env` configuration
3. Test Gmail connection manually
4. Review this guide

---

**Generated:** March 14, 2026
**Version:** 2.0
**Status:** Ready for Production
