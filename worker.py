import logging
from celery import Celery
from common import config

# Configure logging
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Celery and config to integrate with RabbitMQ
celery = Celery()
celery.conf.broker_url = config.CELERY_BROKER_URL


@celery.task(name="fetch_similar_words")
def process_crawl_request_task(word_to_compare):
    # TODO add logic to find similar words and return result
    similar_words = []
    return similar_words
