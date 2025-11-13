#!/usr/bin/env python3
"""
IMAGE FOOD LOGGER (Claude Desktop Version)
-------------------------------------------
Drop food photos in a folder, script analyzes them with Claude Desktop CLI.

Workflow:
1. Take photo on phone
2. Send to PC via WhatsApp/Google Photos/Email
3. Save to: ~/food-photos/
4. Script auto-processes and logs to Google Sheets

Uses: Claude Desktop (your subscription) - NO API costs!

Author: Built for Vedanth
Date: November 2025
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

# Configuration
WATCH_FOLDER = os.path.expanduser("~/food-photos")
PROCESSED_FOLDER = os.path.expanduser("~/food-photos/processed")
GOOGLE_CREDS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/home/ved/.config/google-credentials.json')
HEALTH_SHEET_ID = os.getenv('HEALTH_SHEET_ID')

# Create folders if they don't exist
os.makedirs(WATCH_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

print(f"📁 Watching folder: {WATCH_FOLDER}")
print(f"💾 Processed files move to: {PROCESSED_FOLDER}")

def analyze_food_image_with_desktop(image_path):
    """Analyze food image using Claude Desktop CLI (with image support)"""
    try:
        print(f"🤖 Calling Claude Desktop to analyze image...")

        # Create prompt
        prompt = f"""Analyze this food photo and return ONLY valid JSON (no markdown, no explanation):

{{
  "foods": [
    {{
      "name": "food name",
      "portion_size": "estimated portion (grams or cups)",
      "calories": estimated_calories,
      "protein_g": estimated_protein,
      "carbs_g": estimated_carbs,
      "fat_g": estimated_fat
    }}
  ],
  "total_calories": total,
  "total_protein_g": total_protein,
  "meal_type": "breakfast/lunch/dinner/snack",
  "confidence": "high/medium/low"
}}

Be specific about portion sizes. Use typical serving sizes.
Image: {image_path}"""

        # Call Claude Desktop with image
        # Claude Desktop supports image paths when using --print mode
        result = subprocess.run(
            ['claude', '--print', '--output-format', 'text', prompt],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=os.path.dirname(image_path)  # Set working dir to image folder
        )

        if result.returncode != 0:
            print(f"❌ Claude Desktop error: {result.stderr}")
            return None

        # Parse response
        response_text = result.stdout.strip()

        # Extract JSON from response
        if '{' in response_text:
            json_start = response_text.index('{')
            json_end = response_text.rindex('}') + 1
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)

        print(f"⚠️  Response was not JSON: {response_text[:200]}")
        return None

    except subprocess.TimeoutExpired:
        print("❌ Claude Desktop timeout (60s)")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print(f"Response: {response_text[:500]}")
        return None
    except Exception as e:
        print(f"❌ Error analyzing image: {e}")
        return None

def log_to_sheets(data, image_filename):
    """Log analyzed food to Google Sheets"""
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

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for food in data['foods']:
            row = [
                timestamp,
                food['name'],
                food['portion_size'],
                food['calories'],
                food['protein_g'],
                food['carbs_g'],
                food['fat_g'],
                data['meal_type'],
                f"Photo: {image_filename}",
                data['confidence']
            ]
            meals_sheet.append_row(row)

        print(f"✅ Logged {len(data['foods'])} items to Google Sheets")
        print(f"   Total: {data['total_calories']} cal, {data['total_protein_g']}g protein")

    except Exception as e:
        print(f"❌ Failed to log to sheets: {e}")

def process_image(image_path):
    """Process a single food image"""
    print(f"\n📸 Processing: {os.path.basename(image_path)}")

    # Analyze with Claude Desktop
    data = analyze_food_image_with_desktop(image_path)

    if data:
        print(f"✅ Analysis complete!")
        print(json.dumps(data, indent=2))

        # Log to Google Sheets
        log_to_sheets(data, os.path.basename(image_path))

        # Move to processed folder
        processed_path = os.path.join(PROCESSED_FOLDER, os.path.basename(image_path))
        os.rename(image_path, processed_path)
        print(f"📦 Moved to: {processed_path}")
        return True
    else:
        print("❌ Analysis failed - image not moved")
        return False

def watch_folder():
    """Watch folder for new images"""
    print("\n👀 Watching for new food photos...")
    print(f"📱 Save photos to: {WATCH_FOLDER}")
    print("📊 Data logs to Google Sheets automatically!")
    print("\n" + "="*60)

    processed = set()

    while True:
        try:
            # Check for new images
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG', '*.webp', '*.WEBP']:
                for image_path in Path(WATCH_FOLDER).glob(ext):
                    if str(image_path) not in processed and not image_path.name.startswith('.'):
                        if process_image(str(image_path)):
                            processed.add(str(image_path))

            time.sleep(5)  # Check every 5 seconds

        except KeyboardInterrupt:
            print("\n👋 Stopping image watcher...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    print("🚀 Image Food Logger (Claude Desktop)")
    print("="*60)
    watch_folder()
