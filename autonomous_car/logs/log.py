from redis_communication import RedisCommunication


class Log:
    def __init__(self):
        self._redis_communication = RedisCommunication()
        self._key = "log_car"

    def clean_log(self):
        self._redis_communication.delete_values_of_key(self._key)

    def store_object(self, item):
        self._redis_communication.add_value_by_key(self._key, item)

    def get_log(self):
        self._redis_communication.get_values_by_key(self._key)
