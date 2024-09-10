import sys
import os

root_path = "/".join(os.path.dirname(__file__).split("/")[:-1])
sys.path.append(root_path)

from watch_service.models.watch_full import WatchFull
from watch_service.models.watch import Watch
from watch_service.services import watch_service, listings_service
from watch_service.models.listing import Listing
from watch_service import engine
from typing import List
import json


def _update_watch_price_data(watch: WatchFull, market_price: float) -> dict:
    price_change = percent_change = 0
    retail_price = watch.pricing["retail_price"]

    if not (isinstance(retail_price, str) or retail_price == 0):
        price_change = market_price - retail_price
        percent_change = price_change / retail_price

    watch.pricing = json.dumps(
        {
            "retail_price": watch.pricing["retail_price"],
            "market_price": market_price,
            "price_change": price_change,
            "percent_change": round(percent_change, 3),
        }
    )


def _calculate_market_price(listings: List[Listing]):
    sm = 0
    for listing in listings:
        sm += listing.price_usd

    # might delete later
    return round(sm / len(listings)) // 100 * 100


def update_watch_market_price():
    with engine.connect() as conn:
        watches = watch_service.get_all_watches_full(conn)

        for w in watches:
            watch = WatchFull(**w).watch
            ls = listings_service.get_all_listings_for_reference_number(
                conn, watch.reference_number
            )

            if ls:
                listings = [Listing(**l) for l in ls]
                market_price = _calculate_market_price(listings)
                payload = {
                    "reference_number": watch.reference_number,
                    "brand": watch.brand,
                    "pricing": watch.pricing,
                }
                w = Watch(**payload)
                _update_watch_price_data(w, market_price)
                watch_service.upsert_watch_data(conn, dict(w))


if __name__ == "__main__":
    update_watch_market_price()
