from pandas import Series
from sqlalchemy import text
from sqlalchemy.engine import Connection
from typing import List
from watch_service.utils.db_utils import fetchall


def upsert_image_mappings(conn: Connection, payload: Series):
    sql = """
        INSERT INTO 
        image_mappings(
            reference_number,
            brand,
            image_name
        )
        VALUES (:reference_number, :brand, :image_name)
        ON CONFLICT(reference_number, brand)
        DO UPDATE SET
            reference_number = EXCLUDED.reference_number,
            brand = EXCLUDED.brand,
            image_name = EXCLUDED.image_name
        """
    conn.execute(text(sql), payload)


def get_all_image_mappings(conn: Connection) -> List[tuple]:
    sql = """
        SELECT
            reference_number,
            brand,
            image_name 
        FROM image_mappings
    """
    return fetchall(conn, sql)
