# 📱 WhatsApp Real Auto-Reply - Setup Guide

## ✅ Quick Start (3 Steps)

### **Step 1: Install Requirements**
Open Command Prompt in your project folder and run:
```bash
pip install playwright
playwright install chromium
```

### **Step 2: Run Auto-Reply**
Double-click: **`run_whatsapp_autoreply.bat`**

Or run manually:
```bash
python run_whatsapp_autoreply.py
```

### **Step 3: Scan QR Code**
1. Browser window opens automatically
2. WhatsApp Web QR code appears
3. Open WhatsApp on your phone
4. **Settings → Linked Devices → Link a Device**
5. Point camera at QR code
6. Wait for connection...

---

## 🎯 How It Works

Once running, the system:

1. **Monitors WhatsApp Web** (checks every 3 seconds)
2. **Saves all messages** to `vault/Inbox/`
3. **Auto-replies** to messages containing keywords
4. **Prevents spam** (won't reply to same person within 60 seconds)

---

## 🤖 Auto-Reply Keywords

The system automatically replies to these keywords:

| Keyword | Auto-Reply |
|---------|-----------|
| `hello` | Walaikum Assalam! How can I help you today? |
| `hi` | Hello! Thanks for contacting us. How can we help? |
| `price` | Our pricing starts at $99/month. Would you like to schedule a demo? |
| `payment` | You can make payment via bank transfer. Account: 1234567890 |
| `order` | To place an order, please provide: 1) Product name 2) Quantity 3) Delivery address |
| `thanks` | You're welcome! Is there anything else I can help you with? |
| `thank you` | You're welcome! Feel free to ask if you need anything else. |

---

## 📝 Customizing Auto-Replies

Edit `run_whatsapp_autoreply.py` and modify the `AUTO_REPLY_KEYWORDS` dictionary:

```python
AUTO_REPLY_KEYWORDS = {
    'hello': 'Your custom greeting here',
    'your_keyword': 'Your custom response here',
    'business hours': 'We are open 9 AM - 6 PM daily',
    'location': 'Visit us at: 123 Main Street, City',
    # Add more keywords...
}
```

---

## 📂 Where Messages Are Saved

All incoming messages are saved to:
```
vault/Inbox/WHATSAPP_[SenderName]_[Timestamp].md
```

Example:
```
vault/Inbox/WHATSAPP_John_Smith_2026-03-01-143022.md
```

---

## 🧪 Testing Auto-Reply

1. Run the script: `run_whatsapp_autoreply.bat`
2. Scan QR code
3. Send a test message from another phone:
   - Send: "Hi, what is the price?"
   - Auto-reply: "Our pricing starts at $99/month..."
4. Check console for confirmation
5. Check `vault/Inbox/` for saved message

---

## ⚠️ Troubleshooting

### ❌ "Playwright not found"
**Solution:** Run `pip install playwright`

### ❌ "Chromium not found"
**Solution:** Run `playwright install chromium`

### ❌ QR code doesn't appear
**Solution:** 
- Check internet connection
- Try opening https://web.whatsapp.com in Chrome first
- Make sure WhatsApp is installed on your phone

### ❌ Browser closes immediately
**Solution:** 
- Check for Chrome/Chromium updates
- Try running as Administrator
- Check Windows Defender isn't blocking

### ❌ Auto-reply not working
**Solution:**
- Make sure message contains a keyword
- Check console for errors
- Verify you're not replying too soon (60s cooldown)

### ❌ Messages not saving
**Solution:**
- Check `vault/Inbox/` folder exists
- Check folder permissions
- Look for error messages in console

---

## 🛑 Stopping the System

Press **`Ctrl + C`** in the command window to stop.

Or close the browser window.

---

## 📊 Console Output Example

```
======================================================================
🚀 WhatsApp Real Auto-Reply System
======================================================================

💾 Messages will be saved to: vault/Inbox
🤖 Auto-reply enabled for 7 keywords

Keywords: hello, hi, price, payment, order, thanks, thank you

======================================================================

📱 Launching WhatsApp Web...
⏳ Please scan the QR code with your phone...

✅ Connected to WhatsApp Web!

======================================================================
🎯 Auto-Reply System ACTIVE
======================================================================

Monitoring messages... (Press Ctrl+C to stop)

======================================================================
📨 New message from John Smith
💬 Content: Hi, what is the price?
🤖 Auto-replying (keyword: price)...
✅ Auto-reply sent to John Smith
```

---

## 🔒 Privacy & Security

- ✅ Messages saved locally only (no cloud)
- ✅ No data sent to external servers
- ✅ Your WhatsApp account remains secure
- ✅ Uses official WhatsApp Web interface

⚠️ **Disclaimer:** This uses WhatsApp Web automation. Ensure compliance with WhatsApp's Terms of Service. Use at your own risk.

---

## 🎯 Advanced Features

### Send Message Manually
```python
from AI_Employee_System.Watchers.whatsapp_watcher import WhatsAppWatcher
import asyncio

async def send_manual():
    watcher = WhatsAppWatcher()
    await watcher.launch_browser()
    await watcher.send_message("John Smith", "Hello!")
    await asyncio.sleep(5)
    await watcher.close_browser()

asyncio.run(send_manual())
```

### Get Recent Chats
```python
chats = await watcher.get_recent_chats(limit=5)
for chat in chats:
    print(f"{chat['name']}: {chat['preview']}")
```

---

## 📞 Support

If you need help:
1. Check console for error messages
2. Verify all setup steps completed
3. Test WhatsApp Web manually in browser first

---

**Made with ❤️ by Farha Khan**
