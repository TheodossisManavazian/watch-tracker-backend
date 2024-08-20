from sqlalchemy import text
from sqlalchemy.engine import Connection
from typing import List

from watch_service.utils.db_utils import fetchall


def upsert_listing(conn: Connection, payload: dict):
    sql = """
        INSERT INTO 
        listings(
            hash_id,
            listing_code,
            listing_url,
            reference_number,
            brand,
            model,
            dial,
            year,
            condition,
            accessories,
            location,
            price_usd,
            original_price,
            original_currency,
            exchange_rate
        )
        VALUES (
            :hash_id,
            :listing_code,
            :listing_url,
            :reference_number,
            :brand,
            :model,
            :dial,
            :year,
            :condition,
            :accessories,
            :location,
            :price_usd,
            :original_price,
            :original_currency,
            :exchange_rate
        )
        ON CONFLICT(hash_id)
        DO UPDATE SET
            hash_id = EXCLUDED.hash_id,
            listing_code = EXCLUDED.listing_code,
            listing_url = EXCLUDED.listing_url,
            reference_number = EXCLUDED.reference_number,
            brand = EXCLUDED.brand,
            model = EXCLUDED.model,
            dial = EXCLUDED.dial,
            year = EXCLUDED.year,
            condition = EXCLUDED.condition,
            accessories = EXCLUDED.accessories,
            location = EXCLUDED.location,
            price_usd = EXCLUDED.price_usd,
            original_price = EXCLUDED.original_price,
            original_currency = EXCLUDED.original_currency,
            exchange_rate = EXCLUDED.exchange_rate
        """
    conn.execute(text(sql), payload)


def get_all_listings(conn: Connection) -> List[tuple]:
    sql = """
        SELECT
            hash_id,
            listing_code,
            listing_url,
            reference_number,
            brand,
            model,
            dial,
            year,
            condition,
            accessories,
            location,
            price_usd,
            original_price,
            original_currency,
            exchange_rate,
            updated_at
        FROM listings
    """
    return fetchall(conn, sql)


def get_all_listings_for_reference_number(conn: Connection, payload: dict) -> List[tuple]:
    sql = """
        SELECT
            hash_id,
            listing_code,
            listing_url,
            reference_number,
            brand,
            model,
            dial,
            year,
            condition,
            accessories,
            location,
            price_usd,
            original_price,
            original_currency,
            exchange_rate,
            updated_at
        FROM listings
        WHERE reference_number = :reference_number
    """
    return fetchall(conn, sql, payload)
