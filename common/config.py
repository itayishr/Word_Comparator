import os

# Environment variables
REDIS_HOST: str = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT: int = os.environ.get("REDIS_PORT", "6780")
CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER_URL", "amqp://guest:guest@localhost:5674/"
)
