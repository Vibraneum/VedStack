# 🚀 Deployment Guide - Scalable Food Tracker

Complete guide to deploy your food tracker webhook to the cloud.

---

## Quick Start (5 Minutes)

```bash
# 1. Setup locally
cd /mnt/d/MCP/foodtracker
./setup-webhook.sh

# 2. Configure environment
nano .env  # Add your credentials

# 3. Test locally
./start-local.sh

# 4. Deploy to cloud (choose one)
# Option A: Railway (recommended)
# Option B: Render
```

---

## Prerequisites

### Required:
- ✅ Google Sheet created with ID
- ✅ Google Sheets API credentials (`google-credentials.json`)
- ✅ Omi API key (you have: `omi_dev_2b7983a707b5ede131a0903a1655d918`)
- ✅ Poke API key (you have: `pk_GH6UrWQ1JCpPzmsYTAX0LzNfGKn_TTQDquPUpAOujWM`)

### Optional:
- ⚪ Claude API key (can use Claude Desktop via MCP instead)
- ⚪ GitHub account (for easier deployment)

---

## Step 1: Google Sheets Setup

### 1.1 Create Google Sheet

**On Phone or PC:**

1. Open Google Sheets app/website
2. Create new spreadsheet: "Food Tracker"
3. Rename Sheet1 to "Meals"
4. Add header row:

```
| Date | Time | Food | Portion | Calories | Protein | Carbs | Fat | Fiber | Iron | Calcium | Vit A | Vit C | Meal Type | Timing | Notes | Source | ID |
```

### 1.2 Get Sheet ID

From URL: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit`

Copy the long string between `/d/` and `/edit`

**Example:**
```
https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
                                      ↑
                             THIS IS YOUR SHEET_ID
```

### 1.3 Share Sheet with Service Account

1. Open your `google-credentials.json`
2. Find the `client_email` field (looks like `food-tracker@project-id.iam.gserviceaccount.com`)
3. In Google Sheet, click "Share"
4. Add that email as an Editor
5. Done!

---

## Step 2: Local Setup & Testing

### 2.1 Run Setup Script

```bash
cd /mnt/d/MCP/foodtracker
./setup-webhook.sh
```

This will:
- Create Python virtual environment
- Install all dependencies
- Create `.env` file from example
- Verify Google credentials

### 2.2 Configure Environment

Edit `.env` file:

```bash
nano .env
```

**Required values:**
```bash
HEALTH_SHEET_ID=your_sheet_id_from_step_1_2
OMI_API_KEY=omi_dev_2b7983a707b5ede131a0903a1655d918
POKE_API_KEY=pk_GH6UrWQ1JCpPzmsYTAX0LzNfGKn_TTQDquPUpAOujWM
WEBHOOK_SECRET=generate_random_string_here
GOOGLE_APPLICATION_CREDENTIALS=/home/ved/.config/google-credentials.json
ENVIRONMENT=development
```

**Optional (if using Claude API instead of MCP):**
```bash
CLAUDE_API_KEY=sk-ant-api03-your-key-here
```

Save and exit (Ctrl+O, Enter, Ctrl+X)

### 2.3 Start Local Server

```bash
./start-local.sh
```

You should see:
```
🚀 Starting Food Tracker Webhook Server (Local)...
✅ Virtual environment activated
📝 Configuration:
   Environment: development
   Port: 8000
   Sheet ID: 1BxiMVs0XRA5nFMdKv...
   Claude API: Configured

🌐 Server will be available at:
   Local: http://localhost:8000
   Health: http://localhost:8000/health
   Webhook: http://localhost:8000/omi-webhook

INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2.4 Test Health Endpoint

In another terminal:

```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-12T10:30:00",
  "services": {
    "google_sheets": "connected",
    "claude": "api"
  }
}
```

### 2.5 Test Food Analysis (Development Only)

```bash
curl -X POST http://localhost:8000/test-food-analysis \
  -H "Content-Type: application/json" \
  -d '{"transcript": "I just had a large chicken shawarma with extra sauce"}'
```

Should return detailed food analysis JSON.

---

## Step 3: Deploy to Cloud

### Option A: Railway (Recommended)

**Why Railway:**
- ✅ Free tier: 500 hours/month (enough for this)
- ✅ One-click deploy from GitHub
- ✅ Automatic HTTPS
- ✅ Easy environment variables
- ✅ Generous free tier

**Steps:**

#### 3A.1 Push to GitHub (if not already)

