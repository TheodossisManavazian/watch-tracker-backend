from typing import List
from sqlalchemy import text
from sqlalchemy.engine import Connection
from watch_service.utils.db_utils import fetchall


def get_watches(conn: Connection) -> List[tuple]:
    sql = """
        SELECT
            reference_number,
            years_produced,
            brand,
            model,
            description,
            pricing,
            case_info,
            dial,
            bracelet_info,
            caliber,
            nickname,
            updated_at
        FROM watch
    """

    return fetchall(conn, sql)


def upsert_watch_data(conn: Connection, payload: dict):
    sql = """
        INSERT INTO 
        watch(
            reference_number,
            years_produced,
            brand,
            model,
            description,
            pricing,
            case_info,
            dial,
            bracelet_info,
            caliber,
            nickname
        )
        VALUES (
            :reference_number,
            :years_produced,
            :brand,
            :model,
            :description,
            :pricing,
            :case_info,
            :dial,
            :bracelet_info,
            :caliber,
            :nickname
        )
        ON CONFLICT(reference_number, brand)
        DO UPDATE SET
            reference_number = COALESCE(EXCLUDED.reference_number, watch.reference_number),
            years_produced = COALESCE(EXCLUDED.years_produced, watch.years_produced),
            brand = COALESCE(EXCLUDED.brand, watch.brand),
            model = COALESCE(EXCLUDED.model, watch.model),
            description = COALESCE(EXCLUDED.description, watch.description),
            pricing = COALESCE(EXCLUDED.pricing, watch.pricing),
            case_info = COALESCE(EXCLUDED.case_info, watch.case_info),
            dial = COALESCE(EXCLUDED.dial, watch.dial),
            bracelet_info = COALESCE(EXCLUDED.bracelet_info, watch.bracelet_info),
            caliber = COALESCE(EXCLUDED.caliber, watch.caliber),
            nickname = COALESCE(EXCLUDED.nickname, watch.nickname)
        """
    conn.execute(text(sql), payload)



# i dont like to do this
def get_all_watches_full(conn: Connection):
    sql = """
        SELECT
            row_to_json(w.*) AS watch,
            row_to_json(i.*) AS image_mapping,
            row_to_json(c.*) AS caliber
        FROM watch w
        JOIN image_mappings i ON w.reference_number = i.reference_number
        JOIN caliber c ON w.caliber = c.caliber
        ORDER BY w.brand, w.model ASC
    """

    return fetchall(conn, sql)


def get_watches_full_by_query(conn: Connection, payload: dict):
    payload = {
        "query": f'%{payload["query"]}%',
    }

    sql = """
        SELECT
            row_to_json(w.*) AS watch,
            row_to_json(i.*) AS image_mapping,
            row_to_json(c.*) AS caliber
        FROM watch w
        JOIN image_mappings i ON w.reference_number = i.reference_number
        JOIN caliber c ON w.caliber = c.caliber
        WHERE UPPER(w.reference_number) LIKE UPPER(:query) OR
        UPPER(w.model) LIKE UPPER(:query) OR
        UPPER(w.brand) LIKE UPPER(:query) OR
        UPPER(w.nickname) LIKE UPPER(:query)
        ORDER BY w.brand, w.model ASC
    """

    return fetchall(conn, sql, payload)
