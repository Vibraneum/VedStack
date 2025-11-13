# 🎙️ Omi + VedStack Integration Plan

**Date**: November 13, 2025
**Goal**: Voice-based food logging: "I just ate 3 rotis with dal" → Auto-logged to Airtable

---

## 🧠 SYSTEM ARCHITECTURE

### Current Setup (What Works):

```
Photo → Claude Desktop → Airtable Food Log
```

**Flow:**
1. You take food photo
2. Upload to Claude Desktop
3. Claude reads User Profile, Macro Rules, Goals
4. Claude analyzes photo, calculates macros
5. Claude writes to Airtable via MCP

### Target Setup (With Omi):

```
Voice → Omi → Webhook → Backend → Airtable Food Log
              ↓
         Supermemory (Knowledge Base)
```

**Flow:**
1. You say: "I just ate 3 rotis, dal, and paneer bhurji"
2. Omi transcribes and creates memory
3. Omi triggers webhook to your backend
4. Backend processes with Claude API OR direct logic
5. Backend writes to Airtable
6. Backend writes to Supermemory for context

---

## 🎯 THREE INTEGRATION APPROACHES

### Option A: Memory Creation Trigger (RECOMMENDED)

**Best for**: Post-meal logging (after you finish eating)

**Omi App Type**: Memory Creation Trigger
**Trigger**: When Omi creates a memory containing food-related content

**Flow:**
```
You: "I just ate 3 jowar rotis, one katori of dal,
      and paneer bhurji for lunch"

Omi: [Creates memory after conversation ends]
     ↓
Webhook POST to your backend:
{
  "transcript": [...],
  "structured": {
    "title": "Lunch - Rotis, Dal, Paneer",
    "overview": "Vedanth logged his lunch...",
    "action_items": ["Log meal to VedStack"]
  }
}
     ↓
Backend:
1. Extract food items (3 rotis, dal, paneer bhurji)
2. Look up Macro Calculation Rules in Airtable
3. Calculate macros:
   - 3 rotis: 213 cal, 9g protein, 45g carbs
   - Dal 1 katori: 230 cal, 18g protein, 40g carbs
   - Paneer bhurji: ~200 cal, 15g protein, 20g fat
4. Write to Airtable Food Log
5. Write context to Supermemory
     ↓
Result: Meal logged automatically
```

**Pros:**
- ✅ Natural conversation (just talk normally)
- ✅ Works after meal (accurate description)
- ✅ Omi processes and structures data
- ✅ Can handle complex meals ("I had X, Y, and Z")

**Cons:**
- ⏳ Slight delay (after Omi creates memory)
- ⚠️ Requires backend server

---

### Option B: Real-Time Transcript Processor

**Best for**: Live logging during meal

**Omi App Type**: Real-Time Transcript Processor
**Trigger**: When you say specific keywords ("I'm eating", "just ate", "food")

**Flow:**
```
You: "I'm eating 3 rotis with dal"
     ↓
Omi: [Real-time transcript sent immediately]
Webhook POST:
{
  "session_id": "abc123",
  "segments": [
    {
      "text": "I'm eating 3 rotis with dal",
      "speaker": "SPEAKER_00",
      "start": 0, "end": 3
    }
  ]
}
     ↓
Backend:
1. Detect food keyword ("eating", "ate")
2. Extract food items
3. Look up macros
4. Write to Airtable
     ↓
Result: Instant logging
```

**Pros:**
- ✅ INSTANT logging (real-time)
- ✅ No waiting for memory creation
- ✅ Can remind you: "Did you log that meal?"

**Cons:**
- ⚠️ More complex (need session management)
- ⚠️ Might trigger on non-food conversations
- ⚠️ Need smart logic to avoid duplicates

---

### Option C: Hybrid (Memory Prompt + Integration)

**Best for**: Best of both worlds

**Omi App Type**: Memory Prompt + Memory Creation Trigger

