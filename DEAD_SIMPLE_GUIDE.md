# 💪 DEAD SIMPLE HEALTH COACH

**Goal:** 54.9kg → 60kg in 12 weeks
**Method:** Talk to Omi. Everything else automatic.
**Cost:** $0 (uses your subscriptions)

---

## ⚡ What You Do

```
1. Talk to Omi about EVERYTHING:
   - "I had chicken shawarma for lunch"
   - "Just finished chest workout, 3x10 bench press"
   - "Weighed 55.2kg this morning"
   - "Slept 7 hours, chest is sore"
   - Literally anything related to health

2. Optional: Take photos of food → WhatsApp to yourself
   (Script doesn't analyze photos yet, but Claude can later)

3. Check Google Sheets on phone when you want

4. That's it.
```

---

## 🚀 Setup (5 Minutes)

### Step 1: Create Google Sheet

**On phone or PC:**
1. New spreadsheet: "Health Tracker"
2. Copy Sheet ID from URL: `docs.google.com/spreadsheets/d/YOUR_ID/edit`
3. Share with service account email (from `google-credentials.json`)

### Step 2: Run Setup

```bash
cd /mnt/d/MCP/foodtracker
./setup-dead-simple.sh
```

**It will:**
- ✅ Install dependencies
- ✅ Create Google Sheets structure (5 tabs)
- ✅ Set up auto-start (systemd service)
- ✅ Add helper commands
- ✅ Start the script

### Step 3: Done

Script is now running in background. PC turns on → script auto-starts.

---

## 📊 What Gets Tracked

### Everything You Say to Omi:

**Nutrition** 🍽️
- Food items & portions
- Calories, protein, carbs, fat
- Meal timing & type
- Example: "I had a large chicken shawarma with extra sauce"

**Fitness** 💪
- Workouts & exercises
- Sets, reps, weights
- Muscle groups trained
- Energy levels
- Example: "Just finished back workout, deadlifts 3x8 at 85kg, felt strong"

**Body Metrics** 📏
- Weight measurements
- Body measurements (chest, arms, waist)
- Progress observations
- Example: "Weighed 55.2kg this morning, up 0.3kg"

**Recovery** 🧘
- Sleep hours & quality
- Muscle soreness (location, severity)
- Stress levels
- Example: "Slept 7 hours, lower back is tight from deadlifts"

**Goals** 🎯
- New goals
- Concerns
- Questions
- Example: "Want to bench 100kg by March"

---

## 🤖 How It Works

### Background Process:

```
PC turns on → Script auto-starts → Loops forever:

Every 15 minutes:
1. Fetch new Omi memories
2. Send to Claude Desktop for analysis
3. Claude extracts ALL info (food, gym, sleep, etc.)
4. Log to Google Sheets (appropriate tab)
5. If urgent, send Poke notification

Scheduled check-ins:
- 10:00 AM - Breakfast check
- 1:00 PM - Lunch reminder
- 6:00 PM - Evening summary
```

### Claude Desktop Analysis:

Claude reads your Omi transcripts and extracts:
- **Nutrition:** Food, portions, calories, macros
- **Fitness:** Exercises, weights, sets/reps
- **Recovery:** Sleep, soreness, stress
- **Metrics:** Weight, measurements
- **Goals:** New targets, concerns

**All from natural speech. No special format needed.**

---

## 📱 Daily Poke Notifications

### 10:00 AM - Breakfast Check
```
Morning check! ☀️

Yesterday done. Today's targets:
• 2,850 cal
• 120g protein

Breakfast logged? Energy level? (1-10)
```

### 1:00 PM - Lunch Reminder
```
Lunch check! 🍽️

Current: 850 cal, 35g protein
Need: 2,000 cal, 85g protein more

Lunch logged? How was the gym?
```

### 6:00 PM - Evening Summary
```
Evening summary! 🌙

Today: 2,700/2,850 cal (95%)
Protein: 115/120g (96%)
Meals: 4

Dinner plan? Need 150 cal more.
How's body feeling? Soreness?
```

---

## 📊 Google Sheets Structure

**5 Tabs:**

### 1. Meals
```
| Date | Time | Food | Portion | Cal | Protein | Carbs | Fat | Type | Notes |
```

### 2. Workouts
```
| Date | Time | Type | Muscle Groups | Exercises | Duration | Energy | Notes |
```

### 3. Body Metrics
```
| Date | Weight | Chest | Arms | Waist | Body Fat % | Notes |
```

### 4. Recovery
```
| Date | Sleep Hrs | Quality | Soreness Location | Severity | Stress | Notes |
```

### 5. Goals
```
| Goal Type | Target | Current | Start | Deadline | Progress | Status |
```

**All auto-populated from Omi!**

---

## 🎯 Your 12-Week Plan

### Timeline

**Start:** 54.9 kg (Nov 12, 2025)
**Target:** 60.0 kg (Feb 12, 2026)
**Rate:** +0.4 kg/week (sustainable)

### Why 12 Weeks?

**Safe gain rate:**
- 0.4 kg/week = 80% muscle, 20% fat (excellent ratio)
- You'll feel good, have energy, gym performance up
- Won't get "skinny fat" - will look good at 60kg

**Your plan:**
- Daily: 2,850 calories, 120g protein
- Gym: 6x/week (current schedule)
- Weekly weigh-ins: Track progress
- Adjust if needed: Claude monitors and suggests

### Milestones

| Week | Target Weight | Check |
|------|---------------|-------|
| Week 4 | 56.5 kg (+1.6kg) | First check-in |
| Week 8 | 58.1 kg (+3.2kg) | Halfway |
| Week 12 | 60.0 kg (+5.1kg) | GOAL! 🎉 |

