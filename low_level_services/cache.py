from .interfaces.cache import AbstractCacheService, CacheNotFound
from django.core.cache import cache


class CacheService(AbstractCacheService):

    def __init__(self, prefix: str):
        self.prefix = prefix

    def get(self, key):
        return cache.get(self.prefix + key)

    def set(self, key, value):
        cache.set(self.prefix + key, value)

    def delete(self, key):
        cache.delete(self.prefix + key)
