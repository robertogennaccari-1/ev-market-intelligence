#!/usr/bin/env python3
"""
EV Rankings Delta Calculator - Compares current rankings with previous period
Identifies significant changes in sales volumes and rankings
"""
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import glob

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class RankingsDeltaCalculator:
    """Calculates changes between ranking periods"""
    
    # Thresholds for significant changes
    SIGNIFICANT_SALES_CHANGE = 10000  # Units
    SIGNIFICANT_RANK_CHANGE = 2  # Positions
    SIGNIFICANT_GROWTH_PERCENT = 50.0  # Percent
    
    def __init__(self, data_dir: str = None, history_dir: str = None):
        """Initialize calculator with data directories"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        if data_dir is None:
            data_dir = os.path.join(base_dir, "data")
        if history_dir is None:
            history_dir = os.path.join(base_dir, "history")
        
        self.data_dir = data_dir
        self.history_dir = history_dir
    
    def load_current_rankings(self) -> Optional[Dict[str, Any]]:
        """Load current rankings data"""
        current_path = os.path.join(self.data_dir, "ev_rankings_latest.json")
        
        if not os.path.exists(current_path):
            print(f"Warning: Current rankings not found at {current_path}")
            return None
        
        with open(current_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def load_previous_rankings(self) -> Optional[Dict[str, Any]]:
        """Load most recent historical rankings (excluding current)"""
        # Get all historical files
        pattern = os.path.join(self.history_dir, "ev_rankings_*.json")
        history_files = sorted(glob.glob(pattern), reverse=True)
        
        if len(history_files) < 2:
            print("Info: Not enough historical data for comparison")
            return None
        
        # Skip the most recent (which is current) and load the second most recent
        previous_path = history_files[1]
        print(f"Loading previous rankings from: {os.path.basename(previous_path)}")
        
        with open(previous_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def calculate_model_deltas(self, current: List[Dict], previous: List[Dict], vehicle_type: str) -> List[Dict[str, Any]]:
        """Calculate changes for individual models"""
        deltas = []
        
        # Create lookup for previous data
        prev_lookup = {f"{item['manufacturer']}_{item['model']}": item for item in previous}
        
        for curr_item in current:
            key = f"{curr_item['manufacturer']}_{curr_item['model']}"
            prev_item = prev_lookup.get(key)
            
            delta = {
                "manufacturer": curr_item["manufacturer"],
                "model": curr_item["model"],
                "vehicle_type": vehicle_type,
                "current_rank": curr_item["rank"],
                "current_sales": curr_item["sales_units"],
                "previous_rank": prev_item["rank"] if prev_item else None,
                "previous_sales": prev_item["sales_units"] if prev_item else None,
                "rank_change": None,
                "sales_change": None,
                "sales_change_percent": None,
                "is_new_entry": prev_item is None,
                "is_significant": False
            }
            
            if prev_item:
                # Calculate changes
                delta["rank_change"] = prev_item["rank"] - curr_item["rank"]  # Positive = improved
                delta["sales_change"] = curr_item["sales_units"] - prev_item["sales_units"]
                
                if prev_item["sales_units"] > 0:
                    delta["sales_change_percent"] = round(
                        (delta["sales_change"] / prev_item["sales_units"]) * 100, 1
                    )
                
                # Check if significant
                if (abs(delta["sales_change"]) >= self.SIGNIFICANT_SALES_CHANGE or
                    abs(delta["rank_change"]) >= self.SIGNIFICANT_RANK_CHANGE or
                    (delta["sales_change_percent"] and abs(delta["sales_change_percent"]) >= self.SIGNIFICANT_GROWTH_PERCENT)):
                    delta["is_significant"] = True
            else:
                # New entry is always significant
                delta["is_significant"] = True
            
            deltas.append(delta)
        
        return deltas
    
    def calculate_manufacturer_deltas(self, current_totals: Dict, previous_totals: Dict) -> List[Dict[str, Any]]:
        """Calculate changes for manufacturers"""
        deltas = []
        
        all_manufacturers = set(current_totals.keys()) | set(previous_totals.keys())
        
        for mfr in all_manufacturers:
            curr = current_totals.get(mfr, {"bev": 0, "phev": 0, "total": 0})
            prev = previous_totals.get(mfr, {"bev": 0, "phev": 0, "total": 0})
            
            delta = {
                "manufacturer": mfr,
                "current_total": curr["total"],
                "previous_total": prev["total"],
                "total_change": curr["total"] - prev["total"],
                "current_bev": curr["bev"],
                "previous_bev": prev["bev"],
                "bev_change": curr["bev"] - prev["bev"],
                "current_phev": curr["phev"],
                "previous_phev": prev["phev"],
                "phev_change": curr["phev"] - prev["phev"],
                "is_new": mfr not in previous_totals,
                "is_significant": False
            }
            
            # Calculate percent change
            if prev["total"] > 0:
                delta["total_change_percent"] = round(
                    (delta["total_change"] / prev["total"]) * 100, 1
                )
            else:
                delta["total_change_percent"] = None
            
            # Check if significant
            if abs(delta["total_change"]) >= self.SIGNIFICANT_SALES_CHANGE:
                delta["is_significant"] = True
            
            deltas.append(delta)
        
        # Sort by current total sales
        deltas.sort(key=lambda x: x["current_total"], reverse=True)
        
        return deltas
    
    def generate_alerts(self, model_deltas: List[Dict], manufacturer_deltas: List[Dict]) -> List[Dict[str, str]]:
        """Generate alerts for significant changes"""
        alerts = []
        
        # Model alerts
        for delta in model_deltas:
            if not delta["is_significant"]:
                continue
            
            if delta["is_new_entry"]:
                alerts.append({
                    "type": "new_entry",
                    "severity": "info",
                    "message": f"New entry: {delta['manufacturer']} {delta['model']} ({delta['vehicle_type']}) at rank #{delta['current_rank']} with {delta['current_sales']:,} units"
                })
            elif delta["rank_change"] and abs(delta["rank_change"]) >= self.SIGNIFICANT_RANK_CHANGE:
                direction = "up" if delta["rank_change"] > 0 else "down"
                alerts.append({
                    "type": "rank_change",
                    "severity": "medium",
                    "message": f"{delta['manufacturer']} {delta['model']} moved {direction} {abs(delta['rank_change'])} positions to rank #{delta['current_rank']}"
                })
            
            if delta["sales_change"] and abs(delta["sales_change"]) >= self.SIGNIFICANT_SALES_CHANGE:
                direction = "increased" if delta["sales_change"] > 0 else "decreased"
                alerts.append({
                    "type": "sales_change",
                    "severity": "high" if abs(delta["sales_change"]) > 50000 else "medium",
                    "message": f"{delta['manufacturer']} {delta['model']} sales {direction} by {abs(delta['sales_change']):,} units ({delta['sales_change_percent']:+.1f}%)"
                })
        
        # Manufacturer alerts
        for delta in manufacturer_deltas:
            if delta["is_new"]:
                alerts.append({
                    "type": "new_manufacturer",
                    "severity": "info",
                    "message": f"New manufacturer: {delta['manufacturer']} with {delta['current_total']:,} total units"
                })
            elif delta["is_significant"]:
                direction = "increased" if delta["total_change"] > 0 else "decreased"
                percent_str = f" ({delta['total_change_percent']:+.1f}%)" if delta["total_change_percent"] else ""
                alerts.append({
                    "type": "manufacturer_change",
                    "severity": "high",
                    "message": f"{delta['manufacturer']} total sales {direction} by {abs(delta['total_change']):,} units{percent_str}"
                })
        
        return alerts
    
    def calculate_delta(self) -> Dict[str, Any]:
        """Main delta calculation"""
        print("Calculating rankings delta...")
        
        # Load data
        current = self.load_current_rankings()
        previous = self.load_previous_rankings()
        
        if not current:
            return {
                "generated_at": datetime.now().isoformat(),
                "has_comparison": False,
                "error": "Current rankings not found",
                "alerts": []
            }
        
        if not previous:
            return {
                "generated_at": datetime.now().isoformat(),
                "current_period": current.get("period"),
                "previous_period": None,
                "has_comparison": False,
                "message": "No previous data available for comparison",
                "alerts": []
            }
        
        # Calculate deltas
        bev_deltas = self.calculate_model_deltas(
            current.get("bev_rankings", []),
            previous.get("bev_rankings", []),
            "BEV"
        )
        
        phev_deltas = self.calculate_model_deltas(
            current.get("phev_rankings", []),
            previous.get("phev_rankings", []),
            "PHEV"
        )
        
        manufacturer_deltas = self.calculate_manufacturer_deltas(
            current.get("manufacturer_totals", {}),
            previous.get("manufacturer_totals", {})
        )
        
        # Generate alerts
        all_model_deltas = bev_deltas + phev_deltas
        alerts = self.generate_alerts(all_model_deltas, manufacturer_deltas)
        
        # Compile delta data
        delta_data = {
            "generated_at": datetime.now().isoformat(),
            "current_period": current.get("period"),
            "previous_period": previous.get("period"),
            "has_comparison": True,
            "bev_model_deltas": bev_deltas,
            "phev_model_deltas": phev_deltas,
            "manufacturer_deltas": manufacturer_deltas,
            "alerts": alerts,
            "summary": {
                "total_alerts": len(alerts),
                "high_severity_alerts": len([a for a in alerts if a["severity"] == "high"]),
                "significant_changes": len([d for d in all_model_deltas if d["is_significant"]]),
                "new_entries": len([d for d in all_model_deltas if d["is_new_entry"]])
            }
        }
        
        print(f"Comparison: {previous.get('period')} → {current.get('period')}")
        print(f"  Significant changes: {delta_data['summary']['significant_changes']}")
        print(f"  Total alerts: {delta_data['summary']['total_alerts']}")
        
        return delta_data
    
    def save_delta(self, delta_data: Dict[str, Any]) -> str:
        """Save delta data to file"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        output_path = os.path.join(self.data_dir, "ev_rankings_delta.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(delta_data, f, indent=2, ensure_ascii=False)
        
        print(f"Delta saved to: {output_path}")
        return output_path
    
    def run(self) -> str:
        """Main execution method"""
        print("=" * 60)
        print("EV Rankings Delta Calculator - Starting")
        print("=" * 60)
        
        # Calculate delta
        delta_data = self.calculate_delta()
        
        # Save to file
        output_path = self.save_delta(delta_data)
        
        # Print alerts
        if delta_data.get("alerts"):
            print("\nAlerts:")
            for alert in delta_data["alerts"][:10]:  # Show first 10
                print(f"  [{alert['severity'].upper()}] {alert['message']}")
            
            if len(delta_data["alerts"]) > 10:
                print(f"  ... and {len(delta_data['alerts']) - 10} more")
        
        print("=" * 60)
        print("EV Rankings Delta Calculator - Complete")
        print(f"Output: {output_path}")
        print("=" * 60)
        
        return output_path


if __name__ == "__main__":
    calculator = RankingsDeltaCalculator()
    calculator.run()
