# 🚀 Scalable Food Tracker Architecture

**Built For**: Vedanth's Omi Device → Google Sheets
**Cost**: $0/month (uses existing subscriptions)
**Latency**: 2-3 seconds real-time
**Scalability**: Handles 1000+ meals/month

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     YOUR PHONE (Omi Device)                  │
│  You: "I had a large chicken shawarma with extra sauce"    │
└─────────────────────────────────────────────────────────────┘
                            ↓ (2 seconds)
┌─────────────────────────────────────────────────────────────┐
│              OMI CLOUD (Real-time Processing)                │
│  • Transcribes audio                                         │
│  • Identifies speaker (Vedanth)                              │
│  • Triggers webhook → YOUR ENDPOINT                          │
└─────────────────────────────────────────────────────────────┘
                            ↓ (instant)
┌─────────────────────────────────────────────────────────────┐
│         WEBHOOK ENDPOINT (Railway/Render - Cloud)            │
│  FastAPI server receives:                                    │
│  {                                                           │
│    "transcript": "I had large chicken shawarma...",         │
│    "speaker": "Vedanth",                                     │
│    "timestamp": "2025-11-12T13:30:00Z"                      │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓ (instant)
┌─────────────────────────────────────────────────────────────┐
│         FOOD DETECTION (Python - Pattern Matching)           │
│  Keywords: "ate", "had", "eating", "lunch", "breakfast"     │
│  Extract: "large chicken shawarma with extra sauce"         │
└─────────────────────────────────────────────────────────────┘
                            ↓ (if food detected)
┌─────────────────────────────────────────────────────────────┐
│      CLAUDE DESKTOP (via MCP - Full AI Analysis)             │
│  Prompt: "Analyze this food for Vedanth (54.9kg, goal 60kg) │
│  Food: large chicken shawarma with extra sauce"             │
│                                                              │
│  Claude Returns:                                             │
│  {                                                           │
│    "food": "Chicken Shawarma",                              │
│    "portion": "Large (1.5x) + extra sauce",                 │
│    "calories": 1075,                                         │
│    "protein_g": 67,                                          │
│    "carbs_g": 78,                                            │
│    "fat_g": 38,                                              │
│    "fiber_g": 4,                                             │
│    "micronutrients": {...},                                  │
│    "meal_timing": "lunch",                                   │
│    "recommendation": "Excellent protein! Add veggies..."     │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
                            ↓ (1 second)
┌─────────────────────────────────────────────────────────────┐
│       GOOGLE SHEETS API (Direct Write)                       │
│  Appends row to "Meals" tab:                                │
│  | Date | Time | Food | Portion | Cal | Pro | Carb | Fat...│
│  |11/12|13:30|Shawarma|Large+sauce|1075|67|78|38|...        │
└─────────────────────────────────────────────────────────────┘
                            ↓ (instant)
┌─────────────────────────────────────────────────────────────┐
│              POKE NOTIFICATION (To Your Phone)               │
│  "✅ Meal logged!                                           │
│   🍗 Chicken Shawarma (Large)                               │
│   📊 1,075 cal | 67g protein                                │
│   🎯 1,725 cal remaining today"                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                YOU CHECK (Google Sheets App)                 │
│  All meals visible instantly                                │
│  Daily totals auto-calculated                               │
│  Weekly trends in charts                                     │
└─────────────────────────────────────────────────────────────┘
```

**Total Latency**: 2-4 seconds from speaking to notification!

---

## System Components

### 1. Omi Device (Already Have)
**Role**: Voice capture and transcription
- Captures: Everything you say about food
- Transcribes: Audio → Text in real-time
- Triggers: Webhook when food keywords detected
- **Cost**: Existing subscription

### 2. Webhook Endpoint (Cloud Deployment)
**Role**: Receive and route data
**Technology**: FastAPI (Python)
**Hosting**: Railway or Render (free tier)
**Functions**:
- Receives POST requests from Omi
- Validates webhook signature
- Detects food mentions
- Triggers Claude Desktop analysis
- Writes to Google Sheets
- Sends Poke notifications

**Code Structure**:
```python
from fastapi import FastAPI, Request
import anthropic  # Claude API
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests  # For Poke

app = FastAPI()

@app.post("/omi-webhook")
async def handle_omi_transcript(request: Request):
    # 1. Receive transcript
    data = await request.json()
    transcript = data['transcript']

    # 2. Detect food mention
    if not is_food_mention(transcript):
        return {"status": "ignored"}

    # 3. Analyze with Claude Desktop (via MCP or API)
    analysis = analyze_food_with_claude(transcript)

    # 4. Write to Google Sheets
    append_to_sheets(analysis)

    # 5. Send Poke notification
    send_poke_notification(analysis)

    return {"status": "success", "food": analysis['food']}
```

### 3. Claude Desktop Integration
**Role**: AI-powered food analysis
**Method**: Two approaches (you choose):

**Option A: Via Claude API** (Recommended for webhooks)
```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

def analyze_food_with_claude(transcript):
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Analyze this food for Vedanth:

User Context:
- Current: 54.9kg, Goal: 60kg (bulking)
- Daily: 2,800 cal, 120g protein
- Activity: Gym 6x/week

Food mention: "{transcript}"

Return JSON with:
- food_name
- portion_estimate
- calories, protein_g, carbs_g, fat_g, fiber_g
- micronutrients (iron, calcium, vitamins)
- meal_timing
- recommendation for bulk goals"""
        }]
    )
    return json.loads(response.content[0].text)
```

**Option B: Via Claude Desktop MCP** (No API key needed)
```python
import subprocess

def analyze_food_with_claude(transcript):
    prompt = f"Analyze food: {transcript} for Vedanth (54.9kg→60kg bulk)"
    result = subprocess.run(
        ['claude', '--prompt', prompt],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)
```

### 4. Google Sheets Integration
**Role**: Database storage
**Method**: Google Sheets API v4

**Sheet Structure**:

**Tab 1: "Meals"** (Main log)
| Date | Time | Food | Portion | Calories | Protein | Carbs | Fat | Fiber | Iron | Calcium | Notes |
|------|------|------|---------|----------|---------|-------|-----|-------|------|---------|-------|
| 2025-11-12 | 13:30 | Chicken Shawarma | Large + extra sauce | 1075 | 67 | 78 | 38 | 4 | 4.5 | 150 | Excellent protein! |

**Tab 2: "Daily Summary"** (Auto-calculated)
| Date | Total Cal | Total Protein | Goal Cal | Goal Protein | Remaining Cal | Status |
|------|-----------|---------------|----------|--------------|---------------|--------|
| 2025-11-12 | 2650 | 118 | 2800 | 120 | 150 | On Track ✅ |

**Tab 3: "Weekly Trends"** (Charts)
- Line chart: Calories per day
- Bar chart: Protein per day
- Pie chart: Macro breakdown

**Code**:
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_file(
    '/home/ved/.config/google-credentials.json',
    scopes=SCOPES
)
service = build('sheets', 'v4', credentials=credentials)

def append_to_sheets(analysis):
    sheet_id = os.getenv('HEALTH_SHEET_ID')

    values = [[
        datetime.now().strftime('%Y-%m-%d'),
        datetime.now().strftime('%H:%M:%S'),
        analysis['food_name'],
        analysis['portion_estimate'],
        analysis['calories'],
        analysis['protein_g'],
        analysis['carbs_g'],
        analysis['fat_g'],
        analysis['fiber_g'],
        analysis['micronutrients'].get('iron_mg', 0),
        analysis['micronutrients'].get('calcium_mg', 0),
        analysis['recommendation']
    ]]

    body = {'values': values}

    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range='Meals!A:L',
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
```

### 5. Poke Notification System
**Role**: Instant feedback to phone
**API**: Poke API (you already have key)

**Code**:
```python
import requests

POKE_API_KEY = 'pk_GH6UrWQ1JCpPzmsYTAX0LzNfGKn_TTQDquPUpAOujWM'

def send_poke_notification(analysis):
    # Calculate daily progress
    daily_total = get_todays_total_from_sheets()
    remaining_cal = 2800 - daily_total['calories']
    remaining_protein = 120 - daily_total['protein']

    message = f"""✅ Meal logged!

🍽️ {analysis['food_name']} ({analysis['portion_estimate']})
📊 {analysis['calories']} cal | {analysis['protein_g']}g protein

Today's Progress:
🎯 {remaining_cal} cal remaining
💪 {remaining_protein}g protein remaining

{analysis['recommendation']}
"""

    requests.post(
        'https://api.poke.com/v1/notify',  # Check actual Poke API endpoint
        headers={'Authorization': f'Bearer {POKE_API_KEY}'},
        json={
            'title': 'Food Logged!',
            'message': message,
            'priority': 'normal'
        }
    )
```

---

## Deployment Strategy

### Phase 1: Local Testing (This Week)
1. Build webhook endpoint locally
2. Test with ngrok tunnel
3. Configure Omi webhook to ngrok URL
4. Verify end-to-end flow

### Phase 2: Cloud Deployment (Next Week)
**Option A: Railway (Recommended)**
- Free tier: 500 hours/month (plenty for this)
- One-click deploy from GitHub
- Automatic HTTPS
- Environment variables support

**Option B: Render**
- Free tier: Always on
- Auto-deploy from GitHub
- Custom domains
- Built-in monitoring

### Phase 3: Production Monitoring
- Health checks every 5 minutes
- Error logging to file
- Daily summary email
- Uptime monitoring

---

## Scalability Features

### 1. Rate Limiting
```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.post("/omi-webhook")
@limiter.limit("100/minute")  # Prevent abuse
async def handle_omi_transcript(request: Request):
    ...
```

### 2. Async Processing
```python
import asyncio

async def process_food_mention(transcript):
    # Run analysis and sheet writing in parallel
    analysis_task = analyze_food_with_claude(transcript)
    sheets_task = append_to_sheets(analysis)

    await asyncio.gather(analysis_task, sheets_task)
```

### 3. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_nutrition_data(food_name):
    # Cache frequent foods
    return database_lookup(food_name)
```

### 4. Duplicate Prevention
```python
import hashlib

processed_transcripts = set()

def is_duplicate(transcript):
    hash_val = hashlib.md5(transcript.encode()).hexdigest()
    if hash_val in processed_transcripts:
        return True
    processed_transcripts.add(hash_val)
    return False
```

### 5. Error Recovery
```python
import logging

logger = logging.getLogger(__name__)

@app.post("/omi-webhook")
async def handle_omi_transcript(request: Request):
    try:
        # Process transcript
        ...
    except Exception as e:
        logger.error(f"Error processing transcript: {e}")
        # Save to retry queue
        save_to_retry_queue(transcript)
        return {"status": "error", "message": str(e)}
```

---

## Google Sheets Schema Design

### Sheet Structure (Optimized for Scale)

**Tab 1: Meals (Main Log)**
```
| A: Date | B: Time | C: Food | D: Portion | E: Calories | F: Protein | G: Carbs | H: Fat | I: Fiber | J: Iron | K: Calcium | L: Notes | M: Source | N: ID |
```

**Tab 2: Daily Summary (Auto-Calculated)**
```
Formula in B2: =SUMIFS(Meals!E:E, Meals!A:A, A2)  # Total calories
Formula in C2: =SUMIFS(Meals!F:F, Meals!A:A, A2)  # Total protein
```

**Tab 3: Foods Database (Reference)**
```
| Food Name | Avg Calories | Avg Protein | Common Portions |
| Chicken Shawarma | 650 | 45 | Regular, Large |
| Dal | 115 | 9 | Bowl, Cup |
```

**Tab 4: Weekly Charts**
- Pivot table from Meals tab
- Auto-refreshing charts

---

## Cost Analysis

| Component | Service | Cost |
|-----------|---------|------|
| Omi Device | Existing subscription | $0 |
| Claude Desktop | Existing subscription | $0 |
| Google Sheets | Free (100 requests/100sec) | $0 |
| Poke | Existing subscription | $0 |
| Railway/Render | Free tier (500hrs/month) | $0 |
| **TOTAL** | | **$0/month** |

**At scale** (1000+ meals/month):
- Google Sheets: Still free (within quotas)
- Railway: May need $5/month plan
- **Max cost**: $5/month

---

## Performance Targets

| Metric | Target | Current (Estimated) |
|--------|--------|---------------------|
| Webhook latency | <500ms | ~200ms |
| Claude analysis | <3 seconds | ~2 seconds |
| Sheets write | <1 second | ~500ms |
| Poke notification | <500ms | ~300ms |
| **Total end-to-end** | **<5 seconds** | **~3 seconds** |
| Uptime | 99.5% | TBD |
| Concurrent meals | 10/sec | Unlimited |

---

## Security

### 1. Webhook Signature Verification
```python
import hmac

def verify_omi_signature(request):
    signature = request.headers.get('X-Omi-Signature')
    payload = await request.body()

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        'sha256'
    ).hexdigest()

    return hmac.compare_digest(signature, expected)
```

### 2. Environment Variables
```bash
# .env file (never commit!)
OMI_API_KEY=omi_dev_2b7983a707b5ede131a0903a1655d918
POKE_API_KEY=pk_GH6UrWQ1JCpPzmsYTAX0LzNfGKn_TTQDquPUpAOujWM
HEALTH_SHEET_ID=your_sheet_id
CLAUDE_API_KEY=sk-ant-...  # If using API
WEBHOOK_SECRET=random_secret_string
```

### 3. Rate Limiting
- 100 requests/minute per IP
- 1000 requests/hour per user

### 4. Input Validation
```python
from pydantic import BaseModel

class OmiWebhookPayload(BaseModel):
    transcript: str
    speaker: str
    timestamp: str

    @validator('transcript')
    def transcript_not_empty(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Transcript too short')
        return v
```

---

## Monitoring & Alerts

### 1. Health Check Endpoint
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "sheets": check_sheets_connection(),
            "claude": check_claude_connection(),
            "poke": check_poke_connection()
        }
    }
```

### 2. Error Tracking
- Log all errors to file
- Send critical errors to Poke
- Daily summary of processed meals

### 3. Metrics Dashboard
- Total meals logged
- Average processing time
- Success/error rate
- Daily calorie trends

---

## Next Steps

1. **Create webhook endpoint code** (30 minutes)
2. **Set up Google Sheets structure** (10 minutes)
3. **Test locally with ngrok** (20 minutes)
4. **Deploy to Railway** (15 minutes)
5. **Configure Omi webhook** (5 minutes)
6. **Test end-to-end** (10 minutes)

**Total setup time**: ~90 minutes

---

## Should I Build This Now?

I can create:
1. ✅ Complete webhook endpoint (FastAPI)
2. ✅ Google Sheets integration code
3. ✅ Poke notification system
4. ✅ Claude Desktop integration
5. ✅ Deployment scripts
6. ✅ Setup guide

**Timeline**: 2-3 hours to build, test locally
**Your effort**: Just configure Omi webhook URL

Ready to start building? 🚀
