#!/bin/bash
# DEAD SIMPLE HEALTH COACH - SETUP
# Run once, then forget about it.

set -e

echo "🚀 Dead Simple Health Coach - Setup"
echo "===================================="
echo ""

# ============================================================================
# 1. CHECK REQUIREMENTS
# ============================================================================

echo "📋 Checking requirements..."

# Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    exit 1
fi
echo "  ✅ Python 3"

# Claude CLI
if ! command -v claude &> /dev/null; then
    echo "❌ Claude CLI not found!"
    echo "   Install from: https://docs.claude.com/en/docs/claude-code"
    exit 1
fi
echo "  ✅ Claude CLI"

# Google credentials
if [ ! -f "$HOME/.config/google-credentials.json" ]; then
    echo "❌ Google credentials not found!"
    echo "   Expected: $HOME/.config/google-credentials.json"
    exit 1
fi
echo "  ✅ Google credentials"

echo ""

# ============================================================================
# 2. INSTALL DEPENDENCIES
# ============================================================================

echo "📦 Installing Python dependencies..."

pip3 install --quiet --user \
    google-api-python-client \
    google-auth-httplib2 \
    google-auth-oauthlib \
    requests

echo "  ✅ Dependencies installed"
echo ""

# ============================================================================
# 3. CONFIGURE ENVIRONMENT
# ============================================================================

echo "⚙️  Configuration..."

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "❓ Google Sheet ID?"
    echo "   (from URL: docs.google.com/spreadsheets/d/YOUR_ID/edit)"
    read -p "   Sheet ID: " SHEET_ID

    cat > .env << EOF
# Health Coach Configuration
HEALTH_SHEET_ID=$SHEET_ID
OMI_API_KEY=omi_dev_2b7983a707b5ede131a0903a1655d918
POKE_API_KEY=pk_GH6UrWQ1JCpPzmsYTAX0LzNfGKn_TTQDquPUpAOujWM
GOOGLE_APPLICATION_CREDENTIALS=$HOME/.config/google-credentials.json
EOF

    echo "  ✅ Config saved to .env"
else
    echo "  ✅ .env already exists"
fi

# Load environment
export $(cat .env | grep -v '^#' | xargs)

echo ""

# ============================================================================
# 4. CREATE GOOGLE SHEETS STRUCTURE
# ============================================================================

echo "📊 Setting up Google Sheets..."

python3 << 'PYTHON'
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SHEET_ID = os.getenv('HEALTH_SHEET_ID')
CREDS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

credentials = service_account.Credentials.from_service_account_file(
    CREDS_PATH,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
service = build('sheets', 'v4', credentials=credentials)

# Create sheets structure
requests = []

# Sheet 1: Meals
requests.append({
    'addSheet': {
        'properties': {
            'title': 'Meals',
            'gridProperties': {'frozenRowCount': 1}
        }
    }
})

# Sheet 2: Workouts
requests.append({
    'addSheet': {
        'properties': {
            'title': 'Workouts',
            'gridProperties': {'frozenRowCount': 1}
        }
    }
})

# Sheet 3: Body Metrics
requests.append({
    'addSheet': {
        'properties': {
            'title': 'Body Metrics',
            'gridProperties': {'frozenRowCount': 1}
        }
    }
})

# Sheet 4: Recovery
requests.append({
    'addSheet': {
        'properties': {
            'title': 'Recovery',
            'gridProperties': {'frozenRowCount': 1}
        }
    }
})

# Sheet 5: Goals
requests.append({
    'addSheet': {
        'properties': {
            'title': 'Goals',
            'gridProperties': {'frozenRowCount': 1}
        }
    }
})

try:
    service.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID,
        body={'requests': requests}
    ).execute()
    print("  ✅ Sheets created")
except Exception as e:
    if 'already exists' in str(e):
        print("  ✅ Sheets already exist")
    else:
        print(f"  ⚠️  Error: {e}")

