import redis
import json
from common import config
from collections import defaultdict

class RedisConnector:
    """
    A Class which serves as a controller between app and redis db.
    """

    def __init__(self):
        self.redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
        self.pipe = self.redis_client.pipeline()

    def store_words(self):
        """
        :param self:
        :return: Stores words onto redis when key is sorted word and value is a list containing the existing word in the text file.
        """
        redis_result = self.redis_client.get("is_loaded")
        if redis_result is None:
            # A flag indicating that words are already loaded into db.
            self.redis_client.set("is_loaded", 1)
            # Read from text file and bulk insert to redis from a key-value object.
            sorted_words = defaultdict(list)
            with open('words_clean.txt', 'r') as fd:
                for line in fd:
                    for word in line.split():
                        sorted_word = ''.join(sorted(word))
                        sorted_words[sorted_word].append(word)
            for key in sorted_words.keys():
                self.pipe.set(key, json.dumps(sorted_words[key]))
            # Bulk insert to redis.
            set_response = self.pipe.execute()
            print("bulk insert response:", set_response)
