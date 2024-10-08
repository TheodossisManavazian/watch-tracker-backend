from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import config
import uvicorn


from watch_service.routes import base_route
from watch_service.routes import watch_route
from watch_service.routes import caliber_route 
from watch_service.routes import listings_route
from watch_service.routes import test_route

from watch_service.utils.route_utils import verify_token

app = FastAPI()

origins = [config.FAST_API_ORIGIN, config.REACT_ORIGIN]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_route.router, dependencies=[Depends(verify_token)])
app.include_router(watch_route.router, dependencies=[Depends(verify_token)])
app.include_router(caliber_route.router, dependencies=[Depends(verify_token)])
app.include_router(listings_route.router, dependencies=[Depends(verify_token)])

if config.ENV == "DEV":
    app.include_router(test_route.router, dependencies=[Depends(verify_token)])

if __name__ == "__main__":
    uvicorn.run("application:app", port=8000, log_level="info", reload=True)
