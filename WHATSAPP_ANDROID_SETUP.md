# 📱 WhatsApp Setup for Android Phone

## 🔧 Current Status

Your system currently uses **WhatsApp Web** which only shows messages on your computer.

## ✅ Solution: WhatsApp Business API

To receive messages on your **Android phone** AND auto-reply automatically, you need **WhatsApp Business API**.

---

## 🚀 Setup Steps

### **Step 1: Install WhatsApp Business on Your Phone**

1. Download **WhatsApp Business** from Google Play Store
2. Register with your business phone number
3. Complete the setup

### **Step 2: Get WhatsApp Business API Access**

#### Option A: Meta Cloud API (FREE - Recommended)

1. Go to: https://developers.facebook.com/apps/
2. Create a new App → Select "Business" type
3. Add "WhatsApp" product to your app
4. Get your:
   - **Phone ID** 
   - **Access Token**
   - **Business Account ID**

#### Option B: WhatsApp Business API via Provider

- **Twilio** (Easiest): https://www.twilio.com/whatsapp
- **MessageBird**: https://messagebird.com/
- **360dialog**: https://www.360dialog.com/

### **Step 3: Configure Your System**

1. Open `whatsapp_config.json` in your project folder
2. Add your API credentials:

```json
{
  "phone_number": "+92 300 1234567",
  "access_token": "YOUR_WHATSAPP_API_TOKEN",
  "phone_id": "YOUR_PHONE_ID",
  "webhook_verify_token": "my_verify_token_123",
  "greeting_message": "Assalam-o-Alaikum! Thank you for contacting AI Employee System.",
  "business_hours_message": "We are currently away but will respond within 24 hours.",
  "auto_reply_enabled": true,
  "keywords": [
    {"keyword": "price", "response": "Our pricing starts at $99/month."},
    {"keyword": "payment", "response": "You can make payment via bank transfer."},
    {"keyword": "order", "response": "To place an order, please provide product name and quantity."},
    {"keyword": "hello", "response": "Walaikum Assalam! How can I help you today?"},
    {"keyword": "hi", "response": "Hello! Thanks for contacting us."}
  ]
}
```

### **Step 4: Run WhatsApp Auto-Reply Server**

```bash
# Start the WhatsApp auto-reply system
python whatsapp_real_autoreply.py
```

### **Step 5: Test It**

1. Send a WhatsApp message to your business number from another phone
2. Message will appear on:
   - ✅ Your Android phone (WhatsApp Business app)
   - ✅ Your computer system (auto-reply will send)
3. Auto-reply will be sent automatically!

---

## 🔄 How It Works

```
Customer sends message
        ↓
WhatsApp Business API
        ↓
┌───────┴───────┐
↓               ↓
Your Phone   Your System
(WhatsApp)  (Auto-Reply)
        ↓               ↓
    You see it    Auto-reply sent
    on phone      back to customer
```

---

## 💡 Alternative: Forwarding Setup

If you don't want to use Business API, you can:

### **Use WhatsApp Web + Phone Together**

1. Keep WhatsApp logged in on your **Android phone**
2. Open **WhatsApp Web** on your computer (web.whatsapp.com)
3. Both will receive same messages
4. Your system monitors WhatsApp Web
5. Auto-replies sent via system
6. Replies appear on your phone too!

**Note:** This still requires manual WhatsApp Web connection.

---

## 🎯 Recommended: Meta Cloud API (FREE)

### Setup Guide:

1. **Create Facebook Developer Account**
   - Go to https://developers.facebook.com/
   - Login with Facebook

2. **Create App**
   - Click "My Apps" → "Create App"
   - Select "Business" type
   - Fill in app details

3. **Add WhatsApp Product**
   - In app dashboard, click "Add Product"
   - Select "WhatsApp"
   - Click "Set Up"

4. **Get API Credentials**
   - Go to WhatsApp → API Setup
   - Copy your:
     - **Temporary Access Token** (valid for 24 hours)
     - **Phone Number ID**
     - **WhatsApp Business Account ID**

5. **Test API**
   ```bash
   curl -X POST 'https://graph.facebook.com/v17.0/YOUR_PHONE_ID/messages' \
   -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
   -H 'Content-Type: application/json' \
   -d '{
     "messaging_product": "whatsapp",
     "to": "923001234567",
     "type": "text",
     "text": {
       "body": "Hello from AI Employee System!"
     }
   }'
   ```

6. **Update Config File**
   - Edit `whatsapp_config.json`
   - Add your credentials
   - Save and restart the server

---

## 📞 Need Help?

For WhatsApp Business API setup:
- Meta Documentation: https://developers.facebook.com/docs/whatsapp
- Twilio WhatsApp: https://www.twilio.com/docs/whatsapp

---

## ⚡ Quick Start (Testing)

For now, your system works in **SIMULATION MODE**:
- Messages are stored locally
- Auto-replies are simulated
- No real WhatsApp integration

To enable real WhatsApp:
1. Get WhatsApp Business API credentials
2. Update `whatsapp_config.json`
3. Restart the server

---

**Created by:** AI Employee System
**Version:** 1.0
**Last Updated:** 2026-03-25
