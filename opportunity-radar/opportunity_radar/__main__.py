"""Main Application for Opportunity Radar API

This module orchestrates the entire Opportunity Radar pipeline:
1. Crawls all opportunity sources
2. Normalizes data
3. Deduplicates
4. Generates API endpoints
5. Updates historical snapshots
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import List

from opportunity_radar import (
    Opportunity,
    Aggregator,
    Deduplicator,
    Storage,
    APIGenerator,
    OpportunityRadar
)

# Import all crawlers
from opportunity_radar.crawlers.jobs import JobsCrawler
from opportunity_radar.crawlers.hackathons import HackathonsCrawler
from opportunity_radar.crawlers.competitions import CompetitionsCrawler
from opportunity_radar.crawlers.freelance import FreelanceCrawler
from opportunity_radar.crawlers.grants import GrantsCrawler
from opportunity_radar.crawlers.scholarships import ScholarshipsCrawler
from opportunity_radar.crawlers.startup_programs import StartupProgramsCrawler


class OpportunityRadarApp:
    """Main application class that orchestrates the entire pipeline"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.storage = Storage()
        self.aggregator = Aggregator()
        self.deduplicator = Deduplicator()
        self.api_generator = APIGenerator(self.storage)
        
        # Initialize all crawlers
        self.jobs_crawler = JobsCrawler()
        self.hackathons_crawler = HackathonsCrawler()
        self.competitions_crawler = CompetitionsCrawler()
        self.freelance_crawler = FreelanceCrawler()
        self.grants_crawler = GrantsCrawler()
        self.scholarships_crawler = ScholarshipsCrawler()
        self.startup_programs_crawler = StartupProgramsCrawler()
        
        # Load existing opportunities
        self.opportunities = self.storage.load_opportunities()
        self.logger.info(f"Loaded {len(self.opportunities)} existing opportunities")
    
    async def crawl_all_sources(self) -> List[Opportunity]:
        """Crawl all opportunity sources"""
        self.logger.info("Starting crawl of all opportunity sources")
        
        all_opportunities = []
        
        # Crawl jobs
        try:
            jobs = await self.jobs_crawler.crawl_all()
            all_opportunities.extend(jobs)
            self.logger.info(f"Found {len(jobs)} job opportunities")
        except Exception as e:
            self.logger.error(f"Error crawling jobs: {e}")
        
        # Crawl hackathons
        try:
            hackathons = await self.hackathons_crawler.crawl_all()
            all_opportunities.extend(hackathons)
            self.logger.info(f"Found {len(hackathons)} hackathon opportunities")
        except Exception as e:
            self.logger.error(f"Error crawling hackathons: {e}")
        
        # Crawl competitions
        try:
            competitions = await self.competitions_crawler.crawl_all()
            all_opportunities.extend(competitions)
            self.logger.info(f"Found {len(competitions)} competition opportunities")
        except Exception as e:
            self.logger.error(f"Error crawling competitions: {e}")
        
        # Crawl freelance
        try:
            freelance = await self.freelance_crawler.crawl_all()
            all_opportunities.extend(freelance)
            self.logger.info(f"Found {len(freelance)} freelance opportunities")
        except Exception as e:
            self.logger.error(f"Error crawling freelance: {e}")
        
        # Crawl grants
        try:
            grants = await self.grants_crawler.crawl_all()
            all_opportunities.extend(grants)
            self.logger.info(f"Found {len(grants)} grant opportunities")
        except Exception as e:
            self.logger.error(f"Error crawling grants: {e}")
        
        # Crawl scholarships
        try:
            scholarships = await self.scholarships_crawler.crawl_all()
            all_opportunities.extend(scholarships)
            self.logger.info(f"Found {len(scholarships)} scholarship opportunities")
        except Exception as e:
            self.logger.error(f"Error crawling scholarships: {e}")
        
        # Crawl startup programs
        try:
            startup_programs = await self.startup_programs_crawler.crawl_all()
            all_opportunities.extend(startup_programs)
            self.logger.info(f"Found {len(startup_programs)} startup program opportunities")
        except Exception as e:
            self.logger.error(f"Error crawling startup programs: {e}")
        
        self.logger.info(f"Total opportunities found: {len(all_opportunities)}")
        return all_opportunities
    
    def process_opportunities(self, opportunities: List[Opportunity]) -> List[Opportunity]:
        """Process opportunities through the pipeline"""
        # Add existing opportunities
        all_opportunities = self.opportunities + opportunities
        
        # Aggregate
        aggregated = self.aggregator.aggregate(all_opportunities)
        
        # Deduplicate
        deduplicated = self.deduplicator.deduplicate(aggregated)
        
        return deduplicated
    
    def generate_api(self, opportunities: List[Opportunity]):
        """Generate all API endpoints"""
        self.api_generator.generate_opportunities_api(opportunities)
        self.api_generator.generate_trending_api(opportunities)
        self.api_generator.generate_deadlines_api(opportunities)
        self.api_generator.generate_search_index(opportunities)
        
        # Generate individual type endpoints
        by_type = {}
        for opp in opportunities:
            if opp.type not in by_type:
                by_type[opp.type] = []
            by_type[opp.type].append(opp.model_dump())
        
        for opp_type, opp_list in by_type.items():
            api_file = self.storage.api_dir / f"{opp_type}.json"
            with open(api_file, 'w', encoding='utf-8') as f:
                json.dump(opp_list, f, indent=2, ensure_ascii=False)
    
    def update_history(self, opportunities: List[Opportunity]):
        """Update historical snapshots"""
        self.storage.save_opportunities(opportunities, "current")
    
    async def run(self):
        """Run the entire pipeline"""
        start_time = datetime.now()
        self.logger.info("Starting Opportunity Radar pipeline")
        
        # Crawl all sources
        crawled_opportunities = await self.crawl_all_sources()
        
        # Process opportunities
        processed_opportunities = self.process_opportunities(crawled_opportunities)
        
        # Generate API endpoints
        self.generate_api(processed_opportunities)
        
        # Update history
        self.update_history(processed_opportunities)
        
        # Log completion
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        self.logger.info(f"Pipeline completed in {duration:.2f} seconds")
        self.logger.info(f"Total opportunities processed: {len(processed_opportunities)}")


async def main():
    """Main entry point"""
    app = OpportunityRadarApp()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())