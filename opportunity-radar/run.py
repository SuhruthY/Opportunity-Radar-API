#!/usr/bin/env python3
"""Command-line interface for Opportunity Radar API"""

import asyncio
import logging
import sys
from pathlib import Path

from opportunity_radar.__main__ import OpportunityRadarApp


def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('opportunity_radar.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


async def main():
    setup_logging()
    print("=== Starting Opportunity Radar API ===")
    print("=" * 50)
    app = OpportunityRadarApp()
    await app.run()
    print("=" * 50)
    print("=== Opportunity Radar API completed successfully ===")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)