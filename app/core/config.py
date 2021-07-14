import os

PROJECT_NAME = "User generation content"
MONGO_DSN = os.getenv("MONGO_DSN", None)
AUTH_URL = os.getenv("AUTH_URL", "http://localhost:8001/")
