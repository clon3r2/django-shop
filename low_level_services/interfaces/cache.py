import abc


class CacheNotFound(Exception):
    pass


class AbstractCacheService(abc.ABC):

    @abc.abstractmethod
    def set(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError
