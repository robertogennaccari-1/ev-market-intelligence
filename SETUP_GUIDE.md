# EV Market Intelligence System - Setup Guide

## Overview

The **EV Market Intelligence System** is a comprehensive automated platform for tracking, analyzing, and visualizing the global electric vehicle market. The system collects news from international sources (including Chinese media with English translations), maintains detailed BEV/PHEV rankings, tracks changes over time, and presents everything through an interactive dashboard.

## System Architecture

### Components

The system consists of four main components:

1. **Data Collection Scripts** (Python)
   - News collector with multilingual support
   - Rankings generator with BEV/PHEV distinction
   - Delta calculator for change tracking

2. **Dashboard** (React + TypeScript)
   - Interactive web interface
   - Real-time data visualization
   - Responsive design with dark/light themes

3. **Automation Scripts** (Bash)
   - Update orchestration
   - Bootstrap for fresh deployments
   - Logging and error handling

4. **Persistence Layer** (GitHub)
   - Version control for code
   - Historical data snapshots
   - Automated backups

### Data Flow

```
┌─────────────────────────────────────────────────────────┐
│              SCHEDULED EXECUTION                         │
│           (Tuesday & Friday, 9:00 AM CET)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         1. CLONE REPOSITORY FROM GITHUB                  │
│    https://github.com/robertogennaccari-1/              │
│           ev-market-intelligence.git                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         2. COLLECT NEWS (Python)                         │
│  • Search global sources (last 3-4 days)                │
│  • Include Chinese sources with translations            │
│  • Categorize by region and manufacturer                │
│  • Output: data/ev_news_latest.json                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         3. GENERATE RANKINGS (Python)                    │
│  • Create BEV and PHEV rankings                         │
│  • Calculate market shares and totals                   │
│  • Regional breakdowns                                  │
│  • Output: data/ev_rankings_latest.json                 │
│           + history/ev_rankings_[timestamp].json        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         4. CALCULATE DELTA (Python)                      │
│  • Compare with previous period                         │
│  • Identify significant changes                         │
│  • Generate alerts                                      │
│  • Output: data/ev_rankings_delta.json                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         5. UPDATE DASHBOARD                              │
│  • Copy JSON files to dashboard public folder           │
│  • Dashboard auto-refreshes with new data               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         6. COMMIT TO GITHUB                              │
│  • Stage all changes                                    │
│  • Commit with timestamp                                │
│  • Push to origin/main (if credentials configured)      │
└─────────────────────────────────────────────────────────┘
```

## Installation & Setup

### Prerequisites

- **Python 3.11+** with packages:
  - Standard library only (no external dependencies currently)
  
- **Node.js 22+** with pnpm (for dashboard)

- **Git** with GitHub access

### Step 1: Clone Repository

```bash
cd /home/ubuntu
git clone https://github.com/robertogennaccari-1/ev-market-intelligence.git
cd ev-market-intelligence
```

### Step 2: Configure Git Credentials

For automated GitHub push, configure a Personal Access Token:

```bash
# Create token at: https://github.com/settings/tokens
# Required scopes: repo (full control)

git remote set-url origin https://YOUR_TOKEN@github.com/robertogennaccari-1/ev-market-intelligence.git
```

Alternatively, use SSH:

```bash
git remote set-url origin git@github.com:robertogennaccari-1/ev-market-intelligence.git
```

### Step 3: Setup Dashboard

The dashboard is a separate project that displays the data:

```bash
cd /home/ubuntu/ev-news-dashboard

# Install dependencies
pnpm install

# Copy initial data
cp /home/ubuntu/ev-market-intelligence/data/*.json client/public/

# Start dev server (for testing)
pnpm dev

# Build for production
pnpm build
```

### Step 4: Test Manual Execution

```bash
cd /home/ubuntu/ev-market-intelligence
bash ev_intelligence_update.sh
```

Expected output:
```
[2025-11-12 09:00:00] === EV Intelligence Update Started ===
[2025-11-12 09:00:01] Step 1/6: Collecting EV news...
[2025-11-12 09:00:02] ✓ News collection completed
[2025-11-12 09:00:02] Step 2/6: Generating rankings...
[2025-11-12 09:00:03] ✓ Rankings generation completed
[2025-11-12 09:00:03] Step 3/6: Calculating rankings delta...
[2025-11-12 09:00:04] ✓ Delta calculation completed
[2025-11-12 09:00:04] Step 4/6: Updating dashboard data...
[2025-11-12 09:00:04] ✓ Dashboard data updated
[2025-11-12 09:00:04] Step 5/6: Committing to GitHub...
[2025-11-12 09:00:05] ✓ Changes committed locally
[2025-11-12 09:00:05] ✓ Changes pushed to GitHub
[2025-11-12 09:00:05] Step 6/6: Generating summary...
[2025-11-12 09:00:05] Summary: 28 total alerts, 2 high severity
[2025-11-12 09:00:05] === EV Intelligence Update Completed Successfully ===
```

### Step 5: Configure Scheduled Execution

The system is designed to run biweekly (Tuesday and Friday at 9:00 AM CET).

