#!/usr/bin/env python3
"""
PHONE-FRIENDLY Food Tracker
----------------------------
NO Claude Desktop needed!
NO API keys needed!
Just Omi + Google Sheets!

Works great from phone - script runs on PC in background
"""

import os
import json
import requests
from datetime import datetime
import csv

# Config
OMI_API_KEY = 'omi_dev_2b7983a707b5ede131a0903a1655d918'
SHEET_ID = os.getenv('HEALTH_SHEET_ID', 'YOUR_SHEET_ID')
STATE_FILE = os.path.expanduser('~/.config/phone-food-state.json')
POKE_API_KEY = os.getenv('POKE_API_KEY', 'pk_GH6UrWQ1JCpPzmsYTAX0LzNfGKn_TTQDquPUpAOujWM')
POKE_ENABLED = os.getenv('POKE_ENABLED', 'false').lower() == 'true'

# Simple food database - NO AI NEEDED!
FOODS = {
    'chicken shawarma': (650, 45, 52, 28), 'shawarma': (650, 45, 52, 28),
    'dal': (115, 9, 20, 0.4), 'chapati': (70, 3, 15, 0.4), 'roti': (70, 3, 15, 0.4),
    'rice': (200, 4, 45, 0.4), 'paneer': (265, 18, 3, 20),
    'chicken curry': (250, 25, 10, 12), 'biryani': (450, 20, 60, 15),
    'paratha': (150, 4, 20, 6), 'idli': (39, 2, 8, 0.3), 'dosa': (133, 4, 22, 3),
    'samosa': (262, 5, 24, 17), 'oats': (150, 5, 27, 3), 'banana': (105, 1.3, 27, 0.4),
    'eggs': (70, 6, 0.6, 5), 'egg': (70, 6, 0.6, 5), 'milk': (150, 8, 12, 8),
    'bread': (80, 3, 15, 1), 'peanut butter': (190, 8, 7, 16),
    'chicken breast': (165, 31, 0, 3.6), 'protein shake': (120, 24, 3, 1),
    'whey protein': (120, 24, 3, 1), 'biscuit': (50, 1, 8, 2), 'biscuits': (50, 1, 8, 2),
    'chips': (160, 2, 15, 10), 'chocolate': (210, 3, 24, 12)
}

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {'processed': []}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def get_omi_memories():
    try:
        r = requests.get(
            'https://api.omi.me/v1/dev/user/memories?limit=50',
            headers={'Authorization': f'Bearer {OMI_API_KEY}'},
            timeout=10
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log(f"❌ Error getting Omi data: {e}")
        return []

def detect_food(text):
    keywords = ['eat', 'ate', 'food', 'meal', 'breakfast', 'lunch', 'dinner', 'snack', 'had', 'having']
    t = text.lower()
    return any(k in t for k in keywords) or any(f in t for f in FOODS.keys())

def parse_food(text):
    import re
    results = []
    t = text.lower()

    for food, (cal, pro, carb, fat) in FOODS.items():
        if food in t:
            # Detect quantity
            match = re.search(rf'(\d+)\s*{re.escape(food)}', t)
            qty = int(match.group(1)) if match else 1

            results.append({
                'food': food,
                'cal': cal * qty,
                'pro': pro * qty,
                'carb': carb * qty,
                'fat': fat * qty
            })

    # If no match, use default estimate
    if not results and detect_food(text):
        results.append({'food': text[:30], 'cal': 400, 'pro': 20, 'carb': 40, 'fat': 15, 'est': True})

    return results

def append_to_sheet(data):
    """Append to Google Sheet via simple CSV export"""
    csv_file = os.path.expanduser('~/.config/food-log.csv')

    # Append to local CSV
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d'),
            datetime.now().strftime('%H:%M:%S'),
            data['food'],
            round(data['cal']),
            round(data['pro'], 1),
            round(data['carb'], 1),
            round(data['fat'], 1)
        ])

    log(f"  ✅ Logged: {data['food']} - {round(data['cal'])} cal, {round(data['pro'], 1)}g protein")

    # TODO: Upload CSV to Google Sheets
    # For now, manual: Import -> Upload -> Replace

    return True

def send_poke_notification(msg):
    """Send notification to Poke device"""
    if not POKE_ENABLED:
        return

    try:
        requests.post(
            'https://poke.com/api/v1/inbound-sms/webhook',
            headers={'Authorization': f'Bearer {POKE_API_KEY}'},
            json={'message': msg},
            timeout=5
        )
        log(f"  📳 Poke notified")
    except:
        pass

def sync():
    log("\n" + "="*50)
    log("🚀 Food Sync Starting")
    log("="*50)

    state = load_state()
    memories = get_omi_memories()
    log(f"📥 Found {len(memories)} Omi memories")

    new_count = 0

    for mem in memories:
        if mem['id'] in state['processed']:
            continue

        text = mem['content']

        if not detect_food(text):
            state['processed'].append(mem['id'])
            continue

        log(f"\n📝 Processing: {text[:60]}...")

        foods = parse_food(text)

        for food in foods:
            append_to_sheet(food)
            new_count += 1

            # Poke notification
            if POKE_ENABLED:
                msg = f"Logged: {food['food']} - {round(food['cal'])} cal, {round(food['pro'], 1)}g protein ✅"
                send_poke_notification(msg)

        state['processed'].append(mem['id'])

    state['processed'] = state['processed'][-1000:]  # Keep last 1000
    save_state(state)

    log("\n" + "="*50)
    log(f"✅ Done! Logged {new_count} items")
    log("="*50 + "\n")

if __name__ == '__main__':
    sync()
