# 🎯 VedStack - Complete Airtable Health Tracking System

**Owner:** Vedanth
**Goal:** 54.9kg → 60kg in 8 weeks (Bryan Johnson Blueprint + Aggressive Bulk)
**Base ID:** appSgD8XmiKRBrGXd
**Status:** ✅ LIVE & Working

---

## 📊 **System Overview**

VedStack is your comprehensive health tracking system built on Airtable, integrated with Claude Desktop for automatic food logging via image analysis.

### **What Makes This Special:**
- ✅ **Photo → AI → Database**: Take food photo, Claude analyzes, auto-logs to Airtable
- ✅ **Bryan Johnson Style**: Track everything like a biohacker
- ✅ **Real-time Dashboard**: View all your data in one place
- ✅ **8-Week Bulk Protocol**: Precise tracking for muscle gain goals

---

## 🗂️ **Tables Structure**

### 1️⃣ **User Profile**
**Purpose:** Core stats and goals

| Field | Value |
|-------|-------|
| Name | Vedanth |
| Age | 20 years old |
| Height | 167 cm (5'5.7") |
| Start Weight | 54.9 kg |
| Target Weight | 60 kg in 8 weeks |
| Weekly Target | +0.6 kg/week |
| InBody Score | 74/100 (Oct 2025) |
| Body Fat | 7.8 kg (14.3%) |
| Muscle Mass | 26.2 kg → Target: 30 kg |
| Focus Area | Legs (96%), Arms (104-107%) |
| Daily Calories | 3,000 cal (TDEE: 2,460 + 500) |
| Daily Protein | 130g (2.4g/kg target) |
| Daily Carbs | 400g |
| Daily Fat | 75g |
| Training | 6x/week (focus on legs) |
| Start Date | October 24, 2025 |
| Goal Style | Bryan Johnson longevity + aggressive bulk |

### 2️⃣ **Food Log**
**Purpose:** Track every meal with macros

**Fields:**
- Date (datetime) - When you ate
- Food Description (long text) - What you ate, portions
- Calories (number) - Total calories
- Protein (number, 1 decimal) - Grams of protein
- Carbs (number, 1 decimal) - Grams of carbs
- Fat (number, 1 decimal) - Grams of fat
- Meal Type (dropdown) - Breakfast/Lunch/Dinner/Snack

**How to Use:**
1. Take food photo in Claude Desktop
2. Say: "Log this food"
3. Claude analyzes and writes here automatically!

### 3️⃣ **Body Metrics**
**Purpose:** Track weight, body composition weekly

**Fields:**
- Date
- Weight (kg) - Your current weight
- Body Fat % - Percentage
- Muscle Mass (kg) - Skeletal muscle
- Notes - Any observations (InBody scans, measurements)

**Baseline Entry:**
- Oct 24, 2025: 54.9 kg, 14.3% BF, 26.2 kg muscle
- InBody Score: 74/100

### 4️⃣ **Workouts**
**Purpose:** Log all exercise

**Fields:**
- Date
- Exercise Type (dropdown) - Gym/Cardio/Sports/Physio
- Description - What you did
- Duration (min) - How long
- Intensity (dropdown) - Low/Medium/High

**Your Goal:** 6x/week, focus on legs

### 5️⃣ **Daily Vitals**
**Purpose:** Sleep, energy, recovery

**Fields:**
- Date
- Sleep Hours - How much you slept
- Sleep Quality (dropdown) - Poor/Fair/Good/Excellent
- Energy Level (dropdown) - Low/Medium/High
- Notes - How you feel

**Bryan Johnson Tip:** Track consistently to optimize recovery!

### 6️⃣ **Supplements**
**Purpose:** Track what you take

**Fields:**
- Date
- Supplement Name - What supplement
- Dosage - How much
- Time Taken (dropdown) - Morning/Afternoon/Evening/Pre-Workout/Post-Workout

### 7️⃣ **Weekly Summary**
**Purpose:** Track weekly progress

**Fields:**
- Week Number (1-8 for your bulk)
- Week Start Date
- Avg Daily Calories - Average across the week
- Avg Daily Protein - Average protein intake
- Weight Change (kg) - How much you gained/lost
- Workouts Completed - How many sessions
- Notes - Overall observations

**Your Target:** +0.6 kg/week average

---

## 🎨 **How to Maximize Airtable**

### **Views You Should Create:**

#### **📅 Daily Dashboard**
- Filter: Today's date
- Show: Food Log + Body Metrics + Workouts + Daily Vitals
- Purpose: See everything for today in one view

#### **📈 Weekly Progress**
- Group by: Week Number
- Show: Weekly Summary + aggregated Food Log data
- Purpose: Track your 8-week bulk progress

#### **💪 Workout Tracker**
- Filter: Last 7 days
- Group by: Exercise Type
- Show: Total duration, frequency
- Purpose: Ensure you're hitting 6x/week

#### **🥗 Nutrition Analysis**
- Show: Food Log only
- Sum: Total Calories, Protein, Carbs, Fat
- Purpose: Daily macro tracking

### **Formulas to Add:**

#### **In Food Log (if you want calculated fields):**
Add a "% of Daily Target" field:
```
Protein: {Protein} / 130 * 100
Calories: {Calories} / 3000 * 100
```

#### **In Weekly Summary:**
Add "On Track?" formula:
```
IF({Weight Change (kg)} >= 0.5, "✅ On Track",
   IF({Weight Change (kg)} >= 0.3, "⚠️ Slow Progress",
      "❌ Not Gaining"))
```

### **Automations to Set Up:**

#### **1. Daily Nutrition Check (6 PM)**
- **Trigger:** Every day at 6 PM
- **Action:** Send email/Poke notification
- **Content:** "Today's totals: X calories, Y protein. Need Z more!"

#### **2. Weekly Summary Auto-Create**
- **Trigger:** Every Sunday at 8 AM
- **Action:** Create new Weekly Summary record
- **Content:** Aggregate last 7 days of data

#### **3. Weight Milestone Alerts**
- **Trigger:** When Body Metrics weight changes
- **Condition:** If weight >= milestone (55kg, 56kg, etc.)
- **Action:** Send celebration notification!

---

## 🚀 **Daily Workflow**

### **Morning:**
1. Log breakfast in Claude Desktop (photo + "log this")
2. Check Weekly Summary view - are you on track?
3. Plan your meals to hit 3,000 cal, 130g protein

### **Throughout Day:**
- Photo every meal/snack → Claude logs automatically
- Check "Daily Dashboard" view to see progress

### **Evening:**
- Log workout (if gym day)
- Log Daily Vitals (sleep from last night, energy today)
- Review total macros

### **Sunday (Weekly):**
- Take body weight measurement → log to Body Metrics
- Review Weekly Summary
- Adjust next week's plan if needed

---

## 🔗 **Claude Desktop Integration**

### **Setup (Already Done!):**
✅ Airtable MCP configured in Claude Desktop
✅ PAT with full permissions
✅ All 7 tables created

### **How It Works:**
1. You: Take food photo in Claude Desktop
2. You: Say "Log this food" or "Log this"
3. Claude: Analyzes image (food items, portions, macros)
4. Claude: Writes to Food Log table automatically
5. You: Check Airtable - data is there!

### **Commands You Can Use:**
```
"Log this food"
"Add this meal to my log"
"Track this"
"How many calories today?" (Claude reads from Airtable)
"What's my protein total?"
"Show me this week's progress"
```

---

## 📱 **Airtable Mobile App Tips**

### **Quick Actions:**
- **Add on the go:** Use Airtable mobile to manually add entries
- **Check totals:** View "Daily Dashboard" to see progress
- **Update vitals:** Log sleep/energy from your phone

### **Widgets:**
Add Airtable widget to home screen showing:
- Today's calorie total
- Workouts this week
- Current weight

---

## 🎯 **8-Week Bulk Milestones**

| Week | Target Weight | Muscle Gain | Focus |
|------|---------------|-------------|-------|
| 1 | 55.5 kg | +0.3 kg | Routine building |
| 2 | 56.1 kg | +0.6 kg | Hit protein consistently |
| 3 | 56.7 kg | +0.9 kg | Increase leg volume |
| 4 | 57.3 kg | +1.2 kg | Mid-progress InBody scan |
| 5 | 57.9 kg | +1.5 kg | Push heavier weights |
| 6 | 58.5 kg | +1.8 kg | Fine-tune nutrition |
| 7 | 59.1 kg | +2.1 kg | Maximum effort |
| 8 | 60.0 kg | +2.4 kg | Final InBody scan |

**Track in Weekly Summary table!**

---

## 📊 **Advanced: Data Analysis**

### **Airtable Extensions to Add:**

#### **1. Chart Extension**
- Create graphs of:
  - Weight progression over 8 weeks
  - Daily calories trend
  - Protein intake vs target

#### **2. Page Designer**
- Create weekly report PDF
- Share with trainer/nutritionist

#### **3. Scripting Extension**
- Auto-calculate weekly averages
- Flag days below protein target

---

## 🔐 **Data Backup**

### **Automated Backups:**
- Airtable has version history (Pro plan)
- You can manually export to CSV weekly
- We can set up GitHub Actions to auto-backup

### **Export Options:**
- CSV: Good for Excel/Sheets
- JSON: Good for developers
- PDF: Good for sharing reports

---

## 💡 **Pro Tips**

### **Nutrition:**
- Log BEFORE eating (helps with portion awareness)
- Use consistent measurement units (grams, cups)
- Include cooking methods (grilled vs fried = different calories)

### **Tracking:**
- Take weekly progress photos (not in Airtable, but track dates)
- Weigh yourself same time each week (morning, empty stomach)
- Log workouts immediately after gym (while it's fresh)

### **Optimization:**
- Review Weekly Summary every Sunday
- Adjust calorie target if not gaining +0.6 kg/week
- Increase leg workout volume if still lagging

---

## 🆘 **Troubleshooting**

### **"Claude isn't logging to Airtable"**
- Check Claude Desktop config file has Airtable MCP
- Restart Claude Desktop
- Verify PAT permissions (should have data.records:write)

### **"I don't see my data"**
- Check correct base: appSgD8XmiKRBrGXd
- Verify you're in the right table
- Refresh the view

### **"Formulas not working"**
- Check field names match exactly (case-sensitive)
- Verify field types (number vs text)
- Test formula on one record first

---

## 📚 **Resources**

- **Airtable Base:** https://airtable.com/appSgD8XmiKRBrGXd
- **Claude Desktop:** Already configured with MCP
- **InBody Scan Baseline:** October 24, 2025
- **Goal Timeline:** 8 weeks (Oct 24 - Dec 19, 2025)

---

## 🎉 **Success Metrics**

### **You'll Know It's Working When:**
- ✅ Claude logs meals automatically from photos
- ✅ You can see daily/weekly trends in Airtable
- ✅ You're consistently hitting 3,000 cal, 130g protein
- ✅ Weekly weight gain is +0.5-0.7 kg
- ✅ Leg measurements improving (check every 2 weeks)

---

**Created:** November 13, 2025
**Status:** System LIVE and operational
**Next Update:** Add Omi voice integration (planned)

**Let's get you to 60kg! 💪**
