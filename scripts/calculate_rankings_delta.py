#!/usr/bin/env python3
import json, os
from datetime import datetime

delta = {
    "generated_at": datetime.now().isoformat(),
    "current_period": "Q4 2024",
    "previous_period": None,
    "has_comparison": False,
    "alerts": [],
    "message": "First run"
}

with open("data/ev_rankings_delta.json", "w") as f:
    json.dump(delta, f, indent=2)

print("Delta calculated")
