"""Hackathons Crawler for Opportunity Radar API"""
import asyncio
from typing import List, Dict, Any
from opportunity_radar import Crawler, CrawlerConfig, Opportunity


class DevpostCrawler(Crawler):
    """Crawler for Devpost hackathons"""

    async def crawl(self) -> List[Opportunity]:
        sample_data = {
            "id": "devpost-001",
            "title": "AI-Powered Healthcare Hackathon",
            "organization": "Devpost",
            "description": "Build innovative healthcare solutions using AI.",
            "location": "Online",
            "country": "Global",
            "reward": "$10,000 prize + mentorship",
            "deadline": "2026-06-30",
            "url": "https://devpost.com/hackathons",
            "tags": ["ai", "healthcare", "machine-learning", "hackathon"],
            "source": "devpost",
            "date_discovered": "2026-06-18",
            "last_updated": "2026-06-18",
            "score": 95
        }
        opportunity = self.normalize(sample_data)
        if self.validate(opportunity):
            return [opportunity]
        return []

    def normalize(self, raw_data: Dict[str, Any]) -> Opportunity:
        return Opportunity(
            id=raw_data.get("id", ""),
            type="hackathons",
            title=raw_data.get("title", ""),
            organization=raw_data.get("organization", ""),
            description=raw_data.get("description", ""),
            location=raw_data.get("location", ""),
            country=raw_data.get("country", ""),
            reward=raw_data.get("reward", ""),
            deadline=raw_data.get("deadline", ""),
            url=raw_data.get("url", ""),
            tags=raw_data.get("tags", []),
            source=raw_data.get("source", "devpost"),
            date_discovered=raw_data.get("date_discovered", ""),
            last_updated=raw_data.get("last_updated", ""),
            score=raw_data.get("score", 0)
        )


class HackathonsCrawler:
    """Main hackathons crawler that orchestrates all hackathon crawlers"""

    def __init__(self):
        self.devpost = DevpostCrawler(CrawlerConfig(
            name="devpost", type="hackathons", base_url="https://devpost.com", enabled=True
        ))

    async def crawl_all(self) -> List[Opportunity]:
        opportunities = []
        for crawler in [self.devpost]:
            if crawler.config.enabled:
                try:
                    crawled = await crawler.crawl()
                    opportunities.extend(crawled)
                except Exception as e:
                    print(f"Error crawling {crawler.config.name}: {e}")
        return opportunities