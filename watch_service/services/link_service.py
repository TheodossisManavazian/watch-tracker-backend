from typing import List, Union
from sqlalchemy.engine import Connection

from watch_service.utils.model_utils import obj_to_dict
from watch_service.daos import link_dao
from watch_service.models.watch_link import WatchLink


def get_all_links(conn: Connection) -> Union[List[dict], None]:
    with conn.begin():
        results = link_dao.get_all_links(conn)
        if results:
            return [obj_to_dict(WatchLink(**result)) for result in results]

    return None
