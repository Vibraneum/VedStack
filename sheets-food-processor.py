#!/usr/bin/env python3
"""
SHEETS FOOD PROCESSOR
---------------------
Monitors Google Sheets for food entries that need Claude analysis.

Workflow:
1. You email food photo with subject "FOOD"
2. Google Apps Script creates "pending" entry in "Email Queue" tab
3. This script monitors "Email Queue" tab
4. Analyzes with Claude Desktop
5. Moves analyzed data to "Meals" tab

Perfect combo: Google Apps Script (email monitoring) + Claude Desktop (analysis)

Author: Built for Vedanth
Date: November 2025
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

# Configuration
GOOGLE_CREDS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/home/ved/.config/google-credentials.json')
HEALTH_SHEET_ID = os.getenv('HEALTH_SHEET_ID')
CHECK_INTERVAL = 30  # Check every 30 seconds

def analyze_food_with_claude(food_description, has_image=False):
    """Analyze food using Claude Desktop"""
    try:
        prompt = f"""Analyze this food entry and return ONLY valid JSON:

Food: {food_description}
Has image: {has_image}

Return:
{{
  "foods": [
    {{
      "name": "food name",
      "portion_size": "estimated portion",
      "calories": estimate,
      "protein_g": estimate,
      "carbs_g": estimate,
      "fat_g": estimate
    }}
  ],
  "total_calories": total,
  "total_protein_g": total,
  "meal_type": "breakfast/lunch/dinner/snack",
  "confidence": "{\"high\" if has_image else \"medium\"}"
}}"""

        result = subprocess.run(
            ['claude', '--print', '--output-format', 'text', prompt],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            response = result.stdout.strip()
            if '{' in response:
                json_start = response.index('{')
                json_end = response.rindex('}') + 1
                return json.loads(response[json_start:json_end])

        return None

    except Exception as e:
        print(f"❌ Claude analysis error: {e}")
        return None

def process_pending_entries():
    """Process pending food entries from Email Queue tab"""
    try:
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDS_PATH,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(HEALTH_SHEET_ID)

        # Check if Email Queue tab exists
        try:
            queue_sheet = sheet.worksheet('Email Queue')
        except:
            # Create it if it doesn't exist
            queue_sheet = sheet.add_worksheet(title='Email Queue', rows=1000, cols=10)
            queue_sheet.append_row([
                'Timestamp', 'Email Subject', 'Email Body', 'Has Images',
                'Image URLs', 'Status', 'Processed At'
            ])
            print("✅ Created 'Email Queue' tab")
            return

        meals_sheet = sheet.worksheet('Meals')

        # Get all pending entries
        rows = queue_sheet.get_all_values()

        if len(rows) <= 1:  # Only header
            return

        processed_count = 0

        for idx, row in enumerate(rows[1:], start=2):  # Start from row 2 (skip header)
            if len(row) < 6:
                continue

            timestamp, subject, body, has_images, image_urls, status = row[:6]

            # Skip if already processed
            if status == 'processed':
                continue

            print(f"\n📧 Processing email from {timestamp}")
            print(f"   Subject: {subject}")
            print(f"   Body: {body[:100]}...")

            # Analyze with Claude
            has_image = has_images.lower() == 'true'
            data = analyze_food_with_claude(body, has_image)

            if data:
                # Log to Meals sheet
                for food in data['foods']:
                    meals_row = [
                        timestamp,
                        food['name'],
                        food['portion_size'],
                        food['calories'],
                        food['protein_g'],
                        food['carbs_g'],
                        food['fat_g'],
                        data['meal_type'],
                        f"Email ({subject})",
                        data['confidence']
                    ]
                    meals_sheet.append_row(meals_row)

                print(f"✅ Logged {len(data['foods'])} items: {data['total_calories']} cal, {data['total_protein_g']}g protein")

                # Mark as processed
                queue_sheet.update_cell(idx, 6, 'processed')
                queue_sheet.update_cell(idx, 7, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                processed_count += 1
            else:
                print("⚠️  Analysis failed")

        if processed_count > 0:
            print(f"\n🎉 Processed {processed_count} email(s)")

    except Exception as e:
        print(f"❌ Error processing queue: {e}")

def main():
    """Main loop"""
    print("🚀 Sheets Food Processor")
    print("="*60)
    print(f"📊 Monitoring Google Sheet: {HEALTH_SHEET_ID}")
    print(f"⏱️  Check interval: {CHECK_INTERVAL}s")
    print("="*60)
    print("\n✅ Ready! Waiting for emails...")
    print("📧 Send emails with subject 'FOOD' to trigger processing\n")

    while True:
        try:
            process_pending_entries()
            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n👋 Stopping processor...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
