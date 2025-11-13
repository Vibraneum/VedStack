# 📧 Email Food Logger - Complete Guide

**The SIMPLEST way to track food with images!**

---

## 🎯 How It Works

1. **Take photo** of your food on phone
2. **Email it** with subject "FOOD" (or reply to food thread)
3. **Script auto-processes** every 2 minutes
4. **Data logs** to Google Sheets automatically

**That's it!** No apps, no manual entry, just email and forget!

---

## 🚀 Setup (5 Minutes)

### Step 1: Get Gmail App Password

1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (custom name)"
3. Name it: "Food Tracker"
4. Click "Generate"
5. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### Step 2: Add to .env File

```bash
cd /mnt/d/MCP/foodtracker
nano .env
```

Add these lines:
```bash
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_APP_PASSWORD=abcdefghijklmnop  # No spaces!
EMAIL_SUBJECT_FILTER=FOOD
```

Save and exit (Ctrl+X, Y, Enter)

### Step 3: Install Python Dependencies

```bash
pip install python-dotenv gspread google-auth
```

### Step 4: Run the Script

```bash
python3 email-food-logger.py
```

You should see:
```
🚀 Email Food Logger
============================================================
📧 Monitoring: your.email@gmail.com
⏱️  Check interval: 120s
📁 Images saved to: ~/food-photos/processed
============================================================

✅ Ready! Send food photos to your email...
```

---

## 📱 Daily Workflow

### Option 1: Subject Line (Easiest)

1. Take photo of food
2. Email to yourself
3. Subject: **FOOD** (or "FOOD - Lunch", "FOOD - Dinner", etc.)
4. Send!

Done! Script processes it automatically in <2 minutes.

### Option 2: Email Thread (Even Easier!)

1. First time: Email yourself with subject "FOOD"
2. Save that email as a conversation
3. From now on: Just **reply to that thread** with food photos
4. No need to type anything!

The script only processes emails with "FOOD" in the subject.

### Option 3: Add Description (Best Accuracy!)

Take photo, email with:
- Subject: FOOD
- Body: "Chicken biryani with raita, about 2 cups rice and 150g chicken"

The script will use BOTH the image AND your description for better calorie estimates!

---

## 🔧 Advanced Configuration

### Change Check Interval

Edit `email-food-logger.py`:
```python
CHECK_INTERVAL = 60  # Check every 1 minute instead of 2
```

### Use Different Subject Filter

In `.env`:
```bash
EMAIL_SUBJECT_FILTER=MEAL  # Now only processes emails with "MEAL" in subject
```

### Multiple Email Addresses

Create multiple scripts monitoring different emails:
- `email-food-logger-personal.py` → monitors personal@gmail.com
- `email-food-logger-shared.py` → monitors family@gmail.com

---

## 🎨 Email Templates

### Breakfast
```
Subject: FOOD - Breakfast
Photo: [attach image]
Body: Had this at 8am
```

### Lunch
```
Subject: FOOD - Lunch
Photo: [attach image]
Body: Office cafeteria meal
```

### Dinner
```
Subject: FOOD - Dinner
Photo: [attach image + attach image]
Body: Main course + dessert
```

### Snack
```
Subject: FOOD
Photo: [attach image]
Body: Quick snack between meals
```

---

## 📊 What Gets Logged

For each food email, the script logs to Google Sheets "Meals" tab:

| Timestamp | Food | Portion | Calories | Protein (g) | Carbs (g) | Fat (g) | Meal Type | Source | Confidence |
|-----------|------|---------|----------|-------------|-----------|---------|-----------|--------|------------|
| 2025-11-12 14:30 | Chicken Biryani | 2 cups | 650 | 35 | 85 | 18 | lunch | Email: IMG_1234.jpg | medium |
| 2025-11-12 14:30 | Raita | 1/2 cup | 80 | 4 | 8 | 4 | lunch | Email: IMG_1234.jpg | medium |

---

## 🤖 How Analysis Works

