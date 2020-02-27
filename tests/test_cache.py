import unittest
from api.utils.cache import ResultsCache

class TestCache(unittest.TestCase):

    def setUp(self) -> None:
        # Clear the cache
        c = ResultsCache.instance()
        c.clear_all()

    def test_cache_singleton(self):
        a = ResultsCache.instance()
        params = {'query': 'hello'}
        output = {'movies': [1, 2]}
        a.store(params, output)

        b = ResultsCache.instance()
        cache_output = b.get(params)
        self.assertDictEqual(cache_output, output)

    def test_cache_hashing(self):
        # Hash of 2 different query_params should be different
        c = ResultsCache.instance()
        params1 = {'query': 'hello'}
        params2 = {'query': 'world'}
        output1 = {'movies': [1, 2]}
        output2 = {'movies': [3, 4]}
        c.store(params1, output1)
        c.store(params2, output2)
        output1 = c.get(params1)
        self.assertTrue(output1)
        output2 = c.get(params2)
        self.assertTrue(output2)
        self.assertNotEqual(output1, output2, 'Outputs from different keys should be different')

    def test_cache_no_hit(self):
        c = ResultsCache.instance()
        c.store({'query': 'world'}, {'movies': [3, 4]})
        missing_output = c.get({'query': 'hello'})
        self.assertFalse(missing_output, 'If no hit, cache.get(key) should return False')

    def test_multi_cache(self):
        c = ResultsCache.instance()
        c1 = 'Name One'
        c2 = 'Name Two'
        params1 = {'query': 'hello'}
        params2 = {'query': 'world'}
        output1 = {'movies': [1, 2]}
        output2 = {'movies': [3, 4]}
        c.store(params1, output1, c1)
        c.store(params2, output2, c2)
        self.assertFalse(c.get(params1, c2), 'Params 1 should not be in Cache 2')
        self.assertFalse(c.get(params2, c1), 'Params 2 should not be in Cache 1')
        self.assertEqual(c.get(params1, c1), output1)
        self.assertEqual(c.get(params2, c2), output2)


if __name__ == '__main__':
    unittest.main()
