#!/usr/bin/env python3
"""
Scalable Food Tracker - Webhook Endpoint
-----------------------------------------
Receives Omi transcripts in real-time, analyzes with Claude, logs to Google Sheets

Architecture:
Omi Device → Webhook → Claude Analysis → Google Sheets → Poke Notification

Author: Built for Vedanth's food tracking system
Last Updated: November 2025
"""

import os
import json
import logging
import hashlib
import hmac
from datetime import datetime
from typing import Dict, Optional, List
import asyncio

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import uvicorn
from pydantic import BaseModel, validator
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import anthropic

# ============================================================================
# CONFIGURATION
# ============================================================================

# Load from environment variables
OMI_API_KEY = os.getenv('OMI_API_KEY', 'omi_dev_2b7983a707b5ede131a0903a1655d918')
POKE_API_KEY = os.getenv('POKE_API_KEY', 'pk_GH6UrWQ1JCpPzmsYTAX0LzNfGKn_TTQDquPUpAOujWM')
HEALTH_SHEET_ID = os.getenv('HEALTH_SHEET_ID')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'default_secret_change_in_production')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')  # Optional if using MCP

# Google Sheets setup
GOOGLE_CREDENTIALS_PATH = os.getenv(
    'GOOGLE_APPLICATION_CREDENTIALS',
    '/home/ved/.config/google-credentials.json'
)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# User context for food analysis
USER_CONTEXT = {
    'name': 'Vedanth',
    'current_weight_kg': 54.9,
    'goal_weight_kg': 60,
    'goal': 'bulking',
    'daily_calories': 2800,
    'daily_protein_g': 120,
    'activity': 'gym 6x/week'
}

# Food detection keywords
FOOD_KEYWORDS = [
    'ate', 'eating', 'eaten', 'had', 'having', 'breakfast', 'lunch',
    'dinner', 'snack', 'meal', 'food', 'hungry', 'full', 'cooked',
    'ordered', 'restaurant', 'calories', 'protein', 'carbs', 'shawarma',
    'biryani', 'dal', 'rice', 'chapati', 'roti', 'chicken', 'paneer'
]

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/food-tracker-webhook.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Scalable Food Tracker API",
    description="Webhook endpoint for Omi device food tracking",
    version="1.0.0"
)

# ============================================================================
# DATA MODELS
# ============================================================================

class OmiWebhookPayload(BaseModel):
    """Omi webhook payload structure"""
    transcript: str
    speaker: Optional[str] = None
    timestamp: Optional[str] = None
    session_id: Optional[str] = None
    segments: Optional[List[Dict]] = None

    @validator('transcript')
    def transcript_not_empty(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Transcript too short')
        return v.strip()

class FoodAnalysis(BaseModel):
    """Food analysis result from Claude"""
    food_name: str
    portion_estimate: str
    calories: int
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    micronutrients: Dict[str, float]
    meal_timing: str
    meal_type: str
    recommendation: str
    fits_goals: bool

# ============================================================================
# GOOGLE SHEETS CLIENT
# ============================================================================

class GoogleSheetsClient:
    """Handles all Google Sheets operations"""

    def __init__(self):
        self.service = None
        self._initialize_service()

    def _initialize_service(self):
        """Initialize Google Sheets API service"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                GOOGLE_CREDENTIALS_PATH,
                scopes=SCOPES
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Google Sheets service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets service: {e}")
            raise

    def append_meal(self, analysis: FoodAnalysis, original_transcript: str) -> bool:
        """Append meal to Google Sheets"""
        try:
            now = datetime.now()
            values = [[
                now.strftime('%Y-%m-%d'),
                now.strftime('%H:%M:%S'),
                analysis.food_name,
                analysis.portion_estimate,
                analysis.calories,
                analysis.protein_g,
                analysis.carbs_g,
                analysis.fat_g,
                analysis.fiber_g,
                analysis.micronutrients.get('iron_mg', 0),
                analysis.micronutrients.get('calcium_mg', 0),
                analysis.micronutrients.get('vitamin_a_iu', 0),
                analysis.micronutrients.get('vitamin_c_mg', 0),
                analysis.meal_type,
                analysis.meal_timing,
                analysis.recommendation,
                'Omi Webhook',
                hashlib.md5(original_transcript.encode()).hexdigest()[:8]
            ]]

            body = {'values': values}

            result = self.service.spreadsheets().values().append(
                spreadsheetId=HEALTH_SHEET_ID,
                range='Meals!A:R',
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()

            logger.info(f"Meal appended to Sheets: {analysis.food_name}")
            return True

        except HttpError as e:
            logger.error(f"Google Sheets API error: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to append meal to Sheets: {e}")
            return False

    def get_todays_totals(self) -> Dict[str, float]:
        """Get today's calorie and protein totals"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')

            result = self.service.spreadsheets().values().get(
                spreadsheetId=HEALTH_SHEET_ID,
                range='Meals!A:F'
            ).execute()

            values = result.get('values', [])
            if not values:
                return {'calories': 0, 'protein': 0}

            # Skip header row
            total_calories = 0
            total_protein = 0

            for row in values[1:]:  # Skip header
                if len(row) >= 6:
                    date = row[0]
                    if date == today:
                        try:
                            total_calories += float(row[4])  # Column E
                            total_protein += float(row[5])   # Column F
                        except (ValueError, IndexError):
                            continue

            return {
                'calories': total_calories,
                'protein': total_protein
            }

        except Exception as e:
            logger.error(f"Failed to get today's totals: {e}")
            return {'calories': 0, 'protein': 0}

