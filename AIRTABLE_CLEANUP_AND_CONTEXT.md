# VedStack Airtable - Data Cleanup & Knowledge Base Enhancement

**Date**: November 13, 2025
**Purpose**: Remove fake data and enhance Airtable as knowledge base for Claude

---

## 🗑️ DATA TO DELETE (Fake/Sample Data)

### Food Log Table
**DELETE these 4 sample entries:**
- Sample oatmeal breakfast entry
- Sample chicken biryani lunch entry
- Sample protein shake snack entry
- Sample salmon dinner entry

**Action**: Open Food Log table in Airtable and delete all records (they were added for demonstration only).

### Workouts Table
**DELETE these 4 sample entries:**
- Sample leg day workout
- Sample physiotherapy session
- Sample upper body workout
- Sample FIFA playing session

**Action**: Open Workouts table and delete all records.

### Daily Vitals Table
**DELETE these 3 sample entries:**
- Sample sleep/energy entries with fabricated data

**Action**: Open Daily Vitals table and delete all records.

### Weekly Summary Table
**DELETE this 1 sample entry:**
- Week 0 sample summary

**Action**: Open Weekly Summary table and delete the record.

---

## ✅ DATA TO KEEP (Real Data Only)

### User Profile Table - ALL 19 FIELDS (KEEP AS IS)
1. Name: Vedanth
2. Age: 20 years old
3. Height: 167 cm (5'5.7")
4. Start Weight: 54.9 kg
5. Target Weight: 60 kg in 8 weeks
6. Weekly Target: +0.6 kg/week
7. InBody Score: 74/100 (Oct 2025)
8. Body Fat: 7.8 kg (14.3%)
9. Muscle Mass: 26.2 kg → Target: 30 kg
10. Focus Area: Legs (96%), Arms (104-107%)
11. Daily Calories: 3,000 cal (TDEE: 2,460 + 500 surplus)
12. Daily Protein: 130g (2.4g/kg target)
13. Daily Carbs: 400g
14. Daily Fat: 75g
15. Training: 6x/week (focus on legs)
16. Start Date: October 24, 2025
17. Goal Style: Bryan Johnson longevity + aggressive bulk
18. Category field (for organization)
19. Last Updated (timestamp)

### Body Metrics Table - 1 RECORD (KEEP AS IS)
- **Date**: October 24, 2025, 9:00 AM
- **Weight**: 54.9 kg
- **Body Fat %**: 14.3%
- **Muscle Mass**: 26.2 kg
- **Notes**: "InBody scan baseline - Score: 74/100. Upper body strong (104-107%), legs lagging (95-96%)"

---

## 📚 CONTEXT TO ADD (Knowledge Base Enhancement)

To make Airtable serve as a comprehensive knowledge base for Claude Desktop, add the following REAL context:

### 1. Add to User Profile Table (New Category: "Context")

**Field Name**: "Background & Goals"
**Value**:
```
Vedanth is a 20-year-old pursuing an 8-week aggressive bulk program inspired by Bryan Johnson's Blueprint longevity approach. Starting from 54.9kg (Oct 24, 2025), targeting 60kg by Dec 19, 2025. Focus on legs which lag behind upper body development (96% vs 104-107% per InBody scan). Using photo-based food tracking via Claude Desktop + Airtable MCP integration for precise macro tracking.
```

**Field Name**: "Nutrition Philosophy"
**Value**:
```
Daily targets: 3,000 cal (TDEE 2,460 + 500 surplus), 130g protein (2.4g/kg), 400g carbs, 75g fat. Prioritizing whole foods, consistent meal timing, and accurate tracking. Bryan Johnson-inspired approach: data-driven decisions, comprehensive tracking, optimization mindset.
```

**Field Name**: "Training Context"
**Value**:
```
6x/week training split with emphasis on leg development to balance upper/lower body ratio. InBody scan shows upper body at 104-107% of standard, legs at 95-96%. Goal: Add 3.8kg muscle mass (26.2kg → 30kg) while maintaining low body fat percentage.
```

**Field Name**: "Measurement Protocol"
**Value**:
```
Weekly weigh-ins: Same time each week, empty stomach, after bathroom, before eating/drinking. InBody scans: Baseline Oct 24, 2025 (Score: 74/100), next scan at Week 4 (mid-November), final scan at Week 8 (Dec 19). Daily tracking: All meals via photo analysis, workouts logged immediately post-gym, vitals tracked morning and evening.
```

**Field Name**: "Success Metrics"
**Value**:
```
Primary: +0.6kg/week weight gain (5.1kg total over 8 weeks). Secondary: Muscle mass 26.2kg → 30kg (+3.8kg). Body fat maintenance: Keep at or below 14.3%. InBody score improvement: 74 → 80+. Leg development: 95-96% → 100%+ per InBody segmental analysis. Consistency: Hit 3,000 cal and 130g protein 6+ days per week.
```

### 2. Create New Table: "System Context"

**Purpose**: Store operational context for Claude to understand the entire system.

**Fields:**
- Context Type (single select): Workflow, Integration, Technical, Historical
- Title (short text)
- Description (long text)
- Date Added (date)
- Relevance (single select): High, Medium, Low

**Records to Add:**

**Record 1:**
- **Context Type**: Workflow
- **Title**: "Photo-to-Database Food Logging"
- **Description**: "User takes food photo in Claude Desktop → Claude analyzes image (identifies food items, estimates portions, calculates macros) → Writes directly to Food Log table via Airtable MCP. No manual data entry required. Claude has context from User Profile to make informed estimates."
- **Relevance**: High

**Record 2:**
- **Context Type**: Integration
- **Title**: "Airtable MCP Configuration"
- **Description**: "Claude Desktop configured with @modelcontextprotocol/server-airtable NPM package. PAT: pat2KeRGsd2jGmNop... (read/write permissions). Base ID: appSgD8XmiKRBrGXd. 7 tables created: Food Log, User Profile, Body Metrics, Workouts, Daily Vitals, Supplements, Weekly Summary."
- **Relevance**: High

**Record 3:**
- **Context Type**: Technical
- **Title**: "InBody Scan Interpretation"
- **Description**: "InBody score 74/100 (good, room for improvement). Segmental lean mass analysis shows upper body 104-107% (above standard), legs 95-96% (below standard). Body fat 14.3% (7.8kg) is healthy for bulk. Skeletal muscle mass 26.2kg is baseline. Target: +3.8kg muscle, maintain/reduce BF%."
- **Relevance**: High

**Record 4:**
- **Context Type**: Historical
- **Title**: "System Evolution"
- **Description**: "Started with Omi voice + Google Sheets approach. Google Sheets MCP didn't work reliably. Pivoted to Airtable MCP (Nov 13, 2025) which works perfectly. SQLite option exists but Airtable preferred for visual dashboard and mobile app. All sample data removed per user request - only real data tracked."
- **Relevance**: Medium

**Record 5:**
- **Context Type**: Workflow
- **Title**: "Daily Routine"
- **Description**: "Morning: Log breakfast via photo, check Weekly Summary for progress. Throughout day: Photo each meal/snack immediately, track in real-time. Evening: Log workout (if gym day), log Daily Vitals (sleep from previous night, energy level today). Before bed: Review total macros, adjust next day if needed. Sunday: Weigh-in, log to Body Metrics, create Weekly Summary entry."
- **Relevance**: High

### 3. Create New Table: "Macro Calculation Rules"

**Purpose**: Help Claude make accurate food analysis from photos.

**Fields:**
- Food Category (single select): Protein Source, Carb Source, Fat Source, Mixed Dish, Beverage, Snack
- Food Item (short text)
- Typical Portion (short text)
- Calories per Portion (number)
- Protein per Portion (number, 1 decimal)
- Carbs per Portion (number, 1 decimal)
- Fat per Portion (number, 1 decimal)
- Notes (long text)

**Records to Add (Based on Common Indian Foods):**

**Protein Sources:**
1. Chicken Breast (100g): 165 cal, 31g protein, 0g carbs, 3.6g fat
2. Eggs (1 large): 70 cal, 6g protein, 0.6g carbs, 5g fat
3. Paneer (100g): 265 cal, 18g protein, 3.6g carbs, 20g fat
4. Dal (1 cup): 230 cal, 18g protein, 40g carbs, 0.8g fat
5. Whey Protein (1 scoop): 120 cal, 24g protein, 3g carbs, 1.5g fat

**Carb Sources:**
1. Rice (1 cup cooked): 205 cal, 4.2g protein, 45g carbs, 0.4g fat
2. Roti/Chapati (1 medium): 71 cal, 3g protein, 15g carbs, 0.4g fat
3. Oats (1 cup cooked): 166 cal, 5.9g protein, 28g carbs, 3.6g fat
4. Banana (1 medium): 105 cal, 1.3g protein, 27g carbs, 0.4g fat

**Mixed Dishes:**
1. Chicken Biryani (1 plate ~300g): 450 cal, 25g protein, 55g carbs, 12g fat
2. Chole (1 cup): 270 cal, 14g protein, 45g carbs, 4g fat

**Beverages:**
1. Whole Milk (1 cup): 150 cal, 8g protein, 12g carbs, 8g fat
2. Chai with milk/sugar (1 cup): 80 cal, 3g protein, 12g carbs, 2g fat

(Add more as Vedanth logs actual foods)

### 4. Add to Body Metrics Table (Context Field)

Add a new field: **"Scan Context" (long text)**

For the existing Oct 24 baseline record, add:
```
First InBody scan. Score 74/100 indicates good foundation but room for improvement. Key findings:
- Skeletal muscle mass 26.2kg (should reach 30kg by Week 8)
- Body fat 14.3% (7.8kg absolute) - healthy for bulk phase
- Segmental analysis: Upper body exceeds standard (104-107%), legs below standard (95-96%)
- Strategy: High-volume leg training 2-3x/week, maintain upper body 2x/week
- Protein visceral fat level normal, body water balance good
- Baseline established for 8-week tracking period
```

---

## 🎯 HOW CLAUDE DESKTOP WILL USE THIS

When you ask Claude Desktop to log a food photo:

1. **Claude reads User Profile** → Knows you need 3,000 cal, 130g protein daily
2. **Claude reads Macro Calculation Rules** → Has reference data for accurate estimates
3. **Claude reads System Context** → Understands the workflow and your goals
4. **Claude analyzes photo** → Identifies food items, estimates portions
5. **Claude calculates macros** → Uses reference data + visual analysis
6. **Claude writes to Food Log** → Logs meal with timestamp and macros
7. **Claude can check daily totals** → Reads Food Log, tells you progress toward daily targets

When you ask for progress updates:

1. **Claude reads Body Metrics** → Knows baseline and any weigh-ins
2. **Claude reads Weekly Summary** → Understands weekly trends
3. **Claude reads System Context** → Knows your success metrics
4. **Claude calculates progress** → Compares current vs target
5. **Claude provides insights** → Personalized recommendations based on data

---

## 📱 NEXT STEPS FOR YOU

### Step 1: Clean Up Fake Data (5 minutes)
1. Open https://airtable.com/appSgD8XmiKRBrGXd
2. Go to Food Log → Delete all records
3. Go to Workouts → Delete all records
4. Go to Daily Vitals → Delete all records
5. Go to Weekly Summary → Delete all records
6. Keep User Profile (19 fields) and Body Metrics (1 baseline) as is

### Step 2: Add Context to User Profile (10 minutes)
Add the 5 new context fields listed above in Section 1

### Step 3: Create System Context Table (15 minutes)
Create new table with 5 records as specified in Section 2

### Step 4: Create Macro Calculation Rules Table (20 minutes)
Create new table with initial food reference data in Section 3

### Step 5: Enhance Body Metrics (5 minutes)
Add "Scan Context" field and populate the baseline entry as shown in Section 4

### Step 6: Test with Claude Desktop
1. Restart Claude Desktop to load updated Airtable data
2. Take a food photo
3. Say: "Log this food to my tracker"
4. Verify Claude uses the context and reference data for accurate logging

---

## ✅ EXPECTED OUTCOME

After cleanup and context enhancement:

**Airtable will contain:**
- ✅ ONLY real data (User Profile baseline, InBody scan Oct 24)
- ✅ Comprehensive context for Claude to understand your goals
- ✅ Reference data for accurate food analysis
- ✅ System documentation for consistent behavior
- ✅ No fake/sample entries

**Claude Desktop will be able to:**
- ✅ Analyze food photos with context-aware accuracy
- ✅ Log meals with proper macro calculations
- ✅ Provide progress insights based on your specific goals
- ✅ Make recommendations aligned with Bryan Johnson philosophy
- ✅ Track your 8-week bulk systematically

---

**Created**: November 13, 2025
**Purpose**: Clean fake data, add real context for knowledge base
**Status**: Ready for user execution
