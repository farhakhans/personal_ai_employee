# 📝 LinkedIn CLI Posting Guide

Post to LinkedIn directly from command line using AI Employee System.

## 🚀 Quick Start

### 1. Setup LinkedIn Credentials

Pehle LinkedIn API credentials configure karein:

**Option A: Auto Get Token (Recommended)**
```bash
python get_linkedin_token.py
```

**Option B: Manual Setup**
`.env` file mein add karein:
```env
LINKEDIN_ACCESS_TOKEN=your-linkedin-access-token
LINKEDIN_PERSON_URN=urn:li:person:YOUR_ID
```

### 2. Test Connection
```bash
python post_linkedin_cli.py --test
```

## 📋 Usage Examples

### Post Text Update
```bash
# Simple post
python post_linkedin_cli.py "Hello LinkedIn! This is my first post from AI Employee."

# Post with title
python post_linkedin_cli.py "Excited to announce our new product launch!" --title "Product Launch"

# Using batch file (Windows)
post_linkedin.bat "Hello from CLI!"
```

### Post from File
```bash
# Create a file with your post content
echo "This is a detailed post about our company achievements..." > post.txt

# Post from file
python post_linkedin_cli.py --file post.txt

# With title
python post_linkedin_cli.py --file post.txt --title "Company Update"
```

### Post with Image
```bash
python post_linkedin_cli.py --image "Check out our new office!" "https://example.com/image.jpg"
```

### View Recent Posts
```bash
# Show last 5 posts
python post_linkedin_cli.py --posts

# Show last 10 posts
python post_linkedin_cli.py --posts --count 10
```

### View Notifications
```bash
# Show recent notifications (likes, comments, mentions)
python post_linkedin_cli.py --notifications

# Show last 20 notifications
python post_linkedin_cli.py --notifications --count 20
```

### Test Connection
```bash
python post_linkedin_cli.py --test
```

## 🔧 Command Reference

| Command | Description |
|---------|-------------|
| `python post_linkedin_cli.py "message"` | Post a message |
| `--file <filename>` | Read message from file |
| `--title <title>` | Add title to post |
| `--test` | Test LinkedIn API connection |
| `--posts` | Show recent posts |
| `--notifications` | Show recent notifications |
| `--image "msg" "url"` | Post with image |
| `--count <number>` | Number of items to fetch |
| `--help` | Show help message |

## 📁 Batch File (Windows)

Quick commands using `post_linkedin.bat`:

```batch
REM Post message
post_linkedin.bat "Hello LinkedIn!"

REM Test connection
post_linkedin.bat --test

REM View posts
post_linkedin.bat --posts

REM View notifications
post_linkedin.bat --notifications
```

## 🔐 Getting LinkedIn Token

### Step 1: Create LinkedIn App
1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
2. Click "Create app"
3. Fill in app details
4. Get **Client ID** and **Client Secret**

### Step 2: Get Access Token
```bash
python get_linkedin_token.py
```

Follow the prompts:
1. Enter Client ID
2. Enter Client Secret
3. Open the authorization URL in browser
4. Authorize the app
5. Copy the code from redirect URL
6. Token will be saved to `.env` automatically

### Step 3: Verify
```bash
python post_linkedin_cli.py --test
```

## 📊 Output Examples

### Successful Post
```
======================================================================
  💼 LINKEDIN CLI POSTER - AI Employee System
======================================================================

📝 Posting to LinkedIn...
   Title: Company Update
   Message length: 150 characters

✅ Post published successfully!
   Post ID: urn:li:share:7045678901234567890
   URL: https://www.linkedin.com/feed/update/urn:li:share:7045678901234567890
   Saved to vault: Yes
```

### Recent Posts
```
======================================================================
  💼 LINKEDIN CLI POSTER - AI Employee System
======================================================================

📊 Fetching recent posts...
✅ Found 5 posts

--- Post 1 ---
ID: urn:li:share:7045678901234567890
Text: Excited to announce our Q4 results...
Created: 1680123456789

--- Post 2 ---
ID: urn:li:share:7045678901234567891
Text: Join us for our upcoming webinar...
Created: 1680023456789
```

### Notifications
```
======================================================================
  💼 LINKEDIN CLI POSTER - AI Employee System
======================================================================

🔔 Fetching notifications...
✅ Found 15 notifications

1. Type: like
   Activity: urn:li:share:7045678901234567890
   Time: 1680123456789

2. Type: comment
   Activity: urn:li:share:7045678901234567890
   Time: 1680123456788

... and 13 more
```

## ❌ Troubleshooting

### Error: LINKEDIN_ACCESS_TOKEN not configured
```
Solution: Run 'python get_linkedin_token.py' or manually add to .env
```

### Error: Invalid token
```
Solution: Token may have expired. Generate a new one using get_linkedin_token.py
```

### Error: 403 Forbidden
```
Solution: Check if your LinkedIn app has 'w_member_social' permission
```

### Error: Network/connection issue
```
Solution: Check internet connection and firewall settings
```

## 📝 Post Best Practices

1. **Character Limit**: Max 3000 characters
2. **Hashtags**: Use 3-5 relevant hashtags
3. **Timing**: Post during business hours (9 AM - 5 PM)
4. **Engagement**: Respond to comments within 24 hours
5. **Media**: Posts with images get 2x engagement

## 🔗 API Endpoints

For programmatic access, use these API endpoints:

```bash
# Create post
curl -X POST http://localhost:8080/api/social/linkedin/publish \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello LinkedIn!", "title": "Test"}'

# Get posts
curl http://localhost:8080/api/social/linkedin/posts?count=10

# Get notifications
curl http://localhost:8080/api/social/linkedin/notifications?count=20

# Test connection
curl http://localhost:8080/api/social/linkedin/test
```

## 📚 Related Files

- `post_linkedin_cli.py` - Main CLI script
- `post_linkedin.bat` - Windows batch file
- `get_linkedin_token.py` - Token generator
- `.env` - Configuration file
- `AI_Employee_System/Watchers/linkedin_poster.py` - LinkedIn API module

## 💡 Tips

1. **Schedule Posts**: Use `--file` to prepare posts in advance
2. **Test First**: Always run `--test` before posting
3. **Save Drafts**: Keep post templates in separate files
4. **Monitor Engagement**: Check `--notifications` regularly
5. **Backup**: Posts are automatically saved to Vault folder

## 🆘 Support

For issues or questions:
1. Check logs in `AI_Employee_System/Vault/System/social_logs/linkedin/`
2. Run with `--test` to diagnose connection issues
3. Verify credentials in `.env` file
4. Check LinkedIn Developer Portal for API status

---

**Happy Posting! 🚀**
