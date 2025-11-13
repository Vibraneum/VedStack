#!/bin/bash
# Setup script for Food Tracker Webhook Server
# Run this once to set up everything

set -e  # Exit on error

echo "🚀 Setting up Scalable Food Tracker Webhook..."
echo ""

# Check if running in correct directory
if [ ! -f "webhook_server.py" ]; then
    echo "❌ Error: webhook_server.py not found!"
    echo "Please run this script from /mnt/d/MCP/foodtracker/"
    exit 1
fi

# Check Python version
echo "📝 Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found! Please install Python 3.8+"
    exit 1
fi

# Create virtual environment
echo ""
echo "🐍 Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env exists
echo ""
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your:"
    echo "   - HEALTH_SHEET_ID (from Google Sheets URL)"
    echo "   - CLAUDE_API_KEY (optional, from https://console.anthropic.com/)"
    echo "   - WEBHOOK_SECRET (generate random string)"
else
    echo "✅ .env file exists"
fi

# Check Google credentials
echo ""
if [ ! -f "$HOME/.config/google-credentials.json" ]; then
    echo "⚠️  Google credentials not found at: $HOME/.config/google-credentials.json"
    echo "   Please ensure you have set up Google Sheets API credentials"
else
    echo "✅ Google credentials found"
fi

# Create log directory
echo ""
echo "📁 Creating log directory..."
mkdir -p /tmp
echo "✅ Log directory ready"

# Test import
echo ""
echo "🧪 Testing imports..."
python3 -c "import fastapi; import anthropic; import google.oauth2" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ All dependencies imported successfully"
else
    echo "⚠️  Some imports failed, but continuing..."
fi

echo ""
echo "============================================"
echo "✅ Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env file with your credentials:"
echo "   nano .env"
echo ""
echo "2. Start the server locally:"
echo "   ./start-local.sh"
echo ""
echo "3. Test with ngrok (for Omi webhook):"
echo "   ./test-with-ngrok.sh"
echo ""
echo "4. Deploy to cloud (Railway or Render):"
echo "   See DEPLOYMENT_GUIDE.md"
echo ""
