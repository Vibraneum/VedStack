# 🔄 COMPLETE INTEGRATION: Claude → Sheets → Omi

**The perfect closed-loop system!**

---

## 🎯 The Vision

```
Photo → Claude Mobile → Google Sheets → Omi Knowledge Base
   ↓           ↓              ↓                ↓
Accuracy   Analysis      Central DB      Conversations
```

**Full cycle:**
1. **Photo → Claude** (accurate nutrition analysis)
2. **Claude → Sheets** (automatic logging via Zapier)
3. **Sheets → Omi** (knowledge base for discussions)
4. **Omi ↔ Sheets** (voice updates + queries)

---

## 🔧 Complete Setup (15 Minutes)

### Part 1: Claude Mobile → Google Sheets (Auto-logging)

**Use Zapier to connect Claude AI to Google Sheets**

#### Step 1: Create Zapier Account
1. Go to: https://zapier.com/sign-up
2. Free plan works! (100 tasks/month)

#### Step 2: Create Zap
1. **Trigger**: Claude AI → "New Message"
2. **Filter**: Only messages containing "FOOD:" or in project "Food Tracker"
3. **Action**: Google Sheets → "Create Spreadsheet Row"

#### Step 3: Configure Mapping
```
Zapier Field Mapping:
- Timestamp → {{zap_meta_human_now}}
- Food → Extract from Claude response
- Portion → Extract from Claude response
- Calories → Extract from Claude response (regex: \d+ cal)
- Protein (g) → Extract from Claude response (regex: \d+g protein)
- Carbs (g) → Extract from Claude response
- Fat (g) → Extract from Claude response
- Meal Type → Extract from message (breakfast/lunch/dinner/snack)
- Source → "Claude Vision"
- Confidence → "high"
```

#### Step 4: Set Up Claude Project
1. Create project: "Food Tracker"
2. Add custom instructions:

```
When user sends food photo:
1. Analyze portion sizes carefully
2. Return response in this EXACT format:

FOOD: [Food Name]
PORTION: [Size with units]
CALORIES: [number] cal
PROTEIN: [number]g protein
CARBS: [number]g carbs
FAT: [number]g fat
MEAL: [breakfast/lunch/dinner/snack]

Be specific about portions (use cups, grams, pieces).
Use Indian food knowledge for accurate estimates.
```

**Example response:**
```
FOOD: Chicken Biryani with Raita
PORTION: 2 cups biryani, 1/2 cup raita
CALORIES: 680 cal
PROTEIN: 38g protein
CARBS: 87g carbs
FAT: 19g fat
MEAL: lunch
```

---

### Part 2: Google Sheets → Omi Integration

**Sheets becomes the single source of truth**

#### Update dead-simple-health-coach.py

Add function to READ from Sheets (not just write):

```python
def get_todays_nutrition_from_sheets():
    """Get today's totals from Google Sheets"""
    meals_sheet = sheet.worksheet('Meals')

    today = datetime.now().strftime('%Y-%m-%d')
    all_rows = meals_sheet.get_all_values()

    total_calories = 0
    total_protein = 0

    for row in all_rows[1:]:  # Skip header
        if row[0].startswith(today):
            total_calories += int(row[3] or 0)
            total_protein += int(row[4] or 0)

    return {
        'calories': total_calories,
        'protein': total_protein,
        'target_calories': 3000,
        'target_protein': 130
    }
```

#### Update Omi Analysis to Include Context

When Omi asks "How's my nutrition today?", script:
1. Fetches current totals from Sheets
2. Sends to Claude Desktop with context
3. Claude responds with personalized advice

---

### Part 3: Omi Voice Commands

**What you can ask Omi:**

```
"How many calories have I eaten today?"
→ Script checks Sheets, Omi responds: "You've had 1,450 out of 3,000 calories"

"Am I hitting my protein goal?"
→ "You've had 62g out of 130g protein. Need 68g more."

"What did I eat for lunch?"
→ "Chicken biryani with raita - 680 calories, 38g protein"

"Should I have a protein shake?"
→ Checks totals, advises based on remaining targets

"Weekly progress?"
→ Analyzes 7 days of Sheets data, shows trends
```

---

## 📱 Your New Daily Workflow

### Logging Food (30 seconds):

**Option A: With Photo (Most Accurate)**
1. Take photo on phone
2. Open Claude mobile app
3. Send photo (no text needed - Project knows what to do)
4. ✅ Auto-logs to Sheets via Zapier
5. ✅ Available to Omi immediately

**Option B: Voice Only (Fastest)**
1. Tell Omi: "I had chicken biryani for lunch"
2. ✅ Auto-logs to Sheets

**Option C: Hybrid (Best of Both)**
1. Photo → Claude (get exact numbers)
2. Tell Omi: "Had lunch, 680 calories, 38g protein from Claude"
3. ✅ Logs with high confidence

---

