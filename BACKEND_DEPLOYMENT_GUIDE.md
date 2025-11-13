# 🚀 VedStack Backend - Deployment Guide

**Created**: November 13, 2025
**Purpose**: Deploy FastAPI backend for Omi voice → Airtable integration

---

## 📊 PLATFORM COMPARISON

| Platform | Free Tier | Pros | Cons | Recommended? |
|----------|-----------|------|------|--------------|
| **Railway** | 500 hours/month + $5 credit | Easy setup, great logs, auto-deploy from Git | Credit runs out | ✅ **BEST** |
| **Vercel** | Unlimited | Super fast, instant deploy, great DX | 10s timeout (might be tight) | ✅ **GOOD** |
| **Cloudflare Workers** | 100k requests/day | Global edge network, blazing fast | Needs code adaptation | ⚠️ **COMPLEX** |
| **Fly.io** | 3 VMs free | Full control, Docker-based | Slightly complex | ✅ **GOOD** |
| **Render** | Free tier | Simple, reliable | Can be slow to wake | ⚠️ **OKAY** |

**Recommendation**: Start with **Railway** → If you hit credit limits, move to **Vercel** → If timeouts are an issue, try **Fly.io**

---

## 🏗️ WHAT WE BUILT

### Backend Features:
- ✅ Real-time Omi transcript webhook receiver
- ✅ Food keyword detection ("eating", "ate", "roti", "dal", etc.)
- ✅ Food item extraction (regex-based)
- ✅ Macro calculation (from reference data)
- ✅ Session-based deduplication (no duplicate logs)
- ✅ Airtable Food Log integration
- ✅ Daily total calculation
- ✅ Response message for Omi to speak back

### Files Created:
```
backend/
├── main.py              # FastAPI application (300 lines)
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker container config
├── .env.example        # Environment variables template
├── railway.json        # Railway deployment config
├── vercel.json         # Vercel deployment config
└── wrangler.toml       # Cloudflare config
```

---

## 🚀 OPTION 1: RAILWAY (RECOMMENDED)

### Why Railway?
- ✅ Easiest setup (5 minutes)
- ✅ Auto-deploys from Git
- ✅ Great logs and monitoring
- ✅ $5 free credit + 500 hours/month
- ✅ Docker support
- ✅ Environment variables easy to set

### Step-by-Step:

**1. Create Railway Account**
- Go to https://railway.app
- Sign up with GitHub

**2. Create New Project**
- Click "New Project"
- Select "Deploy from GitHub repo"
- Connect your GitHub account
- Select your foodtracker repo

**3. Configure Build**
- Railway auto-detects Dockerfile
- Build path: `backend/`
- Port: `8000`

**4. Add Environment Variables**
- Click project → Variables
- Add:
  ```
  AIRTABLE_PAT=YOUR_AIRTABLE_PAT_HERE
  AIRTABLE_BASE=YOUR_AIRTABLE_BASE_ID_HERE
  ```

**5. Deploy**
- Railway auto-deploys
- Wait 2-3 minutes
- Get public URL: `https://vedstack-omi-backend.up.railway.app`

**6. Test**
- Visit: `https://your-url.railway.app/`
- Should see: `{"status": "online", "service": "VedStack Omi Backend"}`

**7. Get Webhook URL for Omi**
- Your webhook URL: `https://your-url.railway.app/omi/transcript`
- Copy this for Omi app configuration

---

## 🚀 OPTION 2: VERCEL

### Why Vercel?
- ✅ Unlimited free tier
- ✅ Super fast (edge network)
- ✅ Instant deploys
- ⚠️ 10-second timeout (should be fine for our use case)

### Step-by-Step:

**1. Install Vercel CLI**
```bash
npm install -g vercel
```

**2. Login**
```bash
vercel login
```

**3. Navigate to backend folder**
```bash
cd /mnt/d/MCP/foodtracker/backend
```

**4. Deploy**
```bash
vercel
```

**5. Follow prompts:**
- Project name: `vedstack-omi-backend`
- Framework: `Other`
- Deploy: `Yes`

