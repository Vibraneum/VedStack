# 🎯 CLAUDE-ONLY Food Tracking Solution

**The SIMPLEST possible method - just Claude mobile app!**

---

## 📱 Daily Workflow (30 seconds per meal)

### Step 1: Take Photo + Send to Claude
- Open Claude mobile app
- Send food photo
- Add text: "Log this meal"

### Step 2: Claude Responds with Link
Claude analyzes and replies:
```
✅ Logged!

Chicken Biryani with Raita
- Calories: 650
- Protein: 35g
- Carbs: 85g
- Fat: 18g

[Click to view in Google Sheets]
```

**That's it!** Data is already in your sheet.

---

## 🔧 Setup (One-Time, 2 Minutes)

### Create Claude Project with Custom Instructions

1. **Open Claude (mobile or desktop)**
2. **Create new Project**: "Food Tracker"
3. **Add this to Project Instructions:**

```
You are a nutrition tracking assistant for Vedanth's 8-week bulk.

GOAL: 54.9kg → 60kg (0.6kg/week)
DAILY TARGETS: 3,000 cal, 130g protein

When user sends food photo or description:
1. Analyze nutrition (be specific about portions)
2. Return formatted response with calories, protein, carbs, fat
3. Automatically log to Google Sheet via webhook

Format response as:
✅ Logged!

[Food Name]
- Calories: XXX
- Protein: XXg
- Carbs: XXg
- Fat: XXg
- Meal type: [breakfast/lunch/dinner/snack]

Today's totals: [running totals]
```

4. **Add Knowledge Base:**
   - Upload DATA_TODO.md
   - Upload your InBody scan image
   - Add text: "User is 20yo, 167cm, current weight 54.9kg, target 60kg"

5. **Set up Zapier/Make webhook** (optional - for auto-logging)

---

## 🤖 How It Works

### Option A: Manual Copy-Paste (Simplest)
1. Claude analyzes food
2. You copy the calories/macros
3. Paste into Google Sheets mobile app
4. Done!

**Time:** ~15 seconds per meal

### Option B: Zapier Integration (Automated)
1. Claude uses a function to call Zapier webhook
2. Zapier automatically logs to Google Sheets
3. You just send photos, everything else is automatic

**Setup:** https://zapier.com/apps/claude/integrations

---

## 📊 What Gets Logged

Every food entry logs to your Google Sheet:

| Timestamp | Food | Portion | Cal | Protein | Carbs | Fat | Meal | Source |
|-----------|------|---------|-----|---------|-------|-----|------|--------|
| 2025-11-12 14:30 | Chicken Biryani | 2 cups | 650 | 35g | 85g | 18g | lunch | Claude |

---

## 💡 Pro Tips

### For Better Accuracy:
- **Include reference**: "This is about 2 cups" or "Medium portion"
- **Multiple angles**: Send 2-3 photos if complex meal
- **Voice input**: Use voice-to-text to describe while looking at food

### For Speed:
- **Create shortcut**: "Log food" → Opens Claude + camera
- **Batch send**: Take photos during meal, send all at once later
- **Use templates**: Save common meals in Claude memory

### For Running Totals:
Claude Project remembers your daily intake:
- "How many calories today?" → Claude shows running total
- "Am I hitting my protein goal?" → Claude checks against 130g target
- "Weekly progress?" → Claude shows week-over-week changes

---

## 🎨 Sample Conversation

**You:** [Sends photo of dal rice]

**Claude:**
```
✅ Analyzed!

Dal Rice with Sabzi
- Portion: ~2 cups rice, 1 cup dal, 1/2 cup sabzi
- Calories: 520
- Protein: 18g
- Carbs: 92g
- Fat: 8g
- Meal type: Lunch

💪 Today's Progress:
- Total: 1,450 / 3,000 cal (48%)
- Protein: 62 / 130g (48%)
- On track for 60kg goal!

Need: 1,550 more calories today
```

---

## 🔗 Optional: Zapier Automation

### Setup Zapier (5 minutes):

1. **Create Zap**: Claude AI → Google Sheets
2. **Trigger**: New message in Claude project "Food Tracker"
3. **Action**: Add row to Google Sheets
4. **Map fields**:
   - Timestamp → Column A
   - Food name → Column B
   - Calories → Column D
   - Protein → Column E
   - etc.

**Result:** Every Claude analysis auto-logs to Sheets!

**Link:** https://zapier.com/apps/claude-ai/integrations/google-sheets

---

## ✅ Why This Is PERFECT

✅ **No PC needed** - Works from phone only
✅ **No Omi needed** - Just Claude mobile app
✅ **No coding** - Set up once in Claude Project
✅ **High accuracy** - Claude vision analyzes portions
✅ **Conversational** - Ask questions, get insights
✅ **Always available** - Cloud-based, works anywhere
✅ **Running totals** - Claude tracks daily progress
✅ **Voice input** - Speak your meals instead of typing

---

## 🚀 Start Now

1. Open Claude mobile app
2. Create project "Food Tracker"
3. Add the instructions above
4. Send your first food photo!

**That's it! You're tracking!** 📊

---

## 📞 Troubleshooting

**Q: Can Claude actually log to Google Sheets?**
A: Yes, via Zapier or Make. Or just manually copy-paste.

**Q: Does Claude remember previous meals?**
A: Yes! Project memory keeps daily running totals.

**Q: What if I forget to log a meal?**
A: Just send photo later - add time in message: "Had this at 1pm"

**Q: Can I bulk-send multiple meals?**
A: Yes! Send all photos at once: "Here are my 3 meals today"

---

## 🎯 Result

**Before:**
- Complex setup with scripts, APIs, email monitoring
- PC needs to be on
- Multiple systems to maintain

**After:**
- One app (Claude mobile)
- Send photo
- Done!

**The simplest solution is often the best!** 🎉

---

**Created:** November 2025
**For:** Vedanth's 8-week bulk (54.9kg → 60kg)
