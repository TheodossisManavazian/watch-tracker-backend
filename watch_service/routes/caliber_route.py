from fastapi import APIRouter, HTTPException

from watch_service import engine
from watch_service.services import caliber_service

router = APIRouter(prefix="/v1/calibers")


@router.get("/")
def get_caliber() -> dict:
    with engine.connect() as conn:
        calibers = caliber_service.get_calibers(conn)
    
    if calibers:
        return {"data": calibers} 
    
    raise HTTPException(status_code=404, detail="No Records Found")


@router.get("/{brand}/{caliber}")
def get_caliber(brand: str, caliber: str) -> dict:
    payload = {"caliber": caliber, "brand": brand}

    with engine.connect() as conn:
        caliber = caliber_service.get_caliber(conn, payload)
    
    if caliber:
        return {"data": caliber} 

    raise HTTPException(status_code=404, detail="No Records Found")


