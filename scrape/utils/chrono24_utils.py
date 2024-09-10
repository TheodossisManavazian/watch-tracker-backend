import re

from typing import List
from watch_service.utils.model_utils import generate_hash


def scrape_parse_year(year_str: str) -> str:
    if year_str.lower() == "unknown":
        return None
    year = year_str.split(" ")

    return year[0]


# price has a few different formats on a chrono24 listing
def scrape_parse_price(price_str: str) -> List[float]:
    match = re.match(r"([^\d]+)([\d,]+)\s*\(= \$([\d,]+)\)", price_str)
    if match:
        original_currency = match.group(1).strip()
        original_price = float(match.group(2).replace(",", ""))
        price_usd = float(match.group(3).replace(",", ""))
        exchange_rate = price_usd / original_price
        return original_price, original_currency, price_usd, exchange_rate

    match = re.match(r"\$([\d,]+)\s*(\[Negotiable\])?", price_str)
    if match:
        original_currency = "USD"
        original_price = float(match.group(1).replace(",", ""))
        price_usd = original_price
        exchange_rate = 1.0
        return original_price, original_currency, price_usd, exchange_rate

    raise ValueError("Price string format is incorrect")


def map_listing_from_scrape_payload(payload: dict) -> dict:
    og_price, og_currency, price_usd, exchange_rate = scrape_parse_price(
        payload["price"]
    )
    payload["hash_id"] = generate_hash(payload["listing_url"])
    payload["year"] = scrape_parse_year(payload["year"])
    payload["original_price"] = og_price
    payload["original_currency"] = og_currency
    payload["price_usd"] = price_usd
    payload["exchange_rate"] = round(exchange_rate, 6)
    return payload
