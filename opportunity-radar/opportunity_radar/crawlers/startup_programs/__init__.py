"""Startup Programs Crawler for Opportunity Radar API"""
import asyncio
from typing import List, Dict, Any
from opportunity_radar import Crawler, CrawlerConfig, Opportunity


class YCombinatorCrawler(Crawler):
    """Crawler for Y Combinator startup accelerator"""

    async def crawl(self) -> List[Opportunity]:
        sample_data = {
            "id": "yc-001",
            "title": "Y Combinator Summer 2026",
            "organization": "Y Combinator",
            "description": "Join the most prestigious startup accelerator program.",
            "location": "Remote",
            "country": "Global",
            "reward": "$120,000 seed + mentorship",
            "deadline": "2026-09-15",
            "url": "https://www.ycombinator.com/apply/",
            "tags": ["accelerator", "startup", "yc", "seed-funding"],
            "source": "ycombinator",
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
            type="accelerators",
            title=raw_data.get("title", ""),
            organization=raw_data.get("organization", ""),
            description=raw_data.get("description", ""),
            location=raw_data.get("location", ""),
            country=raw_data.get("country", ""),
            reward=raw_data.get("reward", ""),
            deadline=raw_data.get("deadline", ""),
            url=raw_data.get("url", ""),
            tags=raw_data.get("tags", []),
            source=raw_data.get("source", "ycombinator"),
            date_discovered=raw_data.get("date_discovered", ""),
            last_updated=raw_data.get("last_updated", ""),
            score=raw_data.get("score", 0)
        )


class TechstarsCrawler(Crawler):
    """Crawler for Techstars startup accelerator"""

    async def crawl(self) -> List[Opportunity]:
        sample_data = {
            "id": "techstars-001",
            "title": "Techstars Accelerator Program",
            "organization": "Techstars",
            "description": "Mentorship-driven accelerator program for startups.",
            "location": "Various cities",
            "country": "Global",
            "reward": "$20,000 + mentorship",
            "deadline": "2026-08-01",
            "url": "https://www.techstars.com/apply",
            "tags": ["accelerator", "startup", "techstars", "mentorship"],
            "source": "techstars",
            "date_discovered": "2026-06-18",
            "last_updated": "2026-06-18",
            "score": 90
        }
        opportunity = self.normalize(sample_data)
        if self.validate(opportunity):
            return [opportunity]
        return []

    def normalize(self, raw_data: Dict[str, Any]) -> Opportunity:
        return Opportunity(
            id=raw_data.get("id", ""),
            type="accelerators",
            title=raw_data.get("title", ""),
            organization=raw_data.get("organization", ""),
            description=raw_data.get("description", ""),
            location=raw_data.get("location", ""),
            country=raw_data.get("country", ""),
            reward=raw_data.get("reward", ""),
            deadline=raw_data.get("deadline", ""),
            url=raw_data.get("url", ""),
            tags=raw_data.get("tags", []),
            source=raw_data.get("source", "techstars"),
            date_discovered=raw_data.get("date_discovered", ""),
            last_updated=raw_data.get("last_updated", ""),
            score=raw_data.get("score", 0)
        )


class StartupProgramsCrawler:
    """Main startup programs crawler that orchestrates all startup program crawlers"""

    def __init__(self):
        self.yc = YCombinatorCrawler(CrawlerConfig(
            name="ycombinator", type="accelerators", base_url="https://ycombinator.com", enabled=True
        ))
        self.techstars = TechstarsCrawler(CrawlerConfig(
            name="techstars", type="accelerators", base_url="https://techstars.com", enabled=True
        ))

    async def crawl_all(self) -> List[Opportunity]:
        opportunities = []
        for crawler in [self.yc, self.techstars]:
            if crawler.config.enabled:
                try:
                    crawled = await crawler.crawl()
                    opportunities.extend(crawled)
                except Exception as e:
                    print(f"Error crawling {crawler.config.name}: {e}")
        return opportunities