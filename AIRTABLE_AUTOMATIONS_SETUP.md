# VedStack Airtable Automations - Step-by-Step Setup

**Time to Complete**: 15-20 minutes
**Difficulty**: Easy (just follow clicks)

---

## 🤖 WHAT ARE AUTOMATIONS?

Airtable automations = automatic actions triggered by events or schedules.

**Examples:**
- Every day at 6 PM → Send you a notification with today's calorie total
- Every Sunday 8 AM → Remind you to weigh in
- When you hit 55kg, 56kg, etc. → Celebrate! 🎉

---

## ⚠️ IMPORTANT: AIRTABLE FREE PLAN LIMITS

**Free Plan:**
- ✅ 100 automation runs per month
- ✅ Basic triggers (scheduled time, record created)
- ✅ Basic actions (send email, update record)

**If you run out:**
- Upgrade to Plus ($10/month) for 25,000 runs
- OR prioritize only 1-2 automations (see recommendations below)

---

## 🎯 RECOMMENDED AUTOMATIONS (Priority Order)

### 1. **Daily Nutrition Check** (6 PM) - HIGHEST PRIORITY
**Runs**: 30x/month (within free limit)
**Value**: Reminds you to hit 3,000 cal before bed

### 2. **Weekly Weigh-In Reminder** (Sunday 8 AM) - HIGH PRIORITY
**Runs**: 4-5x/month (within free limit)
**Value**: Never miss your weekly measurement

### 3. **Milestone Celebrations** (When weight increases) - NICE TO HAVE
**Runs**: ~8x total (when you hit 55, 56, 57, 58, 59, 60 kg)
**Value**: Motivational boost

**SKIP FOR NOW:**
- Low protein day alert (would use 30 runs/month)
- Daily check-ins (would exceed free limit)

---

## 🔧 AUTOMATION 1: DAILY NUTRITION CHECK (6 PM)

**Goal**: Every day at 6 PM, remind you to check if you've hit 3,000 cal and 130g protein.

### Step-by-Step:

**1. Open Automations**
- Go to your VedStack base: https://airtable.com/appSgD8XmiKRBrGXd
- Top menu bar → Click **"Automations"**
- Click **"Create automation"**

**2. Name It**
- Click "Untitled automation" at top
- Rename: **"Daily Nutrition Check (6 PM)"**

**3. Set Trigger**
- Click **"Add trigger"**
- Choose: **"At a scheduled time"**
- Settings:
  - Frequency: **Daily**
  - Time: **6:00 PM**
  - Timezone: **Your timezone** (probably Asia/Kolkata - IST)
- Click **"Done"**

**4. Add Action (Option A: Email - Easiest)**
- Click **"Add action"**
- Choose: **"Send an email"**
- Settings:
  - To: **Your email address**
  - From name: **VedStack Bot**
  - Subject: **Daily Check: Did you hit your targets?**
  - Message:
```
Hey Vedanth! 👋

It's 6 PM - time for your daily nutrition check.

Go to Airtable Food Log and check:
✅ Have you hit 3,000 calories today?
✅ Have you hit 130g protein today?

If not, you have 6 hours before bed to:
- Add a protein shake (25g protein, 120 cal)
- Eat a high-calorie snack (mathri, banana, etc.)
- Plan one more meal

Remember: You can't optimize what you don't measure! 💪

View Food Log: https://airtable.com/appSgD8XmiKRBrGXd/tblXXXXXXXX

- VedStack Bot
```
- Click **"Done"**

**5. Test It**
- Click **"Test automation"** (top right)
- Check your email - did you receive it?
- If yes: Click **"Turn on automation"** (toggle at top)

**6. Done!**
- You'll now get a 6 PM email every day

---

**4. Add Action (Option B: Slack - If you use Slack)**

If you prefer Slack notifications instead of email:

- Click **"Add action"**
- Choose: **"Send a Slack message"**
- Connect your Slack account
- Settings:
  - Channel: **#vedstack-tracking** (or DM yourself)
  - Message:
