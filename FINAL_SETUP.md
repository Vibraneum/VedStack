# ✅ FINAL SETUP - 8 Weeks to 60kg

**Sheet ID:** `1LYz3qgsR5GF3tt-ut6PpOVyKfCb4y-H6a5EW8Okw5SI`
**Timeline:** 8 weeks (aggressive but doable)
**Target:** 54.9kg → 60kg (+0.6kg/week)
**End Date:** January 7, 2026

---

## 🔐 Authentication Check

### ✅ What You Already Have:

**1. Omi API Key** ✅
```
omi_dev_2b7983a707b5ede131a0903a1655d918
```
- Already in your config
- Used to fetch Omi memories
- **NO Omi app installation needed** (just API)

**2. Poke API Key** ✅
```
pk_GH6UrWQ1JCpPzmsYTAX0LzNfGKn_TTQDquPUpAOujWM
```
- Already in your config
- Used for notifications

**3. Google Service Account** ✅
```
/home/ved/.config/google-credentials.json
```
- Already exists
- Used for Google Sheets API

**4. Google Sheet** ✅
```
https://docs.google.com/spreadsheets/d/1LYz3qgsR5GF3tt-ut6PpOVyKfCb4y-H6a5EW8Okw5SI/edit
```
- Just created
- Need to share with service account

---

## 🚀 Setup Steps (2 Minutes)

### Step 1: Share Google Sheet

**Find service account email:**
```bash
cat /home/ved/.config/google-credentials.json | grep client_email
```

You'll see something like:
```
"client_email": "food-tracker@your-project.iam.gserviceaccount.com"
```

**Share your sheet:**
1. Open: https://docs.google.com/spreadsheets/d/1LYz3qgsR5GF3tt-ut6PpOVyKfCb4y-H6a5EW8Okw5SI/edit
2. Click "Share" button
3. Add that email
4. Set to "Editor"
5. Done!

### Step 2: Run Setup

```bash
cd /mnt/d/MCP/foodtracker
./setup-dead-simple.sh
```

**It will:**
- Create 9 tabs in your Google Sheet
- Set up auto-start (systemd)
- Configure environment
- Start the script

### Step 3: Start Talking to Omi

**That's it!**

---

## ❓ About Omi App

### Do You Need the Omi App?

**NO - for this script!**

**How it works:**
```
Your Omi Device → Omi Cloud (transcribes voice)
                      ↓
              Omi API (we fetch from here)
                      ↓
               Python Script (this system)
```

**The script uses Omi API**, not the Omi mobile app.

**You DO need:**
- ✅ Omi device (physical wearable)
- ✅ Omi account (to get API key)
- ✅ Omi API key (you have it)

**You DON'T need:**
- ❌ Omi mobile app installed
- ❌ To interact with Omi app
- ❌ Any Omi app features

**Your workflow:**
1. Talk to Omi device (wearable)
2. Omi device uploads to cloud
3. Script fetches from cloud (API)
4. Done!

---

## 🎯 8-Week Plan (Finalized)

### Timeline

| Week | Weight Target | Gain | Date |
|------|---------------|------|------|
| **Week 0** | 54.9 kg | Start | Nov 12 |
| **Week 2** | 56.1 kg | +1.2 | Nov 26 |
| **Week 4** | 57.3 kg | +2.4 | Dec 10 |
| **Week 6** | 58.5 kg | +3.6 | Dec 24 |
| **Week 8** | 60.0 kg | +5.1 | **Jan 7** 🎉 |

### Updated Macros (Aggressive)

**Daily targets:**
- **Calories:** 3,000 (up from 2,850)
- **Protein:** 130g (up from 120g)

**Why higher?**
- 0.6kg/week needs ~500 cal surplus
- Still doable, won't feel terrible
- 60-70% muscle, 30-40% fat (acceptable)

### What to Expect

**Week 1-2:**
- Initial water weight gain (+0.8-1kg)
- Body adjusting to more food
- Energy levels high

