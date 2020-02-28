import unittest
import time
from ir_eval.ranking.phrase_search import query_phrase_search
from ir_eval.preprocessing import preprocess

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

    def test_phrase_search_force(self):
        # "May the Force be with you." should return some Star Wars quotes in the results.
        query = preprocess("May the Force be with you.")
        self.assertEqual(query, ["may", "forc"])
        query_params = {'query': query, 'movie_title': '', 'year': '', 'actor': ''}
        start = time.time()
        results = query_phrase_search(query_params)
        end = time.time()
        print("May the force be with you. {:.4f} s".format(end - start))
        star_wars_sentence_ids = [
            9603737,   # Star Wars: Episode VI - Return of the Jedi
            50966637,  # Star Wars: Episode VII - The Force Awakens
            14887784,  # Star Wars: Episode I - The Phantom Menace
            14886719,  # Star Wars: Episode I - The Phantom Menace
            14886561,  # Star Wars: Episode I - The Phantom Menace
            14904435,  # Star Wars: Episode III - Revenge of the Sith
            14904433,  # Star Wars: Episode III - Revenge of the Sith
            14903103,  # Star Wars: Episode II - Attack of the Clones
            14903102,  # Star Wars: Episode II - Attack of the Clones
            13503009   # Hackers
        ]
        for id in star_wars_sentence_ids:
            self.assertIn(id, results, f"Sentence _id {id} should be in the results.")

    def test_phrase_search_box_of_chocolates(self):
        query = preprocess("Box of chocolates.")
        query_params = {'query': query}
        start = time.time()
        results = query_phrase_search(query_params)
        end = time.time()
        print(end-start)
        print(results)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
