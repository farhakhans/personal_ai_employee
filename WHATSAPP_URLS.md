# 📱 WhatsApp Manager - Access Guide

## ✅ Server is Running!

The Flask API server is now running on: **http://localhost:5000**

---

## 🔗 WhatsApp Manager URLs

### **Main WhatsApp Manager:**
```
http://localhost:5000/whatsapp-manager
```

### **WhatsApp Analysis:**
```
http://localhost:5000/whatsapp_analysis.html
```

---

## 🚀 Quick Access

1. **Open your browser**
2. **Go to:** http://localhost:5000/whatsapp-manager
3. **You should see the WhatsApp Manager dashboard!**

---

## 📋 All Available URLs

| Page | URL |
|------|-----|
| **Login** | http://localhost:5000/ |
| **Main Dashboard** | http://localhost:5000/main-dashboard |
| **WhatsApp Manager** | http://localhost:5000/whatsapp-manager |
| **WhatsApp Analysis** | http://localhost:5000/whatsapp_analysis.html |
| **Bronze Tier** | http://localhost:5000/bronze |
| **Silver Tier** | http://localhost:5000/silver |
| **Gold Tier** | http://localhost:5000/gold |
| **Platinum Tier** | http://localhost:5000/platinum |
| **Status** | http://localhost:5000/status |

---

## 🧪 Test WhatsApp API Endpoints

### **Send WhatsApp Message:**
```bash
curl -X POST http://localhost:5000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{"to":"+92 300 1234567","message":"Hello from API!"}'
```

### **Get Configuration:**
```bash
curl http://localhost:5000/api/whatsapp/config
```

### **Save Configuration:**
```bash
curl -X POST http://localhost:5000/api/whatsapp/config \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"+92 300 1234567","greeting_message":"Hello!"}'
```

---

## ⚠️ If Page Not Found

### **Error: 404 Not Found**

1. **Make sure server is running:**
   - Check if `run_server.py` is running
   - Look for: `* Running on http://localhost:5000`

2. **Clear browser cache:**
   - Press `Ctrl + Shift + Delete`
   - Or try incognito/private mode

3. **Check URL spelling:**
   - Correct: `/whatsapp-manager` (with hyphen)
   - Wrong: `/whatsapp_manager` (with underscore)

4. **Try alternative URL:**
   - http://127.0.0.1:5000/whatsapp-manager

---

## 🛑 How to Stop Server

Press **`Ctrl + C`** in the command window where the server is running.

---

## 📞 Troubleshooting

### **"Port 5000 already in use"**
```bash
# Kill the process using port 5000
netstat -ano | findstr :5000
taskkill /F /PID <process_id>
```

### **"Module not found: flask_cors"**
```bash
pip install flask-cors
```

### **"Module not found: jwt"**
```bash
pip install PyJWT
```

### **"Module not found: bcrypt"**
```bash
pip install bcrypt
```

---

## 🎯 WhatsApp Manager Features

Once you open the page, you can:

1. **Send Messages** - Send WhatsApp messages directly
2. **View Message History** - See all sent/received messages
3. **Configure Auto-Reply** - Set up keyword-based auto-replies
4. **Test API** - Test WhatsApp Business API integration
5. **Monitor Status** - Check connection status

---

**Made with ❤️ by Farha Khan**
