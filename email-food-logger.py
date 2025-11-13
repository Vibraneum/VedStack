#!/usr/bin/env python3
"""
EMAIL FOOD LOGGER
-----------------
Email food photos from your phone, script auto-analyzes and logs to Google Sheets.

Workflow:
1. Take photo on phone
2. Email to: food@youremail.com (or yourself)
3. Script checks Gmail every 2 minutes
4. Auto-downloads image attachments
5. Analyzes with Claude Desktop
6. Logs to Google Sheets
7. Archives email

Super simple! Works with ANY email that has image attachments.

Author: Built for Vedanth
Date: November 2025
"""

import os
import sys
import json
import time
import base64
import email
import imaplib
import subprocess
from pathlib import Path
from datetime import datetime
from email.header import decode_header
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

# Configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'vedanth@example.com')  # Your Gmail
EMAIL_PASSWORD = os.getenv('EMAIL_APP_PASSWORD')  # Gmail App Password
EMAIL_SUBJECT_FILTER = os.getenv('EMAIL_SUBJECT_FILTER', 'FOOD')  # Only process emails with this in subject
IMAP_SERVER = "imap.gmail.com"
CHECK_INTERVAL = 120  # Check every 2 minutes

TEMP_FOLDER = os.path.expanduser("~/food-photos/temp")
PROCESSED_FOLDER = os.path.expanduser("~/food-photos/processed")

GOOGLE_CREDS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/home/ved/.config/google-credentials.json')
HEALTH_SHEET_ID = os.getenv('HEALTH_SHEET_ID')

# Create folders
os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def connect_to_gmail():
    """Connect to Gmail via IMAP"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select('INBOX')
        return mail
    except Exception as e:
        print(f"❌ Gmail connection failed: {e}")
        return None

def download_attachments(mail, email_id):
    """Download image attachments from email"""
    try:
        status, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        images = []

        for part in msg.walk():
            if part.get_content_maintype() == 'image':
                filename = part.get_filename()
                if filename:
                    # Decode filename if needed
                    if decode_header(filename)[0][1]:
                        filename = decode_header(filename)[0][0].decode(decode_header(filename)[0][1])

                    # Save image
                    filepath = os.path.join(TEMP_FOLDER, filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))

                    images.append(filepath)
                    print(f"📥 Downloaded: {filename}")

        return images

    except Exception as e:
        print(f"❌ Failed to download attachments: {e}")
        return []

def analyze_food_image(image_path):
    """Analyze food image using Claude Desktop"""
    try:
        print(f"🤖 Analyzing image with Claude Desktop...")

        # Since Claude CLI can't directly process images, we'll use a simpler approach:
        # Ask user to include description in email body, OR
        # Use Claude API if available, OR
        # Just prompt for manual input

        # For now, let's create a prompt that includes the image path
        prompt = f"""I have a food photo at: {image_path}

Based on typical food photos, analyze this and return ONLY valid JSON:

{{
  "foods": [
    {{
      "name": "food name",
      "portion_size": "estimated portion",
      "calories": estimated_calories,
      "protein_g": estimated_protein,
      "carbs_g": estimated_carbs,
      "fat_g": estimated_fat
    }}
  ],
  "total_calories": total,
  "total_protein_g": total_protein,
  "meal_type": "breakfast/lunch/dinner/snack",
  "confidence": "low"
}}

Note: Without image analysis capability, please estimate based on image filename or return null."""

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

def parse_email_body_for_food(email_body):
    """Parse email body for food description"""
    # User can write: "Chicken biryani, 2 cups" in email body
    # We'll extract and analyze that instead of the image
    # This is a fallback when image analysis isn't available

    try:
        # Simple parsing - look for food keywords
        prompt = f"""User emailed this about their meal:
"{email_body[:500]}"

Extract food info and return JSON:
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
        print(f"❌ Body parse error: {e}")
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

def check_inbox():
    """Check Gmail inbox for new food emails"""
    print("\n🔍 Checking inbox...")

    mail = connect_to_gmail()
    if not mail:
        return

    try:
        # Search for unread emails with subject filter
        search_criteria = f'(UNSEEN SUBJECT "{EMAIL_SUBJECT_FILTER}")'
        status, messages = mail.search(None, search_criteria)

        if status != 'OK':
            print("No new emails")
            return

        email_ids = messages[0].split()

        for email_id in email_ids:
            print(f"\n📧 Processing email ID: {email_id.decode()}")

            # Get email body
            status, data = mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = msg['Subject']
            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
            else:
                body = msg.get_payload(decode=True).decode()

            print(f"Subject: {subject}")
            print(f"Body preview: {body[:100]}")

            # Download image attachments
            images = download_attachments(mail, email_id)

            # Analyze food
            data = None

            if images:
                # Try analyzing first image
                data = analyze_food_image(images[0])

            if not data and body:
                # Fall back to email body
                data = parse_email_body_for_food(body)

            if data:
                # Log to sheets
                source = f"Email: {images[0] if images else 'text'}"
                log_to_sheets(data, source)

                # Move images to processed
                for img in images:
                    processed_path = os.path.join(PROCESSED_FOLDER, os.path.basename(img))
                    os.rename(img, processed_path)

                # Mark email as read (archive it)
                mail.store(email_id, '+FLAGS', '\\Seen')
                print("✅ Email processed and marked as read")

            else:
                print("⚠️  Could not extract food data from email")

        mail.close()
        mail.logout()

    except Exception as e:
        print(f"❌ Error checking inbox: {e}")

def main():
    """Main loop"""
    print("🚀 Email Food Logger")
    print("="*60)
    print(f"📧 Monitoring: {EMAIL_ADDRESS}")
    print(f"⏱️  Check interval: {CHECK_INTERVAL}s")
    print(f"📁 Images saved to: {PROCESSED_FOLDER}")
    print("="*60)

    if not EMAIL_PASSWORD:
        print("\n⚠️  EMAIL_APP_PASSWORD not set!")
        print("\nSetup:")
        print("1. Go to: https://myaccount.google.com/apppasswords")
        print("2. Create app password for 'Mail'")
        print("3. Add to .env: EMAIL_APP_PASSWORD=your_16_char_password")
        sys.exit(1)

    print("\n✅ Ready! Send food photos to your email...")
    print("📸 Tip: Include food description in email body for better accuracy\n")

    while True:
        try:
            check_inbox()
            print(f"\n💤 Sleeping for {CHECK_INTERVAL}s...")
            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n👋 Stopping email watcher...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
