#!/usr/bin/env python3
import json, os
from datetime import datetime, timedelta

class EVNewsCollector:
    def __init__(self, output_dir="/home/ubuntu/ev-market-intelligence/data"):
        self.output_dir = output_dir
    
    def generate_mock_news(self):
        today = datetime.now()
        return [
            {
                "title": "Tesla Reports Record Q4 2024 Deliveries",
                "url": "https://example.com/tesla-q4-2024",
                "source": "CleanTechnica",
                "date": (today - timedelta(days=1)).isoformat(),
                "description": "Tesla delivered 495,000 vehicles in Q4 2024.",
                "region": "USA",
                "manufacturer": "Tesla",
                "category": "sales"
            },
            {
                "title": "BYD Surpasses 3 Million EV Sales in 2024",
                "url": "https://example.com/byd-3m-sales",
                "source": "CnEVPost",
                "date": (today - timedelta(days=2)).isoformat(),
                "description": "BYD becomes first automaker to sell 3 million EVs.",
                "region": "Asia_ex_Japan",
                "manufacturer": "BYD",
                "category": "sales"
            }
        ]
    
    def run(self):
        news = self.generate_mock_news()
        categorized = {"USA": [], "Europe": [], "Asia_ex_Japan": [], "Japan": [], "Global": []}
        for item in news:
            categorized[item["region"]].append(item)
        
        summaries = {region: f"{len(items)} articles" for region, items in categorized.items()}
        
        output = {
            "generated_at": datetime.now().isoformat(),
            "news_by_region": categorized,
            "regional_summaries": summaries,
            "total_articles": len(news)
        }
        
        os.makedirs(self.output_dir, exist_ok=True)
        with open(os.path.join(self.output_dir, "ev_news_latest.json"), "w") as f:
            json.dump(output, f, indent=2)
        
        return os.path.join(self.output_dir, "ev_news_latest.json")

if __name__ == "__main__":
    EVNewsCollector().run()
