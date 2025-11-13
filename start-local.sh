#!/bin/bash
# Start webhook server locally for testing

set -e

echo "🚀 Starting Food Tracker Webhook Server (Local)..."
echo ""

# Check if in correct directory
if [ ! -f "webhook_server.py" ]; then
    echo "❌ Error: webhook_server.py not found!"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found! Run ./setup-webhook.sh first"
    exit 1
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "❌ .env file not found! Copy .env.example and fill in values"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Verify critical variables
if [ -z "$HEALTH_SHEET_ID" ]; then
    echo "⚠️  Warning: HEALTH_SHEET_ID not set in .env"
fi

echo ""
echo "📝 Configuration:"
echo "   Environment: ${ENVIRONMENT:-development}"
echo "   Port: ${PORT:-8000}"
echo "   Sheet ID: ${HEALTH_SHEET_ID:-NOT SET}"
echo "   Claude API: $([ -n "$CLAUDE_API_KEY" ] && echo 'Configured' || echo 'Using MCP')"
echo ""

echo "🌐 Server will be available at:"
echo "   Local: http://localhost:${PORT:-8000}"
echo "   Health: http://localhost:${PORT:-8000}/health"
echo "   Webhook: http://localhost:${PORT:-8000}/omi-webhook"
echo ""

echo "Press Ctrl+C to stop"
echo ""

# Start server
python3 webhook_server.py
