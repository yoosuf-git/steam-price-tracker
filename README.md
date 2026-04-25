
# Steam Game Price Tracker 🎮

An AI-powered Python web scraper that monitors Steam game prices 
daily and provides intelligent buying recommendations using Google Gemini AI.

## Features
- Fetches real-time prices from Steam
- Stores historical price data in CSV format
- Compares against highest recorded price to detect genuine discounts
- AI-powered analysis via Google Gemini when price drop detected
- Error handling for network issues
- Runs automatically via Windows Task Scheduler

## Technologies Used
- Python 3.12
- BeautifulSoup4
- Requests
- Google Gemini AI API
- CSV / DateTime

## How It Works
1. Script fetches Steam pages for tracked games
2. Extracts current price from HTML
3. Saves to CSV with timestamp
4. Compares with highest ever recorded price
5. If price dropped — sends data to Gemini AI for analysis
6. Gemini provides buying recommendation

## Games Currently Tracked
- Crimson Desert
- Red Dead Redemption 2
