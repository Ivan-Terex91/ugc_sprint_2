import os

PROJECT_NAME = "User generated content"
MONGO_DSN = os.getenv("MONGO_DSN", "mongodb://localhost:27017")
MONGO_USER = os.getenv("MONGO_USER", "user")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "pass")
AUTH_URL = os.getenv("AUTH_URL", "http://localhost:8001/")
DB = os.getenv("DB", "ugcDb")
RATING_COLLECTION = os.getenv("RATING_COLLECTION", "movie_ratingCollection")
REVIEW_COLLECTION = os.getenv("REVIEW_COLLECTION", "movie_reviewCollection")
BOOKMARK_COLLECTION = os.getenv("BOOKMARK_COLLECTION", "movie_bookmarkCollection")
SENTRY_DSN = os.getenv(
    "SENTRY_DSN",
    "https://98e564952079451c9edd214ad32c4ac8@o918758.ingest.sentry.io/5862335",
)
LOGSTASH_HOST = os.getenv("LOGSTASH_HOST", "logstash")
LOGSTASH_PORT = os.getenv("LOGSTASH_PORT", 5044)
