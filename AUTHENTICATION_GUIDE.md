# 🔐 Authentication System - Setup Guide

## ✅ What Has Been Implemented

### Real Authentication with Login Required Before Accessing Tiers

Your Personal AI Employee system now has **complete authentication** with:

1. **Login/Register Page** (`index.html`)
   - Beautiful tabbed interface
   - Login form with email/password
   - Registration form with validation
   - Demo account credentials displayed
   - Password visibility toggle
   - Auto-redirect after login

2. **Protected Dashboard Routes**
   - `/bronze` - Bronze tier dashboard
   - `/silver` - Silver tier dashboard
   - `/gold` - Gold tier dashboard
   - `/platinum` - Platinum tier dashboard
   - `/status` - System status page
   - `/dashboard` - Complete dashboard

3. **Authentication Checks**
   - All dashboards check for valid JWT token
   - Auto-redirect to login if not authenticated
   - Token validation with API on each page load
   - User info display (username, tier, role)

4. **Backend API** (`api_routes.py`)
   - JWT token authentication (24-hour expiry)
   - Refresh token support (7-day expiry)
   - bcrypt password hashing (12 rounds)
   - SQLite database for user storage
   - Audit logging for all actions
   - Role-based access control

---

## 🚀 How to Run

### Step 1: Start the API Server

```bash
cd "D:\DocuBook-Chatbot folder\Personal AI Employee"
python api_routes.py
```

Expected output:
```
======================================================================
PERSONAL AI EMPLOYEE - API SERVER
======================================================================
Starting server on: http://localhost:5000

Available Endpoints:
  Authentication:
    POST /api/auth/register  - Register new user
    POST /api/auth/login     - Login
    POST /api/auth/logout    - Logout (requires token)
    GET  /api/auth/me        - Get current user (requires token)

  Protected Pages:
    GET /status   - System status
    GET /bronze   - Bronze tier dashboard
    GET /silver   - Silver tier dashboard
    GET /gold     - Gold tier dashboard
    GET /platinum - Platinum tier dashboard
    GET /dashboard - Complete dashboard

Default Accounts:
  Admin:   admin@employee.ai    / Admin@2026!
  Manager: manager@employee.ai  / Manager@2026!
  User:    user@employee.ai     / User@2026!

Press Ctrl+C to stop the server
======================================================================
```

### Step 2: Open Browser

```
http://localhost:5000/
```

### Step 3: Login or Register

**Option A: Use Demo Account**
- Click on any demo credential
- Email: `admin@employee.ai`
- Password: `Admin@2026!`
- Click "Sign In"

**Option B: Register New Account**
1. Click "Register" tab
2. Fill in:
   - Full Name: Your name
   - Email: your.email@example.com
   - Username: yourname (3-20 chars)
   - Password: Strong password (see requirements)
   - Confirm Password: Same as above
3. Click "Create Account"
4. Auto-switches to Login tab
5. Login with your new credentials

---

## 🔒 Password Requirements

