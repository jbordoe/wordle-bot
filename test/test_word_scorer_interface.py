import unittest

from lib.word_scorer.word_scorer_interface import WordScorerInterface


class TestWordScorerInterface(unittest.TestCase):
    def test_instantiation(self):
        """
        Tests that the WordScorerInterface can be instantiated.
        """
        try:
            WordScorerInterface(wordlist=[])
        except Exception as e:
            self.fail(f"WordScorerInterface instantiation raised an exception: {e}")

    def test_methods_exist(self):
        """
        Tests that the interface has the expected methods.
        """
        interface = WordScorerInterface(wordlist=[])
        # Check that the methods exist and can be called without error
        try:
            interface.rank(words=[])
            interface.update(wordlist=[])
        except Exception as e:
            self.fail(f"Interface method call raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
