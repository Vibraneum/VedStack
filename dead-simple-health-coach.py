#!/usr/bin/env python3
"""
DEAD SIMPLE HEALTH COACH
-------------------------
Talk to Omi. PC syncs. That's it.

Features:
- Voice: Omi captures everything (food, gym, sleep, how you feel)
- Photos: Upload to Omi app (if supported) or WhatsApp to yourself
- Analysis: Claude Desktop analyzes EVERYTHING
- Storage: Google Sheets (check on phone anytime)
- Notifications: Poke (3x per day check-ins)
- Timeline: 12 weeks to 60kg (0.4kg/week = sustainable)

Author: Built for Vedanth
Date: November 2025
"""

import os
import sys
import json
import time
import logging
import hashlib
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

# From environment variables
OMI_API_KEY = os.getenv('OMI_API_KEY', 'omi_dev_2b7983a707b5ede131a0903a1655d918')
POKE_API_KEY = os.getenv('POKE_API_KEY', 'pk_GH6UrWQ1JCpPzmsYTAX0LzNfGKn_TTQDquPUpAOujWM')
HEALTH_SHEET_ID = os.getenv('HEALTH_SHEET_ID')
GOOGLE_CREDS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '/home/ved/.config/google-credentials.json')

# User profile (8-week aggressive bulk plan)
USER_PROFILE = {
    'name': 'Vedanth',
    'age': 20,
    'height_cm': 167,  # From InBody scan
    'start_weight_kg': 54.9,
    'current_weight_kg': 54.9,
    'target_weight_kg': 60.0,
    'target_weeks': 8,
    'target_rate_kg_per_week': 0.6,

    # InBody data (Oct 24, 2025)
    'start_body_fat_kg': 7.8,
    'start_muscle_kg': 26.2,
    'start_bf_percent': 14.3,
    'inbody_score': 74,

    # Nutrition targets
    'daily_calories': 3000,
    'daily_protein_g': 130,
    'daily_carbs_g': 400,
    'daily_fat_g': 75,

    # Training
    'gym_frequency': '6x per week',
    'focus_area': 'legs (lagging at 96%)',
    'start_date': '2025-10-24',

    # TODO: Get and add later
    # 'bench_press_kg': None,  # Current 1RM or working weight
    # 'deadlift_kg': None,
    # 'squat_kg': None,
    # 'resting_hr': None,  # Beats per minute
    # 'hrv_ms': None,  # Heart rate variability
    # 'sleep_score': None,  # From tracker (0-100)
    # 'testosterone_ng_dl': None,  # From blood work
    # 'vitamin_d_ng_ml': None,  # From blood work
}

# Check-in times (your preference)
CHECK_IN_TIMES = {
    'breakfast': '10:00',
    'lunch': '13:00',
    'dinner': '18:00'
}