# Initialize Sheets client
sheets_client = GoogleSheetsClient()

# ============================================================================
# CLAUDE INTEGRATION
# ============================================================================

class ClaudeAnalyzer:
    """Handles food analysis with Claude AI"""

    def __init__(self):
        if CLAUDE_API_KEY:
            self.client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
            self.use_api = True
            logger.info("Claude API client initialized")
        else:
            self.use_api = False
            logger.warning("No Claude API key found, will use MCP fallback")

    def analyze_food(self, transcript: str) -> Optional[FoodAnalysis]:
        """Analyze food mention with Claude"""
        try:
            if self.use_api:
                return self._analyze_with_api(transcript)
            else:
                return self._analyze_with_mcp(transcript)
        except Exception as e:
            logger.error(f"Claude analysis failed: {e}")
            return self._fallback_analysis(transcript)

    def _analyze_with_api(self, transcript: str) -> FoodAnalysis:
        """Use Claude API for analysis"""
        prompt = f"""You are analyzing food for {USER_CONTEXT['name']}.

User Context:
- Current weight: {USER_CONTEXT['current_weight_kg']}kg
- Goal weight: {USER_CONTEXT['goal_weight_kg']}kg ({USER_CONTEXT['goal']})
- Daily targets: {USER_CONTEXT['daily_calories']} calories, {USER_CONTEXT['daily_protein_g']}g protein
- Activity level: {USER_CONTEXT['activity']}

Food mention from transcript:
"{transcript}"

Analyze this food and return ONLY valid JSON (no markdown, no code blocks):
{{
  "food_name": "exact food identified",
  "portion_estimate": "serving size with reasoning",
  "calories": <number>,
  "protein_g": <number>,
  "carbs_g": <number>,
  "fat_g": <number>,
  "fiber_g": <number>,
  "micronutrients": {{
    "iron_mg": <number>,
    "calcium_mg": <number>,
    "vitamin_a_iu": <number>,
    "vitamin_c_mg": <number>
  }},
  "meal_timing": "HH:MM or 'now'",
  "meal_type": "breakfast/lunch/dinner/snack",
  "recommendation": "specific advice for {USER_CONTEXT['name']}'s bulk goals",
  "fits_goals": true/false
}}

Be specific to Indian foods and bulking goals. If unsure, make reasonable estimates.
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract JSON from response
        content = response.content[0].text.strip()
        # Remove markdown code blocks if present
        content = content.replace('```json', '').replace('```', '').strip()

        data = json.loads(content)
        return FoodAnalysis(**data)

    def _analyze_with_mcp(self, transcript: str) -> FoodAnalysis:
        """Use Claude Desktop via MCP (subprocess)"""
        import subprocess

        prompt = f"Analyze food for {USER_CONTEXT['name']}: {transcript}"

        result = subprocess.run(
            ['claude', '--prompt', prompt],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            response = result.stdout.strip()
            response = response.replace('```json', '').replace('```', '').strip()
            data = json.loads(response)
            return FoodAnalysis(**data)
        else:
            raise Exception(f"MCP call failed: {result.stderr}")

    def _fallback_analysis(self, transcript: str) -> FoodAnalysis:
        """Fallback to basic analysis if Claude fails"""
        # Simple keyword-based extraction
        food_name = "Unknown Food"
        calories = 400
        protein = 20

        # Try to extract food name from transcript
        words = transcript.lower().split()
        food_keywords = ['chicken', 'rice', 'dal', 'chapati', 'shawarma', 'biryani']
        for keyword in food_keywords:
            if keyword in transcript.lower():
                food_name = keyword.title()
                break

        return FoodAnalysis(
            food_name=food_name,
            portion_estimate="1 serving (estimated)",
            calories=calories,
            protein_g=protein,
            carbs_g=50,
            fat_g=15,
            fiber_g=5,
            micronutrients={'iron_mg': 2, 'calcium_mg': 100, 'vitamin_a_iu': 0, 'vitamin_c_mg': 0},
            meal_timing=datetime.now().strftime('%H:%M'),
            meal_type="unknown",
            recommendation="Log manually for accuracy",
            fits_goals=True
        )

# Initialize Claude analyzer
claude_analyzer = ClaudeAnalyzer()

# ============================================================================
# POKE NOTIFICATIONS
# ============================================================================

def send_poke_notification(analysis: FoodAnalysis, totals: Dict[str, float]):
    """Send notification via Poke"""
    try:
        remaining_cal = USER_CONTEXT['daily_calories'] - totals['calories']
        remaining_protein = USER_CONTEXT['daily_protein_g'] - totals['protein']

        message = f"""✅ Meal logged!

