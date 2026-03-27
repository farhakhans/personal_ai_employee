# 🔧 LinkedIn Post Troubleshooting Guide

## Problem: Post API mein create ho rahi hai par LinkedIn par show nahi ho rahi

### Common Issues & Solutions

---

## 1. ❌ Wrong API Endpoint (FIXED ✓)

**Problem:** Purana `/shares` endpoint use ho raha tha jo deprecated hai.

**Solution:** Ab `/ugcPosts` endpoint use hota hai for proper visibility.

```python
# OLD (Deprecated)
endpoint = "https://api.linkedin.com/v2/shares"

# NEW (Correct)
endpoint = "https://api.linkedin.com/v2/ugcPosts"
```

**Changes Made:**
- Updated `linkedin_poster.py` to use `ugcPosts` endpoint
- Added proper UGC (User Generated Content) format
- Added `LinkedIn-Version: 202402` header

---

## 2. ❌ Token Scope Issue

**Problem:** Token mein `w_member_social` permission nahi hai.

**Solution:** Dobara token generate karein with correct scope:

```bash
python get_linkedin_token.py
```

**Required Scope:**
```
w_member_social r_liteprofile
```

---

## 3. ❌ Person URN Format Issue

**Problem:** Person URN galat format mein hai.

**Solution:** Check karein ki URN sahi format mein ho:

```env
# Correct format
LINKEDIN_PERSON_URN=urn:li:person:ACoAABCD123
```

**NOT:**
```env
# Wrong formats
LINKEDIN_PERSON_URN=ACoAABCD123
LINKEDIN_PERSON_URN=person:ACoAABCD123
```

---

## 4. ❌ LinkedIn App Permissions

**Problem:** LinkedIn app mein required permissions enable nahi hain.

**Solution:**

1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps)
2. Select your app
3. Click "Auth" tab
4. Under "Default scope", ensure these are checked:
   - `w_member_social` (Share on LinkedIn)
   - `r_liteprofile` (View basic profile)
5. Save changes
6. Regenerate token

---

## 5. ❌ API Version Mismatch

**Problem:** Old LinkedIn API version use ho rahi hai.

**Solution:** Add version header:

```python
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0",
    "LinkedIn-Version": "202402"  # Latest version
}
```

---

## 6. ❌ Post Content Issues

**Problem:** Post content mein invalid characters ya format issues.

**Solution:**

- Max 3000 characters
- No HTML tags
- Valid UTF-8 encoding
- No spam links

**Example Valid Post:**
```python
message = "Excited to share our latest product update! 🚀 #Innovation #Tech"
```

---

## 7. ❌ Visibility Settings

**Problem:** Post private visibility mein create ho rahi hai.

**Solution:** Ensure PUBLIC visibility:

```python
share_data = {
    "author": f"urn:li:person:{person_urn}",
    "lifecycleState": "PUBLISHED",  # Important!
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {"text": message},
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"  # Important!
    }
}
```

---

## Testing Steps

### Step 1: Test Connection
```bash
python post_linkedin_cli.py --test
```

**Expected Output:**
```
✅ Connected successfully!
   User: Your Name
   ID: ACoAABCD123
```

### Step 2: Post Test Message
```bash
python post_linkedin_cli.py "Test post from CLI - $(date)"
```

**Expected Output:**
```
✅ Post published successfully!
   Post ID: urn:li:ugcPost:7045678901234567890
   URL: https://www.linkedin.com/feed/update/urn:li:ugcPost:7045678901234567890
```

### Step 3: Verify on LinkedIn
1. Open the URL from response
2. Or go to your LinkedIn profile
3. Check if post appears in your activity

---

## API Response Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 201 | Success | Post created ✓ |
| 400 | Bad Request | Check request format |
| 401 | Unauthorized | Token invalid/expired |
| 403 | Forbidden | Missing permissions |
| 404 | Not Found | Invalid endpoint |
| 429 | Rate Limited | Too many requests |

---

## Debug Mode

Enable detailed logging:

```bash
# Set environment variable
export LINKEDIN_DEBUG=true

# Run CLI
python post_linkedin_cli.py "Test message"
```

**Check logs in:**
```
AI_Employee_System/Vault/System/social_logs/linkedin/
```

---

## Manual Verification

### Check Token Validity
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://api.linkedin.com/v2/me
```

### Check Recent Posts
```bash
python post_linkedin_cli.py --posts
```

### Check Notifications
```bash
python post_linkedin_cli.py --notifications
```

---

## Quick Fix Checklist

- [ ] Token generated with `w_member_social` scope
- [ ] Person URN in correct format
- [ ] Using `ugcPosts` endpoint (not `shares`)
- [ ] `LinkedIn-Version: 202402` header added
- [ ] Post visibility set to PUBLIC
- [ ] `lifecycleState: PUBLISHED`
- [ ] LinkedIn app permissions enabled
- [ ] No special characters causing issues

---

## Still Not Working?

### 1. Check API Deprecation
Visit: https://www.linkedin.com/developers/changelog

### 2. Verify App Status
- App must be in "Live" mode (not "Draft")
- Brand account must be verified

### 3. Contact LinkedIn Support
https://www.linkedin.com/help/linkedin/answer/a1348417

---

## Updated Code Location

**File:** `AI_Employee_System/Watchers/linkedin_poster.py`

**Key Changes:**
```python
# Line 114: New endpoint
endpoint = f"{self.base_url}/ugcPosts"

# Line 117-120: Updated headers
headers = {
    "Authorization": f"Bearer {self.access_token}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0",
    "LinkedIn-Version": "202402"
}

# Line 127-140: UGC format
share_data = {
    "author": f"urn:li:person:{self.person_urn}",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {"text": post_text},
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}
```

---

**After applying these fixes, your posts should appear on LinkedIn!** ✅
