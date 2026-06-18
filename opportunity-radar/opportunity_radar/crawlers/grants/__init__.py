"""Grants Crawler for Opportunity Radar API

This module contains crawlers for grant opportunities.
"""

import asyncio
from typing import List, Dict, Any

from opportunity_radar import Crawler, CrawlerConfig, Opportunity


class GrantsCrawler:
    """Main grants crawler for grant opportunities"""
    
    async def crawl_all(self) -> List[Opportunity]:
        """Crawl grant platforms for opportunities"""
        opportunities = []
        
        # In a real implementation, this would scrape grant platforms
        # For now, return sample data
        sample_data = {
            "id": "grant-001",
            "title": "National Science Foundation Research Grant",
            "organization": "National Science Foundation",
            "description": "Support innovative research in computer science...",
            "location": "USA",
            "country": "USA",
            "reward": "$500,000 - $1,000,000",
            "deadline": "2026-08-15",
            "url": "https://www.nsf.gov/funding/",
            "tags": ["research", "grant", "funding", "science"],
            "source": "nsf",
            "date_discovered": "2026-06-18",
            "last_updated": "2026-06-18",
            "score": 90
        }
        
        try:
            opportunity = Opportunity(
                id=sample_data.get("id", ""),
                type="grants",
                title=sample_data.get("title", ""),
                organization=sample_data.get("organization", ""),
                description=sample_data.get("description", ""),
                location=sample_data.get("location", ""),
                country=sample_data.get("country", ""),
                reward=sample_data.get("reward", ""),
                deadline=sample_data.get("deadline", ""),
                url=sample_data.get("url", ""),
                tags=sample_data.get("tags", []),
                source=sample_data.get("source", "nsf"),
                date_discovered=sample_data.get("date_discovered", ""),
                last_updated=sample_data.get("last_updated", ""),
                score=sample_data.get("score", 0)
            )
            opportunities.append(opportunity)
        except Exception as e:
            print(f"Error validating grant opportunity: {e}")
        
        return opportunities