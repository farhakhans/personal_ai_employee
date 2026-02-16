# 🤖 MacroDroid WhatsApp Automation Setup
## Easier Alternative to Tasker - FREE Version Available

---

## 📥 Step 1: Install MacroDroid

1. Open **Google Play Store** on Android
2. Search: **"MacroDroid"**
3. Install: **MacroDroid - Device Automation** (by Arlo Games)
4. Open the app
5. Grant all permissions when asked

---

## 📥 Step 2: Import MacroDroid Configuration

### Option A: Import from File

1. Copy `whatsapp_macrodroid_config.macro` to your phone
2. Open **MacroDroid** app
3. Tap **⋮ (3 dots)** → **Import/Export** → **Import Macro**
4. Select the file
5. Tap **Import**

### Option B: Create Manually (Easy!)

#### Macro 1: Payment Received Auto-Reply

**Trigger:**
1. Tap **Add Macro**
2. **+** (Add Trigger)
3. **Messaging** → **Notification Received**
4. Select App: **WhatsApp**
5. Notification Title: Contains → `WhatsApp`
6. Notification Text: Contains → `payment received`

**Actions:**
1. **+** (Add Action)
2. **Messaging** → **Send WhatsApp Message**
3. Phone Number: Tap **%trigger_value[sender]**
4. Message:
```
🎉 Payment Received!

Thank you for your payment.
We've received your payment of Rs. {amount}.

Your account has been credited.

Thank you for your business! 🙏
```
5. ✅ Save

**Constraints:** (Optional)
- Add → **Date/Time** → **Time of Day**
- Set: 9:00 AM to 6:00 PM (business hours)

---

#### Macro 2: Order Inquiry Auto-Reply

**Trigger:**
1. **Add Macro** → **+** (Trigger)
2. **Messaging** → **Notification Received**
3. App: **WhatsApp**
4. Text Contains: `order status` OR `where is my order`

**Actions:**
1. **Messaging** → **Send WhatsApp Message**
2. Number: **%trigger_value[sender]**
3. Message:
```
📦 Order Status Inquiry

Thank you for contacting us!

To check your order status, please provide:
- Order ID
- Phone Number

Our team will respond within 1 hour.

Business Hours: 9 AM - 6 PM
```

---

#### Macro 3: Auto-Save Payment Details

**Trigger:**
1. **Add Macro** → **+** (Trigger)
2. **Messaging** → **Notification Received**
3. App: **WhatsApp**
4. Text Contains: `payment sent` OR `bank transfer`

**Actions:**
1. **Variables** → **Set Variable**
   - Name: `%payment_amount`
   - Value: **%trigger_value[text]**
2. **File I/O** → **Write to File**
   - File: `payments.txt`
   - Content: `%date %time - %payment_amount from %trigger_value[sender]`
   - Append: ✅ Yes
3. **Notification** → **Display Notification**
   - Title: `💰 Payment Received`
   - Text: `From: %trigger_value[sender]`
   - Sound: Default

---

#### Macro 4: Quick Send Payment Request

**Trigger:**
1. **Add Macro** → **+** (Trigger)
2. **Device Events** → **Widget Clicked**
3. Configure widget: **Payment Request**

**Actions:**
1. **Input** → **Pop Up Dialog**
   - Title: `Payment Request`
   - Input Type: Number
   - Store in: `%amount`
2. **Input** → **Pop Up Dialog**
   - Title: `Customer Phone`
   - Input Type: Phone Number
   - Store in: `%phone`
3. **Messaging** → **Send WhatsApp Message**
   - Number: `%phone`
   - Message:
```
💰 Payment Request

Amount: Rs. %amount
Please send to:
Account: 1234-5678-9012
Bank: MCB Bank
Title: Your Name

Thank you!
```

---

## 📥 Step 3: Create Home Screen Widgets

### Payment Request Widget:

1. Long press on **Home Screen**
2. **Widgets** → **MacroDroid**
3. Select: **Payment Request**
4. Tap **Add**
5. Choose icon (💰 money icon)
6. **Done!**

### Order Status Widget:

1. Repeat above steps
2. Select: **Order Status**
3. Choose icon (📦 box icon)

---

## 📊 MacroDroid vs Tasker:

| Feature | MacroDroid | Tasker |
|---------|-----------|--------|
| Cost | FREE (5 macros) | Rs. 350 |
| Difficulty | Easy | Medium |
| Setup Time | 5 minutes | 20 minutes |
| UI | Simple | Complex |
| Community | Good | Excellent |

**Recommendation:** Start with MacroDroid (FREE), upgrade to Tasker if needed.

---

## 🔗 Connect to Dashboard (Advanced)

### Webhook Receiver Macro:

**Trigger:**
1. **Add Macro** → **+** (Trigger)
2. **Connectivity** → **HTTP Request**
3. Method: **POST**
4. Path: `/send_whatsapp`

**Actions:**
1. **Variables** → **Set Variable**
   - `%webhook_data` = **%http_request_body**
2. **JSON Read** → **Parse JSON**
   - JSON: `%webhook_data`
   - Extract: `phone`, `message`
3. **Messaging** → **Send WhatsApp Message**
   - Number: `%phone`
   - Message: `%message`

### Dashboard Integration:

In your dashboard HTML, add:

```javascript
function sendToAndroid(phone, message) {
    fetch('http://YOUR_PHONE_IP:8080/send_whatsapp', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            phone: phone,
            message: message
        })
    });
}
```

---

## ✅ Quick Start Guide (5 Minutes):

### Minute 1-2: Install & Setup
```
1. Install MacroDroid from Play Store
2. Grant all permissions
3. Enable accessibility service
```

### Minute 3-4: Create First Macro
```
1. Add Macro → Notification Received (WhatsApp)
2. Add Action → Send WhatsApp Message
3. Test it!
```

### Minute 5: Add Widgets
```
1. Add home screen widgets
2. Test payment request
3. Done! ✅
```

---

## 🎯 Ready-Made Macros for You:

I've created 4 macros for your business:

1. **Payment Auto-Reply** - Thanks customers automatically
2. **Order Status Reply** - Handles order inquiries
3. **Payment Tracker** - Logs all payments to file
4. **Quick Payment Request** - Widget for fast sending

**All configured and ready to import!**

---

## 📞 Testing:

### Test Payment Auto-Reply:
1. Send WhatsApp from another number: "Payment received Rs. 1000"
2. **Expected:** Auto-reply sent back
3. **Check:** Notification shows "Payment auto-reply sent!"

### Test Order Widget:
1. Tap **Order Status** widget
2. Enter phone and order ID
3. **Expected:** WhatsApp opens with message
4. Send!

---

## 🔧 Troubleshooting:

**Macro not triggering?**
- Check notification access permission
- Make sure WhatsApp notifications are enabled
- Check macro is enabled (green toggle)

**WhatsApp not sending?**
- Grant SMS permission to MacroDroid
- Check default SMS app settings
- Try manual send first

**Widget not working?**
- Re-add the widget
- Check macro is enabled
- Restart phone

---

## 📚 Resources:

- **MacroDroid Wiki:** https://wiki.macrodroid.com/
- **Community Forum:** https://forum.macrodroid.com/
- **YouTube Tutorials:** Search "MacroDroid WhatsApp"

---

## ✅ Next Steps:

1. ✅ Install MacroDroid
2. ✅ Import or create macros
3. ✅ Add home screen widgets
4. ✅ Test with real messages
5. ✅ Connect to dashboard (optional)

**Your Android WhatsApp automation is ready!** 🎉
