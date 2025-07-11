import unittest

from lib.game.dummy_wordle_game import DummyWordleGame
from lib.player.nn_player import NNPlayer
from lib.words.word_index import WordIndex


class TestNNPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_wordlist = ["APPLE", "BAKER", "CRANE", "DRIVE", "EAGLE"]
        cls.word_index = WordIndex(cls.test_wordlist)
        cls.dummy_model_path = "test/models/dummy_wordle_guesser.pth"

    def setUp(self):
        self.game_state = DummyWordleGame(self.test_wordlist)
        self.player = NNPlayer(
            self.game_state,
            self.word_index,
            model_path=self.dummy_model_path
        )

    def test_guess_returns_valid_word(self):
        guess = self.player.guess(self.game_state)
        self.assertIsInstance(guess, str)
        self.assertEqual(len(guess), 5)
        self.assertIn(guess.upper(), self.test_wordlist)

if __name__ == '__main__':
    unittest.main()