```bash
cd /mnt/d/MCP/foodtracker

# Initialize git (if needed)
git init

# Add files
git add webhook_server.py requirements.txt .env.example
git commit -m "Initial commit: Food tracker webhook"

# Create GitHub repo (via gh CLI or web)
gh repo create food-tracker-webhook --private --source=. --remote=origin --push
```

#### 3A.2 Deploy to Railway

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `food-tracker-webhook` repo
6. Railway auto-detects Python and installs dependencies

#### 3A.3 Configure Environment Variables

In Railway dashboard:

1. Click your project
2. Go to "Variables" tab
3. Add each variable from your `.env` file:
   - `HEALTH_SHEET_ID`
   - `OMI_API_KEY`
   - `POKE_API_KEY`
   - `WEBHOOK_SECRET`
   - `CLAUDE_API_KEY` (if using API)
   - `ENVIRONMENT=production`
   - `PORT=8000`

**For Google Credentials:**
- Copy entire content of `google-credentials.json`
- Add as variable: `GOOGLE_CREDENTIALS_JSON` = `{paste entire JSON}`
- Update webhook_server.py to read from this env var:

```python
# Add at top of webhook_server.py
import json
if os.getenv('GOOGLE_CREDENTIALS_JSON'):
    # Write to temp file
    with open('/tmp/google-creds.json', 'w') as f:
        f.write(os.getenv('GOOGLE_CREDENTIALS_JSON'))
    GOOGLE_CREDENTIALS_PATH = '/tmp/google-creds.json'
```

#### 3A.4 Get Your Public URL

1. In Railway dashboard, go to "Settings"
2. Under "Domains", click "Generate Domain"
3. Copy URL (e.g., `your-app.railway.app`)

#### 3A.5 Verify Deployment

```bash
curl https://your-app.railway.app/health
```

---

### Option B: Render

**Why Render:**
- ✅ Free tier: Always-on web service
- ✅ Auto-deploy from GitHub
- ✅ Built-in monitoring
- ✅ Custom domains

**Steps:**

#### 3B.1 Push to GitHub (same as 3A.1)

#### 3B.2 Create Web Service

1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Connect your `food-tracker-webhook` repo
5. Configure:
   - **Name:** food-tracker-webhook
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python webhook_server.py`

#### 3B.3 Add Environment Variables

In Render dashboard:

1. Go to "Environment" tab
2. Add all variables from `.env` file
3. For `GOOGLE_CREDENTIALS_JSON`, paste entire JSON content

#### 3B.4 Deploy

Click "Create Web Service" - Render will build and deploy automatically.

#### 3B.5 Get Your URL

Copy from Render dashboard (e.g., `your-app.onrender.com`)

---

## Step 4: Configure Omi Webhook

### 4.1 Get Your Webhook URL

From Railway or Render:
```
https://your-app.railway.app/omi-webhook
```
or
```
https://your-app.onrender.com/omi-webhook
```

### 4.2 Register Webhook with Omi

**Method 1: Via Omi Dashboard** (if available)

1. Go to Omi developer dashboard
2. Navigate to Webhooks settings
3. Add new webhook:
   - **URL:** `https://your-app.railway.app/omi-webhook`
   - **Events:** Select "transcript.created" or "segment.created"
   - **Secret:** Use the `WEBHOOK_SECRET` from your `.env`

**Method 2: Via API**

```bash
curl -X POST https://api.omi.me/v1/webhooks \
  -H "Authorization: Bearer omi_dev_2b7983a707b5ede131a0903a1655d918" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-app.railway.app/omi-webhook",
    "events": ["transcript.created"],
    "secret": "your_webhook_secret_here"
  }'
```

**Method 3: Via Omi MCP** (if webhook registration tool available)

Check if Omi MCP has webhook configuration tools.

---

## Step 5: Test End-to-End

### 5.1 Speak to Omi Device

Say something like:
```
"I just had a large chicken shawarma with extra sauce for lunch"
```

### 5.2 Watch the Logs

**Railway:**
- Dashboard → Deployments → View Logs

**Render:**
- Dashboard → Logs tab

You should see:
```
INFO: Received transcript: I just had a large chicken shawarma...
INFO: Food mention detected
INFO: Processing food mention from Vedanth
INFO: Analyzed food: Chicken Shawarma, 1075 cal
INFO: Meal appended to Sheets: Chicken Shawarma
INFO: Poke notification sent successfully
INFO: Food tracking complete: Chicken Shawarma
```

### 5.3 Check Google Sheets

