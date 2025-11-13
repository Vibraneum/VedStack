"""
VedStack Omi Backend - Real-Time Food Logging
FastAPI server for Omi voice → Airtable integration
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

app = FastAPI(title="VedStack Omi Backend", version="1.0.0")

# CORS middleware (allow Omi webhooks)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables (set these in Railway/Vercel dashboard or .env file)
AIRTABLE_PAT = os.getenv("AIRTABLE_PAT")
AIRTABLE_BASE = os.getenv("AIRTABLE_BASE")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")  # Optional: for smarter extraction

if not AIRTABLE_PAT or not AIRTABLE_BASE:
    raise ValueError("AIRTABLE_PAT and AIRTABLE_BASE must be set as environment variables")

# In-memory session tracking (for deduplication)
active_sessions: Dict[str, Dict] = {}

# Food keywords for detection
FOOD_KEYWORDS = [
    "eating", "ate", "having", "had", "consumed",
    "breakfast", "lunch", "dinner", "snack", "meal",
    "roti", "chapati", "dal", "rice", "paneer", "egg",
    "upma", "poha", "biryani", "chicken", "sabzi",
    "food", "hungry", "full"
]

# Macro calculation reference (simplified - full version queries Airtable)
FOOD_MACROS = {
    "roti": {"cal": 71, "protein": 3, "carbs": 15, "fat": 0.4},
    "chapati": {"cal": 71, "protein": 3, "carbs": 15, "fat": 0.4},
    "dal": {"cal": 230, "protein": 18, "carbs": 40, "fat": 0.8},
    "rice": {"cal": 205, "protein": 4.2, "carbs": 45, "fat": 0.4},
    "paneer": {"cal": 265, "protein": 18, "carbs": 3.6, "fat": 20},
    "egg": {"cal": 70, "protein": 6, "carbs": 0.6, "fat": 5},
    "upma": {"cal": 200, "protein": 5, "carbs": 35, "fat": 5},
    "poha": {"cal": 250, "protein": 6, "carbs": 50, "fat": 5},
}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "VedStack Omi Backend",
        "version": "1.0.0",
        "endpoints": {
            "health": "/",
            "omi_webhook": "/omi/transcript",
            "stats": "/stats"
        }
    }


@app.get("/stats")
async def get_stats():
    """Get session statistics"""
    return {
        "active_sessions": len(active_sessions),
        "sessions": list(active_sessions.keys())
    }


@app.post("/omi/transcript")
async def handle_omi_transcript(request: Request):
    """
    Handle real-time transcript from Omi

    Omi sends overlapping transcript segments as user speaks.
    We detect food mentions, extract items, calculate macros,
    and log to Airtable - WITHOUT creating Omi memories.
    """
    try:
        # Parse request
        data = await request.json()
        query_params = request.query_params

        uid = query_params.get("uid", "unknown_user")
        session_id = data.get("session_id", "unknown_session")
        segments = data.get("segments", [])

        if not segments:
            return {"status": "ignored", "reason": "no segments"}

        # Combine all user-spoken text
        full_text = " ".join([
            seg.get("text", "")
            for seg in segments
            if seg.get("is_user", True)
        ])

        print(f"[{session_id}] Received: {full_text[:100]}")

        # Check if this is food-related
        if not is_food_mention(full_text):
            return {"status": "ignored", "reason": "not food related"}

        # Deduplication: Has this session already logged recently?
        if session_id in active_sessions:
            last_log = active_sessions[session_id]
            seconds_since = (datetime.now() - last_log["timestamp"]).seconds

            if seconds_since < 60:  # Within last 60 seconds
                # Check if food items are the same (avoid duplicate logging)
                if full_text.lower() == last_log.get("text", "").lower():
                    print(f"[{session_id}] Duplicate detected, skipping")
                    return {
                        "status": "duplicate",
                        "reason": "already logged in last 60s",
                        "previous_log_id": last_log.get("airtable_id")
                    }

        # Extract food items from transcript
        food_items = extract_food_items(full_text)

        if not food_items:
            return {"status": "ignored", "reason": "no food items detected"}

        print(f"[{session_id}] Extracted: {food_items}")

        # Calculate macros (simple version - can be enhanced with Airtable lookup)
        macros = calculate_macros_simple(food_items)

        # Get today's total before logging this meal
        daily_total = await get_daily_total(uid)

        # Write to Airtable Food Log
        log_entry = await log_to_airtable(
            uid=uid,
            description=full_text,
            food_items=food_items,
            macros=macros
        )

        # Update session tracking
        active_sessions[session_id] = {
            "timestamp": datetime.now(),
            "text": full_text,
            "airtable_id": log_entry.get("id"),
            "macros": macros
        }

        # Calculate new daily total
        new_daily_total = daily_total + macros["calories"]
        remaining = 3000 - new_daily_total

        # Prepare response message (Omi can speak this back)
        response_message = (
            f"Logged: {macros['calories']} cal, {macros['protein']}g protein. "
            f"You're at {new_daily_total} cal today"
        )

        if remaining > 0:
            response_message += f", {remaining} remaining."
        else:
            response_message += f". Target hit!"

        print(f"[{session_id}] Success: {response_message}")

        return {
            "status": "logged",
            "message": response_message,
            "data": {
                "airtable_id": log_entry.get("id"),
                "calories": macros["calories"],
                "protein": macros["protein"],
                "carbs": macros["carbs"],
                "fat": macros["fat"],
                "daily_total": new_daily_total,
                "target": 3000,
                "remaining": max(0, remaining)
            }
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def is_food_mention(text: str) -> bool:
    """Check if text mentions food"""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in FOOD_KEYWORDS)


def extract_food_items(text: str) -> List[Dict]:
    """
    Extract food items and quantities from text

    Example: "I'm eating 3 rotis with dal and paneer"
    Returns: [
        {"item": "roti", "quantity": 3},
        {"item": "dal", "quantity": 1},
        {"item": "paneer", "quantity": 1}
    ]
    """
    text_lower = text.lower()
    items = []

    # Pattern 1: Number + food (e.g., "3 rotis", "2 eggs")
    pattern = r'(\d+|one|two|three|four|five|six)\s+(\w+)'
    matches = re.findall(pattern, text_lower)

    # Convert word numbers to digits
    word_to_num = {
        "one": 1, "two": 2, "three": 3,
        "four": 4, "five": 5, "six": 6
    }

    for quantity, food in matches:
        qty = word_to_num.get(quantity, int(quantity) if quantity.isdigit() else 1)

        # Normalize food name (remove plurals)
        food_normalized = food.rstrip('s')

        # Check if it's a known food
        if food_normalized in FOOD_MACROS:
            items.append({"item": food_normalized, "quantity": qty})

    # Pattern 2: Foods without quantities (assume 1 serving)
    for food in FOOD_MACROS.keys():
        if food in text_lower and not any(item["item"] == food for item in items):
            items.append({"item": food, "quantity": 1})

    return items


def calculate_macros_simple(food_items: List[Dict]) -> Dict:
    """
    Calculate total macros from food items (simple version)

    For production, this should query Airtable's Macro Calculation Rules table
    """
    total = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

    for item in food_items:
        food = item["item"]
        qty = item["quantity"]

        if food in FOOD_MACROS:
            macros = FOOD_MACROS[food]
            total["calories"] += macros["cal"] * qty
            total["protein"] += macros["protein"] * qty
            total["carbs"] += macros["carbs"] * qty
            total["fat"] += macros["fat"] * qty

    # Round values
    total["calories"] = round(total["calories"])
    total["protein"] = round(total["protein"], 1)
    total["carbs"] = round(total["carbs"], 1)
    total["fat"] = round(total["fat"], 1)

    return total


async def log_to_airtable(uid: str, description: str, food_items: List[Dict], macros: Dict) -> Dict:
    """Write meal to Airtable Food Log table"""

    # Infer meal type based on time of day
    meal_type = infer_meal_type()

    # Format food description
    food_description = f"{description}\n\nExtracted: {', '.join([f'{i['quantity']} {i['item']}' for i in food_items])}"

    payload = {
        "records": [{
            "fields": {
                "Date": datetime.now().isoformat(),
                "Food Description": food_description,
                "Calories": macros["calories"],
                "Protein": macros["protein"],
                "Carbs": macros["carbs"],
                "Fat": macros["fat"],
                "Meal Type": meal_type,
                "Source": "Omi Voice (Real-time)"
            }
        }]
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"https://api.airtable.com/v0/{AIRTABLE_BASE}/Food%20Log",
            headers={
                "Authorization": f"Bearer {AIRTABLE_PAT}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        return data["records"][0]


async def get_daily_total(uid: str) -> int:
    """Get today's total calories from Airtable"""
    try:
        # Get today's date range
        today = datetime.now().date()
        today_start = f"{today}T00:00:00.000Z"
        today_end = f"{today}T23:59:59.999Z"

        # Query Airtable with filter
        formula = f"AND(IS_AFTER({{Date}}, '{today_start}'), IS_BEFORE({{Date}}, '{today_end}'))"

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"https://api.airtable.com/v0/{AIRTABLE_BASE}/Food%20Log",
                headers={"Authorization": f"Bearer {AIRTABLE_PAT}"},
                params={"filterByFormula": formula}
            )

            if response.status_code == 200:
                data = response.json()
                records = data.get("records", [])
                total = sum(record["fields"].get("Calories", 0) for record in records)
                return total
            else:
                print(f"Error fetching daily total: {response.status_code}")
                return 0

    except Exception as e:
        print(f"Error getting daily total: {e}")
        return 0


def infer_meal_type() -> str:
    """Infer meal type based on time of day (IST)"""
    hour = datetime.now().hour

    if 6 <= hour < 11:
        return "Breakfast"
    elif 11 <= hour < 16:
        return "Lunch"
    elif 16 <= hour < 19:
        return "Snack"
    else:
        return "Dinner"


# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