**6. Add Environment Variables**
```bash
vercel env add AIRTABLE_PAT
# Paste: YOUR_AIRTABLE_PAT_HERE

vercel env add AIRTABLE_BASE
# Paste: YOUR_AIRTABLE_BASE_ID_HERE
```

**7. Redeploy**
```bash
vercel --prod
```

**8. Get URL**
- Copy production URL: `https://vedstack-omi-backend.vercel.app`
- Webhook URL: `https://vedstack-omi-backend.vercel.app/omi/transcript`

---

## 🚀 OPTION 3: FLY.IO

### Why Fly.io?
- ✅ Full Docker support
- ✅ 3 VMs free
- ✅ Global regions
- ✅ Good logs

### Step-by-Step:

**1. Install Fly CLI**
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Or via Scoop
scoop install flyctl
```

**2. Login**
```bash
fly auth login
```

**3. Navigate to backend**
```bash
cd /mnt/d/MCP/foodtracker/backend
```

**4. Create app**
```bash
fly launch --name vedstack-omi-backend --region sin --dockerfile Dockerfile
```

**5. Set environment variables**
```bash
fly secrets set AIRTABLE_PAT=YOUR_AIRTABLE_PAT_HERE

fly secrets set AIRTABLE_BASE=YOUR_AIRTABLE_BASE_ID_HERE
```

**6. Deploy**
```bash
fly deploy
```

**7. Get URL**
- Your URL: `https://vedstack-omi-backend.fly.dev`
- Webhook: `https://vedstack-omi-backend.fly.dev/omi/transcript`

---

## 🧪 TESTING YOUR DEPLOYMENT

### Test 1: Health Check

```bash
curl https://your-backend-url.com/
```

**Expected response:**
```json
{
  "status": "online",
  "service": "VedStack Omi Backend",
  "version": "1.0.0"
}
```

### Test 2: Mock Omi Webhook

```bash
curl -X POST https://your-backend-url.com/omi/transcript \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test123",
    "segments": [
      {
        "text": "I am eating 3 rotis with dal",
        "speaker": "SPEAKER_00",
        "is_user": true,
        "start": 0,
        "end": 3
      }
    ]
  }'
```

**Expected response:**
```json
{
  "status": "logged",
  "message": "Logged: 443 cal, 27g protein. You're at 443 cal today, 2557 remaining.",
  "data": {
    "calories": 443,
    "protein": 27,
    "daily_total": 443,
    "target": 3000,
    "remaining": 2557
  }
}
```

### Test 3: Check Airtable

1. Go to https://airtable.com/YOUR_AIRTABLE_BASE_ID_HERE
2. Open Food Log table
3. Check for new entry with:
   - Description: "I am eating 3 rotis with dal"
   - Calories: 443
   - Protein: 27
   - Source: "Omi Voice (Real-time)"

---

## 🎯 CONFIGURE OMI APP

### Once backend is deployed:

**1. Open Omi Mobile App**
- Tap profile → Apps
- Tap "+ Create App"

**2. Choose App Type**
- Select "Integration"
- Select "Real-Time Transcript Processor"

**3. Configure**
- **Name**: VedStack Food Logger
- **Description**: Real-time food tracking for 8-week bulk
- **Webhook URL**: `https://your-backend-url.com/omi/transcript`
- **Capabilities**: Real-time transcript processing

**4. Test**
- Say to Omi: "I'm eating 3 rotis with dal"
- Check backend logs (Railway/Vercel/Fly dashboard)
- Check Airtable Food Log
- Omi should respond: "Logged: 443 cal, 27g protein..."

---

## 📊 MONITORING & LOGS

### Railway:
- Dashboard → Your project → Logs
- Real-time logs visible
- Can search/filter

### Vercel:
- Dashboard → Your project → Functions → Logs
- Shows requests, responses, errors

### Fly.io:
```bash
fly logs
```