**Week 3-4:**
- Visible size increase (chest, arms)
- Strength going up
- Getting used to eating more

**Week 5-6:**
- Noticeable muscle gain
- PRs in gym
- Clothes fitting tighter

**Week 7-8:**
- Final push to 60kg
- Looking bigger and fuller
- Goal achieved! 🎉

---

## 📊 Google Sheets Structure (9 Tabs)

Setup script creates:

### Core Tracking (5 tabs)
1. **Meals** - Food logged
2. **Workouts** - Gym sessions
3. **Body Metrics** - Weight, measurements
4. **Recovery** - Sleep, soreness, stress
5. **Goals** - Progress tracking

### Biohacking (4 tabs)
6. **Daily Vitals** - RHR, HRV, mood, energy
7. **Supplements** - What you're taking
8. **Lifestyle** - Water, steps, sunlight
9. **Weekly Summary** - Auto-calculated trends

**All populated automatically from Omi!**

---

## 🔔 Poke Notifications (Updated)

**6 reminders per day:**

**7:00 AM** - Morning stats
```
Morning protocol! ☀️
Target: 3,000 cal, 130g protein
Log: weight, RHR, mood, energy
```

**10:00 AM** - Breakfast check
```
Breakfast logged?
Target: 800+ cal, 40g+ protein
Energy level?
```

**1:00 PM** - Lunch reminder
```
Lunch check! 🍽️
Current: X/3,000 cal
Need: X more
```

**4:00 PM** - Pre-gym snack
```
Pre-workout fuel!
Snack logged?
Energy for gym?
```

**6:00 PM** - Evening summary
```
Evening summary! 🌙
Today: X/3,000 cal (X%)
Protein: X/130g (X%)
Dinner plan?
```

**10:00 PM** - Sleep prep
```
Sleep prep! 😴
Supplements taken?
Target: 7.5hr
```

---

## ✅ Final Checklist

Before running setup:

- [x] Google Sheet created (done)
- [x] Sheet ID extracted (done)
- [ ] Service account email found (do this)
- [ ] Sheet shared with service account (do this)
- [x] Omi API key (have it)
- [x] Poke API key (have it)
- [x] Google credentials JSON (have it)
- [x] Claude Desktop installed (have it)

**2 things left:**
1. Find service account email
2. Share sheet with it

---

## 🚀 Run Setup Now

```bash
cd /mnt/d/MCP/foodtracker

# Check service account email
cat /home/ved/.config/google-credentials.json | grep client_email

# Share your sheet with that email (in browser)

# Run setup
./setup-dead-simple.sh
```

**Takes 2 minutes. Then you're done.**

---

## 💪 Your 8-Week Journey Starts Now

**Today:** Setup (2 min)
**Tomorrow:** Start tracking everything
**January 7:** Hit 60kg! 🎉

**Just talk to Omi. Everything else automatic.**

---

## 🔧 Commands You'll Use

```bash
# Check if running
health-status

# View logs
health-logs

# Restart if needed
health-restart
```

---

## ❓ Quick FAQ

**Q: Do I need the Omi app?**
A: No. Script uses Omi API directly.

**Q: Does PC need to be on 24/7?**
A: No. Turn on 1-2x per day, or leave on. Flexible.

**Q: Can I change the 8-week timeline?**
A: Yes. Edit `USER_PROFILE` in script. 10-12 weeks = safer.

**Q: What if I miss a day?**
A: No problem. Script syncs everything when PC turns on.

**Q: Is 3,000 cal too much?**
A: For 0.6kg/week gain, it's correct. Start and adjust based on progress.

---

## 🎉 You're Ready!

**Sheet configured:** ✅
**Auth setup:** ✅
**8-week plan:** ✅
**Script ready:** ✅

**Next:** Share sheet + run setup!

**LET'S GET TO 60KG! 💪🔥**
