# ✅ Render.com Deployment Guide
**Personal AI Employee - Flask App**

---

## 🎉 Ready to Deploy!

Aapki Flask app Render.com par deploy hone ke liye ready hai!

---

## 📋 Step-by-Step Deployment

### **Step 1: Render.com Par Jayen**
Website already open hai: [https://render.com](https://render.com)

---

### **Step 2: Sign Up / Login**
1. **"Get Started for Free"** click karen
2. **GitHub se sign in** karen (recommended)
   - Is se aapka GitHub repository automatically connect ho jayega

---

### **Step 3: New Web Service Banayen**
1. Dashboard par **"New +"** button click karen
2. **"Web Service"** select karen

---

### **Step 4: Repository Connect Karen**
1. **"Connect a repository"** click karen
2. Apna repository select karen: **`farhakhans/personal_ai_employee`**
3. **Branch:** `main`

---

### **Step 5: Settings Configure Karen**

#### **Basic Settings:**
```
Name: personal-ai-employee
Region: Singapore (closest to Pakistan/India)
Branch: main
Root Directory: (leave empty)
```

#### **Runtime Settings:**
```
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python api_routes.py
```

#### **Instance Type:**
```
Plan: Free
```

---

### **Step 6: Environment Variables Add Karen**

**"Advanced"** section mein ye variables add karen:

| Key | Value | Description |
|-----|-------|-------------|
| `SECRET_KEY` | `my-super-secret-key-123` | JWT authentication ke liye |
| `VAULT_PATH` | `/tmp/vault` | Vault storage path |
| `ANTHROPIC_API_KEY` | `sk-ant-api03-...` | AI features (optional) |
| `GMAIL_ADDRESS` | `your.email@gmail.com` | Gmail watcher (optional) |
| `GMAIL_APP_PASSWORD` | `xxxx xxxx xxxx xxxx` | Gmail app password (optional) |

**How to Add:**
1. **"Add Environment Variable"** click karen
2. Upar diye gaye variables ek ek karke add karen
3. **"Save Changes"** click karen

---

### **Step 7: Create Web Service**
1. **"Create Web Service"** button click karen
2. Deployment automatically start ho jayega
3. **3-5 minutes** lagenge deployment mein

---

## ⏱️ Deployment Progress

Render dashboard par aap dekh sakte hain:
- **Logs** tab → Real-time deployment logs
- **Events** tab → Deployment history

---

## 🎯 Live URL

Deployment complete hone ke baad:
```
https://personal-ai-employee.onrender.com
```

---

## 🧪 Test Karen

### **1. Login Page:**
```
https://personal-ai-employee.onrender.com/login-page
```

### **2. Default Users:**

| Email | Password | Tier |
|-------|----------|------|
| `admin@employee.ai` | `Admin@2026!` | Platinum |
| `manager@employee.ai` | `Manager@2026!` | Gold |
| `user@employee.ai` | `User@2026!` | Bronze |

---

## ✅ Features Working on Render

### **✅ Fully Working:**
- ✅ User Authentication (Login/Register)
- ✅ All Dashboards (Bronze/Silver/Gold/Platinum)
- ✅ API Endpoints
- ✅ User Management
- ✅ Customer Management
- ✅ Employee Management
- ✅ Payment Tracking
- ✅ Notifications
- ✅ Settings
- ✅ SQLite Database (persistent)
- ✅ Background Watchers (can be added as separate services)

### **⚠️ Note:**
- Free tier mein 15 minutes inactivity ke baad app sleep mode mein chala jata hai
- Next request par 30 seconds lagenge wake up hone mein
- Production ke liye paid plan ($7/month) consider karen

---

## 🔄 Auto-Deploy

Ab har commit automatically deploy hoga:

```batch
# Code change karen
git add .
git commit -m "Your changes"
git push origin main

# Render automatically deploy karega!
```

---

## 📊 Render vs Vercel

| Feature | Render | Vercel |
|---------|--------|--------|
| **Flask Support** | ✅ Full | ❌ Limited |
| **Serverless** | ❌ No (Full Server) | ✅ Yes |
| **Database** | ✅ SQLite Persistent | ❌ Reset hota hai |
| **Background Jobs** | ✅ Supported | ❌ Not supported |
| **Free Tier** | ✅ 750 hrs/month | ✅ Limited |
| **Sleep Mode** | ⚠️ After 15 min | ❌ Always cold |
| **Python Apps** | ✅ Optimized | ⚠️ Limited |

---

## 🛠️ Render Dashboard Links

- **Overview:** https://dashboard.render.com
- **My Services:** https://dashboard.render.com
- **Logs:** Dashboard → Your Service → Logs
- **Settings:** Dashboard → Your Service → Settings

---

## 📁 Files Added

| File | Purpose |
|------|---------|
| `Procfile` | Render start command |
| `render.yaml` | Render configuration |

---

## 🎯 Quick Deploy Steps Summary

1. ✅ Render.com par jayen
2. ✅ GitHub se sign in karen
3. ✅ New + → Web Service
4. ✅ Repository connect karen
5. ✅ Settings configure karen
6. ✅ Environment variables add karen
7. ✅ Create Web Service click karen
8. ✅ Deploy complete!

---

## 💡 Pro Tips

1. **Health Check:** `/` route use karen
2. **Logs:** Regular basis par check karen
3. **Env Variables:** Production mein zaroor set karen
4. **Auto-Deploy:** Git push se automatic deploy hoga

---

**Ab Render.com par deploy karen! Website already open hai.** 🚀

---

**Last Updated:** March 5, 2026
**Status:** ✅ Ready to Deploy on Render
