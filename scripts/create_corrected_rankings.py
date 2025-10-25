#!/usr/bin/env python3
import json, os
from datetime import datetime

data = {
    "generated_at": datetime.now().isoformat(),
    "period": "Q3 2025",
    "bev_rankings": [
        {"rank": 1, "manufacturer": "BYD", "model": "Seagull", "sales_units": 425000, "revenue_usd_millions": 8500, "yoy_growth_percent": 145.5},
        {"rank": 2, "manufacturer": "Tesla", "model": "Model Y", "sales_units": 385000, "revenue_usd_millions": 19250, "yoy_growth_percent": 28.3}
    ],
    "phev_rankings": [
        {"rank": 1, "manufacturer": "BYD", "model": "Song Plus DM-i", "sales_units": 365000, "revenue_usd_millions": 8395, "yoy_growth_percent": 112.5}
    ],
    "manufacturer_totals": {
        "BYD": {"bev": 710000, "phev": 663000, "total": 1373000},
        "Tesla": {"bev": 705000, "phev": 0, "total": 705000}
    }
}

os.makedirs("data", exist_ok=True)
os.makedirs("history", exist_ok=True)

with open("data/ev_rankings_latest.json", "w") as f:
    json.dump(data, f, indent=2)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"history/ev_rankings_{timestamp}.json", "w") as f:
    json.dump(data, f, indent=2)

print("Rankings generated")
