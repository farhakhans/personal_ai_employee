# 🔐 Personal AI Employee - API Endpoints Reference

## Base URL
```
http://localhost:5000/api
```

---

## 🔑 AUTHENTICATION ENDPOINTS

### Register New User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "Password123!",
  "full_name": "Full Name"
}
```
✅ **No auth required**

---

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "admin@employee.ai",
  "password": "Admin@2026!"
}
```
✅ **No auth required**
**Response includes:** `access_token`, `refresh_token`

---

### Get Current User
```http
GET /auth/me
Authorization: Bearer YOUR_ACCESS_TOKEN
```
✅ **Requires token**

---

### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```
✅ **Returns new access_token**

---

### Update Profile
```http
PUT /auth/profile
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "full_name": "New Name",
  "tier": "silver"
}
```
✅ **Requires token**

---

### Logout
```http
POST /auth/logout
Authorization: Bearer YOUR_ACCESS_TOKEN
```
✅ **Invalidates session**

---

## 👨‍💼 ADMIN ENDPOINTS (admin role required)

### List All Users
```http
GET /admin/users
Authorization: Bearer ADMIN_TOKEN
```

---

### Get Specific User
```http
GET /admin/users/<user_id>
Authorization: Bearer ADMIN_TOKEN
```

---

### Update User
```http
PUT /admin/users/<user_id>
Authorization: Bearer ADMIN_TOKEN
Content-Type: application/json

{
  "email": "new@email.com",
  "role": "manager",
  "is_active": true
}
```

---

### Delete User
```http
DELETE /admin/users/<user_id>
Authorization: Bearer ADMIN_TOKEN
```

---

## 📊 AUDIT ENDPOINTS

### Get All Audit Logs (admin only)
```http
GET /audit/logs?limit=50
Authorization: Bearer ADMIN_TOKEN
```

---

### Get My Audit Logs
```http
GET /audit/my-logs?limit=20
Authorization: Bearer YOUR_TOKEN
```

---

## 🏥 SYSTEM ENDPOINTS

### Health Check
```http
GET /health
```
✅ **No auth required**

---

### System Version
```http
GET /version
```
✅ **No auth required**

---

### Vault Stats
```http
GET /vault/stats
Authorization: Bearer YOUR_TOKEN
```

---

### System Logs
```http
GET /system/logs?limit=50
Authorization: Bearer YOUR_TOKEN
```

---

## 🥉 BRONZE TIER ENDPOINTS

### Control Watcher
```http
POST /bronze/watcher/<watcher_name>
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "action": "start" | "stop" | "restart"
}
```

---

### Get Watcher Status
```http
GET /bronze/watcher/status
Authorization: Bearer YOUR_TOKEN
```

---

## 🥈 SILVER TIER ENDPOINTS

### Get Approval Queue
```http
GET /silver/approval/queue
Authorization: Bearer YOUR_TOKEN
```

---

### Approve/Reject Task
```http
POST /silver/approval/<task_id>
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "action": "approve" | "reject",
  "comments": "Optional comments"
}
```

---

### Schedule Social Media Post
```http
POST /silver/schedule/post
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "platform": "linkedin",
  "content": "Post content",
  "scheduled_time": "2026-02-25T14:30:00"
}
```

---

### Get Social Metrics
```http
GET /silver/social/metrics
Authorization: Bearer YOUR_TOKEN
```

---

## 🏆 GOLD TIER ENDPOINTS

### Get Accounting Data
```http
GET /gold/accounting/summary
Authorization: Bearer YOUR_TOKEN
```

---

### Generate Audit Report
```http
POST /gold/audit/generate
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "report_type": "weekly" | "monthly"
}
```

---

### Generate CEO Briefing
```http
POST /gold/briefing/generate
Authorization: Bearer YOUR_TOKEN
```

---

### Get Compliance Status
```http
GET /gold/compliance/status
Authorization: Bearer YOUR_TOKEN
```

---

## 💎 PLATINUM TIER ENDPOINTS

### Get Real-time Metrics
```http
GET /platinum/metrics/realtime
Authorization: Bearer YOUR_TOKEN
```

---

### Get Performance KPIs
```http
GET /platinum/kpis/dashboard
Authorization: Bearer YOUR_TOKEN
```

---

### Get Error Recovery Stats
```http
GET /platinum/errors/recovery-stats
Authorization: Bearer YOUR_TOKEN
```

---

### Get AI Insights
```http
GET /platinum/ai/insights
Authorization: Bearer YOUR_TOKEN
```

---

### Trigger AI Optimization
```http
POST /platinum/ai/optimize
Authorization: Bearer YOUR_TOKEN
```

---

## 📋 ERROR HANDLING

### Standard Error Response
```json
{
  "error": "Description of the error"
}
```

**Common Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad request (missing fields)
- `401` - Unauthorized (no token or invalid)
- `403` - Forbidden (insufficient role)
- `404` - Endpoint not found
- `409` - Conflict (user exists)
- `500` - Server error

---

## 🧪 QUICK TEST EXAMPLES

### 1. Get Health Status
```bash
curl http://localhost:5000/api/health
```

### 2. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@employee.ai","password":"Admin@2026!"}'
```

### 3. Use Token (replace TOKEN_HERE)
```bash
curl -H "Authorization: Bearer TOKEN_HERE" \
  http://localhost:5000/api/auth/me
```

### 4. List Users (admin only)
```bash
curl -H "Authorization: Bearer ADMIN_TOKEN_HERE" \
  http://localhost:5000/api/admin/users
```

---

## 🔐 Default Test Credentials

| Role    | Email                  | Password      |
|---------|------------------------|---------------|
| Admin   | admin@employee.ai      | Admin@2026!   |
| Manager | manager@employee.ai    | Manager@2026! |
| User    | user@employee.ai       | User@2026!    |

---

## 🚨 Troubleshooting "Endpoint not found"

1. **Check the URL path** - Make sure it's exactly correct (case-sensitive)
2. **Check HTTP method** - Use POST/GET/PUT/DELETE as specified
3. **Check token** - Most endpoints need `Authorization: Bearer TOKEN` header
4. **Check server running** - Make sure api_routes.py is running
5. **Check JSON format** - POST requests need valid JSON with Content-Type header

### Example Correct Request:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@employee.ai","password":"Admin@2026!"}'
```

### Example Incorrect Request (will give 404):
```bash
curl http://localhost:5000/api/auth/login  # Missing -X POST
curl http://localhost:5000/api/Auth/login  # Wrong case
curl http://localhost:5000/auth/login      # Missing /api
```

