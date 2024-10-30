import threading
from datetime import datetime, timedelta

"""
A simple cache implementation should use Redis or other key-value cache systems in practice
"""


class CacheDict:
    def __init__(self, expire_time: timedelta):
        self._cache = {}
        self._expire_time = expire_time
        self._lock = threading.RLock()

    def set(self, key, value):
        expiration_time = datetime.now() + self._expire_time
        with self._lock:
            self._cache[key] = (value, expiration_time)

    def get(self, key, default=None):
        with self._lock:
            if key in self._cache:
                value, expiration_time = self._cache[key]
                if datetime.now() < expiration_time:
                    return value
                else:
                    del self._cache[key]
        return default

    def delete_expired(self):
        with self._lock:
            current_time = datetime.now()
            expired_keys = [key for key, (_, expiration_time) in self._cache.items()
                            if current_time > expiration_time]
            for key in expired_keys:
                del self._cache[key]

    def clear(self):
        with self._lock:
            self._cache.clear()