**Option A: Using Manus Scheduler** (Recommended)

A scheduled task has been created: `ev-market-intelligence-update`

To enable it:
1. Upgrade your Manus account to access scheduling features
2. The task will run automatically on the configured schedule

**Option B: Using System Cron**

```bash
# Edit crontab
crontab -e

# Add this line (9:00 AM CET = 8:00 AM UTC in winter, 7:00 AM UTC in summer)
# Adjust for your timezone
0 8 * * 2,5 cd /home/ubuntu/ev-market-intelligence && bash ev_intelligence_update.sh >> logs/cron.log 2>&1
```

**Option C: Using Bootstrap Script**

For environments where the repository needs to be cloned fresh each time:

```bash
0 8 * * 2,5 bash /home/ubuntu/ev-market-intelligence/bootstrap.sh >> /tmp/ev-bootstrap.log 2>&1
```

## File Structure

```
ev-market-intelligence/
├── README.md                    # Project overview
├── ARCHITECTURE.md              # Architecture documentation
├── SETUP_GUIDE.md              # This file
├── .gitignore                  # Git ignore rules
│
├── scripts/                    # Python scripts
│   ├── ev_news_collector.py   # News collection
│   ├── create_corrected_rankings.py  # Rankings generation
│   └── calculate_rankings_delta.py   # Delta calculation
│
├── data/                       # Current data (JSON)
│   ├── ev_news_latest.json    # Latest news
│   ├── ev_rankings_latest.json # Current rankings
│   └── ev_rankings_delta.json  # Changes from previous
│
├── history/                    # Historical snapshots
│   └── ev_rankings_YYYYMMDD_HHMMSS.json
│
├── logs/                       # Execution logs
│   └── ev_update.log
│
├── ev_intelligence_update.sh   # Main update script
└── bootstrap.sh                # Bootstrap script
```

## Data Formats

### News Data (`ev_news_latest.json`)

```json
{
  "generated_at": "2025-11-12T09:00:00",
  "date_range": {
    "from": "2025-11-08T09:00:00",
    "to": "2025-11-12T09:00:00"
  },
  "news_by_region": {
    "USA": [...],
    "Europe": [...],
    "Asia_ex_Japan": [...],
    "Japan": [...],
    "Global": [...]
  },
  "regional_summaries": {
    "USA": "3 articles covering 2 manufacturers...",
    ...
  },
  "total_articles": 19
}
```

Each news item includes:
- `title`: English title
- `url`: Article URL
- `source`: Publication name
- `date`: Publication date (ISO 8601)
- `description`: English summary
- `region`: Geographic region
- `manufacturer`: Relevant manufacturer
- `category`: Type (sales, production, recall, etc.)
- `impact`: Significance level (high, medium, low)
- `original_language`: "zh" for Chinese, "en" for English
- `original_title`: Original Chinese title (if applicable)
- `original_url`: Original source URL

### Rankings Data (`ev_rankings_latest.json`)

```json
{
  "generated_at": "2025-11-12T09:00:00",
  "period": "Q4 2025",
  "bev_rankings": [
    {
      "rank": 1,
      "manufacturer": "BYD",
      "model": "Seagull",
      "sales_units": 425000,
      "revenue_usd_millions": 8500,
      "yoy_growth_percent": 145.5,
      "market_share_percent": 8.2,
      "regions": {
        "China": 420000,
        "Asia_ex_China": 5000,
        "Europe": 0,
        "USA": 0
      }
    },
    ...
  ],
  "phev_rankings": [...],
  "manufacturer_totals": {
    "BYD": {
      "bev": 710000,
      "phev": 663000,
      "total": 1373000
    },
    ...
  },
  "regional_breakdown": {...},
  "market_statistics": {
    "total_bev_sales": 2190000,
    "total_phev_sales": 1463000,
    "total_ev_sales": 3653000,
    "bev_market_share": 60.0,
    "phev_market_share": 40.0
  }
}
```

### Delta Data (`ev_rankings_delta.json`)

```json
{
  "generated_at": "2025-11-12T09:00:00",
  "current_period": "Q4 2025",
  "previous_period": "Q3 2025",
  "has_comparison": true,
  "bev_model_deltas": [
    {
      "manufacturer": "BYD",
      "model": "Seagull",
      "vehicle_type": "BEV",
      "current_rank": 1,
      "current_sales": 425000,
      "previous_rank": 1,
      "previous_sales": 385000,
      "rank_change": 0,
      "sales_change": 40000,
      "sales_change_percent": 10.4,
      "is_new_entry": false,
      "is_significant": true
    },
    ...
  ],
  "phev_model_deltas": [...],
  "manufacturer_deltas": [...],
  "alerts": [
    {
      "type": "sales_change",
      "severity": "high",
      "message": "BYD Seagull sales increased by 40,000 units (+10.4%)"
    },
    ...
  ],
  "summary": {
    "total_alerts": 28,
    "high_severity_alerts": 2,
    "significant_changes": 17,
    "new_entries": 8
  }
}
```

## Dashboard Features

