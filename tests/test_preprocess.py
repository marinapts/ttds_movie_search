import unittest
from ir_eval.preprocessing import preprocess

class TestPhraseSearch(unittest.TestCase):

    def test_preprocess(self):
        query = preprocess("I am your father.")
        self.assertEqual(query, ["i", "father"])

if __name__ == '__main__':
    unittest.main()
