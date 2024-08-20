from typing import List
from sqlalchemy.engine import Connection

from watch_service.utils.model_utils import obj_to_dict
from watch_service.daos import caliber_dao
from watch_service.models.caliber import Caliber


def get_calibers(conn: Connection) -> List[dict] | None:
    with conn.begin():
        results = caliber_dao.get_all_calibers(conn)
        if results:
            return [obj_to_dict(Caliber(**result)) for result in results]

    return None


def get_caliber(conn: Connection, payload: dict) -> dict | None:
    with conn.begin():
        results = caliber_dao.get_caliber(conn, payload)
        if results:
            return obj_to_dict(Caliber(**results))
        
    return None