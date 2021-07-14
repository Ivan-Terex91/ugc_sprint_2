import logging

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api.v1 import rating, review, movie_bookmark
from core import config
from core.logger import LOGGING

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


app.include_router(rating.router, prefix="/api/v1/rating", tags=["ratings"])
app.include_router(review.router, prefix="/api/v1/review", tags=["reviews"])
app.include_router(movie_bookmark.router, prefix="/api/v1/movie_bookmark", tags=["movie_bookmarks"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=7777,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
