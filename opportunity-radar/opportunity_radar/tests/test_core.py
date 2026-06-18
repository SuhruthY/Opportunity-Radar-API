"""Tests for Opportunity Radar API

This module contains unit tests and integration tests for the Opportunity Radar API.
"""

import asyncio
import json
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List

import pytest
from pydantic import ValidationError

from opportunity_radar import (
    Opportunity,
    CrawlerConfig,
    Aggregator,
    Deduplicator,
    Storage,
    APIGenerator
)


class TestOpportunityModel:
    """Test the Opportunity data model"""
    
    def test_valid_opportunity(self):
        """Test creating a valid opportunity"""
        opportunity = Opportunity(
            id="test-001",
            type="jobs",
            title="Test Job",
            organization="Test Company",
            description="Test description",
            location="Test Location",
            country="USA",
            reward="$100,000",
            deadline="2026-07-15",
            url="https://example.com",
            tags=["python", "testing"],
            source="test",
            date_discovered="2026-06-18",
            last_updated="2026-06-18",
            score=85
        )
        
        assert opportunity.id == "test-001"
        assert opportunity.type == "jobs"
        assert opportunity.title == "Test Job"
        assert opportunity.organization == "Test Company"
        assert opportunity.score == 85
    
    def test_opportunity_validation_failure(self):
        """Test opportunity validation failure"""
        with pytest.raises(ValidationError):
            Opportunity(
                id="test-002",
                type="jobs",
                title="Test Job",
                organization="Test Company",
                description="Test description",
                location="Test Location",
                country="USA",
                reward="$100,000",
                deadline="2026-07-15",
                url="https://example.com",
                tags=["python", "testing"],
                source="test",
                date_discovered="invalid-date",
                last_updated="2026-06-18",
                score=150  # Invalid score
            )
    
    def test_opportunity_duplicate_key(self):
        """Test duplicate key generation"""
        opp1 = Opportunity(
            id="test-003",
            type="jobs",
            title="Test Job",
            organization="Test Company",
            description="Test description",
            location="Test Location",
            country="USA",
            reward="$100,000",
            deadline="2026-07-15",
            url="https://example.com",
            tags=["python", "testing"],
            source="test",
            date_discovered="2026-06-18",
            last_updated="2026-06-18",
            score=85
        )
        
        opp2 = Opportunity(
            id="test-004",
            type="jobs",
            title="Test Job",  # Same title
            organization="Test Company",  # Same organization
            description="Test description",
            location="Test Location",
            country="USA",
            reward="$100,000",
            deadline="2026-07-15",  # Same deadline
            url="https://example.com",
            tags=["python", "testing"],
            source="test",
            date_discovered="2026-06-18",
            last_updated="2026-06-18",
            score=85
        )
        
        assert opp1.get_duplicate_key() == opp2.get_duplicate_key()
    
    def test_opportunity_freshness_score(self):
        """Test freshness score calculation"""
        opportunity = Opportunity(
            id="test-005",
            type="jobs",
            title="Test Job",
            organization="Test Company",
            description="Test description",
            location="Test Location",
            country="USA",
            reward="$100,000",
            deadline="2026-07-15",
            url="https://example.com",
            tags=["python", "testing"],
            source="test",
            date_discovered="2026-06-18",  # Today
            last_updated="2026-06-18",
            score=85
        )
        
        freshness = opportunity.calculate_freshness_score()
        assert freshness >= 100
    
    def test_opportunity_to_dict(self):
        """Test opportunity to_dict method"""
        opportunity = Opportunity(
            id="test-006",
            type="jobs",
            title="Test Job",
            organization="Test Company",
            description="Test description",
            location="Test Location",
            country="USA",
            reward="$100,000",
            deadline="2026-07-15",
            url="https://example.com",
            tags=["python", "testing"],
            source="test",
            date_discovered="2026-06-18",
            last_updated="2026-06-18",
            score=85
        )
        
        data = opportunity.to_dict()
        assert isinstance(data, dict)
        assert data["id"] == "test-006"
        assert data["title"] == "Test Job"
        assert data["score"] == 85


