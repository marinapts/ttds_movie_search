from cacheout.lru import LRUCache
from api.utils.singleton import Singleton


@Singleton  # get ResultsCache by calling ResultsCache.instance(). There will be only one instance of ResultsCache.
class ResultsCache:
    def __init__(self):
        self.cache = LRUCache(maxsize=256, ttl=0, default=False)  # if key doesn't exist, cache.get(key) will return False
        # cache will strictly store only key -> dict() pairs.

    def __hash_params(self, query_params):
        return hash(frozenset(query_params.items()))

    def get(self, query_params):
        return self.cache.get(self.__hash_params(query_params))

    def store(self, query_params, output):
        self.cache.add(self.__hash_params(query_params), output)