Open your Google Sheet - new row should appear:

| Date | Time | Food | Portion | Calories | ... |
|------|------|------|---------|----------|-----|
| 2025-11-12 | 13:45 | Chicken Shawarma | Large + extra sauce | 1075 | ... |

### 5.4 Check Phone for Poke Notification

You should receive:
```
✅ Meal logged!
🍽️ Chicken Shawarma (Large + extra sauce)
📊 1,075 cal | 67g protein

Today's Progress:
🎯 1,725 cal remaining
💪 53g protein remaining

💡 Excellent protein! Add vegetables for fiber.
```

---

## Step 6: Monitoring & Maintenance

### 6.1 Health Checks

Set up automatic health checks:

**UptimeRobot (Free):**
1. Go to https://uptimerobot.com
2. Add monitor:
   - **Type:** HTTP(S)
   - **URL:** `https://your-app.railway.app/health`
   - **Interval:** 5 minutes
3. Get alerts if server goes down

### 6.2 View Logs

**Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# View logs
railway logs
```

**Render:**
- Dashboard → Logs (real-time)

### 6.3 Error Notifications

Webhook server logs errors to `/tmp/food-tracker-webhook.log`

For critical errors, Poke notifications are sent.

### 6.4 Database Cleanup

Periodically archive old Google Sheets data:

1. Create new tab: "Archive_2025"
2. Move old rows there
3. Keep main "Meals" tab under 10,000 rows for performance

---

## Troubleshooting

### Problem: Webhook not receiving data

**Check:**
1. Verify webhook URL registered with Omi
2. Check Omi dashboard for webhook delivery status
3. View server logs for incoming requests
4. Test webhook manually:
```bash
curl -X POST https://your-app.railway.app/omi-webhook \
  -H "Content-Type: application/json" \
  -d '{"transcript": "I had chicken", "speaker": "Test"}'
```

### Problem: Google Sheets write fails

**Check:**
1. Service account email added as Editor to sheet
2. Sheet ID correct in environment variables
3. Google credentials JSON valid
4. Check logs for specific error

**Test manually:**
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file(
    'google-credentials.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=credentials)

# Try to read sheet
result = service.spreadsheets().values().get(
    spreadsheetId='YOUR_SHEET_ID',
    range='Meals!A1:A10'
).execute()
print(result)
```

### Problem: Claude analysis fails

