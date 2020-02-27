import unittest
from db.MongoDB import MongoDB

db = MongoDB()
pipeline = [  # May the force be with us.
    {'$match': {'term': {'$in': ['may', 'forc']}, 'movies._id': 'tt0086190', 'movies.sentences._id': 9603737}}
    # {'$unwind': '$movies'},
    # {'$unwind': '$movies.sentences'},
    # {'$match': {'term': {'$in': ['may', 'forc']}, 'movies._id': 'tt0086190', 'movies.sentences._id': 9603737}}
]

class TestInvertedIndex(unittest.TestCase):

    def test_inverted_index_movies_sorted(self):
        # Ensure that movies in inverted index are sorted
        for index in db.inverted_index.aggregate(pipeline):
            last_movie_id = None
            for movie in index['movies']:
                if last_movie_id is None:
                    last_movie_id = movie['_id']
                self.assertGreaterEqual(movie['_id'], last_movie_id)
                last_movie_id = movie['_id']

    def test_inverted_index_sentences_sorted(self):
        # Ensure that sentences in inverted index are sorted
        for index in db.inverted_index.aggregate(pipeline):
            for movie in index['movies']:
                last_sentence_id = None
                for sentence in movie['sentences']:
                    if last_sentence_id is None:
                        last_sentence_id = sentence['_id']
                    self.assertGreaterEqual(sentence['_id'], last_sentence_id)
                    last_sentence_id = sentence['_id']

    def test_inverted_index_positions_sorted(self):
        # Ensure that sentences in inverted index are sorted
        for index in db.inverted_index.aggregate(pipeline):
            for movie in index['movies']:
                for sentence in movie['sentences']:
                    last_pos = None
                    for pos in sentence['pos']:
                        if last_pos is None:
                            last_pos = pos
                        self.assertGreaterEqual(pos, last_pos)
                        last_pos = pos

if __name__ == '__main__':
    unittest.main()
