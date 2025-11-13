# 🚀 Airtable + Claude Desktop Setup Guide

**Quick setup guide for VedStack health tracking system**

---

## ✅ What's Already Done

1. ✅ Airtable base created (`appSgD8XmiKRBrGXd`)
2. ✅ 7 tables created with proper structure
3. ✅ Claude Desktop MCP configured
4. ✅ Personal Access Token (PAT) set up
5. ✅ User profile data populated
6. ✅ System tested and working!

---

## 📋 Tables Created

1. **Food Log** - Meal tracking with macros
2. **User Profile** - Your stats and goals
3. **Body Metrics** - Weight, body fat, muscle tracking
4. **Workouts** - Exercise logs
5. **Daily Vitals** - Sleep, energy, recovery
6. **Supplements** - What you take daily
7. **Weekly Summary** - Progress tracking

---

## 🎯 How to Use

### **Step 1: Access Your Base**
https://airtable.com/appSgD8XmiKRBrGXd

### **Step 2: Log Food (Claude Desktop)**
```
1. Take photo of food
2. Open Claude Desktop
3. Upload image
4. Say: "Log this food"
5. Done! Check Airtable.
```

### **Step 3: Track Progress**
- Add body weight weekly to "Body Metrics"
- Log workouts to "Workouts"
- Track sleep in "Daily Vitals"
- Review "Weekly Summary" every Sunday

---

## 🔧 Airtable Enhancements to Add

### **Views to Create:**

#### 1. **Today's Dashboard**
- Go to Food Log table
- Click "+ Create view"
- Name: "Today"
- Filter: `Date` is `today`
- Show: All fields
- Purpose: See today's meals at a glance

#### 2. **This Week's Progress**
- Go to Food Log
- Create view: "This Week"
- Filter: `Date` is `within the last 7 days`
- Group by: `Meal Type`
- Sum fields: Calories, Protein, Carbs, Fat

#### 3. **Workout Tracker**
- Go to Workouts table
- Create view: "Recent Workouts"
- Filter: Last 7 days
- Sort: Date descending

### **Formulas to Add:**

#### In Food Log Table:
Add new formula fields:

**1. Protein % of Target**
```
{Protein} / 130 * 100
```

**2. Calories % of Target**
```
{Calories} / 3000 * 100
```

**3. Date (Day Name)**
```
DATETIME_FORMAT({Date}, 'dddd, MMMM D')
```

#### In Weekly Summary Table:

**1. Weight Progress Status**
```
IF(
  {Weight Change (kg)} >= 0.5,
  "✅ On Track",
  IF(
    {Weight Change (kg)} >= 0.3,
    "⚠️ Slow Progress",
    "❌ Need to Eat More"
  )
)
```

**2. Protein Target Hit?**
```
IF({Avg Daily Protein} >= 130, "✅", "❌")
```

### **Automations to Set Up:**

#### Automation 1: Daily Nutrition Check
```
Trigger: Every day at 6 PM
Action: Send notification via Poke
Message: "Today's nutrition check - have you hit 3,000 cal?"
```

**How to set up:**
1. Click "Automations" in Airtable
2. "Create automation"
3. Trigger: "At scheduled time" → 6:00 PM daily
4. Action: "Send notification" (requires Poke integration)

#### Automation 2: Weekly Summary Reminder
```
Trigger: Every Sunday at 8 AM
Action: Send notification
Message: "Time for weekly weigh-in and progress review!"
```

#### Automation 3: Milestone Celebrations
```
Trigger: When "Weight (kg)" in Body Metrics reaches milestone
Condition: Weight >= 55, 56, 57, 58, 59, or 60 kg
Action: Send celebration message!
```

---

## 📱 Mobile App Setup

### **Airtable Mobile:**
1. Download Airtable app (iOS/Android)
2. Login with your account
3. Pin "VedStack" base to home

### **Quick Add Widget:**
- Add Airtable widget to home screen
- Select: Food Log table
- Shows: Today's calorie total

---

## 🎨 Appearance Customizations

### **Color Code Your Data:**

**Food Log - Meal Types:**
- Breakfast: 🟡 Yellow
- Lunch: 🟠 Orange
- Dinner: 🔴 Red
- Snack: 🟢 Green

**Workouts - Intensity:**
- Low: 🟢 Green
- Medium: 🟡 Yellow
- High: 🔴 Red

**Daily Vitals - Sleep Quality:**
- Poor: 🔴 Red
- Fair: 🟡 Yellow
- Good: 🟢 Green
- Excellent: 🔵 Blue

### **Field Descriptions:**
Add descriptions to fields so you remember what to track:
1. Click field name → "Customize field type"
2. Add description
3. Example: "Protein (g)" → "Target: 130g per day (2.4g/kg)"

---

## 📊 Dashboard Ideas

### **Create an Interface (Airtable Pro):**
If you upgrade to Pro, create a custom dashboard with:
- Today's meals card
- Weekly calorie chart
- Weight progression graph
- Workout frequency calendar
- Daily vitals summary

---

## 🔗 Integrations

### **Already Working:**
- ✅ Claude Desktop (via MCP)

### **Can Add:**
- **Poke**: Notifications for check-ins
- **Google Calendar**: Sync workout schedule
- **Zapier**: Auto-backup to Google Sheets
- **Slack**: Daily progress updates

---

## 🆘 Common Issues

### **"Claude can't write to Airtable"**
**Fix:**
```bash
# Check config file
cat "C:\Users\vedan\AppData\Roaming\Claude\claude_desktop_config.json"

# Should see "airtable" section with your PAT
# If not, add it and restart Claude Desktop
```

### **"I don't see my tables"**
- Verify you're in the correct base: appSgD8XmiKRBrGXd
- Check you're logged into the right Airtable account
- Refresh the page (Ctrl+R / Cmd+R)

### **"Formulas showing error"**
- Field names are case-sensitive
- Make sure field types match (number fields for calculations)
- Test formula on single record first

---

## 💾 Backup Strategy

### **Option 1: Manual Weekly Export**
1. Go to each table
2. Click "..." menu
3. "Download CSV"
4. Save to backup folder

### **Option 2: GitHub Actions (Automated)**
We can set up automatic daily backups to GitHub - let me know if you want this!

### **Option 3: Airtable Snapshots**
- Airtable Pro has automatic snapshots
- Can restore to any point in time

---

## 🎓 Learning Resources

- **Airtable University:** https://airtable.com/university
- **Formula Guide:** https://support.airtable.com/docs/formula-field-reference
- **Automation Guide:** https://support.airtable.com/docs/getting-started-with-airtable-automations

---

## 🎯 Next Steps

1. [ ] Create "Today's Dashboard" view
2. [ ] Add formula fields for % of targets
3. [ ] Set up daily 6 PM automation
4. [ ] Install Airtable mobile app
5. [ ] Test logging a meal via Claude Desktop
6. [ ] Add this week's body weight to Body Metrics
7. [ ] Review User Profile - all data correct?

---

**Created:** November 13, 2025
**Status:** System ready to use
**Base URL:** https://airtable.com/appSgD8XmiKRBrGXd

**Questions?** Just ask Claude in your next chat! 🚀
