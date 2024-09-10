from fastapi import APIRouter
from watch_service.services import watch_service
from watch_service.services import image_service 
from watch_service import engine
from watch_service.models.watch_image_mapping import WatchImageMapping

import json

router = APIRouter(prefix="/dev")

@router.post("/insert")
def test():
    data = {
        'reference_number': "TEST",
        'brand': "Rolex",
        'years_produced': '2000',
        'description': '',
        'nickname': '',
        'model': 'test',
        'caliber': '4131',
        'image_path': 'test_image.avif',
        'pricing': json.dumps({
            "market_price":217600,
            "price_change":115912,
            "retail_price":101688,
            "percent_change":1.14
        }),
        'case_info': json.dumps({
            "crystal":"Sapphire",
            "case_size":"40mm",
            "case_material":"Oystersteel",
            "water_resistance":"100 meters"
        }),
        'bracelet_info': json.dumps({
            "clasp_type":"Oysterlock",
            "bracelet_color":"Silver",
            "bracelet_material":"Oystersteel"
        }),
        'dial': 'Black'
    }

    with engine.connect() as conn:
        watch_service.upsert_watch_data(conn, data)    
        image_service.upsert_watch_image_mapping(conn, data)


@router.post('/image_mapping/update')
def change_image_path(data: WatchImageMapping):
    with engine.connect() as conn:
        image_service.upsert_watch_image_mapping(conn, dict(data))