"""Jobs Crawler for Opportunity Radar API

This module contains crawlers for job opportunities from various platforms.
"""

import asyncio
import json
from typing import List, Dict, Any
from urllib.parse import urljoin

from opportunity_radar import Crawler, CrawlerConfig, Opportunity


class GreenhouseCrawler(Crawler):
    """Crawler for Greenhouse job board"""
    
    async def crawl(self) -> List[Opportunity]:
        """Crawl Greenhouse for job opportunities"""
        opportunities = []
        
        # In a real implementation, this would scrape Greenhouse
        # For now, return sample data
        sample_data = {
            "id": "greenhouse-001",
            "title": "Senior Software Engineer",
            "organization": "TechCorp",
            "description": "We are looking for a senior software engineer...",
            "location": "San Francisco, CA",
            "country": "USA",
            "reward": "$120,000 - $180,000",
            "deadline": "2026-07-15",
            "url": "https://boards.greenhouse.io/",
            "tags": ["python", "javascript", "aws"],
            "source": "greenhouse",
            "date_discovered": "2026-06-18",
            "last_updated": "2026-06-18",
            "score": 85
        }
        
        opportunity = self.normalize(sample_data)
        if self.validate(opportunity):
            opportunities.append(opportunity)
        
        return opportunities
    
    def normalize(self, raw_data: Dict[str, Any]) -> Opportunity:
        """Normalize Greenhouse data"""
        return Opportunity(
            id=raw_data.get("id", ""),
            type="jobs",
            title=raw_data.get("title", ""),
            organization=raw_data.get("organization", ""),
            description=raw_data.get("description", ""),
            location=raw_data.get("location", ""),
            country=raw_data.get("country", ""),
            reward=raw_data.get("reward", ""),
            deadline=raw_data.get("deadline", ""),
            url=raw_data.get("url", ""),
            tags=raw_data.get("tags", []),
            source=raw_data.get("source", "greenhouse"),
            date_discovered=raw_data.get("date_discovered", ""),
            last_updated=raw_data.get("last_updated", ""),
            score=raw_data.get("score", 0)
        )


class LeverCrawler(Crawler):
    """Crawler for Lever job board"""
    
    async def crawl(self) -> List[Opportunity]:
        """Crawl Lever for job opportunities"""
        opportunities = []
        
        # In a real implementation, this would scrape Lever
        # For now, return sample data
        sample_data = {
            "id": "lever-001",
            "title": "Product Manager",
            "organization": "InnovateTech",
            "description": "We are looking for a product manager...",
            "location": "New York, NY",
            "country": "USA",
            "reward": "$110,000 - $150,000",
            "deadline": "2026-07-20",
            "url": "https://jobs.lever.co/",
            "tags": ["product", "agile", "scrum"],
            "source": "lever",
            "date_discovered": "2026-06-18",
            "last_updated": "2026-06-18",
            "score": 90
        }
        
        opportunity = self.normalize(sample_data)
        if self.validate(opportunity):
            opportunities.append(opportunity)
        
        return opportunities
    
    def normalize(self, raw_data: Dict[str, Any]) -> Opportunity:
        """Normalize Lever data"""
        return Opportunity(
            id=raw_data.get("id", ""),
            type="jobs",
            title=raw_data.get("title", ""),
            organization=raw_data.get("organization", ""),
            description=raw_data.get("description", ""),
            location=raw_data.get("location", ""),
            country=raw_data.get("country", ""),
            reward=raw_data.get("reward", ""),
            deadline=raw_data.get("deadline", ""),
            url=raw_data.get("url", ""),
            tags=raw_data.get("tags", []),
            source=raw_data.get("source", "lever"),
            date_discovered=raw_data.get("date_discovered", ""),
            last_updated=raw_data.get("last_updated", ""),
            score=raw_data.get("score", 0)
        )


