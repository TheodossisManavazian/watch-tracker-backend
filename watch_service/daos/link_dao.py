from pandas import Series
from sqlalchemy import text
from sqlalchemy.engine import Connection
from typing import List
from watch_service.utils.db_utils import fetchall


def upsert_link_data(conn: Connection, payload: Series):
    sql = """
        INSERT INTO 
        links(
            reference_number,
            brand,
            links,
            watch_link,
            image_link
        )
        VALUES (:reference_number, :brand, :links, :watch_link, :image_link)
        ON CONFLICT(reference_number, brand)
        DO UPDATE SET
            reference_number = EXCLUDED.reference_number,
            brand = EXCLUDED.brand,
            links = EXCLUDED.links,
            watch_link = EXCLUDED.watch_link,
            image_link = EXCLUDED.image_link
        """
    conn.execute(text(sql), payload)


def get_all_links(conn: Connection) -> List[tuple]:
    sql = """
        SELECT
            reference_number,
            brand,
            links,
            watch_link,
            image_link
        FROM links
    """
    return fetchall(conn, sql)
