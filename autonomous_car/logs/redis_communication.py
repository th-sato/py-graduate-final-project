import redis
import pickle
from env.constants import REDIS_HOST, REDIS_PORT


class RedisCommunication:
    def __init__(self):
        self.connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def add_value_by_key(self, key, value):
        self.connection.sadd(key, value)

    def delete_values_of_key(self, key):
        self.connection.delete(key)

    def get_values_by_key(self, key):
        pickled_value = self.connection.smembers(key)
        if pickled_value is None:
            return None
        return pickle.loads(pickled_value)
