# 🎯 SIMPLE START - No API Keys Needed!

**The Problem**: All those guides were too complicated!

**Simple Solution**: Use what you ALREADY HAVE:
- ✅ Your Claude Desktop subscription (no API needed!)
- ✅ Your Omi device subscription
- ✅ Your Poke device
- ✅ Google Sheets (free)

**No Gemini API, no extra costs, no complexity!**

---

## How This Works (Simple Version)

```
YOU TALK TO OMI
     ↓
"I had chicken shawarma"
     ↓
OMI CAPTURES IT (in Omi app)
     ↓
Every hour: Script pulls from Omi
     ↓
Asks CLAUDE DESKTOP (your subscription!) to analyze
     ↓
Claude figures out: "650 calories, 45g protein"
     ↓
Logs to GOOGLE SHEETS
     ↓
DONE! ✅
```

**You don't need any API keys!** We use Claude Desktop (which you're already paying for).

---

## Setup (5 Minutes, 3 Steps)

### Step 1: Create Google Sheet (2 minutes)

1. Go to https://sheets.google.com
2. Create new sheet, name it: **"My_Health_Tracker"**
3. Copy the ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[COPY_THIS_PART]/edit
   ```
4. Create one tab called **"Meals"** with these columns in row 1:
   ```
   Date | Time | Food | Calories | Protein | Carbs | Fat | Notes
   ```

That's it for the sheet!

### Step 2: Save Your Sheet ID

```bash
# In terminal (WSL):
echo 'export HEALTH_SHEET_ID="paste_your_sheet_id_here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 3: Run Simple Setup

```bash
cd /mnt/d/MCP
./SIMPLE_SETUP.sh
```

**Done!** It will now auto-sync every hour using Claude Desktop.

---

## Daily Use (Super Simple)

### Just Talk to Omi:

**Morning**: "I had oats with banana for breakfast"
**Lunch**: "Chicken shawarma for lunch"
**Dinner**: "Dal and 2 chapatis"
**Snack**: "Protein shake"

**Every hour**: The script automatically:
1. Pulls your Omi memories
2. Sends to Claude Desktop: "What food did Vedanth eat? Calculate calories"
3. Claude responds with nutrition
4. Logs to your Google Sheet

**You do nothing!** Just check your sheet anytime to see all your meals logged.

---

## Manual Sync (Anytime)

Want to sync right now instead of waiting?

```bash
sync-now
```

That's it!

---

## How To See Your Data

**Option 1**: Open Google Sheet
- Go to: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`
- See all meals logged automatically

**Option 2**: Ask Claude
```
Open Claude Desktop and say:
"Show me my nutrition data from my Google Sheet today"
```

Claude can read your sheet and give you summaries!

---

## What Gets Logged

| You Say to Omi | What Appears in Sheet |
|----------------|----------------------|
| "I ate banana" | Banana \| 105 cal \| 1.3g protein |
| "Chicken shawarma for lunch" | Chicken shawarma \| 650 cal \| 45g protein |
| "2 chapatis with dal" | 2 chapatis \| 140 cal \| 6g protein<br>Dal \| 115 cal \| 9g protein |
| "My weight is 55.2 kg" | (can add weight tracking later) |

---

## Commands You'll Use

```bash
# Sync right now (manual)
sync-now

# Check if auto-sync is running
check-sync

# View what was logged today
view-logs
```

Super simple!

---

## No API Keys Needed!

**Other guides said**: "Get Gemini API key, configure this, set up that..."
**This guide says**: "Just use Claude Desktop that you're already paying for!"

The script sends Omi data to Claude Desktop, Claude analyzes it, and we log the results. Simple!

---

## Files in D:\MCP

```
D:\MCP\
├── SIMPLE_START.md          ← YOU ARE HERE (read this first!)
├── SIMPLE_SETUP.sh           ← Run this once to set up
├── sync-now.sh               ← Run anytime to sync manually
├── simple-omi-sync.py        ← The magic script (auto-runs every hour)
│
└── (Other guides if you want to go deeper later)
    ├── README_START_HERE.md
    ├── COMPLETE_AI_PRODUCTIVITY_SYSTEM.md
    └── ... etc
```

**Start here**, ignore the rest for now!

---

## Troubleshooting

### "Sync not working?"

Check Claude Desktop is running:
- Open Claude Desktop app
- It needs to be running for the script to use it

### "Nothing logged to sheet?"

```bash
# Test manually
sync-now

# Check logs
cat ~/.config/simple-sync.log
```

### "Don't see my Omi data?"

- Make sure you talked to Omi recently (last few hours)
- Omi needs 2-3 minutes to process audio → text
- Then sync will pick it up

---

## What's Next?

**Week 1**: Just let it run, check sheet occasionally
**Week 2**: Once you trust it, check the advanced guides in D:\MCP
**Week 3**: Add automations (Poke notifications, calendar sync, etc.)

But for now, **keep it simple!** Just this guide is enough.

---

## The Difference

**Complex guides** (old approach):
- Get Gemini API key ($$$)
- Install Python packages
- Configure systemd
- Set environment variables
- Debug API errors
- 😵 Too much!

**Simple guide** (this one):
- Use Claude Desktop (you already have it!)
- Run one setup script
- Talk to Omi
- Check Google Sheet
- ✅ Done!

---

## Ready?

1. Create Google Sheet (2 min)
2. Save Sheet ID to terminal (30 sec)
3. Run `./SIMPLE_SETUP.sh` (2 min)
4. Talk to Omi
5. Check sheet in 1 hour

**That's literally it!** No APIs, no complexity, no nonsense.

Let me know when you've created the Google Sheet and I'll help with the rest!