**Memory Prompt:**
```
You are Vedanth's nutrition tracking assistant.

When Vedanth mentions eating food, extract:
1. Food items (name and quantity)
2. Meal type (breakfast/lunch/dinner/snack)
3. Approximate time

Format as:
MEAL: [food items]
TYPE: [meal type]
TIME: [time]

Examples:
- "I just had 3 rotis with dal for lunch"
  → MEAL: 3 rotis, 1 katori dal | TYPE: Lunch | TIME: now

- "This morning I ate upma and 3 eggs"
  → MEAL: upma (1 bowl), 3 boiled eggs | TYPE: Breakfast | TIME: morning
```

**Integration:**
When memory is created with food data → Webhook triggers → Backend logs to Airtable

**Pros:**
- ✅ Omi does extraction (you don't need NLP)
- ✅ Structured data in webhook payload
- ✅ Reliable and accurate

**Cons:**
- ⚠️ Still delayed (after memory creation)
- ⚠️ Requires backend

---

## 🏗️ BACKEND ARCHITECTURE

You'll need a simple backend server to receive Omi webhooks and write to Airtable.

### Tech Stack Options:

**Option 1: Python + FastAPI (RECOMMENDED)**
```python
from fastapi import FastAPI, Request
import airtable
import os

app = FastAPI()

AIRTABLE_PAT = "pat2KeRGsd2jGmNop..."
AIRTABLE_BASE = "appSgD8XmiKRBrGXd"

@app.post("/omi/memory-trigger")
async def handle_omi_memory(request: Request):
    data = await request.json()

    # Extract food info from transcript
    transcript = data.get("transcript", [])
    text = " ".join([seg["text"] for seg in transcript])

    # Parse food items (using Claude API or regex)
    food_items = extract_food_items(text)

    # Look up macros from Airtable Macro Calculation Rules
    macros = calculate_macros(food_items)

    # Write to Airtable Food Log
    create_food_log_entry(macros)

    # Write to Supermemory (optional)
    write_to_supermemory(text, macros)

    return {"status": "success", "logged": True}

def extract_food_items(text):
    # Use Claude API OR simple NLP
    # Example: "3 rotis, dal, paneer" → ["3 rotis", "1 dal", "paneer"]
    pass

def calculate_macros(food_items):
    # Query Airtable Macro Calculation Rules
    # Match food items to reference data
    # Return total macros
    pass

def create_food_log_entry(macros):
    # POST to Airtable Food Log
    pass
```

**Option 2: Node.js + Express**
**Option 3: Cloudflare Workers (serverless)**
**Option 4: Zapier/Make.com (no-code)**

---

## 🔑 WHAT YOU'LL NEED

### 1. Omi App Setup:
- Create app in Omi mobile app
- Choose type: Memory Creation Trigger OR Real-Time Processor
- Add webhook URL (your backend endpoint)
- Optional: Add memory prompt for extraction

### 2. Backend Server:
- Deploy FastAPI server (Vercel, Railway, Fly.io)
- Expose public webhook URL
- Environment variables:
  - `AIRTABLE_PAT`
  - `AIRTABLE_BASE_ID`
  - `CLAUDE_API_KEY` (for food extraction)

### 3. Airtable Access:
- Already have PAT ✅
- Already have Base ID ✅
- Already have Macro Calculation Rules ✅

### 4. Supermemory Integration (Optional):
- Supermemory API for storing meal context
- Benefits: Claude Desktop can query past meals

---

## 📱 COMPLETE DATA FLOW

### Scenario: You eat lunch

**Step 1: Voice Input**
```
You (to Omi): "I just finished lunch. I had 3 jowar-wheat rotis,
one katori of dal, paneer bhurji, mixed vegetables, and curd."
```

**Step 2: Omi Processing**
```
Omi: [Transcribes] → [Creates Memory]

Memory:
{
  "title": "Lunch - Rotis, Dal, Paneer, Vegetables",
  "transcript": [...],
  "structured": {
    "overview": "Vedanth logged his lunch consisting of rotis, dal, paneer bhurji, vegetables, and curd.",
    "category": "health",
    "action_items": ["Log meal to VedStack"]
  }
}
```

**Step 3: Webhook Trigger**
```
POST https://your-backend.com/omi/memory-trigger
{
  "uid": "vedanth_user_id",
  "session_id": "abc123",
  "transcript": [
    {"text": "I just finished lunch", ...},
    {"text": "I had 3 jowar-wheat rotis", ...},
    {"text": "one katori of dal", ...},
    {"text": "paneer bhurji", ...},
    {"text": "mixed vegetables", ...},
    {"text": "and curd", ...}
  ],
  "structured": {
    "title": "Lunch - Rotis, Dal, Paneer, Vegetables",
    "overview": "...",
    "action_items": ["Log meal to VedStack"]
  }
}
```

**Step 4: Backend Processing**
```python
# Extract food items
foods = [
  "3 jowar-wheat rotis",
  "1 katori dal",
  "paneer bhurji (estimated 70g)",
  "mixed vegetables (large bowl ~250ml)",
  "curd (small katori ~90ml)"
]

# Query Airtable Macro Calculation Rules
rotis_macros = query_airtable("Roti/Chapati") * 3  # 213 cal, 9g protein
dal_macros = query_airtable("Dal (cooked)")         # 230 cal, 18g protein
paneer_macros = estimate("Paneer", "70g")           # ~185 cal, 13g protein
veg_macros = query_airtable("Mixed Veg Sabzi")      # 150 cal, 5g protein
curd_macros = query_airtable("Curd/Dahi")           # 60 cal, 3.5g protein

# Total
total = {
  "calories": 838,
  "protein": 48.5,
  "carbs": 110,
  "fat": 23
}
```

**Step 5: Write to Airtable**
```python
airtable.create("Food Log", {
  "Date": "2025-11-13T13:00:00Z",
  "Food Description": "3 jowar-wheat rotis | 1 katori dal | Paneer bhurji ~70g | Mixed veg sabzi 250ml | Curd 90ml",
  "Calories": 838,
  "Protein": 48.5,
  "Carbs": 110,
  "Fat": 23,
  "Meal Type": "Lunch",
  "Source": "Omi Voice"
})
```

**Step 6: Write to Supermemory (Optional)**
```python
supermemory.store({
  "content": "Lunch on Nov 13: 3 rotis, dal, paneer, veggies, curd. 838 cal, 48.5g protein.",
  "metadata": {
    "type": "meal",
    "date": "2025-11-13",
    "meal_type": "lunch",
    "source": "omi"
  }
})
```

**Step 7: Confirmation (Optional)**
```
Omi (to you): "Logged lunch: 838 calories, 48.5g protein.
You're at 2,100 cal today (70% of target)."
```

---

## 🎯 RECOMMENDED IMPLEMENTATION

### Phase 1: Manual Testing (No Backend Yet)

**Setup:**
1. Create Omi Memory Prompt (extraction prompt above)
2. Test with voice: "I just ate X"
3. Check if Omi memory has structured food data
4. Manually copy to Airtable

**Goal**: Validate that Omi can extract food data accurately

---

### Phase 2: Backend + Webhook

**Setup:**
1. Deploy FastAPI backend (Vercel/Railway)
2. Create Omi Integration App (Memory Creation Trigger)
3. Add webhook URL to Omi app
4. Test: Voice → Omi → Webhook → Check logs

**Goal**: Verify webhook delivers data to your backend

---

### Phase 3: Airtable Integration

**Setup:**
1. Add Airtable logic to backend
2. Parse food items from transcript
3. Query Macro Calculation Rules
4. Write to Food Log

**Goal**: Full automation: Voice → Airtable

---

### Phase 4: Claude API Integration (Advanced)

**Setup:**
1. Add Claude API to backend
2. Use Claude to extract food items (more accurate than regex)
3. Claude can handle complex descriptions

**Example:**
```python
import anthropic

client = anthropic.Client(api_key="your_key")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{
        "role": "user",
        "content": f"""Extract food items and quantities from this transcript:

{transcript_text}

Refer to this macro database:
{macro_rules_from_airtable}

Return JSON:
{{
  "foods": [
    {{"item": "roti", "quantity": 3, "macros": {{...}}}},
    ...
  ],
  "total_macros": {{...}}
}}"""
    }]
)

# Parse response and write to Airtable
```

---

### Phase 5: Supermemory Integration (Optional)

**Setup:**
1. Write meals to Supermemory after logging
2. Claude Desktop can query: "What did I eat this week?"
3. Full context across voice, desktop, mobile

---

## 🆚 OMI APP vs CLAUDE DESKTOP

### Current (Claude Desktop):
- ✅ Visual analysis (photo recognition)
- ✅ Detailed portion estimation
- ✅ Direct MCP to Airtable
- ❌ Requires manual photo upload
- ❌ Not hands-free

### Future (Omi Integration):
- ✅ Hands-free (voice only)
- ✅ Faster (just speak)
- ✅ Works anywhere (no phone needed, just Omi device)
- ⚠️ Less accurate (no visual confirmation)
- ⚠️ Requires backend server

### Best Approach: BOTH

**Use Omi for:**
- Quick logging: "I'm eating 3 rotis"
- On-the-go meals
- When you forget to take photo

**Use Claude Desktop for:**
- Complex meals (photo shows everything)
- Accurate portion sizes
- New foods not in reference database

---

## 💰 COST ESTIMATE

### Backend Hosting:
- **Railway/Fly.io**: Free tier (500 hours/month)
- **Vercel**: Free tier (unlimited)
- **Cloudflare Workers**: Free tier (100k requests/day)

### Claude API:
- **Claude 3.5 Sonnet**: $3/million input tokens, $15/million output
- **Cost per meal**: ~$0.001 (1/10th of a cent)
- **Monthly (90 meals)**: ~$0.09

### Airtable:
- Already free (within limits)

### Omi:
- Device cost: One-time purchase
- No API costs (webhooks are free)

**Total Monthly**: ~$0-5 (basically free if using free hosting tiers)

---

## 📋 STEP-BY-STEP IMPLEMENTATION CHECKLIST

### Week 1: Setup & Testing
- [ ] Create Omi Memory Prompt for food extraction
- [ ] Test with voice: "I ate X" → Check Omi memory
- [ ] Verify structured data extraction

### Week 2: Backend Development
- [ ] Set up FastAPI backend locally
- [ ] Create `/omi/memory-trigger` webhook endpoint
- [ ] Test locally with ngrok tunnel
- [ ] Deploy to Railway/Vercel

### Week 3: Omi Integration
- [ ] Create Omi Integration App in mobile app
- [ ] Add webhook URL (your backend)
- [ ] Test: Voice → Webhook → Check backend logs
- [ ] Debug any issues

### Week 4: Airtable Connection
- [ ] Add Airtable SDK to backend
- [ ] Implement food extraction logic
- [ ] Query Macro Calculation Rules
- [ ] Write to Food Log table
- [ ] Test end-to-end: Voice → Airtable

### Week 5: Claude API Enhancement (Optional)
- [ ] Add Claude API for smarter extraction
- [ ] Handle complex meal descriptions
- [ ] Improve accuracy

### Week 6: Supermemory (Optional)
- [ ] Write meal context to Supermemory
- [ ] Test Claude Desktop queries: "What did I eat yesterday?"

---

## 🎉 END RESULT

**Before Omi Integration:**
```
1. Take photo of meal (10 seconds)
2. Upload to Claude Desktop (5 seconds)
3. Say "Log this" (2 seconds)
4. Wait for Claude to analyze (5 seconds)
5. Verify in Airtable (5 seconds)

Total: ~30 seconds per meal
```

**After Omi Integration:**
```
1. Say to Omi: "I just ate 3 rotis with dal" (3 seconds)
2. Omi processes and logs automatically (background)
3. Check Airtable later if needed

Total: ~3 seconds per meal (10x faster!)
```

**Plus:**
- Hands-free
- Works while eating
- No phone needed
- More natural

---

## 🚀 READY TO START?

**Next Steps:**
1. I can help you create the Omi Memory Prompt
2. I can help you build the FastAPI backend
3. I can help you deploy to Railway/Vercel
4. I can help you set up the Omi Integration App

**What do you want to tackle first?**

---

**Created**: November 13, 2025
**Status**: Design complete, ready for implementation
**Estimated Time**: 4-6 weeks for full integration
**Difficulty**: Moderate (requires backend development)
