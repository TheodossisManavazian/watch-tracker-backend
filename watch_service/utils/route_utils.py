from fastapi import HTTPException, Header
import config

def verify_token(authorization: str = Header(None)):
    if authorization != f"Bearer {config.AUTH_TOKEN}":
        raise HTTPException(status_code=403, detail="Invalid token")