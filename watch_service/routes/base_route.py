from fastapi import APIRouter

router = APIRouter(prefix="")


@router.get("/")
@router.get("/ping")
def ping() -> dict:
    return {"data": "pong"}
