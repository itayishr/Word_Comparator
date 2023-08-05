import json
import logging
from collections import defaultdict

import redis

from common import config

AVG_PROCESS_TIME = "avg_process_time"
TOTAL_REQUESTS = "total_requests"
TOTAL_WORDS = "total_words"
IS_LOADED = "is_loaded"

# Configure logging
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


class RedisConnector:
    """
    A Class which serves as a controller between app and redis db.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            logger.info("Initializing redis client.")
            self.redis_client = redis.Redis(
                host=config.REDIS_HOST, port=config.REDIS_PORT
            )
            self.pipe = self.redis_client.pipeline()
            self.initialized = True

    def store_words(self):
        """
        :param self:
        :return: Stores words onto redis when key is sorted word and value is a list containing the existing word in the text file.
        """
        word_count = 0
        redis_result = self.redis_client.get(IS_LOADED)
        if redis_result is None:
            logger.info("Storing words from dictionary to redis")
            # A flag indicating that words are already loaded into db.
            self.redis_client.set(IS_LOADED, 1)
            # Set request number to zero.
            self.redis_client.set(TOTAL_REQUESTS, 0)
            # Set average processing time to zero (no requests yet)
            self.redis_client.set(AVG_PROCESS_TIME, 0)

            # Read from text file and bulk insert to redis from a key-value object.
            sorted_words = defaultdict(list)
            with open("words_clean.txt", "r") as fd:
                for line in fd:
                    for word in line.split():
                        sorted_word = "".join(sorted(word))
                        sorted_words[sorted_word].append(word)
                        word_count += 1
            for key in sorted_words.keys():
                self.pipe.set(key, json.dumps(sorted_words[key]))
            self.redis_client.set(TOTAL_WORDS, word_count)
            # Bulk insert to redis.
            self.pipe.execute()
            logger.info("Words bulk insert to redis finished successfully.")

    def get_word_permutations(self, word_to_compare: str):
        logger.info("Fetching word permutations and updating statistics.")
        sorted_word_to_compare = "".join(sorted(word_to_compare))
        redis_result = self.redis_client.get(sorted_word_to_compare)
        total_requests = self.get_total_requests() + 1
        self.redis_client.set(TOTAL_REQUESTS, str(total_requests))
        return json.loads(redis_result) if redis_result else [word_to_compare]

    def get_word_count(self):
        return int(self.redis_client.get(TOTAL_WORDS))

    def get_total_requests(self):
        return int(self.redis_client.get(TOTAL_REQUESTS))

    def get_average_process_time(self):
        return int(self.redis_client.get(AVG_PROCESS_TIME))

    def update_average_time(self, current_process_time):
        logger.info("Calculating new average time and saving to redis.")
        current_average = self.get_average_process_time()
        total_requests = self.get_total_requests() - 1
        new_average = int(
            (current_average * total_requests + current_process_time)
            / (total_requests + 1)
        )
        self.redis_client.set(AVG_PROCESS_TIME, new_average)
