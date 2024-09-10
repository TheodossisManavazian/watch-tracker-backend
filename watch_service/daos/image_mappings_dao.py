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
            image_path
        )
        VALUES (:reference_number, :brand, :image_path)
        ON CONFLICT(reference_number, brand)
        DO UPDATE SET
            reference_number = EXCLUDED.reference_number,
            brand = EXCLUDED.brand,
            image_path = EXCLUDED.image_path
        """
    conn.execute(text(sql), payload)


def get_all_image_mappings(conn: Connection) -> List[tuple]:
    sql = """
        SELECT
            reference_number,
            brand,
            image_path
        FROM image_mappings
    """
    return fetchall(conn, sql)

def get_all_image_mappings_by_brand(conn: Connection, payload: dict) -> List[tuple]:
    sql = """
        SELECT
            reference_number,
            brand,
            image_path
        FROM image_mappings
        WHERE brand = :brand
    """
    return fetchall(conn, sql, payload)
