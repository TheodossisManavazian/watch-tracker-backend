from fastapi import APIRouter, HTTPException

from watch_service import engine
from watch_service.services import listings_service

router = APIRouter(prefix="/v1/listings")


@router.get("/{reference_number}")
def get_listings(reference_number) -> dict:
    with engine.connect() as conn:
        listings = listings_service.get_all_listings_for_reference_number(
            conn, reference_number
        )

    if listings is not None:
        return {"data": listings}
        
    raise HTTPException(status_code=404, detail='Listings Not Found')
