# 📱 WhatsApp Real Auto-Reply - Roman Urdu Guide

## 🚀 Kaise Start Karein (3 Steps)

### **Step 1: Playwright Install Karein**
Command Prompt mein yeh command chalayein:

```bash
pip install playwright
playwright install chromium
```

### **Step 2: WhatsApp Receiver Start Karein**
Double-click karein: **`START_REAL_WHATSAPP.bat`**

Ya manually chalayein:
```bash
python run_whatsapp_receiver.py
```

### **Step 3: QR Code Scan Karein**
1. Browser window apne aap khulega
2. WhatsApp Web ka QR code dikhega
3. Apne phone se WhatsApp kholein
4. **Settings → Linked Devices → Link a Device**
5. Camera ko QR code par le jayein
6. Connect hone ka intezar karein...

---

## ✅ Ab Kya Hoga?

Jab aapka phone connect ho jayega:

1. ✅ **Real-time messages** dikhenge console mein
2. ✅ **Auto-reply** jayega keywords par
3. ✅ **Messages save** honge `vault/Inbox/` mein
4. ✅ **Spam protection** (60 seconds ka cooldown)

---

## 🤖 Auto-Reply Keywords (Default)

| Jab koi bheje | Auto-reply jayega |
|--------------|-------------------|
| `hello` | Walaikum Assalam! How can I help you today? |
| `hi` | Hello! Thanks for contacting us... |
| `price` | Our pricing starts at $99/month... |
| `payment` | Bank transfer se payment kar sakte hain... |
| `order` | Order ke liye: 1) Product 2) Quantity 3) Address |
| `thanks` | You're welcome! |

---

## 📝 Apne Keywords Kaise Add Karein?

`run_whatsapp_receiver.py` file ko edit karein aur `AUTO_REPLY_KEYWORDS` mein apne keywords dalein:

```python
AUTO_REPLY_KEYWORDS = {
    'hello': 'Walaikum Assalam! Aap ki kaise madad karun?',
    'aap kaise hain': 'Main theek hoon, shukriya! Bataiye main aap ki kaise madad karun?',
    'price': 'Hamara price $99/month se start hota hai',
    'location': 'Hamara address: 123 Main Street, Karachi',
    'business hours': 'Hum 9 AM se 6 PM tak khule hain',
    # Aur keywords add karein...
}
```

---

## 📂 Messages Kahan Save Honge?

Saare incoming messages save honge yahan:
```
vault/Inbox/WHATSAPP_[SenderName]_[Timestamp].md
```

Misal:
```
vault/Inbox/WHATSAPP_Ahmed_Hassan_2026-03-01-143022.md
```

---

## 🧪 Test Kaise Karein?

1. Script chalayein: `START_REAL_WHATSAPP.bat`
2. QR code scan karein
3. Doosre phone se test message bhejein:
   - Bhejein: "Hi, what is the price?"
   - Auto-reply: "Our pricing starts at $99/month..."
4. Console mein confirmation dekhein
5. `vault/Inbox/` mein saved message check karein

---

## ⚠️ Agar Kaam Na Kare (Troubleshooting)

### ❌ "Playwright not found"
**Hal:** `pip install playwright` chalayein

### ❌ "Chromium not found"
**Hal:** `playwright install chromium` chalayein

### ❌ QR code nahi aa raha
**Hal:** 
- Internet connection check karein
- Pehle Chrome mein https://web.whatsapp.com khol kar dekhein
- Make sure karein phone mein WhatsApp install hai

### ❌ Browser foran band ho jata hai
**Hal:** 
- Chrome/Chromium update karein
- Administrator ki tarah chalayein
- Windows Defender check karein

### ❌ Auto-reply nahi aa raha
**Hal:**
- Message mein keyword hona chahiye
- Console mein errors check karein
- 60 second ka cooldown check karein

### ❌ Messages save nahi ho rahe
**Hal:**
- `vault/Inbox/` folder bana hona chahiye
- Folder permissions check karein
- Console mein error messages dekhein

---

## 🛑 Kaise Rokain?

Command window mein **`Ctrl + C`** dabayein.

Ya browser window band kar dein.

---

## 📊 Console Output Example

```
======================================================================
🚀 WhatsApp Real-Time Message Receiver
======================================================================

💾 Messages saved to: vault/Inbox
🤖 Auto-reply: ENABLED

Keywords: hello, hi, price, payment, order, thanks

======================================================================

📱 Starting WhatsApp Web...
⏳ Please scan QR code with your phone...

✅ WhatsApp Web connected successfully!

======================================================================
🎯 MONITORING ACTIVE - Waiting for messages...
======================================================================

======================================================================
📨 NEW MESSAGE
👤 From: Ahmed Hassan
💬 Message: Hi, what is the price?
🕐 Time: 2026-03-01T14:30:22
🤖 Sending auto-reply...
✅ Auto-reply sent!
💾 Saved to vault: WHATSAPP_Ahmed_Hassan_2026-03-01-143022.md
```

---

## 🔒 Privacy & Security

- ✅ Messages sirf locally save hote hain (cloud nahi)
- ✅ Koi data external servers ko nahi jata
- ✅ Aapka WhatsApp account secure rehta hai
- ✅ Official WhatsApp Web interface use hota hai

⚠️ **Disclaimer:** Yeh WhatsApp Web automation use karta hai. WhatsApp ke Terms of Service ka khayal rakhein. Apne risk par use karein.

---

## 🎯 Advanced Features

### Message Manually Bhejein
```python
from playwright.async_api import async_playwright
import asyncio

async def send_message():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto("https://web.whatsapp.com")
    # QR scan karein...
    # Message bhejein...
    await browser.close()

asyncio.run(send_message())
```

---

## 📞 Support

Agar koi masla ho:
1. Console mein error messages check karein
2. Saare setup steps complete kiye hain verify karein
3. Pehle WhatsApp Web manually browser mein test karein

---

## 📁 Files Jo Banayi Gayi Hain:

| File | Maqsad |
|------|--------|
| `run_whatsapp_receiver.py` | Main auto-reply script |
| `START_REAL_WHATSAPP.bat` | Easy launcher (double-click) |
| `whatsapp_config.json` | Keywords aur replies ki settings |
| `whatsapp_messages.json` | Sent/received messages ka record |

---

**Abhi try karein!** `START_REAL_WHATSAPP.bat` par double-click karein aur test karne ke liye doosre phone se "hi" ya "price" bhejein. 📱

---

**Made with ❤️ by Farha Khan**
