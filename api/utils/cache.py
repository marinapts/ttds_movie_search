from cacheout.lru import LRUCache
from api.utils.singleton import Singleton
from collections import defaultdict


@Singleton  # get ResultsCache by calling ResultsCache.instance(). There will be only one instance of ResultsCache.
class ResultsCache:
    def __init__(self):
        self.caches = defaultdict(lambda: LRUCache(maxsize=512, ttl=0, default=False))
        # if key doesn't exist, cache.get(key) will return False
        # cache will strictly store only key -> dict() pairs.

        # quote query results take up to 50kB space. 512 cache entries would take approximately 25MB
        # 512 quote results + 512 movie results = up to 50MB of main memory.

    def __hash_params(self, query_params):
        return hash(frozenset(query_params.items()))

    def get(self, query_params, which_cache='quotes'):
        return self.caches[which_cache].get(self.__hash_params(query_params))

    def store(self, query_params, output, which_cache='quotes'):
        self.caches[which_cache].add(self.__hash_params(query_params), output)

    def clear_all(self):
        for k in list(self.caches):
            self.caches[k].clear()
            self.caches.pop(k, False)