# Add headers
headers = {
    'Meals': [['Date', 'Time', 'Food', 'Portion', 'Calories', 'Protein (g)', 'Carbs (g)', 'Fat (g)', 'Meal Type', 'Notes']],
    'Workouts': [['Date', 'Time', 'Type', 'Muscle Groups', 'Exercises', 'Duration (min)', 'Energy (1-10)', 'Notes']],
    'Body Metrics': [['Date', 'Weight (kg)', 'Chest (cm)', 'Arms (cm)', 'Waist (cm)', 'Body Fat %', 'Notes']],
    'Recovery': [['Date', 'Sleep (hrs)', 'Sleep Quality (1-10)', 'Soreness Location', 'Soreness Severity', 'Stress Level', 'Notes']],
    'Goals': [['Goal Type', 'Target', 'Current', 'Start Date', 'Deadline', 'Progress', 'Status']]
}

for sheet_name, header in headers.items():
    try:
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=f'{sheet_name}!A1:Z1',
            valueInputOption='RAW',
            body={'values': header}
        ).execute()
    except:
        pass

# Add initial goal
initial_goals = [
    ['Weight', '60 kg', '54.9 kg', '2025-11-12', '2026-02-12', '0%', 'In Progress'],
    ['Calories/day', '2,850 cal', '- cal', '2025-11-12', 'Ongoing', '-', 'Active'],
    ['Protein/day', '120g', '- g', '2025-11-12', 'Ongoing', '-', 'Active']
]

try:
    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range='Goals!A:Z',
        valueInputOption='USER_ENTERED',
        body={'values': initial_goals}
    ).execute()
    print("  ✅ Initial goals added")
except:
    pass

PYTHON

echo ""

# ============================================================================
# 5. CREATE SYSTEMD SERVICE (AUTO-START)
# ============================================================================

echo "🤖 Setting up auto-start..."

SERVICE_FILE="$HOME/.config/systemd/user/health-coach.service"
mkdir -p "$HOME/.config/systemd/user"

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Dead Simple Health Coach
After=network.target

[Service]
Type=simple
WorkingDirectory=$(pwd)
ExecStart=$(which python3) $(pwd)/dead-simple-health-coach.py
Restart=on-failure
RestartSec=10
Environment="PATH=$PATH"
EnvironmentFile=$(pwd)/.env

[Install]
WantedBy=default.target
EOF

# Enable and start
systemctl --user daemon-reload
systemctl --user enable health-coach.service
systemctl --user start health-coach.service

echo "  ✅ Auto-start enabled"
echo ""

# ============================================================================
# 6. CREATE HELPER COMMANDS
# ============================================================================

echo "🔧 Creating helper commands..."

# Add to bashrc if not already there
if ! grep -q "health-coach commands" "$HOME/.bashrc"; then
    cat >> "$HOME/.bashrc" << 'EOF'

# Health coach commands
alias health-status='systemctl --user status health-coach.service'
alias health-restart='systemctl --user restart health-coach.service'
alias health-logs='journalctl --user -u health-coach.service -f'
alias health-stop='systemctl --user stop health-coach.service'
EOF

    echo "  ✅ Commands added to .bashrc"
    echo "     Run: source ~/.bashrc"
else
    echo "  ✅ Commands already in .bashrc"
fi

echo ""

# ============================================================================
# 7. FINAL STATUS
# ============================================================================

echo "✅ SETUP COMPLETE!"
echo "=================="
echo ""
echo "📱 YOUR WORKFLOW:"
echo "   1. Talk to Omi about EVERYTHING"
echo "   2. Script syncs automatically (every 15 min)"
echo "   3. Check Google Sheets on phone anytime"
echo "   4. Get Poke notifications 3x per day"
echo ""
echo "🎯 YOUR GOAL:"
echo "   54.9kg → 60kg in 12 weeks"
echo "   Target: 0.4kg/week (sustainable)"
echo "   End date: February 2026"
echo ""
echo "📊 GOOGLE SHEETS:"
echo "   https://docs.google.com/spreadsheets/d/$HEALTH_SHEET_ID"
echo ""
echo "🔧 COMMANDS:"
echo "   health-status  - Check if running"
echo "   health-logs    - View live logs"
echo "   health-restart - Restart service"
echo "   health-stop    - Stop service"
echo ""
echo "✅ Service is running! Talk to Omi now."
echo ""