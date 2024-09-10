from typing import List, Union

from sqlalchemy.engine import Connection
from watch_service.utils.model_utils import obj_to_dict
from watch_service.daos import watch_dao
from watch_service.models.watch import Watch
from watch_service.models.watch_full import WatchFull


def get_watches(conn: Connection) -> dict | None:
    with conn.begin():
        results = watch_dao.get_watches(conn)
        if results:
            return [obj_to_dict(Watch(**result)) for result in results]

    return None


def get_all_watches_full(conn: Connection) -> dict | None:
    with conn.begin():
        results = watch_dao.get_all_watches_full(conn)
        if results:
            return [obj_to_dict(WatchFull(**result)) for result in results]

    return None


def get_watches_full_by_query(conn: Connection, payload: str) -> dict | None:
    payload = {"query": payload}
    with conn.begin():
        results = watch_dao.get_watches_full_by_query(conn, payload)

        if results:
            return [obj_to_dict(WatchFull(**result)) for result in results]

    return None

def upsert_watch_data(conn: Connection, payload: dict):
    with conn.begin():
        watch_dao.upsert_watch_data(conn, payload)