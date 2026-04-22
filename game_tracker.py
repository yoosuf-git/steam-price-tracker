import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

def get_game_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    cookies = {"birthtime": "786239999", "mature_content": "1"}
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, "html.parser")
    game_name = soup.title.text
    price_div = soup.find("div", class_="game_purchase_price price")
    price = int(price_div["data-price-final"])
    return game_name, price

   


def save_price(game_name, price):
    today = date.today()
    with open("prices.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([today, game_name, price])


def check_price_drop(game_name, current_price):
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
        print(f"PRICE DROP ALERT! {game_name} original: {highest_price} now: {current_price}")
    else:
        print(f"No drop. Current: {current_price} Highest ever: {highest_price}")


url = "https://store.steampowered.com/app/3321460/Crimson_Desert/"
game_name, price = get_game_price(url)
save_price(game_name, price)
print(f"Saved: {game_name} - {price}")
check_price_drop(game_name, price)

url="https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/"
game_name, price = get_game_price(url)
save_price(game_name, price)
print(f"Saved: {game_name} - {price}")
check_price_drop(game_name, price)