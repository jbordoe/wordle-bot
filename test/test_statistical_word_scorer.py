import unittest
from lib.word_scorer.statistical_word_scorer import StatisticalWordScorer

class TestStatisticalWordScorer(unittest.TestCase):

    def setUp(self):
        self.initial_words = ['adder', 'baker', 'class', 'dread', 'eagle', 'feast']
        self.scorer = StatisticalWordScorer(self.initial_words)

    def test_instantiation(self):
        """
        Tests that the StatisticalWordScorer can be instantiated correctly.
        """
        self.assertIsInstance(self.scorer, StatisticalWordScorer)
        self.assertEqual(self.scorer.wordlist, self.initial_words)

    def test_rank_method(self):
        """
        Tests that the rank method returns words ranked by statistical score.
        """
        words_to_rank = ['aaaaa', 'aaaab', 'aaabc', 'aabcd', 'abcde']
        ranked_list = self.scorer.rank(words_to_rank)

        self.assertEqual(ranked_list, ['abcde', 'aabcd', 'aaabc', 'aaaab', 'aaaaa'])

    def test_update_method(self):
        """
        Tests that the update method correctly updates the internal wordlist.
        """
        new_words = ['dog', 'cat', 'mouse']
        self.scorer.update(new_words)
        self.assertEqual(self.scorer.wordlist, new_words)

if __name__ == '__main__':
    unittest.main()
