# 🚀 Individual Watcher CLI Commands

## Run Each Watcher Separately

### 1️⃣ Gmail Watcher
**Batch File:**
```bash
RUN_GMAIL_WATCHER.bat
```

**Python Command:**
```bash
python AI_Employee_System\Watchers\start_gmail_watcher.py
```

**Purpose:** Monitors Gmail inbox for new emails

---

### 2️⃣ File Watcher
**Batch File:**
```bash
RUN_FILE_WATCHER.bat
```

**Python Command:**
```bash
python AI_Employee_System\Watchers\start_file_watcher.py
```

**Purpose:** Monitors file system for changes

---

### 3️⃣ WhatsApp Watcher
**Batch File:**
```bash
RUN_WHATSAPP_WATCHER.bat
```

**Python Command:**
```bash
python AI_Employee_System\Watchers\start_whatsapp_watcher.py
```

**Purpose:** Monitors WhatsApp messages

---

### 4️⃣ MCP Server
**Batch File:**
```bash
RUN_MCP.bat
```

**Python Command:**
```bash
python run_mcp_server.py
```

**Purpose:** Email & Approval workflow API

---

## All Commands Summary

| Watcher | Batch Command | Python Command |
|---------|--------------|----------------|
| **Gmail** | `RUN_GMAIL_WATCHER.bat` | `python AI_Employee_System\Watchers\start_gmail_watcher.py` |
| **File** | `RUN_FILE_WATCHER.bat` | `python AI_Employee_System\Watchers\start_file_watcher.py` |
| **WhatsApp** | `RUN_WHATSAPP_WATCHER.bat` | `python AI_Employee_System\Watchers\start_whatsapp_watcher.py` |
| **MCP Server** | `RUN_MCP.bat` | `python run_mcp_server.py` |

---

## Run All Together

```bash
RUN_ALL_WATCHERS.bat
```

---

## Verify Running

Open browser and check:
```
http://localhost:5000/api/mcp/servers
```

---

**Quick Start - Run Any Watcher:**
```bash
RUN_GMAIL_WATCHER.bat
RUN_FILE_WATCHER.bat
RUN_WHATSAPP_WATCHER.bat
RUN_MCP.bat
```
