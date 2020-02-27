import unittest
import time
from ir_eval.ranking.movie_search import ranked_movie_search

class TestMovieSearch(unittest.TestCase):

    def test_movie_search_basic(self):
        query_params = {'query': ['luke', 'father'], 'movie_title': '', 'year': '', 'actor': ''}
        start = time.time()
        results = ranked_movie_search(query_params, 20)
        end = time.time()
        print("Basic {:.4f} s".format(end-start))
        self.assertIn("tt0080684", results)  # Star Wars V should definitely be within Top 20 results

    def test_movie_search_advanced(self):
        query_params = {'query': ['luke', 'father'], 'movie_title': '', 'year': '1980-1980', 'actor': ''}
        start = time.time()
        results = ranked_movie_search(query_params, 100)
        end = time.time()
        print("Advanced match {:.4f} s".format(end-start))
        self.assertEqual("tt0080684", results[0])  # Star Wars V should definitely be Top 1 result in year 1980

    def test_movie_search_advanced_categories(self):
        query_params = {'query': ['luke', 'father'], 'categories': 'History,Biography'}
        start = time.time()
        results = ranked_movie_search(query_params, 100)
        end = time.time()
        print("Advanced categories match {:.4f} s".format(end - start))
        self.assertNotIn("tt0080684", results)  # Star Wars V should not be among history movies
        self.assertIn("tt0112573", results[:10])  # Braveheart, however, should be among top results

if __name__ == '__main__':
    unittest.main()