🍽️ {analysis.food_name} ({analysis.portion_estimate})
📊 {analysis.calories} cal | {analysis.protein_g}g protein

Today's Progress:
🎯 {remaining_cal:.0f} cal remaining
💪 {remaining_protein:.1f}g protein remaining

💡 {analysis.recommendation}
"""

        # Note: Adjust Poke API endpoint based on actual API documentation
        response = requests.post(
            'https://api.poke.com/v1/notify',  # Verify actual endpoint
            headers={'Authorization': f'Bearer {POKE_API_KEY}'},
            json={
                'title': 'Food Logged!',
                'message': message,
                'priority': 'normal'
            },
            timeout=10
        )

        if response.status_code == 200:
            logger.info("Poke notification sent successfully")
        else:
            logger.warning(f"Poke notification failed: {response.status_code}")

    except Exception as e:
        logger.error(f"Failed to send Poke notification: {e}")

# ============================================================================
# FOOD DETECTION
# ============================================================================

def is_food_mention(transcript: str) -> bool:
    """Detect if transcript mentions food"""
    transcript_lower = transcript.lower()

    # Check for food keywords
    for keyword in FOOD_KEYWORDS:
        if keyword in transcript_lower:
            return True

    return False

# ============================================================================
# DUPLICATE PREVENTION
# ============================================================================

processed_hashes = set()

def is_duplicate(transcript: str) -> bool:
    """Check if transcript was already processed"""
    hash_val = hashlib.md5(transcript.encode()).hexdigest()

    if hash_val in processed_hashes:
        return True

    processed_hashes.add(hash_val)

    # Keep only last 1000 hashes to prevent memory bloat
    if len(processed_hashes) > 1000:
        processed_hashes.pop()

    return False

# ============================================================================
# WEBHOOK SIGNATURE VERIFICATION
# ============================================================================

def verify_webhook_signature(request: Request, body: bytes) -> bool:
    """Verify Omi webhook signature"""
    signature = request.headers.get('X-Omi-Signature')
    if not signature:
        # In development, allow without signature
        if os.getenv('ENVIRONMENT') == 'development':
            return True
        return False

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Scalable Food Tracker API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {}
    }

    # Check Google Sheets connection
    try:
        sheets_client.service.spreadsheets().get(spreadsheetId=HEALTH_SHEET_ID).execute()
        health_status["services"]["google_sheets"] = "connected"
    except:
        health_status["services"]["google_sheets"] = "disconnected"
        health_status["status"] = "degraded"

    # Check Claude availability
    if claude_analyzer.use_api:
        health_status["services"]["claude"] = "api"
    else:
        health_status["services"]["claude"] = "mcp"

    return health_status

@app.post("/omi-webhook")
async def handle_omi_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    """Main webhook endpoint for Omi transcripts"""
    try:
        # Get raw body for signature verification
        body = await request.body()

        # Verify signature
        if not verify_webhook_signature(request, body):
            logger.warning("Invalid webhook signature")
            raise HTTPException(status_code=401, detail="Invalid signature")

        # Parse JSON
        data = json.loads(body)

        # Validate payload
        try:
            payload = OmiWebhookPayload(**data)
        except Exception as e:
            logger.error(f"Invalid payload: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid payload: {e}")

        transcript = payload.transcript
        logger.info(f"Received transcript: {transcript[:100]}...")

        # Check for duplicate
        if is_duplicate(transcript):
            logger.info("Duplicate transcript, ignoring")
            return {"status": "ignored", "reason": "duplicate"}

        # Detect food mention
        if not is_food_mention(transcript):
            logger.info("No food mention detected")
            return {"status": "ignored", "reason": "no_food_detected"}

        # Process in background
        background_tasks.add_task(
            process_food_mention,
            transcript,
            payload.speaker or "Unknown"
        )

        return {
            "status": "processing",
            "transcript_id": hashlib.md5(transcript.encode()).hexdigest()[:8]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_food_mention(transcript: str, speaker: str):
    """Process food mention (runs in background)"""
    try:
        logger.info(f"Processing food mention from {speaker}")

        # Analyze with Claude
        analysis = claude_analyzer.analyze_food(transcript)
        if not analysis:
            logger.error("Failed to analyze food")
            return

        logger.info(f"Analyzed food: {analysis.food_name}, {analysis.calories} cal")

        # Write to Google Sheets
        success = sheets_client.append_meal(analysis, transcript)
        if not success:
            logger.error("Failed to write to Google Sheets")
            return

        # Get today's totals
        totals = sheets_client.get_todays_totals()

        # Send Poke notification
        send_poke_notification(analysis, totals)

        logger.info(f"Food tracking complete: {analysis.food_name}")

    except Exception as e:
        logger.error(f"Error processing food mention: {e}")

@app.post("/test-food-analysis")
async def test_food_analysis(request: Request):
    """Test endpoint for food analysis (development only)"""
    if os.getenv('ENVIRONMENT') != 'development':
        raise HTTPException(status_code=403, detail="Only available in development")

    data = await request.json()
    transcript = data.get('transcript', '')

    if not transcript:
        raise HTTPException(status_code=400, detail="Missing transcript")

    analysis = claude_analyzer.analyze_food(transcript)
    return analysis.dict()

# ============================================================================
# STARTUP & SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Scalable Food Tracker API...")

    # Verify environment variables
    if not HEALTH_SHEET_ID:
        logger.error("HEALTH_SHEET_ID not set!")

    logger.info("Startup complete!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Scalable Food Tracker API...")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    uvicorn.run(
        "webhook_server:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv('ENVIRONMENT') == 'development'
    )
