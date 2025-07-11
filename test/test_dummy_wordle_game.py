import random
import unittest

from lib.game.dummy_wordle_game import DummyWordleGame
from lib.game.game_constants import GameConstants
from lib.game.game_guess_letter import GameGuessLetter


class TestDummyWordleGame(unittest.TestCase):
    def setUp(self):
        """
        Set up a dummy game with a predictable wordlist and seed.
        """
        self.wordlist = ["APPLE", "BEAST", "CRANE", "DREAM", "EAGLE"]
        random.seed(1)
        self.game = DummyWordleGame(wordlist=self.wordlist)
        self.expected_answer = "BEAST"

    def test_initialization(self):
        """
        Tests that the game is initialized with a word from the wordlist.
        """
        self.assertEqual(self.game.word_length, 5)
        self.assertIn(self.game.answer, self.wordlist)
        self.assertEqual(self.game.answer, self.expected_answer)
        self.assertEqual(self.game.guesses, 0)

    def test_update_with_correct_guess(self):
        """
        Tests that a correct guess returns a correct GameGuessResult.
        """
        result = self.game.update(self.expected_answer)

        self.assertTrue(result.correct)
        self.assertEqual(result.guess, self.expected_answer)
        self.assertEqual(self.game.guesses, 1)

    def test_update_with_incorrect_guess(self):
        """
        Tests that an incorrect guess returns the correct letter states.
        """
        result = self.game.update("CRANE")

        self.assertFalse(result.correct)
        self.assertEqual(result.guess, "CRANE")

        expected_letters = [
            GameGuessLetter(value="C", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="R", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="A", state=GameConstants.LETTER_STATE_PLACED),
            GameGuessLetter(value="N", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="E", state=GameConstants.LETTER_STATE_PRESENT),
        ]
        self.assertEqual(result.letters, expected_letters)
        self.assertEqual(self.game.guesses, 1)

    def test_update_with_duplicate_letters(self):
        """
        Tests that an incorrect guess returns the correct letter states.
        """
        result = self.game.update("SALES")

        self.assertFalse(result.correct)
        self.assertEqual(result.guess, "SALES")

        expected_letters = [
            # Only one S is present
            GameGuessLetter(value="S", state=GameConstants.LETTER_STATE_PRESENT),
            GameGuessLetter(value="A", state=GameConstants.LETTER_STATE_PRESENT),
            GameGuessLetter(value="L", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="E", state=GameConstants.LETTER_STATE_PRESENT),
            # seconf S is absent
            GameGuessLetter(value="S", state=GameConstants.LETTER_STATE_ABSENT)
        ]
        self.assertEqual(result.letters, expected_letters)
        self.assertEqual(self.game.guesses, 1)


if __name__ == "__main__":
    unittest.main()
