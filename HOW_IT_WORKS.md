# ❓ How Does This Actually Work?

## The Simple Answer

**Your PC does NOT need to be on all the time!**

Here are your 3 options:

---

## Option 1: PC On (Auto Everything) ✨ EASIEST

**Setup**: Run the setup script once
**Daily**: Nothing! PC auto-syncs every hour
**Your Phone**: Just talk to Omi, check Sheets

```
┌─────────────────────────────────────────────┐
│  YOUR PHONE                                  │
│  • Talk to Omi: "I ate banana"             │
│  • Omi app processes (2-3 min)             │
│  • Data saved to Omi cloud                  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  YOUR PC (RUNNING IN BACKGROUND)            │
│  • Script wakes up every hour              │
│  • Pulls from Omi cloud API                 │
│  • Finds: "banana" → 105 cal, 1.3g protein │
│  • Saves to local CSV file                  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  YOUR PHONE                                  │
│  • Open Google Sheets app                  │
│  • Import CSV (once per week)               │
│  • See all your meals!                      │
└─────────────────────────────────────────────┘
```

**Pros**:
- ✅ Completely automatic
- ✅ Hourly updates
- ✅ Zero effort

**Cons**:
- ⚠️ PC must be on (or sleep with wake timers)

**Best for**: If your PC is usually on anyway

---

## Option 2: PC Off (Manual Sync) ⚡ FLEXIBLE

**Setup**: Run the setup script once
**Daily**: Use phone normally
**Weekend**: Turn on PC, sync everything at once

```
MONDAY - FRIDAY (PC OFF)
┌─────────────────────────────────────────────┐
│  YOUR PHONE                                  │
│  • Monday: "Oats for breakfast"            │
│  • Tuesday: "Chicken shawarma"             │
│  • Wednesday: "Dal and chapati"            │
│  • Thursday: "Protein shake"                │
│  • Friday: "Biryani"                        │
│                                              │
│  Data stored in Omi cloud (safe!)          │
└─────────────────────────────────────────────┘

SATURDAY (PC ON)
┌─────────────────────────────────────────────┐
│  YOUR PC                                     │
│  1. Turn on PC                              │
│  2. Open terminal (WSL)                     │
│  3. Run: food-sync-now                      │
│  4. Script pulls ENTIRE WEEK from Omi      │
│  5. All 5 days logged to CSV!               │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  YOUR PHONE                                  │
│  • Open Google Sheets app                  │
│  • Import CSV                               │
│  • See full week of meals!                  │
└─────────────────────────────────────────────┘
```

**Pros**:
- ✅ PC can be off all week
- ✅ Still get all data
- ✅ Sync when convenient

**Cons**:
- ⚠️ Must remember to sync manually
- ⚠️ Not real-time (batch updates)

**Best for**: Laptop users, PC not always on

---

## Option 3: Cloud Server (Always On) 🚀 ADVANCED

**Setup**: Deploy script to free cloud service
**Daily**: Nothing! Cloud syncs hourly forever
**Your Phone**: Just talk to Omi, check Sheets

```
┌─────────────────────────────────────────────┐
│  YOUR PHONE                                  │
│  • Talk to Omi anytime                     │
│  • Data goes to Omi cloud                   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  CLOUD SERVER (RAILWAY/RENDER - FREE!)      │
│  • Runs 24/7 automatically                  │
│  • Syncs every hour                         │
│  • Your PC can be off/broken/anywhere!      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  YOUR PHONE                                  │
│  • Google Sheets always up-to-date         │
│  • No PC needed at all!                     │
└─────────────────────────────────────────────┘
```

**Pros**:
- ✅ Completely automatic
- ✅ No PC needed ever
- ✅ Free cloud services available
- ✅ Always running

**Cons**:
- ⚠️ Requires one-time cloud setup (I can help!)

**Best for**: True "set and forget" solution

---

## What Actually Needs To Run?

### Just This Python Script:

```python
# This is ALL that needs to run:
phone-food-sync.py

# What it does:
1. Pulls from Omi API (https://api.omi.me)
2. Finds food mentions
3. Looks up nutrition in database
4. Saves to CSV file

# How long: 5-10 seconds per run
# How often: Every hour (or when you run manually)
```

**That's it!** Super lightweight.

---

## Detailed: What Happens During Sync?

