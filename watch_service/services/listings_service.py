from typing import List
from sqlalchemy.engine import Connection

from scrape.utils.chrono24_utils import scrape_parse_price, scrape_parse_year, map_listing_from_scrape_payload

from watch_service.utils.model_utils import obj_to_dict
from watch_service.daos import listings_dao
from watch_service.models.listing import Listing



def get_all_listings(conn: Connection) -> List[dict] | None:
    with conn.begin():
        results = listings_dao.get_all_listings(conn)
        if results:
            return [obj_to_dict(Listing.from_db(result)) for result in results]

    return None


def get_all_listings_for_reference_number(conn: Connection, reference_number: str) -> List[dict] | None:
    payload = {"reference_number": reference_number}
    with conn.begin():
        results = listings_dao.get_all_listings_for_reference_number(conn, payload)

        if results:
            return [obj_to_dict(Listing(**result)) for result in results]

        return None


def upsert_listing_from_chrono24_service(conn: Connection, listing: dict) -> List[dict] | None:
    not_inserted = []
    with conn.begin():
        for l in listing["listing_data"]:
            payload = {**l}
            payload["reference_number"] = listing["reference_number"]
            payload = map_listing_from_scrape_payload(payload)
            
            try:
                listings_dao.upsert_listing(conn, dict(Listing(**payload)))
            except Exception:
                not_inserted.append(payload)
    return not_inserted

