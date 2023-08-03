import logging
from celery import Celery
from common import config
from celery import current_app
from redis_connector import RedisConnector

current_app.conf.CELERY_ALWAYS_EAGER = False

# Configure logging
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Celery and config to integrate with RabbitMQ
celery = Celery()
celery.conf.broker_url = config.CELERY_BROKER_URL
redis = RedisConnector()


@celery.task(name="store_words_to_redis")
def store_words_to_redis():
    redis.store_words()
