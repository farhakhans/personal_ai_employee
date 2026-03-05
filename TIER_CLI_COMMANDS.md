# 🚀 TIER CLI COMMANDS - Quick Reference

**Personal AI Employee System - Run Each Tier Individually**

---

## 📋 QUICK START

### Run Each Tier (Batch Files):

| Tier | Command |
|------|---------|
| 🥉 **Bronze** | `RUN_BRONZE_TIER.bat` |
| 🥈 **Silver** | `RUN_SILVER_TIER.bat` |
| 🥇 **Gold** | `RUN_GOLD_TIER.bat` |
| 💎 **Platinum** | `RUN_PLATINUM_TIER.bat` |

---

## 🥉 BRONZE TIER

**Features:** File Watcher, MCP Server, Flask API Dashboard

### Run Command:
```batch
RUN_BRONZE_TIER.bat
```

### Services Running:
- ✓ Flask API Server (Port 5000)
- ✓ File Watcher
- ✓ MCP Server

### Dashboard:
http://localhost:5000/bronze

---

## 🥈 SILVER TIER

**Features:** Bronze + WhatsApp, LinkedIn, Twitter

### Run Command:
```batch
RUN_SILVER_TIER.bat
```

### Services Running:
- ✓ Flask API Server (Port 5000)
- ✓ WhatsApp Watcher
- ✓ LinkedIn Poster
- ✓ Twitter Poster
- ✓ File Watcher

### Dashboard:
http://localhost:5000/silver

---

## 🥇 GOLD TIER

**Features:** Silver + Facebook, Instagram

### Run Command:
```batch
RUN_GOLD_TIER.bat
```

### Services Running:
- ✓ Flask API Server (Port 5000)
- ✓ WhatsApp Watcher
- ✓ LinkedIn Poster
- ✓ Twitter Poster
- ✓ Facebook Poster
- ✓ Instagram Poster
- ✓ File Watcher

### Dashboard:
http://localhost:5000/gold

---

## 💎 PLATINUM TIER

**Features:** Gold + WhatsApp Real API, MCP Server

### Run Command:
```batch
RUN_PLATINUM_TIER.bat
```

### Services Running:
- ✓ Flask API Server (Port 5000)
- ✓ WhatsApp Real API
- ✓ LinkedIn Poster
- ✓ Twitter Poster
- ✓ Facebook Poster
- ✓ Instagram Poster
- ✓ File Watcher
- ✓ MCP Server

### Dashboard:
http://localhost:5000/platinum

---

## 🛑 STOP SERVICES

### Method 1: Close Windows
Close each console window individually

### Method 2: Task Manager
```
Ctrl+Shift+Esc → Find Python processes → End Task
```

### Method 3: Command Line
```batch
taskkill /F /IM python.exe
```

---

## 📊 TIER COMPARISON

| Service | Bronze | Silver | Gold | Platinum |
|---------|--------|--------|------|----------|
| Gmail Watcher | ✓ | ✓ | ✓ | ✓ |
| File Watcher | ✓ | ✓ | ✓ | ✓ |
| MCP Server | ✓ | ✓ | ✓ | ✓ |
| WhatsApp Watcher | - | ✓ | ✓ | ✓ |
| LinkedIn Poster | - | ✓ | ✓ | ✓ |
| Twitter Poster | - | ✓ | ✓ | ✓ |
| HITL Framework | - | ✓ | ✓ | ✓ |
| Facebook Poster | - | - | ✓ | ✓ |
| Instagram Poster | - | - | ✓ | ✓ |
| Odoo Integration | - | - | ✓ | ✓ |
| System Orchestrator | - | - | ✓ | ✓ |
| Watchdog Monitor | - | - | - | ✓ |
| Flask API Server | - | - | - | ✓ |

---

## 🔧 PREREQUISITES

### Before Running Any Tier:

1. **Setup .env file:**
   ```env
   ANTHROPIC_API_KEY=sk-ant-...
   GMAIL_ADDRESS=your.email@gmail.com
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
   ```

2. **Install Dependencies:**
   ```batch
   pip install -r requirements.txt
   ```

3. **Start Flask API (for dashboard):**
   ```batch
   python api_routes.py
   ```
   Access: http://localhost:5000

---

## 📁 FILE LOCATIONS

### Batch Files:
- `RUN_BRONZE_TIER.bat` - Bronze tier launcher
- `RUN_SILVER_TIER.bat` - Silver tier launcher
- `RUN_GOLD_TIER.bat` - Gold tier launcher
- `RUN_PLATINUM_TIER.bat` - Platinum tier launcher

### Python Scripts:
- `AI_Employee_System/Watchers/start_gmail_watcher.py`
- `AI_Employee_System/Watchers/start_file_watcher.py`
- `AI_Employee_System/Watchers/start_whatsapp_watcher.py`
- `AI_Employee_System/Watchers/linkedin_poster.py`
- `AI_Employee_System/Watchers/twitter_poster.py`
- `AI_Employee_System/Watchers/facebook_poster.py`
- `AI_Employee_System/Watchers/instagram_poster.py`
- `AI_Employee_System/hitl_framework.py`
- `AI_Employee_System/odoo_integration.py`
- `AI_Employee_System/system_orchestrator.py`
- `AI_Employee_System/watchdog_monitor.py`

---

## 🎯 RECOMMENDED FLOW

### Week 1: Bronze Tier
```batch
RUN_BRONZE_TIER.bat
```
Focus: Email & File monitoring

### Week 2-3: Silver Tier
```batch
RUN_SILVER_TIER.bat
```
Focus: Multi-channel communication

### Week 4-5: Gold Tier
```batch
RUN_GOLD_TIER.bat
```
Focus: Full automation

### Week 6-8: Platinum Tier
```batch
RUN_PLATINUM_TIER.bat
```
Focus: Production 24/7 operation

---

## 📞 SUPPORT

**Documentation:**
- `ALL_TIERS_WORKFLOW.md` - Complete workflow guide
- `BRONZE_TIER_FEATURES.md` - Bronze tier details
- `ALL_COMMANDS.md` - All CLI commands

**Dashboards:**
- Bronze: http://localhost:5000/bronze
- Silver: http://localhost:5000/silver
- Gold: http://localhost:5000/gold
- Platinum: http://localhost:5000/platinum

---

**Created:** March 5, 2026
**Status:** ✅ All Tiers Operational
