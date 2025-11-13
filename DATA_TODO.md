# 📋 Data to Collect & Add Later

**Created:** November 12, 2025
**Status:** Optional baseline data for better tracking

---

## 🏋️ Strength Levels (Current)

Get these from gym:

### Primary Lifts
- [ ] **Bench Press:** ___ kg (1RM or working weight for 5 reps)
- [ ] **Deadlift:** ___ kg (1RM or working weight for 5 reps)
- [ ] **Squat:** ___ kg (1RM or working weight for 5 reps)
- [ ] **Overhead Press:** ___ kg (optional)
- [ ] **Barbell Row:** ___ kg (optional)

**Why:** Track strength progress alongside weight gain

**How to tell Omi:**
```
"Benched 75kg for 5 reps today"
"Deadlifted 120kg, new PR"
"Working weight for squat is 90kg"
```

---

## ❤️ Vitals (Baseline)

Get from smart watch/fitness tracker/manual:

### Daily Metrics
- [ ] **Resting Heart Rate:** ___ bpm (measure first thing in morning)
- [ ] **HRV (Heart Rate Variability):** ___ ms (from tracker)
- [ ] **Sleep Score:** ___/100 (from tracker)
- [ ] **Average Daily Steps:** ___

**Why:** Detect overtraining, track recovery

**How to tell Omi:**
```
"Morning stats: resting heart rate 58 bpm"
"HRV today was 65 milliseconds"
"Sleep score last night was 85"
```

---

## 🩸 Blood Work (Optional)

Get from doctor or at-home test kit:

### Hormone Panel
- [ ] **Testosterone:** ___ ng/dL (optimal: 500-900 for males 20yo)
- [ ] **Free Testosterone:** ___ pg/mL
- [ ] **Estradiol:** ___ pg/mL
- [ ] **Cortisol:** ___ mcg/dL

### Health Markers
- [ ] **Vitamin D:** ___ ng/mL (optimal: 40-60)
- [ ] **Vitamin B12:** ___ pg/mL (optimal: >400)
- [ ] **Iron/Ferritin:** ___ ng/mL
- [ ] **Fasting Glucose:** ___ mg/dL (optimal: <100)
- [ ] **HbA1c:** ___% (optimal: <5.7)

### Lipid Panel
- [ ] **Total Cholesterol:** ___ mg/dL
- [ ] **LDL Cholesterol:** ___ mg/dL (optimal: <100)
- [ ] **HDL Cholesterol:** ___ mg/dL (optimal: >40)
- [ ] **Triglycerides:** ___ mg/dL (optimal: <150)

### Inflammation
- [ ] **CRP (C-Reactive Protein):** ___ mg/L (optimal: <1)

**Why:** Baseline for health optimization, detect deficiencies

**When:** Get tested before starting (baseline), then 3-6 months

**How to tell Omi:**
```
"Blood work results: testosterone 620, vitamin D 45, glucose 88"
"Got lab results: LDL 95, HDL 55, CRP 0.8"
```

---

## 📏 Body Measurements (Weekly)

Measure with tape measure:

### Key Measurements
- [ ] **Chest:** ___ cm (at nipple line, relaxed)
- [ ] **Arms:** ___ cm (flexed, at peak)
- [ ] **Waist:** ___ cm (at belly button)
- [ ] **Hips:** ___ cm
- [ ] **Thighs:** ___ cm (midpoint)
- [ ] **Calves:** ___ cm (widest point)
- [ ] **Neck:** ___ cm

**Why:** Track where you're gaining (muscle vs fat)

**When:** Every Sunday morning

**How to tell Omi:**
```
"Weekly measurements: chest 92cm, arms 32cm, waist 75cm"
"Measured today: thighs 52cm, calves 36cm"
```

---

## 🏃 Cardio/Activity (Optional)

### Fitness Tests
- [ ] **VO2 Max:** ___ ml/kg/min (from smart watch estimate)
- [ ] **Mile Time:** ___ minutes
- [ ] **Max Push-ups:** ___
- [ ] **Max Pull-ups:** ___
- [ ] **Plank Hold:** ___ seconds

**Why:** Track overall fitness, not just strength

**How to tell Omi:**
```
"Fitness test: did 45 push-ups, 8 pull-ups, held plank 90 seconds"
"VO2 max estimate from watch: 42 ml/kg/min"
```

---

## 🧘 Recovery Metrics (Optional)

### Track These Daily
- [ ] **Grip Strength:** ___ kg (left/right, use dynamometer)
- [ ] **Morning Temperature:** ___ °C
- [ ] **Morning Weight:** ___ kg (track daily variation)
- [ ] **Stress Level:** ___/10
- [ ] **Libido:** ___/10 (testosterone indicator)

**Why:** Detect overtraining, hormonal issues

**How to tell Omi:**
```
"Morning: weight 55.2kg, temp 36.8°C, grip 42kg left 45kg right"
"Stress today is 3 out of 10, feeling good"
```

---

## 📊 How to Add This Data

### Option 1: Tell Omi (Best)
Just talk naturally:
```
"Benched 75kg today"
"Resting heart rate this morning was 58"
"Blood work: vitamin D is 45"
```

Claude extracts and logs automatically.

### Option 2: Add to Script Manually

Edit `dead-simple-health-coach.py`:
```python
USER_PROFILE = {
    # ... existing data ...

    # Add your numbers here:
    'bench_press_kg': 75,
    'deadlift_kg': 120,
    'squat_kg': 90,
    'resting_hr': 58,
    'hrv_ms': 65,
    'testosterone_ng_dl': 620,
    'vitamin_d_ng_ml': 45,
}
```

Then restart: `health-restart`

### Option 3: Add to Google Sheets

Manually enter in appropriate tab.

---

## 🎯 Priority Order

### Must Have (Week 1)
1. ✅ Weight (you have: 54.9kg)
2. ✅ Height (you have: 167cm)
3. ✅ Age (you have: 20)
4. ✅ InBody data (you have)
5. ✅ Goal weight (60kg)

### Should Have (Week 1-2)
1. [ ] Resting heart rate
2. [ ] Current strength levels (bench/deadlift/squat)
3. [ ] Body measurements (chest/arms/waist)
4. [ ] Sleep quality baseline

### Nice to Have (Month 1)
1. [ ] HRV tracking
2. [ ] Vitamin D level
3. [ ] VO2 max estimate
4. [ ] Testosterone baseline

### Advanced (Month 2-3)
1. [ ] Full blood panel
2. [ ] Grip strength
3. [ ] Body temperature
4. [ ] Full lipid panel

---

## 📅 Reminder Schedule

**Week 1:** Get strength numbers + RHR + measurements
**Week 4:** Mid-bulk check-in, remeasure everything
**Week 8:** Final measurements + InBody scan
**Month 3:** Blood work follow-up

---

## ✅ When You Have Data

**Just tell Omi or message me:**
```
"Got my strength numbers:
Bench 75kg
Deadlift 120kg
Squat 90kg
Resting HR 58 bpm"
```

**I'll update the script immediately.**

---

## 💡 Why This Matters

**Complete data = better coaching:**
- Claude can give specific strength goals
- Detect overtraining before injury
- Optimize recovery strategies
- Track health biomarkers
- Prove your bulk is working (muscle, not just fat)

**But it's ALL optional. Core system works without it.**

---

**Save this file. Check back when you have data.** ✅

**For now: Just start talking to Omi about food/gym/sleep!** 🚀
