# 🎙️ Omi VedStack - Real-Time Chat Approach (No Memories)

**Date**: November 13, 2025
**Philosophy**: Don't pollute memories with food logs. Use real-time chat processing instead.

---

## 🧠 WHY NOT MEMORIES?

**Problem with Memory-Based Approach:**
- ❌ Every meal = new memory in Omi
- ❌ 3 meals/day × 56 days = 168 food memories
- ❌ Clutters your memory base
- ❌ Mixes food logs with actual important memories
- ❌ Hard to find real memories later

**Better Approach: Real-Time Chat Processing**
- ✅ Catch food mentions in real-time
- ✅ Log to Airtable immediately
- ✅ NO memory created
- ✅ Clean separation: Food data in Airtable, real memories in Omi
- ✅ Omi stays focused on meaningful conversations

---

## 🏗️ NEW ARCHITECTURE

### Flow:

```
You talk to Omi: "I'm eating 3 rotis with dal"
         ↓
Omi transcribes in REAL-TIME
         ↓
Webhook fires immediately (every few seconds)
         ↓
Your backend receives transcript segment
         ↓
Detect food keyword: "eating", "ate", "having"
         ↓
Extract food items: "3 rotis", "dal"
         ↓
Query Macro Calculation Rules (Airtable)
         ↓
Write to Food Log (Airtable)
         ↓
Optional: Omi responds "Logged: 838 cal, 48g protein"
```

**Key difference**: This happens DURING conversation, not after. No memory created.

---

## 🎯 OMI APP CONFIGURATION

### App Type: **Real-Time Transcript Processor**

**Setup in Omi mobile app:**

1. **Name**: VedStack Food Logger
2. **Description**: Real-time food tracking for aggressive bulk
3. **Type**: Integration → Real-Time Transcript Processor
4. **Webhook URL**: `https://your-backend.com/omi/transcript`
5. **Capabilities**:
   - ✅ Real-time transcript processing
   - ❌ Memory creation (DISABLED)

### Optional Chat Prompt (For Omi responses):

```
You are Vedanth's nutrition tracking assistant for his 8-week bulk.

When Vedanth mentions food:
1. Acknowledge: "Logged"
2. Tell him macros: "That's ~838 cal, 48g protein"
3. Tell him progress: "You're at 2,100 cal today (70% of 3,000 target)"

Keep responses SHORT (1 sentence max).

Do NOT create memories for food logs.
```

---

## 📡 WEBHOOK DATA STRUCTURE

### What Omi sends to your backend:

```json
POST https://your-backend.com/omi/transcript?uid=vedanth123&session_id=abc
Content-Type: application/json

{
  "session_id": "abc123",
  "segments": [
    {
      "text": "I'm eating three rotis",
      "speaker": "SPEAKER_00",
      "speakerId": 0,
      "is_user": true,
      "start": 0.5,
      "end": 2.3
    },
    {
      "text": "with dal and paneer bhurji",
      "speaker": "SPEAKER_00",
      "speakerId": 0,
      "is_user": true,
      "start": 2.5,
      "end": 4.8
    }
  ]
}
```

**Key points:**
- Fired EVERY FEW SECONDS during conversation
- `session_id`: Identifies the conversation
- `segments`: Array of recent transcript chunks
- Real-time: No waiting for memory creation

---

## 🔥 BACKEND LOGIC (Smart Processing)

### Challenge: Don't log duplicates

**Problem**: Omi sends overlapping segments
- First webhook: "I'm eating three rotis"
- Second webhook: "I'm eating three rotis with dal"
- Third webhook: "I'm eating three rotis with dal and paneer"

**Solution: Session-based deduplication**