### With Image Only
- Script uses filename and common food patterns
- Estimates based on typical portions
- Confidence: Low-Medium

### With Image + Description
- Combines visual analysis with your text
- Much better calorie/macro estimates
- Confidence: Medium-High

### With Description Only (no image)
- Processes just the text you write
- Uses Claude to estimate nutrition
- Confidence: Medium

**Recommendation:** Always include a brief description with your photo for best accuracy!

---

## 🔍 Troubleshooting

### "Gmail connection failed"
- Check EMAIL_APP_PASSWORD is correct (no spaces)
- Verify app password is for "Mail" not "Omi"
- Try generating a new app password

### "No new emails"
- Make sure subject contains "FOOD"
- Check email is unread
- Verify you're sending to the correct email address

### "Could not extract food data"
- Add description to email body
- Make sure image is attached (not just pasted inline)
- Check image format (JPG, PNG supported)

### Script keeps crashing
- Check logs for error details
- Verify Google Sheets ID is correct
- Make sure service account has access to sheet

---

## 💡 Pro Tips

1. **Create a contact** named "Food Tracker" with your own email
   - Makes it easier to send to yourself

2. **Use voice-to-text** for descriptions
   - "Chicken biryani two cups" while looking at the food

3. **Batch send**
   - Take photos throughout the day
   - Email them all at once in evening

4. **Set up auto-forward**
   - Forward food photos from WhatsApp/Instagram to your email
   - Script processes them automatically

5. **Use Gmail labels**
   - Create label "Food Logged"
   - Script can auto-label processed emails

---

## 🔐 Privacy & Security

- **App Password** is NOT your Gmail password
  - It's a 16-character code specific to this app
  - You can revoke it anytime at myaccount.google.com

- **Images are local**
  - Stored in `~/food-photos/processed`
  - Never uploaded to cloud (except Google Sheets data)

- **Delete processed images**
  - Script moves to processed/ folder after logging
  - You can delete them anytime to save space

---

## 📅 Sample Week

**Monday**
- Breakfast: Email photo of oats + banana
- Lunch: Email photo of dal rice
- Snack: Email photo of protein shake
- Dinner: Email photo of chicken + veggies

**Result:** 4 emails → 4 automatic logs → Full day tracked!

**Tuesday**
- Just reply to Monday's email thread with today's photos
- Even easier!

---

## 🎯 Why This Method is PERFECT

✅ **No new app** - Just use email (you already have it)
✅ **Works from anywhere** - Phone, tablet, computer
✅ **No manual entry** - Take photo, send, done!
✅ **Automatic sync** - Script runs in background
✅ **Includes images** - Better accuracy than voice-only
✅ **Searchable history** - All in your Gmail
✅ **Zero cost** - No APIs needed

---

## 🚦 Running the Script

### Run Manually (for testing)
```bash
cd /mnt/d/MCP/foodtracker
python3 email-food-logger.py
```

### Run in Background
```bash
cd /mnt/d/MCP/foodtracker
nohup python3 email-food-logger.py > email-logger.log 2>&1 &
```

### Auto-start on PC Boot
```bash
cd /mnt/d/MCP/foodtracker
./setup-email-logger.sh  # Creates systemd service
```

---

## 📞 Support

**Issues?**
1. Check logs: `tail -f email-logger.log`
2. Verify .env settings
3. Test Gmail connection manually

**Questions?**
- Email filtering not working → Check subject line spelling
- Images not downloading → Check file size (Gmail limit: 25MB)
- Analysis failing → Add text description to help

---

## 🎉 You're Ready!

**Next steps:**
1. Generate Gmail app password
2. Add to .env file
3. Run script
4. Email yourself a food photo with subject "FOOD"
5. Watch it appear in Google Sheets! 📊

**That's it! Enjoy automatic food tracking!** 🚀

---

**Created:** November 2025
**For:** Vedanth's 8-week bulk (54.9kg → 60kg)
**Goal:** 3,000 cal/day, 130g protein
