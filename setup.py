from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="opportunity-radar-api",
    version="0.1.0",
    description="Opportunity Radar API - A centralized opportunity discovery platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Opportunity Radar Team",
    author_email="team@opportunityradar.com",
    url="https://github.com/opportunity-radar/opportunity-radar-api",
    packages=find_packages(where="opportunity-radar"),
    package_dir={"": "opportunity-radar"},
    install_requires=[
        "pydantic>=2.4.2",
    ],
    extras_require={
        "scrapy": ["scrapy>=2.8.0"],
        "playwright": ["playwright>=1.40.0"],
        "all": [
            "scrapy>=2.8.0",
            "beautifulsoup4>=4.12.0",
            "playwright>=1.40.0",
            "requests>=2.31.0",
        ],
    },
    classifiers=[
        "Development Status 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)