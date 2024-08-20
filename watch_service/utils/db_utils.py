from typing import Union, List
from sqlalchemy.engine import Connection
from sqlalchemy import text


def fetchall(conn: Connection, sql: str, payload: dict = None) -> List | None:
    result = conn.execute(text(sql), payload)
    res = result.all()
    if res:
        columns = result.keys()
        return [dict(zip(columns, row)) for row in res]
    return None


def fetchone(conn: Connection, sql: str, payload: dict = None) -> dict | None:
    result = conn.execute(text(sql), payload)
    res = result.first()
    if res:
        columns = result.keys()
        return dict(zip(columns, res))
    return None