The dashboard (`/home/ubuntu/ev-news-dashboard`) provides:

### 1. Overview Page
- Total EV sales (BEV + PHEV)
- Market share breakdown
- Recent news count
- Alert summary for significant changes
- Quick links to detailed sections

### 2. News Page
- Regional tabs (USA, Europe, Asia ex-Japan, Japan, Global)
- Regional summaries
- Article cards with:
  - English title and description
  - Original Chinese title (if applicable)
  - Source, date, manufacturer
  - Category and impact badges
  - External links

### 3. Rankings Page
- Separate tabs for BEV and PHEV
- Sortable tables with:
  - Current rank and changes
  - Sales units and revenue
  - Year-over-year growth
  - Market share
  - Change indicators (arrows, percentages)
- Visual highlighting for significant changes

### 4. Manufacturers Page
- Company comparison table
- Total sales (BEV + PHEV)
- BEV/PHEV mix visualization
- Change tracking
- Top performers cards

### Theme Support
- Dark mode (default)
- Light mode
- Switchable via UI

## Monitoring & Maintenance

### Logs

All execution logs are stored in `logs/ev_update.log`:

```bash
# View recent logs
tail -f /home/ubuntu/ev-market-intelligence/logs/ev_update.log

# Search for errors
grep "✗" /home/ubuntu/ev-market-intelligence/logs/ev_update.log

# Check alerts
grep "high severity" /home/ubuntu/ev-market-intelligence/logs/ev_update.log
```

### Historical Data

All ranking snapshots are preserved in `history/`:

```bash
# List all snapshots
ls -lh /home/ubuntu/ev-market-intelligence/history/

# View specific snapshot
cat /home/ubuntu/ev-market-intelligence/history/ev_rankings_20251112_090000.json | jq .
```

### Dashboard Status

Check if dashboard is serving updated data:

```bash
# Check file timestamps
ls -lh /home/ubuntu/ev-news-dashboard/client/public/*.json

# Verify dashboard is running
curl http://localhost:3000
```

## Troubleshooting

### Issue: Scripts fail with Python errors

**Solution**: Ensure Python 3.11+ is installed:
```bash
python3 --version
```

### Issue: Dashboard not updating

**Solution**: Manually copy data files:
```bash
cp /home/ubuntu/ev-market-intelligence/data/*.json \
   /home/ubuntu/ev-news-dashboard/client/public/
```

### Issue: GitHub push fails

**Solution**: Configure credentials:
```bash
# Check current remote
git remote -v

# Update with token
git remote set-url origin https://TOKEN@github.com/robertogennaccari-1/ev-market-intelligence.git
```

### Issue: No changes detected

**Solution**: This is normal if data hasn't changed. The system will commit only when there are actual updates.

### Issue: Scheduled task not running

**Solution**: 
1. Check if Manus scheduling is enabled (requires account upgrade)
2. Verify cron configuration: `crontab -l`
3. Check system time and timezone: `date`

## Advanced Configuration

### Customizing News Sources

Edit `scripts/ev_news_collector.py`:

```python
CHINESE_SOURCES = [
    "36kr.com",           # Tech/startup news
    "autohome.com.cn",    # Auto news
    "d1ev.com",           # EV focused
    "yicai.com",          # Financial news
    "cls.cn",             # Financial news
    # Add more sources here
]
```

### Adjusting Significance Thresholds

Edit `scripts/calculate_rankings_delta.py`:

```python
SIGNIFICANT_SALES_CHANGE = 10000  # Units
SIGNIFICANT_RANK_CHANGE = 2       # Positions
SIGNIFICANT_GROWTH_PERCENT = 50.0 # Percent
```

### Changing Update Frequency

Modify the cron expression in the scheduled task:

```bash
# Current: Tuesday and Friday at 9:00 AM
0 0 9 * * 2,5

# Daily at 9:00 AM
0 0 9 * * *

# Every Monday, Wednesday, Friday at 9:00 AM
0 0 9 * * 1,3,5
```

## Security Considerations

### GitHub Token

- Store token securely
- Use tokens with minimal required permissions (repo access only)
- Rotate tokens periodically
- Never commit tokens to repository

### Dashboard Access

The dashboard is currently configured for local access. To expose publicly:

1. Deploy to a hosting service (Vercel, Netlify, GitHub Pages)
2. Configure appropriate access controls
3. Consider adding authentication if needed

## Support & Resources

### Repository
- GitHub: https://github.com/robertogennaccari-1/ev-market-intelligence

### Key Files
- Main update script: `ev_intelligence_update.sh`
- Bootstrap script: `bootstrap.sh`
- Architecture doc: `ARCHITECTURE.md`

### Logs
- Update logs: `logs/ev_update.log`
- Cron logs: `/tmp/ev-bootstrap.log` (if using bootstrap)

## Version History

- **v1.0** (2025-11-12): Initial complete implementation
  - Python scripts for data collection and processing
  - React dashboard with full visualization
  - GitHub integration for persistence
  - Automated scheduling support
  - Chinese news sources with translations

---

**Maintained by**: Manus AI  
**Last Updated**: November 12, 2025
