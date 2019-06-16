from redis import RedisCommunication


class Log:
    def __init__(self):
        self._redis = RedisCommunication()
        self._key = "log_car"

    def clean_log(self):
        self._redis.delete_values_of_key(self._key)

    def store_object(self, item):
        self._redis.add_value_by_key(self._key, item)

    def get_log(self):
        self._redis.get_values_by_key(self._key)
