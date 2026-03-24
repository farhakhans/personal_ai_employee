# 🚀 Gmail Watcher - Quick Start

## 3-Step Setup

### 1️⃣ Get Gmail App Password
1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification**
3. Click **App passwords**
4. Generate password for "Mail"
5. Copy the 16-character password

### 2️⃣ Edit .env File
Open `.env` and replace:
```env
GMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
NOTIFICATION_EMAIL=your.email@gmail.com
```

### 3️⃣ Run It
```cmd
TEST_GMAIL_SETUP.bat
```
Choose option [1] to start the watcher

---

## What You Get

✅ **Receive Emails** - Real emails from Gmail  
✅ **Send Notifications** - Email alerts when new mail arrives  
✅ **Save to Vault** - Emails stored in `Vault/Inbox/`  
✅ **CLI Support** - Works on localhost  

---

## Commands

| Command | Purpose |
|---------|---------|
| `TEST_GMAIL_SETUP.bat` | Test configuration |
| `RUN_GMAIL_WATCHER.bat` | Start watcher |
| `python AI_Employee_System\Watchers\start_gmail_watcher.py` | Python CLI |

---

## Testing

1. Start watcher
2. Send email to your Gmail
3. Wait 5 minutes
4. Check:
   - Console output
   - `Vault/Inbox/` folder
   - Notification email

---

## Need Help?

- **Full Guide:** `GMAIL_WATCHER_SETUP.md`
- **Details:** `GMAIL_CONFIGURATION_COMPLETE.md`
- **Test:** `TEST_GMAIL_SETUP.bat`

---

**Ready to go! Just fill in your Gmail credentials in `.env`**
