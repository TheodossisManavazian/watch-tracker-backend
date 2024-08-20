from fastapi import APIRouter, HTTPException

from watch_service.services import watch_service
from watch_service import engine

router = APIRouter(prefix="/v1/watches")


@router.get("/")
def get_watches() -> dict:
    with engine.connect() as conn:
        data = watch_service.get_watches(conn)

    if data is None:
        raise HTTPException(status_code=404, detail='No Records Found')
    return {"data": data}


@router.get("/image_mappings")
def get_watch_image_mappings() -> dict:
    with engine.connect() as conn:
        data = watch_service.get_watch_image_mappings(conn)

    if data is None:
        raise HTTPException(status_code=404, detail='No Records Found')
    return {"data": data}


@router.get("/full")
def get_watches_full() -> dict:
    with engine.connect() as conn:
        data = watch_service.get_all_watches_full(conn)

    if data is None:
        raise HTTPException(status_code=404, detail='No Records Found')
    return {"data": data}


@router.get("/full/{query}")
def get_watches_full_ref(query: str) -> dict:
    with engine.connect() as conn:
        data = watch_service.get_watches_full_by_query(conn, query)

    if data is None:
        raise HTTPException(status_code=404, detail='No Records Found')
    return {"data": data}
