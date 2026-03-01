# 🚀 Personal AI Employee - Complete CLI Commands

## 📋 Quick Reference

### Run All Watchers Together
```bash
RUN_ALL_WATCHERS.bat
```

---

## 🔍 Individual Watcher Commands

### 1. Gmail Watcher 📧
```bash
RUN_GMAIL_WATCHER.bat
```
**Python:** `python AI_Employee_System\Watchers\start_gmail_watcher.py`

---

### 2. File Watcher 📁
```bash
RUN_FILE_WATCHER.bat
```
**Python:** `python AI_Employee_System\Watchers\start_file_watcher.py`

---

### 3. WhatsApp Watcher 💬
```bash
RUN_WHATSAPP_WATCHER.bat
```
**Python:** `python AI_Employee_System\Watchers\start_whatsapp_watcher.py`

---

### 4. MCP Server 🤖
```bash
RUN_MCP.bat
```
**Python:** `python run_mcp_server.py`

---

## 🌐 Main API Server

### Flask API
```bash
python api_routes.py
```
**Access:** http://localhost:5000

---

## 📊 All Commands Table

| Service | Batch File | Python Command |
|---------|-----------|----------------|
| **All Watchers** | `RUN_ALL_WATCHERS.bat` | `python run_all_watchers.py` |
| **Gmail Watcher** | `RUN_GMAIL_WATCHER.bat` | `python AI_Employee_System\Watchers\start_gmail_watcher.py` |
| **File Watcher** | `RUN_FILE_WATCHER.bat` | `python AI_Employee_System\Watchers\start_file_watcher.py` |
| **WhatsApp Watcher** | `RUN_WHATSAPP_WATCHER.bat` | `python AI_Employee_System\Watchers\start_whatsapp_watcher.py` |
| **MCP Server** | `RUN_MCP.bat` | `python run_mcp_server.py` |
| **Flask API** | - | `python api_routes.py` |

---

## 🔧 API Test Commands

### Test MCP Servers
```bash
curl http://localhost:5000/api/mcp/servers
```

### Test Agent Skills
```bash
curl http://localhost:5000/api/agent/skills
```

### Health Check
```bash
curl http://localhost:5000/api/health
```

---

## 🛑 Stop Services

**Method 1:** Close console window

**Method 2:** Press `Ctrl+C` in console

**Method 3:** Task Manager
```
Ctrl+Shift+Esc → Find Python → End Task
```

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `RUN_ALL_WATCHERS.bat` | Start all watchers |
| `run_all_watchers.py` | Python script for all watchers |
| `RUN_GMAIL_WATCHER.bat` | Gmail watcher only |
| `RUN_FILE_WATCHER.bat` | File watcher only |
| `RUN_WHATSAPP_WATCHER.bat` | WhatsApp watcher only |
| `RUN_MCP.bat` | MCP server only |
| `WATCHER_COMMANDS.md` | Individual commands guide |
| `CLI_COMMANDS_GUIDE.md` | Complete guide |

---

## ✅ Quick Start

**Run All:**
```bash
RUN_ALL_WATCHERS.bat
```

**Run Individual:**
```bash
RUN_GMAIL_WATCHER.bat
RUN_FILE_WATCHER.bat
RUN_WHATSAPP_WATCHER.bat
RUN_MCP.bat
```

---

**Created:** March 1, 2026  
**System:** Personal AI Employee
