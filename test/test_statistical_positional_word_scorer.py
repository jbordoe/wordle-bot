import unittest
from lib.word_scorer.statistical_positional_word_scorer import StatisticalPositionalWordScorer

class TestStatisticalPositionalWordScorer(unittest.TestCase):

    def setUp(self):
        self.initial_words = ['soups', 'shout', 'paler', 'eagle', 'hilly', 'worst', 'grunt', 'burnt', 'older']
        self.scorer = StatisticalPositionalWordScorer(self.initial_words)

    def test_instantiation(self):
        """
        Tests that the StatisticalPositionalWordScorer can be instantiated correctly.
        """
        self.assertIsInstance(self.scorer, StatisticalPositionalWordScorer)
        self.assertEqual(self.scorer.wordlist, self.initial_words)

    def test_rank_method(self):
        """
        Tests that the rank method returns words ranked by statistical score.
        """
        words_to_rank = ['salet', 'noons', 'paler', 'shout', 'zingy']
        ranked_list = self.scorer.rank(words_to_rank)

        self.assertEqual(ranked_list, ['salet', 'shout', 'noons', 'paler', 'zingy'])

    def test_update_method(self):
        """
        Tests that the update method correctly updates the internal wordlist.
        """
        new_words = ['dog', 'cat', 'mouse']
        self.scorer.update(new_words)
        self.assertEqual(self.scorer.wordlist, new_words)

if __name__ == '__main__':
    unittest.main()

