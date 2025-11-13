# 🎯 THE SIMPLEST SOLUTION

**Claude Projects + Google Sheets Knowledge Base = Perfect!**

---

## 💡 The Insight

Claude Projects can use **Google Sheets as a knowledge base**!

No scripts, no Zapier, no APIs - just:
1. Photo → Claude mobile
2. Claude writes to Sheets (via project knowledge)
3. Omi reads from same Sheets
4. Done!

---

## 🔧 Setup (5 Minutes)

### Step 1: Share Your Google Sheet Publicly

1. Open: https://docs.google.com/spreadsheets/d/1LYz3qgsR5GF3tt-ut6PpOVyKfCb4y-H6a5EW8Okw5SI/edit
2. Click "Share"
3. Change to: **"Anyone with the link can EDIT"**
4. Copy the link

### Step 2: Create Claude Project

1. **Open Claude** (mobile or desktop)
2. **Create Project**: "Food Tracker"
3. **Add Knowledge**:
   - Click "Add Knowledge"
   - Paste Google Sheets URL
   - Claude will sync the sheet!

4. **Add Custom Instructions**:

```
You are my nutrition tracking assistant.

GOAL: 54.9kg → 60kg in 8 weeks (0.6kg/week)
DAILY: 3,000 cal, 130g protein

YOUR KNOWLEDGE BASE:
- Google Sheet with my food logs (Meals tab)
- Contains: Timestamp, Food, Portion, Calories, Protein, Carbs, Fat

WHEN I SEND A FOOD PHOTO:
1. Analyze portion sizes carefully
2. Estimate nutrition (use Indian food knowledge)
3. ADD A NEW ROW to the Meals tab with:
   - Current timestamp
   - Food name
   - Portion size
   - Calories
   - Protein (g)
   - Carbs (g)
   - Fat (g)
   - Meal type (breakfast/lunch/dinner/snack based on time)
   - Source: "Claude Vision"
   - Confidence: "high"

4. Respond with summary:
   "✅ Logged! [Food] - [calories] cal, [protein]g protein

   Today's total: [sum from sheet]
   Remaining: [3000 - total] cal, [130 - total protein]g protein"

WHEN I ASK QUESTIONS:
- Read the Google Sheet for current data
- Calculate totals, trends, averages
- Give personalized advice based on MY data

Be conversational but data-driven!
```

### Step 3: Test It!

1. Send food photo to Claude
2. Say: "lunch"
3. Claude analyzes, adds row to sheet, responds with totals
4. ✅ Check Google Sheets - new row should be there!

---

## 🗣️ For Omi Integration

Update `dead-simple-health-coach.py` to also READ from Sheets:

```python
def get_context_from_sheets():
    """Get today's nutrition from Sheets to give Omi context"""
    # Fetch today's meals
    # Calculate totals
    # Return as context for Claude Desktop analysis
```

When you ask Omi:
- "How many calories today?"
- Script reads Sheets (which has Claude's data)
- Responds with totals

**Both systems use same Sheet - perfect sync!**

---

## 📱 Your New Workflow

### Logging Food:
1. 📸 Photo → Claude mobile: "lunch"
2. ✅ Claude logs to Sheets automatically
3. 💬 Claude responds with totals

### Checking Progress:
- **Via Claude**: "How am I doing today?"
- **Via Omi**: "What's my calorie count?" (reads same Sheet)

### Adding Details:
- **Claude**: Photo analysis (accurate)
- **Omi**: Voice updates ("Had protein shake, 30g protein")

---

## 🎯 Why This Works

✅ **No intermediary scripts** - Claude writes directly to Sheets
✅ **No Zapier** - Built into Claude Projects
✅ **No APIs** - Uses your existing subscriptions
✅ **Bi-directional** - Claude reads AND writes
✅ **Shared knowledge** - Omi script reads same Sheet
✅ **Real-time** - Updates immediately
✅ **Simple** - Just send photos to Claude!

---

## ⚡ Advanced: GitHub Actions (Optional)

If you want automatic backups:

**Create `.github/workflows/sync-sheet.yml`:**

```yaml
name: Backup Google Sheets

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Download Sheet as CSV
        run: |
          wget -O data/meals-backup.csv \
          "https://docs.google.com/spreadsheets/d/1LYz3qgsR5GF3tt-ut6PpOVyKfCb4y-H6a5EW8Okw5SI/export?format=csv&gid=0"

      - name: Commit backup
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add data/
          git commit -m "Daily backup: $(date)"
          git push
```

Now your Google Sheets data is also versioned on GitHub!

---

## 🔄 Complete Data Flow

```
YOU (Phone)
    ↓
📸 Photo
    ↓
Claude Mobile (Vision Analysis)
    ↓
Google Sheets (Knowledge Base)
    ↙         ↘
Claude         Omi Script
(read/write)   (reads for context)
    ↘         ↙
    Your Questions
```

---

## 🎉 Final Setup Summary

1. ✅ Make Google Sheet editable by anyone with link
2. ✅ Add Sheet URL to Claude Project knowledge
3. ✅ Add custom instructions to Claude Project
4. ✅ Send test photo
5. ✅ Verify row appears in Sheet
6. ✅ Ask Omi "How many calories today?" (should read from Sheet)

**Total setup time: 5 minutes**
**Total cost: $0/month**
**Total complexity: Minimal!**

---

## 💬 Example Conversation

**You:** [Sends photo of biryani]

**Claude:**
```
✅ Logged!

Chicken Biryani with Raita
- Portion: 2 cups biryani, 1/2 cup raita
- 680 cal, 38g protein, 87g carbs, 19g fat

Today's totals:
- 1,450 / 3,000 cal (48%)
- 62 / 130g protein (48%)

On track! Need 1,550 more cal today.
Aim for 68g more protein at dinner.
```

**You (to Omi):** "How's my protein today?"

**Omi:** "You've had 62 grams out of 130. You need 68 more grams to hit your goal."

**Both reading from same Sheet - perfect sync!**

---

**This is THE solution. No over-engineering. Just works.** ✅
