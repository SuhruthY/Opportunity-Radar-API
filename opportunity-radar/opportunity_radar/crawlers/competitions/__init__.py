"""Competitions Crawler for Opportunity Radar API

This module contains crawlers for competition opportunities.
"""

import asyncio
from typing import List, Dict, Any

from opportunity_radar import Crawler, CrawlerConfig, Opportunity


class KaggleCrawler(Crawler):
    """Crawler for Kaggle competitions"""
    
    async def crawl(self) -> List[Opportunity]:
        """Crawl Kaggle for competition opportunities"""
        opportunities = []
        
        # In a real implementation, this would scrape Kaggle
        # For now, return sample data
        sample_data = {
            "id": "kaggle-001",
            "title": "Titanic Survival Prediction Challenge",
            "organization": "Kaggle",
            "description": "Predict passenger survival on the Titanic...",
            "location": "Online",
            "country": "Global",
            "reward": "$5,000 prize + $1,000 runner-up",
            "deadline": "2026-07-10",
            "url": "https://kaggle.com/competitions/titanic",
            "tags": ["machine-learning", "data-science", "kaggle", "competition"],
            "source": "kaggle",
            "date_discovered": "2026-06-18",
            "last_updated": "2026-06-18",
            "score": 85
        }
        
        opportunity = self.normalize(sample_data)
        if self.validate(opportunity):
            opportunities.append(opportunity)
        
        return opportunities
    
    def normalize(self, raw_data: Dict[str, Any]) -> Opportunity:
        """Normalize Kaggle data"""
        return Opportunity(
            id=raw_data.get("id", ""),
            type="competitions",
            title=raw_data.get("title", ""),
            organization=raw_data.get("organization", ""),
            description=raw_data.get("description", ""),
            location=raw_data.get("location", ""),
            country=raw_data.get("country", ""),
            reward=raw_data.get("reward", ""),
            deadline=raw_data.get("deadline", ""),
            url=raw_data.get("url", ""),
            tags=raw_data.get("tags", []),
            source=raw_data.get("source", "kaggle"),
            date_discovered=raw_data.get("date_discovered", ""),
            last_updated=raw_data.get("last_updated", ""),
            score=raw_data.get("score", 0)
        )


class CompetitionsCrawler:
    """Main competitions crawler that orchestrates all competition crawlers"""
    
    def __init__(self):
        self.kaggle = KaggleCrawler(CrawlerConfig(
            name="kaggle",
            type="competitions",
            base_url="https://kaggle.com",
            enabled=True
        ))
    
    async def crawl_all(self) -> List[Opportunity]:
        """Crawl all competition platforms"""
        crawlers = [
            self.kaggle
        ]
        
        opportunities = []
        
        for crawler in crawlers:
            if crawler.config.enabled:
                try:
                    crawled = await crawler.crawl()
                    opportunities.extend(crawled)
                    print(f"Crawled {len(crawled)} opportunities from {crawler.config.name}")
                except Exception as e:
                    print(f"Error crawling {crawler.config.name}: {e}")
        
        return opportunities