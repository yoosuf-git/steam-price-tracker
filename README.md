
# Steam Game Price Tracker 🎮

A Python web scraper that monitors Steam game prices daily and alerts you when a genuine price drop is detected.

## Features
- Fetches real-time prices from Steam
- Stores historical price data in CSV format
- Compares against highest recorded price to detect genuine discounts
- Runs automatically via Windows Task Scheduler

## Technologies Used
- Python 3.12
- BeautifulSoup4
- Requests
- CSV / DateTime

## How It Works
1. Script fetches the Steam page for tracked games
2. Extracts current price from HTML
3. Saves to CSV with timestamp
4. Compares with highest ever recorded price
5. Prints alert if price has dropped

## Games Currently Tracked
- Crimson Desert
- Red Dead Redemption 2
