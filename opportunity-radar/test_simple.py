#!/usr/bin/env python3
"""Simple test script to verify the Opportunity Radar API works"""

import json
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, '.')
from opportunity_radar import Opportunity, Aggregator, Deduplicator, Storage, APIGenerator


def test_opportunity_model():
    """Test the Opportunity data model"""
    print("Testing Opportunity model...")

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

    print("OK - Opportunity model works correctly")
    print("    ID:", opportunity.id)
    print("    Title:", opportunity.title)
    print("    Type:", opportunity.type)
    print("    Score:", opportunity.score)
    print("    Freshness:", opportunity.calculate_freshness_score())
    return opportunity


def test_aggregator():
    """Test the Aggregator class"""
    print("\nTesting Aggregator...")

    aggregator = Aggregator()

    opp1 = Opportunity(
        id="test-002", type="jobs", title="Old Job",
        organization="Company A", description="Old job", location="Location A",
        country="USA", reward="$100,000", deadline="2026-07-15",
        url="https://example.com", tags=["python"], source="test",
        date_discovered="2026-01-01", last_updated="2026-01-01", score=50
    )

    opp2 = Opportunity(
        id="test-003", type="jobs", title="New Job",
        organization="Company B", description="New job", location="Location B",
        country="USA", reward="$100,000", deadline="2026-07-15",
        url="https://example.com", tags=["python"], source="test",
        date_discovered="2026-06-18", last_updated="2026-06-18", score=50
    )

    opportunities = [opp1, opp2]
    aggregated = aggregator.aggregate(opportunities)

    assert aggregated[0].date_discovered == "2026-06-18"
    assert aggregated[1].date_discovered == "2026-01-01"

    print("OK - Aggregator works correctly (freshness-first sort)")
    print("    First:", aggregated[0].title, "(", aggregated[0].date_discovered, ")")
    print("    Second:", aggregated[1].title, "(", aggregated[1].date_discovered, ")")
    return aggregated


def test_deduplicator():
    """Test the Deduplicator class"""
    print("\nTesting Deduplicator...")

    deduplicator = Deduplicator()

    opp1 = Opportunity(
        id="test-004", type="jobs", title="Test Job",
        organization="Test Company", description="Test description",
        location="Test Location", country="USA", reward="$100,000",
        deadline="2026-07-15", url="https://example.com",
        tags=["python", "testing"], source="test",
        date_discovered="2026-06-18", last_updated="2026-06-18", score=85
    )

    opp2 = Opportunity(
        id="test-005", type="jobs", title="Test Job",
        organization="Test Company", description="Test description",
        location="Test Location", country="USA", reward="$100,000",
        deadline="2026-07-15", url="https://example.com",
        tags=["python", "testing"], source="test",
        date_discovered="2026-06-18", last_updated="2026-06-18", score=85
    )

    opp3 = Opportunity(
        id="test-006", type="jobs", title="Different Job",
        organization="Different Company", description="Different description",
        location="Different Location", country="USA", reward="$150,000",
        deadline="2026-08-01", url="https://example.com",
        tags=["javascript", "web"], source="test",
        date_discovered="2026-06-18", last_updated="2026-06-18", score=90
    )

    opportunities = [opp1, opp2, opp3]
    deduplicated = deduplicator.deduplicate(opportunities)

    assert len(deduplicated) == 2
    assert any(opp.title == "Test Job" for opp in deduplicated)
    assert any(opp.title == "Different Job" for opp in deduplicated)

    print("OK - Deduplicator works correctly")
    print("    Input: 3 opportunities (2 duplicates)")
    print("    Output:", len(deduplicated), "unique opportunities")
    return deduplicated


def test_storage():
    """Test the Storage class"""
    print("\nTesting Storage...")

    temp_dir = tempfile.mkdtemp()

    try:
        storage = Storage(temp_dir)

        opportunities = [
            Opportunity(
                id="test-007", type="jobs", title="Test Job 1",
                organization="Company A", description="Test description",
                location="Location A", country="USA", reward="$100,000",
                deadline="2026-07-15", url="https://example.com",
                tags=["python"], source="test",
                date_discovered="2026-06-18", last_updated="2026-06-18", score=85
            ),
            Opportunity(
                id="test-008", type="jobs", title="Test Job 2",
                organization="Company B", description="Test description",
                location="Location B", country="USA", reward="$150,000",
                deadline="2026-08-01", url="https://example.com",
                tags=["javascript"], source="test",
                date_discovered="2026-06-18", last_updated="2026-06-18", score=90
            )
        ]

        storage.save_opportunities(opportunities, "test")
        loaded = storage.load_opportunities("test")

        assert len(loaded) == 2
        assert loaded[0].title == "Test Job 1"
        assert loaded[1].title == "Test Job 2"

        print("OK - Storage works correctly")
        print("    Saved and loaded", len(loaded), "opportunities")
        print("    History file:", storage.history_dir / "2026-06-18.json")

    finally:
        shutil.rmtree(temp_dir)