**What to look for:**
- `[session_id] Received: I'm eating...`
- `[session_id] Extracted: [{'item': 'roti', 'quantity': 3}, ...]`
- `[session_id] Success: Logged: 443 cal...`

---

## 🐛 TROUBLESHOOTING

### Issue 1: Backend not receiving webhooks

**Check:**
1. Webhook URL is correct in Omi app
2. Backend is running (visit health check endpoint)
3. Check backend logs for incoming requests

**Fix:**
- Verify Omi app webhook URL
- Check if URL is publicly accessible
- Look for CORS errors in logs

### Issue 2: "Not food related" response

**Cause:** Food keywords not detected

**Fix:**
- Add more keywords to `FOOD_KEYWORDS` list in main.py
- Or say explicit food keywords: "I'm eating", "I had", "food"

### Issue 3: Airtable write fails

**Check:**
1. Airtable PAT is correct
2. Base ID is correct
3. Food Log table exists

**Fix:**
- Verify credentials in environment variables
- Check Airtable API permissions (read/write)
- Look for error message in backend logs

### Issue 4: Duplicate logs

**Cause:** Session deduplication not working

**Fix:**
- Check `active_sessions` dict is persisting
- Increase deduplication window (currently 60 seconds)
- Or ignore - better to have duplicates than miss logs

---

## 🔒 SECURITY

### Current Setup:
- ✅ Airtable PAT stored in environment variables (not in code)
- ✅ HTTPS webhooks (secure)
- ✅ No user authentication (Omi app handles this)

### If you want to add authentication:

```python
# Add to main.py

OMI_WEBHOOK_SECRET = os.getenv("OMI_WEBHOOK_SECRET", "")

@app.post("/omi/transcript")
async def handle_omi_transcript(request: Request):
    # Verify webhook signature
    signature = request.headers.get("X-Omi-Signature")
    if not verify_signature(signature, OMI_WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # ... rest of code
```

---

## 💰 COST ESTIMATE

### Railway:
- Free: $5 credit + 500 hours/month
- Paid: $5/month for 500 hours (if you exceed free tier)
- **Expected usage**: ~30 hours/month (well within free tier)

### Vercel:
- Free: Unlimited
- **Expected cost**: $0

### Fly.io:
- Free: 3 VMs (256MB RAM each)
- **Expected cost**: $0

**Recommendation**: All three are FREE for your use case!

---

## 📈 SCALING (Future)

If you get MANY requests (>100k/month):

**Option 1: Cloudflare Workers**
- Adapt FastAPI code to Cloudflare Workers format
- 100k requests/day FREE
- Global edge network

**Option 2: AWS Lambda + API Gateway**
- Serverless
- Pay per request
- Auto-scaling

**Option 3: Self-hosted VPS**
- DigitalOcean/Linode
- $5-10/month
- Full control

**But for now**: Railway/Vercel/Fly free tiers are perfect!

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] Choose platform (Railway, Vercel, or Fly.io)
- [ ] Create account
- [ ] Deploy backend
- [ ] Add environment variables (AIRTABLE_PAT, AIRTABLE_BASE)
- [ ] Test health check endpoint
- [ ] Test mock webhook
- [ ] Verify Airtable write
- [ ] Get webhook URL
- [ ] Configure Omi app with webhook URL
- [ ] Test voice → Airtable flow
- [ ] Monitor logs
- [ ] Celebrate! 🎉

---

## 🎉 WHEN EVERYTHING WORKS

**Your flow:**
```
You: "I'm eating 3 rotis with dal"
     ↓
Omi: [Transcribes in real-time]
     ↓
Webhook → Your Backend → Airtable Food Log
     ↓
Omi: "Logged: 443 cal, 27g protein. You're at 443 cal today, 2557 remaining."
```

**Result:**
- ✅ 3-second logging (vs 30-second photo logging)
- ✅ Hands-free
- ✅ NO memory pollution
- ✅ Real-time feedback
- ✅ Automatic macro calculation

---

**Created**: November 13, 2025
**Status**: Backend code complete, ready to deploy
**Next**: Deploy to platform → Configure Omi app → Test
