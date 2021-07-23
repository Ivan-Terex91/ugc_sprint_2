import logging

import logstash
import sentry_sdk
import uvicorn
from api.v1 import bookmark, rating, review
from core import auth, config, mongo
from core.logger import LOGGING
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

sentry_sdk.init(dsn=config.SENTRY_DSN, traces_sample_rate=1.0)

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    auth.auth_client = auth.AuthClient(base_url=config.AUTH_URL)
    mongo.mongo_client = AsyncIOMotorClient(
        config.MONGO_DSN, username=config.MONGO_USER, password=config.MONGO_PASSWORD
    )


@app.on_event("shutdown")
async def shutdown():
    mongo.mongo_client.close()


logger = logging.getLogger("Ugc FastAPI logger")
logger.setLevel(logging.INFO)
logger.addHandler(
    logstash.LogstashHandler(config.LOGSTASH_HOST, int(config.LOGSTASH_PORT), version=1)
)


@app.middleware("http")
async def logging_request(request: Request, call_next):
    response = await call_next(request)
    req_logger = logging.LoggerAdapter(logger=logger, extra={"tag": "ugc"})
    req_logger.info(request)
    return response


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
