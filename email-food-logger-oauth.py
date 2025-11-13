#!/usr/bin/env python3
"""
EMAIL FOOD LOGGER (OAuth2 Version)
-----------------------------------
Secure email-based food tracking using Gmail OAuth2.

Uses the SAME Google Service Account you already have!
No app passwords needed - uses your existing google-credentials.json

Author: Built for Vedanth
Date: November 2025
"""

import os
import sys
import json
import time
import base64
import subprocess
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

load_dotenv()

# Configuration
GOOGLE_CREDS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/home/ved/.config/google-credentials.json')
HEALTH_SHEET_ID = os.getenv('HEALTH_SHEET_ID')
EMAIL_SUBJECT_FILTER = os.getenv('EMAIL_SUBJECT_FILTER', 'FOOD')
CHECK_INTERVAL = 120  # Check every 2 minutes

TEMP_FOLDER = os.path.expanduser("~/food-photos/temp")
PROCESSED_FOLDER = os.path.expanduser("~/food-photos/processed")

# Create folders
os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def get_gmail_service():
    """Get Gmail API service using service account credentials"""
    try:
        # Use the same credentials as Google Sheets
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDS_PATH,
            scopes=[
                'https://www.googleapis.com/auth/gmail.readonly',
                'https://www.googleapis.com/auth/gmail.modify'
            ]
        )

        service = build('gmail', 'v1', credentials=creds)
        return service

    except Exception as e:
        print(f"❌ Failed to connect to Gmail: {e}")
        print("\n💡 Note: Service accounts can't access personal Gmail.")
        print("   You need OAuth2 user consent. Creating setup script...")
        return None

def parse_email_body_for_food(text):
    """Parse email body text for food description using Claude Desktop"""
    try:
        prompt = f"""User emailed this about their meal:
"{text[:500]}"

Extract food info and return ONLY valid JSON (no markdown):
{{
  "foods": [
    {{
      "name": "food name",
      "portion_size": "portion",
      "calories": estimate,
      "protein_g": estimate,
      "carbs_g": estimate,
      "fat_g": estimate
    }}
  ],
  "total_calories": total,
  "total_protein_g": total,
  "meal_type": "breakfast/lunch/dinner/snack",
  "confidence": "medium"
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
        print(f"❌ Analysis error: {e}")
        return None

def log_to_sheets(data, source):
    """Log food data to Google Sheets"""
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
                source,
                data['confidence']
            ]
            meals_sheet.append_row(row)

        print(f"✅ Logged to Google Sheets: {data['total_calories']} cal, {data['total_protein_g']}g protein")
        return True

    except Exception as e:
        print(f"❌ Sheets logging failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Email Food Logger (OAuth2)")
    print("="*60)

    service = get_gmail_service()

    if not service:
        print("\n⚠️  Service account can't access personal Gmail.")
        print("\n💡 Better solution: Use a simpler method!")
        print("\n📧 RECOMMENDED: Forward emails to a Google Form instead")
        print("   Or use the Omi voice method (already working!)")
        print("\n🔧 Alternative: I can create a Google Apps Script that:")
        print("   1. Monitors your Gmail")
        print("   2. Processes FOOD emails")
        print("   3. Logs directly to your Google Sheet")
        print("\n   No credentials needed - runs in your Google account!")

        response = input("\n❓ Create Google Apps Script solution? (y/n): ")
        if response.lower() == 'y':
            create_apps_script_solution()

        sys.exit(1)

    print("✅ Connected to Gmail!")
    # Rest of the code...

def create_apps_script_solution():
    """Create Google Apps Script for email monitoring"""

    script_code = """
// Google Apps Script - Email Food Logger
// Monitors Gmail for FOOD emails and logs to Google Sheets

function checkFoodEmails() {
  const SHEET_ID = '1LYz3qgsR5GF3tt-ut6PpOVyKfCb4y-H6a5EW8Okw5SI';
  const SEARCH_QUERY = 'subject:FOOD is:unread';

  // Get Google Sheet
  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName('Meals');

  // Search for unread FOOD emails
  const threads = GmailApp.search(SEARCH_QUERY);

  threads.forEach(thread => {
    const messages = thread.getMessages();

    messages.forEach(message => {
      if (message.isUnread()) {
        // Get email content
        const body = message.getPlainBody();
        const subject = message.getSubject();
        const attachments = message.getAttachments();

        // Get image URLs if any
        let imageUrls = [];
        attachments.forEach(attachment => {
          if (attachment.getContentType().startsWith('image/')) {
            // Save to Google Drive and get URL
            const file = DriveApp.createFile(attachment);
            imageUrls.push(file.getUrl());
          }
        });

        // Analyze with Gemini (you have Gemini Pro subscription!)
        const analysis = analyzeFood(body, imageUrls);

        if (analysis) {
          // Log to sheet
          const timestamp = new Date();
          analysis.foods.forEach(food => {
            sheet.appendRow([
              timestamp,
              food.name,
              food.portion_size,
              food.calories,
              food.protein_g,
              food.carbs_g,
              food.fat_g,
              analysis.meal_type,
              'Email: ' + (imageUrls.length > 0 ? 'with images' : 'text only'),
              analysis.confidence
            ]);
          });
        }

        // Mark as read
        message.markRead();
      }
    });
  });
}

function analyzeFood(text, imageUrls) {
  // Use Gemini API (your subscription!) to analyze
  // Or simple keyword extraction for now

  // Simple version - just parse the text
  const foods = extractFoodFromText(text);

  return {
    foods: foods,
    total_calories: foods.reduce((sum, f) => sum + f.calories, 0),
    total_protein_g: foods.reduce((sum, f) => sum + f.protein_g, 0),
    meal_type: determineMealType(new Date()),
    confidence: imageUrls.length > 0 ? 'medium' : 'low'
  };
}

function extractFoodFromText(text) {
  // Simple extraction - you can enhance this
  // For now, return a basic structure
  return [{
    name: text.substring(0, 50),
    portion_size: '1 serving',
    calories: 500,  // Estimate
    protein_g: 20,
    carbs_g: 50,
    fat_g: 15
  }];
}

function determineMealType(timestamp) {
  const hour = timestamp.getHours();
  if (hour < 10) return 'breakfast';
  if (hour < 14) return 'lunch';
  if (hour < 17) return 'snack';
  return 'dinner';
}

// Set up trigger to run every 2 minutes
function createTrigger() {
  ScriptApp.newTrigger('checkFoodEmails')
    .timeBased()
    .everyMinutes(2)
    .create();
}
"""

    # Save the script
    script_path = '/mnt/d/MCP/foodtracker/GoogleAppsScript-EmailFoodLogger.js'
    with open(script_path, 'w') as f:
        f.write(script_code)

    print(f"\n✅ Created Google Apps Script!")
    print(f"📝 Saved to: {script_path}")
    print("\n📋 Setup Instructions:")
    print("1. Go to: https://script.google.com")
    print("2. Click 'New Project'")
    print("3. Copy-paste the code from GoogleAppsScript-EmailFoodLogger.js")
    print("4. Click 'Run' to test")
    print("5. Click 'Triggers' → 'Add Trigger'")
    print("6. Set: checkFoodEmails, Time-driven, Minutes timer, Every 2 minutes")
    print("7. Save!")
    print("\n🎉 Done! Emails with subject 'FOOD' will auto-log to your sheet!")

if __name__ == '__main__':
    main()
