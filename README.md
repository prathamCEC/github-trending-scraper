# GitHub Trending Scraper

A Python web scraper that collects GitHub Trending repositories and
displays a useful CLI report.

## Features

- Scrapes GitHub Trending
- Extracts repository name and URL
- Extracts programming language
- Extracts total stars
- Extracts stars gained today
- Extracts repository description
- Saves data to CSV
- Dockerized

## Technologies

- Python
- Requests
- BeautifulSoup
- Regex
- CSV
- Docker

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scraper.py
