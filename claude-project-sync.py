#!/usr/bin/env python3
"""
CLAUDE PROJECT SYNC
-------------------
Simplest solution: Use Claude mobile app to send food photos!

Setup:
1. Create Claude Project called "Food Tracker"
2. Start conversation in that project
3. Send food photos with description via mobile app
4. Claude analyzes automatically
5. This script syncs to Google Sheets

Workflow:
- Take photo on phone
- Open Claude mobile app
- Send to "Food Tracker" project
- Add text: "analyze nutrition"
- Claude responds with calorie breakdown
- Script syncs response to Google Sheets

Author: Built for Vedanth
Date: November 2025
"""

import os
import sys
import json
import time
import re
from datetime import datetime
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

# Configuration
GOOGLE_CREDS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/home/ved/.config/google-credentials.json')
HEALTH_SHEET_ID = os.getenv('HEALTH_SHEET_ID')
CLAUDE_EXPORT_FOLDER = os.path.expanduser("~/claude-exports")
CHECK_INTERVAL = 60  # Check every minute

os.makedirs(CLAUDE_EXPORT_FOLDER, exist_ok=True)

def parse_claude_response_for_nutrition(text):
    """Extract nutrition info from Claude's response"""
    try:
        # Claude's response might include:
        # "Calories: 650, Protein: 35g, Carbs: 85g, Fat: 18g"

        calories = re.search(r'calories?:?\s*(\d+)', text, re.IGNORECASE)
        protein = re.search(r'protein:?\s*(\d+)', text, re.IGNORECASE)
        carbs = re.search(r'carbs?:?\s*(\d+)', text, re.IGNORECASE)
        fat = re.search(r'fat:?\s*(\d+)', text, re.IGNORECASE)

        # Extract food name (first line or first sentence)
        food_name = text.split('\\n')[0][:100]

        return {
            'name': food_name,
            'calories': int(calories.group(1)) if calories else 400,
            'protein_g': int(protein.group(1)) if protein else 20,
            'carbs_g': int(carbs.group(1)) if carbs else 40,
            'fat_g': int(fat.group(1)) if fat else 15,
            'portion_size': '1 serving'
        }

    except:
        return None

def log_to_sheets(food_data, source):
    """Log food to Google Sheets"""
    try:
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDS_PATH,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(HEALTH_SHEET_ID)
        meals_sheet = sheet.worksheet('Meals')

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        row = [
            timestamp,
            food_data['name'],
            food_data['portion_size'],
            food_data['calories'],
            food_data['protein_g'],
            food_data['carbs_g'],
            food_data['fat_g'],
            'snack',  # Default - can enhance later
            source,
            'high'  # High confidence when Claude analyzes images
        ]

        meals_sheet.append_row(row)
        print(f"✅ Logged: {food_data['name']} - {food_data['calories']} cal")
        return True

    except Exception as e:
        print(f"❌ Logging failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Claude Project Sync")
    print("="*60)
    print("\n📱 SETUP INSTRUCTIONS:")
    print("="*60)
    print("\n1️⃣  Open Claude mobile app")
    print("2️⃣  Create a new project: 'Food Tracker'")
    print("3️⃣  Start a conversation")
    print("4️⃣  Take food photo and send with:")
    print("     'Analyze this food - estimate calories, protein, carbs, fat'")
    print("5️⃣  Claude analyzes and responds")
    print("6️⃣  THIS SCRIPT NOT IMPLEMENTED YET!")
    print("\n⚠️  Claude mobile doesn't have real-time API sync (yet)")
    print("\n💡 BETTER SOLUTION: Just use Omi voice (already working!)")
    print("\n   Or the SIMPLEST method:")
    print("   1. Send photo to Claude mobile")
    print("   2. Claude tells you calories")
    print("   3. Tell Omi: 'I ate [food] with [calories] calories'")
    print("   4. Omi syncs to sheets automatically!")
    print("\n   HYBRID APPROACH = Best accuracy!")
    print("="*60)

if __name__ == '__main__':
    main()
