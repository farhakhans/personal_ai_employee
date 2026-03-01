# 🥉 Bronze Tier - Features & Functionality

## Overview
**Bronze Tier** is the foundation tier with only **3 core features**:
1. Gmail Watcher
2. File Watcher
3. Vault System

---

## ✅ Features Included

### 1. **Gmail Watcher** 📧
**Purpose:** Monitor Gmail inbox for new emails

**Functionality:**
- Checks Gmail every 5 minutes
- Downloads email (sender, subject, body, date)
- Saves to `Vault/Inbox/EMAIL_*.md`
- Marks emails as processed

**Setup:**
1. Go to https://mail.google.com
2. Enable 2FA on Google Account
3. Generate App Password
4. Update `.env` file:
   ```env
   GMAIL_ADDRESS=your.email@gmail.com
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
   ```
5. Run: `python AI_Employee_System\Watchers\start_gmail_watcher.py`

**Direct Link:** [Open Gmail](https://mail.google.com)

---

### 2. **File Watcher** 📁
**Purpose:** Monitor file system for changes

**Functionality:**
- Watches specified folders
- Detects new/modified files
- Triggers actions based on file changes
- Logs all file operations

**Setup:**
1. Navigate to Watchers folder
2. Run: `python AI_Employee_System\Watchers\start_file_watcher.py`

**Direct Access:** [Open Vault Folder](file:///D:/DocuBook-Chatbot folder/Personal AI Employee/AI_Employee_System/Vault)

---

### 3. **Vault System** 🗄️
**Purpose:** Organized knowledge base (Obsidian vault)

**Folder Structure:**
```
Vault/
├── Dashboard.md              # Main status
├── Company_Handbook.md       # Business info
├── Inbox/                    # New items
│   ├── EMAIL_*.md
│   └── FILE_*.md
├── Needs_Action/             # To process
├── In_Progress/              # Currently working
├── Plans/                    # Action plans
├── Pending_Approval/         # Awaiting approval
├── Approved/                 # Ready to execute
└── Done/                     # Completed
```

**Functionality:**
- Central storage for all items
- Organized folder structure
- Markdown files for easy reading
- Full text search in Obsidian

**Direct Access:** Open in Obsidian or File Explorer

---

## ❌ NOT Included in Bronze

The following are **NOT** part of Bronze Tier (available in higher tiers):

- ❌ WhatsApp Integration (Silver+)
- ❌ LinkedIn Automation (Silver+)
- ❌ Twitter/X Posting (Silver+)
- ❌ Facebook Automation (Gold+)
- ❌ Instagram Posting (Gold+)
- ❌ Odoo Accounting (Gold+)
- ❌ Cloud 24/7 (Platinum+)

---

## 🚀 Quick Start Commands

### Run Gmail Watcher:
```batch
python AI_Employee_System\Watchers\start_gmail_watcher.py
```

### Run File Watcher:
```batch
python AI_Employee_System\Watchers\start_file_watcher.py
```

### Open Vault:
```batch
explorer "D:\DocuBook-Chatbot folder\Personal AI Employee\AI_Employee_System\Vault"
```

### Open Gmail:
```
https://mail.google.com
```

---

## 📊 Bronze Tier Workflow

```
1. Gmail Watcher polls every 5 min
   ↓
2. New email arrives
   ↓
3. Saved to Vault/Inbox/EMAIL_*.md
   ↓
4. User reviews in Vault
   ↓
5. Move to Needs_Action/ for processing
   ↓
6. Process and move to Done/
```

---

## 🎯 Bronze Tier Dashboard

Access the Bronze Tier dashboard at:
- `bronze_dashboard.html` - Full featured dashboard
- `all_tiers_form.html` - Select and compare tiers

**Dashboard Features:**
- Real-time vault statistics
- Watcher controls
- System status
- Task tracking
- Approvals pending

---

## 📋 Requirements

**Time Required:** 8-12 hours

**Prerequisites:**
- Gmail account
- Python 3.8+
- Obsidian (optional, for vault viewing)

**Files Needed:**
- `Watchers/gmail_watcher.py`
- `Watchers/file_watcher.py`
- `vault_manager.py`
- `.env` file with credentials

---

## 🔐 Security

✅ **DO:**
- Use App Password (not regular password)
- Enable 2FA on Gmail
- Keep `.env` file private
- Never commit `.env` to Git

❌ **DON'T:**
- Share Gmail credentials
- Use personal email for business
- Skip 2FA setup

---

## 📞 Support

**Documentation:**
- `GMAIL_SETUP_GUIDE.md` - Gmail setup instructions
- `ALL_TIERS_WORKFLOW.md` - Complete workflow guide
- `AI_Employee_System/Watchers/README.md` - Watcher docs

**Direct Links:**
- [Gmail](https://mail.google.com)
- [Google Account Security](https://myaccount.google.com/security)
- [Generate App Password](https://myaccount.google.com/apppasswords)

---

**Last Updated:** February 26, 2026
**Status:** ✅ Complete & Operational
