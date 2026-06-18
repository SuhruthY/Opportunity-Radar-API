# Opportunity Radar API

A centralized opportunity discovery platform that continuously collects opportunities from across the internet and exposes them through a free public API.

## Vision

Opportunity Radar API is "Google News for Opportunities" - a platform that helps users discover:

- Jobs
- Freelance Projects
- Hackathons
- Grants
- Startup Accelerators
- Incubators
- Scholarships
- Fellowships
- Competitions
- Open Source Bounties
- Research Funding
- Developer Programs

## Features

- Automatic crawling every 15-20 minutes
- Unified data model for all opportunity types
- Duplicate removal and normalization
- Static JSON API endpoints
- GitHub Pages deployment
- Freshness-first sorting
- Historical snapshots
- Trending opportunities
- Deadline tracking
- Plugin architecture for extensibility

## Tech Stack

- Python
- Scrapy
- BeautifulSoup
- Playwright
- GitHub Actions
- GitHub Pages
- JSON-based static API

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python run.py`
4. The application will automatically crawl sources and generate API endpoints

## Project Structure

```
opportunity-radar/
├── crawlers/
│   ├── jobs/           # Job opportunity crawlers
│   ├── grants/         # Grant opportunity crawlers
│   ├── scholarships/   # Scholarship opportunity crawlers
│   ├── hackathons/     # Hackathon opportunity crawlers
│   ├── competitions/   # Competition opportunity crawlers
│   └── freelance/      # Freelance opportunity crawlers
│
├── normalizers/        # Data normalization and validation
├── aggregation/        # Data aggregation pipeline
├── dedupe/             # Duplicate detection and removal
├── storage/            # Data storage and persistence
├── api/                # API generation and serving
├── data/               # Raw and processed data
├── history/            # Historical snapshots
├── tests/              # Test suite
├── docs/               # Documentation
└── .github/workflows/  # CI/CD workflows
```

## Data Model

Every opportunity is normalized into a unified schema:

```json
{
  "id": "",
  "type": "",
  "title": "",
  "organization": "",
  "description": "",
  "location": "",
  "country": "",
  "reward": "",
  "deadline": "",
  "url": "",
  "tags": [],
  "source": "",
  "date_discovered": "",
  "last_updated": "",
  "score": 0
}
```

## API Endpoints

- `/api/opportunities.json` - All opportunities sorted by freshness (newest first)
- `/api/jobs.json` - Job opportunities only
- `/api/freelance.json` - Freelance opportunities only
- `/api/hackathons.json` - Hackathon opportunities only
- `/api/grants.json` - Grant opportunities only
- `/api/accelerators.json` - Accelerator opportunities only
- `/api/scholarships.json` - Scholarship opportunities only
- `/api/fellowships.json` - Fellowship opportunities only
- `/api/competitions.json` - Competition opportunities only
- `/api/bounties.json` - Bounty opportunities only
- `/api/research-funding.json` - Research funding opportunities only
- `/api/trending.json` - Trending opportunities (top 50)
- `/api/deadlines.json` - Opportunities sorted by nearest deadline
- `/api/search-index.json` - Search index optimized for frontend search

## Development

### Running Tests

```bash
pytest
```

### Running Linting

```bash
ruff check opportunity-radar/
```

### Running Type Checking

```bash
mypy opportunity-radar/
```

### Running Black Formatter

```bash
black opportunity-radar/
```

## GitHub Actions

The project includes a GitHub Actions workflow that:
- Runs every 15 minutes to crawl new opportunities
- Commits updated data
- Deploys to GitHub Pages

## License

MIT
