# EV Market Intelligence System

Automated system for collecting, analyzing, and visualizing electric vehicle market data.

## Features

- **News Collection**: Automated scraping of EV news from global sources
- **Rankings Management**: BEV and PHEV sales data tracking
- **Change Detection**: Delta calculation and significant change alerts
- **Interactive Dashboard**: React-based visualization of market trends
- **Automated Backup**: GitHub integration for data persistence

## Structure

```
ev-market-intelligence/
├── scripts/           # Python and shell scripts
├── data/             # Current data files (JSON)
├── dashboard/        # React dashboard application
├── history/          # Historical snapshots
├── logs/             # Execution logs
└── README.md
```

## Components

### 1. News Collector (`scripts/ev_news_collector.py`)
Collects EV news from the last 3-4 days covering:
- USA, Europe, Asia (ex-Japan), Japan markets
- Major manufacturers (Tesla, BYD, NIO, Xpeng, Li Auto, Geely, BMW, VW, etc.)
- Market-impacting events (sales, features, recalls, quality issues)

### 2. Rankings Generator (`scripts/create_corrected_rankings.py`)
Generates current rankings with:
- Clear BEV vs PHEV distinction
- Global rankings and regional breakdowns
- Revenue data and forecasts

### 3. Delta Calculator (`scripts/calculate_rankings_delta.py`)
Compares current data with previous reports:
- Sales volume changes
- Ranking position changes
- Significant change detection (>10K units or rank changes)

### 4. Dashboard (`dashboard/`)
React-based interactive dashboard displaying:
- Latest news by region
- Rankings tables
- Change indicators
- Historical trends

### 5. Update Script (`ev_intelligence_update.sh`)
Master script that orchestrates:
1. News collection
2. Rankings update
3. Delta calculation
4. Dashboard rebuild
5. GitHub backup

## Scheduling

Runs biweekly (Tuesday and Friday at 9:00 AM CET) via cron:
```
0 0 9 * * 2,5 /home/ubuntu/ev-market-intelligence/ev_intelligence_update.sh
```

## Data Sources

- Official manufacturer press releases
- CleanTechnica
- CnEVPost
- InsideEVs
- Electrek
- Regional EV news outlets

## Backup

Automatic GitHub backup after each update to:
https://github.com/robertogennaccari-1/ev-market-intelligence

## Logs

Execution logs stored in: `/home/ubuntu/ev-market-intelligence/logs/ev_update.log`

## Author

Managed by Manus AI Agent