Passwords must contain:
- ✅ At least 8 characters
- ✅ One uppercase letter (A-Z)
- ✅ One lowercase letter (a-z)
- ✅ One number (0-9)
- ✅ One special character (!@#$%^&*)

**Examples:**
- ✅ `MyPass@123` - Valid
- ✅ `SecureP@ss` - Valid
- ❌ `password` - Invalid (no uppercase, number, special char)
- ❌ `Pass` - Invalid (too short)

---

## 🎯 Authentication Flow

### Login Flow:
```
1. User visits http://localhost:5000/
2. Enters email and password
3. Clicks "Sign In"
4. API validates credentials
5. Returns JWT access token + refresh token
6. Tokens stored in localStorage
7. Auto-redirect to /status page
8. User info displayed
```

### Tier Access:
```
1. User clicks tier button (e.g., "Bronze")
2. Browser navigates to /bronze
3. Page loads auth check script
4. Script checks localStorage for token
5. If no token → redirect to /
6. If token exists → verify with API
7. If valid → show dashboard + user info
8. If invalid → clear tokens → redirect to /
```

### Logout Flow:
```
1. User clicks "Logout" button
2. API call to /api/auth/logout
3. Server invalidates session
4. Client clears localStorage
5. Redirect to login page
```

---

## 📊 Default Accounts

| Role    | Email                  | Password      | Tier      |
|---------|------------------------|---------------|-----------|
| Admin   | admin@employee.ai      | Admin@2026!   | Platinum  |
| Manager | manager@employee.ai    | Manager@2026! | Gold      |
| User    | user@employee.ai       | User@2026!    | Bronze    |

---

## 🧪 Testing the Authentication

### Test 1: Access Without Login
1. Open incognito/private browser
2. Go to `http://localhost:5000/bronze`
3. Should auto-redirect to login page

### Test 2: Login with Demo Account
1. Go to `http://localhost:5000/`
2. Use demo credentials
3. Should redirect to `/status`
4. See user info displayed

### Test 3: Access Tier After Login
1. Login successfully
2. Click "Bronze" tier button
3. Should access dashboard
4. See user info badge at top-right

### Test 4: Register New User
1. Click "Register" tab
2. Fill registration form
3. Click "Create Account"
4. Should show success message
5. Auto-switch to Login tab
6. Email pre-filled
7. Login with new credentials

### Test 5: Logout
1. Login successfully
2. Click "Logout" button
3. Should redirect to login page
4. Try accessing `/bronze` → should redirect to login

### Test 6: Token Expiry Simulation
1. Login successfully
2. Open browser DevTools (F12)
3. Go to Application → Local Storage
4. Delete `accessToken`
5. Refresh page
6. Should redirect to login

---

## 🔧 API Endpoints

### Authentication
```bash
# Register
POST http://localhost:5000/api/auth/register
Content-Type: application/json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "username": "johndoe",
  "password": "SecureP@ss123"
}

# Login
POST http://localhost:5000/api/auth/login
Content-Type: application/json
{
  "email": "admin@employee.ai",
  "password": "Admin@2026!"
}

# Logout (requires token)
POST http://localhost:5000/api/auth/logout
Authorization: Bearer YOUR_ACCESS_TOKEN

# Get Current User (requires token)
GET http://localhost:5000/api/auth/me
Authorization: Bearer YOUR_ACCESS_TOKEN

# Refresh Token
POST http://localhost:5000/api/auth/refresh
Content-Type: application/json
{
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

### System
```bash
# Health Check (no auth required)
GET http://localhost:5000/api/health

# Version Info (no auth required)
GET http://localhost:5000/api/version
```

---

## 📁 Files Modified/Created

### Created:
- `api_routes.py` - Main Flask API server with authentication
- `index.html` - New login/register page

### Modified:
- `bronze_dashboard.html` - Added auth check + user info display
- `silver_dashboard.html` - Added auth check + user info display
- `gold_dashboard.html` - Added auth check + user info display
- `platinum_dashboard.html` - Added auth check + user info display
- `status.html` - Added auth check + improved user info display

---

## 🐛 Troubleshooting

### "Cannot access login page"
- Make sure server is running: `python api_routes.py`
- Check port 5000 is not in use
- Try: `http://localhost:5000/`

### "Token invalid" error
- Token may have expired (24 hours)
- Clear localStorage and login again
- Check system time is correct

### "Registration fails"
- Check password meets requirements
- Ensure email format is valid
- Username must be 3-20 chars (letters, numbers, underscore)
- Email/username must be unique

### "Page redirects to login"
- Token not found in localStorage
- Token expired or invalid
- API server not running
- Check browser console for errors

### "Logout doesn't work"
- Check API server is running
- Token may already be invalid
- Clear localStorage manually (F12 → Application → Local Storage → Clear)

---

## 🔐 Security Features

✅ **Implemented:**
- bcrypt password hashing (12 rounds)
- JWT token authentication (HS256)
- 24-hour access token expiry
- 7-day refresh token expiry
- Input validation (email, username, password)
- SQL injection prevention (parameterized queries)
- Audit logging of all auth actions
- Session tracking
- Duplicate email/username prevention

🔜 **Future Enhancements:**
- Email verification
- Password reset functionality
- 2FA (Two-factor authentication)
- Rate limiting on login attempts
- Account lockout after failed attempts
- Social login (Google, GitHub)

---

## 📝 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    role TEXT DEFAULT 'user',
    tier TEXT DEFAULT 'bronze',
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Sessions Table
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

### Audit Logs Table
```sql
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    details TEXT,
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

---

## 🎉 Summary

Your Personal AI Employee system now has:

✅ **Real authentication** - No fake login
✅ **Mandatory login** - Must login before accessing any tier
✅ **JWT tokens** - Secure, industry-standard authentication
✅ **User registration** - Anyone can create an account
✅ **Password validation** - Strong password enforcement
✅ **Auto-redirect** - Unauthenticated users sent to login
✅ **User info display** - See logged-in user on all dashboards
✅ **Audit logging** - All actions tracked
✅ **Role-based access** - Admin, Manager, User roles
✅ **Tier system** - Bronze, Silver, Gold, Platinum

---

**Ready to use!** 🚀

Start the server: `python api_routes.py`
Open browser: `http://localhost:5000/`
Login and enjoy!

---

**Last Updated:** February 27, 2026
**Version:** 2.0 - Authentication Complete