```python
from fastapi import FastAPI, Request
import airtable
from datetime import datetime, timedelta

app = FastAPI()

# In-memory session tracking
active_sessions = {}

@app.post("/omi/transcript")
async def handle_transcript(request: Request):
    data = await request.json()
    uid = request.query_params.get("uid")
    session_id = data.get("session_id")
    segments = data.get("segments", [])

    # Combine all text
    full_text = " ".join([seg["text"] for seg in segments if seg.get("is_user")])

    # Check if this is food-related
    if not is_food_mention(full_text):
        return {"status": "ignored", "reason": "not food related"}

    # Deduplication: Has this session already logged?
    if session_id in active_sessions:
        last_logged = active_sessions[session_id]["last_logged"]
        if (datetime.now() - last_logged).seconds < 60:
            # Already logged in last 60 seconds, ignore
            return {"status": "skipped", "reason": "recently logged"}

    # Extract food items
    food_items = extract_food_items(full_text)

    if not food_items:
        return {"status": "ignored", "reason": "no food items found"}

    # Calculate macros
    macros = calculate_macros(food_items)

    # Write to Airtable
    log_entry = create_food_log(uid, full_text, macros)

    # Track session to prevent duplicates
    active_sessions[session_id] = {
        "last_logged": datetime.now(),
        "log_id": log_entry["id"]
    }

    # Return response (Omi can speak this back)
    return {
        "status": "logged",
        "message": f"Logged: {macros['calories']} cal, {macros['protein']}g protein. You're at {get_daily_total(uid)} cal today.",
        "macros": macros
    }

def is_food_mention(text: str) -> bool:
    """Check if text mentions food"""
    keywords = [
        "eating", "ate", "having", "had",
        "breakfast", "lunch", "dinner", "snack",
        "roti", "dal", "rice", "paneer", "egg",
        "food", "meal"
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in keywords)

def extract_food_items(text: str) -> list:
    """Extract food items from text

    Example: "I'm eating 3 rotis with dal and paneer"
    Returns: ["3 rotis", "dal", "paneer"]
    """
    # Option 1: Simple regex/NLP
    # Option 2: Use Claude API for smarter extraction

    # For now, simple approach:
    import re

    # Match patterns like "3 rotis", "one dal", etc.
    pattern = r'(\d+|one|two|three|four|five)\s+(\w+)'
    matches = re.findall(pattern, text.lower())

    items = []
    for quantity, food in matches:
        # Convert word numbers to digits
        quantity_map = {"one": "1", "two": "2", "three": "3",
                       "four": "4", "five": "5"}
        qty = quantity_map.get(quantity, quantity)
        items.append(f"{qty} {food}")

    # Also catch foods without quantities
    known_foods = ["dal", "paneer", "curd", "dahi", "rice",
                   "sabzi", "vegetables", "chicken", "egg"]
    for food in known_foods:
        if food in text.lower() and not any(food in item for item in items):
            items.append(f"1 {food}")

    return items

def calculate_macros(food_items: list) -> dict:
    """Query Airtable Macro Calculation Rules and calculate totals"""
    # Query Airtable for each food item
    # Match to reference data
    # Sum up macros

    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    for item in food_items:
        # Query Macro Calculation Rules table
        # Match food name, multiply by quantity
        # Add to totals
        pass

    return {
        "calories": total_calories,
        "protein": total_protein,
        "carbs": total_carbs,
        "fat": total_fat
    }

def create_food_log(uid: str, description: str, macros: dict) -> dict:
    """Write to Airtable Food Log"""
    AIRTABLE_PAT = "pat2KeRGsd2jGmNop..."
    BASE_ID = "appSgD8XmiKRBrGXd"

    data = {
        "Date": datetime.now().isoformat(),
        "Food Description": description,
        "Calories": macros["calories"],
        "Protein": macros["protein"],
        "Carbs": macros["carbs"],
        "Fat": macros["fat"],
        "Meal Type": infer_meal_type(),  # Based on time of day
        "Source": "Omi Voice (Real-time)"
    }

    # POST to Airtable
    # Return created record
    return {"id": "recXXX"}

def get_daily_total(uid: str) -> int:
    """Get today's total calories from Airtable"""
    # Query Food Log for today
    # SUM calories
    return 2100  # Example

def infer_meal_type() -> str:
    """Infer meal type based on time of day"""
    hour = datetime.now().hour

    if 6 <= hour < 11:
        return "Breakfast"
    elif 11 <= hour < 16:
        return "Lunch"
    elif 16 <= hour < 19:
        return "Snack"
    else:
        return "Dinner"
```

---

## 🎯 USER EXPERIENCE

### Scenario 1: Quick Meal Mention

**You (while eating):** "I'm having 3 rotis with dal"

**Omi (immediately):** "Logged: 443 calories, 27g protein. You're at 2,100 cal today."

**What happened:**
1. Omi transcribed in real-time
2. Webhook fired to backend
3. Backend detected food keywords
4. Extracted: "3 rotis", "dal"
5. Looked up macros in Airtable
6. Wrote to Food Log
7. Returned response to Omi
8. Omi spoke response back

