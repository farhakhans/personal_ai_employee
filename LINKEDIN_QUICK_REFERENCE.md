# 🚀 LinkedIn CLI - Quick Reference

## Setup (One Time)

```bash
# Step 1: Get LinkedIn token
python get_linkedin_token.py

# Step 2: Test connection
python post_linkedin_cli.py --test
```

## Quick Commands

```bash
# Post to LinkedIn
python post_linkedin_cli.py "Your message here"

# Or use batch file (Windows)
post_linkedin.bat "Your message here"

# Post from file
python post_linkedin_cli.py --file post.txt

# View recent posts
python post_linkedin_cli.py --posts

# View notifications
python post_linkedin_cli.py --notifications

# Test connection
python post_linkedin_cli.py --test
```

## Examples

```bash
# Simple post
python post_linkedin_cli.py "Excited to share our Q4 results! #Business #Growth"

# Post with title
python post_linkedin_cli.py "Join our webinar tomorrow" --title "Event Announcement"

# Post from file
echo "Detailed company update..." > update.txt
python post_linkedin_cli.py --file update.txt

# Check recent activity
python post_linkedin_cli.py --posts --count 10
python post_linkedin_cli.py --notifications --count 20
```

## Credentials Setup

Add to `.env` file:
```env
LINKEDIN_ACCESS_TOKEN=your-token-here
LINKEDIN_PERSON_URN=urn:li:person:YOUR_ID
```

Get token: `python get_linkedin_token.py`

---
**Full Guide:** See `LINKEDIN_CLI_GUIDE.md`
