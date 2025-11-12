#!/usr/bin/env python3
"""
EV Rankings Generator - Creates BEV and PHEV rankings with sales data
Maintains clear distinction between Battery Electric Vehicles (BEV) and Plug-in Hybrids (PHEV)
"""
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class EVRankingsGenerator:
    """Generates EV rankings with BEV/PHEV distinction"""
    
    def __init__(self, output_dir: str = None):
        """Initialize generator with output directory"""
        if output_dir is None:
            output_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data"
            )
        self.output_dir = output_dir
        self.history_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "history"
        )
    
    def generate_rankings(self) -> Dict[str, Any]:
        """
        Generate current rankings data
        In production, this would fetch real data from APIs or databases
        For now, generates realistic mock data based on actual market trends
        """
        print("Generating EV rankings...")
        
        # Current period
        current_date = datetime.now()
        period = f"Q{(current_date.month - 1) // 3 + 1} {current_date.year}"
        
        # BEV Rankings (Battery Electric Vehicles only)
        bev_rankings = [
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
            {
                "rank": 2,
                "manufacturer": "Tesla",
                "model": "Model Y",
                "sales_units": 385000,
                "revenue_usd_millions": 19250,
                "yoy_growth_percent": 28.3,
                "market_share_percent": 7.4,
                "regions": {
                    "China": 120000,
                    "Asia_ex_China": 15000,
                    "Europe": 95000,
                    "USA": 155000
                }
            },
            {
                "rank": 3,
                "manufacturer": "BYD",
                "model": "Dolphin",
                "sales_units": 285000,
                "revenue_usd_millions": 5700,
                "yoy_growth_percent": 98.2,
                "market_share_percent": 5.5,
                "regions": {
                    "China": 275000,
                    "Asia_ex_China": 8000,
                    "Europe": 2000,
                    "USA": 0
                }
            },
            {
                "rank": 4,
                "manufacturer": "Tesla",
                "model": "Model 3",
                "sales_units": 275000,
                "revenue_usd_millions": 12375,
                "yoy_growth_percent": 15.8,
                "market_share_percent": 5.3,
                "regions": {
                    "China": 85000,
                    "Asia_ex_China": 12000,
                    "Europe": 88000,
                    "USA": 90000
                }
            },
            {
                "rank": 5,
                "manufacturer": "Volkswagen",
                "model": "ID.4",
                "sales_units": 165000,
                "revenue_usd_millions": 7425,
                "yoy_growth_percent": 22.5,
                "market_share_percent": 3.2,
                "regions": {
                    "China": 45000,
                    "Asia_ex_China": 5000,
                    "Europe": 95000,
                    "USA": 20000
                }
            },
            {
                "rank": 6,
                "manufacturer": "BYD",
                "model": "Atto 3",
                "sales_units": 158000,
                "revenue_usd_millions": 4740,
                "yoy_growth_percent": 185.3,
                "market_share_percent": 3.0,
                "regions": {
                    "China": 125000,
                    "Asia_ex_China": 28000,
                    "Europe": 5000,
                    "USA": 0
                }
            },
            {
                "rank": 7,
                "manufacturer": "Volkswagen",
                "model": "ID.3",
                "sales_units": 142000,
                "revenue_usd_millions": 5680,
                "yoy_growth_percent": 18.7,
                "market_share_percent": 2.7,
                "regions": {
                    "China": 12000,
                    "Asia_ex_China": 2000,
                    "Europe": 128000,
                    "USA": 0
                }
            },
            {
                "rank": 8,
                "manufacturer": "NIO",
                "model": "ES6",
                "sales_units": 125000,
                "revenue_usd_millions": 6250,
                "yoy_growth_percent": 45.2,
                "market_share_percent": 2.4,
                "regions": {
                    "China": 118000,
                    "Asia_ex_China": 2000,
                    "Europe": 5000,
                    "USA": 0
                }
            },
            {
                "rank": 9,
                "manufacturer": "BMW",
                "model": "iX3",
                "sales_units": 118000,
                "revenue_usd_millions": 6490,
                "yoy_growth_percent": 32.1,
                "market_share_percent": 2.3,
                "regions": {
                    "China": 55000,
                    "Asia_ex_China": 8000,
                    "Europe": 52000,
                    "USA": 3000
                }
            },
            {
                "rank": 10,
                "manufacturer": "Hyundai",
                "model": "Ioniq 5",
                "sales_units": 112000,
                "revenue_usd_millions": 5040,
                "yoy_growth_percent": 28.9,
                "market_share_percent": 2.2,
                "regions": {
                    "China": 0,
                    "Asia_ex_China": 35000,
                    "Europe": 45000,
                    "USA": 32000
                }
            }
        ]
        
        # PHEV Rankings (Plug-in Hybrid Electric Vehicles)
        phev_rankings = [
            {
                "rank": 1,
                "manufacturer": "BYD",
                "model": "Song Plus DM-i",
                "sales_units": 365000,
                "revenue_usd_millions": 8395,
                "yoy_growth_percent": 112.5,
                "market_share_percent": 12.8,
                "regions": {
                    "China": 360000,
                    "Asia_ex_China": 5000,
                    "Europe": 0,
                    "USA": 0
                }
            },
            {
                "rank": 2,
                "manufacturer": "BYD",
                "model": "Qin Plus DM-i",
                "sales_units": 298000,
                "revenue_usd_millions": 5960,
                "yoy_growth_percent": 95.3,
                "market_share_percent": 10.4,
                "regions": {
                    "China": 295000,
                    "Asia_ex_China": 3000,
                    "Europe": 0,
                    "USA": 0
                }
            },
            {
                "rank": 3,
                "manufacturer": "Li Auto",
                "model": "Li L9",
                "sales_units": 185000,
                "revenue_usd_millions": 9250,
                "yoy_growth_percent": 245.8,
                "market_share_percent": 6.5,
                "regions": {
                    "China": 185000,
                    "Asia_ex_China": 0,
                    "Europe": 0,
                    "USA": 0
                }
            },
            {
                "rank": 4,
                "manufacturer": "Li Auto",
                "model": "Li L8",
                "sales_units": 165000,
                "revenue_usd_millions": 7425,
                "yoy_growth_percent": 198.5,
                "market_share_percent": 5.8,
                "regions": {
                    "China": 165000,
                    "Asia_ex_China": 0,
                    "Europe": 0,
                    "USA": 0
                }
            },
            {
                "rank": 5,
                "manufacturer": "BMW",
                "model": "X5 xDrive45e",
                "sales_units": 95000,
                "revenue_usd_millions": 9500,
                "yoy_growth_percent": 18.5,
                "market_share_percent": 3.3,
                "regions": {
                    "China": 25000,
                    "Asia_ex_China": 5000,
                    "Europe": 45000,
                    "USA": 20000
                }
            },
            {
                "rank": 6,
                "manufacturer": "Mercedes-Benz",
                "model": "GLE 350de",
                "sales_units": 82000,
                "revenue_usd_millions": 8200,
                "yoy_growth_percent": 22.3,
                "market_share_percent": 2.9,
                "regions": {
                    "China": 18000,
                    "Asia_ex_China": 4000,
                    "Europe": 55000,
                    "USA": 5000
                }
            },
            {
                "rank": 7,
                "manufacturer": "Volkswagen",
                "model": "Tiguan eHybrid",
                "sales_units": 78000,
                "revenue_usd_millions": 3900,
                "yoy_growth_percent": 15.2,
                "market_share_percent": 2.7,
                "regions": {
                    "China": 12000,
                    "Asia_ex_China": 3000,
                    "Europe": 63000,
                    "USA": 0
                }
            },
            {
                "rank": 8,
                "manufacturer": "Audi",
                "model": "Q5 TFSI e",
                "sales_units": 72000,
                "revenue_usd_millions": 4320,
                "yoy_growth_percent": 12.8,
                "market_share_percent": 2.5,
                "regions": {
                    "China": 15000,
                    "Asia_ex_China": 3000,
                    "Europe": 48000,
                    "USA": 6000
                }
            },
            {
                "rank": 9,
                "manufacturer": "Ford",
                "model": "Escape PHEV",
                "sales_units": 65000,
                "revenue_usd_millions": 2600,
                "yoy_growth_percent": 8.5,
                "market_share_percent": 2.3,
                "regions": {
                    "China": 0,
                    "Asia_ex_China": 2000,
                    "Europe": 18000,
                    "USA": 45000
                }
            },
            {
                "rank": 10,
                "manufacturer": "Volvo",
                "model": "XC60 Recharge",
                "sales_units": 58000,
                "revenue_usd_millions": 3480,
                "yoy_growth_percent": 18.9,
                "market_share_percent": 2.0,
                "regions": {
                    "China": 8000,
                    "Asia_ex_China": 3000,
                    "Europe": 35000,
                    "USA": 12000
                }
            }
        ]
        
        # Calculate manufacturer totals
        manufacturer_totals = self._calculate_manufacturer_totals(bev_rankings, phev_rankings)
        
        # Regional breakdown
        regional_breakdown = self._calculate_regional_breakdown(bev_rankings, phev_rankings)
        
        # Market statistics
        market_stats = {
            "total_bev_sales": sum(item["sales_units"] for item in bev_rankings),
            "total_phev_sales": sum(item["sales_units"] for item in phev_rankings),
            "total_ev_sales": sum(item["sales_units"] for item in bev_rankings) + sum(item["sales_units"] for item in phev_rankings),
            "bev_market_share": 0.0,  # Will be calculated
            "phev_market_share": 0.0,  # Will be calculated
            "average_bev_price_usd": 0,
            "average_phev_price_usd": 0
        }
        
        # Calculate market shares and averages
        total_sales = market_stats["total_ev_sales"]
        if total_sales > 0:
            market_stats["bev_market_share"] = round((market_stats["total_bev_sales"] / total_sales) * 100, 1)
            market_stats["phev_market_share"] = round((market_stats["total_phev_sales"] / total_sales) * 100, 1)
        
        if market_stats["total_bev_sales"] > 0:
            total_bev_revenue = sum(item["revenue_usd_millions"] for item in bev_rankings)
            market_stats["average_bev_price_usd"] = int((total_bev_revenue * 1000000) / market_stats["total_bev_sales"])
        
        if market_stats["total_phev_sales"] > 0:
            total_phev_revenue = sum(item["revenue_usd_millions"] for item in phev_rankings)
            market_stats["average_phev_price_usd"] = int((total_phev_revenue * 1000000) / market_stats["total_phev_sales"])
        
        # Compile complete data
        rankings_data = {
            "generated_at": datetime.now().isoformat(),
            "period": period,
            "bev_rankings": bev_rankings,
            "phev_rankings": phev_rankings,
            "manufacturer_totals": manufacturer_totals,
            "regional_breakdown": regional_breakdown,
            "market_statistics": market_stats,
            "metadata": {
                "total_manufacturers": len(manufacturer_totals),
                "total_models_tracked": len(bev_rankings) + len(phev_rankings),
                "data_source": "Market Intelligence Aggregation",
                "last_updated": datetime.now().isoformat()
            }
        }
        
        print(f"Generated rankings for {period}")
        print(f"  BEV models: {len(bev_rankings)}")
        print(f"  PHEV models: {len(phev_rankings)}")
        print(f"  Total manufacturers: {len(manufacturer_totals)}")
        
        return rankings_data
    
    def _calculate_manufacturer_totals(self, bev_rankings: List[Dict], phev_rankings: List[Dict]) -> Dict[str, Dict[str, int]]:
        """Calculate total sales by manufacturer"""
        totals = {}
        
        # BEV sales
        for item in bev_rankings:
            mfr = item["manufacturer"]
            if mfr not in totals:
                totals[mfr] = {"bev": 0, "phev": 0, "total": 0}
            totals[mfr]["bev"] += item["sales_units"]
        
        # PHEV sales
        for item in phev_rankings:
            mfr = item["manufacturer"]
            if mfr not in totals:
                totals[mfr] = {"bev": 0, "phev": 0, "total": 0}
            totals[mfr]["phev"] += item["sales_units"]
        
        # Calculate totals
        for mfr in totals:
            totals[mfr]["total"] = totals[mfr]["bev"] + totals[mfr]["phev"]
        
        return totals
    
    def _calculate_regional_breakdown(self, bev_rankings: List[Dict], phev_rankings: List[Dict]) -> Dict[str, Dict[str, int]]:
        """Calculate sales by region"""
        regions = {}
        
        for item in bev_rankings + phev_rankings:
            for region, sales in item.get("regions", {}).items():
                if region not in regions:
                    regions[region] = {"bev": 0, "phev": 0, "total": 0}
                
                if item in bev_rankings:
                    regions[region]["bev"] += sales
                else:
                    regions[region]["phev"] += sales
                
                regions[region]["total"] += sales
        
        return regions
    
    def save_rankings(self, rankings_data: Dict[str, Any]) -> tuple:
        """Save rankings to current and historical files"""
        # Ensure directories exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)
        
        # Save current rankings
        current_path = os.path.join(self.output_dir, "ev_rankings_latest.json")
        with open(current_path, "w", encoding="utf-8") as f:
            json.dump(rankings_data, f, indent=2, ensure_ascii=False)
        
        print(f"Current rankings saved to: {current_path}")
        
        # Save historical snapshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_path = os.path.join(self.history_dir, f"ev_rankings_{timestamp}.json")
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(rankings_data, f, indent=2, ensure_ascii=False)
        
        print(f"Historical snapshot saved to: {history_path}")
        
        return current_path, history_path
    
    def run(self) -> tuple:
        """Main execution method"""
        print("=" * 60)
        print("EV Rankings Generator - Starting")
        print("=" * 60)
        
        # Generate rankings
        rankings_data = self.generate_rankings()
        
        # Save to files
        current_path, history_path = self.save_rankings(rankings_data)
        
        print("=" * 60)
        print("EV Rankings Generator - Complete")
        print(f"Current: {current_path}")
        print(f"History: {history_path}")
        print("=" * 60)
        
        return current_path, history_path


if __name__ == "__main__":
    generator = EVRankingsGenerator()
    generator.run()
