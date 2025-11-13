#!/usr/bin/env python3
"""
CLAUDE CONVERSATION SYNC
------------------------
Monitor Claude conversations and sync food logs to Google Sheets.

How it works:
1. You send food photo to Claude mobile (in "Food Tracker" project)
2. Claude Desktop exports conversations periodically
3. This script monitors the export folder
4. Extracts food data from Claude's responses
5. Logs to Google Sheets

NO ZAPIER NEEDED - All local processing!

Author: Vibraneum
Date: November 2025
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

# Configuration
GOOGLE_CREDS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/home/ved/.config/google-credentials.json')
HEALTH_SHEET_ID = os.getenv('HEALTH_SHEET_ID')

# Claude Desktop stores conversations in ~/.config/Claude/
CLAUDE_CONVERSATIONS_PATH = os.path.expanduser("~/.config/Claude/conversations")
CHECK_INTERVAL = 30  # Check every 30 seconds

# Track processed messages to avoid duplicates
PROCESSED_FILE = os.path.expanduser("~/.config/health-coach-claude-processed.json")

def load_processed_messages():
    """Load set of already processed message IDs"""
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_processed_messages(processed_set):
    """Save processed message IDs"""
    with open(PROCESSED_FILE, 'w') as f:
        json.dump(list(processed_set), f)

def parse_claude_nutrition_response(text):
    """Extract nutrition info from Claude's response"""
    import re

    # Look for patterns like:
    # "FOOD: Chicken Biryani"
    # "CALORIES: 650 cal"
    # "PROTEIN: 35g protein"

    food_match = re.search(r'FOOD:\s*(.+?)(?:\n|$)', text, re.IGNORECASE)
    calories_match = re.search(r'CALORIES?:\s*(\d+)', text, re.IGNORECASE)
    protein_match = re.search(r'PROTEIN:\s*(\d+)', text, re.IGNORECASE)
    carbs_match = re.search(r'CARBS?:\s*(\d+)', text, re.IGNORECASE)
    fat_match = re.search(r'FAT:\s*(\d+)', text, re.IGNORECASE)
    portion_match = re.search(r'PORTION:\s*(.+?)(?:\n|$)', text, re.IGNORECASE)
    meal_match = re.search(r'MEAL:\s*(\w+)', text, re.IGNORECASE)

    if not calories_match:
        return None

    return {
        'name': food_match.group(1).strip() if food_match else 'Food',
        'portion_size': portion_match.group(1).strip() if portion_match else '1 serving',
        'calories': int(calories_match.group(1)),
        'protein_g': int(protein_match.group(1)) if protein_match else 20,
        'carbs_g': int(carbs_match.group(1)) if carbs_match else 40,
        'fat_g': int(fat_match.group(1)) if fat_match else 15,
        'meal_type': meal_match.group(1) if meal_match else 'snack'
    }

def scan_claude_conversations():
    """Scan Claude Desktop conversation files for new food logs"""

    print("\n🔍 Scanning Claude conversations...")

    if not os.path.exists(CLAUDE_CONVERSATIONS_PATH):
        print(f"⚠️  Claude conversations path not found: {CLAUDE_CONVERSATIONS_PATH}")
        print("\n💡 Alternative: Export conversations manually")
        print("   Settings → Export Data → Download conversations")
        return []

    processed = load_processed_messages()
    new_foods = []

    # Scan all conversation files
    for conv_file in Path(CLAUDE_CONVERSATIONS_PATH).glob("*.json"):
        try:
            with open(conv_file, 'r') as f:
                conv_data = json.load(f)

            # Check if this is the "Food Tracker" project
            project_name = conv_data.get('project_name', '')
            if 'food' not in project_name.lower():
                continue

            # Scan messages
            messages = conv_data.get('messages', [])

            for msg in messages:
                msg_id = msg.get('id')
                role = msg.get('role')
                content = msg.get('content', '')

                # Skip if already processed or not from assistant
                if msg_id in processed or role != 'assistant':
                    continue

                # Try to extract nutrition data
                food_data = parse_claude_nutrition_response(content)

                if food_data:
                    food_data['message_id'] = msg_id
                    food_data['timestamp'] = msg.get('timestamp', datetime.now().isoformat())
                    new_foods.append(food_data)
                    processed.add(msg_id)

        except Exception as e:
            print(f"⚠️  Error reading {conv_file.name}: {e}")

    save_processed_messages(processed)
    return new_foods

def log_to_sheets(food_data):
    """Log food to Google Sheets"""
    try:
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDS_PATH,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(HEALTH_SHEET_ID)
        meals_sheet = sheet.worksheet('Meals')

        # Add headers if empty
        if len(meals_sheet.get_all_values()) == 0:
            meals_sheet.append_row([
                'Timestamp', 'Food', 'Portion', 'Calories', 'Protein (g)',
                'Carbs (g)', 'Fat (g)', 'Meal Type', 'Source', 'Confidence'
            ])

        timestamp = datetime.fromisoformat(food_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

        row = [
            timestamp,
            food_data['name'],
            food_data['portion_size'],
            food_data['calories'],
            food_data['protein_g'],
            food_data['carbs_g'],
            food_data['fat_g'],
            food_data['meal_type'],
            'Claude Vision',
            'high'
        ]

        meals_sheet.append_row(row)
        print(f"✅ Logged: {food_data['name']} - {food_data['calories']} cal, {food_data['protein_g']}g protein")
        return True

    except Exception as e:
        print(f"❌ Failed to log to sheets: {e}")
        return False

def main():
    """Main monitoring loop"""
    print("🚀 Claude Conversation Sync")
    print("="*60)
    print(f"📊 Google Sheet: {HEALTH_SHEET_ID}")
    print(f"📁 Monitoring: {CLAUDE_CONVERSATIONS_PATH}")
    print(f"⏱️  Check interval: {CHECK_INTERVAL}s")
    print("="*60)

    if not os.path.exists(CLAUDE_CONVERSATIONS_PATH):
        print("\n⚠️  Claude Desktop conversations not found!")
        print("\n📋 MANUAL EXPORT METHOD:")
        print("1. Open Claude Desktop")
        print("2. Settings → Privacy → Export Data")
        print("3. Download ZIP file")
        print("4. Extract to ~/claude-exports/")
        print("5. Update CLAUDE_CONVERSATIONS_PATH in this script")
        print("\nOR use the Claude API version (requires API key)")
        return

    print("\n✅ Ready! Send food photos to Claude mobile...")
    print("📱 Make sure to use 'Food Tracker' project\n")

    while True:
        try:
            new_foods = scan_claude_conversations()

            for food in new_foods:
                log_to_sheets(food)

            if new_foods:
                print(f"\n🎉 Processed {len(new_foods)} new food log(s)")

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n👋 Stopping sync...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
