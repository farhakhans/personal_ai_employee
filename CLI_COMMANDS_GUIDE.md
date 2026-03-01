# 🚀 Personal AI Employee - CLI Run Commands

Complete guide to running all watchers, MCP servers, and services.

---

## 📋 Quick Start Commands

### Start Everything at Once
```bash
START_ALL_SERVICES.bat
```

---

## 🔍 Individual Watchers

### 1. Gmail Watcher
**Batch File:**
```bash
START_GMAIL_WATCHER.bat
```

**Command Line:**
```bash
python AI_Employee_System\Watchers\start_gmail_watcher.py
```

**Purpose:** Monitors Gmail inbox for new emails

---

### 2. File Watcher
**Batch File:**
```bash
START_FILE_WATCHER.bat
```

**Command Line:**
```bash
python AI_Employee_System\Watchers\start_file_watcher.py
```

**Purpose:** Monitors file system for changes

---

### 3. WhatsApp Watcher
**Batch File:**
```bash
START_WHATSAPP_WATCHER.bat
```

**Command Line:**
```bash
python AI_Employee_System\Watchers\start_whatsapp_watcher.py
```

**Purpose:** Monitors WhatsApp messages

---

## 🤖 MCP Servers

### MCP Server (Email + Approval)
**Batch File:**
```bash
RUN_MCP_SERVER.bat
```

**Command Line:**
```bash
python run_mcp_server.py
```

**Purpose:** Model Context Protocol server for email and approval workflows

---

## 🌐 Main API Server

### Flask API Server
**Command Line:**
```bash
python api_routes.py
```

**Purpose:** Main Flask API server with all endpoints

**Access URLs:**
- Dashboard: http://localhost:5000/
- Agent Skills: http://localhost:5000/agent-skills
- MCP Servers: http://localhost:5000/api/mcp/servers

---

## 📊 Social Media Posters (Gold Tier)

### Facebook Poster
```bash
python AI_Employee_System\Watchers\facebook_poster.py
```

### Instagram Poster
```bash
python AI_Employee_System\Watchers\instagram_poster.py
```

### LinkedIn Poster
```bash
python AI_Employee_System\Watchers\linkedin_poster.py
```

### Twitter Poster
```bash
python AI_Employee_System\Watchers\twitter_poster.py
```

---

## 🔧 API Test Commands

### Test MCP Servers API
```bash
# List all MCP servers
curl http://localhost:5000/api/mcp/servers

# Get Email Server capabilities
curl http://localhost:5000/api/mcp/EmailServer/capabilities

# Get Approval Server capabilities
curl http://localhost:5000/api/mcp/ApprovalServer/capabilities

# Execute email tool
curl -X POST http://localhost:5000/api/mcp/EmailServer/execute ^
  -H "Content-Type: application/json" ^
  -d "{\"tool\":\"send_email\",\"params\":{\"to\":\"test@example.com\",\"subject\":\"Test\",\"body\":\"Hello\"}}"
```

### Test Agent Skills API
```bash
# List all agent skills
curl http://localhost:5000/api/agent/skills

# Execute a skill
curl -X POST http://localhost:5000/api/agent/skills/VaultRead/execute ^
  -H "Content-Type: application/json" ^
  -d "{\"file_path\":\"test.md\"}"
```

### Test System Health
```bash
# Health check
curl http://localhost:5000/api/health

# Version info
curl http://localhost:5000/api/version
```

---

## 📁 Complete Service List

| Service | Batch File | Python Command | Port |
|---------|-----------|----------------|------|
| **Flask API** | - | `python api_routes.py` | 5000 |
| **MCP Server** | `RUN_MCP_SERVER.bat` | `python run_mcp_server.py` | - |
| **Gmail Watcher** | `START_GMAIL_WATCHER.bat` | `python AI_Employee_System/Watchers/start_gmail_watcher.py` | - |
| **File Watcher** | `START_FILE_WATCHER.bat` | `python AI_Employee_System/Watchers/start_file_watcher.py` | - |
| **WhatsApp Watcher** | `START_WHATSAPP_WATCHER.bat` | `python AI_Employee_System/Watchers/start_whatsapp_watcher.py` | - |
| **Facebook Poster** | - | `python AI_Employee_System/Watchers/facebook_poster.py` | - |
| **Instagram Poster** | - | `python AI_Employee_System/Watchers/instagram_poster.py` | - |
| **LinkedIn Poster** | - | `python AI_Employee_System/Watchers/linkedin_poster.py` | - |
| **Twitter Poster** | - | `python AI_Employee_System/Watchers/twitter_poster.py` | - |

---

## 🎯 Recommended Startup Order

1. **Start Flask API Server** (Required for all services)
   ```bash
   python api_routes.py
   ```

2. **Start MCP Server** (For email/approval workflows)
   ```bash
   python run_mcp_server.py
   ```

3. **Start Watchers** (As needed)
   ```bash
   python AI_Employee_System\Watchers\start_gmail_watcher.py
   python AI_Employee_System\Watchers\start_file_watcher.py
   python AI_Employee_System\Watchers\start_whatsapp_watcher.py
   ```

---

## 🛑 Stop Services

### Windows Task Manager
1. Press `Ctrl+Shift+Esc`
2. Find Python processes
3. End task

### Command Line
```bash
# Stop by process name
taskkill /F /IM python.exe

# Stop specific PID
taskkill /F /PID <process_id>
```

### Individual Windows
- Click on each console window
- Press `Ctrl+C`

---

## 📝 Notes

- **Prerequisites:** Python 3.8+ installed
- **Dependencies:** Run `pip install -r requirements.txt` first
- **Configuration:** Check `.env` file for API keys and settings
- **Logs:** Check console output for each service

---

## 🔗 Quick Links

- Dashboard: http://localhost:5000/
- Agent Skills: http://localhost:5000/agent-skills
- MCP API: http://localhost:5000/api/mcp/servers
- Health Check: http://localhost:5000/api/health

---

**Created for Personal AI Employee System**
**Last Updated:** March 1, 2026