class TestCrawlerConfig:
    """Test the CrawlerConfig model"""
    
    def test_valid_config(self):
        """Test creating a valid crawler config"""
        config = CrawlerConfig(
            name="test-crawler",
            type="jobs",
            base_url="https://example.com",
            enabled=True,
            rate_limit=60,
            timeout=30,
            max_pages=10
        )
        
        assert config.name == "test-crawler"
        assert config.type == "jobs"
        assert config.base_url == "https://example.com"
        assert config.enabled is True
    
    def test_config_validation_failure(self):
        """Test config validation failure"""
        with pytest.raises(ValidationError):
            CrawlerConfig(
                name="",  # Empty name
                type="jobs",
                base_url="https://example.com"
            )


class TestAggregator:
    """Test the Aggregator class"""
    
    def test_aggregate_sorting(self):
        """Test that aggregator sorts by freshness"""
        aggregator = Aggregator()
        
        # Create opportunities with different dates
        opp1 = Opportunity(
            id="test-007",
            type="jobs",
            title="Old Job",
            organization="Company A",
            description="Old job",
            location="Location A",
            country="USA",
            reward="$100,000",
            deadline="2026-07-15",
            url="https://example.com",
            tags=["python"],
            source="test",
            date_discovered="2026-01-01",  # Old date
            last_updated="2026-01-01",
            score=50
        )
        
        opp2 = Opportunity(
            id="test-008",
            type="jobs",
            title="New Job",
            organization="Company B",
            description="New job",
            location="Location B",
            country="USA",
            reward="$100,000",
            deadline="2026-07-15",
            url="https://example.com",
            tags=["python"],
            source="test",
            date_discovered="2026-06-18",  # New date
            last_updated="2026-06-18",
            score=50
        )
        
        opportunities = [opp1, opp2]
        aggregated = aggregator.aggregate(opportunities)
        
        # opp2 should come first (newer date)
        assert aggregated[0].date_discovered == "2026-06-18"
        assert aggregated[1].date_discovered == "2026-01-01"


class TestDeduplicator:
    """Test the Deduplicator class"""
    
    def test_deduplicate(self):
        """Test deduplication"""
        deduplicator = Deduplicator()
        
        # Create duplicate opportunities
        opp1 = Opportunity(
            id="test-009",
            type="jobs",
            title="Test Job",
            organization="Test Company",
            description="Test description",
            location="Test Location",
            country="USA",
            reward="$100,000",
            deadline="2026-07-15",
            url="https://example.com",
            tags=["python", "testing"],
            source="test",
            date_discovered="2026-06-18",
            last_updated="2026-06-18",
            score=85
        )
        
        opp2 = Opportunity(
            id="test-010",
            type="jobs",
            title="Test Job",  # Same title
            organization="Test Company",  # Same organization
            description="Test description",
            location="Test Location",
            country="USA",
            reward="$100,000",
            deadline="2026-07-15",  # Same deadline
            url="https://example.com",
            tags=["python", "testing"],
            source="test",
            date_discovered="2026-06-18",
            last_updated="2026-06-18",
            score=85
        )
        
        opp3 = Opportunity(
            id="test-011",
            type="jobs",
            title="Different Job",
            organization="Different Company",
            description="Different description",
            location="Different Location",
            country="USA",
            reward="$150,000",
            deadline="2026-08-01",
            url="https://example.com",
            tags=["javascript", "web"],
            source="test",
            date_discovered="2026-06-18",
            last_updated="2026-06-18",
            score=90
        )
        
        opportunities = [opp1, opp2, opp3]
        deduplicated = deduplicator.deduplicate(opportunities)
        
        # Should have 2 unique opportunities (opp1 and opp3)
        assert len(deduplicated) == 2
        assert any(opp.title == "Test Job" for opp in deduplicated)
        assert any(opp.title == "Different Job" for opp in deduplicated)


