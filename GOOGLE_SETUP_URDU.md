# 🔐 Google Sign-In Real Setup - Complete Guide

## 📌 Step-by-Step Setup (آسان طریقہ)

### **Step 1: Google Cloud Project بنائیں**

1. اس لنک پر جائیں: https://console.cloud.google.com/
2. **"Select a project"** پر کلک کریں
3. **"+ NEW PROJECT"** پر کلک کریں
4. Project کا نام دیں: `AI Employee`
5. **"CREATE"** پر کلک کریں
6. Project select کریں

---

### **Step 2: Google+ API Enable کریں**

1. بائیں جانب سے **"APIs & Services"** پر کلک کریں
2. **"Library"** پر کلک کریں
3. Search box میں **"Google+ API"** لکھیں
4. **"Google+ API"** پر کلک کریں
5. **"ENABLE"** بٹن دبائیں

---

### **Step 3: OAuth Consent Screen Setup**

1. **"APIs & Services"** → **"OAuth consent screen"** پر جائیں
2. **"External"** منتخب کریں
3. **"CREATE"** پر کلک کریں

**App Information:**
- **App name**: `AI Employee System`
- **User support email**: اپنا Gmail ایڈریس لکھیں
- **App logo**: (چھوڑ دیں)
- **App domain**: (خالی چھوڑ دیں)
- **Developer contact**: اپنا Gmail ایڈریس لکھیں

4. **"SAVE AND CONTINUE"** پر کلک کریں
5. **Scopes page**: کچھ نہ کریں، بس **"SAVE AND CONTINUE"** دبائیں
6. **Test users**: اپنا Gmail ایڈریس add کریں
7. **"SAVE AND CONTINUE"** پر کلک کریں

---

### **Step 4: OAuth Client ID بنائیں**

1. **"APIs & Services"** → **"Credentials"** پر جائیں
2. **"+ CREATE CREDENTIALS"** پر کلک کریں
3. **"OAuth client ID"** منتخب کریں

**Application type**: `Web application` منتخب کریں

**Name**: `AI Employee Web`

**Authorized JavaScript origins** میں add کریں:
```
http://localhost
http://localhost:5000
http://127.0.0.1
http://127.0.0.1:5000
```

**Authorized redirect URIs** میں add کریں:
```
http://localhost:5000
http://localhost:5000/login-page
http://127.0.0.1:5000
http://127.0.0.1:5000/login-page
```

4. **"CREATE"** پر کلک کریں

---

### **Step 5: Client ID Copy کریں**

ایک popup کھلے گا جس میں آپ کا **Client ID** ہوگا۔ یہ کچھ ایسا لگتا ہے:

```
123456789012-abcdefghijklmnop.apps.googleusercontent.com
```

اسے **copy** کر لیں!

---

### **Step 6: login_custom.html میں Client ID ڈالیں**

1. اپنی فائل کھولیں: `login_custom.html`
2. لائن نمبر ~280 پر یہ کوڈ تلاش کریں:

```javascript
const GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com';
```

3. اپنا Client ID یہاں paste کریں:

```javascript
const GOOGLE_CLIENT_ID = '123456789012-abcdefghijklmnop.apps.googleusercontent.com';
```

4. فائل save کریں

---

### **Step 7: Flask Server Restart کریں**

1. پرانا server بند کریں (Ctrl+C)
2. نیا server شروع کریں:

```bash
cd "D:\DocuBook-Chatbot folder\Personal AI Employee"
python api_routes.py
```

---

### **Step 8: Test کریں!**

1. browser میں جائیں: `http://localhost:5000/login-page`
2. **"Sign in with Google"** بٹن پر کلک کریں
3. Google کی popup کھلے گی
4. اپنا **Gmail account** منتخب کریں
5. **Allow** پر کلک کریں
6. Dashboard میں redirect ہو جائیں گے! ✅

---

## ✅ یہ کیسے کام کرتا ہے:

1. User "Sign in with Google" پر کلک کرتا ہے
2. **اصل Google popup** کھلتا ہے
3. User اپنا Gmail account منتخب کرتا ہے
4. Google user کی معلومات بھیجتا ہے (email, name, photo)
5. Backend user account بناتا/کھولتا ہے
6. Dashboard میں redirect ہوتا ہے

---

## ⚠️ Important Notes:

### **Testing کے دوران:**
- صرف وہی Gmail accounts کام کریں گے جو آپ نے **Test Users** میں add کیے ہیں
- اپنا Gmail ضرور add کریں

### **Production کے لیے:**
- App کو **Publish** کرنا ہوگا
- Google verification درکار ہوگی

---

## 🐛 Troubleshooting:

### **"Access Blocked" یا "Error 400"**
- Test Users میں اپنا Gmail add کریں
- OAuth Consent Screen save کریں

### **"redirect_uri_mismatch"**
- Redirect URIs صحیح سے add کریں
- http://localhost:5000 ضرور ہو

### **"invalid_client"**
- Client ID صحیح سے copy کریں
- `.apps.googleusercontent.com` سمیت پورا ID ہو

---

## 📞 مدد چاہیے؟

Google Console: https://console.cloud.google.com/
OAuth Docs: https://developers.google.com/identity/protocols/oauth2

---

## 🎯 مکمل ہونے کے بعد:

✅ Real Google Sign-In کام کرے گا
✅ اصلی Gmail accounts سے login ہوگا
✅ User کی photo اور name show ہوگی
✅ کوئی demo نہیں، بالکل اصلی!
