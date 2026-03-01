# 📱 WhatsApp Live Auto-Reply - Complete Guide

## ✅ **Setup Complete!**

Ab aap ke paas **2 tarikon** hain WhatsApp chalane ke:

---

## 🚀 **Method 1: WhatsApp Manager Se (Recommended)**

### **Step 1: Server Start Karein**
Already running hai! 

### **Step 2: WhatsApp Manager Kholein**
```
http://localhost:5000/whatsapp-manager
```

### **Step 3: START WHATSAPP RECEIVER Click Karein**
1. WhatsApp Manager page par jayein
2. **"START WHATSAPP RECEIVER"** button click karein
3. WhatsApp Web khulega automatically
4. QR code scan karein

### **Step 4: Live Messages Dekhein**
- Messages **real-time** mein dikhenge
- **Auto-reply** jayega automatically
- Stats update honge automatically

---

## 🚀 **Method 2: Direct Batch File**

### **Double-click karein:**
```
START_WHATSAPP_LIVE.bat
```

### **Kya Hoga:**
1. ✅ Browser khulega
2. ✅ QR code scan karein
3. ✅ Messages receive honge
4. ✅ Auto-reply jayega
5. ✅ Messages save honge vault mein

---

## 🤖 **Auto-Reply Keywords (Default):**

| Jab koi bheje | Auto-reply jayega |
|--------------|-------------------|
| `hello` | Walaikum Assalam! How can I help you today? |
| `hi` | Hello! Thanks for contacting us... |
| `hey` | Hello! How can I assist you? |
| `price` | Our pricing starts at $99/month... |
| `cost` | Our pricing starts at $99/month... |
| `payment` | Bank transfer details... |
| `pay` | Payment details... |
| `order` | Order ke liye: Product, Quantity, Address |
| `buy` | Order ke liye: Product, Quantity, Address |
| `thanks` | You're welcome! |
| `thank you` | You're welcome! |
| `help` | How can I assist you today? |
| `support` | Our support team is here to help! |
| `contact` | Contact details... |
| `location` | Visit us at: 123 Main Street, Karachi |
| `address` | Our address... |
| `business hours` | We are open Monday-Saturday, 9 AM to 6 PM |
| `timing` | Business hours... |

---

## 📝 **Apne Keywords Kaise Add Karein?**

`whatsapp_live_server.py` file edit karein (line 27 ke paas):

```python
AUTO_REPLY_KEYWORDS = {
    'hello': 'Walaikum Assalam! Aap ki kaise madad karun?',
    'aap kaise hain': 'Main theek hoon, shukriya!',
    'price': 'Hamara price $99/month hai',
    'location': '123 Main Street, Karachi',
    'business hours': 'Hum 9 AM se 6 PM tak khule hain',
    # Aur keywords add karein...
}
```

---

## 📊 **Live Features:**

### **WhatsApp Manager Page Par:**

| Feature | Status |
|---------|--------|
| Real-time Messages | ✅ 3 seconds mein update |
| Auto-Reply Status | ✅ Live indicator |
| Message Stats | ✅ Auto-update |
| Start/Stop Receiver | ✅ One-click control |
| Message History | ✅ Saved locally |
| Vault Integration | ✅ Auto-save |

---

## 🧪 **Test Kaise Karein?**

### **Step 1: WhatsApp Manager Kholein**
```
http://localhost:5000/whatsapp-manager
```

### **Step 2: Receiver Start Karein**
- **"START WHATSAPP RECEIVER"** button click karein
- WhatsApp Web khulega
- QR code scan karein

### **Step 3: Test Message Bhejein**
Doosre phone se bhejein:
```
Hi, what is the price?
```

### **Step 4: Result Dekhein**
- ✅ Message WhatsApp Manager mein dikhega
- ✅ Auto-reply jayega: "Our pricing starts at $99/month..."
- ✅ Stats update honge
- ✅ Message vault mein save hoga

---

## 📂 **Messages Kahan Save Honge?**

### **Live Messages:**
```
whatsapp_messages_live.json
```

### **Vault Backup:**
```
vault/Inbox/WHATSAPP_[Sender]_[Timestamp].md
```

---

## ⚠️ **Troubleshooting:**

### ❌ "Playwright not found"
```bash
pip install playwright
playwright install chromium
```

### ❌ QR code nahi aa raha
- Internet connection check karein
- Chrome mein https://web.whatsapp.com khol kar dekhein
- Phone mein WhatsApp updated hona chahiye

### ❌ Auto-reply nahi aa raha
- Message mein keyword hona chahiye
- 60 second ka cooldown hai (ek hi person ko baar baar reply nahi)
- Console mein error check karein

### ❌ Messages show nahi ho rahe
- Page refresh karein (F5)
- Receiver running hai check karein
- Browser console mein error check karein (F12)

---

## 🛑 **Kaise Rokain?**

### **WhatsApp Manager Se:**
- **"STOP RECEIVER"** button click karein

### **Direct Stop:**
- Command window mein **Ctrl + C** dabayein
- Ya WhatsApp Web window band kar dein

---

## 📋 **Complete Workflow:**

```
┌─────────────────────────────────────┐
│  WhatsApp Manager Page              │
│  http://localhost:5000/whatsapp-mgr │
│                                      │
│  [START WHATSAPP RECEIVER]          │
│                                      │
│  ✓ Live Messages (3s refresh)       │
│  ✓ Auto-Reply Status                │
│  ✓ Message Stats                    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  WhatsApp Live Receiver             │
│  (whatsapp_live_server.py)          │
│                                      │
│  ✓ Monitors WhatsApp Web            │
│  ✓ Detects new messages             │
│  ✓ Sends auto-reply                 │
│  ✓ Saves to vault                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Backend API (Flask)                │
│  (api_routes.py)                    │
│                                      │
│  ✓ Status endpoint                  │
│  ✓ Messages endpoint                │
│  ✓ Config endpoint                  │
└─────────────────────────────────────┘
```

---

## 🎯 **Quick Commands:**

### **Start Everything:**
```bash
# Terminal 1: Start API Server
python api_routes.py

# Terminal 2: Start WhatsApp Receiver
python whatsapp_live_server.py

# Ya batch file use karein
START_WHATSAPP_LIVE.bat
```

### **Open WhatsApp Manager:**
```
http://localhost:5000/whatsapp-manager
```

---

## 🔒 **Privacy & Security:**

- ✅ Messages sirf locally save hote hain
- ✅ Koi data external servers ko nahi jata
- ✅ WhatsApp account secure rehta hai
- ✅ Official WhatsApp Web interface

⚠️ **Disclaimer:** Yeh WhatsApp Web automation use karta hai. WhatsApp ke Terms of Service ka khayal rakhein.

---

## 📞 **Support:**

Agar koi masla ho:
1. Console mein error messages check karein
2. Receiver running hai verify karein
3. QR code properly scan hua hai check karein
4. Internet connection verify karein

---

**Abhi try karein!** 📱

1. http://localhost:5000/whatsapp-manager par jayein
2. "START WHATSAPP RECEIVER" click karein
3. QR code scan karein
4. Doosre phone se "hello" bhejein
5. Auto-reply dekhein! ✅

---

**Made with ❤️ by Farha Khan**
