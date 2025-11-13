# 🚀 START HERE - Dead Simple Health Coach

**Built:** November 12, 2025
**Goal:** 54.9kg → 60kg in 12 weeks
**Method:** Talk to Omi. Everything automatic.
**Cost:** $0/month

---

## ⚡ Quick Start (5 Minutes)

### 1. Create Google Sheet
- New spreadsheet: "Health Tracker"
- Get Sheet ID from URL
- Share with service account (from `google-credentials.json`)

### 2. Run Setup
```bash
cd /mnt/d/MCP/foodtracker
./setup-dead-simple.sh
```

### 3. Start Talking to Omi
```
"I had chicken shawarma for lunch"
"Just finished chest workout"
"Weighed 55kg this morning"
```

**Done. Everything else automatic.**

---

## 📁 Files You Need

### Core System
- **`dead-simple-health-coach.py`** - Main script (runs automatically)
- **`setup-dead-simple.sh`** - One-time setup
- **`.env`** - Your config (created during setup)

### Documentation
- **`START_HERE.md`** ← You are here
- **`DEAD_SIMPLE_GUIDE.md`** - Complete user guide
- **`BIOHACKING_PROTOCOL.md`** - Advanced tracking (Bryan Johnson style)

### Old Files (Ignore These)
- `webhook_server.py` - Old webhook version
- `phone-food-sync.py` - Old simple version
- All other `.md` files - Research/old docs

---

## 💡 What You Track

### Just Talk to Omi About:

**Food** 🍽️
```
"I had chicken shawarma, large portion, with extra sauce"
```

**Gym** 💪
```
"Finished back workout, deadlifts 3 sets of 8 at 85kg, felt strong"
```

**Body** 📏
```
"Weighed 55.2kg this morning, up 0.3kg"
```

**Sleep/Recovery** 😴
```
"Slept 7.5 hours, sleep score was 85, chest is sore from yesterday"
```

**Vitals** ❤️
```
"Morning stats: resting heart rate 58, mood 8/10, energy 8/10"
```

**Lifestyle** 🧘
```
"Had 3 liters of water today, got 15 minutes of sunlight"
"Took vitamin D and omega-3 this morning"
```

**Claude Desktop analyzes everything and logs to Google Sheets.**

---

## 🎯 Your 12-Week Plan

| Week | Weight Target | Progress |
|------|---------------|----------|
| **Start** | 54.9 kg | Baseline |
| **Week 4** | 56.5 kg | +1.6 kg ✅ |
| **Week 8** | 58.1 kg | +3.2 kg ✅ |
| **Week 12** | 60.0 kg | **GOAL!** 🎉 |

**Rate:** +0.4 kg/week (sustainable, mostly muscle)
**Daily:** 2,850 calories, 120g protein
**Gym:** 6x per week (your current schedule)

**Why 12 weeks?**
- Safe, sustainable rate
- 80% muscle, 20% fat (good ratio)
- Won't feel like shit
- Actually look good at 60kg

---

## 📊 Google Sheets Tabs

Your data gets logged to 5+ tabs:

1. **Meals** - All food logged
2. **Workouts** - All gym sessions
3. **Body Metrics** - Weight, measurements
4. **Recovery** - Sleep, soreness, stress
5. **Goals** - Progress tracking

**Optional (Biohacking):**
6. **Daily Vitals** - RHR, HRV, mood, energy
7. **Supplements** - What you're taking
8. **Lifestyle** - Water, steps, sunlight, meditation
9. **Weekly Summary** - Auto-calculated trends

**Check on phone anytime!**

---

## 🔔 Poke Notifications

You'll get 3-6 reminders per day:

**7:00 AM** - Morning stats
**10:00 AM** - Breakfast check
**1:00 PM** - Lunch reminder
**6:00 PM** - Evening summary
**10:00 PM** - Sleep prep *(optional)*
**Sunday 9:00 AM** - Weekly measurements *(optional)*

---

## 🔧 Commands

```bash
# Check if running
health-status

# View logs
health-logs

# Restart
health-restart

# Stop
health-stop
```

---

## 📚 Read Next

### New User?
Read: **`DEAD_SIMPLE_GUIDE.md`**
- Complete walkthrough
- Daily workflow
- Troubleshooting
- Pro tips

### Want to Go Deeper?
Read: **`BIOHACKING_PROTOCOL.md`**
- Bryan Johnson-style tracking
- Advanced biomarkers
- Supplement stack
- Lifestyle optimization
- "Project Vedanth" vision

---

## ✅ What You Built

**Complete AI health coach:**
- ✅ Voice logging (Omi)
- ✅ AI analysis (Claude Desktop)
- ✅ Auto-logging (Google Sheets)
- ✅ Reminders (Poke)
- ✅ Nutrition tracking
- ✅ Fitness tracking
- ✅ Body metrics tracking
- ✅ Recovery tracking
- ✅ Goal progress tracking
- ✅ Biohacking metrics *(optional)*

**All for $0/month using your subscriptions.**

---

## 🚨 Important Notes

### PC Must Be On (Sometimes)
- Turn on 1-2x per day (morning, evening)
- Or leave on all day
- Or use laptop (flexible)
- When off: Data queues, syncs when on

### Timeline is Flexible
- 12 weeks recommended (sustainable)
- Can do 10 weeks (0.5kg/week, faster)
- Can do 16 weeks (0.3kg/week, slower)
- **Don't go faster than 0.6kg/week** (fat gain)

### Claude Desktop Required
- Must be installed and working
- Test: `claude --prompt "test"`
- Uses your subscription ($0 cost)

---

## 🎉 You're Ready!

**Setup done?** → Start talking to Omi
**Have questions?** → Read `DEAD_SIMPLE_GUIDE.md`
**Want advanced tracking?** → Read `BIOHACKING_PROTOCOL.md`

**Your next meal?** → Tell Omi about it! 🚀

---

## 💪 Let's Get to 60kg!

**Week 1 starts now.**
**Talk naturally. Track everything. Hit your goals.**

*System by AI. Gains by you.* 🔥

---

**Files Location:** `/mnt/d/MCP/foodtracker/`
**Google Sheets:** Check your phone!
**Support:** Read the guides, check logs, restart if needed.
