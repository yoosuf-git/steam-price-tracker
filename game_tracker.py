import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
import os
import re

try:
    from google import genai
except ImportError:
    genai = None

def _parse_price_to_cents(price_text):
    cleaned_text = price_text.replace(",", "")
    match = re.search(r"(\d+(?:\.\d{1,2})?)", cleaned_text)
    if not match:
        return None
    return int(round(float(match.group(1)) * 100))


def _extract_price_cents(soup):
    for selector in [
        "div.game_purchase_price.price",
        "div.game_purchase_price",
        "[data-price-final]",
    ]:
        price_element = soup.select_one(selector)
        if not price_element:
            continue
        if price_element.get("data-price-final"):
            return int(price_element["data-price-final"])
        parsed_price = _parse_price_to_cents(price_element.get_text(" ", strip=True))
        if parsed_price is not None:
            return parsed_price

    meta_price = soup.select_one('meta[itemprop="price"]')
    if meta_price and meta_price.get("content"):
        return _parse_price_to_cents(meta_price["content"])

    return None

def get_game_price(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        cookies = {"birthtime": "786239999", "mature_content": "1"}
        response = requests.get(url, headers=headers, cookies=cookies, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        game_name = soup.title.text if soup.title else url
        price = _extract_price_cents(soup)
        if price is None:
            raise ValueError("Could not find a valid game price on the page")
        return game_name, price
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None, None

def save_price(game_name, price):
    try:
        today = date.today()
        with open("prices.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([today, game_name, price])
    except Exception as e:
        print(f"Error saving price: {e}")

def check_price_drop(game_name, current_price):
    try:
        prices = []
        with open("prices.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == game_name:
                    prices.append(int(row[2]))
        if len(prices) == 0:
            print("No previous price found")
            return
        highest_price = max(prices)
        if current_price < highest_price:
            analyse_with_gemini(game_name, current_price, highest_price)
        else:
            print(f"No drop. Current: {current_price} Highest ever: {highest_price}")
    except Exception as e:
        print(f"Error checking price: {e}")

def analyse_with_gemini(game_name, current_price, highest_price):
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("Skipping Gemini analysis: GEMINI_API_KEY not set")
            return
        if genai is None:
            print("Skipping Gemini analysis: google-genai dependency is not installed")
            return
        client = genai.Client(api_key=api_key)
        drop_percentage = round((highest_price - current_price) / highest_price * 100)
        prompt = f"""
        A Steam game price drop has been detected.
        Game: {game_name}
        Highest recorded price: ${highest_price / 100:.2f}
        Current price: ${current_price / 100:.2f}
        Drop percentage: {drop_percentage}%
        
        Give a short 2-3 sentence analysis on whether this is a good time to buy.
        Be conversational and helpful.
        """
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        print(f"\n🎮 PRICE DROP DETECTED!")
        print(f"Game: {game_name}")
        print(f"Was: ${highest_price / 100:.2f} → Now: ${current_price / 100:.2f} ({drop_percentage}% off)")
        print(f"\n🤖 Gemini says: {response.text}")
    except Exception as e:
        print(f"Error with Gemini analysis: {e}")

def main():
    games = [
        "https://store.steampowered.com/app/3321460/Crimson_Desert/",
        "https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/"
    ]

    for url in games:
        game_name, price = get_game_price(url)
        if game_name and price:
            save_price(game_name, price)
            check_price_drop(game_name, price)


if __name__ == "__main__":
    main()
