#!/bin/bash
# Phone-Friendly Food Tracker Setup
# NO Claude Desktop needed!
# NO API keys needed!

echo "==========================================="
echo "📱 Phone-Friendly Food Tracker Setup"
echo "==========================================="
echo ""
echo "This works from your phone!"
echo "  ✅ Omi app (phone)"
echo "  ✅ Google Sheets app (phone)"
echo "  ✅ PC runs sync in background (can be off!)"
echo ""

# Check Sheet ID
if [ -z "$HEALTH_SHEET_ID" ]; then
    echo "⚠️  HEALTH_SHEET_ID not set!"
    echo ""
    echo "Please:"
    echo "1. Create Google Sheet on phone: 'Food_Tracker'"
    echo "2. Add tab: 'Meals'"
    echo "3. Columns: Date | Time | Food | Calories | Protein | Carbs | Fat"
    echo "4. Share -> Anyone with link can edit"
    echo "5. Copy Sheet ID from URL"
    echo ""
    read -p "Paste Sheet ID here: " sheet_id

    if [ -n "$sheet_id" ]; then
        echo "export HEALTH_SHEET_ID='$sheet_id'" >> ~/.bashrc
        export HEALTH_SHEET_ID="$sheet_id"
        echo "  ✅ Saved!"
    else
        echo "❌ No ID, exiting"
        exit 1
    fi
fi

echo ""
echo "📦 Installing requirements..."
pip3 install --user requests

echo ""
echo "⚙️  Creating auto-sync (runs every hour)..."

mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/phone-food-sync.service <<EOF
[Unit]
Description=Phone Food Tracker Sync

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /mnt/d/MCP/foodtracker/phone-food-sync.py
Environment="HEALTH_SHEET_ID=$HEALTH_SHEET_ID"
Environment="POKE_ENABLED=false"
StandardOutput=append:$HOME/.config/food-sync.log
StandardError=append:$HOME/.config/food-sync.log
EOF

cat > ~/.config/systemd/user/phone-food-sync.timer <<EOF
[Unit]
Description=Phone Food Sync Timer (hourly)

[Timer]
OnBootSec=5min
OnUnitActiveSec=1h
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl --user daemon-reload
systemctl --user enable phone-food-sync.timer
systemctl --user start phone-food-sync.timer

echo "  ✅ Auto-sync enabled (runs every hour)"

# Create manual sync
cat > /mnt/d/MCP/foodtracker/sync-now.sh <<'EOF'
#!/bin/bash
echo "🔄 Syncing food data..."
python3 /mnt/d/MCP/foodtracker/phone-food-sync.py
echo ""
echo "Check: ~/.config/food-log.csv"
EOF

chmod +x /mnt/d/MCP/foodtracker/sync-now.sh
chmod +x /mnt/d/MCP/foodtracker/phone-food-sync.py

# Create aliases
if ! grep -q "food-sync-now" ~/.bashrc; then
    echo "alias food-sync-now='/mnt/d/MCP/foodtracker/sync-now.sh'" >> ~/.bashrc
    echo "alias food-check='systemctl --user status phone-food-sync.timer'" >> ~/.bashrc
    echo "alias food-logs='tail -f ~/.config/food-sync.log'" >> ~/.bashrc
fi

echo ""
echo "==========================================="
echo "✅ Setup Complete!"
echo "==========================================="
echo ""
echo "What happens now:"
echo "  • Every hour: Auto-syncs Omi → CSV file"
echo "  • Data saved to: ~/.config/food-log.csv"
echo "  • NO Claude Desktop needed!"
echo "  • NO API keys needed!"
echo ""
echo "Commands:"
echo "  food-sync-now   - Sync right now"
echo "  food-check      - Check sync status"
echo "  food-logs       - View sync logs"
echo ""
echo "Phone use:"
echo "  1. Talk to Omi: 'I had chicken shawarma'"
echo "  2. Wait 3-5 min (Omi processing)"
echo "  3. Sync runs automatically every hour"
echo "  4. Check Google Sheets app on phone!"
echo ""
echo "Manual import to Sheets (one-time):"
echo "  1. Open Google Sheets on phone/PC"
echo "  2. File -> Import -> Upload"
echo "  3. Choose: ~/.config/food-log.csv"
echo "  4. Replace data or Append"
echo ""
echo "💡 Reload: source ~/.bashrc"
echo ""
