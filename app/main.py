import logging

import uvicorn as uvicorn
from api.v1 import bookmark, rating, review
from core import auth, config, mongo
from core.auth import AuthClient
from core.logger import LOGGING
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    auth.auth_client = AuthClient(base_url=config.AUTH_URL)
    mongo.mongo_client = AsyncIOMotorClient(config.MONGO_DSN)


@app.on_event("shutdown")
async def shutdown():
    mongo.mongo_client.close()


app.include_router(rating.router, prefix="/api/v1/rating", tags=["ratings"])
app.include_router(review.router, prefix="/api/v1/review", tags=["reviews"])
app.include_router(bookmark.router, prefix="/api/v1/bookmark", tags=["bookmarks"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=7777,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