```
┌────────────────────────────────────────────┐
│ 1. FETCH OMI DATA (2 seconds)              │
│    curl https://api.omi.me/memories        │
│    Gets last 50 memories                    │
└────────────────────────────────────────────┘
                  ↓
┌────────────────────────────────────────────┐
│ 2. DETECT FOOD (1 second)                  │
│    Check each memory for food keywords     │
│    "I had banana" → Food detected!         │
└────────────────────────────────────────────┘
                  ↓
┌────────────────────────────────────────────┐
│ 3. LOOKUP NUTRITION (instant)              │
│    Check database: banana = 105 cal        │
│    No AI needed! Just lookup table         │
└────────────────────────────────────────────┘
                  ↓
┌────────────────────────────────────────────┐
│ 4. SAVE TO CSV (1 second)                  │
│    Append: 2025-11-12,banana,105,1.3,...   │
│    File: ~/.config/food-log.csv            │
└────────────────────────────────────────────┘
                  ↓
┌────────────────────────────────────────────┐
│ 5. OPTIONAL: POKE NOTIFICATION             │
│    Send to Poke: "Logged: banana 105 cal" │
└────────────────────────────────────────────┘

TOTAL TIME: ~5 seconds
TOTAL CPU: Negligible
TOTAL MEMORY: ~20 MB
```

**Super lightweight!** Barely uses resources.

---

## FAQ

### Q: Do I need Claude Desktop running?
**A**: NO! This version uses a simple food database. No AI needed.

### Q: What if I forget to sync for a month?
**A**: No problem! Omi keeps ALL your data in the cloud. When you sync, it pulls everything since last sync.

### Q: Can I check my data before syncing?
**A**: Yes! Open Omi app on phone → See all your memories there.

### Q: What about internet connection?
**A**: Omi needs internet to upload (uses phone data). Sync needs internet to download (uses PC/server).

### Q: Does Omi work offline?
**A**: Omi records offline, uploads when back online. Script syncs whenever it can connect.

### Q: Can I sync from multiple devices?
**A**: Yes! Same script can run on PC + laptop + cloud server. They all pull from same Omi cloud.

---

## My Recommendation

**For you, Vedanth**:

### Week 1: Option 2 (Manual Sync)
- Try it out with PC off
- Sync once at end of week
- See if you like the workflow

### Week 2-4: Option 1 (PC On)
- If PC is usually on anyway
- Let it auto-sync hourly
- More convenient

### Month 2: Option 3 (Cloud)
- Once you're comfortable
- Deploy to cloud
- Complete automation
- I'll help you set it up!

---

## Step-by-Step: Manual Sync (Option 2)

### One-Time Setup (5 minutes)

```bash
# 1. Create Google Sheet on phone
# 2. Get Sheet ID
# 3. On PC:
cd /mnt/d/MCP/foodtracker
export HEALTH_SHEET_ID="your_id"
./phone-setup.sh
```

### Daily Use (100% Phone)

```
Monday: Talk to Omi
Tuesday: Talk to Omi
Wednesday: Talk to Omi
Thursday: Talk to Omi
Friday: Talk to Omi

(Omi stores everything in cloud)
```

### Saturday Morning (5 minutes on PC)

```bash
# Turn on PC
# Open WSL terminal

cd /mnt/d/MCP/foodtracker
food-sync-now

# This pulls ENTIRE WEEK:
# - Monday breakfast: oats
# - Monday lunch: shawarma
# - Tuesday breakfast: eggs
# - ... all 5 days!

# Check the file:
cat ~/.config/food-log.csv

# Looks good? Import to Google Sheets!
```

### Import to Sheets (on phone)

```
1. Open Google Sheets app
2. Your "Food_Tracker" sheet
3. Menu → Import
4. Upload file (transfer from PC or use Google Drive)
5. Append rows
6. Done! See full week!
```

---

## Bottom Line

**PC does NOT need to be on 24/7!**

**You have 3 flexible options**:
1. PC on = Auto hourly
2. PC off = Manual weekly
3. Cloud = Auto forever

**All work great!** Pick what fits your lifestyle.

---

## Next Step

**Try Option 2 first** (manual sync):
1. Setup now (5 min)
2. Use phone all week
3. Sync this weekend
4. See if you like it!

Then upgrade to Option 1 or 3 if you want more automation.

**Ready?** Run `./phone-setup.sh` to begin!
