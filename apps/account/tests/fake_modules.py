from low_level_services.interfaces.cache import AbstractCacheService


class FakeCacheService(AbstractCacheService):
    def __init__(self, prefix):
        self.prefix = prefix
        self.cache = {}

    def get(self, key):
        return self.cache[key]

    def set(self, key, value):
        self.cache[self.prefix + key] = value

    def delete(self, key):
        del self.cache[self.prefix + key]
