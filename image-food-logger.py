#!/usr/bin/env python3
"""
IMAGE FOOD LOGGER
-----------------
Drop food photos in a folder, script analyzes them with Claude Vision API.

Workflow:
1. Take photo on phone
2. Send to yourself on WhatsApp/Telegram
3. Save to: ~/food-photos/
4. Script auto-processes and logs to Google Sheets

Author: Built for Vedanth
Date: November 2025
"""

import os
import sys
import json
import time
import base64
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import requests
import gspread
from google.oauth2.service_account import Credentials
from anthropic import Anthropic

load_dotenv()

# Configuration
WATCH_FOLDER = os.path.expanduser("~/food-photos")
PROCESSED_FOLDER = os.path.expanduser("~/food-photos/processed")
CLAUDE_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GOOGLE_CREDS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/home/ved/.config/google-credentials.json')
HEALTH_SHEET_ID = os.getenv('HEALTH_SHEET_ID')

# Create folders if they don't exist
os.makedirs(WATCH_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

print(f"📁 Watching folder: {WATCH_FOLDER}")
print(f"💾 Processed files move to: {PROCESSED_FOLDER}")

def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_food_image(image_path):
    """Analyze food image using Claude Vision API"""
    if not CLAUDE_API_KEY:
        print("❌ ANTHROPIC_API_KEY not set! Using fallback...")
        return None

    try:
        client = Anthropic(api_key=CLAUDE_API_KEY)

        # Read image
        with open(image_path, "rb") as image_file:
            image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")

        # Detect image type
        ext = Path(image_path).suffix.lower()
        media_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        media_type = media_type_map.get(ext, 'image/jpeg')

        # Analyze with Claude
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyze this food photo and return JSON with:
{
  "foods": [
    {
      "name": "food name",
      "portion_size": "estimated portion (grams or cups)",
      "calories": estimated_calories,
      "protein_g": estimated_protein,
      "carbs_g": estimated_carbs,
      "fat_g": estimated_fat
    }
  ],
  "total_calories": total,
  "total_protein_g": total_protein,
  "meal_type": "breakfast/lunch/dinner/snack",
  "confidence": "high/medium/low"
}

Be specific about portion sizes. Use your knowledge of typical serving sizes."""
                        }
                    ],
                }
            ],
        )

        # Parse response
        response_text = message.content[0].text
        # Extract JSON from response
        if '{' in response_text:
            json_start = response_text.index('{')
            json_end = response_text.rindex('}') + 1
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)

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

    # Analyze with Claude Vision
    data = analyze_food_image(image_path)

    if data:
        print(f"✅ Analysis complete!")
        print(json.dumps(data, indent=2))

        # Log to Google Sheets
        log_to_sheets(data, os.path.basename(image_path))

        # Move to processed folder
        processed_path = os.path.join(PROCESSED_FOLDER, os.path.basename(image_path))
        os.rename(image_path, processed_path)
        print(f"📦 Moved to: {processed_path}")
    else:
        print("❌ Analysis failed")

def watch_folder():
    """Watch folder for new images"""
    print("\n👀 Watching for new food photos...")
    print("📱 Drop images in the folder to analyze them!")

    processed = set()

    while True:
        try:
            # Check for new images
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
                for image_path in Path(WATCH_FOLDER).glob(ext):
                    if str(image_path) not in processed:
                        process_image(str(image_path))
                        processed.add(str(image_path))

            time.sleep(5)  # Check every 5 seconds

        except KeyboardInterrupt:
            print("\n👋 Stopping image watcher...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    if not CLAUDE_API_KEY:
        print("\n⚠️  WARNING: ANTHROPIC_API_KEY not set!")
        print("This script needs Claude API for vision analysis.")
        print("\nGet your API key: https://console.anthropic.com/")
        print("Then add to .env file: ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    watch_folder()