### Checking Progress (Ask Omi):

```
"How am I doing today?"
→ Omi fetches from Sheets, responds with totals

"What should I eat for dinner?"
→ Omi sees you need 1,500 more cal, 68g protein
→ Suggests high-protein meal

"Weekly weight progress?"
→ Checks Body Metrics tab
→ Shows: 54.9kg → 55.3kg (+0.4kg this week)
```

---

## 🔄 Data Flow Diagram

```
┌─────────────┐
│ Claude      │ ← Photo + "lunch"
│ Mobile App  │
└──────┬──────┘
       │ (Zapier)
       ↓
┌─────────────────────────────────┐
│   GOOGLE SHEETS                 │
│   (Single Source of Truth)      │
│                                 │
│   Tabs:                         │
│   - Meals (Claude + Omi data)   │
│   - Body Metrics                │
│   - Workouts                    │
│   - Daily Vitals                │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────┐
│ Omi Device      │ ← "How many calories today?"
│ + Script        │
│                 │ → Fetches from Sheets
│                 │ → "1,450 / 3,000 cal"
└─────────────────┘
```

---

## 🛠️ Implementation Steps

### Immediate (Now):
1. ✅ Omi voice sync is running
2. ✅ Google Sheets created (9 tabs)
3. ⏳ Set up Zapier (15 min)
4. ⏳ Configure Claude Project

### This Week:
1. Update script to READ from Sheets
2. Test Claude → Zapier → Sheets flow
3. Test Omi queries from Sheets

### Enhancements (Later):
1. Add Gemini API for advanced Omi responses
2. Weekly summary emails via Poke
3. Trend analysis and predictions
4. Meal suggestions based on remaining macros

---

## 💰 Costs

- **Zapier Free**: 100 tasks/month (3-4 meals/day = ~100/month) ✅
- **Claude**: Your existing subscription ✅
- **Omi API**: Free ✅
- **Google Sheets**: Free ✅
- **Total**: $0/month!

If you exceed 100 Zapier tasks:
- Zapier Starter: $20/month (750 tasks)
- OR just use voice-only on heavy days

---

## 🎯 Benefits of This System

### Accuracy:
- ✅ Claude vision analyzes photos (best portion estimates)
- ✅ Auto-logs (no manual entry errors)
- ✅ Consistent format

### Convenience:
- ✅ One central database (Google Sheets)
- ✅ Access from anywhere (phone, PC, voice)
- ✅ Natural conversations with Omi

### Intelligence:
- ✅ Omi knows your full context (all meals logged)
- ✅ Can answer "What's my weekly average?"
- ✅ Personalized advice based on real data

### Flexibility:
- ✅ Photo when you want accuracy
- ✅ Voice when you're in a hurry
- ✅ Manual entry if needed (Sheets mobile app)

---

## 🧪 Testing the System

### Test 1: Photo → Sheets
1. Send food photo to Claude mobile
2. Check if row appears in Google Sheets (within 2 min)
3. ✅ If yes, Zapier is working!

### Test 2: Omi → Sheets
1. Tell Omi: "I had oatmeal for breakfast, about 300 calories"
2. Wait 15 min
3. Check Google Sheets
4. ✅ Should see new row

### Test 3: Omi Queries Sheets
1. Ask Omi: "How many calories have I eaten today?"
2. ✅ Should fetch from Sheets and respond

---

## 📋 Zapier Setup (Detailed)

### Create the Zap:

**Trigger:**
- App: Claude AI
- Event: New Conversation Message
- Filter: Project = "Food Tracker"

**Parser (Formatter):**
- Extract using regex:
  - `FOOD: (.+)` → food_name
  - `CALORIES: (\d+)` → calories
  - `PROTEIN: (\d+)g` → protein
  - `CARBS: (\d+)g` → carbs
  - `FAT: (\d+)g` → fat
  - `MEAL: (\w+)` → meal_type

**Action:**
- App: Google Sheets
- Event: Create Spreadsheet Row
- Spreadsheet: VedStack Health Tracker
- Worksheet: Meals
- Values:
  - Timestamp: `{{zap_meta_human_now}}`
  - Food: `{{food_name}}`
  - Portion: `{{portion}}`
  - Calories: `{{calories}}`
  - Protein (g): `{{protein}}`
  - Carbs (g): `{{carbs}}`
  - Fat (g): `{{fat}}`
  - Meal Type: `{{meal_type}}`
  - Source: "Claude Vision"
  - Confidence: "high"

---

## 🎉 End Result

**You get:**
1. Photo-based food logging (Claude mobile)
2. Voice-based logging (Omi device)
3. Automatic sync to Google Sheets
4. Conversational queries with Omi
5. Single source of truth for all health data

**All working together seamlessly!**

---

**Next Step:** Set up Zapier integration (15 minutes)

Want me to create a Zapier setup video/guide or just start with the Claude Project configuration?