class AshbyCrawler(Crawler):
    """Crawler for Ashby job board"""
    
    async def crawl(self) -> List[Opportunity]:
        """Crawl Ashby for job opportunities"""
        opportunities = []
        
        # In a real implementation, this would scrape Ashby
        # For now, return sample data
        sample_data = {
            "id": "ashby-001",
            "title": "Data Scientist",
            "organization": "DataDriven",
            "description": "We are looking for a data scientist...",
            "location": "Remote",
            "country": "Global",
            "reward": "$100,000 - $140,000",
            "deadline": "2026-07-25",
            "url": "https://ashbyhq.com/jobs",
            "tags": ["python", "machine-learning", "sql"],
            "source": "ashby",
            "date_discovered": "2026-06-18",
            "last_updated": "2026-06-18",
            "score": 80
        }
        
        opportunity = self.normalize(sample_data)
        if self.validate(opportunity):
            opportunities.append(opportunity)
        
        return opportunities
    
    def normalize(self, raw_data: Dict[str, Any]) -> Opportunity:
        """Normalize Ashby data"""
        return Opportunity(
            id=raw_data.get("id", ""),
            type="jobs",
            title=raw_data.get("title", ""),
            organization=raw_data.get("organization", ""),
            description=raw_data.get("description", ""),
            location=raw_data.get("location", ""),
            country=raw_data.get("country", ""),
            reward=raw_data.get("reward", ""),
            deadline=raw_data.get("deadline", ""),
            url=raw_data.get("url", ""),
            tags=raw_data.get("tags", []),
            source=raw_data.get("source", "ashby"),
            date_discovered=raw_data.get("date_discovered", ""),
            last_updated=raw_data.get("last_updated", ""),
            score=raw_data.get("score", 0)
        )


class WorkdayCrawler(Crawler):
    """Crawler for Workday job board"""
    
    async def crawl(self) -> List[Opportunity]:
        """Crawl Workday for job opportunities"""
        opportunities = []
        
        # In a real implementation, this would scrape Workday
        # For now, return sample data
        sample_data = {
            "id": "workday-001",
            "title": "UX Designer",
            "organization": "DesignStudio",
            "description": "We are looking for a UX designer...",
            "location": "Seattle, WA",
            "country": "USA",
            "reward": "$90,000 - $120,000",
            "deadline": "2026-08-01",
            "url": "https://www.myworkdayjobs.com/",
            "tags": ["ux", "design", "figma", "sketch"],
            "source": "workday",
            "date_discovered": "2026-06-18",
            "last_updated": "2026-06-18",
            "score": 75
        }
        
        opportunity = self.normalize(sample_data)
        if self.validate(opportunity):
            opportunities.append(opportunity)
        
        return opportunities
    
    def normalize(self, raw_data: Dict[str, Any]) -> Opportunity:
        """Normalize Workday data"""
        return Opportunity(
            id=raw_data.get("id", ""),
            type="jobs",
            title=raw_data.get("title", ""),
            organization=raw_data.get("organization", ""),
            description=raw_data.get("description", ""),
            location=raw_data.get("location", ""),
            country=raw_data.get("country", ""),
            reward=raw_data.get("reward", ""),
            deadline=raw_data.get("deadline", ""),
            url=raw_data.get("url", ""),
            tags=raw_data.get("tags", []),
            source=raw_data.get("source", "workday"),
            date_discovered=raw_data.get("date_discovered", ""),
            last_updated=raw_data.get("last_updated", ""),
            score=raw_data.get("score", 0)
        )


class JobsCrawler:
    """Main jobs crawler that orchestrates all job board crawlers"""
    
    def __init__(self):
        self.greenhouse = GreenhouseCrawler(CrawlerConfig(
            name="greenhouse",
            type="jobs",
            base_url="https://greenhouse.io",
            enabled=True
        ))
        
        self.lever = LeverCrawler(CrawlerConfig(
            name="lever",
            type="jobs",
            base_url="https://lever.co",
            enabled=True
        ))
        
        self.ashby = AshbyCrawler(CrawlerConfig(
            name="ashby",
            type="jobs",
            base_url="https://ashby.co",
            enabled=True
        ))
        
        self.workday = WorkdayCrawler(CrawlerConfig(
            name="workday",
            type="jobs",
            base_url="https://workday.com",
            enabled=True
        ))
    
    async def crawl_all(self) -> List[Opportunity]:
        """Crawl all job boards"""
        crawlers = [
            self.greenhouse,
            self.lever,
            self.ashby,
            self.workday
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