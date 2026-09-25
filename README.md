# 🐶 Puppy Monitor

An automated Python website monitoring tool that detects updates to a
puppy reservation page and sends real-time notifications through
Telegram and email.

## How It Works

1. Fetches the puppy reservation webpage.
2. Parses and cleans the page content using BeautifulSoup.
3. Generates a SHA-256 hash of the current page content.
4. Compares the hash with the previous version stored in `last.txt`.
5. If a change is detected, sends:
   - Telegram notification
   - Email notification
6. Saves the new hash for the next monitoring cycle.

## Tech Stack

- Python
- Requests
- BeautifulSoup
- SHA-256 / hashlib
- Telegram Bot API
- SMTP / Gmail
- ScraperAPI
- GitHub Actions

## Features

- Automated website change detection
- SHA-256 based content comparison
- Telegram and email alerts
- Scheduled cloud execution with GitHub Actions
- Environment-variable based secret management
- Handles HTTP 403 responses without generating false alerts
- Optional proxy-based scraping through ScraperAPI

## Project Structure

puppy-monitor/
├── .github/
│   └── workflows/
│       └── run.yml
├── monitor.py
├── last.txt
└── README.md

## Monitoring Workflow

Website
   ↓
Fetch HTML
   ↓
BeautifulSoup
   ↓
Extract Page Text
   ↓
SHA-256 Hash
   ↓
Compare With Previous Hash
   ↓
Change Detected?
   ↓
Telegram + Email Notification
