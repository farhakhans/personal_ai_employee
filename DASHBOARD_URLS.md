# ✅ Correct Dashboard URLs

## Working Endpoints

### Root
```
http://localhost:5000
→ Login page
Status: 200 ✓
```

### Bronze Tier
```
http://localhost:5000/bronze
→ Bronze dashboard with vault monitoring
Status: 200 ✓
```

### Silver Tier
```
http://localhost:5000/silver
→ Silver dashboard with approval workflows
Status: 200 ✓
```

### Gold Tier
```
http://localhost:5000/gold
→ Gold dashboard with accounting & audits
Status: 200 ✓
```

### Platinum Tier
```
http://localhost:5000/platinum
→ Platinum dashboard with advanced metrics
Status: 200 ✓
```

---

## ❌ INCORRECT URLs (Will return 404)

```
http://localhost:5000/bronze_dashboard.html      ✗
http://localhost:5000/silver_dashboard.html      ✗
http://localhost:5000/gold_dashboard.html        ✗
http://localhost:5000/platinum_dashboard.html    ✗
http://localhost:5000/api/bronze                 ✗
http://localhost:5000/index.html                 ✗
```

---

## API Endpoints (Use these for testing)

```
http://localhost:5000/api/health          → System status
http://localhost:5000/api/version         → Version info
http://localhost:5000/api/auth/login      → Login endpoint
http://localhost:5000/api/bronze/stats    → Bronze tier stats
http://localhost:5000/api/silver/workflows → Silver tier workflows
http://localhost:5000/api/gold/reports    → Gold tier reports
http://localhost:5000/api/platinum/metrics → Platinum metrics
```

---

## Default Credentials

```
Admin:    admin@employee.ai / Admin@2026!
Manager:  manager@employee.ai / Manager@2026!
User:     user@employee.ai / User@2026!
```

---

## Troubleshooting

**If you get "Endpoint not found":**
1. Make sure you're using `/bronze` not `/bronze_dashboard.html`
2. Make sure the URL exactly matches (case-sensitive)
3. Clear browser cache (Ctrl+Shift+Delete)
4. Check the terminal to see if Flask is still running
5. Make sure Flask returned 200 status code

**If you get "Connection refused":**
1. Make sure `python api_routes.py` is still running
2. Check that port 5000 is not blocked
3. Try `http://127.0.0.1:5000` instead of `localhost:5000`