```
🍽️ Daily Nutrition Check

It's 6 PM! Time to review today's intake:

✅ Calories target: 3,000
✅ Protein target: 130g

Check Food Log: https://airtable.com/appSgD8XmiKRBrGXd

If you're short, add a protein shake or snack before bed! 💪
```

---

## 🔧 AUTOMATION 2: WEEKLY WEIGH-IN REMINDER (Sunday 8 AM)

**Goal**: Every Sunday at 8 AM, remind you to weigh yourself and log to Body Metrics.

### Step-by-Step:

**1. Create New Automation**
- Automations → **"Create automation"**
- Name: **"Weekly Weigh-In Reminder"**

**2. Set Trigger**
- Click **"Add trigger"**
- Choose: **"At a scheduled time"**
- Settings:
  - Frequency: **Weekly**
  - Day: **Sunday**
  - Time: **8:00 AM**
  - Timezone: **Asia/Kolkata (IST)**
- Click **"Done"**

**3. Add Action (Email)**
- Click **"Add action"**
- Choose: **"Send an email"**
- Settings:
  - To: **Your email**
  - From name: **VedStack Bot**
  - Subject: **🏋️ Weekly Weigh-In Time!**
  - Message:
```
Good morning Vedanth! ☀️

It's Sunday - time for your weekly weigh-in!

📊 Protocol:
1. Empty stomach (go to bathroom first)
2. Same time every week (8 AM Sunday)
3. Same scale
4. Weigh yourself 2-3 times, take average

Then log to Body Metrics table:
https://airtable.com/appSgD8XmiKRBrGXd/tblXqlBNY8WFqw2Gy

🎯 Target: +0.6kg from last week
🎯 Goal: 54.9kg → 60kg (Week X/8)

Last week: [You'll need to check manually]
This week: [Log after weighing]

After logging, ask Claude Desktop: "How was my week?"

Let's get to 60kg! 💪

- VedStack Bot
```
- Click **"Done"**

**4. Test & Enable**
- Test it (check email)
- Turn on automation

---

## 🔧 AUTOMATION 3: MILESTONE CELEBRATIONS (When you hit 55, 56, 57... kg)

**Goal**: Automatic celebration when you hit weight milestones.

### Step-by-Step:

**1. Create New Automation**
- Automations → **"Create automation"**
- Name: **"Milestone Celebrations 🎉"**

**2. Set Trigger**
- Click **"Add trigger"**
- Choose: **"When record matches conditions"**
- Settings:
  - Table: **Body Metrics**
  - Conditions: **When record meets these conditions...**
  - Add condition: **Weight (kg)** is **greater than or equal to** **55**
- Click **"Done"**

**3. Add Conditional Logic (Optional - Advanced)**

If you want different messages for different milestones:

- Click **"Add action"**
- Choose: **"Conditional action"**
- Create conditions for 55kg, 56kg, 57kg, etc.

**OR just use a simple email:**

**4. Add Action (Email)**
- Click **"Add action"**
- Choose: **"Send an email"**
- Settings:
  - To: **Your email**
  - From name: **VedStack Bot**
  - Subject: **🎉 MILESTONE REACHED! 🎉**
  - Message:
```
🎉🎉🎉 CONGRATULATIONS VEDANTH! 🎉🎉🎉

You just hit a weight milestone!

📊 Your Progress:
- Starting weight: 54.9 kg (Oct 24)
- Current weight: [Check Body Metrics]
- Target: 60 kg (Dec 19)

🔥 You're getting CLOSER!

Keep going:
✅ 3,000 cal daily
✅ 130g protein daily
✅ 6 workouts weekly
✅ Legs 2-3x focus

Bryan Johnson would be proud! 💪

- VedStack Bot
```
- Click **"Done"**

**5. Test & Enable**
- You can manually create a test Body Metrics entry with weight 55kg
- See if email arrives
- Delete test entry
- Turn on automation

