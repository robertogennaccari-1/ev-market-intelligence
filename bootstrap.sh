#!/bin/bash
# Bootstrap Script for EV Market Intelligence
# Sets up the environment and runs the update

set -e

# Configuration
REPO_URL="https://github.com/robertogennaccari-1/ev-market-intelligence.git"
WORK_DIR="/tmp/ev-intelligence-$(date +%s)"
DASHBOARD_REPO_DIR="/home/ubuntu/ev-news-dashboard"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "=== EV Market Intelligence Bootstrap Started ==="

# 1. Clone repository
log "Step 1/5: Cloning repository..."
git clone "$REPO_URL" "$WORK_DIR"
cd "$WORK_DIR"

# 2. Check Python dependencies
log "Step 2/5: Checking Python environment..."
python3 --version

# 3. Run update script
log "Step 3/5: Running update script..."
bash ev_intelligence_update.sh

# 4. Update dashboard if it exists
log "Step 4/5: Checking dashboard..."
if [ -d "$DASHBOARD_REPO_DIR" ]; then
    log "Dashboard found, updating data files..."
    cp data/*.json "$DASHBOARD_REPO_DIR/client/public/"
    log "✓ Dashboard data updated"
else
    log "⚠ Dashboard not found at $DASHBOARD_REPO_DIR"
fi

# 5. Cleanup
log "Step 5/5: Cleanup..."
cd /tmp
rm -rf "$WORK_DIR"

log "=== EV Market Intelligence Bootstrap Completed ==="

exit 0
