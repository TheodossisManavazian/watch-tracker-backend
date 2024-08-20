from sqlalchemy import text
from sqlalchemy.engine import Connection

from watch_service.utils.db_utils import fetchall, fetchone


def upsert_caliber_data(conn: Connection, payload: dict):
    sql = """
        INSERT INTO 
        caliber(
            caliber,
            brand,
            movement,
            power_reserve,
            qty_jewels
        )
        VALUES (
            :caliber, 
            :brand, 
            :movement, 
            :power_reserve, 
            :qty_jewels
        )
        ON CONFLICT(caliber, brand)
        DO UPDATE SET
            caliber = COALESCE(EXCLUDED.caliber, caliber.caliber),
            brand = COALESCE(EXCLUDED.brand, caliber.brand),
            movement = COALESCE(EXCLUDED.movement, caliber.movement),
            power_reserve = COALESCE(EXCLUDED.power_reserve, caliber.power_reserve),
            qty_jewels = COALESCE(EXCLUDED.qty_jewels caliber.qty_jewels)
        """
    conn.execute(text(sql), payload)


def get_all_calibers(conn: Connection):
    sql = """
        SELECT
            caliber,
            brand,
            movement,
            power_reserve,
            qty_jewels
        FROM caliber
    """
    return fetchall(conn, sql)


def get_caliber(conn: Connection, payload: dict):
    sql = """
        SELECT
            caliber,
            brand,
            movement,
            power_reserve,
            qty_jewels
        FROM caliber
        WHERE LOWER(brand) = LOWER(:brand) AND caliber = :caliber
    """
    print(payload)
    return fetchone(conn, sql, payload)