**Note**: This will trigger every time ANY weigh-in is ≥55kg. To make it trigger only ONCE per milestone, you'd need more complex logic (skip for now).

---

## 🚫 AUTOMATIONS TO SKIP (Free Plan Limitations)

### ❌ Daily Low Protein Alert (11 PM)
**Why skip**: Would use 30 runs/month, plus needs complex calculation

**Alternative**: Just check Airtable "Today" view before bed manually

### ❌ Daily Morning Motivation
**Why skip**: 30 runs/month for low value

**Alternative**: Set phone alarm/reminder instead

### ❌ Auto-Create Weekly Summary
**Why skip**: Complex, requires aggregations, uses API calls

**Alternative**: Manually create weekly summary, or ask Claude to do it

---

## 📊 TRACKING AUTOMATION USAGE

**Check how many runs you've used:**

1. Go to Automations tab
2. Top right corner shows: **"X / 100 runs this month"**
3. Resets every month on the 1st

**If you're running out:**
- Disable low-priority automations
- Upgrade to Plus ($10/month for 25,000 runs)

---

## 🎯 RECOMMENDED SETUP FOR FREE PLAN

**Enable these (total ~38 runs/month):**
1. ✅ Daily Nutrition Check (6 PM) - 30 runs/month
2. ✅ Weekly Weigh-In Reminder (Sunday 8 AM) - 4 runs/month
3. ✅ Milestone Celebrations - ~4 runs over 8 weeks

**Total**: 38 runs/month (within 100 limit)

**Skip everything else** - do manually or use phone reminders.

---

## 🔔 ALTERNATIVE: USE PHONE REMINDERS (FREE)

If you don't want to use Airtable automation runs:

**iOS Reminders / Android Google Tasks:**
- 6 PM daily: "Check VedStack - hit 3,000 cal & 130g protein?"
- 8 AM Sunday: "Weigh-in time! Log to Body Metrics"

**Pros**: Free, unlimited, works offline
**Cons**: Not automated (you dismiss them)

---

## 📱 BETTER OPTION: POKE NOTIFICATIONS (If Available)

You mentioned Poke integration in your Claude config. If Poke works:

**Ask Claude Desktop:**
"Send me a Poke notification at 6 PM daily saying: Check VedStack nutrition - 3,000 cal? 130g protein?"

**Poke advantages:**
- More likely to read than email
- Faster than email
- Can integrate with Airtable via Zapier

---

## 🤖 FUTURE: OMI VOICE INTEGRATION

Once Omi is integrated:

**Voice-triggered automation:**
- "Omi, did I hit my protein today?" → Omi reads Airtable Food Log → Answers
- "Omi, log my workout" → Omi transcribes → Claude analyzes → Airtable logs

**This is MUCH better than scheduled automations** - you ask when YOU want, not on a fixed schedule.

---

## ✅ SETUP CHECKLIST

- [ ] Automation 1: Daily Nutrition Check (6 PM) - Created & Enabled
- [ ] Automation 2: Weekly Weigh-In Reminder (Sunday 8 AM) - Created & Enabled
- [ ] Automation 3: Milestone Celebrations - Created & Enabled
- [ ] Tested all 3 automations (received emails)
- [ ] Confirmed automation run count is under 100/month
- [ ] Set phone alarm as backup for 6 PM check

---

## 🚀 NEXT STEPS

**After setting up automations:**

1. **Test food logging** - Take photo, say "Log this to my tracker"
2. **Create views** - "Today's Meals" view in Food Log
3. **Install mobile app** - Airtable iOS/Android
4. **Start tracking** - Every meal, every day, for 8 weeks

**Remember**: Automations are nice-to-have. The CORE system (photo logging via Claude) is what matters most.

---

**Questions?** Ask Claude in Claude Desktop: "Help me set up Airtable automations"

**Time to set up**: 15-20 minutes
**Value**: Daily reminders + weekly accountability + milestone motivation

**LET'S GO! 💪**
