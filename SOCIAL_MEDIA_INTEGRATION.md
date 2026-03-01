# 📱 Social Media Integration Guide

## Quick Setup for All Platforms

### **Gmail Integration** (All Tiers - Bronze+)

**Setup Steps:**
1. Go to https://myaccount.google.com/
2. Security → 2-Step Verification → App passwords
3. Generate app password for 'Mail'
4. Update `.env` file:
   ```env
   GMAIL_ADDRESS=your.email@gmail.com
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
   ```
5. Run watcher:
   ```batch
   python AI_Employee_System\Watchers\start_gmail_watcher.py
   ```

**Direct Link:** [Open Gmail](https://mail.google.com)

---

### **WhatsApp Integration** (Silver Tier+)

**Setup Steps:**
1. Install WhatsApp Business on your phone
2. Open WhatsApp Web in browser
3. Scan QR code with phone
4. Install Playwright:
   ```batch
   pip install playwright
   playwright install chromium
   ```
5. Run watcher:
   ```batch
   python AI_Employee_System\Watchers\start_whatsapp_watcher.py
   ```

**Direct Link:** [Open WhatsApp Web](https://web.whatsapp.com)

---

### **LinkedIn Integration** (Silver Tier+)

**Setup Steps:**
1. Go to LinkedIn Developer Portal
2. Create new app at https://www.linkedin.com/developers/apps
3. Get API credentials:
   - Client ID
   - Client Secret
   - Access Token
4. Update `.env` file:
   ```env
   LINKEDIN_ACCESS_TOKEN=your_access_token
   LINKEDIN_ORGANIZATION_ID=your_org_id
   ```
5. Run poster:
   ```batch
   python AI_Employee_System\Watchers\linkedin_poster.py
   ```

**Direct Links:**
- [LinkedIn Home](https://www.linkedin.com)
- [Create LinkedIn App](https://www.linkedin.com/developers/apps/create)
- [LinkedIn API Docs](https://docs.microsoft.com/en-us/linkedin/)

---

### **Facebook Integration** (Gold Tier+)

**Setup Steps:**
1. Go to Facebook Developers
2. Create app at https://developers.facebook.com/apps
3. Add Facebook Login product
4. Get Page Access Token
5. Update `.env` file:
   ```env
   FACEBOOK_ACCESS_TOKEN=your_page_token
   FACEBOOK_PAGE_ID=your_page_id
   ```
6. Run poster:
   ```batch
   python AI_Employee_System\Watchers\facebook_poster.py
   ```

**Direct Links:**
- [Facebook Business](https://www.facebook.com/business)
- [Facebook Developers](https://developers.facebook.com)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer)

---

### **Instagram Integration** (Gold Tier+)

**Setup Steps:**
1. Convert to Instagram Business Account
2. Connect to Facebook Page
3. Get Instagram Basic Display API credentials
4. Update `.env` file:
   ```env
   INSTAGRAM_ACCESS_TOKEN=your_token
   INSTAGRAM_ACCOUNT_ID=your_account_id
   ```
5. Run poster:
   ```batch
   python AI_Employee_System\Watchers\instagram_poster.py
   ```

**Direct Links:**
- [Instagram Home](https://www.instagram.com)
- [Instagram for Business](https://business.instagram.com)
- [Instagram API Docs](https://developers.facebook.com/docs/instagram-api)

---

### **Twitter/X Integration** (Silver Tier+)

**Setup Steps:**
1. Go to Twitter Developer Portal
2. Apply for developer account at https://developer.twitter.com
3. Create new project and app
4. Get API credentials:
   - API Key
   - API Secret
   - Bearer Token
   - Access Token & Secret
5. Update `.env` file:
   ```env
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_secret
   TWITTER_BEARER_TOKEN=your_bearer_token
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_SECRET=your_access_secret
   ```
6. Run poster:
   ```batch
   python AI_Employee_System\Watchers\twitter_poster.py
   ```

**Direct Links:**
- [Twitter Home](https://twitter.com)
- [Twitter Developer Portal](https://developer.twitter.com)
- [Twitter API Docs](https://developer.twitter.com/en/docs)

---

## 📋 Credential Checklist

| Platform | Credential | Location | Tier |
|----------|-----------|----------|------|
| **Gmail** | App Password | Google Account Security | Bronze+ |
| **WhatsApp** | QR Code Scan | WhatsApp Web | Silver+ |
| **LinkedIn** | Access Token | LinkedIn Developers | Silver+ |
| **Facebook** | Page Access Token | Facebook Developers | Gold+ |
| **Instagram** | Access Token | Instagram Basic Display | Gold+ |
| **Twitter** | API Keys | Twitter Developer Portal | Silver+ |

---

## 🔧 Quick Commands

### Run Individual Watchers:
```batch
# Gmail (All Tiers)
python AI_Employee_System\Watchers\start_gmail_watcher.py

# WhatsApp (Silver+)
python AI_Employee_System\Watchers\start_whatsapp_watcher.py

# LinkedIn (Silver+)
python AI_Employee_System\Watchers\linkedin_poster.py

# Facebook (Gold+)
python AI_Employee_System\Watchers\facebook_poster.py

# Instagram (Gold+)
python AI_Employee_System\Watchers\instagram_poster.py

# Twitter (Silver+)
python AI_Employee_System\Watchers\twitter_poster.py
```

### Run All Watchers (Silver+):
```batch
python AI_Employee_System\Watchers\multi_watchers.py
```

---

## 🔐 Security Best Practices

✅ **DO:**
- Use environment variables (`.env` file)
- Never commit `.env` to Git
- Use app-specific passwords
- Enable 2FA on all accounts
- Rotate credentials monthly

❌ **DON'T:**
- Hardcode credentials in Python files
- Share API keys publicly
- Use personal accounts for business automation
- Skip 2FA setup

---

## 📊 Platform Availability

| Feature | Bronze | Silver | Gold | Platinum |
|---------|--------|--------|------|----------|
| Gmail | ✓ | ✓ | ✓ | ✓ |
| WhatsApp | ✗ | ✓ | ✓ | ✓ |
| LinkedIn | ✗ | ✓ | ✓ | ✓ |
| Twitter | ✗ | ✓ | ✓ | ✓ |
| Facebook | ✗ | ✗ | ✓ | ✓ |
| Instagram | ✗ | ✗ | ✓ | ✓ |

---

## 🆘 Troubleshooting

### Gmail Not Working:
- Make sure IMAP is enabled in Gmail settings
- Use App Password, not regular password
- Check 2FA is enabled

### WhatsApp Not Connecting:
- Make sure QR code is scanned
- Keep browser tab open
- Check Playwright is installed

### LinkedIn API Errors:
- Verify app is approved by LinkedIn
- Check token hasn't expired
- Ensure correct permissions are granted

### Facebook/Instagram Issues:
- Business account required
- Page must be linked to Instagram
- Check token permissions

### Twitter Rate Limits:
- Free tier has limited posts/hour
- Consider elevated access for more posts
- Implement retry logic

---

## 📞 Support

**Documentation:**
- `ALL_TIERS_WORKFLOW.md` - Complete workflow guide
- `GMAIL_SETUP_GUIDE.md` - Gmail setup instructions
- `AI_Employee_System/Watchers/README.md` - Watcher documentation

**Developer Resources:**
- [Gmail API](https://developers.google.com/gmail/api)
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [LinkedIn API](https://docs.microsoft.com/en-us/linkedin/)
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Instagram API](https://developers.facebook.com/docs/instagram-api)
- [Twitter API](https://developer.twitter.com/en/docs)

---

**Last Updated:** February 26, 2026
**Version:** 1.0.0
