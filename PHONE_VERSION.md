# 📱 Food Tracker - Phone Version

**Works completely from your phone! No PC needed, no Claude Desktop needed!**

---

## How This Works (Phone-Friendly)

```
YOU TALK TO OMI (on your phone)
        ↓
OMI APP processes and stores
        ↓
SCRIPT runs on PC (in background)
        ↓
Pulls from Omi API automatically
        ↓
Logs to GOOGLE SHEETS
        ↓
CHECK SHEET ON PHONE anytime!
```

**Key Point**: Claude Desktop does **NOT** need to be running! The script uses a built-in food database (30+ foods).

---

## Setup (One-Time, 10 Minutes)

### Step 1: Create Google Sheet (on phone)

1. Open **Google Sheets app** on phone
2. Create new sheet: "Food_Tracker"
3. Create tab: "Meals"
4. Add columns in row 1:
   ```
   Date | Time | Food | Calories | Protein | Carbs | Fat
   ```
5. Tap Share → "Anyone with link can edit"
6. Copy the sheet URL

### Step 2: Get Sheet ID (on phone)

From the URL you copied, extract the ID:
```
https://docs.google.com/spreadsheets/d/[THIS_IS_YOUR_ID]/edit
```

Example:
```
1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
```

**Save this ID** - you'll need it in Step 3!

### Step 3: Setup on PC (one time)

On your PC (can close later!):

```bash
cd /mnt/d/MCP/foodtracker
export HEALTH_SHEET_ID="paste_your_id_here"
./phone-setup.sh
```

**That's it!** Now your PC can be closed/asleep. The script runs on a server or can run whenever PC is on.

---

## Daily Use (100% on Phone)

### Morning

**Open Omi app** on phone, talk naturally:
```
"I had oats with banana for breakfast"
```

Omi processes (2-3 min) and stores in cloud.

### Throughout Day

Just talk to Omi:
- "Chicken shawarma for lunch"
- "Protein shake as snack"
- "Dal and 2 chapatis for dinner"

### Check Your Data

**Open Google Sheets app** on phone → See all meals logged!

| Date | Time | Food | Calories | Protein |
|------|------|------|----------|---------|
| 11/12 | 08:15 | oats | 150 | 5g |
| 11/12 | 08:15 | banana | 105 | 1.3g |
| 11/12 | 13:30 | chicken shawarma | 650 | 45g |

---

## How It Works Without Claude Desktop

### Built-in Food Database (30+ Foods)

The script knows these foods **automatically** (no AI needed!):

**Indian**:
- chicken shawarma, dal, chapati, roti, rice, paneer
- chicken curry, biryani, paratha, idli, dosa, samosa

**Breakfast**:
- oats, banana, eggs, milk, bread, peanut butter

**Protein**:
- chicken breast, protein shake, whey protein

**For unknown foods**: Uses a simple estimate (400 cal, 20g protein)

**No Claude Desktop needed!** The script is smart enough on its own.

---

## Sync Schedule

### Auto-Sync (Recommended)

If your PC is on/server is running:
- **Every hour**: Automatically pulls Omi data → logs to Sheets
- You do nothing!
- Just check Google Sheets app anytime

### Manual Sync (If PC off)

When you turn on PC:
```bash
cd /mnt/d/MCP/foodtracker
./sync-now.sh
```

Syncs all missed data since last run.

---

## Phone Apps You Need

1. **Omi App** (iOS/Android)
   - Talk to record meals
   - Data syncs to cloud automatically

2. **Google Sheets App** (iOS/Android)
   - View your logged meals
   - See daily totals
   - Check progress

**That's it!** No other apps needed.

---

## Can I Do This 100% on Phone?

### Option A: PC Runs in Background (Easiest)

- Setup once on PC
- Leave PC on (or use a cloud server)
- Script runs every hour automatically
- Use phone for everything else (Omi + checking Sheets)

### Option B: Manual Sync (PC off most of the time)

- Setup once on PC
- Turn off PC
- Use phone (Omi app) all week
- Weekend: Turn on PC, run sync-now
- All week's data logs to Sheets at once

### Option C: Cloud Server (Advanced)

- Deploy script to a free cloud service (Railway, Render)
- Runs 24/7 even with PC off
- Completely phone-based daily use
- (Need help setting this up? Let me know!)

---

## What About Poke?

**Great question!** Poke can send you notifications:

**Setup Poke Notifications**:
1. After script logs to Sheets
2. Sends summary to Poke device
3. You get haptic notification on wrist
4. "Logged: Chicken shawarma, 650 cal, 45g protein ✅"

**Add this** (optional):
```bash
# Edit phone-setup.sh and enable Poke notifications
POKE_ENABLED=true
POKE_API_KEY="pk_GH6UrWQ1JCpPzmsYTAX0LzNfGKn_TTQDquPUpAOujWM"
```

Now every time food is logged, Poke vibrates with the summary!

---

## Troubleshooting (From Phone)

### "Nothing showing in Google Sheet"

**Check**:
1. Did Omi process your audio? (open Omi app, see if memory is there)
2. Is PC on? (if using PC-based sync)
3. Wait for next hourly sync (or run sync-now on PC)

### "Can't access from phone"

**Make sure**:
1. Google Sheet is set to "Anyone with link can edit"
2. You're logged into same Google account on phone
3. Open Google Sheets app (not browser)

### "Want to sync right now"

**Two options**:
1. Turn on PC, run: `cd /mnt/d/MCP/foodtracker && ./sync-now.sh`
2. Or wait for next hourly auto-sync

---

## Sample Daily Flow (Phone Only)

**7:00 AM** - Wake up
- Talk to Omi: "My weight is 55.2 kg"

**8:00 AM** - Breakfast
- Talk to Omi: "Oats with banana and milk for breakfast"

**9:00 AM** - Auto-sync runs (PC in background)
- Weight logged ✅
- Breakfast logged ✅

**9:30 AM** - Check progress
- Open Google Sheets app on phone
- See today's meals
- Running total: 255 cal, 14.3g protein

**1:00 PM** - Lunch
- Talk to Omi: "Chicken shawarma"

**2:00 PM** - Auto-sync
- Lunch logged ✅
- Total now: 905 cal, 59.3g protein

**6:00 PM** - Dinner
- Talk to Omi: "Dal and 2 chapatis"

**7:00 PM** - Auto-sync
- Dinner logged ✅
- Daily total: 1,160 cal, 74.3g protein

**10:00 PM** - Review
- Open Sheets app
- See full day logged automatically
- No manual entry needed! ✅

---

## Advanced: Add Custom Foods

If you eat something not in the database:

**On PC**, edit `/mnt/d/MCP/foodtracker/simple-omi-sync.py`:

Find `NUTRITION_DB` (around line 30) and add:
```python
'your_food': (calories, protein, carbs, fat),
```

Example:
```python
'paneer tikka': (350, 25, 10, 20),
```

Save, and now the script knows this food!

---

## Summary

**What you have**:
- ✅ Voice-based food logging (Omi app on phone)
- ✅ Auto-sync to Google Sheets (hourly)
- ✅ View on phone anytime (Sheets app)
- ✅ No Claude Desktop needed
- ✅ No API keys needed
- ✅ Works even when PC is off (manual sync)

**What you need**:
- Omi app (phone)
- Google Sheets app (phone)
- PC setup once (can turn off later)

**Daily effort**: 0 minutes (just talk to Omi!)

---

**Next**: Run `/mnt/d/MCP/foodtracker/phone-setup.sh` on PC to get started!
