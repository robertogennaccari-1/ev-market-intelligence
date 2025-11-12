#!/bin/bash
# EV Market Intelligence Update Script
# Runs biweekly to collect news, update rankings, and deploy dashboard

set -e

# Configuration
PROJECT_DIR="/home/ubuntu/ev-market-intelligence"
DASHBOARD_DIR="/home/ubuntu/ev-news-dashboard"
LOG_FILE="$PROJECT_DIR/logs/ev_update.log"

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_DIR/logs"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== EV Intelligence Update Started ==="

# Change to project directory
cd "$PROJECT_DIR"

# 1. Run news collector
log "Step 1/6: Collecting EV news..."
if python3 scripts/ev_news_collector.py >> "$LOG_FILE" 2>&1; then
    log "✓ News collection completed"
else
    log "✗ News collection failed"
    exit 1
fi

# 2. Generate rankings
log "Step 2/6: Generating rankings..."
if python3 scripts/create_corrected_rankings.py >> "$LOG_FILE" 2>&1; then
    log "✓ Rankings generation completed"
else
    log "✗ Rankings generation failed"
    exit 1
fi

# 3. Calculate delta
log "Step 3/6: Calculating rankings delta..."
if python3 scripts/calculate_rankings_delta.py >> "$LOG_FILE" 2>&1; then
    log "✓ Delta calculation completed"
else
    log "✗ Delta calculation failed"
    exit 1
fi

# 4. Update dashboard data
log "Step 4/6: Updating dashboard data..."
if [ -d "$DASHBOARD_DIR" ]; then
    cp data/*.json "$DASHBOARD_DIR/client/public/"
    log "✓ Dashboard data updated"
else
    log "⚠ Dashboard directory not found, skipping dashboard update"
fi

# 5. Commit to GitHub (optional, requires credentials)
log "Step 5/6: Committing to GitHub..."
git add -A
if git diff --staged --quiet; then
    log "⚠ No changes to commit"
else
    git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE" 2>&1
    log "✓ Changes committed locally"
    # Push only if credentials are configured
    if git config --get remote.origin.url | grep -q "@"; then
        if git push origin main >> "$LOG_FILE" 2>&1; then
            log "✓ Changes pushed to GitHub"
        else
            log "⚠ Push to GitHub failed (will retry next run)"
        fi
    else
        log "⚠ GitHub push skipped (credentials not configured)"
        log "  To enable: git remote set-url origin https://TOKEN@github.com/robertogennaccari-1/ev-market-intelligence.git"
    fi
fi

# 6. Generate summary
log "Step 6/6: Generating summary..."
if [ -f "data/ev_rankings_delta.json" ]; then
    TOTAL_ALERTS=$(python3 -c "import json; data=json.load(open('data/ev_rankings_delta.json')); print(data.get('summary', {}).get('total_alerts', 0))")
    HIGH_SEVERITY=$(python3 -c "import json; data=json.load(open('data/ev_rankings_delta.json')); print(data.get('summary', {}).get('high_severity_alerts', 0))")
    log "Summary: $TOTAL_ALERTS total alerts, $HIGH_SEVERITY high severity"
fi

log "=== EV Intelligence Update Completed Successfully ==="
log ""

exit 0