class TestStorage:
    """Test the Storage class"""
    
    def setup_method(self):
        """Set up test storage"""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = Storage(self.temp_dir)
    
    def teardown_method(self):
        """Clean up test storage"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_save_and_load_opportunities(self):
        """Test saving and loading opportunities"""
        opportunities = [
            Opportunity(
                id="test-012",
                type="jobs",
                title="Test Job 1",
                organization="Company A",
                description="Test description",
                location="Location A",
                country="USA",
                reward="$100,000",
                deadline="2026-07-15",
                url="https://example.com",
                tags=["python"],
                source="test",
                date_discovered="2026-06-18",
                last_updated="2026-06-18",
                score=85
            ),
            Opportunity(
                id="test-013",
                type="jobs",
                title="Test Job 2",
                organization="Company B",
                description="Test description",
                location="Location B",
                country="USA",
                reward="$150,000",
                deadline="2026-08-01",
                url="https://example.com",
                tags=["javascript"],
                source="test",
                date_discovered="2026-06-18",
                last_updated="2026-06-18",
                score=90
            )
        ]
        
        # Save opportunities
        self.storage.save_opportunities(opportunities, "test")
        
        # Load opportunities
        loaded = self.storage.load_opportunities("test")
        
        assert len(loaded) == 2
        assert loaded[0].title == "Test Job 1"
        assert loaded[1].title == "Test Job 2"
    
    def test_get_history(self):
        """Test getting historical opportunities"""
        opportunities = [
            Opportunity(
                id="test-014",
                type="jobs",
                title="Historical Job",
                organization="Company A",
                description="Test description",
                location="Location A",
                country="USA",
                reward="$100,000",
                deadline="2026-07-15",
                url="https://example.com",
                tags=["python"],
                source="test",
                date_discovered="2026-06-18",
                last_updated="2026-06-18",
                score=85
            )
        ]
        
        # Save historical data
        self.storage.save_opportunities(opportunities, "current")
        
        # Get history (should include current)
        history = self.storage.get_history(90)
        
        assert len(history) == 1
        assert history[0].title == "Historical Job"


class TestAPIGenerator:
    """Test the APIGenerator class"""
    
    def setup_method(self):
        """Set up test API generator"""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = Storage(self.temp_dir)
        self.api_generator = APIGenerator(self.storage)
    
    def teardown_method(self):
        """Clean up test API generator"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_generate_opportunities_api(self):
        """Test generating opportunities API"""
        opportunities = [
            Opportunity(
                id="test-015",
                type="jobs",
                title="Test Job 1",
                organization="Company A",
                description="Test description",
                location="Location A",
                country="USA",
                reward="$100,000",
                deadline="2026-07-15",
                url="https://example.com",
                tags=["python"],
                source="test",
                date_discovered="2026-06-18",
                last_updated="2026-06-18",
                score=85
            ),
            Opportunity(
                id="test-016",
                type="jobs",
                title="Test Job 2",
                organization="Company B",
                description="Test description",
                location="Location B",
                country="USA",
                reward="$150,000",
                deadline="2026-08-01",
                url="https://example.com",
                tags=["javascript"],
                source="test",
                date_discovered="2026-06-18",
                last_updated="2026-06-18",
                score=90
            )
        ]
        
        # Generate API
        self.api_generator.generate_opportunities_api(opportunities)
        
        # Check that files were created
        assert (self.storage.api_dir / "opportunities.json").exists()
        assert (self.storage.api_dir / "jobs.json").exists()
        
        # Load and verify data
        with open(self.storage.api_dir / "opportunities.json", 'r') as f:
            data = json.load(f)
        
        assert len(data) == 2
        assert data[0]["title"] == "Test Job 1"
        assert data[1]["title"] == "Test Job 2"
    
    def test_generate_trending_api(self):
        """Test generating trending API"""
        opportunities = [
            Opportunity(
                id="test-017",
                type="jobs",
                title="Trending Job 1",
                organization="Company A",
                description="Test description",
                location="Location A",
                country="USA",
                reward="$100,000",
                deadline="2026-07-15",
                url="https://example.com",
                tags=["python"],
                source="test",
                date_discovered="2026-06-18",
                last_updated="2026-06-18",
                score=95
            ),
            Opportunity(
                id="test-018",
                type="jobs",
                title="Trending Job 2",
                organization="Company B",
                description="Test description",
                location="Location B",
                country="USA",
                reward="$150,000",
                deadline="2026-08-01",
                url="https://example.com",
                tags=["javascript"],
                source="test",
                date_discovered="2026-06-18",
                last_updated="2026-06-18",
                score=85
            )
        ]
        
        # Generate API
        self.api_generator.generate_trending_api(opportunities)
        
        # Check that file was created
        assert (self.storage.api_dir / "trending.json").exists()
        
        # Load and verify data
        with open(self.storage.api_dir / "trending.json", 'r') as f:
            data = json.load(f)
        
        assert len(data) == 2
        # Should be sorted by trending score
        assert data[0]["score"] == 95
        assert data[1]["score"] == 85
    
    def test_generate_deadlines_api(self):
        """Test generating deadlines API"""
        opportunities = [
            Opportunity(
                id="test-019",
                type="jobs",
                title="Deadline Job 1",
                organization="Company A",
                description="Test description",
                location="Location A",
                country="USA",
                reward="$100,000",
                deadline="2026-06-25",  # 10 days from now
                url="https://example.com",
                tags=["python"],
                source="test",
                date_discovered="2026-06-18",
                last_updated="2026-06-18",
                score=85
            ),
            Opportunity(
                id="test-020",
                type="jobs",
                title="Deadline Job 2",
                organization="Company B",
                description="Test description",
                location="Location B",
                country="USA",
                reward="$150,000",
                deadline="2026-06-20",  # 5 days from now
                url="https://example.com",
                tags=["javascript"],
                source="test",
                date_discovered="2026-06-18",
                last_updated="2026-06-18",
                score=90
            )
        ]
        
        # Generate API
        self.api_generator.generate_deadlines_api(opportunities)
        
        # Check that file was created
        assert (self.storage.api_dir / "deadlines.json").exists()
        
        # Load and verify data
        with open(self.storage.api_dir / "deadlines.json", 'r') as f:
            data = json.load(f)
        
        assert len(data) == 2
        # Should be sorted by days_left (nearest first)
        assert data[0]["days_left"] <= data[1]["days_left"]
    
    def test_generate_search_index(self):
        """Test generating search index API"""
        opportunities = [
            Opportunity(
                id="test-021",
                type="jobs",
                title="Search Job 1",
                organization="Company A",
                description="Test description for search indexing",
                location="Location A",
                country="USA",
                reward="$100,000",
                deadline="2026-07-15",
                url="https://example.com",
                tags=["python", "testing"],
                source="test",
                date_discovered="2026-06-18",
                last_updated="2026-06-18",
                score=85
            )
        ]
        
        # Generate API
        self.api_generator.generate_search_index(opportunities)
        
        # Check that file was created
        assert (self.storage.api_dir / "search-index.json").exists()
        
        # Load and verify data
        with open(self.storage.api_dir / "search-index.json", 'r') as f:
            data = json.load(f)
        
        assert len(data) == 1
        assert data[0]["title"] == "Search Job 1"
        assert data[0]["organization"] == "Company A"
        assert "python" in data[0]["tags"]
        assert "testing" in data[0]["tags"]


