#!/bin/bash
# SIMPLE SETUP - No API keys needed!
# Uses your Claude Desktop subscription instead

set -e

echo "=================================="
echo "🚀 Simple Omi Sync Setup"
echo "=================================="
echo ""
echo "This uses:"
echo "  ✅ Your Claude Desktop subscription (no API!)"
echo "  ✅ Your Omi device"
echo "  ✅ Google Sheets (free)"
echo ""
echo "No Gemini API, no complexity!"
echo ""

# Check if HEALTH_SHEET_ID is set
if [ -z "$HEALTH_SHEET_ID" ]; then
    echo "⚠️  HEALTH_SHEET_ID not set!"
    echo ""
    echo "Please:"
    echo "1. Create a Google Sheet named 'My_Health_Tracker'"
    echo "2. Add a tab called 'Meals' with columns:"
    echo "   Date | Time | Food | Calories | Protein | Carbs | Fat | Notes"
    echo "3. Copy the Sheet ID from the URL"
    echo ""
    read -p "Enter your Google Sheet ID now: " sheet_id

    if [ -n "$sheet_id" ]; then
        echo "export HEALTH_SHEET_ID='$sheet_id'" >> ~/.bashrc
        export HEALTH_SHEET_ID="$sheet_id"
        echo "  ✅ Saved to ~/.bashrc"
    else
        echo "❌ No Sheet ID provided, exiting"
        exit 1
    fi
else
    echo "✅ Sheet ID found: $HEALTH_SHEET_ID"
fi

echo ""
echo "📦 Installing Python dependencies..."
pip3 install --user requests

echo ""
echo "⚙️  Creating hourly timer..."

# Create timer using systemd
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/simple-omi-sync.service <<EOF
[Unit]
Description=Simple Omi to Sheets Sync

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /mnt/d/MCP/simple-omi-sync.py
Environment="HEALTH_SHEET_ID=$HEALTH_SHEET_ID"
StandardOutput=append:$HOME/.config/simple-sync.log
StandardError=append:$HOME/.config/simple-sync.log
EOF

cat > ~/.config/systemd/user/simple-omi-sync.timer <<EOF
[Unit]
Description=Simple Omi Sync Timer (every hour)

[Timer]
OnBootSec=5min
OnUnitActiveSec=1h
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Reload and start
systemctl --user daemon-reload
systemctl --user enable simple-omi-sync.timer
systemctl --user start simple-omi-sync.timer

echo "  ✅ Timer created and started"

# Create manual sync script
cat > /mnt/d/MCP/sync-now.sh <<'EOF'
#!/bin/bash
echo "🔄 Syncing Omi data now..."
python3 /mnt/d/MCP/simple-omi-sync.py
EOF

chmod +x /mnt/d/MCP/sync-now.sh
chmod +x /mnt/d/MCP/simple-omi-sync.py

# Create aliases
if ! grep -q "alias sync-now" ~/.bashrc; then
    echo "alias sync-now='/mnt/d/MCP/sync-now.sh'" >> ~/.bashrc
    echo "alias check-sync='systemctl --user status simple-omi-sync.timer'" >> ~/.bashrc
    echo "alias view-logs='tail -f ~/.config/simple-sync.log'" >> ~/.bashrc
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "What happens now:"
echo "  • Every hour: Auto-syncs Omi → Sheets"
echo "  • Uses Claude Desktop (your subscription!)"
echo "  • No API keys needed"
echo ""
echo "Commands:"
echo "  sync-now       - Sync right now (manual)"
echo "  check-sync     - Check if timer is running"
echo "  view-logs      - See what's being logged"
echo ""
echo "Test it:"
echo "  1. Say to Omi: 'I had a banana'"
echo "  2. Wait 3 minutes (Omi processing)"
echo "  3. Run: sync-now"
echo "  4. Check your Google Sheet!"
echo ""
echo "📊 Your sheet: https://docs.google.com/spreadsheets/d/$HEALTH_SHEET_ID/edit"
echo ""
echo "💡 Reload shell: source ~/.bashrc"
echo ""