**Check:**
1. If using API: Verify `CLAUDE_API_KEY` set correctly
2. If using MCP: Ensure Claude Desktop running on server (won't work in cloud - use API)
3. Check Claude API quota/billing

**Recommendation:** Use Claude API for cloud deployment, MCP only for local testing.

### Problem: Poke notifications not sending

**Check:**
1. Poke API key valid
2. Poke API endpoint correct (verify documentation)
3. Check logs for Poke API response

### Problem: Duplicate meals logged

**Check:**
1. Omi webhook firing multiple times
2. Duplicate detection working (check `processed_hashes`)
3. Adjust duplicate detection threshold if needed

---

## Scaling Considerations

### Current Capacity

**Free Tier Limits:**
- Railway: 500 hours/month = always-on for 20 days
- Render: 750 hours/month = always-on for 31 days
- Google Sheets: 100 requests per 100 seconds = plenty for personal use

**Estimated Usage:**
- Meals per day: ~10
- Requests per day: ~50 (meals + health checks)
- Easily within free tier limits

### If You Exceed Free Tier

**Option 1: Upgrade to Paid Plan**
- Railway: $5/month for 500 hours of always-on
- Render: $7/month for unlimited

**Option 2: Optimize Usage**
- Reduce health check frequency (every 15 min instead of 5)
- Batch write to sheets (every 5 meals instead of real-time)
- Use Railway's "sleep after inactivity" (not ideal for webhooks)

### High-Volume Scaling (100+ meals/day)

1. **Add Redis Cache:**
   - Cache frequent foods
   - Reduce Claude API calls

2. **Add Database:**
   - PostgreSQL instead of Sheets
   - Much faster writes
   - Sync to Sheets daily

3. **Add Queue:**
   - RabbitMQ or Redis Queue
   - Process meals asynchronously
   - Handle bursts better

---

## Cost Analysis

### Free Tier (Recommended for personal use)

| Service | Free Tier | Estimated Usage | Cost |
|---------|-----------|-----------------|------|
| Railway | 500 hrs/month | ~24/7 service | $0 |
| Render | 750 hrs/month | ~24/7 service | $0 |
| Google Sheets API | 100 req/100sec | ~50 req/day | $0 |
| Claude API | 100k tokens/month free | ~10k tokens/month | $0 |
| **TOTAL** | | | **$0/month** |

### Paid Tier (if needed)

| Service | Paid Plan | Cost |
|---------|-----------|------|
| Railway Pro | Unlimited hours | $5/month |
| Render Starter | Unlimited hours | $7/month |
| Claude API | Pay-as-you-go | ~$3/month (estimated) |
| **TOTAL** | | **$8-10/month** |

### Claude API Cost Estimate

**Per meal analysis:**
- Prompt: ~500 tokens
- Response: ~300 tokens
- Total: ~800 tokens per meal

**Monthly (10 meals/day):**
- 10 meals × 30 days = 300 meals
- 300 × 800 = 240,000 tokens
- At $3/million tokens (Claude Sonnet) = **~$0.72/month**

Very affordable!

---

## Security Best Practices

### 1. Environment Variables

✅ **DO:**
- Store all secrets in environment variables
- Use different secrets for dev/prod
- Rotate secrets periodically

❌ **DON'T:**
- Commit `.env` file to git
- Share secrets in plaintext
- Use same secret everywhere

### 2. Webhook Security

✅ **DO:**
- Verify webhook signatures
- Use HTTPS only
- Rate limit webhook endpoint

❌ **DON'T:**
- Accept unsigned webhooks in production
- Allow unlimited requests

### 3. API Keys

✅ **DO:**
- Use API keys with minimum required permissions
- Monitor API usage
- Set up billing alerts

❌ **DON'T:**
- Use admin/root keys
- Ignore unusual usage patterns

---

## Backup & Recovery

### Backup Strategy

**1. Google Sheets (Automatic)**
- Google auto-saves and versions
- Can restore previous versions
- Download CSV backup weekly:
```bash
# Manual backup script
gsheet-backup.sh  # See below
```

**2. Environment Config**
- Keep `.env.example` updated
- Document all environment variables
- Store credentials securely (1Password, etc.)

**3. Code**
- Git repository (private)
- Tag releases: `git tag v1.0.0`

### Recovery Procedure

**If webhook goes down:**
1. Check health endpoint
2. View logs for errors
3. Restart service (Railway/Render auto-restarts)
4. If needed, redeploy from GitHub

**If data lost:**
1. Restore Google Sheets from version history
2. Check webhook logs for missed meals
3. Manually enter from Omi app history

---

## Next Steps

### Week 1: Setup & Testing
- ✅ Run setup script
- ✅ Test locally
- ✅ Deploy to Railway/Render
- ✅ Configure Omi webhook
- ✅ Test end-to-end

### Week 2: Monitoring
- ⚪ Set up UptimeRobot
- ⚪ Configure error alerts
- ⚪ Review logs daily
- ⚪ Fine-tune food detection

### Week 3: Optimization
- ⚪ Add food database cache
- ⚪ Improve portion detection
- ⚪ Add custom foods
- ⚪ Tweak Claude prompts

### Month 2: Advanced Features
- ⚪ Add weekly summary emails
- ⚪ Create Google Sheets charts
- ⚪ Build mobile dashboard
- ⚪ Add meal photos (if Omi supports)

---

## Support & Resources

### Documentation
- FastAPI: https://fastapi.tiangolo.com
- Google Sheets API: https://developers.google.com/sheets/api
- Claude API: https://docs.anthropic.com
- Railway: https://docs.railway.app
- Render: https://render.com/docs

### Omi Resources
- Omi Docs: https://docs.omi.me (check for webhooks documentation)
- Omi API: https://api.omi.me (explore available endpoints)
- Omi Community: Check for Discord/forum

### Getting Help

**If something breaks:**
1. Check logs (Railway/Render dashboard)
2. Test health endpoint
3. Verify environment variables
4. Review this troubleshooting guide
5. Check Omi webhook delivery status

---

## Summary Checklist

Before deploying, ensure:

- ✅ Google Sheet created and shared with service account
- ✅ Sheet ID added to `.env`
- ✅ All API keys configured
- ✅ Tested locally successfully
- ✅ Code pushed to GitHub
- ✅ Deployed to Railway or Render
- ✅ Environment variables set in cloud
- ✅ Webhook registered with Omi
- ✅ End-to-end test completed
- ✅ Health check monitoring set up

**You're ready to track food automatically!** 🎉

Just talk to your Omi device and meals appear in Google Sheets within seconds.
