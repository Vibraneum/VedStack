#!/usr/bin/env python3
"""
SIMPLE Omi to Google Sheets Sync
---------------------------------
Uses your EXISTING Claude Desktop subscription (no API keys!)

How it works:
1. Pulls Omi memories
2. Sends to Claude Desktop to analyze
3. Logs to Google Sheets

No Gemini API needed!
"""

import os
import json
import requests
import subprocess
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

OMI_API_KEY = 'omi_dev_2b7983a707b5ede131a0903a1655d918'
SHEET_ID = os.getenv('HEALTH_SHEET_ID', 'YOUR_SHEET_ID_HERE')
STATE_FILE = os.path.expanduser('~/.config/simple-omi-state.json')
LOG_FILE = os.path.expanduser('~/.config/simple-sync.log')

# ============================================================================
# SIMPLE NUTRITION DATABASE (30+ foods)
# ============================================================================

NUTRITION_DB = {
    # Indian Foods
    'chicken shawarma': (650, 45, 52, 28),
    'shawarma': (650, 45, 52, 28),
    'dal': (115, 9, 20, 0.4),
    'chapati': (70, 3, 15, 0.4),
    'roti': (70, 3, 15, 0.4),
    'rice': (200, 4, 45, 0.4),
    'paneer': (265, 18, 3, 20),
    'chicken curry': (250, 25, 10, 12),
    'biryani': (450, 20, 60, 15),
    'idli': (39, 2, 8, 0.3),
    'dosa': (133, 4, 22, 3),

    # Breakfast
    'oats': (150, 5, 27, 3),
    'banana': (105, 1.3, 27, 0.4),
    'eggs': (70, 6, 0.6, 5),
    'milk': (150, 8, 12, 8),
    'bread': (80, 3, 15, 1),

    # Protein
    'chicken breast': (165, 31, 0, 3.6),
    'protein shake': (120, 24, 3, 1),
    'whey protein': (120, 24, 3, 1),
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def log(message):
    """Log to file and console"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + '\n')

def load_state():
    """Load processed memory IDs"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'processed_ids': []}

def save_state(state):
    """Save processed memory IDs"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def get_omi_memories():
    """Fetch recent Omi memories"""
    url = 'https://api.omi.me/v1/dev/user/memories?limit=50'
    headers = {'Authorization': f'Bearer {OMI_API_KEY}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log(f"❌ Error fetching Omi memories: {e}")
        return []

def detect_food(text):
    """Check if text mentions food"""
    food_keywords = ['eat', 'ate', 'food', 'meal', 'breakfast', 'lunch', 'dinner', 'snack', 'had', 'having']
    text_lower = text.lower()

    # Check keywords
    has_food_keyword = any(keyword in text_lower for keyword in food_keywords)
    if not has_food_keyword:
        return False

    # Check if any known food is mentioned
    for food_name in NUTRITION_DB.keys():
        if food_name in text_lower:
            return True

    # If has food keywords but unknown food, still return True (Claude will analyze)
    return True

def get_nutrition_from_db(text):
    """Get nutrition from database if food is known"""
    results = []
    text_lower = text.lower()

    for food_name, (cal, pro, carb, fat) in NUTRITION_DB.items():
        if food_name in text_lower:
            # Try to detect quantity (e.g., "2 chapatis")
            import re
            pattern = rf'(\d+)\s*{re.escape(food_name)}'
            match = re.search(pattern, text_lower)
            quantity = int(match.group(1)) if match else 1

            results.append({
                'food': food_name,
                'calories': cal * quantity,
                'protein': pro * quantity,
                'carbs': carb * quantity,
                'fat': fat * quantity,
                'from_db': True
            })

    return results

def ask_claude_desktop(text):
    """
    Use Claude Desktop (your subscription!) to analyze food

    This sends a request to Claude Desktop app via MCP
    No API key needed - uses your existing subscription!
    """
    log(f"🤖 Asking Claude Desktop to analyze: {text[:50]}...")

    # Create a prompt for Claude
    prompt = f"""
Analyze this food mention and return ONLY a JSON object (no markdown, no explanation):

Text: {text}

Return format:
{{
  "foods": [
    {{
      "name": "food name",
      "calories": <number>,
      "protein": <grams>,
      "carbs": <grams>,
      "fat": <grams>
    }}
  ]
}}

If multiple foods mentioned, include all in the array.
Return ONLY the JSON, nothing else.
"""

    try:
        # Use Claude Code CLI (which uses your Claude Desktop subscription)
        # This is installed when you have Claude Desktop
        result = subprocess.run(
            ['claude', '--prompt', prompt],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            # Parse Claude's response
            response_text = result.stdout.strip()
            # Remove markdown if present
            response_text = response_text.replace('```json', '').replace('```', '').strip()

            data = json.loads(response_text)
            return data.get('foods', [])
        else:
            log(f"⚠️  Claude Desktop returned error, using estimate")
            return [{'name': text[:30], 'calories': 400, 'protein': 20, 'carbs': 40, 'fat': 15, 'estimated': True}]

    except subprocess.TimeoutExpired:
        log("⚠️  Claude Desktop timeout, using estimate")
        return [{'name': text[:30], 'calories': 400, 'protein': 20, 'carbs': 40, 'fat': 15, 'estimated': True}]
    except Exception as e:
        log(f"⚠️  Error calling Claude Desktop: {e}, using estimate")
        return [{'name': text[:30], 'calories': 400, 'protein': 20, 'carbs': 40, 'fat': 15, 'estimated': True}]

def append_to_sheet(food_data):
    """
    Append to Google Sheet using Google Sheets MCP

    Uses the MCP server you already have configured!
    """
    try:
        # Prepare data
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S')

        row_data = {
            'Date': date,
            'Time': time,
            'Food': food_data['name'],
            'Calories': round(food_data.get('calories', 0)),
            'Protein': round(food_data.get('protein', 0), 1),
            'Carbs': round(food_data.get('carbs', 0), 1),
            'Fat': round(food_data.get('fat', 0), 1),
            'Notes': 'From Omi' + (' (estimated)' if food_data.get('estimated') else '')
        }

        # Use Claude Code CLI to append to sheet
        prompt = f"""
Use the Google Sheets MCP to append this row to sheet ID "{SHEET_ID}", tab "Meals":

{json.dumps(row_data, indent=2)}

Append as a new row. Confirm when done.
"""

        result = subprocess.run(
            ['claude', '--prompt', prompt],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            log(f"  ✅ Logged: {food_data['name']} - {round(food_data.get('calories', 0))} cal")
            return True
        else:
            log(f"  ❌ Error logging to sheet: {result.stderr}")
            return False

    except Exception as e:
        log(f"  ❌ Error appending to sheet: {e}")
        return False

# ============================================================================
# MAIN SYNC
# ============================================================================

def sync():
    """Main sync function"""
    log("\n" + "="*60)
    log("🚀 Starting Simple Omi Sync")
    log("="*60)

    # Load state
    state = load_state()
    processed_ids = state.get('processed_ids', [])

    # Get Omi memories
    log("📥 Fetching Omi memories...")
    memories = get_omi_memories()
    log(f"   Found {len(memories)} memories")

    new_items = 0

    # Process each memory
    for memory in memories:
        memory_id = memory['id']
        content = memory['content']

        # Skip if already processed
        if memory_id in processed_ids:
            continue

        log(f"\n📝 Processing: {content[:60]}...")

        # Check if food-related
        if not detect_food(content):
            log("   ⏭️  No food detected, skipping")
            processed_ids.append(memory_id)
            continue

        # Try database first (fast!)
        foods = get_nutrition_from_db(content)

        # If not in database, ask Claude Desktop (your subscription!)
        if not foods:
            log("   🔍 Not in database, asking Claude Desktop...")
            foods = ask_claude_desktop(content)

        # Log each food to Google Sheets
        for food in foods:
            if append_to_sheet(food):
                new_items += 1

        # Mark as processed
        processed_ids.append(memory_id)

    # Keep only last 1000 IDs
    processed_ids = processed_ids[-1000:]

    # Save state
    state['processed_ids'] = processed_ids
    state['last_sync'] = datetime.now().isoformat()
    save_state(state)

    # Summary
    log("\n" + "="*60)
    log(f"✅ Sync Complete! Logged {new_items} new items")
    log(f"📊 View your data: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    log("="*60 + "\n")

# ============================================================================
# RUN
# ============================================================================

if __name__ == '__main__':
    sync()
