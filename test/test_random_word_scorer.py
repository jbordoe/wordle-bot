import unittest

from lib.word_scorer.random_word_scorer import RandomWordScorer


class TestRandomWordScorer(unittest.TestCase):
    def setUp(self):
        self.initial_words = ["apple", "banana", "cherry"]
        self.scorer = RandomWordScorer(self.initial_words)

    def test_instantiation(self):
        """
        Tests that the RandomWordScorer can be instantiated correctly.
        """
        self.assertIsInstance(self.scorer, RandomWordScorer)
        self.assertEqual(self.scorer.wordlist, self.initial_words)

    def test_rank_method(self):
        """
        Tests that the rank method returns randomly ordered words.
        """
        words_to_rank = ["acorn", "berry", "carrot", "date"]
        ranked_list = self.scorer.rank(words_to_rank)

        self.assertEqual(set(ranked_list), set(words_to_rank))

    def test_update_method(self):
        """
        Tests that the update method correctly updates the internal wordlist.
        """
        new_words = ["dog", "cat", "mouse"]
        self.scorer.update(new_words)
        self.assertEqual(self.scorer.wordlist, new_words)


if __name__ == "__main__":
    unittest.main()
