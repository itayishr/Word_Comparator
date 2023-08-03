import logging
from celery import Celery
from common import config
from celery import current_app
current_app.conf.CELERY_ALWAYS_EAGER = False

# Configure logging
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Celery and config to integrate with RabbitMQ
celery = Celery()
celery.conf.broker_url = config.CELERY_BROKER_URL



@celery.task(name='fetch_similar_words_task')
def fetch_similar_words_task(word_to_compare):
    # TODO add logic to find similar words and return result
    similar_words = []
    return word_to_compare