# Sync settings
SYNC_INTERVAL_MINUTES = 15
STATE_FILE = os.path.expanduser('~/.config/health-coach-state.json')

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.expanduser('~/.config/health-coach.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def load_state() -> dict:
    """Load last sync state"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load state: {e}")

    return {
        'last_sync': None,
        'processed_ids': [],
        'last_check_ins': {}
    }

def save_state(state: dict):
    """Save sync state"""
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save state: {e}")

# ============================================================================
# OMI INTEGRATION
# ============================================================================

def get_omi_memories(since: Optional[str] = None) -> List[dict]:
    """Fetch memories from Omi (includes text and photos)"""
    try:
        url = 'https://api.omi.me/v1/dev/user/memories'
        headers = {'Authorization': f'Bearer {OMI_API_KEY}'}
        params = {'limit': 100}

        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        memories = response.json()

        # Omi automatically transcribes photos you send via chat
        # The 'content' field will include descriptions of food images
        # Example: "User took a photo of chicken biryani with raita"

        # Note: Current Omi API doesn't include timestamps
        # We'll process all memories and use content hash to avoid duplicates

        return memories

    except Exception as e:
        logger.error(f"Failed to fetch Omi memories: {e}")
        return []

# ============================================================================
# CLAUDE DESKTOP INTEGRATION
# ============================================================================

def call_claude_desktop(prompt: str) -> Optional[dict]:
    """
    Call Claude Desktop via MCP
    Returns parsed JSON response or None
    """
    try:
        logger.info("Calling Claude Desktop...")

        result = subprocess.run(
            ['claude', '--print', '--output-format', 'json', prompt],
            capture_output=True,
            text=True,
            timeout=45
        )

        if result.returncode != 0:
            logger.error(f"Claude Desktop error: {result.stderr}")
            return None

        # Parse response
        response = result.stdout.strip()
        # Remove markdown code blocks if present
        response = response.replace('```json', '').replace('```', '').strip()

        return json.loads(response)

    except subprocess.TimeoutExpired:
        logger.error("Claude Desktop timeout (45s)")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Claude response: {e}")
        logger.error(f"Raw response: {result.stdout[:500]}")
        return None
    except Exception as e:
        logger.error(f"Claude Desktop call failed: {e}")
        return None

# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_everything(transcript: str, context: dict) -> Optional[dict]:
    """
    Send transcript to Claude to analyze EVERYTHING
    (food, workout, sleep, measurements, feelings, whatever)
    """

    prompt = f"""You are Vedanth's AI health coach. Style: Technical buddy.

USER PROFILE (12-week bulk to 60kg):
- Current: {USER_PROFILE['current_weight_kg']}kg
- Target: {USER_PROFILE['target_weight_kg']}kg in {USER_PROFILE['target_weeks']} weeks
- Rate: {USER_PROFILE['target_rate_kg_per_week']}kg/week (sustainable)
- Daily: {USER_PROFILE['daily_calories']} cal, {USER_PROFILE['daily_protein_g']}g protein
- Gym: {USER_PROFILE['gym_frequency']}

CONTEXT (Today's progress):
{json.dumps(context, indent=2)}

NEW DATA FROM OMI:
"{transcript}"

TASK:
Analyze this transcript and extract ALL relevant information. It might contain:
- Food (meal, snacks, drinks)
- Workout (exercises, sets, reps, weights, muscle groups, duration)
- Body metrics (weight, measurements, progress photos mentioned)
- Recovery (sleep hours, quality, soreness, pain, stress)
- Feelings (energy, mood, motivation, struggles)
- Goals (new goals, adjustments, concerns)

Return ONLY valid JSON (no markdown):
{{
  "categories": ["nutrition", "fitness", "recovery", "body_metrics", "goals"],
  "data": {{
    "nutrition": {{
      "found": true/false,
      "food_name": "...",
      "portion": "...",
      "calories": 0,
      "protein_g": 0,
      "carbs_g": 0,
      "fat_g": 0,
      "meal_type": "breakfast/lunch/dinner/snack",
      "timing_analysis": "..."
    }},
    "fitness": {{
      "found": true/false,
      "workout_type": "...",
      "muscle_groups": [...],
      "exercises": [
        {{"name": "...", "sets": 0, "reps": 0, "weight_kg": 0}}
      ],
      "duration_min": 0,
      "energy_level": 0,
      "notes": "..."
    }},
    "recovery": {{
      "found": true/false,
      "sleep_hours": 0,
      "sleep_quality": 0,
      "soreness": {{"location": "...", "severity": "..."}},
      "stress_level": "...",
      "notes": "..."
    }},
    "body_metrics": {{
      "found": true/false,
      "weight_kg": 0,
      "measurements": {{}},
      "notes": "..."
    }},
    "goals": {{
      "found": true/false,
      "new_goal": "...",
      "concern": "...",
      "question": "...",
      "notes": "..."
    }}
  }},
  "summary": "One sentence summary of this entry",
  "action_needed": "What to tell Vedanth (advice, question, encouragement)",
  "priority": "high/medium/low"
}}

Be thorough. Extract everything mentioned. If nothing found in a category, set found=false.
"""

    return call_claude_desktop(prompt)

# ============================================================================
# GOOGLE SHEETS INTEGRATION
# ============================================================================

class SheetsClient:
    """Google Sheets client"""

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            GOOGLE_CREDS_PATH,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build('sheets', 'v4', credentials=credentials)

    def append_row(self, sheet_name: str, values: list):
        """Append row to sheet"""
        try:
            body = {'values': [values]}
            result = self.service.spreadsheets().values().append(
                spreadsheetId=HEALTH_SHEET_ID,
                range=f'{sheet_name}!A:Z',
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            return True
        except HttpError as e:
            logger.error(f"Sheets append error: {e}")
            return False

    def get_today_summary(self) -> dict:
        """Get today's totals from Sheets"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')

            # Get all meals today
            result = self.service.spreadsheets().values().get(
                spreadsheetId=HEALTH_SHEET_ID,
                range='Meals!A:H'
            ).execute()

            values = result.get('values', [])
            if not values:
                return {'calories': 0, 'protein': 0, 'meals': 0}

            total_cal = 0
            total_protein = 0
            meal_count = 0

            for row in values[1:]:  # Skip header
                if len(row) >= 6 and row[0] == today:
                    try:
                        total_cal += float(row[4])
                        total_protein += float(row[5])
                        meal_count += 1
                    except (ValueError, IndexError):
                        continue

            return {
                'calories': total_cal,
                'protein': total_protein,
                'meals': meal_count,
                'remaining_calories': USER_PROFILE['daily_calories'] - total_cal,
                'remaining_protein': USER_PROFILE['daily_protein_g'] - total_protein
            }

        except Exception as e:
            logger.error(f"Failed to get today summary: {e}")
            return {'calories': 0, 'protein': 0, 'meals': 0}

sheets = SheetsClient()

# ============================================================================
# LOGGING TO SHEETS
# ============================================================================

def log_nutrition(data: dict):
    """Log nutrition to Meals tab"""
    if not data.get('found'):
        return

    row = [
        datetime.now().strftime('%Y-%m-%d'),
        datetime.now().strftime('%H:%M:%S'),
        data.get('food_name', 'Unknown'),
        data.get('portion', '1 serving'),
        data.get('calories', 0),
        data.get('protein_g', 0),
        data.get('carbs_g', 0),
        data.get('fat_g', 0),
        data.get('meal_type', 'snack'),
        data.get('timing_analysis', '')
    ]

    if sheets.append_row('Meals', row):
        logger.info(f"✅ Logged meal: {data['food_name']}")

def log_workout(data: dict):
    """Log workout to Workouts tab"""
    if not data.get('found'):
        return

    exercises_str = ', '.join([f"{e['name']} {e.get('sets','')}x{e.get('reps','')}"
                                for e in data.get('exercises', [])])

    row = [
        datetime.now().strftime('%Y-%m-%d'),
        datetime.now().strftime('%H:%M:%S'),
        data.get('workout_type', 'Strength'),
        ', '.join(data.get('muscle_groups', [])),
        exercises_str,
        data.get('duration_min', 0),
        data.get('energy_level', 0),
        data.get('notes', '')
    ]

    if sheets.append_row('Workouts', row):
        logger.info(f"✅ Logged workout: {data['workout_type']}")

def log_recovery(data: dict):
    """Log recovery to Recovery tab"""
    if not data.get('found'):
        return

    soreness = data.get('soreness', {})

    row = [
        datetime.now().strftime('%Y-%m-%d'),
        data.get('sleep_hours', 0),
        data.get('sleep_quality', 0),
        soreness.get('location', ''),
        soreness.get('severity', ''),
        data.get('stress_level', ''),
        data.get('notes', '')
    ]

    if sheets.append_row('Recovery', row):
        logger.info(f"✅ Logged recovery: {data['sleep_hours']}hr sleep")

def log_body_metrics(data: dict):
    """Log body metrics to Body Metrics tab"""
    if not data.get('found'):
        return

    measurements = data.get('measurements', {})

    row = [
        datetime.now().strftime('%Y-%m-%d'),
        data.get('weight_kg', 0),
        measurements.get('chest_cm', ''),
        measurements.get('arms_cm', ''),
        measurements.get('waist_cm', ''),
        measurements.get('body_fat_pct', ''),
        data.get('notes', '')
    ]

    if sheets.append_row('Body Metrics', row):
        logger.info(f"✅ Logged metrics: {data['weight_kg']}kg")

# ============================================================================
# POKE NOTIFICATIONS
# ============================================================================

def send_poke(message: str, title: str = "Health Coach"):
    """Send Poke notification"""
    try:
        # Note: Adjust Poke API endpoint based on actual API
        response = requests.post(
            'https://api.poke.dev/v1/push',
            headers={'Authorization': f'Bearer {POKE_API_KEY}'},
            json={
                'title': title,
                'body': message,
                'priority': 'default'
            },
            timeout=10
        )

        if response.status_code == 200:
            logger.info(f"✅ Poke sent: {title}")
        else:
            logger.warning(f"Poke failed: {response.status_code}")

    except Exception as e:
        logger.error(f"Failed to send Poke: {e}")

def should_send_check_in(check_in_type: str, state: dict) -> bool:
    """Check if it's time for a check-in"""
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    target_time = CHECK_IN_TIMES.get(check_in_type, '00:00')

    # Check if we're within 5 minutes of target time
    target_dt = datetime.strptime(target_time, '%H:%M').replace(
        year=now.year, month=now.month, day=now.day
    )
    diff = abs((now - target_dt).total_seconds() / 60)

    if diff > 5:
        return False

    # Check if we already sent today
    last_check_in = state.get('last_check_ins', {}).get(check_in_type)
    if last_check_in == now.strftime('%Y-%m-%d'):
        return False

    return True

def send_check_in(check_in_type: str):
    """Generate and send check-in"""
    summary = sheets.get_today_summary()

    if check_in_type == 'breakfast':
        msg = f"""Morning check! ☀️

Yesterday done. Today's targets:
• {USER_PROFILE['daily_calories']} cal
• {USER_PROFILE['daily_protein_g']}g protein

Breakfast logged? Energy level? (1-10)"""

    elif check_in_type == 'lunch':
        msg = f"""Lunch check! 🍽️

Current: {summary['calories']} cal, {summary['protein']}g protein
Need: {summary['remaining_calories']} cal, {summary['remaining_protein']}g protein more

Lunch logged? How was the gym?"""

    elif check_in_type == 'dinner':
        msg = f"""Evening summary! 🌙

Today: {summary['calories']}/{USER_PROFILE['daily_calories']} cal ({summary['calories']*100//USER_PROFILE['daily_calories']}%)
Protein: {summary['protein']}/{USER_PROFILE['daily_protein_g']}g ({summary['protein']*100//USER_PROFILE['daily_protein_g']}%)
Meals: {summary['meals']}

Dinner plan? Need {summary['remaining_calories']} cal more.
How's body feeling? Soreness?"""

    send_poke(msg, f"{check_in_type.title()} Check-In")

# ============================================================================
# MAIN SYNC LOOP
# ============================================================================

def sync_once():
    """Single sync iteration"""
    state = load_state()

    logger.info("🔄 Starting sync...")

    # Get new memories
    last_sync = state.get('last_sync')
    memories = get_omi_memories(since=last_sync)

    if not memories:
        logger.info("No new memories")
        return

    logger.info(f"📥 Processing {len(memories)} memories")

    # Process each memory
    processed_ids = state.get('processed_ids', [])

    for memory in memories:
        memory_id = memory.get('id', hashlib.md5(memory['content'].encode()).hexdigest())

        if memory_id in processed_ids:
            continue

        transcript = memory['content']
        logger.info(f"Analyzing: {transcript[:100]}...")

        # Get context
        context = sheets.get_today_summary()

        # Analyze with Claude
        analysis = analyze_everything(transcript, context)

        if not analysis:
            logger.warning("Claude analysis failed")
            continue

        # Log to appropriate sheets
        if 'data' in analysis:
            data = analysis['data']
            log_nutrition(data.get('nutrition', {}))
            log_workout(data.get('fitness', {}))
            log_recovery(data.get('recovery', {}))
            log_body_metrics(data.get('body_metrics', {}))

        # Send Poke if action needed and priority high
        if analysis.get('priority') == 'high' and analysis.get('action_needed'):
            send_poke(analysis['action_needed'], "Action Needed")

        # Mark as processed
        processed_ids.append(memory_id)

    # Update state
    state['last_sync'] = datetime.now().isoformat()
    state['processed_ids'] = processed_ids[-1000:]  # Keep last 1000
    save_state(state)

    logger.info("✅ Sync complete")

def main_loop():
    """Main loop - runs continuously while PC is on"""
    logger.info("🚀 Dead Simple Health Coach starting...")
    logger.info(f"Target: {USER_PROFILE['target_weight_kg']}kg in {USER_PROFILE['target_weeks']} weeks")
    logger.info(f"Sync interval: {SYNC_INTERVAL_MINUTES} minutes")

    # Initial sync
    sync_once()

    # Main loop
    while True:
        try:
            # Check for scheduled check-ins
            state = load_state()
            for check_in_type in CHECK_IN_TIMES.keys():
                if should_send_check_in(check_in_type, state):
                    send_check_in(check_in_type)
                    state['last_check_ins'][check_in_type] = datetime.now().strftime('%Y-%m-%d')
                    save_state(state)

            # Wait for next sync
            time.sleep(SYNC_INTERVAL_MINUTES * 60)

            # Sync
            sync_once()

        except KeyboardInterrupt:
            logger.info("Stopping...")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(60)  # Wait 1 min before retry

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    if not HEALTH_SHEET_ID:
        logger.error("HEALTH_SHEET_ID not set!")
        sys.exit(1)

    main_loop()
