"""Opportunity Radar API - Main Application Module

This module contains the core application logic for the Opportunity Radar API,
including the unified data model, crawlers, normalizers, and aggregation pipeline.
"""

import hashlib
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

from pydantic import BaseModel, Field, field_validator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('opportunity_radar.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Unified Data Model
class Opportunity(BaseModel):
    """Unified data model for all opportunity types"""
    
    id: str = Field(default="", description="Unique identifier for the opportunity")
    type: str = Field(default="", description="Type of opportunity (jobs, freelance, hackathons, etc.)")
    title: str = Field(default="", description="Title of the opportunity")
    organization: str = Field(default="", description="Organization offering the opportunity")
    description: str = Field(default="", description="Description of the opportunity")
    location: str = Field(default="", description="Location of the opportunity")
    country: str = Field(default="", description="Country of the opportunity")
    reward: str = Field(default="", description="Reward or stipend information")
    deadline: str = Field(default="", description="Deadline for the opportunity")
    url: str = Field(default="", description="URL to the opportunity")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    source: str = Field(default="", description="Source of the opportunity")
    date_discovered: str = Field(default="", description="Date when the opportunity was discovered")
    last_updated: str = Field(default="", description="Last update timestamp")
    score: int = Field(default=0, description="Opportunity score for ranking")

    @field_validator('date_discovered', 'last_updated')
    @classmethod
    def validate_date_format(cls, v):
        """Validate date format"""
        if v and not v.startswith('20'):
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v

    @field_validator('score')
    @classmethod
    def validate_score(cls, v):
        """Validate score range"""
        if v < 0 or v > 100:
            raise ValueError('Score must be between 0 and 100')
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump()

    def get_duplicate_key(self) -> str:
        """Generate a unique key for deduplication"""
        normalized_title = self.title.lower().strip()
        normalized_org = self.organization.lower().strip()
        return hashlib.md5(
            f"{normalized_title}{normalized_org}{self.deadline}".encode()
        ).hexdigest()

    def calculate_freshness_score(self) -> float:
        """Calculate freshness score based on discovery date"""
        try:
            discovery_date = datetime.strptime(self.date_discovered, '%Y-%m-%d')
            days_ago = (datetime.now() - discovery_date).days
            return max(0, 100 - (days_ago * 2))
        except:
            return 50.0


class CrawlerConfig(BaseModel):
    """Configuration for crawlers"""
    
    name: str = Field(..., description="Name of the crawler")
    type: str = Field(..., description="Type of opportunity")
    base_url: str = Field(..., description="Base URL for the crawler")
    enabled: bool = Field(default=True, description="Whether the crawler is enabled")
    rate_limit: int = Field(default=60, description="Rate limit in seconds")
    timeout: int = Field(default=30, description="Timeout in seconds")
    max_pages: int = Field(default=10, description="Maximum pages to crawl")


class Crawler:
    """Base class for all crawlers"""
    
    def __init__(self, config: CrawlerConfig):
        self.config = config
        self.logger = logging.getLogger(f"crawler.{config.name}")
    
    async def crawl(self) -> List[Opportunity]:
        """Crawl for opportunities"""
        raise NotImplementedError("Subclasses must implement crawl method")
    
    def normalize(self, raw_data: Dict[str, Any]) -> Opportunity:
        """Normalize raw data to Opportunity object"""
        raise NotImplementedError("Subclasses must implement normalize method")
    
    def validate(self, opportunity: Opportunity) -> bool:
        """Validate opportunity data"""
        try:
            opportunity.model_dump()
            return True
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False


class Aggregator:
    """Aggregates opportunities from multiple sources"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def aggregate(self, opportunities: List[Opportunity]) -> List[Opportunity]:
        """Aggregate opportunities from multiple sources"""
        self.logger.info(f"Aggregating {len(opportunities)} opportunities")
        
        # Sort by freshness (newest first)
        opportunities.sort(
            key=lambda x: (
                x.date_discovered,
                x.last_updated,
                x.score
            ),
            reverse=True
        )
        
        return opportunities


class Deduplicator:
    """Removes duplicates from opportunities"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.seen_ids = set()
    
    def deduplicate(self, opportunities: List[Opportunity]) -> List[Opportunity]:
        """Remove duplicates from opportunities"""
        self.logger.info(f"Deduplicating {len(opportunities)} opportunities")
        
        unique_opportunities = []
        duplicates_removed = 0
        
        for opportunity in opportunities:
            opp_id = opportunity.get_duplicate_key()
            
            if opp_id not in self.seen_ids:
                self.seen_ids.add(opp_id)
                unique_opportunities.append(opportunity)
            else:
                duplicates_removed += 1
                self.logger.debug(f"Duplicate removed: {opportunity.title}")
        
        self.logger.info(f"Removed {duplicates_removed} duplicates")
        return unique_opportunities


class Storage:
    """Storage and persistence layer"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.history_dir = self.data_dir / "history"
        self.api_dir = self.data_dir / "api"
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.api_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
    
    def save_opportunities(self, opportunities: List[Opportunity], source: str = "current"):
        """Save opportunities to storage"""
        current_file = self.data_dir / f"{source}.json"
        with open(current_file, 'w', encoding='utf-8') as f:
            json.dump([opp.model_dump() for opp in opportunities], f, indent=2, ensure_ascii=False)
        
        history_file = self.history_dir / f"{datetime.now().strftime('%Y-%m-%d')}.json"
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump([opp.model_dump() for opp in opportunities], f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved {len(opportunities)} opportunities to {current_file}")
    
    def load_opportunities(self, source: str = "current") -> List[Opportunity]:
        """Load opportunities from storage"""
        file_path = self.data_dir / f"{source}.json"
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return [Opportunity(**opp) for opp in data]
    
    def get_history(self, days: int = 90) -> List[Opportunity]:
        """Get historical opportunities"""
        opportunities = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for history_file in self.history_dir.glob("*.json"):
            try:
                file_date = datetime.strptime(history_file.stem, '%Y-%m-%d')
                if file_date >= cutoff_date:
                    with open(history_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    opportunities.extend([Opportunity(**opp) for opp in data])
            except Exception as e:
                self.logger.error(f"Error loading history file {history_file}: {e}")
        
        return opportunities


class APIGenerator:
    """Generates static API endpoints"""
    
    def __init__(self, storage: Storage):
        self.storage = storage
        self.logger = logging.getLogger(__name__)
    
    def generate_opportunities_api(self, opportunities: List[Opportunity]):
        """Generate opportunities.json API endpoint"""
        api_file = self.storage.api_dir / "opportunities.json"
        
        by_type = {}
        for opp in opportunities:
            if opp.type not in by_type:
                by_type[opp.type] = []
            by_type[opp.type].append(opp.model_dump())
        
        for opp_type, opp_list in by_type.items():
            type_file = self.storage.api_dir / f"{opp_type}.json"
            with open(type_file, 'w', encoding='utf-8') as f:
                json.dump(opp_list, f, indent=2, ensure_ascii=False)
        
        with open(api_file, 'w', encoding='utf-8') as f:
            json.dump([opp.model_dump() for opp in opportunities], f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Generated API endpoints in {self.storage.api_dir}")
    
    def generate_trending_api(self, opportunities: List[Opportunity]):
        """Generate trending.json API endpoint"""
        scored_opps = []
        for opp in opportunities:
            freshness_score = opp.calculate_freshness_score()
            trending_score = (opp.score * 0.7) + (freshness_score * 0.3)
            scored_opps.append((opp, trending_score))
        
        scored_opps.sort(key=lambda x: x[1], reverse=True)
        
        trending_opps = [opp.model_dump() for opp, _ in scored_opps[:50]]
        
        trending_file = self.storage.api_dir / "trending.json"
        with open(trending_file, 'w', encoding='utf-8') as f:
            json.dump(trending_opps, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Generated trending API endpoint")
    
    def generate_deadlines_api(self, opportunities: List[Opportunity]):
        """Generate deadlines.json API endpoint"""
        deadlines = []
        
        for opp in opportunities:
            if opp.deadline:
                try:
                    deadline_date = datetime.strptime(opp.deadline, '%Y-%m-%d')
                    today = datetime.now()
                    days_left = (deadline_date - today).days
                    
                    if days_left >= 0:
                        deadline_info = {
                            "title": opp.title,
                            "organization": opp.organization,
                            "deadline": opp.deadline,
                            "days_left": days_left,
                            "url": opp.url,
                            "type": opp.type
                        }
                        deadlines.append(deadline_info)
                except Exception as e:
                    self.logger.error(f"Error parsing deadline for {opp.title}: {e}")
        
        deadlines.sort(key=lambda x: x['days_left'])
        
        deadlines_file = self.storage.api_dir / "deadlines.json"
        with open(deadlines_file, 'w', encoding='utf-8') as f:
            json.dump(deadlines, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Generated deadlines API endpoint")
    
    def generate_search_index(self, opportunities: List[Opportunity]):
        """Generate search-index.json API endpoint"""
        search_index = []
        
        for opp in opportunities:
            search_entry = {
                "title": opp.title,
                "organization": opp.organization,
                "tags": opp.tags,
                "type": opp.type,
                "url": opp.url,
                "description": opp.description[:200] + "..." if len(opp.description) > 200 else opp.description,
                "date_discovered": opp.date_discovered
            }
            search_index.append(search_entry)
        
        search_file = self.storage.api_dir / "search-index.json"
        with open(search_file, 'w', encoding='utf-8') as f:
            json.dump(search_index, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Generated search index API endpoint")


class OpportunityRadar:
    """Main application class"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.storage = Storage()
        self.aggregator = Aggregator()
        self.deduplicator = Deduplicator()
        self.api_generator = APIGenerator(self.storage)
        
        self.opportunities = self.storage.load_opportunities()
    
    def run(self):
        """Run the main application"""
        self.logger.info("Starting Opportunity Radar")
        self.logger.info(f"Loaded {len(self.opportunities)} existing opportunities")
        
        aggregated = self.aggregator.aggregate(self.opportunities)
        deduplicated = self.deduplicator.deduplicate(aggregated)
        
        self.api_generator.generate_opportunities_api(deduplicated)
        self.api_generator.generate_trending_api(deduplicated)
        self.api_generator.generate_deadlines_api(deduplicated)
        self.api_generator.generate_search_index(deduplicated)
        
        self.storage.save_opportunities(deduplicated, "current")
        
        self.logger.info("Opportunity Radar completed successfully")


if __name__ == "__main__":
    app = OpportunityRadar()
    app.run()