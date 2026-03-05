# 🚀 Vercel Deployment - Complete Guide
**Personal AI Employee System**

---

## ⚡ Quick Deploy (5 Minutes)

### **Step 1: Vercel Account Banayen**
1. [vercel.com](https://vercel.com) par jayen
2. "Sign Up" click karen
3. **GitHub se sign in** karen (recommended)

---

### **Step 2: GitHub Repository Push Karen**

```batch
# Git initialize karen (agar nahi hai)
git init

# Sab files add karen
git add .

# Commit karen
git commit -m "Initial commit - Personal AI Employee"

# GitHub par push karen
git remote add origin https://github.com/YOUR_USERNAME/ai-employee.git
git push -u origin main
```

---

### **Step 3: Vercel Par Deploy**

#### **Option A: Vercel Dashboard (Easiest)**

1. **[vercel.com/new](https://vercel.com/new)** par jayen
2. **"Import Git Repository"** click karen
3. Apna repository select karen: `ai-employee`
4. **"Import"** click karen
5. Configure karen:
   - **Framework Preset**: `Python`
   - **Root Directory**: `./`
   - **Build Command**: (empty chhor den)
   - **Output Directory**: (empty chhor den)
6. **"Deploy"** click karen

#### **Option B: Vercel CLI**

```batch
# Vercel CLI install karen
npm install -g vercel

# Login karen
vercel login

# Deploy karen
vercel

# Production deploy
vercel --prod
```

---

### **Step 4: Environment Variables Set Karen**

Vercel Dashboard → Project → Settings → Environment Variables

**Add these variables:**

| Name | Value | Example |
|------|-------|---------|
| `ANTHROPIC_API_KEY` | AI API key | `sk-ant-api03-...` |
| `SECRET_KEY` | JWT secret | `my-super-secret-key-123` |
| `VAULT_PATH` | Vault path | `/tmp/vault` |
| `GMAIL_ADDRESS` | Gmail ID | `your.email@gmail.com` |
| `GMAIL_APP_PASSWORD` | App password | `xxxx xxxx xxxx xxxx` |

**Save** click karen aur **Redeploy** karen.

---

### **Step 5: Test Karen**

```
https://your-project.vercel.app
```

Dashboard open hoga!

---

## ⚠️ Important: Vercel Limitations

### **What Works ✅**
- User Authentication (Login/Register)
- Dashboard Pages
- API Endpoints
- Static Files
- JWT Tokens
- Database Reads

### **What Doesn't Work ❌**
- Background Watchers (Gmail, WhatsApp, File)
- Long-running processes
- WebSocket connections
- SQLite persistence (data reset hota hai)

---

## 🔧 Solutions for Limitations

### **1. Database Issue (SQLite → PostgreSQL)**

Vercel par SQLite persist nahi hota. **PostgreSQL use karen:**

#### **Free PostgreSQL Options:**

**A) Supabase (Recommended)**
1. [supabase.com](https://supabase.com) par sign up karen
2. New project banayen
3. Connection string copy karen
4. Vercel mein add karen:
   ```
   DATABASE_URL=postgresql://postgres:password@xxx.supabase.co:5432/postgres
   ```

**B) Neon (Serverless)**
1. [neon.tech](https://neon.tech) par sign up karen
2. Database banayen
3. Connection string Vercel mein add karen

---

### **2. Background Watchers**

Vercel serverless hai, watchers nahi chalenge. **Alternatives:**

**A) External Cron Jobs:**
- [cron-job.org](https://cron-job.org) - Free
- [EasyCron](https://easycron.com) - Free tier

**B) Separate Service:**
- Heroku par workers deploy karen
- Railway.app use karen
- Render.com use karen

---

## 📁 Files Update for Production

### **Update `api_routes.py`:**

```python
# Add at top of file
import os

# Replace SQLite path
DATABASE_PATH = os.environ.get('DATABASE_PATH', 'auth_database.db')

# For PostgreSQL (optional)
# DATABASE_URL = os.environ.get('DATABASE_URL')
```

---

## 🧪 Local Testing (Before Deploy)

```batch
# Vercel CLI install karen
npm install -g vercel

# Local test
vercel dev

# Visit: http://localhost:3000
```

---

## 📊 Deployment Checklist

- [ ] GitHub repository banaya
- [ ] Code push kiya
- [ ] Vercel account banaya
- [ ] Project deploy kiya
- [ ] Environment variables set kiye
- [ ] Database migration kiya (if needed)
- [ ] Test kiya
- [ ] Custom domain connect kiya (optional)

---

## 🌐 Custom Domain (Optional)

1. Vercel Dashboard → Project → Settings → Domains
2. Apna domain add karen
3. DNS records update karen:
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   ```

---

## 🛠️ Troubleshooting

### **Build Failed**
```batch
# Check requirements.txt
pip freeze > requirements.txt

# Test locally
python app.py
```

### **Runtime Errors**
- Vercel Dashboard → Functions → Logs check karen
- Environment variables verify karen
- Database connection test karen

### **Database Reset**
- SQLite use kar rahe hain to PostgreSQL migrate karen
- Supabase ya Neon use karen

---

## 📞 Support Links

- [Vercel Python Docs](https://vercel.com/docs/runtimes/official-runtimes/python)
- [Vercel Environment Variables](https://vercel.com/docs/environment-variables)
- [Supabase Setup](https://supabase.com/docs)
- [Neon Setup](https://neon.tech/docs)

---

## 🎯 Quick Commands

```batch
# GitHub push
git add .
git commit -m "Update"
git push

# Vercel deploy
vercel --prod

# View logs
vercel logs

# Local test
vercel dev
```

---

## ✅ Final Result

Aapka app live hoga at:
```
https://your-project.vercel.app
```

**Features Working:**
- ✓ Login/Register
- ✓ Dashboard (Bronze/Silver/Gold/Platinum)
- ✓ API Endpoints
- ✓ User Management

**Features Limited:**
- ⚠️ Background Watchers (external service needed)
- ⚠️ SQLite Database (PostgreSQL recommended)

---

**Last Updated:** March 5, 2026
**Status:** ✅ Ready to Deploy
