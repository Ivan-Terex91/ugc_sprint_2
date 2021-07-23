import logging
from os import getenv

import sentry_sdk
import uvicorn
from api.v1 import bookmark, rating, review
from core import auth, config, mongo
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from logstash import LogstashHandler
from motor.motor_asyncio import AsyncIOMotorClient
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

sentry_sdk.init(
    dsn=config.SENTRY_DSN,
)

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

logger = logging.getLogger("ugc")
logger.addHandler(
    LogstashHandler(
        getenv("LOGSTASH_HOST"), getenv("LOGSTASH_PORT"), version=1, tags=["ugc"]
    )
)
logger.setLevel(logging.INFO)
uvicorn.logger = logger


@app.on_event("startup")
async def startup():
    auth.auth_client = auth.AuthClient(base_url=config.AUTH_URL)
    mongo.mongo_client = AsyncIOMotorClient(config.MONGO_DSN)


@app.on_event("shutdown")
async def shutdown():
    mongo.mongo_client.close()


app.include_router(rating.router, prefix="/api/v1/rating", tags=["ratings"])
app.include_router(review.router, prefix="/api/v1/review", tags=["reviews"])
app.include_router(bookmark.router, prefix="/api/v1/bookmark", tags=["bookmarks"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7777, reload=True, log_config=None)
