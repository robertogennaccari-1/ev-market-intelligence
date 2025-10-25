#!/bin/bash
set -e

PROJECT_DIR="/home/ubuntu/ev-market-intelligence"
DASHBOARD_DIR="/home/ubuntu/ev-news-dashboard"

echo "=== EV Intelligence Update ==="
cd "$PROJECT_DIR"

# Run scripts
python3 scripts/ev_news_collector.py
python3 scripts/create_corrected_rankings.py  
python3 scripts/calculate_rankings_delta.py

# Update dashboard
cp data/*.json "$DASHBOARD_DIR/client/public/"

# Backup to GitHub (token in remote URL)
git add -A
git diff --staged --quiet || git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main || echo "Push failed or no changes"

echo "=== Update Complete ==="
