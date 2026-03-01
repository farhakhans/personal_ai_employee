# 🔐 Google Sign-In Setup Guide

## Step 1: Create Google Cloud Project

1. Go to **Google Cloud Console**: https://console.cloud.google.com/
2. Click **"Create Project"** or select existing project
3. Name it: `AI Employee System`
4. Click **"Create"**

## Step 2: Enable Google+ API

1. In the Google Cloud Console, go to **APIs & Services** → **Library**
2. Search for **"Google+ API"**
3. Click on it and press **"Enable"**

## Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. If prompted, configure the **OAuth consent screen**:
   - User Type: **External**
   - App name: **AI Employee System**
   - User support email: Your email
   - Developer contact: Your email
   - Click **"Save and Continue"**
   - Scopes: Skip this step
   - Test users: Add your Gmail address
   - Click **"Save and Continue"**

4. Now create OAuth Client ID:
   - Application type: **Web application**
   - Name: `AI Employee Web Client`
   - **Authorized JavaScript origins**:
     - `http://localhost:5000`
     - `http://127.0.0.1:5000`
   - **Authorized redirect URIs**:
     - `http://localhost:5000/auth/google/callback`
     - `http://127.0.0.1:5000/auth/google/callback`
   - Click **"Create"**

5. **Copy your Client ID** - it will look like:
   ```
   123456789-abcdefghijklmnop.apps.googleusercontent.com
   ```

## Step 4: Update login_custom.html

Open `login_custom.html` and find this line (around line 280):

```javascript
const GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com';
```

Replace with your actual Client ID:

```javascript
const GOOGLE_CLIENT_ID = '123456789-abcdefghijklmnop.apps.googleusercontent.com';
```

## Step 5: Restart Flask Server

1. Stop the current Flask server (Ctrl+C)
2. Run: `python api_routes.py`
3. Open: `http://localhost:5000/login-page`

## Step 6: Test Google Sign-In

1. Click **"Sign in with Google"** button
2. Google popup will appear
3. Select your Gmail account
4. You'll be redirected to the dashboard!

## 🎯 What Happens:

1. User clicks Google Sign-In
2. Google shows account selector
3. User selects Gmail account
4. Google returns user info (name, email, picture)
5. System creates/logs in user
6. Redirects to dashboard

## ⚠️ Important Notes:

- **For Development**: Use `http://localhost:5000`
- **For Production**: Add your domain to authorized origins
- **Test Users**: Only test users can sign in until app is verified
- **Scopes**: Default scopes include email and profile

## 🔧 Troubleshooting:

### "Invalid Client ID"
- Make sure you copied the full Client ID
- Check that it ends with `.apps.googleusercontent.com`

### "Redirect URI Mismatch"
- Verify the redirect URI in Google Console matches exactly
- Include `http://` and no trailing slash

### "Access Blocked"
- Add your test email to OAuth consent screen test users
- Or publish the app (requires verification)

## 📧 Need Help?

Google Cloud Console: https://console.cloud.google.com/
OAuth Documentation: https://developers.google.com/identity/protocols/oauth2
