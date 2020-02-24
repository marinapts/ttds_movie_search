import unittest
import time
from ir_eval.ranking.phrase_search import query_phrase_search

class TestPhraseSearch(unittest.TestCase):

    def test_phrase_search_basic(self):
        query_params = {'query': ['togeth', 'utopia'], 'movie_title': '', 'year': '', 'actor': ''}
        start = time.time()
        results = query_phrase_search(query_params)
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertEqual(results, [258464])

    def test_phrase_search_advanced_year_match(self):
        query_params = {'query': ['togeth', 'utopia'], 'movie_title': '', 'year': '1933-1934', 'actor': ''}
        start = time.time()
        results = query_phrase_search(query_params)
        end = time.time()
        print("Advanced match {:.4f} s".format(end-start))
        self.assertEqual(results, [258464])

    def test_phrase_search_advanced_year_no_match(self):
        query_params = {'query': ['togeth', 'utopia'], 'movie_title': '', 'year': '1995-1996', 'actor': ''}
        start = time.time()
        results = query_phrase_search(query_params)
        end = time.time()
        print("Advanced no match {:.4f} s".format(end - start))
        self.assertEqual(results, [])

if __name__ == '__main__':
    unittest.main()
