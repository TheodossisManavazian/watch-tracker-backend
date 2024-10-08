from typing import Union, List
from sqlalchemy.engine import Connection

from watch_service.daos import image_mappings_dao
from watch_service.utils.model_utils import obj_to_dict
from watch_service.models.watch_image_mapping import WatchImageMapping


def get_watch_image_mappings(conn: Connection) -> List[dict] | None:
    with conn.begin():
        results = image_mappings_dao.get_all_image_mappings(conn)
        if results:
            return [obj_to_dict(WatchImageMapping(**result)) for result in results]

    return None


def upsert_watch_image_mapping(conn: Connection, payload: dict) -> None:
    with conn.begin():
        image_mappings_dao.upsert_image_mappings(conn, obj_to_dict(WatchImageMapping(**payload)))