class TestIntegration:
    """Integration tests"""
    
    def test_full_pipeline(self):
        """Test the full pipeline"""
        temp_dir = tempfile.mkdtemp()
        
        try:
            storage = Storage(temp_dir)
            api_generator = APIGenerator(storage)
            
            opportunities = [
                Opportunity(
                    id="test-022",
                    type="jobs",
                    title="Integration Test Job",
                    organization="Test Company",
                    description="Test description",
                    location="Test Location",
                    country="USA",
                    reward="$100,000",
                    deadline="2026-07-15",
                    url="https://example.com",
                    tags=["python", "testing"],
                    source="test",
                    date_discovered="2026-06-18",
                    last_updated="2026-06-18",
                    score=85
                )
            ]
            
            # Generate all APIs
            api_generator.generate_opportunities_api(opportunities)
            api_generator.generate_trending_api(opportunities)
            api_generator.generate_deadlines_api(opportunities)
            api_generator.generate_search_index(opportunities)
            
            # Verify all files exist
            assert (storage.api_dir / "opportunities.json").exists()
            assert (storage.api_dir / "trending.json").exists()
            assert (storage.api_dir / "deadlines.json").exists()
            assert (storage.api_dir / "search-index.json").exists()
            assert (storage.api_dir / "jobs.json").exists()
            
            # Verify data is valid JSON
            for endpoint in ["opportunities.json", "trending.json", "deadlines.json", "search-index.json", "jobs.json"]:
                with open(storage.api_dir / endpoint, 'r') as f:
                    data = json.load(f)
                assert isinstance(data, list)
                
        finally:
            import shutil
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])