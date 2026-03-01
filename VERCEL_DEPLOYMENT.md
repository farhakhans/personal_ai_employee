# Vercel Deployment Guide - Personal AI Employee

## Quick Deploy

### Step 1: Vercel Account Setup
1. Visit [vercel.com](https://vercel.com)
2. Sign up with GitHub (recommended) or email
3. Install Vercel CLI (optional):
   ```bash
   npm install -g vercel
   ```

### Step 2: Deploy to Vercel

**Option A: Using Vercel Dashboard (Recommended)**
1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Git Repository"
3. Select your GitHub repository
4. Click "Import"
5. Configure project:
   - **Framework Preset**: Python
   - **Root Directory**: `./`
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
6. Click "Deploy"

**Option B: Using Vercel CLI**
```bash
# Login to Vercel
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Step 3: Environment Variables

Vercel Dashboard mein ja kar ye environment variables set karen:

1. Vercel Dashboard → Project → Settings → Environment Variables
2. Add following variables:

```
ANTHROPIC_API_KEY=sk-ant-...your-api-key...
VAULT_PATH=/tmp/vault
SECRET_KEY=your-production-secret-key-change-this
GMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
WHATSAPP_PHONE_ID=your_phone_id
WHATSAPP_ACCESS_TOKEN=your_meta_token
```

### Step 4: Database Configuration

**Important**: Vercel serverless hai, SQLite persist nahi hoga. 

**Solutions:**

1. **Use External Database (Recommended)**
   - [Supabase](https://supabase.com) - Free PostgreSQL
   - [Neon](https://neon.tech) - Free serverless PostgreSQL
   - [Railway](https://railway.app) - Free tier

2. **Update `api_routes.py`** for external DB:
   ```python
   # Replace SQLite connection string
   DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://...')
   ```

### Step 5: Test Deployment

```bash
# Test locally with Vercel environment
vercel dev

# Visit your deployed URL
https://your-project.vercel.app
```

## Important Notes

### ⚠️ Limitations on Vercel

1. **SQLite Database**: Serverless environment mein persist nahi hoti
   - Solution: External PostgreSQL use karen

2. **File System**: Read-only except `/tmp` directory
   - `/tmp` folder temporary files ke liye use ho sakta hai
   - Permanent storage ke liye external service use karen

3. **Background Processes**: WhatsApp watcher, Gmail watcher serverless mein nahi chalenge
   - Solution: External cron jobs ya separate service use karen

4. **WebSocket/Long-running Connections**: Support nahi hai
   - WhatsApp real-time features limit ho sakte hain

### ✅ What Works

- User authentication (login/register)
- Dashboard pages
- API endpoints
- Static file serving (HTML, CSS, JS)
- JWT tokens

### 🔧 Recommended Changes for Production

1. **Update `api_routes.py`**:
   - Use external PostgreSQL database
   - Remove file-based operations
   - Use environment variables for all secrets

2. **Add `DATABASE_URL`** environment variable

3. **Update WhatsApp integration**:
   - Use webhook-based approach
   - Remove local file watchers

## Troubleshooting

### Build Fails
```bash
# Check requirements.txt
pip install -r requirements.txt

# Test locally
python app.py
```

### Runtime Errors
- Check Vercel Functions logs in dashboard
- Verify environment variables are set
- Check database connection string

### Database Issues
- SQLite Vercel par persist nahi hota
- PostgreSQL migration recommended

## Useful Commands

```bash
# Local development
python app.py

# Vercel local testing
vercel dev

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs

# List deployments
vercel ls
```

## Next Steps

1. ✅ Deploy to Vercel
2. ⚠️ Migrate to PostgreSQL for production
3. ⚠️ Setup external services for WhatsApp/Gmail watchers
4. ✅ Test authentication flow
5. ✅ Verify dashboard pages load correctly

## Support

- [Vercel Python Documentation](https://vercel.com/docs/runtimes/official-runtimes/python)
- [Vercel Environment Variables](https://vercel.com/docs/environment-variables)
- [Vercel Serverless Functions](https://vercel.com/docs/functions)