def test_api_generator():
    """Test the APIGenerator class"""
    print("\nTesting APIGenerator...")

    temp_dir = tempfile.mkdtemp()

    try:
        storage = Storage(temp_dir)
        api_generator = APIGenerator(storage)

        opportunities = [
            Opportunity(
                id="test-009", type="jobs", title="API Test Job 1",
                organization="Company A", description="Test description",
                location="Location A", country="USA", reward="$100,000",
                deadline="2026-06-25", url="https://example.com",
                tags=["python"], source="test",
                date_discovered="2026-06-18", last_updated="2026-06-18", score=95
            ),
            Opportunity(
                id="test-010", type="jobs", title="API Test Job 2",
                organization="Company B", description="Test description",
                location="Location B", country="USA", reward="$150,000",
                deadline="2026-06-20", url="https://example.com",
                tags=["javascript"], source="test",
                date_discovered="2026-06-18", last_updated="2026-06-18", score=85
            )
        ]

        api_generator.generate_opportunities_api(opportunities)
        api_generator.generate_trending_api(opportunities)
        api_generator.generate_deadlines_api(opportunities)
        api_generator.generate_search_index(opportunities)

        assert (storage.api_dir / "opportunities.json").exists()
        assert (storage.api_dir / "trending.json").exists()
        assert (storage.api_dir / "deadlines.json").exists()
        assert (storage.api_dir / "search-index.json").exists()
        assert (storage.api_dir / "jobs.json").exists()

        with open(storage.api_dir / "opportunities.json", 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data) == 2
        assert data[0]["title"] == "API Test Job 1"
        assert data[1]["title"] == "API Test Job 2"

        with open(storage.api_dir / "deadlines.json", 'r', encoding='utf-8') as f:
            deadlines = json.load(f)

        print("OK - APIGenerator works correctly")
        print("    Generated endpoints:")
        for f in storage.api_dir.iterdir():
            print("      ", f.name)
        if deadlines:
            print("    Nearest deadline:", deadlines[0]["title"], "(" + str(deadlines[0]["days_left"]) + " days left)")

    finally:
        shutil.rmtree(temp_dir)


def test_validate_opportunity():
    """Test opportunity validation"""
    print("\nTesting Opportunity validation...")

    try:
        Opportunity(
            id="test-invalid", type="jobs", title="Test", organization="Test",
            description="Test", location="Test", country="USA", reward="$100",
            deadline="2026-07-15", url="https://example.com", tags=["test"],
            source="test", date_discovered="invalid", last_updated="2026-06-18", score=85
        )
        print("FAIL - Should have raised ValidationError for invalid date")
        return False
    except Exception as e:
        print("OK - Validation catches invalid dates:", type(e).__name__)
        print("    Error:", str(e)[:80])

    try:
        Opportunity(
            id="test-invalid", type="jobs", title="Test", organization="Test",
            description="Test", location="Test", country="USA", reward="$100",
            deadline="2026-07-15", url="https://example.com", tags=["test"],
            source="test", date_discovered="2026-06-18", last_updated="2026-06-18", score=150
        )
        print("FAIL - Should have raised ValidationError for invalid score")
        return False
    except Exception as e:
        print("OK - Validation catches invalid scores:", type(e).__name__)
        print("    Error:", str(e)[:80])

    return True


def test_duplicate_key_tracking():
    """Test duplicate key generation"""
    print("\nTesting duplicate key generation...")

    opp1 = Opportunity(
        id="test-011", type="jobs", title="Test Job",
        organization="Test Company", description="Test", location="Test",
        country="USA", reward="$100", deadline="2026-07-15",
        url="https://example.com", tags=[], source="test",
        date_discovered="2026-06-18", last_updated="2026-06-18", score=85
    )

    opp2 = Opportunity(
        id="test-012", type="jobs", title="Test Job",
        organization="Test Company", description="Test", location="Test",
        country="USA", reward="$100", deadline="2026-07-15",
        url="https://example.com", tags=[], source="test",
        date_discovered="2026-06-18", last_updated="2026-06-18", score=85
    )

    assert opp1.get_duplicate_key() == opp2.get_duplicate_key()

    print("OK - Duplicate keys match:", opp1.get_duplicate_key()[:16] + "...")
    print("    Same title + organization + deadline -> same hash")


def main():
    """Run all tests"""
    print("=" * 60)
    print("  Testing Opportunity Radar API")
    print("=" * 60)

    passed = 0
    total = 7

    try:
        test_opportunity_model(); passed += 1
        test_aggregator(); passed += 1
        test_deduplicator(); passed += 1
        test_storage(); passed += 1
        test_api_generator(); passed += 1
        if test_validate_opportunity(): passed += 1
        test_duplicate_key_tracking(); passed += 1

        print("\n" + "=" * 60)
        print(f"  Result: {passed}/{total} tests passed")
        print("=" * 60)

    except Exception as e:
        import traceback
        print(f"\nFAIL: {e}")
        traceback.print_exc()
        return 1

    return 0 if passed == total else 1


if __name__ == "__main__":
    exit(main())