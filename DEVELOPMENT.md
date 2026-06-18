# Opportunity Radar API - Development Environment Configuration

This project uses Poetry for dependency management.

## Installation

```bash
pip install poetry
cd opportunity-radar
cpoetry install
```

## Development

```bash
# Run tests
pytest

# Run linting
ruff check

# Run type checking
mypy opportunity-radar/
```

## Project Structure

- `crawlers/` - Web scrapers for different opportunity types
- `normalizers/` - Data normalization and validation
- `aggregation/` - Data aggregation pipeline
- `dedupe/` - Duplicate detection and removal
- `storage/` - Data storage and persistence
- `api/` - API generation and serving
- `data/` - Raw and processed data
- `history/` - Historical snapshots
- `tests/` - Test suite
- `.github/workflows/` - CI/CD workflows