**Memory created?** NO ✅

---

### Scenario 2: Detailed Description

**You:** "Just finished lunch. I had 3 jowar-wheat rotis, one katori of dal, paneer bhurji, mixed vegetables, and curd."

**Omi:** "Logged lunch: 838 calories, 48g protein. You're at 2,900 cal today, 100 cal away from target."

**Memory created?** NO ✅

---

### Scenario 3: Correction

**You:** "Wait, I had 4 rotis, not 3"

**Backend logic:**
- Detects correction keyword: "wait", "actually", "correction"
- Finds last log from this session
- Updates the entry in Airtable
- Adjusts macros

**Omi:** "Updated: 4 rotis. New total: 909 calories."

---

### Scenario 4: Normal Conversation (Not Food)

**You:** "How's the weather today?"

**Backend:**
- Receives transcript
- Checks: is_food_mention() = False
- Returns: {"status": "ignored"}
- Does NOT write to Airtable

**Omi:** [Responds normally about weather]

**Memory created?** Maybe (if Omi thinks it's important), but NOT by VedStack app

---

## 🔧 SESSION MANAGEMENT

### Why Sessions Matter:

Omi sends MANY webhooks during a single conversation:
- T+0s: "I'm eating"
- T+2s: "I'm eating three"
- T+4s: "I'm eating three rotis"
- T+6s: "I'm eating three rotis with"
- T+8s: "I'm eating three rotis with dal"

**We only want to log ONCE.**

### Deduplication Strategy:

**Option 1: Time-based (Simple)**
```python
# If logged in last 60 seconds, ignore
if (now - last_logged) < 60:
    return "skipped"
```

**Option 2: Content-based (Smarter)**
```python
# If food items haven't changed, ignore
if current_foods == previous_foods:
    return "skipped"
```

**Option 3: Confidence-based (Smartest)**
```python
# Wait until transcript stabilizes
if len(segments) < 5:  # Still building up
    return "waiting"

# Check if food description is complete
if text.endswith(("and", "with")):  # Incomplete
    return "waiting"

# Now log
```

---

## 💬 OMI RESPONSE INTEGRATION

### Backend Returns Response → Omi Speaks It

**Backend response format:**
```json
{
  "status": "logged",
  "message": "Logged: 838 cal, 48g protein. You're at 2,900 cal today.",
  "data": {
    "calories": 838,
    "protein": 48,
    "daily_total": 2900,
    "target": 3000,
    "remaining": 100
  }
}
```

**Omi speaks:** "Logged: 838 cal, 48g protein. You're at 2,900 cal today."

**This gives you instant feedback WITHOUT creating a memory.**

---

## 🆚 MEMORY APPROACH vs REAL-TIME APPROACH

### Memory Creation Trigger:

| Aspect | Rating | Notes |
|--------|--------|-------|
| Speed | ⚠️ Slow | Waits for conversation to end |
| Accuracy | ✅ Good | Full context available |
| Memory Pollution | ❌ Bad | 168 food memories over 8 weeks |
| Complexity | ✅ Easy | Omi does extraction |

### Real-Time Transcript Processor:

| Aspect | Rating | Notes |
|--------|--------|-------|
| Speed | ✅ Fast | Logs during conversation |
| Accuracy | ⚠️ Good | Need smart deduplication |
| Memory Pollution | ✅ None | NO memories created |
| Complexity | ⚠️ Moderate | Need session management |

**Winner: Real-Time Approach** ✅

---

## 📋 IMPLEMENTATION CHECKLIST

### Week 1: Local Backend Setup
- [ ] Set up FastAPI backend locally
- [ ] Create `/omi/transcript` endpoint
- [ ] Implement `is_food_mention()` function
- [ ] Test with mock data

### Week 2: Food Extraction
- [ ] Implement `extract_food_items()` (regex-based)
- [ ] Query Airtable Macro Calculation Rules
- [ ] Implement `calculate_macros()`
- [ ] Test with sample transcripts

### Week 3: Airtable Integration
- [ ] Connect to Airtable with PAT
- [ ] Implement `create_food_log()`
- [ ] Test writing to Food Log table
- [ ] Verify data shows up correctly

### Week 4: Session Management
- [ ] Implement session tracking (in-memory dict)
- [ ] Add deduplication logic
- [ ] Test with overlapping transcripts
- [ ] Handle edge cases (corrections, etc.)

### Week 5: Deploy & Test
- [ ] Deploy to Railway/Vercel/Fly.io
- [ ] Get public webhook URL
- [ ] Create Omi Real-Time Processor app
- [ ] Add webhook URL to Omi app
- [ ] Test end-to-end: Voice → Airtable

### Week 6: Polish & Optimize
- [ ] Add Claude API for smarter extraction (optional)
- [ ] Implement meal type inference
- [ ] Add daily total calculation
- [ ] Test Omi response integration
- [ ] Add error handling and logging

---

## 🎯 MINIMAL VIABLE PRODUCT (MVP)

**What you need for MVP:**

1. **Backend endpoint** that:
   - Receives transcript webhook
   - Detects food keywords
   - Extracts food items (simple regex)
   - Writes to Airtable

2. **Omi app** configured as:
   - Real-Time Transcript Processor
   - Webhook URL: Your backend
   - NO memory creation

**That's it.** No Claude API needed initially. No complex NLP. Just:
- Voice → Transcript → Keyword match → Log to Airtable

---

## 🚀 EXAMPLE BACKEND (Minimal)

```python
from fastapi import FastAPI, Request
import httpx
import re
from datetime import datetime

app = FastAPI()

AIRTABLE_PAT = "pat2KeRGsd2jGmNop..."
AIRTABLE_BASE = "appSgD8XmiKRBrGXd"

# Simple in-memory deduplication
last_logged = {}

@app.post("/omi/transcript")
async def handle_transcript(request: Request):
    data = await request.json()
    session_id = data.get("session_id")
    segments = data.get("segments", [])

    # Combine text
    text = " ".join([s["text"] for s in segments if s.get("is_user")])

    # Check for food keywords
    if not any(k in text.lower() for k in ["eating", "ate", "roti", "dal"]):
        return {"status": "ignored"}

    # Deduplication
    if session_id in last_logged:
        if (datetime.now() - last_logged[session_id]).seconds < 60:
            return {"status": "duplicate"}

    # Simple extraction (just count rotis/dal mentions)
    rotis = len(re.findall(r'\d+\s+roti', text, re.I))
    has_dal = "dal" in text.lower()

    calories = (rotis * 71) + (230 if has_dal else 0)
    protein = (rotis * 3) + (18 if has_dal else 0)

    # Write to Airtable
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.airtable.com/v0/{AIRTABLE_BASE}/Food%20Log",
            headers={"Authorization": f"Bearer {AIRTABLE_PAT}",
                    "Content-Type": "application/json"},
            json={"records": [{
                "fields": {
                    "Date": datetime.now().isoformat(),
                    "Food Description": text,
                    "Calories": calories,
                    "Protein": protein,
                    "Meal Type": "Lunch",
                    "Source": "Omi Voice"
                }
            }]}
        )

    last_logged[session_id] = datetime.now()

    return {
        "status": "logged",
        "message": f"Logged: {calories} cal, {protein}g protein"
    }

# Health check
@app.get("/")
async def root():
    return {"status": "VedStack Omi backend running"}
```

**That's 60 lines.** You can deploy this TODAY and have basic voice logging working.

---

## 🎉 FINAL COMPARISON

### Before (Photo Logging):
```
1. Take photo (10s)
2. Upload to Claude Desktop (5s)
3. Say "Log this" (2s)
4. Wait for analysis (5s)
Total: 22 seconds
```

### After (Voice Logging - No Memories):
```
1. Say "I'm eating 3 rotis with dal" (3s)
2. Auto-logged in background (instant)
Total: 3 seconds

PLUS: No memory pollution ✅
```

**7x faster + cleaner memory base.**

---

## 💪 YOUR CALL

**Memory-based approach:**
- ❌ 168 food memories clutter Omi
- ✅ More accurate (full context)
- ⏳ Slower (waits for memory creation)

**Real-time approach:**
- ✅ NO memory pollution
- ✅ Instant logging (during conversation)
- ⚠️ Slightly more complex backend

**Which do you prefer?**

Or do you want a **hybrid**: Real-time for simple meals ("3 rotis"), memory-based only for complex meals ("Can you help me log this meal properly")?

---

**Created**: November 13, 2025
**Philosophy**: Keep memories for memories, data for databases
**Status**: Ready to implement