---

## 🔧 Commands

```bash
# Check if running
health-status

# View live logs
health-logs

# Restart service
health-restart

# Stop service
health-stop
```

---

## 💡 Pro Tips

### For Best Results:

**1. Talk to Omi naturally**
```
✅ Good: "I had a large chicken shawarma with extra sauce after the gym"
✅ Good: "Just weighed myself, 55.2kg"
✅ Good: "Slept like shit, only 6 hours"
✅ Good: "Deadlifts felt heavy today, did 85kg for 3 sets of 8"

❌ Bad: Nothing. Claude understands everything.
```

**2. Be specific when possible**
```
Better: "Large chicken shawarma" vs "chicken"
Better: "3 sets of 8 reps at 85kg" vs "did deadlifts"
Better: "Chest is sore" vs "sore"
```

**3. Mention timing**
```
"Had breakfast at 8am"
"Post-workout meal"
"Before bed snack"
```

**4. Weekly weigh-ins**
```
Every Sunday morning:
"Weighed 55.2kg this morning"
```

**5. Photos (optional)**
- Take photos of meals → WhatsApp to yourself
- Omi doesn't analyze photos (yet), but helpful reference
- Claude can analyze photos in future updates

---

## 🐛 Troubleshooting

### Script not running?
```bash
health-status  # Check status
health-restart # Restart if needed
```

### No data in Sheets?
1. Check script is running: `health-status`
2. View logs: `health-logs`
3. Verify Omi has new memories (check Omi app)
4. Check Sheet ID in `.env` file

### Claude not responding?
1. Make sure Claude Desktop is installed
2. Test: `claude --prompt "test"`
3. If timeout, increase timeout in script

### Poke not sending?
1. Check Poke API key in `.env`
2. Verify Poke app is set up
3. Check logs for Poke errors

---

## 📈 What to Expect

### Week 1-2: Adjustment
- Getting used to talking to Omi about everything
- Seeing how Claude analyzes your data
- Finding your rhythm

### Week 3-4: First Results
- Weight: +0.8-1.2 kg
- Strength: Noticeable increase
- Energy: Good levels
- Sheets: Full of data, seeing patterns

### Week 5-8: Midpoint
- Weight: +2-3 kg
- Gym: PRs happening
- Body: Visibly bigger (chest, arms)
- Confidence: High

### Week 9-12: Final Push
- Weight: +4-5 kg
- Strength: Significant gains
- Body: Clear muscle definition
- Goal: 60kg achieved! 🎉

---

## 🎓 Technical Buddy Style

Claude talks to you like a technical buddy:

**Examples:**

```
"Bro, you hit 2,750 cal (96% of target).
Protein at 118g (98%). Solid day.
One more 200-cal snack before bed puts you at 100%."

"Deadlift volume today: 85kg × 3 × 8 = 2,040kg total.
That's +240kg vs last week (1,800kg).
Progressive overload working. Keep it up."

"Sleep at 6hrs (target: 7.5hr) = recovery deficit.
Lower back DOMS + poor sleep = injury risk elevated.
Consider rest day or light upper body only."
```

**Data-driven. Friendly. Honest.**

---

## 🚨 Important Notes

### PC Must Be On (Sometimes)

**How often?**
- Turn on PC: 1-2x per day (morning, evening)
- Or: Leave on all day
- Or: Use laptop (on/off flexible)

**Why?**
- Script runs locally (uses Claude Desktop)
- Can't run in cloud (no Claude Desktop API)

**What if PC is off?**
- Omi still captures everything
- When PC turns on, script syncs all missed data
- Nothing lost!

### Timeline is Flexible

**Can't hit 12 weeks?**
- No problem. 10 weeks = 0.5kg/week (still healthy)
- 16 weeks = 0.3kg/week (slower but safer)
- Adjust `target_weeks` in script

**Want faster?**
- **Don't go faster than 0.6kg/week**
- Beyond that = mostly fat gain
- Not worth it

### Claude Desktop Required

**Must have:**
- Claude Desktop installed
- Claude CLI working (`claude --prompt "test"`)
- Your Claude subscription active

**Why?**
- Uses your subscription (free for you)
- Full AI intelligence
- No API costs

---

## 📞 Support

### If Something Breaks:

1. **Check logs:**
   ```bash
   health-logs
   ```

2. **Check status:**
   ```bash
   health-status
   ```

3. **Restart:**
   ```bash
   health-restart
   ```

4. **Check Google Sheets:**
   - Make sure shared with service account
   - Verify Sheet ID in `.env`

5. **Test Claude:**
   ```bash
   claude --prompt "Analyze this: I had chicken"
   ```

---

## ✅ Final Checklist

Before you start:

- [ ] Google Sheet created
- [ ] Shared with service account email
- [ ] Sheet ID added to `.env`
- [ ] Setup script ran successfully
- [ ] Service is running (`health-status`)
- [ ] Claude Desktop installed
- [ ] Omi device paired

Ready? **Talk to Omi about your next meal!** 🚀

---

## 🎉 Summary

**Your system:**
```
Talk to Omi → Script analyzes (Claude) → Logs to Sheets → Poke notifies you
```

**Your goal:**
```
54.9kg → 60kg in 12 weeks (sustainable, mostly muscle)
```

**Your effort:**
```
Talk naturally. Everything else automatic.
```

**Cost:**
```
$0/month (uses your subscriptions)
```

---

**LET'S GET TO 60KG! 💪🔥**

*Script by AI, gains by you.*
