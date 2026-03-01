# 🚀 CLI Commands - Run All Watchers

## Quick Start Commands

### Option 1: Batch File (Easiest)
```bash
RUN_ALL_WATCHERS.bat
```

### Option 2: Python Script
```bash
python run_all_watchers.py
```

### Option 3: Individual Commands
```bash
# Start all watchers one by one
python AI_Employee_System\Watchers\start_gmail_watcher.py
python AI_Employee_System\Watchers\start_file_watcher.py
python AI_Employee_System\Watchers\start_whatsapp_watcher.py
python run_mcp_server.py
```

---

## What Runs:

| Service | Description |
|---------|-------------|
| 📧 **Gmail Watcher** | Monitors Gmail for new emails |
| 📁 **File Watcher** | Monitors file system changes |
| 💬 **WhatsApp Watcher** | Monitors WhatsApp messages |
| 🤖 **MCP Server** | Email & Approval workflows |

---

## Verify Running:

Open browser and check:
```
http://localhost:5000/api/mcp/servers
```

Should show:
```json
{
  "status": "success",
  "servers": {
    "EmailServer": {...},
    "ApprovalServer": {...}
  }
}
```

---

## Stop Watchers:

**Method 1:** Close each console window

**Method 2:** Press `Ctrl+C` in each window

**Method 3:** Task Manager
```
Ctrl+Shift+Esc → Find Python → End Task
```

---

**Quick Start:**
```bash
RUN_ALL_WATCHERS.bat
```
